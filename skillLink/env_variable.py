from dotenv import load_dotenv
import urllib.parse
import os

load_dotenv()

# Fetch the environment variables and assign them to Python variables
username = urllib.parse.quote_plus(os.getenv("username"))
password = urllib.parse.quote_plus(os.getenv("password"))