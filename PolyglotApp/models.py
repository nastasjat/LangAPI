from django.db import models

# Create your models here.


class Course(models.Model):
    course_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    level = models.CharField(max_length=2)
    price = models.IntegerField()
    duration_in_weeks = models.CharField(max_length=20)
    number_of_lessons = models.IntegerField()
    number_of_hours_with_native = models.IntegerField()
    type = models.CharField(max_length=15)


class Language(models.Model):
    language_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    iso_code = models.CharField(max_length=2, null=True)


class Teacher(models.Model):
    teacher_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=12)
    email = models.CharField(max_length=30, null=True)


class Course_Teacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class Student(models.Model):
    student_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=12)
    email = models.CharField(max_length=30, null=True)


class Enrolment(models.Model):
    enrolment_ID = models.AutoField(primary_key=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)


class Language_Course(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
