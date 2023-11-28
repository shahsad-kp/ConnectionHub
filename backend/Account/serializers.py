from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from Account.models import User


class UserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'phone',
            'password',
            'id',
            'email',
            'confirm_password'
        ]
        
    def validate_confirm_password(self, confirm_password: str):
        password = self.initial_data.get('password')
        if confirm_password != password:
            raise ValidationError('Password is not equal')
        return password
    
    def save(self, **kwargs):
        self.validated_data.pop('confirm_password')
        validated_data = {**self.validated_data, **kwargs}
        return User.objects.create_user(**validated_data)
