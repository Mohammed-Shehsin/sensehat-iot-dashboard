import os
import csv
import time
from flask import Flask, render_template, jsonify, request, send_file
from sense_hat import SenseHat
from sensehat_interface import get_all_sensor_data

# Define paths
base_dir = os.path.dirname(os.path.abspath(_file_))
template_path = os.path.join(base_dir, '../templates')
static_path = os.path.join(base_dir, '../static')
log_path = os.path.join(base_dir, 'sensor_log.csv')

app = Flask(_name_, template_folder=template_path, static_folder=static_path)
sense = SenseHat()

# Ensure CSV exists with header
csv_headers = [
    'Timestamp', 'Temperature (C)', 'Humidity (%)', 'Pressure (hPa)',
    'Orientation Pitch (°)', 'Orientation Roll (°)', 'Orientation Yaw (°)',
    'Gyroscope X (°/s)', 'Gyroscope Y (°/s)', 'Gyroscope Z (°/s)',
    'Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)'
]

if not os.path.exists(log_path) or os.stat(log_path).st_size == 0:
    with open(log_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

# ROUTES
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
        row = [table.get(h, 0) for h in csv_headers]
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
                ts = row["Timestamp"]
                for key, val in row.items():
                    if key == "Timestamp":
                        continue
                    try:
                        data.setdefault(key, []).append({"x": ts, "y": float(val)})
                    except:
                        data.setdefault(key, []).append({"x": ts, "y": None})
    except Exception as e:
        print("log_data error:", e)
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
    data = request.get_json()
    text = data.get("text", "")
    sense.show_message(text, text_colour=[255, 255, 255])
    return '', 204

@app.route('/api/clear', methods=['POST'])
def clear_display():
    sense.clear()
    return '', 204

# ENTRY POINT
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000)
