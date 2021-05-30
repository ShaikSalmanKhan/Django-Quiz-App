
from django import template

register = template.Library()

@register.filter
def convert_string_to_list(string):
    """this will given string into list by splitting it by *"""
    answers_list = string.split('*')
    return answers_list
