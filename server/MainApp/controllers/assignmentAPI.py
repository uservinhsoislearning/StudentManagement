from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Assignment
from MainApp.serializers import AssignmentSerializer, AssignmentWithIDSerializer

class AssignmentController(APIView):
    def get(self, request, cid):
        assignments = Assignment.objects.filter(class_field = cid)
        assignments_serializer = AssignmentWithIDSerializer(assignments,many=True)
        return Response(assignments_serializer.data)
    
    def post(self, request, cid):
        assignments_data = request.data
        assignments_data['class_field'] = cid
        assignments_data['file'] = None
        assignments_serializer = AssignmentSerializer(data=assignments_data)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return Response("Thêm bài tập thành công!", status=status.HTTP_201_CREATED)
        return Response(assignments_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cid):
        assignments_data = request.data
        assignments = Assignment.objects.get(assignment_id = assignments_data['assignment_id'])
        try:
            assignments_serializer = AssignmentSerializer(assignments, data=assignments_data,class_field = cid)
        except Assignment.DoesNotExist:
            return Response("Không tìm thấy bài tập cho lớp này!", status=status.HTTP_404_NOT_FOUND)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return Response("Cập nhật bài tập thành công!")
        return Response("Lỗi không cập nhật được bài tập!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, cid):
        try:
            assignments = Assignment.objects.get(class_id=cid)
            assignments.delete()
            return Response("Xóa bài tập thành công!")
        except Assignment.DoesNotExist:
            return Response("Không tìm thấy bài tập cho lớp này!", status=status.HTTP_404_NOT_FOUND)
        
class AssignmentFileController(APIView):
    def post(self, request, cid):
        try:
            # Copy POST data and add the class_field
            assignments_data = request.POST.copy()
            assignments_data['class_field'] = cid  # Foreign key to Class

            # Handle uploaded file
            if 'file' in request.FILES:
                assignments_data['file'] = request.FILES['file']
            else:
                return Response('No file uploaded.', status=status.HTTP_400_BAD_REQUEST)

            # Include the file in serializer's files argument
            assignments_serializer = AssignmentSerializer(data=assignments_data)
            if assignments_serializer.is_valid():
                assignments_serializer.save()
                return Response('Đăng bài tập thành công!', status=status.HTTP_201_CREATED)
            else:
                return Response(assignments_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)