from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.utils import timezone

import pandas as pd
from DBApp.models import Class, Enrollment, Assignment, Parent, Registration
from DBApp.serializers import ClassSerializer, ClassWithIDSerializer, ClassWithCourseSerializer, EnrollmentSerializer, EnrollmentGradeSerializer, EnrollmentGradeSubjectSerializer, AssignmentSerializer, ParentSerializer, ParentWithIDSerializer
from DBApp.models import Teacher,Student, Course, Report, Semester, Message
from DBApp.serializers import TeacherSerializer,StudentSerializer, StudentWithIDSerializer, CourseSerializer, ReportSerializer, SemesterSerializer, ClassWithTimetableSerializer, TeacherWithIDSerializer, MessageSerializer
from Login.models import Userlogin
# Create your views here.

@csrf_exempt
def studentAPI(request,sid=0):
    if request.method == 'GET':
        students = Student.objects.all()
        students_serializer = StudentWithIDSerializer(students,many=True)
        return JsonResponse(students_serializer.data, safe=False)
    elif request.method == 'POST':
        students_data=JSONParser().parse(request)
        students_serializer=StudentSerializer(data=students_data)
        if students_serializer.is_valid():
            students_serializer.save()
            return JsonResponse("Thêm học sinh vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse(students_serializer.errors,safe=False)
    elif request.method == 'PUT':
        students_data=JSONParser().parse(request)
        students=Student.objects.get(student_id = sid)
        students_serializer = StudentSerializer(students, data=students_data)
        if students_serializer.is_valid():
            students_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        students=Student.objects.get(student_id=sid)
        students.delete()
        return JsonResponse("Deleted Successfully!",safe=False)
    
@csrf_exempt
def classAPI(request,id=0):
    if request.method == 'GET':
        classes=Class.objects.all()
        classes_serializer = ClassWithIDSerializer(classes,many=True)
        return JsonResponse(classes_serializer.data, safe=False)
    elif request.method == 'POST':
        classes_data=JSONParser().parse(request)
        classes_serializer=ClassWithCourseSerializer(data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Thêm lớp vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse(classes_serializer.errors,safe=False)
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
        teachers_serializer = TeacherWithIDSerializer(teachers,many=True)
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
def EnrollmentAPI(request, class_id=0, student_id=0):
    if request.method == 'GET':
        enrollment=Enrollment.objects.filter(class_field = class_id)
        enrollment_serializer = EnrollmentGradeSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)
    elif request.method == 'POST':
        enrollment_data=JSONParser().parse(request)
        enrollment_data['withdrawal_date'] = None 
        enrollment_data['grade'] = None
        enrollment_data['midterm'] = None
        enrollment_data['final'] = None
        enrollment_serializer=EnrollmentSerializer(data=enrollment_data)
        if enrollment_serializer.is_valid():
            enrollment_serializer.save()
            return JsonResponse("Thêm học sinh vào lớp thành công!",safe=False)
        return JsonResponse("Xin thử lại!",safe=False)
    elif request.method == 'PUT':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)

        try:
            enrollment = Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
        except Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

        update_data = JSONParser().parse(request)

        # Allow partial update for grade fields
        enrollment.grade = update_data.get('grade', enrollment.grade)
        enrollment.midterm = update_data.get('midterm', enrollment.midterm)
        enrollment.final = update_data.get('final', enrollment.final)
        enrollment.save()

        serializer = EnrollmentSerializer(enrollment)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'DELETE':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)

        try:
            enrollment = Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
            enrollment.delete()
            return JsonResponse("Xóa học sinh khỏi lớp thành công!", safe=False)
        except Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

@csrf_exempt
def getStudentInClass(request, id=0):
    if request.method == 'POST':
        try:
            enrollment = Enrollment.objects.filter(class_field_id=id)
            students = [cs.student for cs in enrollment]
            students_serializer = StudentWithIDSerializer(students, many=True)
            return JsonResponse(students_serializer.data, safe=False)
        except Enrollment.DoesNotExist:
            return JsonResponse("Không tìm được lớp!")
        
@csrf_exempt
def getGradeStudent(request, sid=0):
    if request.method == 'GET':
        enrollment=Enrollment.objects.filter(student = sid)
        enrollment_serializer = EnrollmentGradeSubjectSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)
        
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
        
@csrf_exempt
def ReportAPI(request, user_id=0): #This post method is currently not available (but it still exists to insert values into the tables)
    if request.method == 'GET':
        reports = Report.objects.filter(sender=user_id) if user_id != 0 else Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        reports_data = JSONParser().parse(request)
        # reports_data['sender'] = user.user_id  # Inject sender into the data
        serializer = ReportSerializer(data=reports_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Report submitted successfully"}, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def SemesterAPI(request, sem_id=0):
    if request.method == 'GET':
        semesters = Semester.objects.all()
        semesters_serializer = SemesterSerializer(semesters, many=True)
        return JsonResponse(semesters_serializer.data, safe=False)
    elif request.method == 'POST':
        semesters_data = JSONParser().parse(request)
        semesters_serializer = SemesterSerializer(data=semesters_data)
        if semesters_serializer.is_valid():
            semesters_serializer.save()
            return JsonResponse({"message": "Semester created successfully"}, status=201)
        return JsonResponse(semesters_serializer.errors, status=400)
    elif request.method == 'PUT':
        semesters_data = JSONParser().parse(request)
        semesters=Semester.objects.get(semester_id=sem_id)
        semesters_serializer = SemesterSerializer(semesters, data=semesters_data)
        if semesters_serializer.is_valid():
            semesters_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse(semesters_serializer.errors, status=400)
    elif request.method == 'DELETE':
        semesters=Semester.objects.get(semester_id=sem_id)
        semesters.delete()
        return JsonResponse({"message": "Semester deleted successfully"}, status=204)

@csrf_exempt
def SemesterPatchAPI(request, sem_id=0):
    if request.method == 'PATCH':
        try:
            semesters = Semester.objects.get(semester_id=sem_id)
            semesters.isActive = not semesters.isActive
            semesters.save()
            return JsonResponse("Cập nhật trạng thái thành công!", safe=False)
        except Semester.DoesNotExist:
            return JsonResponse({"error": "Semester not found"}, status=404)
    
@csrf_exempt
def ParentAPI(request, pid=0):
    if request.method == 'GET':
        parents=Parent.objects.all()
        parents_serializer = ParentWithIDSerializer(parents,many=True)
        return JsonResponse(parents_serializer.data, safe=False)
    elif request.method == 'POST':
        parents_data=JSONParser().parse(request)
        parents_serializer=ParentSerializer(data=parents_data)
        if parents_serializer.is_valid():
            parents_serializer.save()
            return JsonResponse("Thêm bố/mẹ vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse(parents_serializer.errors,safe=False)
    elif request.method == 'PUT':
        parents_data=JSONParser().parse(request)
        parents=Parent.objects.get(parent_id = parents_data['parent_id'])
        parents_serializer = ParentSerializer(parents, data=parents_data)
        if parents_serializer.is_valid():
            parents_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        parents=Parent.objects.get(parent_id=pid)
        parents.delete()
        return JsonResponse("Xóa bố/mẹ thành công!",safe=False)
    
@csrf_exempt
def ClassTimetableAPI(request, sid=0):
    if request.method == 'GET':
        class_ids = Enrollment.objects.filter(student_id=sid).values_list('class_field_id', flat=True)
        classes = Class.objects.filter(class_id__in=class_ids).prefetch_related('timetables')

        serializer = ClassWithTimetableSerializer(classes, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def MessageAPI(request, user1_id, user2_id):
    if request.method == 'GET':
        try:
            messages_user1_to_user2 = Message.objects.filter(
                sender_id=user1_id, receiver_id=user2_id
            )
            # Get messages from user2 to user1
            messages_user2_to_user1 = Message.objects.filter(
                sender_id=user2_id, receiver_id=user1_id
            )
            # Combine the two querysets
            all_messages = messages_user1_to_user2.union(messages_user2_to_user1).order_by('timestamp')

            serializer = MessageSerializer(all_messages, many=True)
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

            message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                timestamp=timezone.now()
            )

            message_serializer = MessageSerializer(message)
            return JsonResponse(message_serializer.data, safe=False)

        except Userlogin.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def registrationAPI(request, course_id=0):
    if request.method == 'POST':
        try:
            # Get useremail from session
            user_email = request.session.get('useremail')
            if not user_email:
                return JsonResponse({'error': 'User not logged in.'}, status=401)

            # Get Userlogin object
            user = Userlogin.objects.get(useremail=user_email)

            # Ensure user is a student
            if user.usertype != 'student':
                return JsonResponse({'error': 'Only students can register for courses.'}, status=403)

            # Get related student_id from relatedid
            student_id = user.relatedid
            if not student_id:
                return JsonResponse({'error': 'No student profile associated with user.'}, status=400)

            # Check if course exists
            if not Course.objects.filter(course_id=course_id).exists():
                return JsonResponse({'error': 'Course does not exist.'}, status=404)

            # Create Registration
            registration, created = Registration.objects.get_or_create(
                student_id=student_id,
                course_id=course_id
            )

            if created:
                return JsonResponse({'message': 'Registration successful.'}, status=201)
            else:
                return JsonResponse({'message': 'Already registered for this course.'}, status=200)

        except Userlogin.DoesNotExist:
            return JsonResponse({'error': 'Invalid user.'}, status=400)
    elif request.method == 'DELETE':
        try:
            # Get useremail from session
            user_email = request.session.get('useremail')
            if not user_email:
                return JsonResponse({'error': 'User not logged in.'}, status=401)

            # Find user and check if they're a student
            user = Userlogin.objects.get(useremail=user_email)
            if user.usertype != 'student':
                return JsonResponse({'error': 'Only students can unregister from courses.'}, status=403)

            student_id = user.relatedid
            if not student_id:
                return JsonResponse({'error': 'No associated student found.'}, status=400)

            # Delete the registration
            registration = Registration.objects.get(student_id=student_id, course_id=course_id)
            registration.delete()
            return JsonResponse({'message': 'Course unregistered successfully.'}, status=200)

        except Registration.DoesNotExist:
            return JsonResponse({'error': 'Registration does not exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def getSummaryAdmin(request):
    if request.method == 'GET':
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_parents = Parent.objects.count()
        reports_pending = Report.objects.filter(status='Pending').count()

        dashboard = {
            "totalStudents": total_students,
            "totalTeachers": total_teachers,
            "totalParents": total_parents,
            "reportsPending": reports_pending
        }

        return JsonResponse(dashboard, safe=False)