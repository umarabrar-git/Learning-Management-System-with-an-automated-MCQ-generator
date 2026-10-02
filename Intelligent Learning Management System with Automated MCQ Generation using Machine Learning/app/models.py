from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    email = models.EmailField(unique=True, verbose_name='email address')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')

    def __str__(self):
        return self.username

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.subject.name})"

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    subjects = models.ManyToManyField(Subject, related_name='courses')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}: {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} in {self.course.code}"

class PythonQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice'),
        ('code', 'Coding Question'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='mcq')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question_text[:50]}... ({self.get_difficulty_display()})"

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='tests', null=True, blank=True)
    questions = models.ManyToManyField(PythonQuestion, related_name='tests')
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes", default=30)
    max_score = models.PositiveIntegerField(default=100)
    passing_score = models.PositiveIntegerField(default=60)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests_created')
    created_at = models.DateTimeField(auto_now_add=True)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()

    def __str__(self):
        return f"{self.title} ({self.course.code if self.course else 'General'})"

class TestAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField(default=0)

    def calculate_score(self):
        correct = self.results.filter(is_correct=True).count()
        total = self.results.count()
        if total > 0:
            self.correct_answers = correct
            self.score = (correct / total) * 100
            self.save()

    def __str__(self):
        return f"{self.student.username}'s attempt on {self.test.title}"

class TestResult(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='results')
    question = models.ForeignKey(PythonQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.is_correct = self.selected_option == self.question.correct_answer
        super().save(*args, **kwargs)
        self.attempt.calculate_score()

    def __str__(self):
        return f"Result for Q{self.question.id} in {self.attempt}"

class Evaluation(models.Model):
    test_attempt = models.OneToOneField(TestAttempt, on_delete=models.CASCADE, related_name='evaluation')
    evaluated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations_done')
    comments = models.TextField(blank=True)
    feedback = models.TextField()
    score_adjustment = models.IntegerField(default=0)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def final_score(self):
        return min(100, max(0, (self.test_attempt.score or 0) + self.score_adjustment))

    def __str__(self):
        return f"Evaluation of {self.test_attempt} by {self.evaluated_by.username}"
