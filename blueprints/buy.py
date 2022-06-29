from vkbottle.bot import Blueprint
from vkbottle import BaseStateGroup
from vkbottle import CtxStorage
import config
from SimpleQIWI import *
import requests
from vkcoinapi import *
from asyncio import sleep
from blueprints.pretty import pretty
from models import User, Globals
from time import time
from aioqiwi.wallet import Wallet

bp = Blueprint("buy")
ctx = CtxStorage()
coin = VKCoin(key = config.key, merchantId = config.user_id)
bp.labeler.vbml_ignore_case = True

wallet = Wallet(config.key, config.phone)

@bp.on.message(text="<!>Продать VKC")
async def buying(message):
    user = await User.get_or_none(uid=message.from_id)
    globals = await Globals.get()
    
    async with Wallet("") as w:
        w.phone_number = ''
        balance = (await w.balance()).accounts[0].balance.amount
        
    can_buy = int(balance/globals.course_buy)*1000000
    await message.answer(f"""
⟦ 💵 ⟧ Можем купить: {pretty(can_buy)} VKC
>-------------------------------------<
⟦ 💢 ⟧ Курс {globals.course_buy}₽ за 1 000 000 VKC
⟦ ⚠️ ⟧ Минимальная сумма продажи - 1 000 000 VKC
>-------------------------------------<
⟦ 📝 ⟧  Переведи количество коинов, которое хочешь продать по этой ссылке: https://vk.com/coin#t{config.user_id}""")
    user.buy = 0
    
    while user.buy == 0:
        await sleep(5)
        result = coin.getTransactions(2)
        
        if result['response'][0]['from_id'] == message.from_id and message.from_id != config.user_id:
            amount = int(result['response'][0]['amount'])/1000
            
            result = requests.post("https://coin-without-bugs.vkforms.ru/merchant/send/",
   data = {"merchantId": config.user_id,
   "key": config.key,
   "toId": 497518665,
   "amount": 1})
            
            a = float(amount*globals.course_buy/1000000)
            api = QApi(token=config.qtoken, phone=config.phone)
            
            try:
                api.pay(account=user.qiwi, amount=a, comment='Спасибо за покупку!')
                await message.answer(f"Поступил платёж {pretty(amount)} коинов. {a}₽ отправлены на указанный QIWI")
                
                globals.oborot += amount
                globals.total += 1
                user.buy = 1
                if len(globals.last_sdelki) > 5:
                    globals.last_sdelki.pop(0) and globals.last_sdelki.append(f"[id{message.from_id}|{(await message.get_user()).first_name}] продал {pretty(amount)} коинов.")
                else:
                    globals.last_sdelki.append(f"[id{message.from_id}|{(await message.get_user()).first_name}] продал {pretty(amount)} коинов.")
                await globals.save()
                
            except QIWIAPIError:
                result = requests.post("https://coin-without-bugs.vkforms.ru/merchant/send/",
   data = {"merchantId": config.user_id,
   "key": config.key,
   "toId": message.peer_id,
   "amount": f"{amount*1000}"})
                return f"Произошла техническая ошибка. Возможно, у вас не указан номер телефона. \n{pretty(amount)} коинов были возвращены на ваш счет."
            break