from typing import Optional
from vkbottle.bot import Blueprint
from models import User
import re

bp = Blueprint("fromat")

def format(text: Optional[str], pattern: Optional[str] = r"[^кkКK0-9]"):
    text = re.sub(pattern, "", text)
    for symbol in "кk":
        text = f"{text.lower()}".replace(symbol,"000")
    return int(text)