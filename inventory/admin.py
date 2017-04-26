from django.contrib import admin
from .models import Choice, Question, Set, Card


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]


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


admin.site.register(Question, QuestionAdmin)
admin.site.register(Set, SetAdmin)
admin.site.register(Card, CardAdmin)
