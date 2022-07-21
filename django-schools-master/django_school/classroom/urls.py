from django.urls import include, path
from django.conf.urls import url
from .views import classroom, students, organizers

urlpatterns = [
    # url(r"^save_state/$", classroom.save_state, name="save_state"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("", classroom.home, name="home"),
    path(
        "students/",
        include(
            (
                [
                    path("event/", students.EventListView.as_view(), name="event_list"),
                    # path("s/", students.StudentList.as_view(), name="student_list"),
                    # path(
                    #     "interests/",
                    #     students.StudentInterestsView.as_view(),
                    #     name="student_interests",
                    # ),
                    # path(
                    #     "event/<int:pk>/",
                    #     students.EventDetailView.as_view(),
                    #     name="event-detail",
                    # ),
                    path(
                        "enrolled/",
                        students.EnrolledEventListView.as_view(),
                        name="enrolled_event_list",
                    ),
                    path("enroll/<int:pk>", students.enroll_event, name="enroll_event"),
                    path("event/<int:pk>/", students.event_detail, name="event-detail"),
                    path(
                        "enrolledevent/<int:pk>/",
                        students.enrolled_event_detail,
                        name="enrolled_event_detail",
                    ),
                    path(
                        "enrolledevent/<int:pk>/download",
                        students.download_certi,
                        name="certi",
                    ),
                    path(
                        "enrolledevent/<int:pk>/feedback",
                        students.feedback_form,
                        name="feedback_form",
                    ),
                    path(
                        "enrolledevent/<int:pk>/feedback/save",
                        students.student_feedback,
                        name="feedback",
                    )
                    # path(
                    #     "event/<int:pk>/studentresults/",
                    #     students.EventResultsView.as_view(),
                    #     name="student_event_results",
                    # ),
                ],
                "classroom",
            ),
            namespace="students",
        ),
    ),
    path(
        "organizers/",
        include(
            (
                [
                    path(
                        "", organizers.EventListView.as_view(), name="event_change_list"
                    ),
                    path(
                        "updatedetails/",
                        organizers.DetailsCreateView.as_view(),
                        name="update_details",
                    ),
                    path(
                        "event/add/",
                        organizers.EventCreateView.as_view(),
                        name="event_add",
                    ),
                    path(
                        "event/<int:pk>/",
                        organizers.EventUpdateView.as_view(),
                        name="event_change",
                    ),
                    path(
                        "event/<int:pk>/results/",
                        organizers.EventResultsView.as_view(),
                        name="event_results",
                    ),
                    path(
                        "event/<int:pk>/results/attendance",
                        organizers.EventAttendanceView.as_view(),
                        name="event_attendance",
                    ),
                    path(
                        "event/<int:pk>/results/attendees/",
                        organizers.AttendeesView.as_view(),
                        name="event_attendees",
                    ),
                    path(
                        "event/<int:pk>/results/gen_certi",
                        organizers.generate_certificate,
                        name="generate",
                    ),
                    path(
                        "event/<int:pk>/results/absent_mail",
                        organizers.absent_mail,
                        name="absent_mail",
                    ),
                    # path("savedata/", organizers.savedata, name="save",),
                    path("savedata/<int:pk>", organizers.save_data, name="savedata",),
                    # path(
                    #     "quiz/<int:quiz_pk>/question/<int:question_pk>/",
                    #     teachers.question_change,
                    #     name="question_change",
                    # ),
                    # path(
                    #     "quiz/<int:quiz_pk>/question/<int:question_pk>/delete/",
                    #     teachers.QuestionDeleteView.as_view(),
                    #     name="question_delete",
                    # ),
                ],
                "classroom",
            ),
            namespace="organizers",
        ),
    ),
]
