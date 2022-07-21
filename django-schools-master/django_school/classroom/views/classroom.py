from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from ..decorators import organizer_required
from django.contrib.auth.decorators import login_required


class SignUpView(TemplateView):
    template_name = "registration/signup.html"


def home(request):
    if request.user.is_authenticated:
        if request.user.is_organizer:
            return redirect("organizers:event_change_list")
        elif request.user.is_student:
            return redirect("students:event_list")
        else:
            return redirect("admin:index")
    return render(request, "classroom/home.html")


# @login_required
# @organizer_required
# def save_state(request):
#     if request.method == "POST":
#         title = request.POST.get("student_name", "")
#         checked = request.POST.get("checked", "")
#         print(title)
#         print(checked)
#         # todo = Todo.objects.get(title=title)
#         # todo.completed = checked
#         # todo.save()
