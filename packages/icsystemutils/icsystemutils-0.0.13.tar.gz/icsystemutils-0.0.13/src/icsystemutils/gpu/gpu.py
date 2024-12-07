from pydantic import BaseModel


class GpuProcessor(BaseModel, frozen=True):

    id: int
