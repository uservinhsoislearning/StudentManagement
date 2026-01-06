from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone

from MainApp.models import Student, Teacher, Report, Class, ClassTimetable
from MainApp.serializers import ReportSerializer

class AdminSummaryController(APIView):
    def get(self, request):
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
    def get(self, request):
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        reports_data = request.data
        serializer = ReportSerializer(data=reports_data)
        if serializer.is_valid():
            serializer.save()
            return Response("Report submitted successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class MessageController(APIView):
#     def get(self, request, user1_id, user2_id):
#         try:
#             messages_user1_to_user2 = Message.objects.filter(
#                 sender_id=user1_id, receiver_id=user2_id
#             )
#             # Get messages from user2 to user1
#             messages_user2_to_user1 = Message.objects.filter(
#                 sender_id=user2_id, receiver_id=user1_id
#             )
#             # Combine the two querysets
#             all_messages = messages_user1_to_user2.union(messages_user2_to_user1).order_by('timestamp')

#             serializer = MessageSerializer(all_messages, many=True)
#             return Response(serializer.data)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     def post(self, request):
#         try:
#             sender_id = request.data.get('sender_id')
#             receiver_id = request.data.get('receiver_id')
#             content = request.data.get('content')

#             if not all([sender_id, receiver_id, content]):
#                 return Response("Missing required fields", status=status.HTTP_400_BAD_REQUEST)

#             sender = Userlogin.objects.get(user_id=sender_id)
#             receiver = Userlogin.objects.get(user_id=receiver_id)

#             message = Message.objects.create(
#                 sender=sender,
#                 receiver=receiver,
#                 content=content,
#                 timestamp=timezone.now()
#             )

#             message_serializer = MessageSerializer(message)
#             return Response(message_serializer.data)

#         except Userlogin.DoesNotExist:
#             return Response("Không tìm thấy người dùng!", status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DetailsController(APIView):
    def get(self, request, cid):
        try:
            # Get the class and related course name
            class_obj = Class.objects.select_related('course').get(class_id=cid)
            course_name = class_obj.course.course_name

            # Get timetable entries
            timetables = ClassTimetable.objects.filter(class_field=class_obj).values(
                'day_of_week', 'start_time', 'end_time'
            )

            # Format the response
            schedule = list(timetables)
            return Response({
                'course_name': course_name,
                'schedule': schedule
            })

        except Class.DoesNotExist:
            return Response("Không tìm thấy lớp!", status=status.HTTP_404_NOT_FOUND)