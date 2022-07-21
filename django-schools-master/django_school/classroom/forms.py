from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms import ModelForm
from .models import User, Student, Event, Organizer


class DateInput(forms.DateInput):
    input_type = "date"


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "organizer",
            "dateofEvent",
            "time",
            "registrationFee",
        ]
        widgets = {
            "dateofEvent": DateInput(),
        }


class OrganizerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organizer = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, help_text="First name",)
    last_name = forms.CharField(max_length=32, help_text="Last name",)
    email = forms.EmailField(max_length=64, help_text="Enter a valid email address",)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email",)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user

