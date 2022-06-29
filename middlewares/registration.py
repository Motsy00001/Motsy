from vkbottle.bot import Message
from vkbottle import BaseMiddleware
from models import User, Globals

class RegistrationMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        message = self.event
        user = await User.get_or_none(uid=message.from_id)
        globals = await Globals.get_or_create()
        if not user:
            name = (await message.get_user()).first_name
            user = await User.create(uid=message.from_id, name=name)
            self.send({"user": user})
            await message.answer(f"Привет, {name}!")
