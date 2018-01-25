from django.contrib import admin

from applications.interview_question.models import *
from zhiliangku.settings import tinymce_js


@admin.register(EnterpriseInfo)
class EnterpriseInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'company', "email", 'position',
        'lowest_monthly_salary', 'highest_monthly_salary', "duration", "path", 'question_img', "detail", "notes"
    )
    search_fields = ('company', 'position',)

    class Media:
        js = tinymce_js


@admin.register(CompletedInterviewQuestion)
class CompletedInterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'interview_question', "customuser", "complete")
    search_fields = ('interview_question__company', 'customuser__nickname',)
    list_filter = ('complete',)

    def suit_row_attributes(self, obj, request):
        css_class = {
            True: 'success',
        }.get(obj.complete)
        if css_class:
            return {'class': css_class}


@admin.register(ExaminationQuestion)
class ExaminationQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'enterprise', "qtype", "title", "right_answer", "score")
    search_fields = ('enterprise__company', 'title',)
    filter_horizontal = ('tech',)


@admin.register(ExaminationAnswer)
class ExaminationAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', "option", "content")
    search_fields = ('question__title',)


@admin.register(AnswerRecord)
class AnswerRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', "custom_user", "result", "create_time")
    search_fields = ('question__title', "custom_user__nickname")
    list_filter = ('result',)

    def suit_row_attributes(self, obj, request):
        css_class = {
            True: 'success',
        }.get(obj.result)
        if css_class:
            return {'class': css_class}
