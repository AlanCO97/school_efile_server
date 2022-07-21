from django.urls import path

from efile.views import StudentDetail, Students, Tutors

urlpatterns = [
    path('createEfile/', Students.as_view(), name='createEfile'),
    path('student/<int:pk>', StudentDetail.as_view(), name="student"),
    path('tutors/', Tutors.as_view(), name='tutors'),
]