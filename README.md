# Voicegain Speech-to-Text Python SDK

Python SDK for the [Voicegain](https://voicegain.github.io/) Speech-to-Text API.

## Installation

From [PyPI](https://pypi.org/project/voicegain-speech/) directly:

```
pip install voicegain-speech
```

## Examples

* sync_transcribe example:

configuration:

```python
from voicegain_speech import ApiClient
from voicegain_speech import Configuration
from voicegain_speech import TranscribeApi
import base64


# configure your JWT token
JWT = "Your <JWT>"

configuration = Configuration()
configuration.access_token = JWT

api_client = ApiClient(configuration=configuration)
```
transcribe local file:
```python
transcribe_api = TranscribeApi(api_client)
file_path = "Your local file path"

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

```

More examples can be found in [examples](examples/) folder.
