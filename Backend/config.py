import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# POSTGRES Configuration
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT'))
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
