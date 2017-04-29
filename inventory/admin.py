from django.contrib import admin
from .models import Set, Card


class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'cards_in_set', 'release_date',)
    list_filter = ('release_date',)
    fieldsets = [
        (None, {'fields': ['name', 'code', 'cards_in_set', 'release_date']})
    ]


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'set', 'rarity', 'foil', 'stock', 'price')
    fieldsets = [
        (None, {'fields': ['name',
                           'set',
                           'color',
                           'super_types',
                           'sub_types',
                           'mana_cost',
                           'card_language',
                           'rules_text',
                           'flavor_text',
                           'collector_number',
                           'artist',
                           'stock',
                           'price',
                           'image',
                           'rarity',
                           'foil',
                           'power',
                           'toughness']
                }
         )
    ]


admin.site.register(Set, SetAdmin)
admin.site.register(Card, CardAdmin)
