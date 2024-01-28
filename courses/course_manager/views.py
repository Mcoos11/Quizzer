from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Course, Files
from .serializers import CourseSerializer, FileSerializer


class CourseViewSet(viewsets.ViewSet):

    def list(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def create(self, request):
        # TODO: check when login fixed
        # user_id = self.request.user.id
        user_id = 1
        data = request.data
        data['owner'] = user_id
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # TODO: check when login fixed
        # user_id = self.request.user.id
        user_id = 1
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
        # TODO: check when login fixed
        # user_id = self.request.user.id
        user_id = 1
        data = request.data
        data['owner'] = user_id
        course = Course.objects.get(id=pk)
        if course.owner == data['owner']:
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        # TODO: check when login fixed
        # user_id = self.request.user.id
        user_id = 2
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
        # TODO: check when login fixed
        # user_id = self.request.user.id
        user_id = 3
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
        data= request.data
        data['k_course_id']= pk
        data['k_class_id']= class_pk
        serializer = FileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success:" f"Dodano plik {class_pk}"}, status=status.HTTP_201_CREATED)
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
        files = Files.objects.filter(class_id=pk)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

class ClassViewSet(viewsets.ViewSet):
    def create(self, request, course_pk):
        pass
