from django.contrib import admin
from .models import MagicSet, MagicCard


class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'cards_in_set', 'release_date',)
    list_filter = ('release_date',)
    fieldsets = [
        (None, {'fields': ['name', 'code', 'cards_in_set', 'release_date']})
    ]


class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'set', 'rarity')
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
                           'image',
                           'rarity',
                           'power',
                           'toughness']
                }
         )
    ]


admin.site.register(MagicSet, SetAdmin)
admin.site.register(MagicCard, CardAdmin)
