from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone
import datetime
import json


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_test = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_test


class Set(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    release_date = models.DateField()
    cards_in_set = models.IntegerField()

    def __str__(self):
        return self.name


class Card(models.Model):
    RARITIES = (
        ('C', 'Common'),
        ('U', 'Uncommon'),
        ('R', 'Rare'),
        ('M', 'Mythic'),
    )

    name = models.CharField(max_length=170)
    set = models.ForeignKey(Set)
    color = JSONField()
    super_types = JSONField()
    sub_types = JSONField()
    mana_cost = models.CharField(max_length=20)
    language = models.CharField(max_length=15)
    rules_text = models.TextField()
    flavor_text = models.TextField()
    collector_number = models.IntegerField()
    artist = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.FloatField()
    art = models.ImageField(upload_to='images/', default='images/None/nothing.img')
    rarity = models.CharField(max_length=1, choices=RARITIES)
    foil = models.BooleanField()
    power = models.SmallIntegerField()
    toughness = models.SmallIntegerField()

    def __str__(self):
        return self.name
