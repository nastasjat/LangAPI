import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.db.models import Q

from PolyglotApp.models import (
    Language,
    Course,
    Teacher,
    Student,
    Enrolment,
)
from PolyglotApp.serializers import (
    LanguageSerializer,
    CourseSerializer,
    TeacherSerializer,
    StudentSerializer,
    EnrolmentSerializer,
)

# Create your views here.


def index(request):
    return render(request, "index.html")


def index2(request):
    return render(request, "index2.html")


def submit_course_data(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        language = data.get("language")
        course_name = data.get("name")
        price = data.get("price")

        # You can save these values to the session for later retrieval
        request.session["language"] = language
        request.session["course_name"] = course_name
        request.session["price"] = price

        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def index3(request):
    if request.method == "POST":
        # Extract form data from POST parameters
        name = request.POST.get("student_name")
        surname = request.POST.get("student_surname")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        language_level = request.POST.get("lang_level")

        # Retrieve course data from the session
        language_name = request.session.get("language")
        course_name = request.session.get("course_name")
        price = request.session.get("price")

        # Create Student instance and save to the database
        student = Student.objects.create(
            name=name, surname=surname, phone_number=phone_number, email=email
        )

        # Find the Course based on the provided parameters
        course = Course.objects.get(name=course_name, price=price, level=language_level)
        language = Language.objects.get(name=language_name)

        # Create Enrolment instance and link it with Student and Course
        enrolment = Enrolment.objects.create(
            student=student,
            course=course,
            language=language,
        )

        # Clear session data after processing
        del request.session["language"]
        del request.session["course_name"]
        del request.session["price"]

    return render(request, "index3.html")


# A helper function to get the appropriate text for hours
def get_hours_text(num_hours):
    if num_hours == 1:
        return "година"
    elif 2 <= num_hours <= 4:
        return "години"
    else:
        return "годин"


# Filter courses function
def filtered_courses(request):
    if request.method == "POST":
        language = request.POST.get("language")
        price_from = request.POST.get("price_from")
        price_to = request.POST.get("price_to")
        language_level = request.POST.get("level")

        # Build filter conditions dynamically
        filter_conditions = Q()
        if language:
            filter_conditions &= Q(language_course__language__name=language)
        if price_from:
            filter_conditions &= Q(price__gte=int(price_from))
        if price_to:
            filter_conditions &= Q(price__lte=int(price_to))
        if language_level:
            filter_conditions &= Q(level=language_level)

        filtered_courses = Course.objects.filter(filter_conditions)

        for course in filtered_courses:
            course.hours_text = get_hours_text(course.number_of_hours_with_native)

        # Pass the selected language to the template
        selected_language = Language.objects.filter(name=language).first()
        return render(
            request,
            "filtered_courses.html",
            {
                "courses": filtered_courses,
                "selected_language": selected_language,
            },
        )

    return render(request, "filtered_courses.html", {"courses": []})


@csrf_exempt
def languageApi(request, id=0):
    if request.method == "GET":
        if id == 0:
            languages = Language.objects.all()
            languages_serializer = LanguageSerializer(languages, many=True)
            return JsonResponse(languages_serializer.data, safe=False)
        else:
            language = Language.objects.get(language_ID=id)
            language_serializer = LanguageSerializer(language)
            return JsonResponse(language_serializer.data, safe=False)
    elif request.method == "POST":
        language_data = JSONParser().parse(request)
        language_serializer = LanguageSerializer(data=language_data)
        if language_serializer.is_valid():
            language_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        language_data = JSONParser().parse(request)
        language = Language.objects.get(language_ID=language_data["language_ID"])
        language_serializer = LanguageSerializer(language, data=language_data)
        if language_serializer.is_valid():
            language_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        language = Language.objects.get(language_ID=id)
        language.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def courseApi(request, id=0):
    if request.method == "GET":
        if id == 0:
            courses = Course.objects.all()
            courses_serializer = CourseSerializer(courses, many=True)
            return JsonResponse(courses_serializer.data, safe=False)
        else:
            course = Course.objects.get(course_ID=id)
            course_serializer = CourseSerializer(course)
            return JsonResponse(course_serializer.data, safe=False)
    elif request.method == "POST":
        course_data = JSONParser().parse(request)
        course_serializer = CourseSerializer(data=course_data)
        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        course_data = JSONParser().parse(request)
        course = Course.objects.get(course_ID=course_data["course_ID"])
        course_serializer = CourseSerializer(course, data=course_data)
        if course_serializer.is_valid():
            course_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        course = Course.objects.get(course_ID=id)
        course.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def teacherApi(request, id=0):
    if request.method == "GET":
        if id == 0:
            teachers = Teacher.objects.all()
            teachers_serializer = TeacherSerializer(teachers, many=True)
            return JsonResponse(teachers_serializer.data, safe=False)
        else:
            teacher = Teacher.objects.get(teacher_ID=id)
            teacher_serializer = TeacherSerializer(teacher)
            return JsonResponse(teacher_serializer.data, safe=False)
    elif request.method == "POST":
        teacher_data = JSONParser().parse(request)
        teacher_serializer = TeacherSerializer(data=teacher_data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        teacher_data = JSONParser().parse(request)
        teacher = Teacher.objects.get(teacher_ID=teacher_data["teacher_ID"])
        teacher_serializer = TeacherSerializer(teacher, data=teacher_data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        teacher = Teacher.objects.get(teacher_ID=id)
        teacher.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def enrolmentApi(request, id=0):
    if request.method == "GET":
        if id == 0:
            enrolments = Enrolment.objects.all()
            enrolments_serializer = EnrolmentSerializer(enrolments, many=True)
            return JsonResponse(enrolments_serializer.data, safe=False)
        else:
            enrolment = Enrolment.objects.get(enrolment_ID=id)
            enrolment_serializer = EnrolmentSerializer(enrolment)
            return JsonResponse(enrolment_serializer.data, safe=False)
    elif request.method == "POST":
        enrolment_data = JSONParser().parse(request)
        enrolment_serializer = EnrolmentSerializer(data=enrolment_data)
        if enrolment_serializer.is_valid():
            enrolment_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        enrolment_data = JSONParser().parse(request)
        enrolment = Enrolment.objects.get(enrolment_ID=enrolment_data["enrolment_ID"])
        enrolment_serializer = EnrolmentSerializer(enrolment, data=enrolment_data)
        if enrolment_serializer.is_valid():
            enrolment_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        enrolment = Enrolment.objects.get(enrolment_ID=id)
        enrolment.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@csrf_exempt
def studentApi(request, id=0):
    if request.method == "GET":
        if id == 0:
            students = Student.objects.all()
            students_serializer = StudentSerializer(students, many=True)
            return JsonResponse(students_serializer.data, safe=False)
        else:
            student = Student.objects.get(student_ID=id)
            student_serializer = StudentSerializer(student)
            return JsonResponse(student_serializer.data, safe=False)
    elif request.method == "POST":
        student_data = JSONParser().parse(request)
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == "PUT":
        student_data = JSONParser().parse(request)
        student = Student.objects.get(student_ID=student_data["student_ID"])
        student_serializer = StudentSerializer(student, data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == "DELETE":
        student = Student.objects.get(student_ID=id)
        student.delete()
        return JsonResponse("Deleted Successfully", safe=False)


@api_view(["POST"])
def signup_for_course(request):
    if request.method == "POST":
        student_data = request.data.get("student")
        enrolment_data = request.data.get("enrolment")

        # Create or update student
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student = student_serializer.save()

            # Create enrolment with student and related data
            enrolment_data["student"] = student["student_ID"]
            enrolment_serializer = EnrolmentSerializer(data=enrolment_data)
            if enrolment_serializer.is_valid():
                enrolment_serializer.save()
                return Response(
                    {"message": "Signup successful"}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    enrolment_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                student_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
