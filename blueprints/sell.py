from vkbottle.bot import Blueprint
from vkbottle import BaseStateGroup, CtxStorage
from models import User, Globals
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink
from aioqiwi.wallet import Wallet
from aioqiwi.wallet.enums import PaymentTypes
from blueprints.pretty import pretty
from blueprints.format import format
from blueprints.menu import menu_handler
from random import randint as rand
from vkcoinapi import *
from typing import Optional
import requests
import config
import regex
import re

bp = Blueprint("sell")
ctx = CtxStorage()
bp.labeler.vbml_ignore_case = True
wallet = Wallet(config.key, phone_number=config.phone)


keyboard = (Keyboard(one_time=False, inline=False))
keyboard.add(Text("💸 Проверить оплату"), color=KeyboardButtonColor.SECONDARY)
    
keyboard.row()
keyboard.add(Text("Назад"), color=KeyboardButtonColor.SECONDARY)
    
class BuyState(BaseStateGroup):
	AMOUNT = 0

@bp.on.message(text="<!>Kупить<!>")
async def selling(message):
    
    globals = await Globals.get()
    course_sell = globals.course_sell

    async with Wallet("") as w:
        w.phone_number = ''
        balance = (await w.balance()).accounts[0].balance.amount
    reserve_vkc = (config.coin.getBalance())["response"][str(config.user_id)]/1000
    
    await bp.state_dispenser.set(message.peer_id, BuyState.AMOUNT)
    await message.answer(f"""
⟦ 💵 ⟧ Сейчас в продаже: {pretty(reserve_vkc)} VKC
>-------------------------------------<
⟦ 💢 ⟧ Курс {course_sell}₽ за 1 000 000 VKC
⟦ ⚠️ ⟧ Минимальный заказ - 1 000 000 VKC
>-------------------------------------<
⟦ 📝 ⟧ Введите количество коинов для покупки: (Например: 1кк, 10кк, или 1000000)""", keyboard=keyboard)


@bp.on.message(text="Назад",state=BuyState.AMOUNT)
async def back(message):
    await bp.state_dispenser.delete(message.peer_id)
    await menu_handler(message)
    
    
@bp.on.message(text="💸 Проверить оплату", state=BuyState.AMOUNT)
async def check(message):
    user = await User.get_or_none(uid=message.from_id)
    
    async with Wallet(config.qtoken, phone_number=config.phone) as w:
        comment = str(user.comment)
        payments = (
        await w.history(rows=5, operation=PaymentTypes.IN)).data
    replenishments = list(p for p in payments if p.comment == comment)
    total_amount = sum(r.sum.amount for r in replenishments)
    
    if not replenishments:
        return "Пополнений не найдено. Обратитесь в тех.поддержку"

    await message.answer(f"✅ Поступил платёж {total_amount}₽, коины отправлены на ваш счёт!")
    globals = await Globals.get()
    user = await User.get_or_none(uid=message.from_id)
    course_sell = globals.course_sell
    amount = (total_amount/course_sell)*1000000000
    requests.post("https://coin-without-bugs.vkforms.ru/merchant/send/", data = {"merchantId": config.user_id,
   "key": config.key,
   "toId": message.from_id,
   "amount": amount})
   
    user.comment = str(rand(1,1000000))
    globals.oborot += amount/1000
    globals.total += 1
    amount = amount/1000
    if len(globals.last_sdelki) > 5:
        globals.last_sdelki.pop(0) and globals.last_sdelki.append(f"[id{message.from_id}|{(await message.get_user()).first_name}] купил {pretty(amount)} коинов.")
    else:
        globals.last_sdelki.append(f"[id{message.from_id}|{(await message.get_user()).first_name}] купил {pretty(amount)} коинов.")
    await globals.save()
    await user.save()
    
    await bp.state_dispenser.delete(message.peer_id)
    await menu_handler(message)
    
    
@bp.on.message(state=BuyState.AMOUNT)
async def sell(message, regex: Optional[str] = r"[^кkКK0-9]"):
    globals = await Globals.get()
    user = await User.get_or_none(uid=message.from_id)
    course_sell = globals.course_sell

    text = re.sub(regex, "", (message.text).lower())
    for symbol in "кk":
        order = f"{text.lower()}".replace(symbol,"000")
        order = int(order)
        user.comment = str(rand(1,1000000))
        amount = (order*course_sell)/1000000
        fraction = round(amount*100 % 100, 2)
        url = await bp.api.utils.get_short_link(url=f"https://qiwi.com/payment/form/99?amountFraction={str(fraction).replace('0.','')}&extra[_comment_]={user.comment}&extra[_account_]=%&amountInteger={int(amount)}&currency=643&blocked[0]=account&blocked[1]=comment")
   
        await message.answer(f"""
⟦ ✅ ⟧ Заказ на {pretty(order)} VKC.
⟦ 💳 ⟧ К оплате {pretty(amount)}₽, произведите оплату с QIWI по этой ссылке: {url.short_url} и нажмите на кнопку "💸 Проверить оплату" """)
        await user.save()