from typing import List, Any, cast
from modelbit.api import MbApi, RuntimeApi
from modelbit.ux import printTemplate
from modelbit.error import UserFacingError

MaxTagChars = 50
MaxTagCount = 20


def _assertTagFormat(tags: Any) -> None:
  if type(tags) is not list:
    raise UserFacingError(f"Tags must be a list of strings, but it is a {type(tags)}")
  tags = cast(List[Any], tags)
  if len(tags) > MaxTagCount:
    raise UserFacingError(f"A maximum of {MaxTagCount} is allowed. This request contains {len(tags)}")
  for t in tags:
    if type(t) is not str:
      raise UserFacingError(f"Tags must be strings. One tag is a {type(t)}")
    if len(t) > MaxTagChars:
      raise UserFacingError(
          f"Tags should be fewer than {MaxTagChars} characters. One tag is {len(t)} characters.")


def _assertRuntimeNameFormat(runtimeName: Any) -> None:
  if type(runtimeName) is not str:
    raise UserFacingError(f"The deployment parameter must be a string. It is a {type(runtimeName)}")


def _assertOverwriteFormat(overwrite: Any) -> None:
  if type(overwrite) is not bool:
    raise UserFacingError(f"The overwrite parameter must be a boolean. It is a {type(overwrite)}")


def _assertBranchFormat(branch: Any) -> None:
  if type(branch) is not str:
    raise UserFacingError(f"The branch parameter must be a string. It is a {type(branch)}")


def getDeploymentTags(mbApi: MbApi, branch: str, runtimeName: str) -> List[str]:
  _assertBranchFormat(branch=branch)
  _assertRuntimeNameFormat(runtimeName=runtimeName)
  return RuntimeApi(mbApi).getTags(branch=branch, runtimeName=runtimeName)


def addDeploymentTags(mbApi: MbApi, branch: str, runtimeName: str, tags: List[str], overwrite: bool) -> None:
  _assertBranchFormat(branch=branch)
  _assertRuntimeNameFormat(runtimeName=runtimeName)
  _assertTagFormat(tags=tags)
  _assertOverwriteFormat(overwrite=overwrite)

  if len(tags) == 0 and not overwrite:
    printTemplate("message", None, msgText=f"Set overwrite=True to remove tags.")
    return
  RuntimeApi(mbApi).addTags(branch=branch, runtimeName=runtimeName, tags=tags, overwrite=overwrite)
  msgText = "Tags successfully updated." if len(tags) > 0 else "Tags successfully removed."
  printTemplate("message", None, msgText=msgText)
