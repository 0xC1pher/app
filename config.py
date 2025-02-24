import os
from dotenv import load_dotenv
from flask import Flask
from config import Config  # Importa la clase Config


app = Flask(__name__)
app.config.from_object(Config)  # Aplica la configuración

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/asistencia_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'admin123')
