import os
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from google import genai

from django.contrib.auth import get_user_model
from .models import Goal, Expense, Challenge
from .serializers import UserSerializer, GoalSerializer, ExpenseSerializer, ChallengeSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = [IsAuthenticated]

class AIAgentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt', 'Give me financial advice based on my goals.')
        
        try:
            # Using the new 2026 Google GenAI format
            client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
            
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
            )
            
            return Response({"advice": response.text})
        except Exception as e:
            return Response({"error": str(e)}, status=500)