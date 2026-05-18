# AI Gym Management Platform

This project is an AI-generated Flask web application for a local gym management scenario.

The system provides a public-facing gym website and a Flask API for managing fitness classes, trainers, booking requests, member enquiries, and payment-related records.

## Features

- Public gym website
- Automatically generated hero image
- Fitness class listing
- Trainer profile listing
- Class booking request form
- Member enquiry form
- Staff-facing booking dashboard
- Flask API with in-memory data stores
- Basic pytest test suite
- Dockerfile for containerized deployment

## Project Structure

flask/
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── static/
│   └── gym_hero.png
├── templates/
│   └── index.html
└── tests/
    └── test_app.py

## Run Locally

Install dependencies:

pip install -r requirements.txt

Start the Flask application:

python app.py

Open the website:

http://127.0.0.1:5000/

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | / | Render the website homepage |
| GET | /health | Check API health |
| GET | /classes | Return fitness classes |
| GET | /trainers | Return trainer profiles |
| GET | /members | Return gym members |
| GET | /bookings | Return booking requests |
| POST | /bookings | Create a booking request |
| PATCH | /bookings/<booking_id>/status | Update booking status |
| GET | /enquiries | Return member enquiries |
| POST | /enquiries | Create a member enquiry |
| GET | /payments | Return payment records |

## Run Tests

Run the test suite:

pytest

## Run with Docker

Build the Docker image:

docker build -t ai-gym-management .

Run the container:

docker run -p 5000:5000 ai-gym-management

Then open:

http://127.0.0.1:5000/

## Notes

This application uses in-memory Python lists for demonstration purposes. Data will reset when the application restarts.

The project was generated as part of a meta-software development workflow, where a Jupyter Notebook is used to generate software artefacts including documentation, UML diagrams, Flask API code, a website, tests, and deployment files.