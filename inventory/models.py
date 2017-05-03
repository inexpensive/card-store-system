from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.utils import timezone
import datetime
import json


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
        ('B', 'Basic Land'),
    )

    CONDITIONS = (
        ('NM', 'Near Mint'),
        ('SP', 'Slightly Played'),
        ('MP', 'Moderately Played'),
        ('HP', 'Heavily Played')
    )

    COLORS = (
        ('W', 'White'),
        ('U', 'Blue'),
        ('B', 'Black'),
        ('R', 'Red'),
        ('G', 'Green'),
        ('C', 'Colorless'),
    )

    name = models.CharField(max_length=170)
    set = models.ForeignKey(Set)
    color = ArrayField(models.CharField(max_length=1, choices=COLORS))
    color_text = models.CharField(max_length=50)
    color_identity = ArrayField(models.CharField(max_length=1, choices=COLORS))
    layout_type = models.CharField(max_length=50)
    ordered_card_names = ArrayField(models.CharField(max_length=170), blank=True)
    is_focal_card = models.BooleanField()
    super_types = ArrayField(models.CharField(max_length=40), blank=True)
    super_types_text = models.CharField(max_length=100)
    types = ArrayField(models.CharField(max_length=40), blank=True)
    types_text = models.CharField(max_length=100)
    sub_types = ArrayField(models.CharField(max_length=40), blank=True)
    sub_types_text = models.CharField(max_length=100)
    mana_cost = models.CharField(max_length=100)
    cmc = models.IntegerField()
    card_language = models.CharField(max_length=15)
    rules_text = models.TextField()
    flavor_text = models.TextField()
    collector_number = models.CharField(max_length=8)
    multiverse_id = models.IntegerField()
    artist = models.CharField(max_length=100)
    stock = models.IntegerField()
    price = models.FloatField()
    image = models.ImageField(upload_to='templates/images/', default='templates/images/None/nothing.img',
                              max_length=300)
    rarity = models.CharField(max_length=1, choices=RARITIES)
    condition = models.CharField(max_length=2, choices=CONDITIONS)
    foil = models.BooleanField()
    power = models.CharField(max_length=5)
    toughness = models.CharField(max_length=5)
    card_search = SearchVectorField(db_index=True, null=True)

    class Meta:
        unique_together = ('name', 'set', 'card_language', 'condition', 'foil', 'collector_number', 'multiverse_id')

    def __str__(self):
        return self.name
