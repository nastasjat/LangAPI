from django.urls import path
from PolyglotApp import views


urlpatterns = [
    path("filtered_courses/", views.filtered_courses, name="filtered_courses"),
    path("submit_course_data/", views.submit_course_data, name="submit_course_data"),
    path("", views.index, name="index"),
    path("index2/", views.index2, name="index2"),
    path("index3/", views.index3, name="index3"),
    path("language/", views.languageApi),  # Retrieve all languages
    path(
        "language/<int:id>/", views.languageApi
    ),  # Retrieve, update, or delete a specific language
    path("course/", views.courseApi),
    path("course/<int:id>/", views.courseApi),
    path("teacher/", views.teacherApi),
    path("teacher/<int:id>/", views.teacherApi),
    path("enrolment/", views.enrolmentApi),
    path("enrolment/<int:id>/", views.enrolmentApi),
    path("student/", views.studentApi),
    path("student/<int:id>/", views.studentApi),
]
