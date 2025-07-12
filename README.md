# Sense HAT IoT Dashboard — Project_Shehsin_05_06

A complete IoT monitoring and control dashboard built on Raspberry Pi using Flask and Sense HAT. This project offers real-time environmental monitoring, LED matrix control, data logging, and visualization in a clean web UI.

---

## 🔧 Features

✅ Real-time sensor readings (temperature, humidity, pressure, orientation, gyro, accelerometer)  
✅ Interactive 8×8 LED Matrix control with RGB sliders  
✅ Matrix row/column selection with sync to actual Sense HAT LED state  
✅ Display scrolling messages on Sense HAT  
✅ Sensor load time benchmark displayed in table  
✅ Log all data with timestamp to CSV file  
✅ Export logs via CSV download button  
✅ Time-series charts rendered with ApexCharts  
✅ Auto-start Flask server on boot via `systemd`  

---

## 📂 Project Structure

```
sensehat-iot-dashboard/
├── server/
│   ├── app.py                  # Flask backend server
│   ├── sensehat_interface.py  # Sensor read + CSV logger
│   └── sensor_log.csv          # Auto-generated CSV log file
├── templates/
│   └── index.html              # Main HTML dashboard UI
├── static/
│   └── (optional CSS/JS files if added)
```

---

## 🚀 Installation & Setup

### 1. Requirements

- Raspberry Pi with Sense HAT
- Python 3.x

### 2. Install Python dependencies

```bash
sudo apt update
sudo apt install python3-pip
pip3 install flask sense-hat
```

### 3. Run the server

```bash
cd ~/sensehat-iot-dashboard/server
python3 app.py
```

Open browser and visit:  
`http://<your_pi_ip>:5000`

---

## 🔁 Auto-Start with systemd (Optional)

Create systemd service:

```bash
sudo nano /etc/systemd/system/shehsin-sensehat.service
```

Paste the following:

```
[Unit]
Description=Shehsin Sense HAT Flask Web App
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/sensehat-iot-dashboard/server/app.py
WorkingDirectory=/home/pi/sensehat-iot-dashboard/server
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

Then run:

```bash
sudo systemctl daemon-reexec
sudo systemctl enable shehsin-sensehat
sudo systemctl start shehsin-sensehat
```

---

## 📊 Dashboard Overview

- **Live Sensor Table**: Displays real-time readings every 1 second
- **Sensor Load Time**: Measures API response latency in ms
- **LED Matrix Control**: Toggle any LED, row, or column with RGB sliders
- **Matrix Sync**: Loads Sense HAT state on refresh
- **Scrolling Message**: Optional message display on matrix
- **CSV Logging**: All sensor data saved to `sensor_log.csv`
- **Export Button**: Download full log instantly
- **Time-Series Chart**: Select sensor and plot trends using ApexCharts

---

## 🧑‍💻 Author

**Mohammed Shehsin Thamarachalil Abdulresak**  
Poznań University of Technology — Robotics & Automation  
GitHub: [@Mohammed-Shehsin](https://github.com/Mohammed-Shehsin)

---

## 🪪 License

MIT License
