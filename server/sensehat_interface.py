from sense_hat import SenseHat
import datetime

sense = SenseHat()

def get_all_sensor_data():
    t = round(sense.get_temperature(), 2)
    h = round(sense.get_humidity(), 2)
    p = round(sense.get_pressure(), 2)
    o = sense.get_orientation()
    g = sense.get_gyroscope()
    a = sense.get_accelerometer()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        ("Timestamp", timestamp),
        ("Temperature (C)", t),
        ("Humidity (%)", h),
        ("Pressure (hPa)", p),
        ("Orientation Pitch (°)", round(o['pitch'], 2)),
        ("Orientation Roll (°)", round(o['roll'], 2)),
        ("Orientation Yaw (°)", round(o['yaw'], 2)),
        ("Gyroscope X (°/s)", round(g['pitch'], 2)),
        ("Gyroscope Y (°/s)", round(g['roll'], 2)),
        ("Gyroscope Z (°/s)", round(g['yaw'], 2)),
        ("Accelerometer X (g)", round(a['pitch'], 2)),
        ("Accelerometer Y (g)", round(a['roll'], 2)),
        ("Accelerometer Z (g)", round(a['yaw'], 2)),
    ]
