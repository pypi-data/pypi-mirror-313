```markdown
# aiotica

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Overview

`aiotica` is a gateway programming library designed for the KASO IoT platform. This library provides various modules to handle event reception, access control, sensor data processing, and more, facilitating seamless interaction with IoT devices and services.

## Features

- Event reception and handling
- IoT access control
- MQTT messaging support
- AWS Greengrass integration
- Sensor data processing
- API service configuration

## Installation

You can install the `aiotica` library using `pip`:

```sh
pip install aiotica
```

## Usage

### Setting Up Your Environment

#### Create a Python Virtual Environment

```sh
python3 -m venv env
```

#### Activate the Virtual Environment

```sh
source env/bin/activate
```

#### Install the Library

```sh
pip install -r requirements.txt
```

#### Only for GDK Build Environment

```sh
python3 -m pip install -U git+https://github.com/aws-greengrass/aws-greengrass-gdk-cli.git@v1.6.2
```

#### Export Environment Variables

##### For Linux

```sh
export AWS_IOT_THING_NAME=YOUR_THING_NAME
export DEV_ACCESS_KEY=YOUR_ACCESS_KEY
export DEV_SECURITY_KEY=YOUR_SECURITY_KEY
export APPLICATION_NAME=WORKING_APPLICATION_NAME
export ENVIRONMENT=Dev
```

##### For Windows (PowerShell)

```powershell
$env:AWS_IOT_THING_NAME = "YOUR_THING_NAME"
$env:DEV_ACCESS_KEY = "YOUR_AWS_ACCESS_KEY"
$env:DEV_SECURITY_KEY = "YOUR_AWS_SECURITY_KEY"
$env:APPLICATION_NAME = "CORRECT_APPLICATOIN_NAME"
$env:ENVIRONMENT = "Dev"
```

### Importing Modules

Here's an example of how to import and use the various modules provided by `aiotica`:

```python
from aiotica.event_receiver import EventReceiver
from aiotica.iot_access_control import IotAccessControl
from aiotica.model.sensor_value import SensorValue
from aiotica.platform.greengrass_client import GreengrassClient

# Initialize modules
event_receiver = EventReceiver()
access_control = IotAccessControl()
sensor_value = SensorValue()
greengrass_client = GreengrassClient()

# Example usage
event_receiver.receive_event()
sensor_data = sensor_value.get_value()
greengrass_client.connect()
```

## Project Structure

The library has the following directory structure:

```
aiotica/
├── event_receiver.py
├── iot_access_control.py
├── model/
│   ├── error_log.py
│   ├── iot_credentials.py
│   ├── log_base.py
│   ├── mqtt_message.py
│   ├── sensor_value.py
│   └── thing_config.py
├── platform/
│   ├── greengrass_client.py
│   ├── ipc_client.py
│   ├── mqtt_base_interface.py
│   └── paho_mqtt_client.py
├── service/
│   ├── api_service.py
│   └── config.py
└── setup.py
```

## Dependencies

The `aiotica` library requires the following dependencies:

- `Rx==3.2.0`
- `paho-mqtt==2.1.0`
- `boto3==1.34.95`
- `awsiotsdk==1.21.4`
- `requests==2.31.0`

These dependencies are automatically installed when you install the library via `pip`.


## Deploying Your Python Library to Test PyPI

To deploy your Python library to Test PyPI, follow these steps:

### Step 1: Install Required Libraries

Ensure you have `setuptools`, `wheel`, and `twine` installed. You can install them using pip:

```bash
pip install setuptools wheel twine
```

### Step 2: Prepare Your Distribution Files

Create the distribution packages for your library. This includes the source distribution (`.tar.gz`) and the built distribution (`.whl`).

In the directory containing your `setup.py` file, run:

```bash
python setup.py sdist bdist_wheel
```

This command will generate the distribution files in a `dist/` directory.

### Step 3: Publish to Test PyPI

Use `twine` to upload these files to Test PyPI. Use the API token you obtained from Test PyPI.

```bash
twine upload dist/* -u __token__ -p <your-api-token>
```

Replace `<your-api-token>` with your actual API token from Test PyPI.

### Alternative: Using an API Command to Publish

If you prefer to use an API command for publishing, you can use `curl` to upload your files. Here’s an example command:



Make sure to replace `yourpackage-0.0.1-py3-none-any.whl` and `yourpackage-0.0.1.tar.gz` with the actual filenames of your distribution files, and `<your-api-token>` with your API token.

### Recap of Commands

1. **Install required libraries:**

    ```bash
    pip install setuptools wheel twine
    ```

2. **Create distribution files:**

    ```bash
    python setup.py sdist bdist_wheel
    ```

3. **Upload to Test PyPI using twine:**

    ```bash
    twine upload dist/* -u __token__ -p <your-api-token>
    ```

    Or, **upload using curl:**

    ```bash
    curl -F "content=@dist/yourpackage-0.0.1-py3-none-any.whl" -F "content=@dist/yourpackage-0.0.1.tar.gz" -u __token__:<your-api-token> https://test.pypi.org/legacy/
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author

KASO

For any queries or further information, you can reach out to [author's email] (you@example.com).

## Acknowledgements

- Thanks to the developers of the dependencies used in this project.
- Special thanks to the KASO team for their continuous support.
```

Feel free to replace placeholders like `YOUR_THING_NAME`, `YOUR_ACCESS_KEY`, `YOUR_SECURITY_KEY`, `WORKING_APPLICATION_NAME`, and `you@example.com` with actual values or instructions.