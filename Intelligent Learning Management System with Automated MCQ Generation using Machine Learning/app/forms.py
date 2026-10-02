from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course, PythonQuestion, Test, Subject

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='student'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
        return user


# ---------------- COURSE CREATION FORM ----------------
class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'name', 'code', 'description',
            'subjects', 'start_date', 'end_date', 'is_active'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),  # Changed to SelectMultiple
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.all()
        self.fields['subjects'].required = True
# ---------------- PYTHON QUESTION FORM ----------------
class PythonQuestionForm(forms.ModelForm):
    class Meta:
        model = PythonQuestion
        fields = [
            'question_text',
            'option_a', 'option_b', 'option_c', 'option_d',
            'correct_answer',
            'explanation',
            'difficulty',
            'question_type',
            'subject',
            'topic'
        ]


# ---------------- TEST CREATION FORM ----------------
class TestCreationForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=PythonQuestion.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'question-selector'}),
        required=True
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['questions'].queryset = PythonQuestion.objects.filter(created_by=user)
        self.fields['course'].queryset = Course.objects.filter(instructor=user)
        self.fields['course'].empty_label = 'Select a course' if self.fields['course'].queryset.exists() else 'Create a course first'
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['time_limit'].widget.attrs.update({'class': 'form-control'})
        self.fields['max_score'].widget.attrs.update({'class': 'form-control'})
        self.fields['passing_score'].widget.attrs.update({'class': 'form-control'})
        self.fields['available_from'].widget.attrs.update({'class': 'form-control'})
        self.fields['available_to'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Test
        fields = [
            'title', 'description', 'course',
            'questions', 'time_limit', 'max_score', 'passing_score',
            'is_published', 'available_from', 'available_to'
        ]
        widgets = {
            'available_from': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'available_to': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ---------------- TEXT TO MCQ GENERATION FORM ----------------
class TextToMCQForm(forms.Form):
    text = forms.CharField(
        label="Text Input",
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Paste text here...'})
    )
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    difficulty = forms.ChoiceField(choices=PythonQuestion.DIFFICULTY_CHOICES)
