import csv
import typing
from pathlib import Path

from pydantic import BaseModel


class Sample(BaseModel, frozen=True):

    cpu_percent: float = 0.0
    average_memory: float = 0.0
    total_memory: float = 0.0
    sample_time: float = 0.0


def read_csv(path: Path) -> list[Sample]:

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [Sample(**typing.cast(dict, row)) for row in reader]
