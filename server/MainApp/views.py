from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.utils import timezone

from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.db.models import F, ExpressionWrapper, DurationField, Avg, Max, Min
from django.db.models.functions import Now, Extract
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
import server.settings as settings

import pandas as pd
from MainApp import models as m
from MainApp import serializers as s

# @csrf_exempt
# def studentAPI(request,sid=0):
#     if request.method == 'GET':
#         students = m.Student.objects.all()
#         students_serializer = s.StudentWithIDSerializer(students,many=True)
#         return JsonResponse(students_serializer.data, safe=False)
#     elif request.method == 'POST':
#         students_data=JSONParser().parse(request)
#         students_serializer=s.StudentSerializer(data=students_data)
#         if students_serializer.is_valid():
#             students_serializer.save()
#             return JsonResponse("Thêm học sinh vào cơ sở dữ liệu thành công!",safe=False)
#         return JsonResponse(students_serializer.errors,safe=False)
#     elif request.method == 'PUT':
#         students_data=JSONParser().parse(request)
#         students=m.Student.objects.get(student_id = sid)
#         students_serializer = s.StudentSerializer(students, data=students_data)
#         if students_serializer.is_valid():
#             students_serializer.save()
#             return JsonResponse("Cập nhật thông tin thành công!", safe=False)
#         return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
#     elif request.method == 'DELETE':
#         students=m.Student.objects.get(student_id=sid)
#         students.delete()
#         return JsonResponse("Deleted Successfully!",safe=False)
    
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
    
# @csrf_exempt
# def teacherAPI(request,tid=0):
#     if request.method == 'GET':
#         teachers=m.Teacher.objects.all()
#         teachers_serializer=s.TeacherWithIDSerializer(teachers,many=True)
#         return JsonResponse(teachers_serializer.data, safe=False)
#     elif request.method == 'POST':
#         teachers_data=JSONParser().parse(request)
#         teachers_serializer=s.TeacherSerializer(data=teachers_data)
#         if teachers_serializer.is_valid():
#             teachers_serializer.save()
#             return JsonResponse("Thêm thầy/cô vào cơ sở dữ liệu thành công!",safe=False)
#         return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
#     elif request.method == 'PUT':
#         teachers_data=JSONParser().parse(request)
#         teachers=m.Teacher.objects.get(teacher_id = teachers_data['teacher_id'])
#         teachers_serializer=s.TeacherSerializer(teachers, data=teachers_data)
#         if teachers_serializer.is_valid():
#             teachers_serializer.save()
#             return JsonResponse("Cập nhật thông tin thành công!", safe=False)
#         return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
#     elif request.method == 'DELETE':
#         teachers=m.Teacher.objects.get(teacher_id=tid)
#         teachers.delete()
#         return JsonResponse("Xóa thầy/cô thành công!",safe=False)

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

            sender = m.Userlogin.objects.get(user_id=sender_id)
            receiver = m.Userlogin.objects.get(user_id=receiver_id)

            message=m.Message.objects.create(
                sender=sender,
                receiver=receiver,
                content=content,
                timestamp=timezone.now()
            )

            message_serializer=s.MessageSerializer(message)
            return JsonResponse(message_serializer.data, safe=False)

        except m.Userlogin.DoesNotExist:
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
        reports_pending = m.Report.objects.filter(status='Pending').count()

        dashboard = {
            "totalStudents": total_students,
            "totalTeachers": total_teachers,
            "reportsPending": reports_pending
        }

        return JsonResponse(dashboard, safe=False)
    
@csrf_exempt
def EnrollmentScoreAPI(request, class_id=0, student_id=0):
    if request.method == "GET":
        enrollment=m.Enrollment.objects.filter(class_field = class_id)
        enrollment_serializer = m.EnrollmentSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)
    elif request.method == 'PUT':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)
        try:
            enrollment = m.Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
            enrollment_data = JSONParser().parse(request)

            serializer = s.EnrollmentSerializer(enrollment, data=enrollment_data, partial=True)  # partial=True allows partial updates

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Cập nhật điểm thành công!", safe=False)
            else:
                return JsonResponse({"error": "Dữ liệu không hợp lệ", "details": serializer.errors}, status=400)
        except m.Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

@csrf_exempt
def AttendanceRecordAPI(request, cid=0, sid=0):
    if request.method == 'GET':
        closest = (
            m.Attendance.objects.filter(class_field_id=cid)
            .annotate(
                time_diff=ExpressionWrapper(
                    Now() - F('timestamp'),
                    output_field=DurationField()
                )
            )
            .annotate(
                seconds_diff=Extract(F('time_diff'), 'epoch')
            )
            .order_by('seconds_diff')
            .values('timestamp__date')
            .first()
        )

        if not closest:
            return JsonResponse([], safe=False)

        closest_date = closest['timestamp__date']
        attendance = m.Attendance.objects.filter(class_field_id=cid, timestamp__date=closest_date)
        attendance_serializer = s.AttendanceSerializer(attendance, many=True)
        return JsonResponse(attendance_serializer.data, safe=False)

    elif request.method == 'POST':
        try:
            if not m.Class.objects.filter(class_id=cid).exists():
                return JsonResponse({"error": "Lớp không tồn tại!"}, status=404)

            enrollments = m.Enrollment.objects.filter(class_field_id=cid)
            if not enrollments.exists():
                return JsonResponse({"error": "Không có học sinh nào trong lớp này!"}, status=404)

            created_records = []
            for enrollment in enrollments:
                attendance = m.Attendance.objects.create(
                    class_field_id=cid,
                    student=enrollment.student_id
                )
                created_records.append(attendance)

            serializer = s.AttendanceSerializer(created_records, many=True)
            return JsonResponse({"message": "Tạo điểm danh thành công!", "data": serializer.data}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'PATCH':
        try:
            closest = (
                m.Attendance.objects.filter(class_field_id=cid, student=sid)
                .annotate(
                    time_diff=ExpressionWrapper(
                        Now() - F('timestamp'),
                        output_field=DurationField()
                    )
                )
                .annotate(
                    seconds_diff=Extract(F('time_diff'), 'epoch')
                )
                .order_by('seconds_diff')
                .first()
            )

            if not closest:
                return JsonResponse({"error": "Attendance record not found."}, status=404)

            closest.is_present = not closest.is_present
            closest.save()

            return JsonResponse({"message": "Student marked as present."}) if closest.is_present else JsonResponse({"message": "Student marked as NOT present."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

# FIX THIS BECAUSE RELATING TO PARENT
@csrf_exempt
def sendAttendance(request, cid=0):
    if request.method == 'POST':
        try:
            closest = (
                m.Attendance.objects.filter(class_field_id=cid)
                .annotate(
                    time_diff=ExpressionWrapper(
                        Now() - F('timestamp'),
                        output_field=DurationField()
                    )
                )
                .annotate(
                    seconds_diff=Extract(F('time_diff'), 'epoch')
                )
                .order_by('seconds_diff')
                .values('timestamp__date')
                .first()
            )

            if not closest:
                return JsonResponse({"error": "Không có bản ghi điểm danh nào để gửi!"}, status=404)

            closest_date = closest['timestamp__date']

            absent_records = m.Attendance.objects.filter(
                class_field_id=cid,
                timestamp__date=closest_date,
                is_present=False
            )

            if not absent_records.exists():
                return JsonResponse("Không có học sinh nào vắng vào ngày gần nhất!", safe=False)

            emails_sent = []
            class_data = m.Class.objects.get(class_id=cid)
            teacher = class_data.class_teacher

            for record in absent_records:
                try:
                    sid = record.student
                    student = m.Student.objects.get(student_id=sid)
                    parent_email = student.parent_email
                    if not parent_email:
                        print(f"Skipping student {student.student_name}: No parent_email found.")
                        continue
                    subject = "Thông báo vắng mặt"

                    html_message = render_to_string('absent.html', {
                        'student_name': student.student_name,
                        'class_name': class_data.class_name,
                        'date': closest_date,
                        'teacher_email': teacher.teacher_email
                    })

                    plain_message = (
                        f"Học sinh {student.student_name} đã vắng mặt buổi học vào ngày {closest_date}, "
                        f"lớp {class_data.class_name}. Email liên hệ giáo viên: {teacher.teacher_email}"
                    )

                    from_email = settings.EMAIL_HOST_USER

                    email = EmailMultiAlternatives(subject, plain_message, from_email, parent_email)
                    email.attach_alternative(html_message, "text/html")
                    email.send()
                    emails_sent.append(parent_email) # for debugging

                except Exception as e:
                    print(f"Error processing student ID {record.student}: {e}")
                    continue

            return JsonResponse({ # for debugging
                "message": "Email đã được gửi đến phụ huynh học sinh vắng mặt!",
                "recipients": emails_sent
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def gradeWorkAPI(request,cid=0,sid=0,aid=0):
    if request.method == 'PUT':
        try:
            # Step 1: Parse request data
            work_data = JSONParser().parse(request)

            # Step 2: Find the specific Work record
            work_instance = m.Work.objects.get(class_field_id=cid, student_id=sid, assignment_id=aid)

            # Step 3: Create serializer and update score
            work_serializer = s.WorkScoreSerializer(work_instance, data={'score': work_data['score']}, partial=True)

            if work_serializer.is_valid():
                work_serializer.save()
                return JsonResponse(work_serializer.data, safe=False)
            else:
                return JsonResponse(work_serializer.errors, status=400)

        except m.Work.DoesNotExist:
            return JsonResponse({'error': 'Work entry not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # DELETE request: delete the work entry
    elif request.method == 'DELETE':
        if cid == 0 or sid == 0 or aid == 0:
            return JsonResponse("Thiếu thông tin trong URL!", safe=False)
        try:
            work = m.Work.objects.get(class_field=cid, student=sid, assignment=aid)
            work.delete()
            return JsonResponse("Work entry deleted successfully", safe=False)
        except m.Work.DoesNotExist:
            return JsonResponse("Không có bài làm này!", safe=False)
        
@csrf_exempt
def getClassStats(request, cid=0):
    if request.method == 'GET':
        # Get all grades for this class
        class_enrollments = m.Enrollment.objects.filter(class_field_id=cid)

        # Compute statistics
        stats = class_enrollments.aggregate(
            maxScore=Max('grade'),
            minScore=Min('grade'),
            avgScore=Avg('grade')
        )

        # Build response
        grade_data = {
            'maxScore': stats['maxScore'],
            'minScore': stats['minScore'],
            'avgScore': round(stats['avgScore'], 2) if stats['avgScore'] is not None else None
        }

        return JsonResponse(data=grade_data, safe=False)

@csrf_exempt
def getMoreDetails(request, cid=0):
    if request.method == 'GET':
        try:
            # Get the class and related course name
            class_obj = m.Class.objects.select_related('course').get(class_id=cid)
            course_name = class_obj.course.course_name

            # Get timetable entries
            timetables = m.ClassTimetable.objects.filter(class_field=class_obj).values(
                'day_of_week', 'start_time', 'end_time'
            )

            # Format the response
            schedule = list(timetables)
            return JsonResponse({
                'course_name': course_name,
                'schedule': schedule
            })

        except m.Class.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=404)
        
@csrf_exempt
def getSummaryTeacher(request, tid=0):
    if request.method == "GET":
        teacher = m.Teacher.objects.get(teacher_id=tid)
        teacher_serializer = s.TeacherWithIDSerializer(teacher)
        return JsonResponse(teacher_serializer.data, safe=False)
    
@csrf_exempt
def userLoginAPI(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        if (not user_data['useremail'] or not user_data['password']):
            return JsonResponse("Bạn cần điền đầy đủ thông tin đăng nhập!.", safe=False)
        try:
            user = m.Userlogin.objects.get(useremail=user_data['useremail'])
            if check_password(user_data['password'], user.password):
                request.session['user_id'] = user.user_id
                return JsonResponse({"message": "Đăng nhập thành công!", "username": user.username, "usertype": user.usertype, "useremail": user.useremail}) #Dang nhap thanh cong
            else:
                return JsonResponse("Mật khẩu không đúng!",safe=False) #Mat khau sai
        except m.Userlogin.DoesNotExist:
            return JsonResponse("Tài khoản không tồn tại!",safe=False) #Khong co nguoi dung
    # elif request.method == 'PUT': #Thay mat khau
    #     user_data = JSONParser().parse(request) #input: new password, confirm new password
    #     if (user_data['new_password'] == user_data['confirm']): # doan nay tu thay:v


@csrf_exempt
def userRegisterAPI(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        username = user_data.get('username')
        useremail = user_data.get('useremail')
        usertype = user_data.get('usertype')

        if m.Userlogin.objects.filter(username=username).exists() or m.Userlogin.objects.filter(useremail=useremail).exists():
            return JsonResponse("Tên tài khoản này/Email này đã tồn tại, vui lòng chọn tên/email khác.", safe=False)

        related_id = None

        # Create related object depending on usertype
        if usertype == 'Teacher':
            teacher_data = {
                'teacher_name': user_data.get('teacher_name'),
                'teacher_gender': user_data.get('teacher_gender'),
                'teacher_email': user_data.get('teacher_email'),
                'teacher_profession': user_data.get('teacher_profession'),
            }
            teacher_serializer = s.TeacherSerializer(data=teacher_data)
            if teacher_serializer.is_valid():
                teacher = teacher_serializer.save()
                related_id = teacher.teacher_id
            else:
                return JsonResponse(teacher_serializer.errors, safe=False)

        elif usertype == 'Student':
            student_data = {
                'student_name' : user_data.get('student_name'),
                'student_dob' : user_data.get('student_dob'),
                'student_gender' : user_data.get('student_gender'),
                'student_email' : user_data.get('student_email'),
                'student_graduating_class' : user_data.get('student_graduating_class'),
                'student_phone_number' : user_data.get('student_phone_number'),
                'student_specialization' : user_data.get('student_specialization'),
                'student_is_active' : user_data.get('student_is_active'),
                'student_school' : user_data.get('student_school')
            }
            student_serializer = s.StudentSerializer(data=student_data)
            if student_serializer.is_valid():
                student = student_serializer.save()
                related_id = student.student_id
            else:
                return JsonResponse(student_serializer.errors, safe=False)
        else:
            return JsonResponse("Loại người dùng không hợp lệ.", safe=False)

        # Continue with creating Userlogin
        user_data['relatedid'] = related_id
        user_serializer = s.UserloginSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("Thêm tài khoản thành công!", safe=False)
        return JsonResponse(user_serializer.errors, safe=False)

@csrf_exempt
def forgotPassword(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        try:
            user_data_by_mail = m.Userlogin.objects.get(useremail=user_data['useremail'])
            token = get_random_string(length=32)
            reset_link = f"https://yourdomain.com/reset-password?token={token}"  # Replace with your actual reset page

            html_content = render_to_string("login.html", {
                'username': user_data_by_mail.username,
                'reset_link': reset_link,
            })

            subject = 'Đặt lại mật khẩu'
            from_email = settings.EMAIL_HOST_USER
            to = user_data_by_mail.useremail

            email = EmailMultiAlternatives(subject, "", from_email, [to])
            email.attach_alternative(html_content, "text/html")
            email.send()

            return JsonResponse("Email reset đã được gửi thành công!", safe=False)
        except m.Userlogin.DoesNotExist:
            return JsonResponse("Tài khoản không tồn tại!", safe=False)
        
@csrf_exempt
def getCurrentUser(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        try:
            user = m.Userlogin.objects.get(user_id=user_id)
        except m.Userlogin.DoesNotExist:
            return JsonResponse({"error": "User not logged in"}, status=401)

        return JsonResponse({
            "user_id": user.user_id,
            "email": user.useremail,
            "usertype": user.usertype,
            "relatedid": user.relatedid
        })

@csrf_exempt
def userLogout(request):
    if request.method == 'POST':
        request.session.flush()
        return JsonResponse("Logged out successfully!", safe=False)
    
@csrf_exempt
def submitWork(request, cid=0, aid=0, sid=0):
    if request.method == 'GET':
        work = m.Work.objects.filter(class_field=cid,assignment=aid,student=sid)
        work_serializer = s.WorkScoreSerializer(work, many=True)
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

        work_serializer = s.WorkSerializer(data=work_data)
        if work_serializer.is_valid():
            work_serializer.save()
            return JsonResponse("Gửi bài tập thành công!", safe=False)
        return JsonResponse(work_serializer.errors, status=400)

@csrf_exempt
def getSummaryStudent(request, sid=0):
    # Get enrolled classes
    enrollments = m.Enrollment.objects.filter(student=sid)
    course_ids = enrollments.values_list('class_field__course_id', flat=True).distinct()
    enrolled_courses = course_ids.count()

    # Upcoming exams (assignments in those classes)
    class_ids = enrollments.values_list('class_field_id', flat=True)
    now = timezone.now()
    upcoming_exams = m.Assignment.objects.filter(
        class_field_id__in=class_ids,
        is_exam=True,
        deadline__gte=now
    ).count()

    # All relevant assignments from enrolled classes
    all_assignments = m.Assignment.objects.filter(class_field_id__in=class_ids)
    assignment_ids = all_assignments.values_list('id', flat=True)

    # Submitted assignments by the student
    submitted_assignments = m.Work.objects.filter(student=sid, assignment_id__in=assignment_ids).values_list('assignment_id', flat=True).distinct()

    # Pending = total - submitted
    assignments_pending = len(set(assignment_ids) - set(submitted_assignments))

    dashboard = {
        "enrolledCourses": enrolled_courses,
        "upcomingExams": upcoming_exams,
        "assignmentsPending": assignments_pending
    }

    return JsonResponse(dashboard, safe=False)

# comment this after running 
# @csrf_exempt
# def addAdmin(request):
#     if request.method == "POST":
#         admin_data=JSONParser().parse(request)
#         admin_serializer=s.AdminSerializer(data=admin_data)
#         if admin_serializer.is_valid():
#             admin_serializer.save()
#             return JsonResponse("Thêm admin vào cơ sở dữ liệu thành công!",safe=False)
#         return JsonResponse(admin_serializer.errors,safe=False)

# @csrf_exempt
# def addUserAdmin(request):
#     if request.method == "POST":
#         admin_data=JSONParser().parse(request)
#         admin_serializer=s.UserloginSerializer(data=admin_data)
#         if admin_serializer.is_valid():
#             admin_serializer.save()
#             return JsonResponse("Thêm user admin vào cơ sở dữ liệu thành công!",safe=False)
#         return JsonResponse(admin_serializer.errors,safe=False)