import boto3


def generate_audio_as_bytes(
    text: str, voice_id: str = "Camila", output_format: str = "mp3"
) -> bytes:
    """
    Generates audio from a text using Amazon Polly and returns it as bytes.
    """
    polly = boto3.client("polly")

    response = polly.synthesize_speech(
        Text=text, OutputFormat=output_format, VoiceId=voice_id
    )

    audio_bytes = response["AudioStream"].read()

    return audio_bytes
