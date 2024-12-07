import logging
from typing import Any, Dict, List, Optional

from .api import MbApi

logger = logging.getLogger(__name__)


# Similar to RecentJobInfo
class JobRunDesc:
  id: str
  userFacingId: int
  jobName: str
  state: str
  finishedAtMs: Optional[int] = None
  startedAtMs: Optional[int] = None
  errorMessage: Optional[str]
  successMessage: Optional[str]
  jobOverviewUrl: Optional[str]

  def __init__(self, data: Dict[str, Any]):
    self.id = data["id"]
    self.userFacingId = data["userFacingId"]
    self.jobName = data["jobName"]
    self.state = data["state"]
    if "finishedAtMs" in data:
      self.finishedAtMs = int(data["finishedAtMs"])
    if "startedAtMs" in data:
      self.startedAtMs = int(data["startedAtMs"])
    self.errorMessage = data.get("errorMessage", None)
    self.successMessage = data.get("successMessage", None)
    self.jobOverviewUrl = data.get("jobOverviewUrl", None)

  def __repr__(self) -> str:
    return str(self.__dict__)


class JobApi:
  api: MbApi

  def __init__(self, api: MbApi):
    self.api = api

  def getJobRun(self, jobId: str) -> JobRunDesc:
    resp = self.api.getJsonOrThrow("api/cli/v1/jobs/run_info", dict(jobId=jobId))
    return JobRunDesc(resp["jobRun"])

  def runJob(self,
             branch: str,
             jobName: str,
             refreshDatasets: Optional[List[str]] = None,
             size: Optional[str] = None,
             emailOnFailure: Optional[str] = None,
             timeoutMinutes: Optional[int] = None,
             args: Optional[List[Any]] = None) -> JobRunDesc:
    resp = self.api.getJsonOrThrow(
        "api/cli/v1/jobs/run_job",
        dict(
            branch=branch,
            jobName=jobName,
            args=args,
            refreshDatasets=refreshDatasets,
            size=size,
            emailOnFailure=emailOnFailure,
            timeoutMinutes=timeoutMinutes,
        ))
    return JobRunDesc(resp["jobRun"])
