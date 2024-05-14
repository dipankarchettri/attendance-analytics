from django.db import models


class Student(models.Model):
    usn = models.CharField(max_length=10)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null= True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],null=False)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def set_date_of_birth(self, value):
        # Convert the value to the correct date format
        try:
            self.date_of_birth = datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError:
            raise ValueError('Enter a valid date in the format DD/MM/YYYY.')
    def __str__(self):
        return f"{self.full_name} "
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    credit = models.IntegerField()

    def __str__(self):
        return self.name
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=[('P', 'Present'), ('A', 'Absent')])
    day_of_week = models.CharField(max_length=10, null=True)  # New field for day of the week

    def save(self, *args, **kwargs):
        # Automatically populate day_of_week based on date
        if self.date:
            self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)