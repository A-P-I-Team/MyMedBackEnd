from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from .models import City

User_Model = get_user_model()

Password_validation = [
    RegexValidator(regex="^(?=.*[A-Z])", message='Password must contain at least one uppercase letter.'),
    RegexValidator(regex="^(?=.*[0-9])", message='Password must contain at least one number.'),
    RegexValidator(regex="^(?=.{8,})", message='Password must be eight characters or longer.')
]


# class QuestionSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Question
#         fields = "__all__"
#         extra_kwargs = {
#             'string_answer' : {'required':False},
#             'bool_answer' : {'required':False},
#         }


# create users
class UserSerializer(serializers.ModelSerializer):
    # questions=QuestionSerializer(many=True)
    class Meta:
        model = User_Model
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'ssn',
            'citizens_ssn',
            'gender',
            'birthdate',
            'profile_pic',
            'user_city',
            'relationship_status',
            'isVaccinated',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_city': {'required': True},

            'ssn': {'required': False},
            'citizens_ssn': {'required': False},

            'relationship_status': {'required': True},
            'isVaccinated': {'required': True},

            'gender': {'required': False},
            'birthdate': {'required': False},
            'profile_pic': {'required': False},
        }

    def create(self, validated_data):
        user = User_Model.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_city=validated_data['user_city'],
        )

        try:
            if (validated_data['ssn'] != None):
                user.ssn = validated_data['ssn']
        except:
            pass

        try:
            if (validated_data['citizens_ssn'] != None):
                user.citizens_ssn = validated_data['citizens_ssn']
        except:
            pass

        try:
            if (validated_data['birthdate'] != None):
                user.birthdate = validated_data['birthdate']
        except:
            pass

        try:
            if (validated_data['gender'] != None):
                user.gender = validated_data['gender']
        except:
            pass

        try:
            if (validated_data['profile_pic'] != None):
                user.profile_pic = validated_data['profile_pic']
        except:
            pass

        try:
            if (validated_data['relationship_status'] != None):
                user.relationship_status = validated_data['relationship_status']
        except:
            pass

        try:
            if (validated_data['isVaccinated'] != None):
                user.isVaccinated = validated_data['isVaccinated']
        except:
            pass

        user.save()
        return user


# change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=30)
    new_password1 = serializers.CharField(
        required=True,
        max_length=30,
        validators=Password_validation
    )
    new_password2 = serializers.CharField(required=True, max_length=30)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError('Old password was entered incorrectly')
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords are not the same")
        if data['old_password'] == data['new_password1']:
            raise serializers.ValidationError("New password cannot be the same as current password")
        return data


# send email before register a user:
class SendregisterEmailSerializer(serializers.Serializer):
    model = User_Model
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)

    def validate(self, data):
        if (User_Model.objects.filter(username=data['email'])):
            raise serializers.ValidationError("There is another account with this email")
        return data


# send reset password email:
class SendpasswordresetEmailSerializer(serializers.Serializer):
    model = User_Model
    email = serializers.EmailField(required=True)

    def validate(self, data):
        # if not(User_model.objects.filter(email=data['email'])):
        #     raise serializers.ValidationError("there is no email like this!")
        if not User_Model.objects.filter(username=data['email']):
            raise serializers.ValidationError("Email Does Not Exist")
        return data


# Serializer for reset password after confirm email
class ResetPasswordSerializer(serializers.Serializer):
    model = User_Model

    new_password1 = serializers.CharField(
        required=True,
        max_length=30,
        validators=Password_validation
    )
    new_password2 = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords are not the same")
        if not User_Model.objects.filter(username=data['email']):
            raise serializers.ValidationError("Email Does Not Exist")
        if get_object_or_404(User_Model, username=data['email']).check_password(data['new_password1']):
            raise serializers.ValidationError("New password cannot be the same as current password")
        return data


class GetCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class GetUserDataSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField('get_profile_url')
    # questions=QuestionSerializer(many=True)
    user_city = GetCitySerializer()

    def get_profile_url(self, model):
        if model.profile_pic:
            request = self.context.get("request")
            base_url = request.build_absolute_uri('/').strip("/")
            profile_url = base_url + '/media/' + f"{model.profile_pic}"
            return profile_url

    class Meta:
        model = User_Model
        exclude = ['password', 'user_permissions', 'groups', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user_city = GetCitySerializer()

    # degree_name = serializers.SerializerMethodField('get_degree')

    # def get_degree(self,obj):
    #     print(obj)
    #     print(obj.degree)
    #     if(obj.degree):
    #         return obj.degree.name
    #     else:
    #         return "None"

    class Meta:
        model = User_Model
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'gender',
            'birthdate',
            'ssn',
            'citizens_ssn',
            'user_city',
            'profile_pic',
        ]

    # def validate(self, data):
    #     birthdate = data.get('birthdate')
    #     if birthdate != None:
    #         today = date.today()
    #         age = (today - birthdate).days / 365
    #         if age < 10:
    #             raise serializers.ValidationError('You must be at least 10 years old')
    #     return data
