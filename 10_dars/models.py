from tortoise import models, fields


class Item(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=212)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=5, decimal_places=2)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
