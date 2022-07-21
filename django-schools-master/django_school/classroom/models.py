from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.html import escape, mark_safe
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_organizer = models.BooleanField(default=False)


class Organizer(models.Model):
    name = models.CharField(max_length=30, verbose_name="Name")
    color = models.CharField(
        max_length=7,
        help_text='Specify color in Hexadecimal format. eg : #007f65 \n Colors in Hexa-Decimal format : <a href = "https://htmlcolorcodes.com/">HTML ColorPicker</a>',
        default="#007bff",
        verbose_name="Color of the badge",
    )

    description = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the Organisation Conducting the Event",
        verbose_name="Description",
    )

    email = models.EmailField()

    contact = PhoneNumberField(null=False, blank=False, unique=True)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse("organizer-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.name}"

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = (
            '<span class="badge badge-primary" style="background-color: %s">%s</span>'
            % (color, name)
        )
        return mark_safe(html)


class Event(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255, null=True, verbose_name="Name")
    description = RichTextUploadingField(blank=True, null=True)
    organizer = models.ForeignKey(
        Organizer, on_delete=models.SET_NULL, null=True, related_name="events"
    )
    dateofEvent = models.DateField(null=True, blank=True, verbose_name="Date of Joining")
    time = models.TimeField(null=True, blank=True, verbose_name="Time of Joining")
    registrationFee = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Location"
    )
    img = models.ImageField(upload_to="images/", verbose_name="Poster")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("event-detail", args=[str(self.id)])


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="student"
    )
    events = models.ManyToManyField(Event, through="EnrolledEvents")
    interests = models.ManyToManyField(Organizer, related_name="interested_students")

    def __str__(self):
        return self.user.username


class EnrolledEvents(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrolled_events"
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="enrolled_events"
    )
    date = models.DateTimeField(auto_now_add=True)
    present = models.BooleanField(default=True)
    certificate = models.BinaryField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

