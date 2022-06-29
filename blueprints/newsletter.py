from asyncio import sleep
from vkbottle.bot import Blueprint
from models import User

bp = Blueprint("Newsletter")
bp.labeler.vbml_ignore_case = True

async def message_deny(ans, uid):

    response = await ans.ctx_api.messages.is_messages_from_group_allowed(
        group_id=ans.group_id, user_id=uid
    )

    return response.is_allowed
    
@bp.on.message(text="рассылка <(\\n)*text>")
async def newsletter_users(ans, text):

    text = [text.replace("~", "\n") for text in text]
    users = await User.all()
    await ans.answer("👑 » Рассылка началась..")
    
    for user in users:
        
        if await message_deny(ans, user.uid):
            await bp.api.messages.send(
            peer_id=user.uid, random_id=0, message="\n".join(text))
        await sleep(0.1)

    return f"👑 » Рассылка закончена! Рассылку получили: {len(users):,} человек."