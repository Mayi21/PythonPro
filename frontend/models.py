from tortoise import fields, models


class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=20)

    class Meta:
        table = "users"