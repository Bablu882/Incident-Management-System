
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer,IncidentSerializer,IncidentSerializerput
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Incident
from django.utils import timezone


class BearerAuthentication(TokenAuthentication):
    keyword = 'Bearer'





class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'User register successfully ! Now login for create token !','user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': {'Both Username and password are required.'}}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'username':user.username,'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': {'Invalid credentials'}}, status=status.HTTP_401_UNAUTHORIZED)



class CreateIncidentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerAuthentication]

    def get(self, request):
        incidents = Incident.objects.filter(reporter=request.user).order_by('-id')
        serializer = IncidentSerializer(incidents, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = IncidentSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            incident = serializer.save(reporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        incident_id=request.data.get('incident_id')
        incident_details=request.data.get('incident_details')
        priority=request.data.get('priority')
        incident_status=request.data.get('incident_status')

        if not incident_id:
            return Response({'message':{'incident_id required !'}})

        try:
            incident = Incident.objects.get(incident_id=incident_id)
        except Incident.DoesNotExist:
            return Response({'message': 'Incident not found.'}, status=status.HTTP_404_NOT_FOUND)
        print(incident.incident_status)
        if incident.reporter != request.user:
            return Response({'message': 'You are not authorized user to update this incident.'},status=status.HTTP_403_FORBIDDEN)
        # Check if the incident status is Closed 
        if incident.incident_status =='Closed':
            return Response({'message':'Closed status can not be updated'},status=status.HTTP_403_FORBIDDEN)    
        if incident_status not in ['In Progress','Open','Closed']:
            return Response({'message': f'Invalid choice {incident_status}'}, status=status.HTTP_400_BAD_REQUEST)    
        if priority not in ['High','Medium','Low']:
            return Response({'message':f'invalid choice {priority}'},status=status.HTTP_400_BAD_REQUEST)
        incident.incident_details=incident_details
        incident.priority=priority
        incident.incident_status=incident_status
        incident.save()
        serializer=IncidentSerializerput(incident)    
        return Response({'message':'Updated successfully','updated_data':serializer.data},status=status.HTTP_200_OK)



                

###------------------------search api------------------------------###



class SearchIncidentAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BearerAuthentication]

    def get(self, request):
        incident_id = request.data.get('incident_id')

        if not incident_id:
            return Response({'message': 'Incident ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract the middle 5 digits from the incident ID
        middle_digits = incident_id[3:8]

        # Get the current year
        current_year = str(timezone.now().year)

        incidents = Incident.objects.filter(
            incident_id__contains=middle_digits,
            incident_id__startswith='RMG',
            incident_id__endswith=current_year,
            reporter=request.user
            )

        if incidents.exists():
            serializer = IncidentSerializer(incidents, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Incident not found.'}, status=status.HTTP_404_NOT_FOUND)
