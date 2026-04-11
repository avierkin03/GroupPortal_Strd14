from django.contrib import admin

from django.contrib import admin
from .models import Vote, Choice, UserVote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class VoteAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Vote, VoteAdmin)
admin.site.register(UserVote)
