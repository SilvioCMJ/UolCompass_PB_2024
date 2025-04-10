import re
from django.http import JsonResponse
from django.views import View
from django.http import HttpRequest
from bot.lex import Chat
from utils.http import get_client_ip
from django.shortcuts import render
from app.aws.s3 import s3
from app.settings import S3_BUCKET_NAME


class ChatBotView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        """Handles GET requests to render the chatbot page."""
        return render(request, "chatbot.html")

    def post(self, request: HttpRequest, *args, **kwargs):
        """Handles POST requests to send a message or image to the chatbot."""

        message = request.POST.get("message", "").strip()
        image = request.FILES.get("image", None)
        session_id = get_client_ip(request=request)

        image_url = (
            s3.put_object(
                bucket=S3_BUCKET_NAME,
                body=image.read(),
                key=f"{session_id}-image.jpg",
                contentType=image.content_type,
            )
            if image
            else None
        )

        regex = r"(?<=\.com\/).+"

        if image_url:
            image_key = re.search(regex, image_url).group(0)

        chat_input = message or image_key
        response_data = Chat.post_message(
            message=chat_input,
            session_id=session_id,
        )

        response = JsonResponse(response_data)
        response.set_cookie("session_id", session_id)

        return response
