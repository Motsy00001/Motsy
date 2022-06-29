from vkbottle.bot import Blueprint
from models import User, Globals
import config


bp = Blueprint("last_sdelki")
bp.labeler.vbml_ignore_case = True

@bp.on.message(text="<!>Последние сделки")
async def sdelki(message):
    globals = await Globals.get()
    await message.answer("Последние сделки:\n"+"\n".join(globals.last_sdelki))