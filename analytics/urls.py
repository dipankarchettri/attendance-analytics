from django.contrib import admin
from django.urls import path
from .views import ai_ds, attendance_per_student_graph, students_present_per_day_graph, attendance_trends_by_day_of_week

urlpatterns = [
    path('aids/', ai_ds, name='ai_ds'),
    path('aids/attendance-per-student/', attendance_per_student_graph, name='attendance_per_student_graph'),
    path('aids/students-present-per-day/', students_present_per_day_graph, name='students_present_per_day_graph'),
    # Add more URLs for other graph views if needed
    path('aids/3/', attendance_trends_by_day_of_week, name='attendance_trends_by_day_of_the_week'),

]