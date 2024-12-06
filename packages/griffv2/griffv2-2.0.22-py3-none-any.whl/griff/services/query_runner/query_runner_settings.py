from pydantic import BaseModel

from griff.utils.pydantic_types import DirectoryStr


class QueryRunnerSettings(BaseModel):
    project_dir: DirectoryStr
    driver: str
