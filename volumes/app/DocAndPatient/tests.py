from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from User.models import User,City
import datetime
from .models import Medicine

# Create your tests here.


class NotLoggedInDoctorsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.city=City.objects.create(city_name="Tehran")
    def test_api_create_list_doctor(self):
        url = reverse("DocAndPatient:ListCreateDoctor")



        data={
        "username": "doctor@test.com",
        "password": "Ab654321",
        "first_name": "test",
        "last_name": "test",
        "ssn": "12125458",
        "gender": "M",
        "birthdate": "2022-05-24",
        "user_city": "1",
        "relationship_status": "string",
        "isVaccinated": "string",
        "msn": "1212545488",
        "degree": "GP",
        "field": "CAR",
        "experience": "0",
        "about": "string",
        "hours_of_work": "string",
        "address": "string",
        "latitude": "12.232323",
        "longitude": "13.656565"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




        data={
        "username": "doctor@test.com",
        "password": "Ab654321",
        "first_name": "test",
        "last_name": "test",
        "ssn": "12125458",
        "gender": "M",
        "birthdate": "2022-05-24",
        "user_city": "1",
        "relationship_status": "string",
        "isVaccinated": "string",
        "msn": "1212545488",
        "degree": "GP",
        "field": "CAR",
        "experience": "0",
        "about": "string",
        "hours_of_work": "string",
        "address": "string",
        "latitude": "12.232323",
        "longitude": "13.656565"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




        url = reverse("DocAndPatient:ListCreateDoctor")
        response = self.client.get(url,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MedicinesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username= "test_email@test.com", password= "Ab654321")
        self.superuser = User.objects.create_superuser(username= "test_email_superuser@test.com", password= "Ab654321")
        Medicine.objects.create(name="testmedicine",type="A")
        self.client = APIClient()



    def test_get_medicine_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("DocAndPatient:Medicines-list")
        response = self.client.get(url,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_post_medicine_list(self):
        self.client.force_authenticate(user=self.superuser)
        url = reverse("DocAndPatient:Medicines-list")
        data={
        "name": "testmedicine",
        "type": "A"
        }
        response = self.client.post(url,data,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_medicine_item(self):   
        self.client.force_authenticate(user=self.user)
        url = reverse("DocAndPatient:Medicines-detail",kwargs={'pk':1})
        response = self.client.get(url,format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)






# class NotLoggedInAccountTest(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.city=City.objects.create(city_name="Tehran")


    
#     def test_api_register_and_login(self):
#         url = reverse("User:register")

#         data =  {"username" : "test_user@test.com", "password" : "Ab654321", "first_name":"testname","last_name":"test_last_name","relationship_status":"inrel","isVaccinated":"yes","user_city":"1"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         data = {"username" : "test_user@test.com", "password" : "12565656", "first_name":"testname","last_name":"test_last_name","relationship_status":"inrel","isVaccinated":"yes","user_city":"1"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

#         url = reverse("User:login")
#         data =  {"username" : "test_user@test.com", "password" : "Ab654321"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


#     def test_api_reset_password(self):
#         user = User.objects.create(username="test_email@test.com", password="Ab654321")

#         url = reverse("User:reset_password")

#         data =  {"new_password1" : "ABcd12345", "new_password2" : "ABcd12345", "email" : "test_email@test.com"}
#         response = self.client.put(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         data =  {"new_password1" : "Ab", "new_password2" : "654321", "email" : "test_email@test.com"}
#         response = self.client.put(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



#     def test_api_get_city(self):
#         url = reverse("User:cities")
#         response = self.client.get(url,format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)



#     def test_api_get_city(self):
#         url = reverse("User:cities")
#         response = self.client.get(url,format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class LoggedInAccountTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create(username= "test_email@test.com", password= "Ab654321")
#         self.client = APIClient()
        
#     def test_api_change_password(self):
#         self.client.force_authenticate(user=self.user)
#         url = reverse("User:change_password")

#         data =  {"new_password1" : "Ab", "new_password2" : "654321", "old_password" : "Ab654321"}
#         response = self.client.put(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    

#     def test_api_get_user(self):
#         self.client.force_authenticate(user=self.user)
#         url = reverse("User:user")
#         response = self.client.get(url,format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)



#     def test_api_send_reset_password_email(self):
#         url = reverse("User:send_reset_password_email")
#         data =  {"email" : "test_email@test.com"}
#         response = self.client.post(url,data,format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)









# class NotLoggedInProfileAccountTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse("User:profile")

#     def test_api_unauthorized_get_profile(self):
#         response = self.client.get(path=self.url, format="json")

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_api_unauthorized_put_profile(self):
#         data = {
#             "first_name": "John", "last_name": "Warner",
#             "gender": "M", "birthdate": "2020-01-01",
#             "ssn": "1234567890", "citizens_ssn": "12"
#         }

#         response = self.client.patch(path=self.url, data=data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_api_unauthorized_patch_profile(self):
#         data = {
#             "first_name": "John", "last_name": "Warner",
#             "gender": "M", "birthdate": "2020-01-01"
#         }
#         response = self.client.patch(path=self.url, data=data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class LoggedInProfileAccountTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username="testuser@domain.com", password="ILoveDjango")
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse("User:profile")
        
#     def test_api_authorized_get_profile(self):
#         response = self.client.get(path=self.url, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_api_authorized_put_profile(self):
#         City.objects.create(city_name="new yourk")
#         data = {
#             "first_name": "John", "last_name": "Warner",
#             "gender": "M", "birthdate": "2020-01-01",
#             "ssn": "1234567890", "citizens_ssn": "12"
#         }

#         response = self.client.patch(path=self.url, data=data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_api_authorized_patch_profile(self):
#         data = {
#             "first_name": "John", "last_name": "Warner",
#             "gender": "M", "birthdate": "2020-01-01"
#         }
#         response = self.client.patch(path=self.url, data=data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
