from voicegain_speech import ApiClient
from voicegain_speech import Configuration
from voicegain_speech import TranscribeApi
import time

# configure your JWT token
JWT = "Your <JWT>"

configuration = Configuration()
configuration.access_token = JWT

api_client = ApiClient(configuration=configuration)
transcribe_api = TranscribeApi(api_client)


# transcribe file from url

file_url = "https://tracker.voicegain.ai/attachments/download/241/The_Princess_and_the_Pea.wav"


async_transcription_request = {
    "sessions": [
        {
            "asyncMode": "OFF-LINE",
            "poll": {
                "afterlife": 60000,
                "persist": 0
            }
        }
    ],
    "audio": {
        "source": {
            "fromUrl": {
                "url": file_url
            }
        }
    }
}

async_transcribe_init_response = transcribe_api.asr_transcribe_async_post(
    async_transcription_request=async_transcription_request
)

async_response_session = async_transcribe_init_response.sessions[0]
session_id = async_response_session.session_id
print("session id", session_id)

while True:
    time.sleep(1)
    poll_response = transcribe_api.asr_transcribe_async_get(
        session_id=session_id,
        full=True
    )
    poll_response_result = poll_response.result

    if poll_response_result.final:
        # get to final
        result_transcript = poll_response_result.transcript
        print("final transcription: " + result_transcript)
        break

    else:
        print("processing...")
