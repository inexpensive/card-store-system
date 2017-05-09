from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=150, blank=True)
    other_address = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)


class MagicSet(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    release_date = models.DateField()
    cards_in_set = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'code', 'release_date')

    def __str__(self):
        return self.name


class MagicCard(models.Model):
    RARITIES = (
        ('C', 'Common'),
        ('U', 'Uncommon'),
        ('R', 'Rare'),
        ('M', 'Mythic'),
        ('B', 'Basic Land'),
    )

    COLORS = (
        ('W', 'White'),
        ('U', 'Blue'),
        ('B', 'Black'),
        ('R', 'Red'),
        ('G', 'Green'),
        ('C', 'Colorless'),
    )

    LANGUAGES = (
        ('EN', 'English'),
        ('CT', 'Chinese (Traditional)'),
        ('CS', 'Chinese (Simplified)'),
        ('FR', 'French'),
        ('DE', 'German'),
        ('IT', 'Italian'),
        ('JP', 'Japanese'),
        ('KR', 'Korean'),
        ('PT', 'Portuguese'),
        ('RU', 'Russian'),
        ('ES', 'Spanish'),
        ('OT', 'Other'),
    )

    name = models.CharField(max_length=170)
    set = models.ForeignKey(MagicSet)
    color = ArrayField(models.CharField(max_length=1, choices=COLORS))
    color_text = models.CharField(max_length=50)
    color_identity = ArrayField(models.CharField(max_length=1, choices=COLORS))
    layout_type = models.CharField(max_length=50, default='normal')
    ordered_card_names = ArrayField(models.CharField(max_length=170), blank=True)
    is_focal_card = models.BooleanField(default=True)
    super_types = ArrayField(models.CharField(max_length=40), blank=True)
    super_types_text = models.CharField(max_length=100, blank=True)
    types = ArrayField(models.CharField(max_length=40), blank=True)
    types_text = models.CharField(max_length=100, blank=True)
    sub_types = ArrayField(models.CharField(max_length=40), blank=True)
    sub_types_text = models.CharField(max_length=100, blank=True)
    mana_cost = models.CharField(max_length=100)
    cmc = models.IntegerField()
    card_language = models.CharField(max_length=15, choices=LANGUAGES, default='EN')
    rules_text = models.TextField(blank=True)
    flavor_text = models.TextField(blank=True)
    collector_number = models.CharField(max_length=8)
    multiverse_id = models.IntegerField(null=True)
    artist = models.CharField(max_length=100)
    image = models.ImageField(upload_to='inventory/static/images/', default='images/None/nothing.img', max_length=300)
    rarity = models.CharField(max_length=1, choices=RARITIES)
    power = models.CharField(max_length=5, blank=True)
    toughness = models.CharField(max_length=5, blank=True)
    card_search = SearchVectorField(db_index=True, null=True)

    class Meta:
        unique_together = ('name', 'set', 'card_language', 'collector_number', 'multiverse_id')

    def __str__(self):
        return self.name


class MagicCardItem(models.Model):
    NM = 'NM'
    SP = 'SP'
    MP = 'MP'
    HP = 'HP'
    CONDITIONS = (
        (NM, 'Near Mint'),
        (SP, 'Slightly Played'),
        (MP, 'Moderately Played'),
        (HP, 'Heavily Played')
    )
    card = models.ForeignKey(MagicCard)
    price = models.FloatField(default=-1)
    buylist = models.FloatField(default=-1)
    stock = models.IntegerField(default=0)
    condition = models.CharField(max_length=2, choices=CONDITIONS)
    foil = models.BooleanField()

    class Meta:
        unique_together = ('card', 'condition', 'foil')


class Item(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    price = models.FloatField(default=-1)
    magic_set = models.ForeignKey(MagicSet, blank=True)

    class Meta:
        unique_together = ('name', 'type')


class Transaction(models.Model):
    BUY = 'BUY'
    DIST = 'DIST'
    SELL = 'SELL'
    CHARITY = 'CHARITY'
    DISCARD = 'DISCARD'
    TRANSACTION_TYPES = (
        (BUY, 'Purchase from Customer'),
        (DIST, 'Distributor Purchase'),
        (SELL, 'Sell'),
        (CHARITY, 'Charitable Donation'),
        (DISCARD, 'Discarded'),
    )
    customer = models.ForeignKey(User, blank=True)
    distributor = models.CharField(max_length=100)
    charity = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    magic_card = models.ForeignKey(MagicCardItem, blank=True)
    item = models.ForeignKey(Item, blank=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    provincial_tax = models.FloatField()
    federal_tax = models.FloatField()
