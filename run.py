from dotenv import load_dotenv
import os

# Explicitly load .env file
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("AgroAI Application started successfully.")
    app.run(debug=True, port=5000)
