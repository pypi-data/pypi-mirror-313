from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict

from modelbit.api import MbApi
from modelbit.runtime import Runtime
from modelbit.utils import getFuncName, convertLambdaToDef

if TYPE_CHECKING:
  import pandas


class LambdaWrapper:

  def __init__(self,
               lambdaFunc: Any,
               name: Optional[str] = None,
               python_version: Optional[str] = None,
               python_packages: Optional[List[str]] = None,
               requirements_txt_path: Optional[str] = None,
               system_packages: Optional[List[str]] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional['pandas.DataFrame'] = None,
               common_files: Union[List[str], Dict[str, str], None] = None,
               extra_files: Union[List[str], Dict[str, str], None] = None,
               skip_extra_files_dependencies: bool = False,
               skip_extra_files_discovery: bool = False,
               snowflake_max_rows: Optional[int] = None,
               snowflake_mock_return_value: Optional[Any] = None,
               require_gpu: Union[bool, str] = False,
               setup: Optional[Union[str, List[str]]] = None,
               tags: Optional[List[str]] = None):

    self.lambdaFunc = lambdaFunc
    self.python_version = python_version
    self.python_packages = python_packages
    self.requirements_txt_path = requirements_txt_path
    self.system_packages = system_packages
    self.dataframe_mode = dataframe_mode
    self.example_dataframe = example_dataframe
    self.common_files = common_files
    self.extra_files = extra_files
    self.skip_extra_files_dependencies = skip_extra_files_dependencies
    self.skip_extra_files_discovery = skip_extra_files_discovery
    self.snowflake_max_rows = snowflake_max_rows
    self.snowflake_mock_return_value = snowflake_mock_return_value
    self.require_gpu = require_gpu
    self.name = name if name is not None else getFuncName(self.lambdaFunc, "predict")
    self.setup = setup
    self.tags = tags

  def makeDeployment(self, api: MbApi) -> Runtime:
    deployFunction, funcSource = convertLambdaToDef(self.lambdaFunc, self.name)

    return Runtime(api=api,
                   main_function=deployFunction,
                   source_override=funcSource,
                   python_version=self.python_version,
                   python_packages=self.python_packages,
                   requirements_txt_path=self.requirements_txt_path,
                   system_packages=self.system_packages,
                   name=self.name,
                   dataframe_mode=self.dataframe_mode,
                   example_dataframe=self.example_dataframe,
                   common_files=self.common_files,
                   extra_files=self.extra_files,
                   skip_extra_files_dependencies=self.skip_extra_files_dependencies,
                   skip_extra_files_discovery=self.skip_extra_files_discovery,
                   snowflake_max_rows=self.snowflake_max_rows,
                   snowflake_mock_return_value=self.snowflake_mock_return_value,
                   require_gpu=self.require_gpu,
                   setupNames=self.setup,
                   tags=self.tags)
