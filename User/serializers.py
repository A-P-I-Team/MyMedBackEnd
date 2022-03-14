from operator import truediv
from tkinter import E
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from datetime import date
from .models import Question

User_Model=get_user_model()


Password_validation=[RegexValidator(regex="^(?=.*[A-Z])",message='Password must contain at least one uppercase letter.'),
                    RegexValidator(regex="^(?=.*[0-9])",message='Password must contain at least one number.'),
                    RegexValidator(regex="^(?=.{8,})",message='Password must be eight characters or longer.')]



class QuestionSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Question
        fields = "__all__"
        extra_kwargs = {
            'string_answer' : {'required':False},
            'bool_answer' : {'required':False},
        }





# create users
class UserSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True)
    class Meta:
        model = User_Model
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'questions',
            'ssn',

            'gender',
            'birthdate',
            'profile_pic',


        )
        extra_kwargs = {
            'password' : {'write_only':True},
            'id' : {'read_only':True},
            'username' : {'required':True},
            'email' : {'required':True},
            'first_name' : {'required':True},
            'last_name' : {'required':True},
            'ssn' : {'required':True},
            
            'questions':{'required':False},
            'gender' : {'required':True},
            'birthdate' : {'required':True},
            'profile_pic' : {'required':False},
        }

    def create(self, validated_data):
        user = User_Model.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            ssn=validated_data['ssn'],
            gender=validated_data['gender'],
            birthdate=validated_data['birthdate'],
        )
        all_questions = validated_data.pop('questions')
        for question_obj in all_questions:
            question_instance=Question.objects.create(**question_obj)
            user.questions.add(question_instance)

        try:
            if(validated_data['profile_pic']!=None):
                user.profile_pic=validated_data['profile_pic']
                user.save()
        except:
                user.save()
        
        return user


#change password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=30)
    new_password1 = serializers.CharField(
        required=True,
        max_length=30,
        validators = Password_validation
        )
    new_password2 = serializers.CharField(required=True, max_length=30)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError(('Old password was entered incorrectly'))
        if data['new_password1']!=data['new_password2']:
            raise serializers.ValidationError("Passwords are not the same")
        if data['old_password']==data['new_password1']:
            raise serializers.ValidationError("New password cannot be the same as current password")
        return data
    


#send email before register a user:
class SendregisterEmailSerializer(serializers.Serializer):
    model = User_Model
    email = serializers.EmailField(required=True)
    username=serializers.CharField(required=True)

    def validate(self,data):
        if (User_Model.objects.filter(email=data['email'])):
            raise serializers.ValidationError("There is another account with this email")
        if (User_Model.objects.filter(username=data['username'])):
            raise serializers.ValidationError("There is another account with this username")
        return data



#send reset password email:
class SendpasswordresetEmailSerializer(serializers.Serializer):
    model = User_Model
    email = serializers.EmailField(required=True)

    def validate(self,data):
        # if not(User_model.objects.filter(email=data['email'])):
        #     raise serializers.ValidationError("there is no email like this!")
        if not User_Model.objects.filter(email=data['email']):
            raise serializers.ValidationError("Email Does Not Exist")
        return data




#Serializer for reset password after confirm email
class ResetPasswordSerializer(serializers.Serializer):
    model = User_Model

    new_password1 = serializers.CharField(
        required=True,
        max_length=30,
        validators = Password_validation
        )
    new_password2 = serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    def validate(self,data):
        if data['new_password1']!=data['new_password2']:
            raise serializers.ValidationError("Passwords are not the same")
        if not User_Model.objects.filter(email=data['email']):
            raise serializers.ValidationError("Email Does Not Exist")
        if get_object_or_404(User_Model, email=data['email']).check_password(data['new_password1']):
            raise serializers.ValidationError("New password cannot be the same as current password")
        return data



class GetUserDataSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField('get_profile_url')
    questions=QuestionSerializer(many=True)
    def get_profile_url(self, model):
        if model.profile_pic:
            request = self.context.get("request")
            base_url = request.build_absolute_uri('/').strip("/")
            profile_url = base_url + '/media/' + f"{model.profile_pic}"
            return profile_url

    class Meta:
        model = User_Model
        exclude =['password','user_permissions','groups']


























# class ProfileSerializer(serializers.ModelSerializer):
#     # degree_name = serializers.SerializerMethodField('get_degree')

#     # def get_degree(self,obj):
#     #     print(obj)
#     #     print(obj.degree)
#     #     if(obj.degree):
#     #         return obj.degree.name
#     #     else:
#     #         return "None"
    
#     class Meta:
#         model = User_Model
#         fields = [
#             'id',
#             'first_name',
#             'last_name',
#             'gender',
#             'birthdate',
#             'degree',
#             'university',
#             'profile_pic',
#             'is_hidden',
#             # 'degree_name'
#         ]


#     def validate(self, data):
#         birthdate = data.get('birthdate')
#         if birthdate != None:
#             today = date.today()
#             age = (today - birthdate).days / 365
#             if age < 10:
#                 raise serializers.ValidationError('You must be at least 10 years old')
#         return data