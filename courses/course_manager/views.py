from django.http import HttpResponse
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
        user_id = self.request.user.id
        request.data['user_id'] = user_id
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        course = Course.objects.get(id=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def update(self, request, pk=None):
        course = Course.objects.get(id=pk)
        serializer = CourseSerializer(instance=course, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        course = Course.objects.get(id=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileViewSet(viewsets.ViewSet):
    def create(self, request, pk, class_pk):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success:" f"Dodano plik {class_pk}"}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        file = Files.objects.get(pk=pk)
        with open(file.file.path, 'rb') as response_file:
            response = HttpResponse(response_file, content_type='application/force-download')
            #TODO: change name of returned file
            response['Content-Disposition'] = f'attachment; filename="plikplikplik.pdf"'
        return response
