from django.contrib import admin

# Register your models here.
from django.contrib import admin
from.models import Question_Choice ,Exam_Result, TIMER_S, Exam_Table, Testing_Choice, TIMER_S_TESTTING, Testing_Result,Testing_Table, TYT_Choice, TIMER_S_TYT, TYT_Table,TYT_Result,AYT_Choice,AYT_TIMER_S,AYT_Table,AYT_Result#, Lesson_ChoiceClass_Choice, Answer_Choice, Period_Choice,
admin.site.register(Question_Choice)
admin.site.register(Exam_Result)
admin.site.register(Exam_Table)
admin.site.register(TIMER_S)
admin.site.register(TIMER_S_TESTTING)
admin.site.register(Testing_Result)
admin.site.register(Testing_Table)
admin.site.register(Testing_Choice)
admin.site.register(TYT_Choice)
admin.site.register(TIMER_S_TYT)
admin.site.register(TYT_Table)
admin.site.register(TYT_Result)
admin.site.register(AYT_Choice)
admin.site.register(AYT_TIMER_S)
admin.site.register(AYT_Table)
admin.site.register(AYT_Result)
# admin.site.register(Lesson_Choice)
# admin.site.register(Period_Choice)
# admin.site.register(Class_Choice)
# admin.site.register(Answer_Choice)
# Register your models here.
