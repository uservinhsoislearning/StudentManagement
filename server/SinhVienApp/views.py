from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from django.utils import timezone

from DBApp.models import Student, Enrollment, Assignment, Work

# Create your views here.
@csrf_exempt
def getSummaryStudent(request, sid=0):
    # Get enrolled classes
    enrollments = Enrollment.objects.filter(student=sid)
    course_ids = enrollments.values_list('class_field__course_id', flat=True).distinct()
    enrolled_courses = course_ids.count()

    # Upcoming exams (assignments in those classes)
    class_ids = enrollments.values_list('class_field_id', flat=True)
    now = timezone.now()
    upcoming_exams = Assignment.objects.filter(
        class_field_id__in=class_ids,
        is_exam=True,
        deadline__gte=now
    ).count()

    # All relevant assignments from enrolled classes
    all_assignments = Assignment.objects.filter(class_field_id__in=class_ids)
    assignment_ids = all_assignments.values_list('id', flat=True)

    # Submitted assignments by the student
    submitted_assignments = Work.objects.filter(student=sid, assignment_id__in=assignment_ids).values_list('assignment_id', flat=True).distinct()

    # Pending = total - submitted
    assignments_pending = len(set(assignment_ids) - set(submitted_assignments))

    dashboard = {
        "enrolledCourses": enrolled_courses,
        "upcomingExams": upcoming_exams,
        "assignmentsPending": assignments_pending
    }

    return JsonResponse(dashboard, safe=False)