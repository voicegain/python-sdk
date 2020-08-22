# Voicegain Speech-to-Text Python SDK

Python SDK for the [Voicegain](https://www.voicegain.ai) [Speech-to-Text API](https://portal.voicegain.ai/api/v1/index.html). 

This API allows for large vocabulary speech-to-text transcription as well as grammar-based speech recognition. Both real-time and offline use cases are supported.

You can see the core Voicegain API documentation [here](https://portal.voicegain.ai/api/v1/index.html). 

The complete documentation for the API covered by this SDK is available [here](https://portal.voicegain.ai/api-documentation) - this link requires an account on the Voicegain portal - see below for how to sign up. 

## Requirements

In order to use this API you need account with Voicegain. You can create an account by signing up on [Voicegain Portal](https://portal.voicegain.ai/signup). No credit card required to sign up.

You can see pricing [here](https://www.voicegain.ai/pricing) - basically, it is 1 cent a minute for off-line and 1.25 cents a minute for real-time. There is a Free Tier of 600 minutes that renews each month.

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

More examples can be found in [examples](https://github.com/voicegain/python-sdk/tree/master/examples) folder on our [GitHub](https://github.com/voicegain/python-sdk)

---
Learn more about Voicegain Platform at [www.voicegain.ai](https://www.voicegain.ai)
