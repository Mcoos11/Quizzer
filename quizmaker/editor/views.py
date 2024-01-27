from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import Quiz, QuizQuestion, QuizAnswer, QuizFile
from .serializers import QuizSerializer, QuizQuestionSerializer, QuizAnswerSerializer, QuizFileSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from django.http.response import HttpResponse
from quizmaker.settings import MEDIA_ROOT, ACCES_KEY
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

import base64
import xml.etree.ElementTree as ET
import os, csv

# nie używane
class StandardPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    page_query_param = 'page'

# tworzenie/edycja/usuwanie quizu
class QuizView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = QuizSerializer
    parser_classes = (JSONParser, FormParser)
    http_method_names = ['post', 'patch', 'delete',]
    queryset = Quiz.objects.all()
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.id)

        return Response("Utworzono nowy quiz.", status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, pk):
        user_id = self.request.user.id
        instance = self.get_object()
        if Quiz.objects.get(pk=pk).author == user_id:
            serializer = self.serializer_class(instance=instance, data=request.data, context={'author': user_id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Success": "Zaktualizowno quiz."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można zaktualizować nieswojego quizu!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        if not request.user.pk == quiz.author:
            return Response({"Fail": "To nie Twój quiz!"}, status=status.HTTP_401_UNAUTHORIZED)
        quiz.delete()
        return Response({"Success": f'Usunięto quiz.'}, status=status.HTTP_200_OK)

# zwaraca wszystkie quizy danego użytkownika 
class UserQuizViewSet(ModelViewSet):
    queryset = Quiz.objects.none()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Quiz.objects.filter(author=self.request.user.id)
    
# zwaraca wszystkie quizy możliwe do wypęłnienia 
class QuizViewSet(APIView, PageNumberPagination):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def get(self, request):
        query_set = Quiz.objects.order_by('-created_time')
        query_set =  self.paginate_queryset(query_set, request, view=self)
        serialize_data = QuizSerializer(query_set, many=True).data
        return self.get_paginated_response(serialize_data)
    
    def post(self, request):
        try:
            topic = request.data['topic']
        except KeyError:
            return Response("Błędny temat!", status=status.HTTP_400_BAD_REQUEST)
        query_set = Quiz.objects.filter(topic=topic).order_by('-created_time')
        query_set = self.paginate_queryset(query_set, request, view=self)
        serialize_data = QuizSerializer(query_set, many=True).data
        return self.get_paginated_response(serialize_data)
    
# zwaraca zestaw pytań z wybranego quizu w celu rozwiązania 
class QuizQuestionViewSet(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def get(self, request, quiz_pk):
        res_questions = dict()
        res_answers = dict()
        res_question_n_answers = dict()
        res_answers_types = dict()
        
        questions = Quiz.objects.get(pk=quiz_pk).get_questions()
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
    serializer_class = QuizQuestionSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['post', 'patch', 'delete',]
    queryset = QuizQuestion.objects.all()
    lookup_field = "pk"

    def create(self, request):
        quiz_id = self.request.POST.get("quiz")
        user_id = self.request.user.id
        if Quiz.objects.get(pk=quiz_id).author == user_id:
            if request.FILES.get("media") != None and request.POST.get("media_url") != None:
                return Response({"Fail": "Możliwe jest dodanie tylko jednego pliku do pytania!"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=request.data, context={'author': user_id})
            if serializer.is_valid():
                serializer.save(author=user_id)
                return Response({"Success": "Utworzono nowe pytanie."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można utworzyć pytania do nieswojego quizu!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def destroy(self, request, pk):
        question = QuizQuestion.objects.get(pk=pk)
        if not request.user.pk == question.author:
            return Response({"Fail": "To nie Twoje pytanie!"}, status=status.HTTP_401_UNAUTHORIZED)
        question.delete()
        return Response({"Success": f'Usunięto pytanie.'}, status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk):
        user_id = self.request.user.id
        instance = self.get_object()
        if QuizQuestion.objects.get(pk=pk).public:
            return Response({"Fail": "Nie można zaktualizować publicznego pytania!"}, status=status.HTTP_400_BAD_REQUEST)
        if QuizQuestion.objects.get(pk=pk).author == user_id:
            serializer = self.serializer_class(instance=instance, data=request.data, context={'author': user_id}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Success": "Zaktualizowno pytanie."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można zaktualizować nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_question_set(request, quiz_pk, pass_key=None):
    quiz = Quiz.objects.get(pk=quiz_pk)
    print(ACCES_KEY, pass_key)
    if ACCES_KEY == pass_key:
        query_set = QuizQuestion.objects.filter(quiz=quiz)
        serialize_data = QuizQuestionSerializer(query_set, many=True).data
        return Response(serialize_data, status=status.HTTP_200_OK)
    return Response({"Fail": "Błędny klucz dostępu!"}, status=status.HTTP_401_UNAUTHORIZED)
    
# dodawnie nowych pytań z pliku csv do bazy (NIE WIDOK)
def add_questions_csv(quiz_pk, file_object):
    new_question = None
    with open(file_object.file_name.path, 'r', encoding="windows-1250") as file:
        reader = csv.reader(file, delimiter='\n') 
        for row in reader:
            row = row[0].split(';')
            if (row[0] == '1' or row[0] == '0') and new_question != None:
                QuizAnswer.objects.create(
                    text = row[1],
                    correct = True if row[0] == '1' else False,
                    question = new_question,
                )
            else:
                new_question = QuizQuestion.objects.create(
                    text = row[0].replace("ď»ż", ""),
                    answers_type = "jednokrotny" if row[1] == '0' else "wielokrotny",
                )
                new_question.quiz.add(Quiz.objects.get(pk=quiz_pk))
    file_object.activated = True
    file_object.save()
    
# dodawnie nowych pytań z pliku xml do bazy (NIE WIDOK)
def add_questions_xml(quiz_pk, file_object):
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
                    new_question = QuizQuestion.objects.create(
                        text = question.find('questiontext').find("text").text,
                        answers_type = "jednokrotny" if question.find('single').text == "true" else "wielokrotny",
                    )
                    new_question.media.save(f'xml_import_image.{Image.open(image).format}', ContentFile(image.getvalue()), save=True)
                    new_question.save()
                else:
                    new_question = QuizQuestion.objects.create(
                        text = question.find('questiontext').find('text').text,
                        answers_type = "jednokrotny" if question.find('single').text == "true" else "wielokrotny",
                        media_url = question_image.text
                    )
            else:
                new_question = QuizQuestion.objects.create(
                        text = question.find('questiontext').find('text').text,
                        answers_type = "jednokrotny" if question.find('single').text == "true" else "wielokrotny"
                    )
            new_question.quiz.add(Quiz.objects.get(pk=quiz_pk))
            
            bs_answers = question.find_all('answer')
            for answer in bs_answers:
                QuizAnswer.objects.create(
                    text = answer.find('text').text,
                    correct = True if answer['fraction'] == "100" else False,
                    question = new_question
                )
    
# odbieranie formularza z przesłanm plikiem csv z pytaniami do dodania,
# wywoływanie funkcji z zapisem pytań do bazy
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def file_question_upload(request, quiz_pk):
    serializer = QuizFileSerializer(data=request.data)
    quiz_name = Quiz.objects.get(pk=quiz_pk).name
    if serializer.is_valid():
        serializer.save()
        file_object = QuizFile.objects.filter(activated=False).order_by('-upload_time')[0]
        ext = os.path.splitext(file_object.file_name.path)[1]
        
        if ext == '.csv':
            add_questions_csv(quiz_pk, file_object)
        elif ext == '.xml':
            add_questions_xml(quiz_pk, file_object)
        else:
            file_object.delete()
            return Response({"Fail": "Nie obsługiwany format pliku."}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        return Response({"Success": f'Dodano nowe pytania do puli quizu <b>{quiz_name}</b>.'}, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# usuwanie wszystkich pytań w quizie  
class QuestionDeleteAll(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = QuizQuestionSerializer
    http_method_names = ['delete',]
    lookup_field = "quiz_pk"
    
    def destroy(self, request, quiz_pk):
        quiz = Quiz.objects.get(pk=quiz_pk)
        if not request.user.pk == quiz.author:
            return Response({"Fail": "To nie Twój quiz!"}, status=status.HTTP_401_UNAUTHORIZED)
        QuizQuestion.objects.filter(quiz=quiz).delete()
        return Response({"Success": f'Usunięto wszystkie pytania w quizie {quiz.name}.'}, status=status.HTTP_200_OK)
    

# zwraca wszystkie pytania quizie
class QuestionViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.none()
    serializer_class = QuizQuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination

    def get_queryset(self, quiz_pk):
        return  QuizQuestion.objects.filter(quiz__in=[Quiz.objects.get(pk=quiz_pk)])
    
    def list(self, request, quiz_pk):
        if Quiz.objects.get(pk=quiz_pk).author == request.user.id:
            query_set = self.get_queryset(quiz_pk)
            page = self.paginate_queryset(query_set)                                                                           
            if page is not None:                                                                                              
                serializer = self.get_serializer(page, many=True)                                                             
                return self.get_paginated_response(serializer.data)                                                           
            serializer = self.get_serializer(query_set, many=True)                                                             
            return Response(serializer.data)
        return Response({"Fail": "Nie można wyświetlić listy pytań nieswojego quizu!"}, status=status.HTTP_401_UNAUTHORIZED)

# zwraca wszystkie dostępne pytania     
class AllQuestionViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.none()
    serializer_class = QuizQuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return QuizQuestion.objects.filter(Q(author=self.request.user.id) | Q(public=True))
         
# zwraca wszystkie publiczne pytania     
class PublicQuestionViewSet(ModelViewSet,):
    queryset = QuizQuestion.objects.none()
    serializer_class = QuizQuestionSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return QuizQuestion.objects.filter(public=True)

# tworzenie/edycja/usuwanie odpowiedzi
class AnswerView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    serializer_class = QuizAnswerSerializer
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ['post', 'patch', 'delete',]
    queryset = QuizAnswer.objects.all()
    lookup_field = "pk"

    def create(self, request):
        question_id = self.request.data["question"]
        user_id = self.request.user.id
        question = QuizQuestion.objects.get(pk=question_id)
        if question.author == user_id:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                if self.request.data['correct'] and question.answers_type == 'jednokrotny':
                    other_answers = QuizAnswer.objects.filter(question=question, correct=True).values_list('correct', flat=True)
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
        answer = QuizAnswer.objects.get(pk=pk)
        if answer.question.public:
            return Response({"Fail": "Nie można zaktualizować odpowiedzi do publicznego pytania!"}, status=status.HTTP_400_BAD_REQUEST)
        if answer.question.author == user_id:
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                if self.request.data['correct'] and  answer.question.answers_type == 'jednokrotny':
                    other_answers = QuizAnswer.objects.filter(question=answer.question, correct=True).values_list('correct', flat=True)
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
        answer = QuizAnswer.objects.get(pk=pk)
        if not request.user.pk == answer.question.author:
            return Response({"Fail": "To nie jest odpowiedź do Twojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
        answer.delete()
        return Response({"Success": f'Usunięto odpowiedź.'}, status=status.HTTP_200_OK)

# zwraca wszystkie odpowiedzi danego pytania quizie
class AnswerViewSet(ModelViewSet):
    queryset = QuizAnswer.objects.none()
    serializer_class = QuizAnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    pagination_class = PageNumberPagination
    
    def list(self, request, question_pk):
        question = QuizQuestion.objects.get(pk=question_pk)
        if question.author == request.user.id:
            query_set = QuizAnswer.objects.filter(question=question)
            query_set =  self.paginate_queryset(query_set)
            serialize_data = self.serializer_class(query_set, many=True).data
            return self.get_paginated_response(serialize_data)
        return Response({"Fail": "Nie można wyświetlić listy odpowiedzi nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def quiz_answer_set(request, question_pk, pass_key=None):
    question = QuizQuestion.objects.get(pk=question_pk)
    if ACCES_KEY == pass_key:
        query_set = QuizAnswer.objects.filter(question=question)
        serialize_data = QuizAnswerSerializer(query_set, many=True).data
        return Response(serialize_data, status=status.HTTP_200_OK)
    return Response({"Fail": "Błędny klucz dostępu!"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_backup_csv(request, quiz_pk):
    if request.method == 'GET':
        quiz = Quiz.objects.get(pk=quiz_pk)
        if not request.user.pk == quiz.author:
            return Response({"To nie Twój quiz!"}, status=status.HTTP_401_UNAUTHORIZED)
        questions = QuizQuestion.objects.filter(quiz=quiz)
        filepath = os.path.join(MEDIA_ROOT, "backup_files_to_download", f'quiz_{quiz.name.lower().replace(" ", "_")}_backup.csv')
        
        with open(filepath, 'w', encoding="windows-1250", newline='') as response_file:
            writer = csv.writer(response_file, delimiter=";")
            for question in questions:
                writer.writerow([question.text.replace('\ufeff', ''), '0' if question.answers_type == "jednokrotny" else '1'])
                for answer in QuizAnswer.objects.filter(question=question):
                    writer.writerow(['1' if answer.correct else '0', answer.text.replace('\ufeff', '')])
        with open(filepath, 'r', encoding="windows-1250") as response_file:
            response = HttpResponse(response_file, content_type='text/csv; charset=windows-1250')
            response['Content-Disposition'] = f'attachment; filename="Quiz_{quiz_pk}.csv"'

        return response
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_backup_xml(request, quiz_pk):
    if request.method == 'GET':
        quiz = Quiz.objects.get(pk=quiz_pk)
        if not request.user.pk == quiz.author:
            return Response({"To nie Twój quiz!"}, status=status.HTTP_401_UNAUTHORIZED)
        questions = QuizQuestion.objects.filter(quiz=quiz)
        
        xml_quiz = ET.Element('quiz')
        for question in questions:
            xml_question = ET.SubElement(xml_quiz, 'question')
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
                                        
            for answer in QuizAnswer.objects.filter(question=question):
                xml_answer = ET.SubElement(xml_question, 'answer')
                ET.SubElement(xml_answer, 'text').text = answer.text
                xml_answer_feedback = ET.SubElement(xml_answer, 'feedback')
                if answer.correct:
                    xml_answer.set('fraction', "100")
                    ET.SubElement(xml_answer_feedback, 'text').text = "Poprawna odpowiedź!"
                else:
                    xml_answer.set('fraction', "0")
                    ET.SubElement(xml_answer_feedback, 'text').text = "Nie poprawna odpowiedź!"
                ET.SubElement(xml_question, 'shuffleanswers').text = "1"
                ET.SubElement(xml_question, 'answernumbering').text = "abc"
                if question.answers_type == 'jednokrotny':
                    ET.SubElement(xml_question, 'single').text = "true"
                elif question.answers_type == 'wielokrotny':
                    ET.SubElement(xml_question, 'single').text = "false"
        
        et = ET.tostring(xml_quiz)
        filepath = os.path.join(MEDIA_ROOT, "backup_files_to_download", f'quiz_{quiz.name.lower().replace(" ", "_")}_backup.xml')
        with open(filepath, 'wb') as response_file:
            response_file.write(bytes('<?xml version="1.0" encoding="UTF-8" ?>', 'utf-8'))
            response_file.write(et)
        with open(filepath, 'r', encoding="utf-8") as response_file:
            response = HttpResponse(response_file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="Quiz_{quiz_pk}.xml"'

        return response
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)