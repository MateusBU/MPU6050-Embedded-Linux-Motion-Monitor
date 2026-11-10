# MPU6050 Embedded Linux Motion Monitor

An Embedded Linux and IoT project built with a Raspberry Pi 4 and an MPU6050 accelerometer/gyroscope sensor.

The application captures motion data, calculates device orientation, stores measurements in InfluxDB, and provides multiple interfaces for real-time monitoring through a Flask REST API, a web dashboard, and a native Qt Quick application.

## Features

- **I2C Communication:** Communicates with the MPU6050 sensor through the Raspberry Pi's I2C interface.
- **Motion Data Acquisition:** Reads raw accelerometer measurements from the MPU6050.
- **Orientation Calculation:** Calculates Roll and Pitch angles using accelerometer data.
- **Data Logging:** Periodically sends sensor measurements to an InfluxDB database.
- **REST API:** Provides sensor measurements in JSON format through a Flask web server.
- **Web Dashboard:** Displays Roll and Pitch measurements through a browser.
- **Native Qt Dashboard:** Provides a graphical monitoring interface developed with C++ and Qt Quick (QML).
- **Dark and Light Themes:** Supports switching between dark and light dashboard themes.
- **Live Monitoring:** Updates sensor readings automatically through HTTP requests to the Flask API.
- **Remote Monitoring:** Allows access to the web dashboard from other devices on the same local network.
- **Makefile Automation:** Simplifies backend startup, Qt compilation, application execution, and cleanup.

## Hardware

- Raspberry Pi 4
- MPU6050 6-axis accelerometer/gyroscope module
- HDMI display (optional, for the native Qt dashboard)

## Software and Technologies

### Backend
- Python 3
- Embedded Linux (Raspberry Pi OS)
- I2C
- SMBus2
- InfluxDB 2.x
- Flask
- Python-dotenv

### Frontend
- C++
- Qt 5
- Qt Quick
- QML
- CMake

### Development Tools
- Git
- GNU Make
- Linux system utilities

## System Architecture

The project is divided into three main components: sensor data acquisition, backend services, and frontend applications.

```text
                  MPU6050 Sensor
                         |
                         | I2C
                         v
                  read_mpu6050.py
                         |
                         | Sensor measurements
                         v
                      InfluxDB
                         |
                         | Flux queries
                         v
                       app.py
                         |
                    Flask REST API
                         |
                 +-------+-------+
                 |               |
                 v               v
           Web Dashboard    Qt Quick Dashboard
              (/live)          (C++ / QML)
```

## Project Structure

```text
MPU6050-Embedded-Linux-Motion-Monitor/
|
├── .env/                   # Python virtual environment
├── config.env              # InfluxDB configuration
├── app.py                  # Flask application and REST API
├── read_mpu6050.py         # Sensor acquisition and InfluxDB logging
├── Makefile                # Project automation
├── README.md
|
└── qt-dashboard/
    ├── main.cpp            # Qt application entry point
    ├── main.qml            # Graphical user interface
    ├── qml.qrc             # QML resource file
    ├── CMakeLists.txt      # Qt build configuration
    └── build/              # Generated build files
```

## Data Acquisition

`read_mpu6050.py` is responsible for:

1. Initializing I2C communication.
2. Waking up the MPU6050 sensor.
3. Reading accelerometer registers.
4. Converting raw measurements into acceleration values (g).
5. Calculating Roll and Pitch angles.
6. Sending measurements to InfluxDB every 100 ms.

## Backend Application

`app.py` provides the Flask web server and REST API.

### Available endpoints

| Endpoint | Description |
|---|---|
| `/` | Returns the latest Roll and Pitch measurements in JSON format. |
| `/live` | Web dashboard displaying sensor orientation with automatic updates. |

Example API response:

```json
{
    "roll": 7.20,
    "pitch": -28.61
}
```

## Qt Quick Dashboard

The native graphical interface is implemented using C++ and Qt Quick (QML).

### Features

- Real-time Roll and Pitch visualization.
- HTTP communication with the Flask REST API.
- Dark and Light theme switching.
- API connection status indicator.
- Start and Stop monitoring controls.
- Manual Refresh and Reset controls.
- Two-decimal precision for sensor readings.

The Qt application retrieves sensor measurements from the Flask API rather than accessing the I2C sensor directly.

This separation keeps sensor acquisition, backend processing, and graphical presentation independent.

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd MPU6050-Embedded-Linux-Motion-Monitor
```

### 2. Create the Python virtual environment

```bash
python3 -m venv .env
source .env/bin/activate
```

### 3. Install Python dependencies

```bash
pip install smbus2 flask python-dotenv 'influxdb-client[ciso]'
```

### 4. Configure InfluxDB

Make sure InfluxDB 2.x is installed and running.

Create a `config.env` file in the project root:

```env
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your_influxdb_token
INFLUXDB_ORG=packt
INFLUXDB_BUCKET=ch12
```

Use your own InfluxDB token. Never commit credentials or API tokens to the repository.

### 5. Enable I2C

Enable the I2C interface on the Raspberry Pi and verify that the MPU6050 is detected:

```bash
sudo i2cdetect -y 1
```

The MPU6050 should normally appear at address `0x68`.

### 6. Install Qt development dependencies

Install the Qt 5, QML, and CMake development packages:

```bash
sudo apt update

sudo apt install build-essential cmake \
    qtbase5-dev qt5-qmake qtbase5-dev-tools \
    qtdeclarative5-dev \
    qml-module-qtquick2 \
    qml-module-qtquick-controls2 \
    qml-module-qtquick-window2 \
    qml-module-qtquick-layouts
```

## Running the Application

The project includes a Makefile to simplify common development tasks.

### Start the backend

Activate the virtual environment and execute:

```bash
source .env/bin/activate
make run-backend
```

This command starts:

- `read_mpu6050.py` in the background.
- `app.py` as the Flask REST API server.

Press `Ctrl+C` to stop the backend processes.

### Build the Qt dashboard

```bash
make build-qt
```

This command configures the project using CMake and compiles the Qt application.

### Run the Qt dashboard

With the backend running in another terminal:

```bash
make run-qt
```

The dashboard will connect to the Flask API at:

```text
http://127.0.0.1:5000/
```

### Run the entire application

To start the backend and Qt dashboard together:

```bash
source .env/bin/activate
make run
```

Press `Ctrl+C` to stop the processes.

### Clean build files

```bash
make clean
```

## Accessing the Web Dashboard

Open the following URL from a browser on the same local network:

```text
http://<RASPBERRY_PI_IP>:5000/live
```

To access the REST API directly:

```text
http://<RASPBERRY_PI_IP>:5000/
```

The native Qt dashboard can also run directly on a display connected to the Raspberry Pi through HDMI.

## Future Improvements

- Implement gyroscope data acquisition.
- Combine accelerometer and gyroscope measurements using a complementary filter.
- Add additional sensor measurements, such as temperature and humidity.
- Implement automatic startup using Linux systemd services.
- Add graphical orientation indicators and historical data visualization.
- Implement a native C/C++ sensor acquisition module.
- Improve error handling and API communication reliability.

## Learning Objectives

This project explores practical concepts related to:

- Embedded Linux development.
- Hardware interfacing through I2C.
- Python-based embedded applications.
- Sensor data acquisition and processing.
- Time-series databases.
- REST API development.
- C++ application development.
- Qt Quick and QML graphical interfaces.
- Linux application build automation using Make and CMake.

---

**Status:** Work in Progress

**Platform:** Raspberry Pi 4 — Embedded Linux