from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Work
from MainApp.serializers import WorkScoreSerializer, WorkSerializer

class WorkController(APIView):
    def get(self, request, cid, sid, aid):
        try:
            work = Work.objects.filter(class_field=cid,assignment=aid,student=sid)
            work_serializer = WorkScoreSerializer(work, many=True)
            return Response(work_serializer.data)
        except Work.DoesNotExist:
            return Response("Không có bài làm này!", status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, cid, sid, aid):
        if request.content_type.startswith("multipart/form-data"):
            work_data = {
                "class_field": cid,
                "assignment": aid,
                "student": sid,
                "text_content": request.POST.get("text_content", ""),
                "file": request.FILES.get("file")
            }
        else:
            work_data = request.data
            work_data["class_field"] = cid
            work_data["assignment"] = aid
            work_data["student"] = sid

        work_serializer = WorkSerializer(data=work_data)
        if work_serializer.is_valid():
            work_serializer.save()
            return Response("Gửi bài tập thành công!")
        return Response(work_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cid, sid, aid):
        try:
            work_data = request.data
            work_instance = Work.objects.get(class_field_id=cid, student_id=sid, assignment_id=aid)
            work_serializer = WorkScoreSerializer(work_instance, data={'score': work_data['score']}, partial=True)

            if work_serializer.is_valid():
                work_serializer.save()
                return Response(work_serializer.data)
            else:
                return Response(work_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Work.DoesNotExist:
            return Response("Không tìm thấy bài tập!", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response("Error")

    def delete(self, request, cid, sid, aid):
        if not cid or not sid or not aid:
            return Response("Thiếu thông tin trong URL!", safe=False)
        try:
            work = Work.objects.get(class_field=cid, student=sid, assignment=aid)
            work.delete()
            return Response("Work entry deleted successfully")
        except Work.DoesNotExist:
            return Response("Không có bài làm này!", status=status.HTTP_404_NOT_FOUND)