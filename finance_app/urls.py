from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import GoalViewSet, ExpenseViewSet, ChallengeViewSet, AIAgentView, RegisterView

router = DefaultRouter()
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'challenges', ChallengeViewSet, basename='challenge')

urlpatterns = [
    # API Endpoints
    path('', include(router.urls)),
    
    # AI Endpoint
    path('ai-agent/', AIAgentView.as_view(), name='ai_agent'),
    
    # Authentication Endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]