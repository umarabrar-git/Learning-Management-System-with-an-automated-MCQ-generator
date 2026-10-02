from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Subject, Topic, Course,
    Enrollment, PythonQuestion,
    Test, TestAttempt, TestResult,
    Evaluation
)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'user_type', 'password1', 'password2'),
        }),
    )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    search_fields = ('name', 'subject__name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor', 'start_date', 'end_date', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('is_active', 'start_date', 'end_date')
    filter_horizontal = ('subjects',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'is_active')
    list_filter = ('is_active', 'course')
    search_fields = ('student__username', 'course__name')


@admin.register(PythonQuestion)
class PythonQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'difficulty', 'question_type', 'subject', 'topic', 'created_by')
    search_fields = ('question_text',)
    list_filter = ('difficulty', 'question_type', 'subject')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_by', 'available_from', 'available_to', 'is_published')
    list_filter = ('is_published', 'course')
    filter_horizontal = ('questions',)


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'started_at', 'completed_at', 'score', 'correct_answers')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct', 'answered_at')
    list_filter = ('is_correct',)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('test_attempt', 'evaluated_by', 'score_adjustment', 'evaluated_at')
    search_fields = ('test_attempt__student__username', 'evaluated_by__username')



