from tortoise import Tortoise

async def init():
    await Tortoise.init(
        db_url='sqlite://vkcshop_ivan/database/database.sqlite',
        modules={'models': ['models.user', 'models.globals']}
    )
    await Tortoise.generate_schemas()