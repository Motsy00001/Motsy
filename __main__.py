from vkbottle.bot import Bot
from database import init
from middlewares import mds
import config
from blueprints import bps

bot = Bot(config.token)

for bp in bps:
    bp.load(bot)


for md in mds:
    bot.labeler.message_view.register_middleware(md)

bot.loop_wrapper.on_startup.append(init())
bot.run_forever()