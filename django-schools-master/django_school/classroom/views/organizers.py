from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from PIL import Image, ImageDraw, ImageFont
import os
import io
from django.conf import settings
from django.utils.encoding import smart_str

from django.core.mail import EmailMessage

from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from django.templatetags.static import static
from bootstrap_datepicker_plus import DateTimePickerInput

from ..decorators import organizer_required
from ..forms import (
    OrganizerSignUpForm,
    EventForm,
)
from ..models import Event, Organizer, EnrolledEvents


User = get_user_model()


class OrganizerSignUpView(CreateView):
    model = User
    form_class = OrganizerSignUpForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "organizer"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            "The account was created Successfully!Please Update your Informtion to get started!",
        )
        return redirect("organizers:update_details")


@method_decorator([login_required, organizer_required], name="dispatch")
class EventListView(ListView):
    model = Event
    ordering = ("name",)
    context_object_name = "events"
    template_name = "classroom/organizers/event_change_list.html"

    def get_queryset(self):
        queryset = self.request.user.events.select_related("organizer")
        return queryset


@method_decorator([login_required, organizer_required], name="dispatch")
class EventCreateView(generic.edit.CreateView):
    model = Event
    form_class = EventForm
    template_name = "classroom/organizers/event_add_form.html"

    def form_valid(self, form):
        event = form.save(commit=False)
        event.owner = self.request.user
        event.save()
        messages.success(self.request, "The event was created with success!Go Ahead!")
        return redirect("organizers:event_change", event.pk)


@method_decorator([login_required, organizer_required], name="dispatch")
class DetailsCreateView(CreateView):
    model = Organizer
    fields = (
        "name",
        "description",
        "email",
        "contact",
        "color",
    )
    template_name = "classroom/organizers/update_details_form.html"

    def form_valid(self, form):
        organizer = form.save(commit=False)
        organizer.save()
        messages.success(self.request, "The Details are Updated Successfully!Go Ahead!")
        return redirect("organizers:event_change_list")


@method_decorator([login_required, organizer_required], name="dispatch")
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    context_object_name = "event"
    template_name = "classroom/organizers/event_change_form.html"

    def get_context_data(self, **kwargs):
        kwargs["questions"] = self.get_object().questions.annotate(
            answers_count=Count("answers")
        )
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.events.all()

    def get_success_url(self):
        return reverse("organizers:event_change", kwargs={"pk": self.object.pk})


@method_decorator([login_required, organizer_required], name="dispatch")
class EventResultsView(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "classroom/organizers/event_results.html"

    def get_context_data(self, **kwargs):
        event = self.get_object()
        enrolled_students = event.enrolled_events.select_related(
            "student__user"
        ).order_by("-date")
        total_enrolled_students = enrolled_students.count()
        extra_context = {
            "enrolled_students": enrolled_students,
            "total_enrolled_students": total_enrolled_students,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.events.all()


@method_decorator([login_required, organizer_required], name="dispatch")
class EventAttendanceView(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "classroom/organizers/event_attendance.html"

    def get_context_data(self, **kwargs):
        event = self.get_object()
        enrolled_students = event.enrolled_events.select_related(
            "student__user"
        ).order_by("-date")
        total_enrolled_students = enrolled_students.count()
        extra_context = {
            "enrolled_students": enrolled_students,
            "total_enrolled_students": total_enrolled_students,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.events.all()


@login_required
@organizer_required
def save_data(request, pk):
    if request.method == "POST":
        # print(request.POST.getlist("present"))
        student_list = request.POST.getlist("present")
        event = Event.objects.get(pk=pk)
        # print(event)

        EnrolledEvents.objects.filter(event=event).filter(
            student__in=student_list
        ).update(present=True)

        EnrolledEvents.objects.filter(event=event).exclude(
            student__in=student_list
        ).update(present=False)
        messages.success(request, "Attendance was Updated Successfully! Go Ahead!")
        return redirect("organizers:event_change_list")


@method_decorator([login_required, organizer_required], name="dispatch")
class AttendeesView(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "classroom/organizers/attendees.html"

    def get_context_data(self, **kwargs):
        event = self.get_object()
        enrolled_students = event.enrolled_events.select_related(
            "student__user"
        ).order_by("-date")
        student_p = EnrolledEvents.objects.filter(event=event, present=True)
        student_a = EnrolledEvents.objects.filter(event=event, present=False)
        attendees_count = student_p.count()
        absentees_count = student_a.count()
        extra_context = {
            "presentees": student_p,
            "absentees": student_a,
            "attendees_count": attendees_count,
            "absentees_count": absentees_count,
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.events.all()


@login_required
@organizer_required
def generate_certificate(request, pk):
    event = Event.objects.get(pk=pk)
    if request.method == "POST":
        enrolled_students = event.enrolled_events.select_related(
            "student__user"
        ).filter(present=True)
        img_url = os.path.join(settings.MEDIA_ROOT, "certi_template.jpg")
        font_path = os.path.join(
            os.path.join(settings.BASE_DIR, "static"), "fonts/Pacifico.ttf"
        )
        font_path1 = os.path.join(
            os.path.join(settings.BASE_DIR, "static"), "fonts/Alexandroupoli.ttf"
        )
        for s in enrolled_students:
            name = s.student.user.first_name + " " + s.student.user.last_name
            text_y_position1 = 550
            text_y_position2 = 780
            text_y_position3 = 950
            img = Image.open(img_url, mode="r")
            image_width = img.width
            image_height = img.height
            draw = ImageDraw.Draw(img)
            date = str(event.dateofEvent)
            font1 = ImageFont.truetype(font_path, 100)
            font2 = ImageFont.truetype(font_path, 70)
            font3 = ImageFont.truetype(font_path, 60)
            font4 = ImageFont.truetype(font_path1, 60)
            text_width1, _ = draw.textsize(name, font=font1)
            text_width2, _ = draw.textsize(event.name, font=font2)
            draw.text(
                ((image_width - text_width1) / 2, text_y_position1,),
                name,
                font=font1,
                fill=(96, 96, 96),
            )
            draw.text(
                ((image_width - text_width2) / 2, text_y_position2,),
                event.name,
                font=font2,
                fill=(96, 96, 96),
            )
            draw.text(
                (1200, text_y_position3,), date, font=font3, fill=(96, 96, 96),
            )
            draw.text(
                (570, text_y_position3,), "Vnrvjiet", font=font4, fill=(96, 96, 96),
            )
            # img.show()
            file_path = os.path.join(settings.MEDIA_ROOT, "gmail_certi/certificate.jpg")
            img.save(file_path)
            student_instance = EnrolledEvents.objects.filter(event=event).filter(
                student=s.student
            )
            student_instance.update(certificate=img.tobytes())
            subject = "Certificate of " + event.name + " from Terrific Trio!"
            message = "Congratulations!!! You have succesfully achieved Certificate from Terrific Trio.Please download it from the website!"
            recepient = s.student.user.email
            msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [recepient])
            msg.content_subtype = "html"
            msg.attach_file(file_path)
            msg.send()

        return redirect("organizers:event_change_list")


@login_required
@organizer_required
def absent_mail(request, pk):
    event = Event.objects.get(pk=pk)
    if request.method == "POST":
        enrolled_students = event.enrolled_events.select_related(
            "student__user"
        ).filter(present=False)
        for s in enrolled_students:
            subject = event.name
            message = (
                "Hey "
                + s.student.user.first_name
                + " "
                + s.student.user.last_name
                + "! We are sorry to inform that you are not eligible to receive certificate as you didn't turn up at the event on dated!"
            )
            recepient = s.student.user.email
            msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [recepient])
            msg.send()
        return redirect("organizers:event_change_list")

