from pydantic import BaseModel

from icsystemutils.cpu import PhysicalProcessor
from icsystemutils.gpu import GpuProcessor


class ComputeNode(BaseModel):

    address: str
    cpus: list[PhysicalProcessor] = []
    gpus: list[GpuProcessor] = []
