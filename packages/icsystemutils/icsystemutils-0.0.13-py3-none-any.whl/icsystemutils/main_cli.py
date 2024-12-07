#!/usr/bin/env python3

import argparse
import logging
import json
from pathlib import Path

from iccore import runtime, logging_utils

from icsystemutils.cpu.cpu_info import CpuInfo
from icsystemutils.monitor import ResourceMonitor, Config, tracing

logger = logging.getLogger(__name__)


def launch_common(args):
    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()


def read_cpu_info(args):
    launch_common(args)

    logger.info("Reading CPU info")

    info = CpuInfo()
    info.read()

    output = json.loads(str(info))
    print(json.dumps(output, indent=4))

    logger.info("Finished Reading CPU info")


def monitor(args) -> None:
    launch_common(args)

    logger.info("Starting monitor")

    output_path: Path | None = None
    if args.output_path:
        output_path = Path(args.output_path)
    stopfile: Path | None = None
    if args.stop_file:
        stopfile = Path(args.stop_file).resolve()

    config = Config(stopfile=stopfile)

    resource_monitor = ResourceMonitor(config, output_path)
    resource_monitor.run()
    logger.info("Finished monitor")


def cli_tracing(args):
    launch_common(args)

    logger.info("Starting processing trace")
    events = tracing.process(args.trace_file.resolve(), args.trace_config.resolve())
    print(events)
    logger.info("Finished processing trace")


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    read_cpu_parser = subparsers.add_parser("read_cpu")
    read_cpu_parser.set_defaults(func=read_cpu_info)

    monitor_parser = subparsers.add_parser("monitor")
    monitor_parser.set_defaults(func=monitor)
    monitor_parser.add_argument(
        "--output_path",
        type=str,
        default="",
        help="Path to an output csv file. Will log to console if empty.",
    )
    monitor_parser.add_argument(
        "--stop_file",
        type=str,
        default="",
        help="Path to a file whose existance causes the monitor to close.",
    )

    tracing_parser = subparsers.add_parser("tracing")
    tracing_parser.add_argument(
        "--trace_file",
        type=Path,
        help="Path to the trace file to load",
    )
    tracing_parser.add_argument(
        "--trace_config",
        type=Path,
        help="Path to the trace config to load",
    )
    tracing_parser.set_defaults(func=cli_tracing)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
