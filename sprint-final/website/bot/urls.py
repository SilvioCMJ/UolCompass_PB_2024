from django.urls import path
from .views import ChatBotView


urlpatterns = [
    path("chatbot/", ChatBotView.as_view(), name="chatbot"),
]
