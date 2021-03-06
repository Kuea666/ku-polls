"""Create admin page."""
from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    """Can add choice in question"""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Custom question fields in admin page."""

    list_filter = ['pub_date']
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': [
         'pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date',
                    'end_date', 'was_published_recently')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
