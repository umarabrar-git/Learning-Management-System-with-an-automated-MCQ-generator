from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Dashboard URLs
    path('', views.dashboard, name='dashboard'),

    # Course Management URLs
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/enroll/', views.enroll_course, name='enroll_course'),

    # Question Bank URLs
    path('questions/create/', views.create_question, name='create_question'),
    path('questions/', views.view_questions, name='view_questions'),

    # Test Management URLs
    path('tests/create/', views.create_test, name='create_test'),
    path('tests/<int:test_id>/take/', views.take_test, name='take_test'),
    path('tests/results/<uuid:attempt_id>/', views.test_result, name='test_result'),  # 🔧 Fixed: UUID not int

    # Performance URLs
    path('performance/', views.performance_history, name='performance_history'),
    path('performance/students/', views.view_student_performance, name='view_student_performance'),

    # MCQ Generation URLs
    path('generate-mcqs/', views.auto_generate_mcqs, name='auto_generate_mcqs'),
    path('save-mcqs/', views.save_generated_mcqs, name='save_generated_mcqs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
