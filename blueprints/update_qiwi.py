from vkbottle.bot import Blueprint
from models import User

bp = Blueprint("update_qiwi")
bp.labeler.vbml_ignore_case = True

@bp.on.message(text=["<!>Изменить<!>"])
async def updqiwi(message):
    user = await User.get_or_none(uid=message.from_id)
    state = None
    await message.answer(f"""
⟦ ✅ ⟧ Укажите номер QIWI кошелька. Пример: "киви 79XXXXXXXXX"
>-------------------------------------< 
⟦ ✏ ⟧ Сейчас указан - {user.qiwi}
>-------------------------------------<
⟦ 💰 ⟧ На данный кошелёк будут производиться выплаты.
>-------------------------------------<
⟦ 💢 ⟧ Ваш статус QIWI должен быть 'Основной' или же выше.""")
    
@bp.on.message(text=["киви <new_qiwi>"])
async def update_qiwi(message, new_qiwi):
        user = await User.get_or_none(uid=message.from_id)
        user.qiwi = new_qiwi
        await user.save()
        return f"✨ {user.name}, ваш QIWI был изменён на {new_qiwi}"
