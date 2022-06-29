from tortoise import Model, fields

class User(Model):

    uid = fields.IntField(default=0)
    name = fields.TextField(default="")
    qiwi = fields.TextField(default="Не указан")
    buy = fields.IntField(default=0)
    sell = fields.IntField(default=0)
    comment = fields.TextField(default="")
    
