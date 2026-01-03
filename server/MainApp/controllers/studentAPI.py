from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

from MainApp.models import Student, Enrollment, Work, Assignment
from MainApp.serializers import StudentSerializer, StudentWithIDSerializer, EnrollmentGradeSubjectSerializer

class StudentController(APIView):
    def get(self, request):
        students = Student.objects.all()
        students_serializer = StudentWithIDSerializer(students,many=True)
        return Response(students_serializer.data)
    
    def post(self, request):
        students_serializer = StudentSerializer(data=request.data)
        if students_serializer.is_valid():
            students_serializer.save()
            return Response("Thêm học sinh vào cơ sở dữ liệu thành công!", status=status.HTTP_201_CREATED)
        return Response(students_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, sid):
        students = Student.objects.get(student_id = sid)
        students_serializer = StudentSerializer(students, data=request.data)
        if students_serializer.is_valid():
            students_serializer.save()
            return Response("Cập nhật thông tin thành công!")
        return Response("Lỗi không cập nhật được thông tin!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, sid):
        try:
            students = Student.objects.get(student_id=sid)
            students.delete()
            return Response("Xóa học sinh thành công!")
        except Student.DoesNotExist:
            return Response("Không tìm thấy học sinh!", status=status.HTTP_404_NOT_FOUND)
        
class StudentGradeController(APIView):
    def get(self, request, sid):
        enrollment = Enrollment.objects.filter(student = sid)
        enrollment_serializer = EnrollmentGradeSubjectSerializer(enrollment,many=True)
        return Response(enrollment_serializer.data)
    
class StudentSummaryController(APIView):
    def get(self, request, sid):
        enrollments = Enrollment.objects.filter(student = sid)
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
        assignment_ids = all_assignments.values_list('assignment_id', flat=True)

        # Submitted assignments by the student
        submitted_assignments = Work.objects.filter(student=sid, assignment_id__in=assignment_ids).values_list('assignment_id', flat=True).distinct()

        # Pending = total - submitted
        assignments_pending = len(set(assignment_ids) - set(submitted_assignments))

        dashboard = {
            "enrolledCourses": enrolled_courses,
            "upcomingExams": upcoming_exams,
            "assignmentsPending": assignments_pending
        }

        return Response(dashboard)