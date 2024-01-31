from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.http.response import HttpResponse
from .serializers import RequestSerializer
from bs4 import BeautifulSoup

import xml.etree.ElementTree as ET
import os, csv, requests

def api_query(no, tpc, ans_no=None, url=None):
    category_list = ['General Knowledge',
                     'Entertainment: Books',
                     'Entertainment: Film',
                     'Entertainment: Music',
                     'Entertainment: Musicals & Theatres',
                     'Entertainment: Television',
                     'Entertainment: Video Games',
                     'Entertainment: Board Games',
                     'Science & Nature',
                     'Science: Computers',
                     'Science: Mathematics',
                     'Mythology',
                     'Sports',
                     'Geography',
                     'History',
                     'Politics',
                     'Art',
                     'Celebrities',
                     'Animals',
                     'Vehicles',
                     'Entertainment: Comics',
                     'Science: Gadgets',
                     'Entertainment: Japanese Anime & Manga',
                     'Entertainment: Cartoon & Animations',
                     ]
    
    category = category_list.index(tpc) + 9
    
    response = requests.get(f'https://opentdb.com/api.php?amount={no}&category={category}&difficulty=medium&type=boolean')
    results = response.json()['results']
    
    set = {}
    for question_answers in results:
        set[question_answers['question']] = [question_answers['correct_answer'], question_answers['incorrect_answers'][0]]

    return set

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_XML(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        question_set = api_query(
        serializer.validated_data.get('questions_number'), 
        serializer.validated_data.get('topic'),
        serializer.validated_data.get('answers_number'),
        serializer.validated_data.get('url')
        )
        xml_quiz = ET.Element('quiz')
        for question, answers in question_set.items():
            xml_question = ET.SubElement(xml_quiz, 'question')
            xml_question.set('type', 'multichoice')
            ET.SubElement(ET.SubElement(xml_question, 'name'), 'text').text = f'[Question] {question}'
            xml_question_text =  ET.SubElement(xml_question, 'questiontext')
            xml_question_text.set('format', "html")
            ET.SubElement(xml_question_text, 'text').text = question
                                        
            for answer in answers:
                xml_answer = ET.SubElement(xml_question, 'answer')
                ET.SubElement(xml_answer, 'text').text = answer
                xml_answer_feedback = ET.SubElement(xml_answer, 'feedback')
                if answer == answers[0]:
                    xml_answer.set('fraction', "100")
                    ET.SubElement(xml_answer_feedback, 'text').text = "Poprawna odpowiedź!"
                else:
                    xml_answer.set('fraction', "0")
                    ET.SubElement(xml_answer_feedback, 'text').text = "Nie poprawna odpowiedź!"
                ET.SubElement(xml_question, 'shuffleanswers').text = "1"
                ET.SubElement(xml_question, 'answernumbering').text = "abc"
                ET.SubElement(xml_question, 'single').text = "true"
        
        et = ET.tostring(xml_quiz)
        filepath = os.path.join(settings.MEDIA_ROOT, f'{serializer.validated_data.get("topic")}_question_set.xml')
        with open(filepath, 'wb') as response_file:
            response_file.write(bytes('<?xml version="1.0" encoding="UTF-8" ?>', 'utf-8'))
            response_file.write(et)
        with open(filepath, 'r', encoding="utf-8") as response_file:
            response = HttpResponse(response_file, content_type='application/force-download')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'

        return response
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_CSV(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        question_set = api_query(
        serializer.validated_data.get('questions_number'), 
        serializer.validated_data.get('topic'),
        serializer.validated_data.get('answers_nuber'),
        serializer.validated_data.get('url')
        )
        filepath = os.path.join(settings.MEDIA_ROOT, f'{serializer.validated_data.get("topic")}_question_set.csv')
        
        with open(filepath, 'w', encoding="windows-1250", newline='') as response_file:
            writer = csv.writer(response_file, delimiter=";")
            for question, answers in question_set.items():
                writer.writerow([question.replace('\ufeff', ''), '0'])
                for count, answer in enumerate(answers):
                    writer.writerow(['1' if count == 0 else '0', answer.replace('\ufeff', '')])
        with open(filepath, 'r', encoding="windows-1250") as response_file:
            response = HttpResponse(response_file, content_type='text/csv; charset=windows-1250')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filepath)}"'

        return response

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)