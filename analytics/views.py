from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count, Q
from django.db.models.functions import ExtractWeekDay
import plotly.graph_objects as go
import pandas as pd
from .models import Attendance
from plotly.offline import plot
from plotly.subplots import make_subplots


def ai_ds(request):
    return render(request, 'home.html')
def attendance_per_student_graph(request):
    # Query attendance data
    attendance_data = Attendance.objects.all().select_related('student').values('student__full_name', 'date', 'status', 'day_of_week')

    # Convert queryset to pandas DataFrame
    df = pd.DataFrame(list(attendance_data))

    # Data Processing for Attendance per Student graph
    attendance_counts = df.groupby('student__full_name')['status'].apply(lambda x: (x == 'P').sum()).reset_index()
    attendance_counts.columns = ['student_name', 'attended_classes']

    # Plotting Graph for Attendance per Student
    fig_attendance_per_student = go.Figure()
    fig_attendance_per_student.add_trace(go.Bar(y=attendance_counts['student_name'], x=attendance_counts['attended_classes'], orientation='h'))
    fig_attendance_per_student.update_layout(
        title='ATTENDANCE PER STUDENT',
        xaxis=dict(title='Attended Classes'),
        yaxis=dict(title='Student Name', tickfont=dict(size=10), tickmode='array', tickvals=attendance_counts['student_name'], ticktext=['<span style="margin-left: 10px;">' + name + '</span>' for name in attendance_counts['student_name']]),  # Adjust font size and padding here
        title_x=0.5,
        title_font=dict(size=20, family="Arial, sans-serif", color="black")  # Bold title
    )

    # Return the graph as an HTTP response
    return HttpResponse(fig_attendance_per_student.to_html(full_html=False), content_type='text/html')



def students_present_per_day_graph(request):
    # Query attendance data
    attendance_data = (
    Attendance.objects
    .values('date')
    .annotate(num_students_present=Count('status', filter=Q(status='P')))
    .annotate(num_classes=Count('date')) # Filter out dates with multiple classes
    .values('date', 'num_students_present')
)

    # Convert queryset to pandas DataFrame
    df = pd.DataFrame(list(attendance_data))

    # Data Processing for Students Present per Day graph
    fig_students_present_per_day = go.Figure()
    fig_students_present_per_day.add_trace(go.Scatter(x=df['date'], y=df['num_students_present'], mode='lines+markers'))
    fig_students_present_per_day.update_layout(
        title='Students Present per Day',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Number of Students Present'),
        title_x=0.5  # Center the title horizontally
    )

    # Return the graph as an HTTP response
    return HttpResponse(fig_students_present_per_day.to_html(full_html=False), content_type='text/html')



def attendance_trends_by_day_of_week(request):
    #  attendance data and sort by day of the week
    attendance_data = (
        Attendance.objects
        .annotate(day_of_week_num=ExtractWeekDay('date'))
        .values('day_of_week_num')
        .annotate(num_students_present=Count('status', filter=Q(status='P')))
        .order_by('day_of_week_num')
        .values('day_of_week_num', 'num_students_present')
    )

    # queryset to pandas DataFrame
    df = pd.DataFrame(list(attendance_data))

    # day of the week number to day name
    day_mapping = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }

    # Map day of the week number to day name
    df['day_of_week'] = df['day_of_week_num'].map(day_mapping)

    fig_attendance_trends = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "pie"}]])
    # Data Processing for Attendance Trends by Day of the Week graph

    # Adding bar chart trace
    fig_attendance_trends.add_trace(go.Bar(x=df['day_of_week'], y=df['num_students_present'], name='Classes Attended'), row=1, col=1)

    # Adding pie chart trace
    fig_attendance_trends.add_trace(go.Pie(labels=df['day_of_week'], values=df['num_students_present'], name='Percentage of Attendance'), row=1, col=2)

    fig_attendance_trends.update_layout(
        height= 920,
        width= 1800,
        title='Attendance Trends by Day of the Week',
        title_x=0.5  # Center the title horizontally
    )

    # Convert the graph to HTML
    graph_html = plot(fig_attendance_trends, output_type='div', include_plotlyjs=False)

    # Pass the HTML data to the template
    return render(request, 'attendance_trends.html', {'graph_html': graph_html})
    
