from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from django.utils import timezone

from DBApp.models import Enrollment, Assignment, Work, Parent
from DBApp.serializers import WorkSerializer, WorkScoreSerializer, ParentWithIDSerializer

# Create your views here.
@csrf_exempt
def submitWork(request, cid=0, aid=0, sid=0):
    if request.method == 'GET':
        work = Work.objects.filter(class_field=cid,assignment=aid,student=sid)
        work_serializer = WorkScoreSerializer(work, many=True)
        return JsonResponse(work_serializer.data, safe=False)
    elif request.method == 'POST':
        if request.content_type.startswith("multipart/form-data"):
            work_data = {
                "class_field": cid,
                "assignment": aid,
                "student": sid,
                "text_content": request.POST.get("text_content", ""),
                "file": request.FILES.get("file")
            }
        else:
            work_data = JSONParser().parse(request)
            work_data["class_field"] = cid
            work_data["assignment"] = aid
            work_data["student"] = sid

        work_serializer = WorkSerializer(data=work_data)
        if work_serializer.is_valid():
            work_serializer.save()
            return JsonResponse("Gửi bài tập thành công!", safe=False)
        return JsonResponse(work_serializer.errors, status=400)

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

@csrf_exempt
def getSummaryParent(request, pid=0):
    if request.method == "GET":
        parent = Parent.objects.get(parent_id=pid)
        parent_serializer = ParentWithIDSerializer(parent)
        return JsonResponse(parent_serializer.data, safe=False)
    
