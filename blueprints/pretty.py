from vkbottle.bot import Blueprint
from models import User

bp = Blueprint("pretty")

def pretty(number: int):
    return f"{round(number, 2):,}".replace(",", " ").replace(".",",")