from typing import OrderedDict, Optional

from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer, ValidationError

from Account.models import User


class UserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)
    current_password = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'confirm_password',
            'current_password',
            'email',
            'id',
            'password',
            'phone',
            'username',
            'profile_id',
            'is_verified',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True}
        }

    def validate(self, data: OrderedDict):
        password = data.get('password', None)
        confirm_password = data.pop('confirm_password', None)
        current_password = data.pop('current_password', None)
        errors = {}

        if password:
            if not confirm_password:
                errors['confirm_password'] = 'This field is required.'
            elif password != confirm_password:
                errors['confirm_password'] = 'Confirm password do not match.'

            if self.instance:
                if not current_password:
                    errors['current_password'] = 'This field is required.'
                elif not self.instance.check_password(current_password):
                    errors['current_password'] = 'Current password is incorrect.'
        if len(errors) > 0:
            raise ValidationError(errors)
        return data

    def create(self, validated_data: OrderedDict):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance: User, validated_data: OrderedDict):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def to_representation(self, instance: User):
        data: OrderedDict = super().to_representation(instance)
        username: Optional[str] = data.get('username', None)
        if username is not None:
            data['username'] = '@' + username
        return data
