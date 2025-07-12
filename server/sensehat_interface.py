from sense_hat import SenseHat
from datetime import datetime

sense = SenseHat()

def get_all_sensor_data():
    data = []

    try:
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data.append(("Timestamp", timestamp))

        # Environment
        data.append(("Temperature (C)", round(sense.get_temperature(), 2)))
        data.append(("Humidity (%)", round(sense.get_humidity(), 2)))
        data.append(("Pressure (hPa)", round(sense.get_pressure(), 2)))

        # Orientation (Pitch, Roll, Yaw)
        orientation = sense.get_orientation()
        data.append(("Orientation Pitch (°)", round(orientation.get("pitch", 0), 2)))
        data.append(("Orientation Roll (°)", round(orientation.get("roll", 0), 2)))
        data.append(("Orientation Yaw (°)", round(orientation.get("yaw", 0), 2)))

        # Gyroscope
        gyro = sense.get_gyroscope()
        data.append(("Gyroscope X (°/s)", round(gyro.get("pitch", 0), 2)))
        data.append(("Gyroscope Y (°/s)", round(gyro.get("roll", 0), 2)))
        data.append(("Gyroscope Z (°/s)", round(gyro.get("yaw", 0), 2)))

        # Accelerometer
        accel = sense.get_accelerometer()
        data.append(("Accelerometer X (g)", round(accel.get("pitch", 0), 2)))
        data.append(("Accelerometer Y (g)", round(accel.get("roll", 0), 2)))
        data.append(("Accelerometer Z (g)", round(accel.get("yaw", 0), 2)))

    except Exception as e:
        data.append(("Error", str(e)))

    return data
