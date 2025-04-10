from services.lex import send_message_to_lex
from services.s3 import upload_file_to_s3
from utils.decode import decode_body
from utils.content_type import get_content_type
from utils.download_media import download_media_file
from utils.get_twilio_phone import get_twilio_phone_number


def twilio(event, context):
    print(event)

    params = decode_body(event)

    from_number = get_twilio_phone_number(params)
    print(f"Número de origem: {from_number}")

    content_type = get_content_type(params)
    response_message = None

    if content_type in ["image", "audio"]:
        media_url = params.get("MediaUrl0")
        print(f"URL da mídia ({content_type}):", media_url)

        try:
            media_content = download_media_file(media_url)
            media_key = upload_file_to_s3(media_content, content_type)
            print(f"Media stored in S3 at: {media_key}")
            response_message = send_message_to_lex(media_key, from_number)
        except Exception as e:
            print(f"Error processing media: {e}")
            response_message = (
                "Houve um problema ao processar seu arquivo."
                " Por favor, tente novamente."
            )

    else:
        text_to_translate = params.get("Body", "")
        response_message = send_message_to_lex(text_to_translate, from_number)
        print(response_message)

    return {"statusCode": 200, "body": response_message}
