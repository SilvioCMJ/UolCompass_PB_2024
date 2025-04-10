import boto3
import os

bot_id = os.getenv("BOT_ID")
alias_id = os.getenv("ALIAS_ID")

locale_id = os.getenv("LOCALE_ID")

lex_client = boto3.client("lexv2-runtime", region_name=os.getenv("REGION"))


def send_message_to_lex(text: str, session_id: str) -> str:
    try:
        response = lex_client.recognize_text(
            botId=bot_id,
            botAliasId=alias_id,
            localeId=locale_id,
            sessionId=session_id,
            text=text,
        )

        bot_message = "\n".join(
            msg.get("content", "").replace("#", "\n")
            for msg in response.get("messages", [])
            if msg.get("contentType") == "PlainText"
        ) or (
            "Desculpe, houve um problema interno. Estamos trabalhando para"
            "resolver. Por favor, tente novamente em instantes.\n"
            " Agradecemos pela compreensão."
        )

        return bot_message
    except Exception as e:
        print(f"Erro ao enviar mensagem para o Lex: {e}")
        return "Erro ao processar a mensagem", None
