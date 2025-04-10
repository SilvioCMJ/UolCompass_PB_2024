import boto3
from contextlib import closing
from tempfile import gettempdir
import os


def synthesize_speech(text: str):
    """
    Transforma o texto recebido em um arquivo de áudio.

    Args:
        text (str): Texto para sintetizar.

    Returns:
        tempfile: Um arquivo temporário em bytes para manipulação, ou None caso ocorra algum erro.
    """

    polly = boto3.client("polly")
    try:
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Thiago", Engine="neural")
    except Exception as e:
        print(f"Error synthesizing speech: {e}")
        return None

    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "polly_speech.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
                return output
            except IOError as e:
                print(f"Error writing audio file: {e}")
                return None
    return None
