import os
import csv
import time
from flask import Flask, render_template, jsonify, request, send_file
from sense_hat import SenseHat
from sensehat_interface import get_all_sensor_data

base_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(base_dir, '../templates')
static_path = os.path.join(base_dir, '../static')
log_path = os.path.join(base_dir, 'sensor_log.csv')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
sense = SenseHat()

# Ensure log file exists with headers
if not os.path.exists(log_path):
    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Timestamp', 'Temperature (C)', 'Humidity (%)', 'Pressure (hPa)',
            'Orientation Pitch (°)', 'Orientation Roll (°)', 'Orientation Yaw (°)',
            'Gyroscope X (°/s)', 'Gyroscope Y (°/s)', 'Gyroscope Z (°/s)',
            'Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)'
        ])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/sensors')
def get_sensor_data():
    start = time.time()
    data = get_all_sensor_data()
    elapsed = round((time.time() - start) * 1000, 2)
    response = {str(i): data[i] for i in range(len(data))}
    response["load_time_ms"] = elapsed

    try:
        table = {label: value for label, value in data}
        row = [
            table.get("Timestamp", ""),
            table.get("Temperature (C)", 0),
            table.get("Humidity (%)", 0),
            table.get("Pressure (hPa)", 0),
            table.get("Orientation Pitch (°)", 0),
            table.get("Orientation Roll (°)", 0),
            table.get("Orientation Yaw (°)", 0),
            table.get("Gyroscope X (°/s)", 0),
            table.get("Gyroscope Y (°/s)", 0),
            table.get("Gyroscope Z (°/s)", 0),
            table.get("Accelerometer X (g)", 0),
            table.get("Accelerometer Y (g)", 0),
            table.get("Accelerometer Z (g)", 0),
        ]
        with open(log_path, 'a', newline='') as f:
            csv.writer(f).writerow(row)
    except Exception as e:
        print("CSV logging error:", e)

    return jsonify(response)

@app.route('/api/logdata')
def log_data():
    data = {}
    try:
        with open(log_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamp = row["Timestamp"]
                for key, value in row.items():
                    if key == "Timestamp":
                        continue
                    data.setdefault(key, []).append({"x": timestamp, "y": float(value)})
    except Exception as e:
        print("Log read error:", e)
    return jsonify(data)

@app.route('/download/log')
def download_log():
    return send_file(log_path, as_attachment=True)

@app.route('/api/ledmatrix', methods=['POST'])
def set_led_matrix():
    data = request.json.get('matrix', [])
    flat = [tuple(pixel) for row in data for pixel in row]
    try:
        sense.set_pixels(flat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return '', 204

@app.route('/api/ledmatrix/clear', methods=['POST'])
def clear_led_matrix():
    sense.clear()
    return '', 204

@app.route('/api/ledmatrix/state')
def get_led_matrix_state():
    pixels = sense.get_pixels()
    matrix = [pixels[i * 8:(i + 1) * 8] for i in range(8)]
    return jsonify(matrix)

@app.route('/api/message', methods=['POST'])
def display_message():
    text = request.get_json().get("text", "")
    sense.show_message(text, text_colour=[255, 255, 255])
    return '', 204

@app.route('/api/clear', methods=['POST'])
def clear_display():
    sense.clear()
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
