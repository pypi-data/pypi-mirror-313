# User guide and documentation

## What can you do with the Python SDK?

1. Search for the device.
2. Check Device Battery
3. Stream Impedance
4. Connect and record data from the earbud.
    - Get live insights of your data (raw eeg and filtered eeg)
    - Get real time predictions of your data (fft, jaw clench)
    - PS: Data feedback from Live insights and Realtime predictions has a latency estimate of approximately 1 second
5. Download the data to your local machine.
6. Generate Reports
7. List all Recordings
8. Delete Recording

---

## Prerequisites

- Python 3.9 - 3.13

---

## Quick installation guide

It is advised to create a new Python Virtual Environment:
  ```bash
  python -m venv idun_env
  source idun_env/bin/activate
  ```
Alternatively you can use third party tools such as [Conda](https://www.anaconda.com/products/distribution) or [Pipenv](https://pypi.org/project/pipenv/):

1. First activate the virtual environment, this command must always be run before using the python SDK:

  ```bash
  source idun_env/bin/activate
  ```

2. After the environment is activated, install the Python SDK using the following command:

  ```bash
  pip install idun-guardian-sdk
  ```

3. After installing the package, make sure that the dependencies are correctly installed by running the following command and inspecting the packages installed in the terminal output:

  ```bash
  pip list
  ```

You should see as output a package named `idun-guardian-sdk`

---

## How to use the Python SDK

You can find sample scripts from this GitHub repository in `examples` folder to do basic operations with guardian earbud.

Before getting started, to do any Cloud API operation you should have your IDUN API TOKEN. You can configure the token whether by setting `IDUN_API_TOKEN` Environment Variable or by initializing `GuardianClient` object in Python with `api_token` argument:

Env Var:
```
export IDUN_API_TOKEN=my-api-token
```

or

```
my_api_token = "xxxxxx"
client = GuardianClient(api_token=my_api_token)
```

## Pre Recording

### **1. Search the earbud manually**

- To search for the earbud, you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_sdk import GuardianClient

client = GuardianClient()

device_address = asyncio.run(client.search_device())
```

- Follow the steps in the terminal to search for the earbud with the name `IGEB`
- If there are more than one IGEB device in the area, you will be asked to select the device you want to connect to connect to, a list such as below will pop up in the terminal:

  - For Windows:

  ```bash
  ----- Available devices -----

  Index | Name | Address
  ----------------------------
  0     | IGEB | XX:XX:XX:XX:XX:XX
  1     | IGEB | XX:XX:XX:XX:XX:XX
  2     | IGEB | XX:XX:XX:XX:XX:XX
  ----------------------------
  ```

  - For Mac OS:

  ```bash
  ----- Available devices -----
  Index | Name | UUID
  ----------------------------
  0    | IGEB | XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  1    | IGEB | XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  2    | IGEB | XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
  ----------------------------
  ```

- Enter the index number of the device you want to connect to.

For the next executions, you can save the address and initialize the GuardianClient with `address` parameter:

```python
import asyncio
from idun_guardian_sdk import GuardianClient

device_address = ""  # add address string here
client = GuardianClient(address=device_address)
```

If the address is not provided and you start connection to the device, the `search_device()` prompt will be automatically started.

### **2. Check battery level**

- To read out the battery level, you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_sdk import GuardianClient

client = GuardianClient()

battery_level = asyncio.run(client.check_battery())
print("Battery Level: %s%%" % battery_level)
```

### **3. Check impedance values**

- To read out the impedance values, you need to run the following commands in your python shell or in your python script. PS: the `stream_impedance` will run until you manually stop by pressing `Ctrl + C` in your terminal (check below for start/stop impedance commands without manual cancellation):

```python
import asyncio
from idun_guardian_sdk import GuardianClient

MAINS_FREQUENCY_60Hz = False
# mains frequency in Hz (50 or 60), for Europe 50Hz, for US 60Hz

client = GuardianClient()

# start a recording session
asyncio.run(
    client.stream_impedance(mains_freq_60hz=MAINS_FREQUENCY_60Hz)
)
```

If you are developing a program that needs to control start/stop streaming the impedance without manual `Ctrl + C` or program exit, you can run `client.stop_impedance`, this would require to start impedance (`client.stream_impedance()`) as a asyncio task:

In this example the `client.stream_impedance()` is created with as a coroutine task along with a `sample_task` function (to be replaced by your usecase) that runs concurrently for 15 seconds, after this sample execution, it calls `client.stop_impedance()` and waits the impedance streaming to gracefully stop.

```python
import asyncio
from idun_guardian_sdk import GuardianClient


def print_impedance(data):
    print(f"{data}\tOhm")


async def sample_task(seconds):
    """
    Replace your function/task here
    """
    for i in range(seconds):
        print(f"Run a sample task for: {i}/{seconds} seconds")
        await asyncio.sleep(1)


async def main():
    client = GuardianClient(debug=True)
    await client.connect_device()  # Connect to the device is not required, sdk handles it

    print("Starting impedance task")
    task = asyncio.create_task(client.stream_impedance(handler=print_impedance))

    try:
        await sample_task(seconds=15)
        client.stop_impedance()
        await task
        await client.disconnect_device()  # Disconnect to the device is not required to be called, sdk handles it on program exit

    except (KeyboardInterrupt, asyncio.CancelledError):
        pass


if __name__ == "__main__":
    asyncio.run(main())
```

## Recording

### **4. Start a recording**

- To start a recording with a pre-defined timer (e.g. `100` in seconds), you need to run the following command in your python shell or in your python script:

```python
import asyncio
from idun_guardian_sdk import GuardianClient

RECORDING_TIMER: int =  60 * 60 * 10  # 10 hours
LED_SLEEP: bool = False

my_api_token = ""
my_device_address = ""


# Example callback function
def print_data(event):
    print("CB Func:", event.message)


client = GuardianClient(api_token=my_api_token, address=my_device_address)

client.subscribe_live_insights(raw_eeg=True, filtered_eeg=True, handler=print_data)

# start a recording session
asyncio.run(
    client.start_recording(
        recording_timer=RECORDING_TIMER,
        led_sleep=LED_SLEEP,
    )
)
```

- To stop the recording, either wait for the timer to run out or interrupt the recording
  - with Mac OS enter the cancellation command in the terminal running the script, this would be `Ctrl+.` or `Ctrl+C`
  - with Windows enter the cancellation command in the terminal running the script, this would be `Ctrl+C` or `Ctrl+Shift+C`

## Post Recording

### **5. Get all recorded info**

At the end of recording, the recording ID will be printed, and you can use it to download the data.

If you somehow lose the terminal logs, you can still get info of previous recordings:

```python
from idun_guardian_sdk import GuardianClient

client = GuardianClient()

# get a list of all recordings
recordings = client.get_recordings(status="COMPLETED", limit=10)

print(recordings)
```

### **6. Download recording**

- To download the recoridng run the following command in your python shell or in your python script

```python
from idun_guardian_sdk import GuardianClient, FileTypes

my_api_token = ""
my_recording_id = ""

client = GuardianClient(api_token=my_api_token)
client.download_file(recording_id=my_recording_id, file_type=FileTypes.EEG)
```

## Generating Reports

Your recording must have at least 10 minutes of data so the reports can be generated

### **7. Generate Sleep Report for a Recording**

To generate sleep report, you can call `generate_and_download_sleep_report`

```python
from idun_guardian_sdk import GuardianClient

my_api_token = ""
my_recording_id = ""

client = GuardianClient(api_token=my_api_token)
client.generate_and_download_sleep_report(recording_id=my_recording_id)
```

### **8. Generate Daytime Report for a Recording**

To generate daytime report, you can call `generate_and_download_daytime_report`

```python
from idun_guardian_sdk import GuardianClient

my_api_token = ""
my_recording_id = ""

client = GuardianClient(api_token=my_api_token)
client.generate_and_download_daytime_report(recording_id=my_recording_id)
```

## Development
- setup: `poetry install`
- build package: `poetry build`
- build docs: `make html`
