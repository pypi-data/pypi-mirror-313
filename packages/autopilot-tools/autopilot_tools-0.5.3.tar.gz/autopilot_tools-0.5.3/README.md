[![](https://badge.fury.io/py/autopilot-tools.svg)](https://pypi.org/project/autopilot-tools/) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/build_package.yml/badge.svg) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/pylint.yml/badge.svg) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/tests.yml/badge.svg)

# PX4/ArduPilot Autopilot tools

[autopilot_tools](https://pypi.org/project/autopilot-tools/) is a python package intended to be used as part of automated work with PX4 and ArduPilot autopilots.

## 1. INSTALLATION

The package is distrubuted via [pypi.org/project/autopilot-tools/](https://pypi.org/project/autopilot-tools/).

```bash
pip install autopilot_tools
```

Alternatively, you can install the package from sources in [Development Mode (a.k.a. “Editable Installs”)](https://setuptools.pypa.io/en/latest/userguide/development_mode.html). Clone the repository, install the package in development mode and use it in virtual environment:

```bash
git clone https://github.com/PonomarevDA/autopilot_tools.git
python3 -m venv venv
./venv/bin/activate
pip install -e .
```

## 2. USE CASES

After the installation the package is accessible as a few executables.

## 2.1. Autopilot configurator

Let's say you have an autopilot, but you’re unsure about its current firmware version or configuration. All you want is to upload the exact firmware you need and configure it according to your specifications. This is where `autopilot-configurator` can be extremely helpful. This script:
- uploads the specified PX4 or ArduPilot firmware to the autopilot,
- resets all parameters to default and then applyed the required parameters in the given order,
- performs a force sensor calibration, which is especially useful for HITL simulators.

<img src="https://github.com/PonomarevDA/autopilot_tools/blob/docs/assets/autopilot_configurator.gif?raw=true" width="768">

There are a few ways how to use this feature.

**First way**. Using `--firmware` and `--params` options you can configure the autopilot with desired firmware and/or parameters:

```
autopilot-configurator -v --firmware https://github.com/ZilantRobotics/PX4-Autopilot/releases/download/v1.15.0-0.4.3-beta1/px4_fmu-v6c_cyphal.px4 --params examples/px4_sys_autostart_13000.yaml
```

**Second way**. Using `--force` or `--load` option you can either configure (upload firmware + load parameters) or only load parameters to the target using a singel yaml file:

```bash
cd ~/zilant/uav_hitl_sim # or your path to the simulator
autopilot-configurator -v --force configs/vehicles/px4_v1_15_0_cyphal_quadplane_vtol.yaml
```

**Third way**. You can import the module and perform the configuration manually from your custom python script:

```python
from autopilot_tools.configurator import AutopilotConfigurator

AutopilotConfigurator.configure_with_yaml_file(config_path="path_to_config_file.yaml",
                                               need_upload_firmware=True,
                                               need_load_parameters=True)
```

## 2.2. Test scenario

`test-scenario` uploads the given mission to the autopilot,
run it and wait until it is finished,
then download the log from the vehicle and upload it to [review.px4.io](https://review.px4.io/).
It returns a user the result of the flight and link to the flight report.

<img src="https://github.com/PonomarevDA/autopilot_tools/blob/docs/assets/test_scenario.gif?raw=true" width="768">

You can run this utility as follows:

```bash
test-scenario examples/plan_without_fence.plan --output flight.ulg
```

This will run mission from the `examples` folder.

### 2.3. Using as a module

The package can be imported as a module. This allows you to implement more customized behaviour and use extended features if you need.

An example is shown below:

```python
from autopilot_tools.vehicle import Vehicle
from autopilot_tools.analyzer import Analyzer

vehicle = Vehicle()
vehicle.connect(device="serial")
vehicle.upload_firmware(firmware_path_or_url)
vehicle.configure(params_path)
vehicle.load_mission(mission_path)

res = vehicle.run_mission()
print(res)

log_file = vehicle.load_latest_log(mission_path)

analzyer = Analyzer()
res = analzyer.analyse_log(log_file, analyze_requests=("airspeed", "ice", "esc_status"))
print(res)
```

## 2. DESIGN

The package is primarily based on [ArduPilot/pymavlink](https://github.com/ArduPilot/pymavlink).

<!-- The project structure should be like:

```
src/autopilot-tools/
├── autopilot_tools/
│   ├── firmware.py
│   ├── parameters.py
│   ├── mission.py
│   ├── logs.py
│   ├── stats.py
│   └── cli/
│       ├── __init__.py
│       ├── upload_firmware.py
│       ├── set_parameters.py
│       ├── run_mission.py
│       ├── download_logs.py
│       ├── upload_logs.py
│       ├── parse_logs.py
│       ├── log_stats.py
│       └── overall_stats.py
├── scripts/
│   ├── deploy.sh
│   ├── install.sh
|   └── code_style.py
├── tests/
│   ├── test_firmware.py
│   ├── test_parameters.py
│   ├── test_mission.py
│   ├── test_logs.py
│   └── test_stats.py
├── LICENSE
├── README.md
├── requirements.txt
└── pyproject.toml
``` -->

## 3. Developer guide

A developer should follow the [CONTRIBUTING.md](CONTRIBUTING.md) guide.

**Deployment**.
Please, deploy initially on [test.pypi.org](https://test.pypi.org/project/autopilot-tools/). Only if everything is fine, then deploy on [pypi.org](https://pypi.org/project/autopilot-tools/). Try the script below to get details:

```bash
./deploy.sh --help
```

## 4. LICENSE

The package inherits [ArduPilot/pymavlink](https://github.com/ArduPilot/pymavlink) license and is distributed under GPLv3 license.
