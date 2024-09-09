from tortoise import fields, models

class About(models.Model):
    name = fields.CharField(max_length=100)
    birthday = fields.CharField(max_length=100)
    address = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100)
    phone = fields.CharField(max_length=20)
    project_count = fields.IntField()
    cv = fields.CharField(max_length=255)

class Resume(models.Model):
    start_year = fields.IntField()
    finish_year = fields.IntField()
    profession = fields.CharField(max_length=100)
    university = fields.CharField(max_length=255)
    description = fields.TextField()

class Service(models.Model):
    image = fields.CharField(max_length=255)
    title = fields.CharField(max_length=100)
    link = fields.CharField(max_length=255)
    price = fields.FloatField()

class Skill(models.Model):
    name = fields.CharField(max_length=100)
    percentage = fields.IntField()

class Project(models.Model):
    image = fields.CharField(max_length=255)
    link = fields.CharField(max_length=255)
    title = fields.CharField(max_length=100)

class Category(models.Model):
    name = fields.CharField(max_length=100)

class Tag(models.Model):
    name = fields.CharField(max_length=100)

class Post(models.Model):
    title = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255)
    description = fields.TextField()
    author_name = fields.CharField(max_length=100)
    category = fields.ForeignKeyField("models.Category", related_name="posts")
    tags = fields.ManyToManyField("models.Tag", related_name="posts")

class Contact(models.Model):
    name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    website = fields.CharField(max_length=255)
    message = fields.TextField()
