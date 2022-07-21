from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import transaction
import json
from django.db.models import Count, Sum
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views import View
from django.views import generic
from django.http import Http404


from ..decorators import student_required
from ..forms import StudentSignUpForm
from ..models import Event, EnrolledEvents, Student, Organizer

from PIL import Image
import os
from django.conf import settings
from django.utils.encoding import smart_str
from django.http import HttpResponse

import mimetypes

User = get_user_model()


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("students:event_list")


@method_decorator([login_required, student_required], name="dispatch")
class EventListView(ListView):
    model = Event
    ordering = ("name",)
    context_object_name = "events"
    template_name = "classroom/students/event_list.html"

    def get_queryset(self):
        student = self.request.user.student
        enrolled_events = student.events.values_list("pk", flat=True)
        queryset = Event.objects.exclude(pk__in=enrolled_events)
        return queryset


@method_decorator([login_required, student_required], name="dispatch")
class EnrolledEventListView(ListView):
    model = EnrolledEvents
    context_object_name = "enrolled_events"
    template_name = "classroom/students/enrolled_event_list.html"

    def get_queryset(self):
        queryset = self.request.user.student.enrolled_events.select_related(
            "event", "event__organizer"
        ).order_by("event__name")
        return queryset


@login_required
@student_required
def event_detail(request, pk):
    # id = request.GET.get("id")
    if request.method == "GET":
        # print(pk)
        event = Event.objects.get(pk=pk)
        organizer = Organizer.objects.get(name=event.organizer)
        # print(organizer)
        return render(
            request,
            "classroom/students/event_detail.html",
            context={"event": event, "organizer": organizer},
        )


@login_required
@student_required
def enrolled_event_detail(request, pk):
    # id = request.GET.get("id")
    if request.method == "GET":
        # print(pk)
        event = Event.objects.get(pk=pk)
        organizer = Organizer.objects.get(name=event.organizer)
        # print(organizer)
        return render(
            request,
            "classroom/students/enrolled_event_detail.html",
            context={"event": event, "organizer": organizer},
        )


@login_required
@student_required
def enroll_event(request, pk):
    event = Event.objects.get(pk=pk)
    student = request.user.student
    if request.method == "GET":
        EnrolledEvents.objects.create(student=student, event=event)
        student.save()
        return redirect("students:enrolled_event_list")
        # return redirect(request, "classroom/students/enrolled_event_list.html")


@login_required
@student_required
def download_certi(request, pk):
    event = Event.objects.get(pk=pk)
    student = request.user.student
    img_url = os.path.join(settings.MEDIA_ROOT, "certi_template.jpg")
    img = Image.open(img_url, mode="r")
    image_width = img.width
    image_height = img.height
    if request.method == "GET":
        bin_img = EnrolledEvents.objects.get(event=event, student=student).certificate
        image = Image.frombytes("RGB", (image_width, image_height), bin_img, "raw")
        # print(image)
        file_path = os.path.join(settings.MEDIA_ROOT, "certi.jpg")
        image.save(file_path)
        if os.path.exists(file_path):
            with open(file_path, "rb") as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/vnd.ms-excel"
                )
                response["Content-Disposition"] = (
                    "inline; filename="
                    + os.path.basename(
                        event.name + "_" + request.user.first_name + ".jpg"
                    )
                )
                return response
        raise Http404


@login_required
@student_required
def student_feedback(request, pk):
    event = Event.objects.get(pk=pk)
    student = request.user.student
    enrolled_event = EnrolledEvents.objects.filter(event=event).filter(student=student)
    if request.method == "POST":
        if request.POST.get("feedback"):
            enrolled_event.update(feedback=request.POST.get("feedback"))
    return redirect("students:enrolled_event_list")


@login_required
@student_required
def feedback_form(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, "classroom/students/feedback.html", {"event": event})

