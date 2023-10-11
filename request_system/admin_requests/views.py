from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import AdminRequest, CustomUser
from .serializers import AdminRequestSerializer
# views.py
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer  # Define your serializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)

            if user is not None:
                # If authentication is successful, generate JWT tokens
                refresh = RefreshToken.for_user(user)

                # Determine the user's role
                user_role = user.role

                # Redirect the user based on their role
                if user_role == CustomUser.Student:
                    redirect_url = f'admin_requests/student/{user.id}/'  # Construct the URL
                elif user_role == CustomUser.Facilitator:
                    # For facilitators, construct the URL with their ID
                    redirect_url = f'admin_requests/facilitator/{user.id}/'
                elif user_role == CustomUser.Team_Lead:
                    redirect_url = 'admin_requests/team_lead/'  # Replace with your team lead view URL
                else:
                    # Handle other roles or invalid roles
                    redirect_url = '/'  # Redirect to a default page or handle as needed
                # Return the tokens, user data, and individual view URL
                response_data = {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'redirect_url': redirect_url,  # Include the URL here
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()  # This saves the user and the associated user profile
        
        # user = serializer.save()  # This saves the user and the associated user profile
        # token, created = Token.objects.get_or_create(user=user)
        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            
        }
        self.headers = self.default_response_headers  # set this for DRF to add `Location` header
        return Response({'user_data': user_data})
    
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from admin_requests.permissions import IsAdminUser  


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AdminRequestListCreateView(generics.ListCreateAPIView):
    queryset = AdminRequest.objects.all()
    serializer_class = AdminRequestSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
# @permission_classes([IsAuthenticated])
class AdminRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AdminRequest.objects.all()
    serializer_class = AdminRequestSerializer   

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentRequestsListView(generics.ListAPIView):
    serializer_class = AdminRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter requests where the sender is the current student
        return AdminRequest.objects.filter(sender=self.request.user)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])    
class StudentRepliesListView(generics.ListAPIView):
    serializer_class = AdminRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter requests where the recipient is the current student and there's a reply
        return AdminRequest.objects.filter(recipient=self.request.user, reply__isnull=False)
    

from django.shortcuts import render
def home(request):
    data = AdminRequest.objects.all()
    return render(request, 'home.html', {'data': data})


# # views.py
# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import CustomUser

# class StudentDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, student_id):
#         # Check if the current user is a student and matches the specified student_id
#         user = request.user
#         if user.role == CustomUser.Student and user.id == student_id:
#             # Retrieve the student's details based on the student_id
#             student = get_object_or_404(CustomUser, id=student_id)

#             # Render the student's details or return them in the response
#             response_data = {
#                 'student_id': student.id,
#                 'username': student.username,
#                 # Add other student details as needed
#             }
#             return Response(response_data)
#         else:
#             # Redirect or handle unauthorized access
#             return Response({'detail': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
