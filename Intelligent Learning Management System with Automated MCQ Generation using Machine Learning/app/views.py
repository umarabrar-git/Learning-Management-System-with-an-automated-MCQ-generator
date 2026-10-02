from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User, Course, Enrollment, PythonQuestion, TestAttempt, TestResult, Subject, Topic,Test
from .mcq_generator import MCQGenerator
from django.contrib import messages
from django.db.models import Count, Avg, Q
import random
from .forms import (
    UserRegistrationForm, 
    PythonQuestionForm, 
    CourseCreationForm,
    TestCreationForm,
    TextToMCQForm
)

# ----------------------- AUTHENTICATION VIEWS -----------------------
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'auth/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# ----------------------- DASHBOARD VIEWS -----------------------

@login_required
def dashboard(request):
    if request.user.user_type == 'instructor':
          return render(request, 'teacher/dashboard.html')  # Or your instructor dashboard view

    # Get enrolled courses
    enrolled_courses = Enrollment.objects.filter(student=request.user, is_active=True).values_list('course', flat=True)

    # Get current time
    now = timezone.now()

    # Get tests for enrolled courses
    active_tests = Test.objects.filter(
        course__in=enrolled_courses,
        is_published=True,
        available_from__lte=now,
        available_to__gte=now
    ).exclude(
        attempts__student=request.user,
        attempts__completed_at__isnull=False
    ).distinct()

    # Completed test attempts
    completed_attempts = TestAttempt.objects.filter(student=request.user, completed_at__isnull=False)

    # Average score
    avg_score = completed_attempts.aggregate(avg=Avg('score'))['avg'] or 0

    return render(request, 'student/dashboard.html', {
        'enrolled_courses': Enrollment.objects.filter(student=request.user),
        'completed_tests': completed_attempts.count(),
        'average_score': round(avg_score, 2),
        'active_tests': active_tests,
    })

# ----------------------- COURSE MANAGEMENT -----------------------

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def create_course(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            form.save_m2m()  # This saves the many-to-many subjects data
            messages.success(request, "Course created successfully!")
            return redirect('dashboard')
    else:
        form = CourseCreationForm()
    
    return render(request, 'teacher/create_course.html', {'form': form})


@login_required
def enroll_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, id=course_id)
        Enrollment.objects.get_or_create(student=request.user, course=course)
        messages.success(request, f"Enrolled in {course.name} successfully!")
        return redirect('dashboard')
    
    available_courses = Course.objects.exclude(
        enrollments__student=request.user
    )
    return render(request, 'student/enroll_course.html', {
        'courses': available_courses
    })

# ----------------------- QUESTION BANK -----------------------

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def create_question(request):
    if request.method == 'POST':
        form = PythonQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            messages.success(request, "Question added successfully!")
            return redirect('view_questions')
    else:
        form = PythonQuestionForm()
    return render(request, 'teacher/create_question.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def view_questions(request):
    questions = PythonQuestion.objects.filter(created_by=request.user)
    return render(request, 'teacher/view_questions.html', {
        'questions': questions
    })

# ----------------------- TEST MANAGEMENT -----------------------

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def create_test(request):
    if not Course.objects.filter(instructor=request.user).exists():
        messages.warning(request, "Create at least one course before creating a test.")
        return redirect('create_course')

    if not PythonQuestion.objects.filter(created_by=request.user).exists():
        messages.warning(request, "Add at least one question before creating a test.")
        return redirect('create_question')

    if request.method == 'POST':
        form = TestCreationForm(request.user, request.POST)
        if form.is_valid():
            try:
                test = form.save(commit=False)
                test.created_by = request.user
                test.save()
                form.save_m2m()  # Save many-to-many for questions
                messages.success(request, "Test created successfully!")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error creating test: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TestCreationForm(request.user)
    
    return render(request, 'teacher/create_test.html', {'form': form})

@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    attempt = TestAttempt.objects.filter(
        student=request.user, 
        test=test
    ).first()

    if not attempt:
        attempt = TestAttempt.objects.create(
            student=request.user,
            test=test,
            total_questions=test.questions.count()
        )
    elif attempt.completed_at:
        messages.warning(request, "You have already completed this test")
        return redirect('test_result', attempt_id=attempt.id)

    if request.method == 'POST':
        score = 0
        for question in test.questions.all():
            selected = request.POST.get(f'question_{question.id}')
            if selected:
                is_correct = selected == question.correct_answer
                if is_correct:
                    score += 1
                
                TestResult.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected,
                    is_correct=is_correct
                )

        attempt.score = (score / test.questions.count()) * 100
        attempt.completed_at = timezone.now()
        attempt.save()
        messages.success(request, f"Test completed! Score: {attempt.score:.2f}%")
        return redirect('test_result', attempt_id=attempt.id)

    questions = test.questions.all()
    return render(request, 'student/take_test.html', {
        'test': test,
        'questions': questions,
        'attempt': attempt
    })

# ----------------------- RESULTS & ANALYTICS -----------------------

@login_required
def test_result(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, id=attempt_id, student=request.user)
    results = TestResult.objects.filter(attempt=attempt)
    return render(request, 'student/test_result.html', {
        'attempt': attempt,
        'results': results
    })

@login_required
def performance_history(request):
    attempts = TestAttempt.objects.filter(student=request.user)
    return render(request, 'student/performance_history.html', {
        'attempts': attempts
    })

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def view_student_performance(request):
    course_id = request.GET.get('course_id')
    students = User.objects.filter(user_type='student')
    
    if course_id:
        students = students.filter(
            enrollments__course_id=course_id
        ).distinct()
    
    performance_data = []
    for student in students:
        attempts = TestAttempt.objects.filter(student=student)
        avg_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0
        performance_data.append({
            'student': student,
            'attempts': attempts.count(),
            'avg_score': avg_score
        })
    
    courses = Course.objects.all()
    return render(request, 'teacher/student_performance.html', {
        'performance_data': performance_data,
        'courses': courses
    })

# ----------------------- AUTOMATED MCQ GENERATION -----------------------

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def auto_generate_mcqs(request):
    generator = MCQGenerator()
    
    if request.method == 'POST':
        form = TextToMCQForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            subject = form.cleaned_data['subject']
            difficulty = form.cleaned_data['difficulty']
            
            generated_mcqs = generator.generate_mcqs(text)
            request.session['generated_mcqs'] = generated_mcqs
            request.session['mcq_context'] = {
                'subject_id': subject.id,
                'difficulty': difficulty
            }
            
            return render(request, 'teacher/review_mcqs.html', {
                'mcqs': generated_mcqs,
                'subject': subject,
                'difficulty': difficulty
            })
    else:
        form = TextToMCQForm()
    
    return render(request, 'teacher/generate_mcqs.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.user_type == 'instructor')
def save_generated_mcqs(request):
    if request.method == 'POST' and 'generated_mcqs' in request.session:
        mcqs = request.session['generated_mcqs']
        context = request.session['mcq_context']
        subject = Subject.objects.get(id=context['subject_id'])
        saved_count = 0
        
        for mcq in mcqs:
            if request.POST.get(f'save_{mcqs.index(mcq)}', False):
              PythonQuestion.objects.create(
                question_text=mcq['question'],
                option_a=mcq['options'][0],
                option_b=mcq['options'][1],
                option_c=mcq['options'][2],
                option_d=mcq['options'][3],
                correct_answer=mcq['correct_answer'],
                subject=subject,
                difficulty=context['difficulty'],
                created_by=request.user
                )
              saved_count += 1
        
        messages.success(request, f"Saved {saved_count} questions to question bank!")
        return redirect('view_questions')
    
    return redirect('auto_generate_mcqs')