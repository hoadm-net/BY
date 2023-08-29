from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Department(models.Model):
    department_key = models.BigAutoField(primary_key=True)
    department_name = models.CharField(max_length=255)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.department_name


class Major(models.Model):
    major_key = models.BigAutoField(primary_key=True)
    major_name = models.CharField(max_length=255)
    all_students = models.BigIntegerField(default=0)
    current_students = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.major_name


EVENT_CHOICES = [
    ("admission", "Admission"),
    ("dropout", "Dropout"),
    ("graduate", "Graduate")
]


class Event(models.Model):
    event_key = models.BigAutoField(primary_key=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=125, choices=EVENT_CHOICES)
    event_date = models.DateField()
    students = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.major} ({self.event_type})"


@receiver(post_save, sender=Event)
def event_post_save(sender, **kwargs):
    major_id = kwargs['instance'].major_id
    event_type = kwargs['instance'].event_type
    students = kwargs['instance'].students

    major = Major.objects.get(pk=major_id)
    print(major.all_students)
    if event_type == "admission":
        major.current_students += students
        major.all_students += students
    elif event_type == "dropout":
        major.current_students -= students
    else:
        # graduate
        major.current_students -= students

    major.save()
