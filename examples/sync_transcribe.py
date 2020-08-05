from voicegain_speech import ApiClient
from voicegain_speech import Configuration
from voicegain_speech import TranscribeApi
import base64


# configure your JWT token
JWT = "Your <JWT>"

configuration = Configuration()
configuration.access_token = JWT

api_client = ApiClient(configuration=configuration)
transcribe_api = TranscribeApi(api_client)

# transcribe local file

file_path = "data/4_8_1_6_9.wav"

with open(file_path, "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

response = transcribe_api.asr_transcribe_post(
    sync_transcription_request={
        "audio": {
            "source": {
                "inline": {
                    "data": audio_base64
                }
            }
        }
    }
)

alternatives = response.result.alternatives
if alternatives:
    local_result = alternatives[0].utterance
    print("result from file: ", local_result)

else:
    local_result = None
    print("no transcription")


# transcribe file from url

file_url = "https://tracker.voicegain.ai/attachments/download/82/4_8_1_6_9.wav"

response = transcribe_api.asr_transcribe_post(
    sync_transcription_request={
        "audio": {
            "source": {
                "fromUrl": {
                    "url": file_url
                }
            }
        }
    }
)

alternatives = response.result.alternatives
if alternatives:
    url_result = alternatives[0].utterance
    print("result from url: ", local_result)

else:
    url_result = None
    print("no transcription")
