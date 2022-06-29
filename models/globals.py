from tortoise import Model, fields

class Globals(Model):
    
    course_sell = fields.FloatField(default=1.0)
    course_buy = fields.FloatField(default=1.0)
    oborot = fields.FloatField(default=0)
    total = fields.IntField(default=0)
    last_sdelki = fields.JSONField(default=[])