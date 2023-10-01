# Problem Statement:
Optimising berth allocation when lacking timely updates from external ship or port operators.
They won’t tell you they are  late...
Because if they do, PSA may allocate their designated berth to another ship to maximise port productivity.

Consequently, PSA will operate at a level substantially below their optimal capacity.

# Solution
With state-of-the-art ML models, predict the trajectory of a ship’s journey, from the start to end, sensitive to important factors.
- Estimates a ship’s arrival time at PSA’s port, and key checkpoint ports, based on vessel size, efficiency of incoming ports, weather conditions, and the distance travelled with powerful machine-learning techniques
- Displays forecasted weather conditions for important port checkpoints
- Adaptable, responsive mobile-friendly UI so that the ETA can be checked anywhere at anytime

# Technology Stack
## Frontend
ReactTS with Vite

## Backend
Flask, Tomorow.io API for weather forecasting

## AI Technologies
Random Forest Regression, SkLearn,  Pandas, NumPy

# Setup and Installation
Clone our frontend and backend repositories onto your local machine.

## Database
1. Seed the SQL database using the provided script.

## Server (Flask)
1. Enter the server directory using the cd command.
2. Enter this command: pip install -r requirements.txt to install dependencies
3. To run the server: python -m flask run
