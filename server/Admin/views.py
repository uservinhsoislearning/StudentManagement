from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

import pandas as pd
# from DBApp.models import Classstudent
# from DBApp.serializers import ClassstudentSerializer
from DBApp.models import Assignment,Class,Teacher,Student, Classstudent, Course
from DBApp.serializers import AssignmentSerializer,ClassSerializer,TeacherSerializer,StudentSerializer, ClassstudentSerializer, CourseSerializer
# Create your views here.

@csrf_exempt
def studentAPI(request,id=0):
    if request.method == 'GET':
        students = Student.objects.all()
        students_serializer = StudentSerializer(students,many=True)
        return JsonResponse(students_serializer.data, safe=False)
    elif request.method == 'DELETE':
        students=Student.objects.get(id=id)
        students.delete()
        return JsonResponse("Deleted Successfully!",safe=False)
    
@csrf_exempt
def classAPI(request,id=0):
    if request.method == 'GET':
        classes=Class.objects.all()
        classes_serializer = ClassSerializer(classes,many=True)
        return JsonResponse(classes_serializer.data, safe=False)
    elif request.method == 'POST':
        classes_data=JSONParser().parse(request)
        classes_serializer=ClassSerializer(data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Thêm lớp vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        classes_data=JSONParser().parse(request)
        classes=Class.objects.get(class_id = classes_data['class_id'])
        classes_serializer = ClassSerializer(classes, data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        classes=Class.objects.get(class_id=id)
        classes.delete()
        return JsonResponse("Xóa lớp thành công!",safe=False)
    
@csrf_exempt
def teacherAPI(request,id=0):
    if request.method == 'GET':
        teachers=Teacher.objects.all()
        teachers_serializer = TeacherSerializer(teachers,many=True)
        return JsonResponse(teachers_serializer.data, safe=False)
    elif request.method == 'POST':
        teachers_data=JSONParser().parse(request)
        teachers_serializer=TeacherSerializer(data=teachers_data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return JsonResponse("Thêm thầy/cô vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        teachers_data=JSONParser().parse(request)
        teachers=Teacher.objects.get(teacher_id = teachers_data['teacher_id'])
        teachers_serializer = TeacherSerializer(teachers, data=teachers_data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        teachers=Teacher.objects.get(class_id=id)
        teachers.delete()
        return JsonResponse("Xóa thầy/cô thành công!",safe=False)

@csrf_exempt
def classStudentAPI(request, class_id=0, student_id=0):
    if request.method == 'POST':
        class_student_data=JSONParser().parse(request)
        class_student_serializer=ClassstudentSerializer(data=class_student_data)
        if class_student_serializer.is_valid():
            class_student_serializer.save()
            return JsonResponse("Thêm học sinh vào lớp dữ liệu thành công!",safe=False)
        return JsonResponse("Cần nhập id học sinh và id lớp!",safe=False)
    elif request.method == 'DELETE':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)

        try:
            class_student = Classstudent.objects.get(class_field_id=class_id, student_id=student_id)
            class_student.delete()
            return JsonResponse("Xóa học sinh khỏi lớp thành công!", safe=False)
        except Classstudent.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

@csrf_exempt
def getStudentInClass(request, id=0):
    if request.method == 'POST':
        try:
            class_students = Classstudent.objects.filter(class_field_id=id)
            students = [cs.student for cs in class_students]
            students_serializer = StudentSerializer(students, many=True)
            return JsonResponse(students_serializer.data, safe=False)
        except Classstudent.DoesNotExist:
            return JsonResponse("Không tìm được lớp!")
        
@csrf_exempt
def AssignmentAPI(request, id=0):
    if request.method == 'GET':
        assignments=Assignment.objects.filter(class_field = id)
        assignments_serializer = AssignmentSerializer(assignments,many=True)
        return JsonResponse(assignments_serializer.data, safe=False)
    elif request.method == 'POST':
        assignments_data=JSONParser().parse(request)
        assignments_data['class_field'] = id
        assignments_data['file'] = None
        assignments_serializer=AssignmentSerializer(data=assignments_data)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return JsonResponse("Thêm bài tập thành công!",safe=False)
        return JsonResponse(
        {"error": "Dữ liệu không hợp lệ.", "details": assignments_serializer.errors},
        status=400
    )
    elif request.method == 'PUT':
        assignments_data=JSONParser().parse(request)
        assignments=Assignment.objects.get(assignment_id = assignments_data['assignment_id'])
        try:
            assignments_serializer = AssignmentSerializer(assignments, data=assignments_data,class_field = id)
        except Assignment.DoesNotExist:
            return JsonResponse("Không tìm thấy bài tập cho lớp này!", safe=False)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return JsonResponse("Cập nhật bài tập thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được bài tập!", safe=False)
    elif request.method == 'DELETE':
        assignments=Assignment.objects.get(class_id=id)
        assignments.delete()
        return JsonResponse("Xóa bài tập thành công!",safe=False)

@csrf_exempt
def AssignmentFileAPI(request,id=0):
    if request.method == "POST":
        assignments_data=JSONParser().parse(request)
        assignments_data['class_field'] = id
        assignments_data['text_content'] = None
        assignments_serializer=AssignmentSerializer(data=assignments_data)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return JsonResponse("Thêm bài tập thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)

@csrf_exempt        
def CourseAPI(request,id=0):
    if request.method == 'GET':
        courses=Course.objects.all()
        courses_serializer = CourseSerializer(courses,many=True)
        return JsonResponse(courses_serializer.data, safe=False)
    elif request.method == 'POST':
        courses_data=JSONParser().parse(request)
        courses_serializer=CourseSerializer(data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return JsonResponse("Thêm môn học vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        courses_data=JSONParser().parse(request)
        courses=Course.objects.get(course_id = id)
        courses_serializer = CourseSerializer(courses, data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return JsonResponse("Cập nhật thông tin môn học thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        courses=Course.objects.get(course_id=id)
        courses.delete()
        return JsonResponse("Xóa môn học thành công!",safe=False)

@csrf_exempt
def CSVUploadCourse(request):
    if request.method == 'POST':
        # Step 1: Check if a file was uploaded
        csv_file = request.FILES.get('file')
        if not csv_file:
            return JsonResponse({'error': 'No CSV file uploaded'}, status=400)

        try:
            # Step 2: Read CSV with pandas
            df = pd.read_csv(csv_file)

            # Validate required columns exist
            required_columns = [
                'course_name',
                'course_semester',
                'class_is_active',
                'course_midterm_coeff',
                'course_final_coeff',
            ]
            if not all(col in df.columns for col in required_columns):
                return JsonResponse({'error': f'Thiếu trường thông tin. Expected: {required_columns}'})

            # Step 3: Iterate over rows and use CourseSerializer to save
            success_count = 0
            errors = []

            for index, row in df.iterrows():
                # Convert row to dict
                data = row.to_dict()

                # Convert "class_is_active" to Python boolean if needed
                if isinstance(data.get('class_is_active'), str):
                    data['class_is_active'] = data['class_is_active'].strip().lower() in ['true', '1', 'yes']

                serializer = CourseSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    success_count += 1
                else:
                    errors.append({'row': index + 1, 'errors': serializer.errors})

            return JsonResponse({
                'message': f'{success_count} courses imported successfully.',
                'errors': errors,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)})
        
