from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.db.models import Q
from django.template.loader import render_to_string
import server.settings as settings

from MainApp.models import Userlogin
from MainApp.serializers import TeacherSerializer, StudentSerializer, UserloginSerializer

# RegisterController is not used by all users, but by the admin only.
class RegisterController(APIView):
    def post(self, request):
        user_data = request.data
        username = user_data.get('username')
        useremail = user_data.get('useremail')
        usertype = user_data.get('usertype')

        if Userlogin.objects.filter(username=username).exists():
            return Response("Tên tài khoản này đã tồn tại!", status=status.HTTP_400_BAD_REQUEST)
        if Userlogin.objects.filter(useremail=useremail).exists():
            return Response("Email này đã tồn tại!", status=status.HTTP_400_BAD_REQUEST)
        
        related_id = None

        if usertype == 'Teacher':
            teacher_data = {
                'teacher_name': user_data.get('teacher_name'),
                'teacher_gender': user_data.get('teacher_gender'),
                'teacher_email': user_data.get('teacher_email'),
                'teacher_profession': user_data.get('teacher_profession'),
            }
            teacher_serializer = TeacherSerializer(data=teacher_data)
            
            if teacher_serializer.is_valid():
                teacher = teacher_serializer.save()
                related_id = teacher.teacher_id
            else:
                return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif usertype == 'Student':
            student_data = {
                'student_name': user_data.get('student_name'),
                'student_dob': user_data.get('student_dob'),
                'student_gender': user_data.get('student_gender'),
                'student_email': user_data.get('student_email'),
                'parent_email': user_data.get('parent_email'),
                'student_phone_number': user_data.get('student_phone_number'),
                'student_specialization': user_data.get('student_specialization'),
                'student_is_active': user_data.get('student_is_active')
            }
            student_serializer = StudentSerializer(data=student_data)
            
            if student_serializer.is_valid():
                student = student_serializer.save()
                related_id = student.student_id
            else:
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Loại người dùng không hợp lệ!", status=status.HTTP_400_BAD_REQUEST)
        
        user_data['relatedid'] = related_id

        user_serializer = UserloginSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("Thêm tài khoản thành công!", status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginController(APIView):
    def post(self, request):
        identifier = request.data.get('username') or request.data.get('useremail')
        password = request.data.get('password')

        if identifier:
            try:
                user = Userlogin.objects.get(
                    Q(useremail = identifier) | Q(username = identifier)
                )

                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    return Response({
                        "message": "Đăng nhập thành công!", 
                        "username": user.username,  
                        "useremail": user.useremail,
                        "usertype": user.usertype
                    })
                else:
                    return Response("Mật khẩu không đúng, Vui lòng thử lại!", status=status.HTTP_401_UNAUTHORIZED)
            except Userlogin.DoesNotExist:
                return Response("Tài khoản không tồn tại!", status=status.HTTP_404_NOT_FOUND)
        else:
            if not identifier:
                return Response("Thiếu username hoặc email!", status=status.HTTP_400_BAD_REQUEST)
            if not password:
                return Response("Thiếu password!", status=status.HTTP_400_BAD_REQUEST)

class SessionController(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        try:
            user = Userlogin.objects.get(user_id=user_id)
        except Userlogin.DoesNotExist:
            return Response("User not logged in", status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "user_id": user.user_id,
            "email": user.useremail,
            "usertype": user.usertype,
            "relatedid": user.relatedid
        })

class LogoutController(APIView):
    def post(self, request):
        request.session.flush()
        return Response("Logged out successfully!")

class ForgotPasswordController(APIView):
    signer = TimestampSigner()
    def post(self, request):
        email = request.data.get('useremail')
        
        try:
            user = Userlogin.objects.get(useremail=email)
            signed_token = self.signer.sign(user.useremail) 
            reset_link = f"http://localhost:5173/reset-password?token={signed_token}"
            
            # Nội dung email
            subject = 'Đặt lại mật khẩu - BKSystem'
            context = {
                'username': user.username,
                'reset_link': reset_link
            }
            html_content = render_to_string('forgot-pass.html', context)
            
            msg = EmailMultiAlternatives(subject, "", settings.EMAIL_HOST_USER, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response("Email reset đã được gửi!", status=status.HTTP_200_OK)

        except Userlogin.DoesNotExist:
            return Response("Tài khoản không tồn tại!", status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not token or not new_password:
            return Response("Thiếu trường thông tin!", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            email_from_token = self.signer.unsign(token, max_age=300)

            user = Userlogin.objects.get(useremail=email_from_token)
            user.password = new_password 
            user.save()

            return Response("Đổi mật khẩu thành công!", status=status.HTTP_200_OK)
        
        except SignatureExpired:
            return Response("Link đã hết hạn, vui lòng gửi lại yêu cầu!", status=status.HTTP_400_BAD_REQUEST)
        
        except BadSignature:
            return Response("Token không hợp lệ hoặc đã bị thay đổi!", status=status.HTTP_400_BAD_REQUEST)
        
        except Userlogin.DoesNotExist:
            return Response("User không tìm thấy!", status=status.HTTP_404_NOT_FOUND)