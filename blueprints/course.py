from vkbottle.bot import Blueprint
from models import User, Globals
import config

bp = Blueprint("course")
bp.labeler.vbml_ignore_case = True
                
@bp.on.message(text=["курс продажа <new>","курс покупка <new>"])
async def course(message, new):
    globals = await Globals.get_or_none()
    if message.from_id in config.admins:
        if "продажа" in message.text:
            await message.answer(f"Курс продажи был изменён на {new}")
            globals.course_sell = float(new)
        elif "покупка" in message.text:
            await message.answer(f"Курс покупки был изменён на {new}")
            globals.course_buy = float(new)
        await globals.save()
        