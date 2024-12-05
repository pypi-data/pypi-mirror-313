`icsystemutils` is a Python package with some low-level utilities for interacting with real system resources (cpu, gpu, network etc).

It is maintained by the Irish Centre for High End Computing (ICHEC), mostly as a dependency of high-level packages and tools used to support ICHEC research and workflows.

# Examples #

Although this is mostly intended to be a library, some example uses to build CLI apps are shown below.

You can read the system CPU info on Linux/Mac via system apis and returns the result as json with:

``` shell
icsystemutils read_cpu
```

You can run a basic resource monitor that outputs CPU and memory use to a file with:


``` shell
icsystemutils monitor
```

You can postprocess a log file with trace info in a specified format with:

``` shell
icsystemutils tracing --trace_file <log_file_with_traces> --trace_config <trace_config_file>
```

The log file should have traces of the format `timestamp | thread_id | message` where the timestamp is Unix time as a float with whole numbers representing seconds. The `message` is used to determine start and end points for events. `The trace_config_file` is a json file used to match strings in the message with Event start and end flags. The output is a series of trace events in json format, which can be used to generate plots with `icplot` or used in further analysis. 

# License #

This project is Copyright of the Irish Centre for High End Computing. You can use it under the terms of the GPLv3+, which further details in the included LICENSE file.
