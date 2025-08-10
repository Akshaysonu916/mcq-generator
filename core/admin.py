from django.contrib import admin
from .models import Candidate, DomainQuestion, TestSession

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name','email','created_at')
    search_fields = ('name','email')

@admin.register(DomainQuestion)
class DomainQuestionAdmin(admin.ModelAdmin):
    list_display = ('domain','correct_option','approved','difficulty','created_at')
    list_filter = ('domain','approved','difficulty')
    search_fields = ('question_text',)

@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('id','candidate','domain','started_at','finished_at','score')
