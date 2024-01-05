from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Quiz, QuizQuestion, QuizAnswer
from .serializers import QuizSerializer, QuizQuestionSerializer, QuizAnswerSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.decorators import action

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

# zwaraca wszystkie quizy danego użytkownika 
class UserQuizViewSet(ModelViewSet):
    queryset = Quiz.objects.none()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]

    def list(self, request):
        query_set = Quiz.objects.filter(author=request.user.id)
        return Response(self.serializer_class(query_set, many=True).data, status=status.HTTP_200_OK)
    
# zwaraca wszystkie quizy możliwe do wypęłnienia 
class QuizViewSet(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def get(self, request):
        query_set = Quiz.objects.order_by('-created_time')
        return Response(QuizSerializer(query_set, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            topic = request.data['topic']
        except KeyError:
            return Response("Błędny temat!", status=status.HTTP_400_BAD_REQUEST)
        query_set = Quiz.objects.filter(topic=topic).order_by('-created_time')
        return Response(QuizSerializer(query_set, many=True).data, status=status.HTTP_200_OK)

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

# zwraca wszystkie pytania quizie
class QuestionViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.none()
    serializer_class = QuizQuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    
    def list(self, request, quiz_pk):
        if Quiz.objects.get(pk=quiz_pk).author == request.user.id:
            query_set = QuizQuestion.objects.filter(quiz__in=[Quiz.objects.get(pk=quiz_pk)])
            return Response(self.serializer_class(query_set, many=True).data, status=status.HTTP_200_OK)
        return Response({"Fail": "Nie można wyświetlić listy pytań nieswojego quizu!"}, status=status.HTTP_401_UNAUTHORIZED)

# zwraca wszystkie dostępne pytania     
class AllQuestionViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.none()
    serializer_class = QuizQuestionSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    
    def list(self, request):
        query_set = QuizQuestion.objects.filter(Q(author=request.user.id) | Q(public=True))
        return Response(self.serializer_class(query_set, many=True).data, status=status.HTTP_200_OK)

# zwraca wszystkie dostępne pytania     
class PublicQuestionViewSet(ModelViewSet):
    queryset = QuizQuestion.objects.none()
    serializer_class = QuizQuestionSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    
    def list(self, request):
        query_set = QuizQuestion.objects.filter(public=True)
        return Response(self.serializer_class(query_set, many=True).data, status=status.HTTP_200_OK)

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
                serializer.save()
                return Response({"Success": "Zaktualizowno odpowiedź."}, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"Fail": "Nie można zaktualizować odpowiedzi do nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)

# zwraca wszystkie pytania quizie
class AnswerViewSet(ModelViewSet):
    queryset = QuizAnswer.objects.none()
    serializer_class = QuizAnswerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)
    http_method_names = ['get', ]
    
    def list(self, request, question_pk):
        question = QuizQuestion.objects.get(pk=question_pk)
        if question.author == request.user.id:
            query_set = QuizAnswer.objects.filter(question=question)
            return Response(self.serializer_class(query_set, many=True).data, status=status.HTTP_200_OK)
        return Response({"Fail": "Nie można wyświetlić listy odpowiedzi nieswojego pytania!"}, status=status.HTTP_401_UNAUTHORIZED)