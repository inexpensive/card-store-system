from django import template

register = template.Library()


def replace_symbols(value):
    value = value.replace('{W}', '<img src="/static/images/icons/W.svg" class="icon"/>')
    value = value.replace('{U}', '<img src="/static/images/icons/U.svg" class="icon"/>')
    value = value.replace('{B}', '<img src="/static/images/icons/B.svg" class="icon"/>')
    value = value.replace('{R}', '<img src="/static/images/icons/R.svg" class="icon"/>')
    value = value.replace('{G}', '<img src="/static/images/icons/G.svg" class="icon"/>')
    value = value.replace('{0}', '<img src="/static/images/icons/0.svg" class="icon"/>')
    value = value.replace('{1}', '<img src="/static/images/icons/1.svg" class="icon"/>')
    value = value.replace('{2}', '<img src="/static/images/icons/2.svg" class="icon"/>')
    value = value.replace('{3}', '<img src="/static/images/icons/3.svg" class="icon"/>')
    value = value.replace('{4}', '<img src="/static/images/icons/4.svg" class="icon"/>')
    value = value.replace('{5}', '<img src="/static/images/icons/5.svg" class="icon"/>')
    value = value.replace('{6}', '<img src="/static/images/icons/6.svg" class="icon"/>')
    value = value.replace('{7}', '<img src="/static/images/icons/7.svg" class="icon"/>')
    value = value.replace('{8}', '<img src="/static/images/icons/8.svg" class="icon"/>')
    value = value.replace('{9}', '<img src="/static/images/icons/9.svg" class="icon"/>')
    value = value.replace('{10}', '<img src="/static/images/icons/10.svg" class="icon"/>')
    value = value.replace('{11}', '<img src="/static/images/icons/11.svg" class="icon"/>')
    value = value.replace('{12}', '<img src="/static/images/icons/12.svg" class="icon"/>')
    value = value.replace('{13}', '<img src="/static/images/icons/13.svg" class="icon"/>')
    value = value.replace('{14}', '<img src="/static/images/icons/14.svg" class="icon"/>')
    value = value.replace('{15}', '<img src="/static/images/icons/15.svg" class="icon"/>')
    value = value.replace('{16}', '<img src="/static/images/icons/16.svg" class="icon"/>')
    value = value.replace('{17}', '<img src="/static/images/icons/17.svg" class="icon"/>')
    value = value.replace('{18}', '<img src="/static/images/icons/18.svg" class="icon"/>')
    value = value.replace('{19}', '<img src="/static/images/icons/19.svg" class="icon"/>')
    value = value.replace('{20}', '<img src="/static/images/icons/20.svg" class="icon"/>')
    value = value.replace('{T}', '<img src="/static/images/icons/T.svg" class="icon"/>')
    value = value.replace('{X}', '<img src="/static/images/icons/X.svg" class="icon"/>')
    return value


def italicize_reminder_text(value):
    value = value.replace('(', '<i>(')
    value = value.replace(')', ')</i>')
    return value


def insert_subtypes(value):
    if value != '':
        value = '- ' + value
    return value

register.filter('replace_symbols', replace_symbols)
register.filter('insert_subtypes', insert_subtypes)
register.filter('italicize_reminder_text', italicize_reminder_text)
