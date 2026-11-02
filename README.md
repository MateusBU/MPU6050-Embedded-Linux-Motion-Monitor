# MPU6050-Embedded-Linux-Motion-Monitor
An Embedded Linux and IoT project built with a Raspberry Pi 4 and an MPU6050 accelerometer/gyroscope sensor. The application captures motion data, calculates device orientation, stores measurements in InfluxDB, and provides a web dashboard to monitor sensor readings in real time.

## Features

- **I2C Communication:** Communicates with the MPU6050 sensor through the Raspberry Pi's I2C interface.
- **Motion Data Acquisition:** Reads raw accelerometer measurements from the MPU6050.
- **Orientation Calculation:** Calculates Roll and Pitch angles using accelerometer data.
- **Data Logging:** Periodically sends sensor measurements to an InfluxDB database.
- **REST API:** Provides sensor measurements in JSON format through a Flask web server.
- **Live Dashboard:** Displays Roll and Pitch measurements with automatic updates every 500 ms.
- **Remote Monitoring:** Allows access to the dashboard from other devices on the same local network.

## Hardware

- Raspberry Pi 4
- MPU6050 6-axis accelerometer and gyroscope module

## Software and Technologies

- Python 3
- Embedded Linux (Raspberry Pi OS)
- I2C
- SMBus2
- InfluxDB 2.x
- Flask
- HTML, CSS and JavaScript

## System Architecture

The application is divided into two independent processes:

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
           +-----+-----+
           |           |
           v           v
        REST API   Web Dashboard
         (JSON)      (/live)
```

### Data Acquisition

`read_mpu6050.py` is responsible for:

1. Initializing I2C communication.
2. Waking up the MPU6050 sensor.
3. Reading accelerometer registers.
4. Converting raw measurements into acceleration values (g).
5. Calculating Roll and Pitch angles.
6. Sending measurements to InfluxDB every 100 ms.

### Web Application

`app.py` provides:

- `/` — REST API endpoint returning the latest Roll and Pitch measurements in JSON format.
- `/live` — Web dashboard displaying sensor orientation with automatic updates every 500 ms.

## Project Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd MPU6050-Embedded-Linux-Motion-Monitor
```

### 2. Create a Python virtual environment

```bash
python3 -m venv .env
source .env/bin/activate
```

### 3. Install dependencies

```bash
pip install smbus2 flask 'influxdb-client[ciso]'
```

### 4. Configure InfluxDB

Make sure InfluxDB is installed and running.

Configure the following parameters in the Python scripts:

- URL: `http://localhost:8086`
- Organization: `packt`
- Bucket: `ch12`

Set your InfluxDB API token as an environment variable:

```bash
export INFLUXDB_TOKEN='your_influxdb_token'
```

**Note:** Use your own InfluxDB token. Never commit credentials or API tokens to the repository.

### 5. Enable I2C

Enable the I2C interface on the Raspberry Pi and verify that the MPU6050 is detected:

```bash
sudo i2cdetect -y 1
```

The MPU6050 should normally appear at address `0x68`.

## Running the Application

The application requires two independent processes.

**Terminal 1 — Sensor Data Acquisition**

```bash
source .env/bin/activate
export INFLUXDB_TOKEN='your_influxdb_token'
python3 read_mpu6050.py
```

**Terminal 2 — Flask Web Server**

```bash
source .env/bin/activate
export INFLUXDB_TOKEN='your_influxdb_token'
python3 app.py
```

## Accessing the Dashboard

Open the following URL from a browser on the same local network:

```text
http://<RASPBERRY_PI_IP>:5000/live
```

To access the REST API directly:

```text
http://<RASPBERRY_PI_IP>:5000/
```

Example JSON response:

```json
{
    "roll": 7.20,
    "pitch": -28.61
}
```

## Future Improvements

- Refactor sensor and database operations into independent Python modules.
- Implement gyroscope data acquisition.
- Combine accelerometer and gyroscope measurements using a complementary filter.
- Add additional sensor measurements, such as temperature and humidity.
- Implement automatic startup using Linux systemd services.
- Improve dashboard visualization and historical data analysis.

## Learning Objectives

This project explores practical concepts related to:

- Embedded Linux development.
- Hardware interfacing through I2C.
- Python-based embedded applications.
- Sensor data acquisition and processing.
- Time-series databases.
- REST API development.
- IoT monitoring and visualization.

---

**Status:** Work in Progress

**Platform:** Raspberry Pi 4 — Embedded Linux