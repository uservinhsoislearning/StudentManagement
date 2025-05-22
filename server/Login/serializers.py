from rest_framework import serializers
from Login.models import Userlogin

class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model=Userlogin
        fields=(
            'username',
            'password',
            'useremail',
            'usertype',
            'relatedid'
        )