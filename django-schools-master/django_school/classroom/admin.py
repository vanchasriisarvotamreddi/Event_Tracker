from django.contrib import admin

# Register your models here.
from .models import User, Organizer, Event, Student, EnrolledEvents

admin.site.register(User)
admin.site.register(Organizer)
admin.site.register(Event)
admin.site.register(Student)
admin.site.register(EnrolledEvents)
# admin.site.register(Attendance)
