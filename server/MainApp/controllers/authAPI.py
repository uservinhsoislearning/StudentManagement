from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
import server.settings as settings
from MainApp.models import Userlogin
from MainApp import serializers as s

# RegisterController is not used by all users, but by the admin only.
class RegisterController(APIView):
    def post(self, request):
        # ... [Paste UserRegisterController logic here] ...
        pass

class LoginController(APIView):
    def post(self, request):
        email = request.data.get('useremail')
        password = request.data.get('password')
        name = request.data.get('username')

        if (name and password) or (email and password):
            try:

                user = Userlogin.objects.get(useremail = email) if email else Userlogin.objects.get(username = name)

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
            if not name or not email:
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
            subject = 'Đặt lại mật khẩu'
            html_content = f'''
                <p>Xin chào {user.username},</p>
                <p>Bạn đã yêu cầu đặt lại mật khẩu.</p>
                <p>Vui lòng click vào link dưới đây (Link hết hạn sau 10 phút):</p>
                <p><a href="{reset_link}"><b>ĐẶT LẠI MẬT KHẨU NGAY</b></a></p>
            '''
            
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