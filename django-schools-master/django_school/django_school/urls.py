from django.urls import include, path
from django.contrib import admin
from classroom.views import classroom, students, organizers
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("classroom.urls")),
    # path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/signup/", classroom.SignUpView.as_view(), name="signup"),
    path(
        "accounts/signup/student/",
        students.StudentSignUpView.as_view(),
        name="student_signup",
    ),
    path(
        "accounts/signup/organizer/",
        organizers.OrganizerSignUpView.as_view(),
        name="organizer_signup",
    ),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
