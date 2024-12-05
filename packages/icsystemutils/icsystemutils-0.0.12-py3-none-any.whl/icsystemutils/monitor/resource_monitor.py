import logging
import time
import psutil
from pathlib import Path
from io import TextIOWrapper

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class CpuSample(BaseModel):

    cpu_percent: float = 0.0
    average_memory: float = 0.0
    total_memory: float = 0.0
    sample_time: float = 0.0

    def to_csv(self):
        content = f"{self.sample_time}, {self.cpu_percent}"
        content += f", {self.average_memory}, {self.total_memory}"
        return content

    @staticmethod
    def get_csv_headers():
        return "Time (s), CPU (Percent), Memory Av (MB), Memory Total (MB)"


class ResourceMonitor:

    def __init__(self, output_path: Path | None = None, stop_file: Path | None = None):
        self.target_proc = -1
        self.self_proc = -1
        self.sample_interval = 2000  # ms
        self.sample_duration = 0.0  # s

        self.output_path = output_path
        self.output_handle: TextIOWrapper | None = None
        if output_path:
            self.output_handle = open(output_path, 'w', encoding="utf-8")

        self.stop_file = stop_file

    def write(self, sample: CpuSample | None = None):

        if sample:
            content = sample.to_csv()
        else:
            content = CpuSample.get_csv_headers()

        if self.output_handle:
            self.output_handle.write(content + "\n")
        else:
            print(content + "\n")

    def sample(self):
        memory = psutil.virtual_memory()
        cpu_sample = CpuSample(
            cpu_percent=psutil.cpu_percent(interval=None),
            average_memory=memory.available / 1.0e6,
            total_memory=memory.total / 1.0e6,
            sample_time=time.time(),
        )
        self.write(cpu_sample)

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
                self.sample_duration > 0
                and (self.sample_interval * count) / 1000 >= self.sample_duration
            ):
                break

            if self.stop_file and self.stop_file.exists():
                break
        logger.info("Closing run")
        if self.output_handle:
            self.output_handle.close()
