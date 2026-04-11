from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'is_active', 'end_date']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title']
    inlines = [ChoiceInline]

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'poll', 'choice', 'voted_at']
    list_filter = ['poll', 'voted_at']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['text', 'poll', 'votes_count']