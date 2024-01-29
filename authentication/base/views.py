from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from .models import UserAccount

@api_view(['POST'])
@permission_classes([AllowAny])
def user_name_dict(request):
    try:
        if not 'pks' in request.data.keys():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        users_ids = request.data['pks']
        out_names = dict()
        for id in users_ids:
            out_names[id] = UserAccount.objects.get(pk=id).first_name
            
        return JsonResponse(out_names, safe=False, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    