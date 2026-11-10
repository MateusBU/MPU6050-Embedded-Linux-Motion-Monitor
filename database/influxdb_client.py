import os
from pathlib import Path

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

MEASUREMENT = "mpu6050_orientation"

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.env"

load_dotenv(CONFIG_PATH)

def create_client():
    """Initialize and return an INfluxDV client"""

    url = os.getenv("INFLUXDB_URL")
    token = os.getenv("INFLUXDB_TOKEN")
    org = os.getenv("INFLUXDB_ORG")

    if not url:
        raise RuntimeError("INFLUXDB_URL is not configured.")

    if not token:
        raise RuntimeError("INFLUXDB_TOKEN is not configured.")

    if not org:
        raise RuntimeError("INFLUXDB_ORG is not configured.")

    return InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

def get_bucket():
    "Return the configured InfluxDB bucket"

    bucket = os.getenv("INFLUXDB_BUCKET")

    if not bucket:
        raise RuntimeError(
            "INFLUXDB_BUCKET environment variable is not set."
        )

    return bucket

def create_write_api(client):
    """Create a synchronous write API."""

    return client.write_api(
        write_options=SYNCHRONOUS
    )

def write_orientation(write_api, roll, pitch):
    """Write Roll and Pitch measurements to InfluxDB."""

    point = (
        Point(MEASUREMENT)
        .tag("location", "raspberry-pi")
        .field("roll", roll)
        .field("pitch", pitch)
    )

    write_api.write(
        bucket=get_bucket(),
        record=point
    )

def get_latest_reading(query_api):
    """Retrieve the latest Roll and Pitch measurements."""  

    query = f'''
        from(bucket: "{get_bucket()}")
        |> range(start: -10m)
        |> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")
        |> filter(fn: (r) => r["_field"] == "roll" or r["_field"] == "pitch")
        |> group(columns: ["_field"])
        |> last()
    '''

    result = query_api.query(query)

    readings = {
        "roll": None,
        "pitch": None
    }

    for table in result:
        for record in table.records:
            readings[record.get_field()] = record.get_value()

    return readings