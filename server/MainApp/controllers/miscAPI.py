from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Student, Teacher, Report
from MainApp.serializers import ReportSerializer

class AdminSummaryController(APIView):
    def get(request):
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        reports_pending = Report.objects.filter(status='Pending').count()

        dashboard = {
            "totalStudents": total_students,
            "totalTeachers": total_teachers,
            "reportsPending": reports_pending
        }

        return Response(dashboard)
    
class ReportController(APIView):
    def get(request, uid):
        reports = Report.objects.filter(sender=uid) if uid != 0 else Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(request):
        reports_data = request.data
        serializer = ReportSerializer(data=reports_data)
        if serializer.is_valid():
            serializer.save()
            return Response("Report submitted successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)