from rest_framework import serializers
from PolyglotApp.models import (
    Language,
    Course,
    Enrolment,
    Student,
    Teacher,
    Language_Course,
    Course_Teacher,
)


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("language_ID", "name", "iso_code")


class CourseSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "course_ID",
            "name",
            "level",
            "price",
            "duration_in_weeks",
            "number_of_lessons",
            "number_of_hours_with_native",
            "type",
            "languages",
        )

    def get_languages(self, obj):
        course_languages = Language_Course.objects.filter(course=obj)
        language_ids = course_languages.values_list("language", flat=True)
        languages = Language.objects.filter(language_ID__in=language_ids)
        return LanguageSerializer(languages, many=True).data


class TeacherSerializer(serializers.ModelSerializer):
    # Use LanguageSerializer for the language field to see all the info about language
    # not only its PK
    language = LanguageSerializer()

    courses = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = (
            "teacher_ID",
            "name",
            "surname",
            "middle_name",
            "level",
            "phone_number",
            "email",
            "language",
            "courses",
        )

    def get_courses(self, obj):
        teacher_courses = Course_Teacher.objects.filter(teacher=obj)
        course_ids = teacher_courses.values_list("course", flat=True)
        courses = Course.objects.filter(course_ID__in=course_ids)
        courses_data = CourseSerializer(courses, many=True).data

        for course_data in courses_data:
            # Remove the 'languages' key from each course data
            course_data.pop("languages", None)

        return courses_data


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("student_ID", "name", "surname", "phone_number", "email")


class EnrolmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    language = LanguageSerializer()
    student = StudentSerializer()

    class Meta:
        model = Enrolment
        fields = ("enrolment_ID", "course", "language", "student")
