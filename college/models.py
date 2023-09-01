from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Choices
class SemesterName(models.IntegerChoices):
    Autumn = 0
    Spring = 1
    Summer = 2
    Winter = 3


class StudentStatus(models.IntegerChoices):
    No_admission = 0
    Studying = 1
    Temporarily_absent = 2
    Drop_out = 3
    Forced_to_drop_out = 4
    Graduate = 5


class EventType(models.IntegerChoices):
    Admission = 1
    Temporarily_absent = 2
    Drop_out = 3
    Forced_to_drop_out = 4
    Graduate = 5


class StudentRanking(models.IntegerChoices):
    A = 0
    B = 1
    C = 2
    D = 3


class PointType(models.IntegerChoices):
    GPA = 0
    S1  = 1
    S2  = 2
    S3  = 3
    S4  = 4
    S5  = 5
    S6  = 6
    S7  = 7
    S8  = 8
    S9  = 9
    S10 = 10


class Department(models.Model):
    department_name = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.department_name


class Major(models.Model):
    major_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.major_name


class Semester(models.Model):
    year = models.IntegerField()
    name = models.IntegerField(choices=SemesterName.choices)

    def __str__(self):
        return f"{SemesterName(self.name).name} - {self.year}"


class Student(models.Model):
    student_key = models.CharField(max_length=10, primary_key=True)
    gender = models.BooleanField()
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    status = models.IntegerField(choices=StudentStatus.choices, default=0)

    def __str__(self):
        return self.student_key


class Point(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    point_type = models.IntegerField(choices=PointType.choices, default=1)
    value = models.FloatField(default=0)


class Fact(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)
    event = models.IntegerField(choices=EventType.choices, default=1)


@receiver(post_save, sender=Fact)
def save_profile(sender, instance, **kwargs):
    student = Student.objects.get(pk=instance.student.student_key)
    student.status = instance.event
    student.save()
