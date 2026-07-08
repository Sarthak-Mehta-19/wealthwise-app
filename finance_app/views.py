import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

# Import the Google GenAI SDK and types for configuration
from google import genai
from google.genai import types

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
            # Using the new Google GenAI format and settings import
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            
            return Response({"advice": response.text})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

@csrf_exempt # Note: Ensure proper Supabase JWT validation in production
def ai_advisor_chat(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_id = body.get('user_id')
            user_message = body.get('message')

            if not user_id or not user_message:
                return JsonResponse({"error": "Missing user_id or message"}, status=400)

            # 1. Fetch User Data from PostgreSQL
            # Replaced 'description' with actual DB columns 'title' and 'notes'
            expenses = list(Expense.objects.filter(user_id=user_id).order_by('-date')[:100].values('amount', 'category', 'date', 'title', 'notes'))
            goals = list(Goal.objects.filter(user_id=user_id).values('name', 'target_amount', 'current_amount', 'deadline'))

            financial_context = {
                "recent_expenses": expenses,
                "active_goals": goals
            }

            # 2. Construct the Strict System Prompt
            system_prompt = f"""
            You are a personal financial analyst for this user. Your goal is extreme clarity.
            Do not provide generic stock market advice or complicated investment strategies.
            Answer the user's question based SOLELY on the following data:
            {json.dumps(financial_context, default=str)}
            
            Keep your response concise, actionable, and focused on helping them optimize their tracked spending to hit their specific goals.
            """

            # 3. Call the Gemini API via the official google-genai client
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=user_message,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3
                )
            )

            return JsonResponse({"response": response.text})

        except Exception as e:
            print(f"Backend AI API Error: {e}")
            return JsonResponse({"error": "Failed to generate AI insights."}, status=500)
            
    return JsonResponse({"error": "Invalid request method"}, status=405)