from pydantic import BaseModel

from icsystemutils.cpu import PhysicalProcessor
from icsystemutils.gpu import GpuProcessor


class ComputeNode(BaseModel, frozen=True):

    address: str
    cpus: list[PhysicalProcessor] = []
    gpus: list[GpuProcessor] = []
