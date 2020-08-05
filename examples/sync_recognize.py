from voicegain_api import ApiClient
from voicegain_api import Configuration
from voicegain_api import RecognizeApi
import base64


# configure your JWT token
JWT = "Your <JWT>"

configuration = Configuration()
configuration.access_token = JWT

api_client = ApiClient(configuration=configuration)
recognize_api = RecognizeApi(api_client)


# recognize local file

file_path = "data/4_8_1_6_9.wav"
grammar_path = "data/zip_code_simple_2.grxml"

print("Recognize {} using grammar {}".format(file_path, grammar_path))

with open(file_path, "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

with open(grammar_path, "rb") as f:
    grammar_base64 = base64.b64encode(f.read()).decode()

response = recognize_api.asr_recognize_post(
    sync_recognition_request={
        "audio": {
            "source": {
                "inline": {
                    "data": audio_base64
                }
            }
        },
        "settings": {
            "asr": {
                "grammars": [
                    {
                        "type": "GRXML",
                        "inline": {
                            "data": grammar_base64
                        }
                    }
                ]
            }
        }
    }
)

alternatives = response.result.alternatives
if alternatives:
    print("result: {}".format(alternatives[0].utterance))
else:
    print("no match")


# recognize file from url

file_url = "https://tracker.voicegain.ai/attachments/download/82/4_8_1_6_9.wav"
grammar_url = "https://tracker.voicegain.ai/attachments/download/300/zip_code_simple_2.grxml"

print("Recognize {} using grammar {}".format(file_url, grammar_url))
response = recognize_api.asr_recognize_post(
    sync_recognition_request={
        "audio": {
            "source": {
                "fromUrl": {
                    "url": file_url
                }
            }
        },
        "settings": {
            "asr": {
                "grammars": [
                    {
                        "type": "GRXML",
                        "fromUrl": {
                            "url": grammar_url
                        }
                    }
                ]
            }
        }
    }
)

alternatives = response.result.alternatives
if alternatives:
    print("result: {}".format(alternatives[0].utterance))
else:
    print("no match")
