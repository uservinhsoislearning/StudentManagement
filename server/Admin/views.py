from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.utils import timezone

import pandas as pd
import DBApp.models as m
import DBApp.serializers as s
from Login.models import Userlogin

@csrf_exempt
def studentAPI(request,sid=0):
    if request.method == 'GET':
        students = m.Student.objects.all()
        students_serializer = s.StudentWithIDSerializer(students,many=True)
        return JsonResponse(students_serializer.data, safe=False)
    elif request.method == 'POST':
        students_data=JSONParser().parse(request)
        students_serializer=s.StudentSerializer(data=students_data)
        if students_serializer.is_valid():
            students_serializer.save()
            return JsonResponse("Thêm học sinh vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse(students_serializer.errors,safe=False)
    elif request.method == 'PUT':
        students_data=JSONParser().parse(request)
        students=m.Student.objects.get(student_id = sid)
        students_serializer = s.StudentSerializer(students, data=students_data)
        if students_serializer.is_valid():
            students_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        students=m.Student.objects.get(student_id=sid)
        students.delete()
        return JsonResponse("Deleted Successfully!",safe=False)
    
@csrf_exempt
def classAPI(request,id=0):
    if request.method == 'GET':
        classes=m.Class.objects.all()
        classes_serializer=s.ClassWithTimetableSerializer(classes,many=True)
        return JsonResponse(classes_serializer.data, safe=False)
    elif request.method == 'POST':
        classes_data=JSONParser().parse(request)
        classes_serializer=s.ClassWithCourseSerializer(data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Thêm lớp vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse(classes_serializer.errors,safe=False)
    elif request.method == 'PUT':
        classes_data=JSONParser().parse(request)
        classes=m.Class.objects.get(class_id = classes_data['class_id'])
        classes_serializer=s.ClassSerializer(classes, data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        classes=m.Class.objects.get(class_id=id)
        classes.delete()
        return JsonResponse("Xóa lớp thành công!",safe=False)
    
@csrf_exempt
def teacherAPI(request,tid=0):
    if request.method == 'GET':
        teachers=m.Teacher.objects.all()
        teachers_serializer=s.TeacherWithIDSerializer(teachers,many=True)
        return JsonResponse(teachers_serializer.data, safe=False)
    elif request.method == 'POST':
        teachers_data=JSONParser().parse(request)
        teachers_serializer=s.TeacherSerializer(data=teachers_data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return JsonResponse("Thêm thầy/cô vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        teachers_data=JSONParser().parse(request)
        teachers=m.Teacher.objects.get(teacher_id = teachers_data['teacher_id'])
        teachers_serializer=s.TeacherSerializer(teachers, data=teachers_data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        teachers=m.Teacher.objects.get(teacher_id=tid)
        teachers.delete()
        return JsonResponse("Xóa thầy/cô thành công!",safe=False)

@csrf_exempt
def EnrollmentAPI(request, class_id=0, student_id=0):
    if request.method == 'POST':
        enrollment_data=JSONParser().parse(request)
        enrollment_data['withdrawal_date'] = None 
        enrollment_data['grade'] = None
        enrollment_data['midterm'] = None
        enrollment_data['final'] = None
        enrollment_serializer=s.EnrollmentSerializer(data=enrollment_data)
        if enrollment_serializer.is_valid():
            enrollment_serializer.save()
            return JsonResponse("Thêm học sinh vào lớp thành công!",safe=False)
        return JsonResponse("Xin thử lại!",safe=False)
    elif request.method == 'PUT':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)

        try:
            enrollment=m.Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
        except m.Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

        update_data = JSONParser().parse(request)

        # Allow partial update for grade fields
        enrollment.grade = update_data.get('grade', enrollment.grade)
        enrollment.midterm = update_data.get('midterm', enrollment.midterm)
        enrollment.final = update_data.get('final', enrollment.final)
        enrollment.save()

        serializer = s.EnrollmentSerializer(enrollment)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)

        try:
            enrollment = m.Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
            enrollment.delete()
            return JsonResponse("Xóa học sinh khỏi lớp thành công!", safe=False)
        except m.Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

@csrf_exempt
def getGradeClass(request, cid=0):
    if request.method == 'GET':
        enrollment=m.Enrollment.objects.filter(class_field = cid)
        enrollment_serializer=s.EnrollmentGradeSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)

@csrf_exempt
def getStudentInClass(request, id=0):
    if request.method == 'POST':
        try:
            enrollment=m.Enrollment.objects.filter(class_field_id=id)
            students = [cs.student for cs in enrollment]
            students_serializer=s.StudentWithIDSerializer(students, many=True)
            return JsonResponse(students_serializer.data, safe=False)
        except m.Enrollment.DoesNotExist:
            return JsonResponse("Không tìm được lớp!")
        
@csrf_exempt
def getGradeStudent(request, sid=0):
    if request.method == 'GET':
        enrollment=m.Enrollment.objects.filter(student = sid)
        enrollment_serializer=s.EnrollmentGradeSubjectSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)
        
@csrf_exempt
def AssignmentAPI(request, id=0):
    if request.method == 'GET':
        assignments=m.Assignment.objects.filter(class_field = id)
        assignments_serializer=s.AssignmentWithIDSerializer(assignments,many=True)
        return JsonResponse(assignments_serializer.data, safe=False)
    elif request.method == 'POST':
        assignments_data=JSONParser().parse(request)
        assignments_data['class_field'] = id
        assignments_data['file'] = None
        assignments_serializer=s.AssignmentSerializer(data=assignments_data)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return JsonResponse("Thêm bài tập thành công!",safe=False)
        return JsonResponse(
        {"error": "Dữ liệu không hợp lệ.", "details": assignments_serializer.errors},
        status=400
    )
    elif request.method == 'PUT':
        assignments_data=JSONParser().parse(request)
        assignments=m.Assignment.objects.get(assignment_id = assignments_data['assignment_id'])
        try:
            assignments_serializer=s.AssignmentSerializer(assignments, data=assignments_data,class_field = id)
        except m.Assignment.DoesNotExist:
            return JsonResponse("Không tìm thấy bài tập cho lớp này!", safe=False)
        if assignments_serializer.is_valid():
            assignments_serializer.save()
            return JsonResponse("Cập nhật bài tập thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được bài tập!", safe=False)
    elif request.method == 'DELETE':
        assignments=m.Assignment.objects.get(class_id=id)
        assignments.delete()
        return JsonResponse("Xóa bài tập thành công!",safe=False)

@csrf_exempt
def AssignmentFileAPI(request,id=0):
    if request.method == "POST":
        try:
            # Copy POST data and add the class_field
            assignments_data = request.POST.copy()
            assignments_data['class_field'] = id  # Foreign key to Class

            # Handle uploaded file
            if 'file' in request.FILES:
                assignments_data['file'] = request.FILES['file']
            else:
                return JsonResponse({'error': 'No file uploaded.'}, status=400)

            # Include the file in serializer's files argument
            assignments_serializer = s.AssignmentSerializer(data=assignments_data)
            if assignments_serializer.is_valid():
                assignments_serializer.save()
                return JsonResponse({'message': 'Assignment uploaded successfully.'}, status=201)
            else:
                return JsonResponse({'error': assignments_serializer.errors}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt        
def CourseAPI(request,crid=0):
    if request.method == 'GET':
        courses=m.Course.objects.all()
        courses_serializer=s.CourseWithIDSerializer(courses,many=True)
        return JsonResponse(courses_serializer.data, safe=False)
    elif request.method == 'POST':
        courses_data=JSONParser().parse(request)
        courses_serializer=s.CourseSerializer(data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return JsonResponse("Thêm môn học vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        courses_data=JSONParser().parse(request)
        courses=m.Course.objects.get(course_id=crid)
        courses_serializer=s.CourseSerializer(courses, data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return JsonResponse("Cập nhật thông tin môn học thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        courses=m.Course.objects.get(course_id=crid)
        courses.delete()
        return JsonResponse("Xóa môn học thành công!",safe=False)

@csrf_exempt
def CourseAndClass(request):
    if request.method == 'GET':
        course_list = []
        courses=m.Course.objects.all()
        for course in courses:
            # Get all classes related to this course
            classes=m.Class.objects.filter(course_id=course.course_id)
            class_data = []
            for cls in classes:
                # Get timetables for this class
                timetables=m.ClassTimetable.objects.filter(class_field_id=cls.class_id)
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
        return JsonResponse(course_list, safe=False)

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

                serializer=s.CourseSerializer(data=data)
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
        
@csrf_exempt
def ReportAPI(request, user_id=0): #This post method is currently not available (but it still exists to insert values into the tables)
    if request.method == 'GET':
        reports=m.Report.objects.filter(sender=user_id) if user_id != 0 else m.Report.objects.all()
        serializer=s.ReportSerializer(reports, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        reports_data = JSONParser().parse(request)
        # reports_data['sender'] = user.user_id  # Inject sender into the data
        serializer=s.ReportSerializer(data=reports_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Report submitted successfully"}, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def SemesterAPI(request, sem_id=0):
    if request.method == 'GET':
        semesters=m.Semester.objects.all()
        semesters_serializer=s.SemesterWithIDSerializer(semesters, many=True)
        return JsonResponse(semesters_serializer.data, safe=False)
    elif request.method == 'POST':
        semesters_data = JSONParser().parse(request)
        semesters_serializer=s.SemesterSerializer(data=semesters_data)
        if semesters_serializer.is_valid():
            semesters_serializer.save()
            return JsonResponse({"message": "Semester created successfully"}, status=201)
        return JsonResponse(semesters_serializer.errors, status=400)
    elif request.method == 'PUT':
        semesters_data = JSONParser().parse(request)
        semesters=m.Semester.objects.get(semester_id=sem_id)
        semesters_serializer=s.SemesterSerializer(semesters, data=semesters_data)
        if semesters_serializer.is_valid():
            semesters_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse(semesters_serializer.errors, status=400)
    elif request.method == 'DELETE':
        semesters=m.Semester.objects.get(semester_id=sem_id)
        semesters.delete()
        return JsonResponse({"message": "Semester deleted successfully"}, status=204)

@csrf_exempt
def SemesterPatchAPI(request, sem_id=0):
    if request.method == 'PATCH':
        try:
            semesters=m.Semester.objects.get(semester_id=sem_id)
            semesters.isActive = not semesters.isActive
            semesters.save()
            return JsonResponse("Cập nhật trạng thái thành công!", safe=False)
        except m.Semester.DoesNotExist:
            return JsonResponse({"error": "Semester not found"}, status=404)
    
@csrf_exempt
def ParentAPI(request, pid=0):
    if request.method == 'GET':
        parents=m.Parent.objects.all()
        parents_serializer=s.ParentWithIDSerializer(parents,many=True)
        return JsonResponse(parents_serializer.data, safe=False)
    elif request.method == 'POST':
        parents_data=JSONParser().parse(request)
        parents_serializer=s.ParentSerializer(data=parents_data)
        if parents_serializer.is_valid():
            parents_serializer.save()
            return JsonResponse("Thêm bố/mẹ vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse(parents_serializer.errors,safe=False)
    elif request.method == 'PUT':
        parents_data=JSONParser().parse(request)
        parents=m.Parent.objects.get(parent_id = parents_data['parent_id'])
        parents_serializer=s.ParentSerializer(parents, data=parents_data)
        if parents_serializer.is_valid():
            parents_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        parents=m.Parent.objects.get(parent_id=pid)
        parents.delete()
        return JsonResponse("Xóa bố/mẹ thành công!",safe=False)
    
@csrf_exempt
def ClassTimetableAPI(request, sid=0):
    if request.method == 'GET':
        class_ids=m.Enrollment.objects.filter(student_id=sid).values_list('class_field_id', flat=True)
        classes=m.Class.objects.filter(class_id__in=class_ids).prefetch_related('timetables')

        serializer=s.ClassWithTimetableSerializer(classes, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def MessageAPI(request, user1_id, user2_id):
    if request.method == 'GET':
        try:
            messages_user1_to_user2=m.Message.objects.filter(
                sender_id=user1_id, receiver_id=user2_id
            )
            # Get messages from user2 to user1
            messages_user2_to_user1=m.Message.objects.filter(
                sender_id=user2_id, receiver_id=user1_id
            )
            # Combine the two querysets
            all_messages = messages_user1_to_user2.union(messages_user2_to_user1).order_by('timestamp')

            serializer=s.MessageSerializer(all_messages, many=True)
            return JsonResponse(serializer.data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            sender_id = request.data.get('sender_id')
            receiver_id = request.data.get('receiver_id')
            content = request.data.get('content')

            if not all([sender_id, receiver_id, content]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            sender = Userlogin.objects.get(user_id=sender_id)
            receiver = Userlogin.objects.get(user_id=receiver_id)

            message=m.Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                timestamp=timezone.now()
            )

            message_serializer=s.MessageSerializer(message)
            return JsonResponse(message_serializer.data, safe=False)

        except Userlogin.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def registrationAPI(request, sid=0, cid=0):
    if request.method == 'POST':
        try:
            # Validate student existence
            if not m.Student.objects.filter(student_id=sid).exists():
                return JsonResponse({'error': 'Student does not exist.'}, status=404)

            # Validate class existence
            if not m.Class.objects.filter(class_id=cid).exists():
                return JsonResponse({'error': 'Class does not exist.'}, status=404)

            # Register the student to the class
            registration, created = m.Registration.objects.get_or_create(
                student_id=sid,
                class_id=cid
            )

            if created:
                return JsonResponse({'message': 'Registration successful.'}, status=201)
            else:
                return JsonResponse({'message': 'Already registered for this class.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            # Validate student existence
            if not m.Student.objects.filter(student_id=sid).exists():
                return JsonResponse({'error': 'Student does not exist.'}, status=404)

            registration = m.Registration.objects.get(student_id=sid, class_id=cid)
            registration.delete()
            return JsonResponse({'message': 'Class unregistered successfully.'}, status=200)

        except m.Registration.DoesNotExist:
            return JsonResponse({'error': 'Registration does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def getRegistrated(request,sid=0):
    if request.method == 'GET':
        try:
            # Get all registrations for the student
            registrations = m.Registration.objects.filter(student_id=sid).select_related('class_field')

            # Extract class names
            class_names = [reg.class_field.class_name for reg in registrations if reg.class_field]

            return JsonResponse({'registered_classes': class_names}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def getSummaryAdmin(request):
    if request.method == 'GET':
        total_students = m.Student.objects.count()
        total_teachers = m.Teacher.objects.count()
        total_parents = m.Parent.objects.count()
        reports_pending = m.Report.objects.filter(status='Pending').count()

        dashboard = {
            "totalStudents": total_students,
            "totalTeachers": total_teachers,
            "totalParents": total_parents,
            "reportsPending": reports_pending
        }

        return JsonResponse(dashboard, safe=False)