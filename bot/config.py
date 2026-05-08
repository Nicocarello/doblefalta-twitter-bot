import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

TENNIS_API_KEY = os.getenv("TENNIS_API_KEY")
TENNIS_BASE_URL = "https://api.api-tennis.com/tennis/"
DRY_RUN = os.getenv("DRY_RUN", "True").lower() == "true"

# Configuración Twitter
TWITTER_CONFIG = {
    'consumer_key': os.getenv("CONSUMER_KEY"),
    'consumer_secret': os.getenv("CONSUMER_SECRET"),
    'access_token': os.getenv("ACCESS_TOKEN"),
    'access_token_secret': os.getenv("ACCESS_TOKEN_SECRET"),
}

# Configuración Email
EMAIL_CONFIG = {
    'sender': os.getenv("EMAIL_SENDER"),
    'password': os.getenv("EMAIL_PASSWORD"),
    'receivers': os.getenv("EMAIL_RECEIVERS", "").split(",")
}
