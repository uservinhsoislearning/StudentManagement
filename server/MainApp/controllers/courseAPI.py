from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import pandas as pd

from MainApp.models import Course, Class, ClassTimetable
from MainApp.serializers import CourseSerializer, CourseWithIDSerializer

class CourseController(APIView):
    def get(self, request):
        courses = Course.objects.all()
        courses_serializer = CourseWithIDSerializer(courses,many=True)
        return Response(courses_serializer.data)
    
    def post(self, request):
        courses_data = request.data
        courses_serializer = CourseSerializer(data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return Response("Thêm môn học thành công!", status=status.HTTP_201_CREATED)
        return Response(courses_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, crid):
        courses_data = request.data
        courses = Course.objects.get(course_id=crid)
        courses_serializer = CourseSerializer(courses, data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return Response("Cập nhật thông tin môn học thành công!")
        return Response("Lỗi không cập nhật được thông tin!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, crid):
        courses = Course.objects.get(course_id=crid)
        courses.delete()
        return Response("Xóa môn học thành công!")

class CourseFileController(APIView):
    def post(request):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response("Không có file CSV!", status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(csv_file)

            required_columns = [
                'course_name',
                'course_semester',
                'class_is_active',
                'course_midterm_coeff',
                'course_final_coeff',
            ]
            if not all(col in df.columns for col in required_columns):
                return Response("Thiếu trường thông tin!", status=status.HTTP_400_BAD_REQUEST)

            success_count = 0
            errors = []

            for index, row in df.iterrows():
                data = row.to_dict()

                if isinstance(data.get('class_is_active'), str):
                    data['class_is_active'] = data['class_is_active'].strip().lower() in ['true', '1', 'yes']

                serializer = CourseSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    success_count += 1
                else:
                    errors.append({'row': index + 1, 'errors': serializer.errors})

            return Response({
                'message': f'{success_count} courses imported successfully.',
                'errors': errors,
            })

        except Exception as e:
            return Response({'error': str(e)})

class CourseClassController(APIView):
    def get(request):
        course_list = []
        courses = Course.objects.all()
        for course in courses:
            # Get all classes related to this course
            classes = Class.objects.filter(course_id=course.course_id)
            class_data = []
            for cls in classes:
                # Get timetables for this class
                timetables = ClassTimetable.objects.filter(class_field_id=cls.class_id)
                timetable_data = [
                    {
                        'day_of_week': t.day_of_week,
                        'start_time': t.start_time,
                        'end_time': t.end_time
                    }
                    for t in timetables
                ]
                class_data.append({
                    'class_id': cls.class_id,
                    'class_name': cls.class_name,
                    'class_semester': cls.class_semester,
                    'timetables': timetable_data
                })
            course_list.append({
                'course_id': course.course_id,
                'course_name': course.course_name,
                'course_semester': course.course_semester,
                'course_midterm_coeff': course.course_midterm_coeff,
                'course_final_coeff': course.course_final_coeff,
                'course_credit': course.course_credit,
                'classes': class_data
            })
        return Response(course_list)