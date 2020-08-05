# Voicegain Speech-to-Text Python SDK

---
[Voicegain Home](https://voicegain.github.io/)

## Examples

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
transcribe_api = TranscribeApi(api_client)
```
transcribe local file:
```python
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
```
get result:
```python
alternatives = response.result.alternatives
if alternatives:
    local_result = alternatives[0].utterance
    print("result from file: ", local_result)

else:
    local_result = None
    print("no transcription")

```

More examples can be found in [examples](examples/) folder.