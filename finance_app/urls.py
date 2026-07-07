from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# All imports grouped together
from .views import (
    GoalViewSet, 
    ExpenseViewSet, 
    ChallengeViewSet, 
    AIAgentView, 
    RegisterView,
    ai_advisor_chat  # <--- Ensure this is imported
)

router = DefaultRouter()
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'challenges', ChallengeViewSet, basename='challenge')

urlpatterns = [
    # REST API Endpoints
    path('', include(router.urls)),
    
    # Existing AI Endpoint 
    path('ai-agent/', AIAgentView.as_view(), name='ai_agent'),
    
    # The Crucial Route for your frontend:
    path('api/ai-chat/', ai_advisor_chat, name='ai_advisor_chat'),
    
    # Authentication Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]