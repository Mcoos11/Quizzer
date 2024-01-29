from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from .models import Course, Files, Class
from .serializers import CourseSerializer, FileSerializer, ClassSerializer


class CourseViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def list(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def create(self, request):
        user_id = self.request.user.id
        data = request.data
        data['owner'] = user_id
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        user_id = self.request.user.id
        data = request.data
        data['owner'] = user_id
        course = Course.objects.get(id=pk)
        serializer = CourseSerializer(instance=course, data=data)
        if course.owner == data['owner']:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        user_id = self.request.user.id
        data = request.data
        data['owner'] = user_id
        course = Course.objects.get(id=pk)
        if course.owner == data['owner']:
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        user_id = self.request.user.id
        course = Course.objects.get(id=pk)
        if user_id == course.owner:
            serializer = CourseSerializer(instance=course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif course.participants:
            if user_id in course.participants:
                serializer = CourseSerializer(instance=course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Fail:" "User not an owner or participant"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"Fail:" "User not an owner or participant"}, status=status.HTTP_401_UNAUTHORIZED)

    def add_user(self, request, pk=None):
        user_id = self.request.user.id
        course = Course.objects.get(id=pk)
        if course.participants:
            if user_id not in course.participants:
                course.participants.append(user_id)
                course.save()
                return Response({"Success:" f"Dodano uzytkownika {user_id}"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"Fail:" "User is already an participant"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            course.participants = [user_id]
            course.save()
            return Response({"Success:" f"Dodano uzytkownika {user_id}"}, status=status.HTTP_201_CREATED)


class FileViewSet(viewsets.ViewSet):
    def create(self, request, pk, class_pk):
        data = request.data
        data['k_course'] = pk
        data['k_class'] = class_pk
        print(data)
        class_obj = Class.objects.get(pk=class_pk)
        if class_obj.k_course_id != pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = FileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Success:" f"Dodano plik do klasy {class_pk}"}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        file = Files.objects.get(pk=pk)
        with open(file.file.path, 'rb') as response_file:
            response = HttpResponse(response_file, content_type='application/force-download')
            # TODO: change name of returned file
            response['Content-Disposition'] = f'attachment; filename="plikplikplik.pdf"'
        return response

    def list(self, request, pk=None):
        files = Files.objects.filter(k_course_id=pk)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

    # TODO: deleting files


class ClassViewSet(viewsets.ViewSet):
    def add_class(self, request, pk, class_pk):
        user_id = self.request.user.id
        course = Course.objects.get(id=pk)
        if course.owner != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            data=request.data
            data['k_course']= pk
            serializer = ClassSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete_class(self, request, pk, class_pk):
        user_id = self.request.user.id
        course = Course.objects.get(id=pk)
        if course.owner != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            class_obj = Class.objects.get(id=class_pk)
            class_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


    def update_class(self, request, pk, class_pk):
        user_id = self.request.user.id
        course = Course.objects.get(id=pk)
        if course.owner != user_id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            data = request.data
            data['k_course'] = course.pk
            class_obj = Class.objects.get(pk=class_pk)
            serializer = ClassSerializer(instance=class_obj, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

