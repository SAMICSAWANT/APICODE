# APICODE
# APICODE
# APICODE
# PARKAPPSYSTEM

# ParkASpot - Smart Parking System

A comprehensive smart parking system that uses computer vision to detect available parking spaces and allows users to book spots through a modern web interface.

## System Components

1. **Computer Vision Backend (Python)**
   - Located in the `Pyt` directory
   - Uses OpenCV to detect available parking spaces from video feeds
   - Exposes a Flask API for the frontend to consume

2. **Web Frontend (React)**
   - Located in the `smart-parking-frontend` directory
   - Modern UI built with React and TailwindCSS
   - Communicates with the Python backend API

## Setup and Installation

### Python Backend

1. Navigate to the Python backend directory:
   ```
   cd Pyt
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask API server:
   ```
   python api.py
   ```
   
   The server will start on http://localhost:5001

4. (Optional) If you want to configure parking spaces:
   ```
   python ParkingSpacePicker.py
   ```
   - Left click to add a parking space
   - Right click to remove a parking space
   - Press 'd' to save and exit

### React Frontend

1. Navigate to the frontend directory:
   ```
   cd smart-parking-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

   The application will start on http://localhost:3000

## System Workflow

1. The Python backend detects parking spaces and their availability using computer vision
2. The Flask API serves this data to the frontend
3. Users can view available spaces in real-time and book a spot
4. The booking information is sent back to the server

## Features

- Real-time parking space detection
- Interactive parking space selection
- Booking system with validation
- Mobile-responsive design
- Ticket generation for bookings

## Technologies Used

- **Backend**: Python, OpenCV, Flask, NumPy
- **Frontend**: React, TailwindCSS, Heroicons, Axios
- **UI Components**: Custom-built component library
