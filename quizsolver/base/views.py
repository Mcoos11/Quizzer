from rest_framework.views import APIView
from .serializers import QuizResultSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http.response import JsonResponse
from quizsolver.settings import MEDIA_ROOT, ACCES_KEY
import requests
import random
from random import shuffle


class QuizListView(APIView):
    def get(self, request):
        url = 'http://web-quiz-editor:8000/quiz_editor/quiz_set/'
        token = request.auth.token
        token_str = token.decode('utf-8')
        headers = {'Authorization': f'JWT {token_str}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Błąd pobierania danych'}, status=500)


class QuizSolveView(APIView):
    def get(self, request, quiz_pk):
        pass_key = ACCES_KEY
        quiz_set_url = 'http://web-quiz-editor:8000/quiz_editor/quiz_set/'
        token = request.auth.token
        token_str = token.decode('utf-8')
        headers = {'Authorization': f'JWT {token_str}'}
        quiz_set_response = requests.get(quiz_set_url, headers=headers)

        if quiz_set_response.status_code == 200:
            quiz_set_data = quiz_set_response.json()

            # Znalezienie quizu
            selected_quiz = None
            for quiz in quiz_set_data['results']:
                if quiz['pk'] == quiz_pk:
                    selected_quiz = quiz
                    break

            if selected_quiz:
                number_of_questions = selected_quiz['number_of_questions']
                max_time = selected_quiz['max_time']
                score_to_pass = selected_quiz['score_to_pass']

                # Pobierz pytania
                quiz_question_url = f'http://web-quiz-editor:8000/quiz_editor/quiz_question_set/{quiz_pk}/{pass_key}'
                quiz_question_response = requests.get(quiz_question_url, headers=headers)

                if quiz_question_response.status_code == 200:
                    quiz_question_data = quiz_question_response.json()
                    all_questions = quiz_question_data
                    num_questions_to_draw = min(len(all_questions), number_of_questions)
                    selected_questions = random.sample(all_questions, num_questions_to_draw)

                    # Pobierz odpowiedzi dla każdego pytania
                    for question in selected_questions:
                        question_pk = question['pk']
                        answer_url = f'http://web-quiz-editor:8000/quiz_editor/quiz_answer_set/{question_pk}/{pass_key}'
                        answer_response = requests.get(answer_url, headers=headers)
                        if answer_response.status_code == 200:
                            answers = answer_response.json()
                            # Wymieszaj odpowiedzi
                            shuffle(answers)
                            question['answers'] = answers
                        else:
                            return Response({'error': 'Błąd pobierania danych o odpowiedziach'},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    return Response({
                        'number_of_questions': number_of_questions,
                        'max_time': max_time,
                        'score_to_pass': score_to_pass,
                        'questions': selected_questions
                    })
                else:
                    return Response({'error': 'Błąd pobierania danych o pytaniach'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'error': 'Quiz nie został znaleziony'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Błąd pobierania danych'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Format odpowiedzi
# {
#   "results": [
#     {
#       "question": 1,
#       "answers": [101, 102]
#     },
#     {
#       "question": 2,
#       "answers": [103]
#     },
#     {
#       "question": 3,
#       "answers": [104, 105, 106]
#     }
#   ]
# }

class QuizResultView(APIView):
    def post(self, request, quiz_pk):
        pass_key = ACCES_KEY

        # Pobierz quizy
        quiz_list_url = 'http://web-quiz-editor:8000/quiz_editor/quiz_set/'
        token = request.auth.token
        token_str = token.decode('utf-8')
        headers = {'Authorization': f'JWT {token_str}'}

        quiz_list_response = requests.get(quiz_list_url, headers=headers)

        # Obsługa odpowiedzi
        if quiz_list_response.status_code == 200:
            quiz_list_data = quiz_list_response.json()
            quiz_list = quiz_list_data.get('results', [])

            # Wybierz quiz o danym pk
            selected_quiz = None
            for quiz in quiz_list:
                if quiz['pk'] == quiz_pk:
                    selected_quiz = quiz
                    break

            if selected_quiz:
                # Pobierz pytania
                quiz_question_url = f'http://web-quiz-editor:8000/quiz_editor/quiz_question_set/{quiz_pk}/{pass_key}'
                quiz_question_response = requests.get(quiz_question_url, headers=headers)

                # Obsługa odpowiedzi
                if quiz_question_response.status_code == 200:
                    quiz_question_data = quiz_question_response.json()
                    all_questions = quiz_question_data
                    results = request.data.get('results', [])
                    score = 0
                    for result in results:
                        question_pk = result['question']
                        answers = result['answers']
                        for question in all_questions:
                            if question['pk'] == question_pk:
                                # Pobierz odpowiedzi dla pytania
                                answer_url = f'http://web-quiz-editor:8000/quiz_editor/quiz_answer_set/{question_pk}/{pass_key}'
                                answer_response = requests.get(answer_url, headers=headers)
                                if answer_response.status_code == 200:
                                    question['answers'] = answer_response.json()
                                    correct_answers = [ans['pk'] for ans in question['answers'] if ans['correct']]

                                    if set(answers) == set(correct_answers):
                                        score += 1
                                    else:
                                        score += 0
                                else:
                                    return Response({'error': 'Błąd pobierania danych o odpowiedziach'},
                                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                                break

                    # Obliczanie wyniku
                    max_score = len(all_questions)
                    percentage = (score / max_score) * 100

                    user_id = self.request.user.id

                    score_to_pass = selected_quiz.get('score_to_pass')

                    # Sprawdź czy użytkownik zdał quiz
                    quiz_pass = score >= score_to_pass

                    serializer = QuizResultSerializer(data={
                        'quiz': quiz_pk,
                        'user': user_id,
                        'score': score,
                        'quiz_pass': quiz_pass
                    })
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # Zwróć wynik
                    return Response({
                        'score': score,
                        'max_score': max_score,
                        'percentage': percentage,
                        'user_id': user_id,
                        'quiz_pass': quiz_pass
                    })
                else:
                    return Response({'error': 'Błąd pobierania danych o pytaniach'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'error': 'Nie znaleziono quizu o podanym pk'},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Błąd pobierania danych o quizach'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)




