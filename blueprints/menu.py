from vkbottle.bot import Blueprint
from aioqiwi import Wallet
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink
from models import User, Globals
from blueprints.pretty import pretty
from vkcoinapi import *
import config

bp = Blueprint("menu")
bp.labeler.vbml_ignore_case = True
        
keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text("💢 Kупить VKC"), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text("💢 Продать VKC"), color=KeyboardButtonColor.SECONDARY)

keyboard.row()
keyboard.add(Text("💸 Изменить QIWI"), color=KeyboardButtonColor.PRIMARY)
keyboard.add(Text("👑 Информация"), color=KeyboardButtonColor.PRIMARY)

keyboard.row().add(Text("💵 Последние сделки"), color=KeyboardButtonColor.POSITIVE)

keyboard.row()
keyboard.add(OpenLink(link="", label="⚙️Тех Поддержка"),KeyboardButtonColor.PRIMARY)
keyboard.add(OpenLink(link="", label="🧾Отзывы"),KeyboardButtonColor.PRIMARY)

#Главное меню, Информация
@bp.on.private_message(text=["Начать", "<!>меню", "Назад<!>", "<!>Информация"])
async def menu_handler(message):
    globals = await Globals.get()
    async with Wallet(config.qtoken) as w:
        w.phone_number = config.phone
        api = await w.balance()
    reserve_vkc = (config.coin.getBalance())["response"][str(config.user_id)]/1000
    user = await User.get_or_none(uid=message.from_id)
    await message.answer(f"""
🔴 Резервы:
⟦ 🔥 ⟧ Резерв QIWI: {pretty(api.accounts[0].balance.amount)}₽
⟦ 💰 ⟧ Резерв VKC: {pretty(reserve_vkc)}
⟦ 🥝 ⟧ Ваш QIWI: {user.qiwi}

🔴 Курсы:
⟦ 💢 ⟧ Продажа: 1 000 000 по: {globals.course_sell}₽ 
⟦ 💢 ⟧ Скупка: 1 000 000 по: {globals.course_buy}₽

🔴 Статистика:
⟦ 📓 ⟧ Оборот: {pretty(globals.oborot)} VKC
⟦ 📓 ⟧ Сделок: {pretty(globals.total)}""", keyboard = keyboard)
    await bp.state_dispenser.delete(message.peer_id)