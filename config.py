import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
GEMINI_KEY=os.getenv("GEMINI_KEY")
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")

