import logging
import csv
import time
from pathlib import Path
from io import TextIOWrapper

import psutil
from pydantic import BaseModel

from iccore.serialization import csv_utils

from .sample import Sample

logger = logging.getLogger(__name__)


class Config(BaseModel, frozen=True):
    target_proc: int = -1
    self_proc: int = -1
    sample_interval: int = 2000  # ms
    sample_duration: float = 0.0  # s
    stopfile: Path | None = None


class ResourceMonitor:

    def __init__(self, config: Config = Config(), output_path: Path | None = None):
        self.output_path = output_path
        self.output_handle: TextIOWrapper | None = None
        self.writer: csv.DictWriter | None = None
        if output_path:
            self.output_handle = open(output_path, "w", encoding="utf-8")
            self.writer = csv.DictWriter(
                self.output_handle, fieldnames=csv_utils.get_fieldnames(Sample)
            )

    def write(self, sample: Sample | None = None):
        if self.writer:
            if not sample:
                self.writer.writeheader()
            else:
                self.writer.writerow(sample.model_dump())
        else:
            if not sample:
                print(csv_utils.get_header_str(Sample) + "\n")
            else:
                print(csv_utils.get_line(sample) + "\n")

    def sample(self):
        memory = psutil.virtual_memory()
        sample = Sample(
            cpu_percent=psutil.cpu_percent(interval=None),
            average_memory=memory.available / 1.0e6,
            total_memory=memory.total / 1.0e6,
            sample_time=time.time(),
        )
        self.write(sample)

    def before_sampling(self):
        # Need to take a first 'dummy' sample before getting real data
        psutil.cpu_percent(interval=None)
        self.write()

    def run(self):
        count = 0
        self.before_sampling()
        while True:
            self.sample()
            time.sleep(self.sample_interval / 1000)
            count += 1
            if (
                self.config.sample_duration > 0
                and (self.config.sample_interval * count) / 1000
                >= self.config.sample_duration
            ):
                break

            if self.config.stopfile and self.config.stopfile.exists():
                break
        logger.info("Closing run")
        if self.output_handle:
            self.output_handle.close()
