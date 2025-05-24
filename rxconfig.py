import reflex as rx
from dotenv import load_dotenv
import os

load_dotenv()

config = rx.Config(
    app_name="app12",
    api_url="http://localhost:8030",
    backend_host="0.0.0.0",
    frontend_port=3030,
    backend_port=8030,
    env_file=".env"
)
