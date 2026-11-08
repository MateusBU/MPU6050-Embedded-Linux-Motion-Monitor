
import os

from flask import Flask, jsonify
from influxdb_client import InfluxDBClient
from flask import Flask, jsonify, render_template_string
from dotenv import load_dotenv

# Flask configuration
app = Flask(__name__)

# InfluxDB configuration
load_dotenv("config.env")

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

MEASUREMENT = "mpu6050_orientation"

# Initialize InfluxDB client
if not INFLUXDB_TOKEN:
    raise RuntimeError("INFLUXDB_TOKEN environment variable is not set.")

client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)

query_api = client.query_api()



@app.route("/")
def get_last_reading():
    """Retrieve the latest Roll and Pitch measurements."""

    query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
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
            field = record.get_field()
            value = record.get_value()

            readings[field] = value

    print(
        f"Roll: {readings['roll']:.2f}° | "
        f"Pitch: {readings['pitch']:.2f}°",
        flush=True
    )
    
    if readings["roll"] is None or readings["pitch"] is None:
        return jsonify({
            "error": "No recent sensor readings found."
        }), 404

    return jsonify(readings)


@app.route("/live")
def live_dashboard():
    """Display live MPU6050 sensor readings."""

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MPU6050 Live Monitor</title>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 80px;
                background-color: #f4f4f4;
            }

            .reading {
                display: inline-block;
                background: white;
                padding: 30px;
                margin: 15px;
                border-radius: 10px;
                min-width: 180px;
            }

            .value {
                font-size: 36px;
                color: #2563eb;
            }
        </style>
    </head>
    <body>
        <h1>MPU6050 Live Monitor</h1>

        <div class="reading">
            <h2>Roll</h2>
            <div class="value" id="roll">--</div>
        </div>

        <div class="reading">
            <h2>Pitch</h2>
            <div class="value" id="pitch">--</div>
        </div>

        <p id="status">Connecting...</p>

        <script>
            async function updateReadings() {
                try {
                    const response = await fetch(
                        "/?t=" + Date.now(),
                        { cache: "no-store" }
                    );

                    if (!response.ok) {
                        throw new Error("Failed to retrieve sensor data");
                    }

                    const data = await response.json();

                    document.getElementById("roll").textContent =
                        data.roll.toFixed(2) + "°";

                    document.getElementById("pitch").textContent =
                        data.pitch.toFixed(2) + "°";

                    document.getElementById("status").textContent =
                        "Connected - Updating every 500 ms";

                } catch (error) {
                    document.getElementById("status").textContent =
                        "Connection error: " + error.message;
                }
            }

            updateReadings();
            setInterval(updateReadings, 300);
        </script>
    </body>
    </html>
    """)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
