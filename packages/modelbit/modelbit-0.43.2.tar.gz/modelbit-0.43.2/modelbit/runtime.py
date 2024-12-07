from typing import Union, List, Dict, Any, Callable, Optional, cast, TYPE_CHECKING, Tuple
import re, json, os, sys

from .environment import ALLOWED_PY_VERSIONS, getInstalledPythonVersion, listMissingPackagesFromImports, systemPackagesForPips, scrubUnwantedPackages, addDependentPackages, annotateSpecialPackages, orderPackages
from .helpers import RuntimePythonProps, getCurrentBranch, getMissingPackageWarningsFromEnvironment, getMissingPackageWarningsFromImportedModules, getProbablyNotAPackageWarnings, warningIfShouldBeUsingDataFrameWarning, mergePipPackageLists, pkgVersion, getVersionProbablyWrongWarnings, assertNoImpossiblePackages, getProbablyWrongRequirementWarning, getSkippedPrivatePackagesNotInMb
from .ux import DifferentPythonVerWarning, GenericError, WarningErrorTip, printTemplate, renderTemplate
from .collect_dependencies import getRuntimePythonProps, getFuncArgNames
from .source_generation import makeSourceFile, DefaultModuleName
from .utils import guessNotebookType, tryPickle, dumpJson
from .error import UserFacingError
from .snowpark import getSnowparkWarnings
import logging

from modelbit.api import DeployedRuntimeDesc, MbApi, RuntimeApi, BranchApi, SecretApi
from modelbit.internal import runtime_objects
from modelbit.internal.metadata import getMetadataWarnings
from modelbit.internal.auth import maybeWarnAboutVersion
from modelbit.setup_manager import selectAndValidateSetups

if TYPE_CHECKING:
  import pandas

logger = logging.getLogger(__name__)


# a bit of a hack for now
def _parseTimeFromDeployMessage(message: Optional[str]) -> Optional[str]:
  if not message:
    return None
  if "will be ready in" in message:
    return message.split("will be ready in")[1]
  return None


class RuntimeStatusNotes:

  def __init__(self, tips: List[WarningErrorTip], warnings: List[WarningErrorTip],
               errors: List[WarningErrorTip]):
    self.tips = tips
    self.warnings = warnings
    self.errors = errors
    self.deployable = len(errors) == 0

  def statusMsg(self) -> str:
    if self.deployable:
      return 'Ready'
    return 'Not Ready'

  def statusStyle(self) -> str:
    if self.deployable:
      return "color:green; font-weight: bold;"
    return "color:gray; font-weight: bold;"


class Runtime:

  def __init__(self,
               api: MbApi,
               name: Optional[str] = None,
               main_function: Optional[Callable[..., Any]] = None,
               python_version: Optional[str] = None,
               python_packages: Optional[List[str]] = None,
               requirements_txt_path: Optional[str] = None,
               system_packages: Optional[List[str]] = None,
               source_override: Optional[str] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional['pandas.DataFrame'] = None,
               common_files: Union[str, List[str], Dict[str, str], None] = None,
               extra_files: Union[str, List[str], Dict[str, str], None] = None,
               skip_extra_files_dependencies: bool = False,
               skip_extra_files_discovery: bool = False,
               snowflake_max_rows: Optional[int] = None,
               snowflake_mock_return_value: Optional[Any] = None,
               isJob: Optional[bool] = False,
               setupNames: Optional[Union[str, List[str]]] = None,
               require_gpu: Union[bool, str] = False,
               tags: Optional[List[str]] = None):

    self._pythonPackages: Optional[List[str]] = None
    self._suppliedRequirementsTxt: Optional[str] = None
    self._systemPackages: Optional[List[str]] = None
    self._deployName: Optional[str] = None
    self._deployFunc: Optional[Callable[..., Any]] = None
    self._sourceOverride = source_override
    self._dataframeMode = dataframe_mode
    self._dataframe_mode_columns: Optional[List[Dict[str, str]]] = None
    self._deploymentInfo: Optional[DeployedRuntimeDesc] = None
    self._tags: Optional[List[str]] = None

    self._require_gpu = 'T4' if require_gpu is True else require_gpu
    self._commonFiles = self.toCommonFilesDict(common_files)
    self._extraFiles = extra_files
    self._ignoreExtraFilesDependencies = skip_extra_files_dependencies
    self._ignoreExtraFileDiscoveries = skip_extra_files_discovery
    self._pythonVersion = getInstalledPythonVersion()
    self._setups = selectAndValidateSetups(setupNames)
    self._isJob = isJob
    self._api = api

    if snowflake_max_rows is not None and (type(snowflake_max_rows) is not int or snowflake_max_rows <= 0):
      raise UserFacingError(f"snowflake_max_rows must be a positive integer.")
    self._snowflakeMaxRows = snowflake_max_rows

    self._snowflakeMockReturnValue = snowflake_mock_return_value

    if name:
      self.setName(name)
    if main_function:
      self.setMainFunction(main_function)
    if python_version:
      self.setPythonVersion(python_version)
    if python_packages is not None:
      if requirements_txt_path is not None:
        raise UserFacingError("Cannot set python_packages= and requirements_txt_path= at the same time.")
      self.setPythonPackages(python_packages)
    if requirements_txt_path is not None:
      self._suppliedRequirementsTxt = self.readRequirementsTxt(requirements_txt_path)
    if system_packages is not None:
      self.setSystemPackages(system_packages)
    self.setDataframeMode(dataframe_mode=dataframe_mode, example_dataframe=example_dataframe)
    self.setTags(tags)

  def _repr_html_(self) -> str:
    return self.__repr__()

  def __repr__(self) -> str:
    if self._deployName is None:
      return ""
    elif self._deploymentInfo is None:
      return renderTemplate("deployment", name=self._deployName, version=None)
    else:
      return renderTemplate("deployment", name=self._deployName, version=self._deploymentInfo.version)

  def setDataframeMode(self, dataframe_mode: bool, example_dataframe: Optional['pandas.DataFrame']) -> None:
    if not dataframe_mode:
      if example_dataframe is not None:
        raise UserFacingError(
            "Setting dataframe_mode=True is required when passing the example_dataframe parameter")
      else:
        return
    elif example_dataframe is None:
      raise UserFacingError("The example_dataframe parameter is required when passing dataframe_mode=True")
    elif len(getFuncArgNames(self._deployFunc)) != 1:
      raise UserFacingError("Deployments using DataFrame Mode can only have one argument.")
    else:
      self._dataframeMode = True
      self._dataframe_mode_columns = self.collectDataFrameModeColumns(example_dataframe)

  def setName(self, name: str) -> None:
    if not re.match('^[a-zA-Z0-9_]+$', name):
      raise UserFacingError("Names should be alphanumeric with underscores.")
    self._deployName = name

  def setPythonVersion(self, version: str) -> None:
    if version not in ALLOWED_PY_VERSIONS:
      return self.selfError(f'Python version should be one of {ALLOWED_PY_VERSIONS}.')
    self._pythonVersion = version

  def setPythonPackages(self, packages: Optional[List[str]]) -> None:
    if packages is None:
      self._pythonPackages = None
      return
    if type(packages) != list:
      raise UserFacingError("The python_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise UserFacingError("The python_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise UserFacingError("The python_packages parameters cannot contain newlines")
      if "==" not in pkg and not pkg.startswith("https") and not pkg.startswith("git+https"):
        raise UserFacingError(
            f"The python_packages parameter '{pkg}' is formatted incorrectly. It should look like 'package-name==X.Y.Z'"
        )
      if pkg.startswith("sklearn=="):
        raise UserFacingError("The 'sklearn' package is deprecated. Use 'scikit-learn'.")
    self._pythonPackages = packages

  def readRequirementsTxt(self, path: str) -> str:
    if not os.path.exists(path):
      raise UserFacingError(f"requirements.txt file not found: {path}")
    try:
      with open(path, "r") as f:
        return f.read()
    except UnicodeDecodeError:
      raise UserFacingError(f"Unexpected binary file used for requirements.txt: {path}")

  def setSystemPackages(self, packages: Optional[List[str]]) -> None:
    if packages is None:
      self._systemPackages = None
      return
    if type(packages) != list:
      raise UserFacingError("The system_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise UserFacingError("The system_packages parameters must be a list of strings.")
      if not re.match("^[a-z0-9.+-]+$", pkg):
        # https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-source
        raise UserFacingError(
            f"Names of system_packages must consist only of lower case letters, numbers, plus, minus, and periods. This package is invalid: {pkg}"
        )
      if "\n" in pkg or "\r" in pkg:
        raise UserFacingError("The system_packages parameters cannot contain newlines.")
    self._systemPackages = sorted(packages)

  def setMainFunction(self, func: Callable[..., Any]) -> None:
    self._deployFunc = func
    if callable(func) and self._deployName == None:
      self.setName(func.__name__)

  def setTags(self, tags: Optional[List[str]]) -> None:
    if tags is None:
      return
    if type(tags) is not list:
      raise UserFacingError("Tags must be a list of strings")
    for t in tags:
      if type(t) is not str:
        raise UserFacingError("Tags must be a list of strings")
    self._tags = sorted(tags)

  def getRequirementsTxt(self) -> Optional[str]:
    if self._pythonPackages:
      packages = "\n".join(orderPackages(self._pythonPackages))
      if "jax[" in packages:
        packages = "--find-links=https://storage.googleapis.com/jax-releases/jax_cuda_releases.html\n" + packages
      if "torch==" in packages or "torchvision==" in packages:
        packages = "--extra-index-url=https://download.pytorch.org/whl/\n" + packages
      if "llama_cpp_python==" in packages:
        packages = "--extra-index-url=https://abetlen.github.io/llama-cpp-python/whl/cu122/\n" + packages
      return packages
    elif self._suppliedRequirementsTxt:
      return self._suppliedRequirementsTxt
    else:
      return None

  def getRuntimePythonProps(self) -> Tuple[Optional[RuntimePythonProps], Optional[GenericError]]:
    props: Optional[RuntimePythonProps] = None
    error: Optional[GenericError] = None

    try:
      localExtraFiles: Optional[List[str]] = list(runtime_objects.expandDirs(self._extraFiles).keys())
      if self._ignoreExtraFilesDependencies:
        localExtraFiles = None
      props = getRuntimePythonProps(self._deployFunc,
                                    sourceOverride=self._sourceOverride,
                                    extraFiles=localExtraFiles,
                                    dataframeMode=self._dataframeMode,
                                    setups=self._setups)
      if props and props.namespaceModules:
        assertNoImpossiblePackages(props.namespaceModules)
    except TypeError:
      raise
    except Exception as err:
      error = GenericError(str(err))
    return props, error

  def makeCreateRuntimeRequest(self, rtProps: RuntimePythonProps) -> Dict[str, Any]:
    integrationEnvVars = SecretApi(self._api).listIntegrationEnvVars()
    sourceFile = makeSourceFile(
        pyProps=rtProps,
        sourceFileName=DefaultModuleName,
        isJob=self._isJob,
        integrationEnvVars=integrationEnvVars).asDict() if self._deployFunc is not None else None

    dataFiles = self.makeAndUploadDataFiles(rtProps)

    createRuntimeRequest: Dict[str, Any] = {
        "name": self._deployName,
        "dataFiles": dataFiles,
        "commonFiles": self._commonFiles,
        "pyState": {
            "sourceFile": sourceFile,
            "valueFiles": {},
            "name": rtProps.name,
            "module": DefaultModuleName,
            "argNames": rtProps.argNames,
            "argTypes": rtProps.argTypes,
            "requirementsTxt": self.getRequirementsTxt(),
            "pythonVersion": self._pythonVersion,
            "systemPackages": self._systemPackages,
            "dataframeModeColumns": self._dataframe_mode_columns,
            "snowflakeMaxRows": self._snowflakeMaxRows,
            "snowflakeMockReturnValue": self._snowflakeMockReturnValue,
        },
        "source": {
            "os": sys.platform,
            "kind": guessNotebookType(),
            "version": pkgVersion
        },
        "tags": self._tags
    }
    if self._require_gpu:
      createRuntimeRequest['pyState']['capabilities'] = [f'gpu={self._require_gpu}']
    if len(dumpJson(createRuntimeRequest)) > 5_000_000:
      raise UserFacingError("Request size exceeds maximum allowed (5MB).")
    return createRuntimeRequest

  def deploy(self) -> None:
    maybeWarnAboutVersion()
    rtProps, error = self.getRuntimePythonProps()
    self.decideAllPackages(rtProps, error)

    if error is not None:
      printTemplate("error", None, errorText=error.errorText)
      return None
    if rtProps is None:
      printTemplate("error", None, errorText="Unable to continue because errors are present.")
      return None

    if self._snowflakeMockReturnValue is not None and rtProps.argTypes is not None and "return" in rtProps.argTypes:
      func_return_type = rtProps.argTypes['return']
      mock_return_type = type(self._snowflakeMockReturnValue).__name__
      if func_return_type != mock_return_type:
        raise UserFacingError(
            f"Type of snowflake_mock_return_value ({mock_return_type}) does not match function return type ({func_return_type})."
        )

    status = self.getStatusNotes(rtProps, error)
    if not status.deployable:
      logger.info("Unable to deploy: %s", status.errors)
      printTemplate("runtime-notes",
                    None,
                    deploymentName=self._deployName,
                    warningsList=status.warnings,
                    tipsList=status.tips,
                    errorsList=status.errors)
      return None

    printTemplate(f"runtime-deploying",
                  None,
                  deployName=self._deployName,
                  warningsList=status.warnings,
                  tipsList=status.tips,
                  errorsList=status.errors)

    BranchApi(self._api).raiseIfProtected()
    createRuntimeRequest = self.makeCreateRuntimeRequest(rtProps)

    if self._isJob:
      resp = RuntimeApi(self._api).createTrainingJob(getCurrentBranch(), createRuntimeRequest)
    else:
      resp = RuntimeApi(self._api).createRuntime(getCurrentBranch(), createRuntimeRequest)
    self._deploymentInfo = resp
    printTemplate(f"runtime-deployed",
                  None,
                  deployKind="Training job" if self._isJob else "Deployment",
                  deployName=self._deployName,
                  deployMessage=resp.message,
                  deployTimeWords=_parseTimeFromDeployMessage(resp.message),
                  runtimeOverviewUrl=resp.runtimeOverviewUrl)
    return None

  def makeAndUploadDataFiles(self, pyState: RuntimePythonProps) -> Dict[str, str]:
    dataFiles: Dict[str, str] = {}
    if pyState.namespaceVars:
      for nName, nVal in pyState.namespaceVars.items():
        uploadResult = runtime_objects.describeAndUploadRuntimeObject(self._api, nVal, tryPickle(nVal, nName),
                                                                      nName)
        if uploadResult:
          dataFiles[f"data/{nName.lower()}.pkl"] = uploadResult
    if pyState.extraDataFiles is not None:
      for nName, nObjBytes in pyState.extraDataFiles.items():
        uploadResult = runtime_objects.describeAndUploadRuntimeObject(self._api, nObjBytes[0], nObjBytes[1],
                                                                      nName)
        if uploadResult:
          dataFiles[nName] = uploadResult
    if pyState.extraSourceFiles:
      dataFiles.update(pyState.extraSourceFiles)
    if pyState.discoveredExtraFiles and not self._ignoreExtraFileDiscoveries:
      dataFiles.update(pyState.discoveredExtraFiles)
    if pyState.discoveredExtraDirs and not self._ignoreExtraFileDiscoveries:
      dataFiles.update(runtime_objects.prepareFileList(self._api, list(pyState.discoveredExtraDirs.keys())))
    dataFiles.update(runtime_objects.prepareFileList(self._api, self._extraFiles))
    if pyState.job is not None:
      dataFiles.update(self.makeAndUploadDataFiles(pyState.job.rtProps))
    return dataFiles

  def toCommonFilesDict(self, files: Union[str, List[str], Dict[str, str], None]) -> Dict[str, str]:
    if files is None:
      return {}

    if type(files) is not list and type(files) is not dict and type(files) is not str:
      raise UserFacingError(f"The common_files parameter must be a list or dict. It is a {type(files)}.")

    if isinstance(files, str):
      return {files: files}

    if isinstance(files, List):
      return {path: path for path in files}

    return files

  def selfError(self, txt: str) -> None:
    printTemplate("error", None, errorText=txt)
    return None

  def decideAllPackages(self, rtPyProps: Optional[RuntimePythonProps],
                        propError: Optional[GenericError]) -> None:
    if propError is not None or rtPyProps is None or self._suppliedRequirementsTxt is not None:
      return
    missingModules = listMissingPackagesFromImports(rtPyProps.namespaceModules, self._pythonPackages)
    missingPips = list(set([m[1] for m in missingModules]))
    mergedPackageList = mergePipPackageLists(self._pythonPackages or [], sorted(missingPips))
    mergedPackageList = addDependentPackages(mergedPackageList)
    mergedPackageList = scrubUnwantedPackages(mergedPackageList)
    mergedPackageList = annotateSpecialPackages(mergedPackageList)
    self.setPythonPackages(mergedPackageList)
    self.setSystemPackages(systemPackagesForPips(self._pythonPackages, self._systemPackages))

  def getStatusNotes(self, rtPyProps: Optional[RuntimePythonProps],
                     propError: Optional[GenericError]) -> RuntimeStatusNotes:
    tips: List[WarningErrorTip] = []
    warnings: List[WarningErrorTip] = []
    errors: List[WarningErrorTip] = []

    # Errors
    if not self._deployName:
      errors.append(GenericError("This deployment needs a name."))
    if propError is not None:
      errors.append(propError)
    if not self._api.isAuthenticated():
      errors.append(GenericError("You are not logged in to Modelbit. Please log in, then deploy."))

    # Warnings
    if rtPyProps is not None and self._suppliedRequirementsTxt is None:
      warnings += getMissingPackageWarningsFromImportedModules(rtPyProps.namespaceModules,
                                                               self._pythonPackages)
      # can re-enable once we also look in common files
      # warnings += getMissingLocalFileWarningsFromImportedModules(rtPyProps.namespaceModules, self._extraFiles)
      warnings += getProbablyNotAPackageWarnings(self._pythonPackages)
      warnings += getSkippedPrivatePackagesNotInMb(rtPyProps.namespaceModules)
      if not self._isJob and not self._dataframeMode:
        warnings += warningIfShouldBeUsingDataFrameWarning(rtPyProps.argNames, rtPyProps.argTypes)
      warnings += getVersionProbablyWrongWarnings(self._pythonPackages)
      warnings += getProbablyWrongRequirementWarning(self._pythonPackages)
    warnings += getMissingPackageWarningsFromEnvironment(self._pythonPackages)
    if not self._isJob:
      warnings += getSnowparkWarnings(self._api, self._pythonVersion, self._pythonPackages)
    if not self._isJob and rtPyProps is not None and rtPyProps.name is not None:
      warnings += getMetadataWarnings(self._api,
                                      branch=getCurrentBranch(),
                                      deploymentName=rtPyProps.name,
                                      snowflakeMockReturnValue=self._snowflakeMockReturnValue)

    localPyVersion = getInstalledPythonVersion()
    if self._pythonVersion != localPyVersion:
      warnings.append(DifferentPythonVerWarning(self._pythonVersion, localPyVersion))

    return RuntimeStatusNotes(tips, warnings, errors)

  def collectDataFrameModeColumns(self, df: 'pandas.DataFrame') -> List[Dict[str, Union[str, Any]]]:

    def shorten(value: Any) -> Union[str, Any]:
      if type(value) is str:
        return value[0:50]
      else:
        return value

    if len(getFuncArgNames(self._deployFunc)) != 1:
      raise UserFacingError(
          "When using dataframe_mode, the deploy function can only have one input argument.")
    config: List[Dict[str, Any]] = []
    examples: Optional[Dict[str, Any]] = None
    if len(df) > 0:
      examples = cast(Dict[str, Any], json.loads(df.head(1).to_json(orient="records"))[0])  # type: ignore
    for col in cast(List[str], list(df.columns)):  # type: ignore
      cf = {"name": col, "dtype": str(df[col].dtype)}
      if examples is not None:
        cf["example"] = shorten(examples[col])
      config.append(cf)
    return config


def add_objects(api: MbApi, deployment: str, values: Dict[str, Any]) -> None:
  """add_object takes the name of a deployment and map of object names to objects.
  These objects will be pickled and stored in `data/object.pkl`
  and can be read using modelbit.load_value('data/object.pkl).
  """
  dataFiles: Dict[str, str] = {}
  for [name, val] in values.items():
    uploadResult = runtime_objects.describeAndUploadRuntimeObject(api, val, tryPickle(val, name), name)
    if uploadResult:
      dataFiles[f"data/{name}.pkl"] = uploadResult
  return _changeFilesAndDeploy(api, deployment, dataFiles)


def add_files(api: MbApi,
              deployment: str,
              files: Union[str, List[str], Dict[str, str]],
              modelbit_file_prefix: Optional[str] = None,
              strip_input_path: Optional[bool] = False) -> None:
  """ add_files takes the name of a deployment and either a list of files or
  a dict of local paths to deployment paths.
  modelbit_file_prefix is an optional folder prefix added to all files when uploaded. For example (deployment="score", files=['myModel.pkl'], modelbit_file_prefix="data")
  would upload myModel.pkl in the current directory to data/myModel.pkl in the deployment named score.
  """

  BranchApi(api).raiseIfProtected()

  dataFiles = runtime_objects.prepareFileList(api,
                                              files,
                                              modelbit_file_prefix=modelbit_file_prefix,
                                              strip_input_path=strip_input_path)
  if len(files) == 0:
    raise UserFacingError("At least one file is required, but the list of files is empty.")
  if len(dumpJson(dataFiles)) > 5_000_000:
    raise UserFacingError("Total file size exceeds maximum allowed (5MB). Use git or add fewer files.")
  return _changeFilesAndDeploy(api, deployment, dataFiles)


def _changeFilesAndDeploy(api: MbApi, deployment: str, dataFiles: Dict[str, str]) -> None:
  resp = RuntimeApi(api).updateRuntime(getCurrentBranch(), deployment, dataFiles)

  printTemplate(f"runtime-deployed",
                None,
                deploymentName=deployment,
                deployMessage=resp.message,
                deployTimeWords=_parseTimeFromDeployMessage(resp.message),
                runtimeOverviewUrl=resp.runtimeOverviewUrl)
  return None


def copy_deployment(api: MbApi, fromBranch: str, toBranch: str, runtimeName: str,
                    runtimeVersion: Union[str, int]) -> None:
  resp = RuntimeApi(api).copyRuntime(fromBranch=fromBranch,
                                     toBranch=toBranch,
                                     runtimeName=runtimeName,
                                     runtimeVersion=runtimeVersion)
  printTemplate(f"runtime-deployed",
                None,
                deploymentName=runtimeName,
                deployMessage=None,
                deployTimeWords="a few seconds",
                runtimeOverviewUrl=resp.runtimeOverviewUrl)
