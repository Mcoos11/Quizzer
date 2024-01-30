from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Survey, SurveyQuestion, SurveyAnswer, SurveyFile
from .serializers import SurveySerializer, SurveyQuestionSerializer, SurveyAnswerSerializer, SurveyFileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from django.http.response import HttpResponse
from surveymaker.settings import MEDIA_ROOT, ACCESS_KEY
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

import base64
import xml.etree.ElementTree as ET
import os, csv

# tworzenie/edycja/usuwanie ankiety
class SurveyView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = SurveySerializer
    parser_classes = (JSONParser, FormParser)
    http_method_names = ['post', 'patch', 'delete',]
    queryset = Survey.objects.all()
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.id)

        return Response("Utworzono nową ankietę.", status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, pk):
        user_id = self.request.user.id
        instance = self.get_object()
        try:
            survey = Survey.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if survey.author == user_id:
            serializer = self.serializer_class(instance=instance, data=request.data, context={'author': user_id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Success": "Zaktualizowno ankietę."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można zaktualizować nieswojej ankiety!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.pk == survey.author:
            return Response({"Fail": "To nie Twoja ankieta!"}, status=status.HTTP_401_UNAUTHORIZED)
        survey.delete()
        return Response({"Success": f'Usunięto ankietę.'}, status=status.HTTP_200_OK)

# zwaraca wszystkie ankiety danego użytkownika 
class UserSurveyViewSet(ModelViewSet):
    queryset = Survey.objects.none()
    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination

    def list(self, request):
        query_set = Survey.objects.filter(author=request.user.id)
        query_set =  self.paginate_queryset(query_set)
        serialize_data = self.serializer_class(query_set, many=True).data
        return self.get_paginated_response(serialize_data)
    
# zwaraca wszystkie ankiety możliwe do wypęłnienia 
class SurveyViewSet(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def get(self, request):
        query_set = Survey.objects.order_by('-created_time')
        query_set =  self.paginate_queryset(query_set, request, view=self)
        serialize_data = SurveySerializer(query_set, many=True).data
        return self.get_paginated_response(serialize_data)
    
    def post(self, request):
        try:
            topic = request.data['topic']
        except KeyError:
            return Response("Błędny temat!", status=status.HTTP_400_BAD_REQUEST)
        query_set = Survey.objects.filter(topic=topic).order_by('-created_time')
        query_set =  self.paginate_queryset(query_set, request, view=self)
        serialize_data = SurveySerializer(query_set, many=True).data
        return self.get_paginated_response(serialize_data)
    
# zwaraca zestaw pytań z wybranej ankiety w celu rozwiązania 
class SurveyQuestionViewSet(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def get(self, request, survey_pk):
        res_questions = dict()
        res_answers = dict()
        res_question_n_answers = dict()
        res_answers_types = dict()
        
        try:
            questions = Survey.objects.get(pk=survey_pk).get_questions()
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        for question in questions:
            res_questions[question.pk] = question.text
            res_answers_types[question.pk] = question.answers_type
            res_question_n_answers[question.pk] = list()
            for answer in question.get_answers():
                res_answers[answer.pk] = answer.text
                res_question_n_answers[question.pk].append(answer.pk)
        
        return JsonResponse(
            {
                'questions': res_questions,
                'answers': res_answers,
                'answers_types': res_answers_types,
                'question_n_answers': res_question_n_answers
            },
            safe=False, status=status.HTTP_200_OK
        )

# tworzenie/edycja/usuwanie pytania
class QuestionView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = SurveyQuestionSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    http_method_names = ['post', 'patch', 'delete',]
    queryset = SurveyQuestion.objects.all()
    lookup_field = "pk"

    def create(self, request):
        survey_id = self.request.data.get("survey")[0]
        user_id = self.request.user.id
        try:
            survey = Survey.objects.get(pk=survey_id)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if survey.author == user_id:
            if request.FILES.get("media") != None and request.data.get("media_url") != None:
                return Response({"Fail": "Możliwe jest dodanie tylko jednego pliku do pytania!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=request.data, context={'author': user_id})
            if serializer.is_valid():
                serializer.save(author=user_id)
                return Response({"Success": "Utworzono nowe pytanie."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można utworzyć pytania do nieswojj ankiety!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        try:
            question = SurveyQuestion.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Pytanie o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.pk == question.author:
            return Response({"Fail": "To nie Twoje pytanie!"}, status=status.HTTP_401_UNAUTHORIZED)
        question.delete()
        return Response({"Success": f'Usunięto pytanie.'}, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk):
        user_id = self.request.user.id
        instance = self.get_object()
        try:
            question = SurveyQuestion.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Pytanie o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if question.author == user_id:
            serializer = self.serializer_class(instance=instance, data=request.data, context={'author': user_id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Success": "Zaktualizowno pytanie."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można zaktualizować nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
    
# dodawnie nowych pytań z pliku csv do bazy (NIE WIDOK)
def add_questions_csv(survey_pk, file_object):
    new_question = None
    with open(file_object.file_name.path, 'r', encoding="windows-1250") as file:
        reader = csv.reader(file, delimiter='\n') 
        for row in reader:
            row = row[0].split(';')
            if (row[0] == '1' or row[0] == '0') and new_question != None:
                SurveyAnswer.objects.create(
                    text = row[1],
                    correct = True if row[0] == '1' else False,
                    question = new_question,
                )
            else:
                new_question = SurveyQuestion.objects.create(
                    text = row[0].replace("ď»ż", ""),
                    answers_type = "jednokrotny" if row[1] == '0' else "wielokrotny",
                    status = False
                )
                try:
                    survey = Survey.objects.get(pk=survey_pk)
                except ObjectDoesNotExist:
                    return False
                new_question.survey.add(survey)
    file_object.activated = True
    file_object.save()
    return True
    
# dodawnie nowych pytań z pliku xml do bazy (NIE WIDOK)
def add_questions_xml(survey_pk, file_object):
    new_question = None
    with open(file_object.file_name.path, 'r') as file:
        data = file.read()
        bs_data = BeautifulSoup(data, "xml")
        bs_questions = bs_data.find_all('question')
        for question in bs_questions:
            question_image = question.find("image")
            if question_image:
                if question.find("image_base64"):
                    image_code = question.find("image_base64").text
                    image_data = image_code.encode()
                    image = BytesIO(base64.b64decode(image_data))
                    new_question = SurveyQuestion.objects.create(
                        text = question.find('questiontext').find("text").text,
                        answers_type = "jednokrotny" if question.find('single').text == "true" else "wielokrotny",
                        status = False,
                    )
                    new_question.media.save(f'xml_import_image.{Image.open(image).format}', ContentFile(image.getvalue()), save=True)
                    new_question.save()
                else:
                    new_question = SurveyQuestion.objects.create(
                        text = question.find('questiontext').find('text').text,
                        answers_type = "jednokrotny" if question.find('single').text == "true" else "wielokrotny",
                        media_url = question_image.text,
                        status = False,
                    )
            else:
                new_question = SurveyQuestion.objects.create(
                        text = question.find('questiontext').find('text').text,
                        answers_type = "jednokrotny" if question.find('single').text == "true" else "wielokrotny",
                        status = False,
                    )
            try:
                survey = Survey.objects.get(pk=survey_pk)
            except ObjectDoesNotExist:
                return False
            new_question.survey.add(survey)
            
            bs_answers = question.find_all('answer')
            for answer in bs_answers:
                SurveyAnswer.objects.create(
                    text = answer.find('text').text,
                    correct = bool(answer['user-answer']),
                    question = new_question,
                )
    return True
    
# odbieranie formularza z przesłanm plikiem csv z pytaniami do dodania,
# wywoływanie funkcji z zapisem pytań do bazy
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def file_question_upload(request, survey_pk):
    serializer = SurveyFileSerializer(data=request.data)
    survey_name = Survey.objects.get(pk=survey_pk).name
    if serializer.is_valid():
        serializer.save()
        file_object = SurveyFile.objects.filter(activated=False).order_by('-upload_time')[0]
        ext = os.path.splitext(file_object.file_name.path)[1]
        
        if ext == '.csv':
            if not add_questions_csv(survey_pk, file_object): return Response({"Fail": "Błędne dane w pliku."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif ext == '.xml':
            if not add_questions_xml(survey_pk, file_object): return Response({"Fail": "Błędne dane w pliku."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            file_object.delete()
            return Response({"Fail": "Nie obsługiwany format pliku."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response({"Success": f'Dodano nowe pytania do ankiety <b>{survey_name}</b>.'}, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# usuwanie wszystkich pytań w ankiecie  
class QuestionDeleteAll(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = SurveyQuestionSerializer
    http_method_names = ['delete',]
    lookup_field = "survey_pk"
    
    def destroy(self, request, survey_pk):
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST) 
        if not request.user.pk == survey.author:
            return Response({"Fail": "To nie Twoja ankieta!"}, status=status.HTTP_401_UNAUTHORIZED)
        SurveyQuestion.objects.filter(survey=survey).delete()
        return Response({"Success": f'Usunięto wszystkie pytania w ankiecie {survey.name}.'}, status=status.HTTP_200_OK)
    

# zwraca wszystkie pytania ankiecie
class QuestionViewSet(ModelViewSet):
    queryset = SurveyQuestion.objects.none()
    serializer_class = SurveyQuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination
    
    def list(self, request, survey_pk):
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if survey.author == request.user.id:
            query_set = SurveyQuestion.objects.filter(survey__in=[Survey.objects.get(pk=survey_pk)])
            query_set =  self.paginate_queryset(query_set)
            serialize_data = self.serializer_class(query_set, many=True).data
            return self.get_paginated_response(serialize_data)
        return Response({"Fail": "Nie można wyświetlić listy pytań nieswojej ankiety!"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def survey_question_set(request, survey_pk, pass_key=None):
    try:
        survey = Survey.objects.get(pk=survey_pk)
    except ObjectDoesNotExist:
        return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)

    if ACCESS_KEY == pass_key:
        query_set = SurveyQuestion.objects.filter(survey=survey)
        serialize_data = SurveyQuestionSerializer(query_set, many=True).data
        return Response(serialize_data, status=status.HTTP_200_OK)
    return Response({"Fail": "Błędny klucz dostępu!"}, status=status.HTTP_401_UNAUTHORIZED)

# tworzenie/edycja/usuwanie odpowiedzi
class AnswerView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = SurveyAnswerSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['post', 'patch', 'delete',]
    queryset = SurveyAnswer.objects.all()
    lookup_field = "pk"

    def create(self, request):
        question_id = self.request.data["question"]
        user_id = self.request.user.id
        try:
            question = SurveyQuestion.objects.get(pk=question_id)
        except ObjectDoesNotExist:
            return Response({"Fail": "Pytanie o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if question.author == user_id:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if self.request.data['correct'] and question.answers_type == 'jednokrotny':
                    other_answers = SurveyAnswer.objects.filter(question=question, correct=True).values_list('correct', flat=True)
                    if True in other_answers:
                        return Response({"Fail": 'Istnieje już poprawna odpowiedź dla tego pytania! Dla pytań jednokrotnego wyboru dopuszczalna jest tylko jedna poprawna odpowiedź.'}, status=status.HTTP_409_CONFLICT)
                    else:
                        serializer.save()
                        return Response({"Success": f'Utworzono nową odpowiedź do pytania <b>{question.text}</b>.'}, status=status.HTTP_201_CREATED)
                else:
                    serializer.save()
                    return Response({"Success": f'Utworzono nową odpowiedź do pytania <b>{question.text}</b>.'}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można utworzyć pytania do nieswojego quizu!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def partial_update(self, request, pk):
        user_id = self.request.user.id
        instance = self.get_object()
        try:
            answer = SurveyAnswer.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Odpowiedź o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if answer.question.public:
            return Response({"Fail": "Nie można zaktualizować odpowiedzi do publicznego pytania!"}, status=status.HTTP_400_BAD_REQUEST)
        if answer.question.author == user_id:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                if self.request.data['correct'] and  answer.question.answers_type == 'jednokrotny':
                    other_answers = SurveyAnswer.objects.filter(question=answer.question, correct=True).values_list('correct', flat=True)
                    if True in other_answers:
                        return Response({"Fail": 'Istnieje już poprawna odpowiedź dla tego pytania! Dla pytań jednokrotnego wyboru dopuszczalna jest tylko jedna poprawna odpowiedź.'}, status=status.HTTP_409_CONFLICT)
                    else:
                        serializer.save()
                        return Response({"Success": "Zaktualizowno odpowiedź."}, status=status.HTTP_201_CREATED)
                else:
                    serializer.save()
                    return Response({"Success": "Zaktualizowno odpowiedź."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można zaktualizować odpowiedzi do nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        try:
            answer = SurveyAnswer.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Odpowiedź o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.pk == answer.question.author:
            return Response({"Fail": "To nie jest odpowiedź do Twojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
        answer.delete()
        return Response({"Success": f'Usunięto odpowiedź.'}, status=status.HTTP_200_OK)

# zwraca wszystkie pytania w ankiecie
class AnswerViewSet(ModelViewSet):
    queryset = SurveyAnswer.objects.none()
    serializer_class = SurveyAnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination
    
    def list(self, request, question_pk):
        try:
            question = SurveyQuestion.objects.get(pk=question_pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Pytanie o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if question.author == request.user.id:
            query_set = SurveyAnswer.objects.filter(question=question)
            query_set =  self.paginate_queryset(query_set)
            serialize_data = self.serializer_class(query_set, many=True).data
            return self.get_paginated_response(serialize_data)
        return Response({"Fail": "Nie można wyświetlić listy odpowiedzi nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def survey_answer_set(request, question_pk, pass_key=None):
    try:
        question = SurveyQuestion.objects.get(pk=question_pk)
    except ObjectDoesNotExist:
        return Response({"Fail": "Pytanie o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
    
    if ACCESS_KEY == pass_key:
        query_set = SurveyAnswer.objects.filter(question=question)
        serialize_data = SurveyAnswerSerializer(query_set, many=True).data
        return Response(serialize_data, status=status.HTTP_200_OK)
    return Response({"Fail": "Błędny klucz dostępu!"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_backup_csv(request, survey_pk):
    if request.method == 'GET':
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.pk == survey.author:
            return Response({"To nie Twoja ankieta!"}, status=status.HTTP_401_UNAUTHORIZED)
        questions = SurveyQuestion.objects.filter(survey=survey)
        filepath = os.path.join(MEDIA_ROOT, "backup_files_to_download", f'quiz_{survey.name.lower().replace(" ", "_")}_backup.csv')
        
        with open(filepath, 'w', encoding="windows-1250", newline='') as response_file:
            writer = csv.writer(response_file, delimiter=";")
            for question in questions:
                writer.writerow([question.text.replace('\ufeff', ''), '0' if question.answers_type == "jednokrotny" else '1'])
                for answer in SurveyAnswer.objects.filter(question=question):
                    if not answer.user_answer:
                        writer.writerow(['', answer.text.replace('\ufeff', '')])
        with open(filepath, 'r', encoding="windows-1250") as response_file:
            response = HttpResponse(response_file, content_type='text/csv; charset=windows-1250')
            response['Content-Disposition'] = f'attachment; filename="Quiz_{survey_pk}.csv"'

        return response
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_backup_xml(request, survey_pk):
    if request.method == 'GET':
        try:
            survey = Survey.objects.get(pk=survey_pk)
        except ObjectDoesNotExist:
            return Response({"Fail": "Ankieta o podanym id nie istnieje!"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.pk == survey.author:
            return Response({"To nie Twoja ankieta!"}, status=status.HTTP_401_UNAUTHORIZED)
        questions = SurveyQuestion.objects.filter(survey=survey)
        
        xml_survey = ET.Element('survey')
        for question in questions:
            xml_question = ET.SubElement(xml_survey, 'question')
            xml_question.set('type', 'multichoice')
            ET.SubElement(ET.SubElement(xml_question, 'name'), 'text').text = f'[Question{question.pk}] {question.text}'
            xml_question_text =  ET.SubElement(xml_question, 'questiontext')
            xml_question_text.set('format', "html")
            ET.SubElement(xml_question_text, 'text').text = question.text
            if question.media_url:
                ET.SubElement(xml_question, 'image').text = question.media_url
            elif question.media:
                with open(question.media.path, 'rb') as image_file:
                    data = base64.b64encode(image_file.read())
                    ET.SubElement(ET.SubElement(xml_question, 'image'), 'image_base64').text = data.decode()
                                        
            for answer in SurveyAnswer.objects.filter(question=question):
                xml_answer = ET.SubElement(xml_question, 'answer')
                ET.SubElement(xml_answer, 'text').text = answer.text
                xml_answer.set('user-answer', str(answer.user_answer))
                ET.SubElement(xml_question, 'shuffleanswers').text = "1"
                ET.SubElement(xml_question, 'answernumbering').text = "abc"
                if question.answers_type == 'jednokrotny':
                    ET.SubElement(xml_question, 'single').text = "true"
                elif question.answers_type == 'wielokrotny':
                    ET.SubElement(xml_question, 'single').text = "false"
        
        et = ET.tostring(xml_survey)
        filepath = os.path.join(MEDIA_ROOT, "backup_files_to_download", f'survey_{survey.name.lower().replace(" ", "_")}_backup.xml')
        with open(filepath, 'wb') as response_file:
            response_file.write(bytes('<?xml version="1.0" encoding="UTF-8" ?>', 'utf-8'))
            response_file.write(et)
        with open(filepath, 'r', encoding="utf-8") as response_file:
            response = HttpResponse(response_file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="Survey_{survey_pk}.xml"'

        return response
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)