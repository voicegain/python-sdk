# coding: utf-8

"""
    Voicegain API v1

    # New  [Telephony Bot API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + Telephony Bot APIs which in addition to speech-to-text allow for control of real-time communications (RTC) session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Web Console](https://console.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  When making Web APi request the JWT has to be included in the \"Authorization: Bearer\" header. For example, when using curl to make a request:  <pre>   curl -i -X POST \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Authorization: Bearer eyJh......BOGCO70w\" \\   -d @data1.json \\   https://api.voicegain.ai/v1/asr/transcribe/async </pre>  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).  # Edge Deployment API URLs  When you are using Voicegain plaform deployed on Edge, the Web API urls will be different from those that are used in the Cloud (and given in the examples).  For example: * a Web API URL in the Cloud may be: https://api.voicegain.ai/v1/asr/transcribe/async  * but when deployed on Edge which e.g. has this IP:port 10.137.16.7:31680 and does not have SSL configured   * the URL for the same API will be http://10.137.16.7:31680/ascalon-web-api/asr/transcribe/async  * if deployed on Edge with SSL cert and IP:port 10.137.16.7:31443   * the URL for the same API will be https://10.137.16.7:31443/ascalon-web-api/asr/transcribe/async  The reason for this is that in the Cloud, the Web API service is on its own hostname, but on the Edge it has to share the hostname/IP with the Web Console  (which would e.g. have this URL: https://10.137.16.7:31443/customer-portal/)  # Context Defaults  Most of the API requests are made within a specific Context identified by the JWT being used. Each Context has some API (mainly ASR API) related settings which can be set from the Web Console, see image below: ![Context Settings](https://github.com/voicegain/platform/raw/master/images/Context-Speech-Recognition-Settings.PNG)  These settings override the corresponding API default values.  For example, if `noInputTimeout` default is 15000, but the Context 'No Input Timeout' setting is 30000,  and no value is provided in the API request for `noInputTimeout` field, then the API request will run with `noInputTimeout` of 30000.    # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Specifically, 2x OFF-LINE use case is not supported because of how the task queue processor is implemented. To transcribe 2-channels separately in OFF-LINE mode you will need to make 2 separate OFF-LINE transcription requests. Please, let us know if you think you have a valid use case for other combinations.  # Telephony Bot API  (previously called RTC Callback API, where RTC stands for Real Time Communications)   Voicegain Telephony Bot APIs allows you to build conversational voice-enabled applications (e.g. IVRs, Voicebots) over an RTC session (a telephone call for example).  See this blog post for an overview of how this API works: [Voicegain releases Telephony Bot APIs for telephony IVRs and bots](https://www.voicegain.ai/post/rtc-callback-api-released)  Telephony Bot API is a callback API - Voicegain platform makes HTTP request to your app with information about the result of e.g. latest recognition and in response you provide instruction for the next step of the conversation. See the spec of these requests [here](#tag/aivr-callback).  # Speech Analytics API  Voicegain Speech Analytics analyzes both the transcript and the audio (typically of a telephone call).  The results are returned per channel (real or diarized) except where the recognized entities span more than one channel. For entities where it is applicable we return the location in the audio (start and end time) and the transcript (index of the words).  ## Capabilities of Speech Analytics  Voicegain Speech Analytics can identify/compute the following: + **named entities** - (NER i.e. named entity recognition) - the following entities are recognized:   + ADDRESS - Postal address.   + CARDINAL - Numerals that do not fall under another type.   + CC - Credit Card   + DATE - Absolute or relative dates or periods.   + DMY - Full date including all of day, month and year.         + EMAIL - Email address   + EVENT - Named hurricanes, battles, wars, sports events, etc.   + FAC - Buildings, airports, highways, bridges, etc.   + GPE - Countries, cities, states.   + LANGUAGE - Any named language.   + LAW - Named documents made into laws.   + NORP - Nationalities or religious or political groups.   + MONEY - Monetary values, including unit.   + ORDINAL - \"first\", \"second\", etc.   + ORG - Companies, agencies, institutions, etc.   + PERCENT - Percentage, including \"%\".   + PERSON - People, including fictional.   + PHONE - Phone number.   + PRODUCT - Objects, vehicles, foods, etc. (Not services.)   + QUANTITY - Measurements, as of weight or distance.   + SSN - Social Security number   + TIME - Times smaller than a day.   + WORK_OF_ART - Titles of books, songs, etc.   + ZIP - Zip Code (if not part of an Address)    In addition to returning the named entity itself, we return the sub-concepts within entity, e.g. for ADDRESs we will return state (e.g. TX) and zip code if found.  + **keywords** - these are single words or short phrases e.g. company or product names.    Currently, keywords are detected using simple matching using stemming - so e.g. a keyword \"cancel\" will match \"cancellation\".    In near future we will support \"smart expansion\" which will also match synonyms while paying attention to the correct meaning of the word.     In addition to keywords we return keyword groups, e.g. several company name keywords can be combined into a `Competition` keyword group.  + **phrases (intent)** - allows for detection of phrases/intents that match the meaning of the phrases specified in the example training Sections).</br>   For each detected phrase/intent the system will also return entities and keywords contained in the phrase, if configured to do so.   For example, transcript \"Hello, my name is Lucy\" may match phrase/intent \"INTRODUCTION\" with the NER of PERSON and value \"Lucy\".       The configuration for phrase/intent detection takes the following parameters:   + _list_ of example phrases - each phrase has a sensitivity value which determines how close it has to match (sensitivity of 1.0 requires the closest match, sensitivity of 0.0 allows for vague matches).   + _regex_ - optional regex phrases to augment the examples - these require exact match   + _slots_ - types on named entities and keywords to be recognized within the phrase/intent</br>     Note: support for slots of same type but different meaning will be added in the future.     Currently it is possible e.g. to recognize places (GPE) but not possible to distinguish e.g. between types of them, like departure or destination place.   + _location_ - this narrows down where the phrase/match must occur - the options are:     + channel - agent or caller      + time in the call - from the start or from the end     + dialogue act - require the phrase to be part of a specified dialogue act, see https://web.stanford.edu/~jurafsky/ws97/manual.august1.html, first table, column SWBD    + **phrase groups** - computed across all channels - this is more powerful than keyword groups as it can be configured to require all phrases/intents in the groups to be present in any or fixed order.   One use case would be to detect a pair of a question and a confirming answer - for example to determine call resolution: \"Have I answered all your question?\", \"Yes\". + **criteria** - computed by rules/conditions looking at the following parameters:   + _call metrics_   + _regex_ - match of the text of the transcript   + _keywords_ - any keywords or keyword groups   + _NER_ - any named entities   + _phrases_ - any phrases/intents or phrase groups   + _dialogElements_ - selection of custom hardcoded rules that may accomplish tasks not possible with other conditions    The individual rules/conditions can be further narrowed down using filters like:   + _channel_ - agent or caller    + _time in the call_ - from the start or from the end    Multiple rules can be combined to form a logical AND expression.   Finally, the individual rules can be negated so that the absence of certain events is considered as a positive match.    When Criteria are satisfied then the system provides a detailed justification information. + **topics** - computed from text across all channels - assigns to the call a set of likely topics with their scores.    A topic classifier is built in a separate step using a corpus. The build process requires manual labeling of the topics.    For each call, the entire transcript is fed to the topic classifier and we get back the set of detected topics and their scores (in the 0..1 range).   It is useful e.g. for separating Billing calls from Troubleshooting calls from Account Change calls, etc.  + **summary** - computed from text across all channels - provides a summary of the call in a form of a set of sentences.   These may either be key sentences directly pulled from the transcript, or sentences generated by summarizing entire call or sections of the call.  + **sentiment** - computed from text - standard call sentiment as used in Call Center Speech Analytics.   Returns sentiment values from -1.0 (negative/mad/angry) to +1.0 (positive/happy/satisfied) + **mood** - computed from text - can distinguish 6 moods:   + neutral    + anger    + disgust    + fear    + happiness   + sadness   + surprise     Values are returned as a map from mood enum values to a number in (0.0, 1.0) range - multiple moods can be detected in the same place in the transcript in varying degrees. + **gender** - computed to audio - Estimates the gender of the speaker as far as it is possible to do it from the voice alone. + **word cloud** - returns word cloud data (map from words/phrases to frequencies) - the algorithm uses: stop word removal, stemming, frequent phrase detection. + **call metrics** - these are simple metrics computed from the audio and the transcript    + _silence_ - amount of silence in the call   + _talk_ - talk streaks for each of the channels   + _overtalk_ - amount of time when call participants talk over ove another   + _energy_ - the volume of the call and the variation   + _pitch_ - the pitch (frequency of the voice) and the variation  Voicegain allows for configuring Speech Analytics processing by preparing a Speech Analytics Configuration which is basically a selection of the capabilities mentioned above plus configuration of variable elements like keywords, phrases, etc.  </br> You can configure Speech Analytics using **[/sa/config API](#operation/saConfigPost)**   Once the configuration is complete you can launch speech transcription and analytics session using the **[/sa API](#operation/saPost)**   ## Offline vs Real-Time Speech Analytics  Speech audio can be transcribed and then analyzed in one of two modes: + **OFF-LINE** - use the `/sa/offline/` API for this.    Audio will be queued for transcription, then transcribed, and both the audio and transcript will pass through various speech analytics algorithms according to the specified configuration.   The results of transcription and speech analytics can be retrieved using the [GET **/sa/offline/{sid}/data** API](#tag/sa-offline/operation/saOfflineGetData)   + **REAL-TIME** - use the `/sa` API for this.    Audio will immediately be submitted to real-time transcription and the stream of transcribed words will be fed to real-time speech analytics.    The results of transcription and speech analytics will be returned over websocket as soon as they are available. </br>   The format of the returned messages is defined [here](#operation/saWebsocketPayload).    Note that not all speech analytics features are available in real-time. Features missing in real-time are: criteria, topics, summary, gender, word cloud, and call metrics.</br>   The results will also be available afterwards using the [GET **/sa/{sid}/data** API](#operation/saDataGet)  ## Agent Review Form  Data computed by Speech Analytics can be used to automatically fill/answer questions of the Call/Agent Review Form.   The automatic answers can be obtained based on previously defined Criteria (see above).  When Criteria are satisfied then the system provides a detailed justification information so it is easily possible to verify that the automated answer on a Review Form was correct.  ## PII Redaction  Being able to recognize occurrence of certain elements in the transcript allows us to remove them from both the text and the audio - this is called PII Redaction where PII stands for Personally Identifiable Information.  Currently, PII Redaction is limited to named entities (NER).  User can select any NER type detected by [Speech Analytics](#section/Speech-Analytics-API/Capabilities-of-Speech-Analytics) to be replaced by a specified placeholder in the text and by silence in the audio.  If your Enterprise account with Voicegain is setup with PCI-DSS compliance option, then PII Redaction of credit card numbers is enabled by default and cannot be disabled.    # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  The supported audio formats are described here: [Supported Audio Formats](https://support.voicegain.ai/hc/en-us/articles/360050477331-Supported-Audio-Formats). Offline transcription supports a very wide set of audio formats, while real-time transcription is limited to a smaller set of formats.  # Rate Limiting  Access to Voicegain resources is controlled using the following limit settings on the account.  Newly created accounts get the limit values listed below.  If you need higher limits please contact us at support@voicegain.ai  The limits apply to the use of the Voicegain Platform in the Cloud.  On the Edge, the limits will be determined by the type of license you will purchase.  ## Types of Rate Limits  | Limit | default value | description | |---|---|---| | apiRequestLimitPerMinute | 75 | Basic rate limit with a fixed window of 1 minute applying to all API requests. Requests to /data API will be counted at 10x other requests. | | apiRequestLimitPerHour | 2000 | Basic rate limit with a fixed window of 1 hour applying to all API requests. Requests to /data API will be counted at 10x other requests. | | asrConcurrencyLimit | 4 | Limit on number of concurrent ASR requests. Does not apply to OFF-LINE requests. | | offlineQueueSizeLimit | 10 | Maximum number of OFF-LINE transcription jobs that may be submitted to the queue. | | offlineThroughputLimitPerHour | 4 | Maximum number of hours of audio that can be processed by OFF-LINE transcription within 1 hour. Note: For Edge deployment the limit interval is per day instead of per hour. | | offlineWorkerLimit | 2 | Maximum number of OFF-LINE transcription job workers that will be used to process the account audio. |  For API requests running longer that the rate limit window length, the request count will be applied to both the window when the request started and the window when the request finished.   Every HTTP API request will return several rate-limit related headers in its response.  The header values show the applicable limit, the remaining request count in the current window, and the number of seconds to when the limit resets. For example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 1 RateLimit-Reset: 7 ```  ## When Rate Limits are Hit  If a rate-limit is hit then [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) HTTP error code will be returned. The response headers will additionally include Retry-After value, for example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 0 RateLimit-Reset: 6 Retry-After: 6 ``` If `asrConcurrencyLimit` is hit then the response headers will contain:  ``` X-ResourceLimit-Type: ASR-Concurrency X-ResourceLimit-Limit: 4 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ``` Note that we return a superset of values that are returned for a basic API request limit.  This will allow a client code that was written to handle basic rate limiting to be able to handle concurrency limiting too.  Note also that for the concurrency limit the Retry-After value is approximate and is not guaranteed - so client code may have to retry multiple times. (We will return increasing back-off Retry-After values in case of the limit being hit multiple times.)   In case of `offlineQueueSizeLimit` limit we will return, for example:  ``` X-ResourceLimit-Type: Offline-Queue-Size X-ResourceLimit-Limit: 10 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ```   # Pagination  Voicegain API supports 2 methods of pagination.  ## Sequential pagination  For methods that support sequential pagination Voicegain has standardized on using the following query parameters: + start_after={object id OR nul}  + end_before={object id OR nul}  + per_page={number items per page}  If `start_after=nul` then the first page will be retrieved.</br> If `end_before=nul` then the last page will be retrieved.  `start_after` and `end_before` should not be used together.  If neither `start_after` nor `end_before` are provided, then `start_after=nul` will be assumed.  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?start_after=nul&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?end_before=5f7f1f7d67f67ddaa622b68e&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?start_after=5f7f1f7d67f67ddaa622b68d&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?start_after=5f7f1f7d67f67ddaa622b68c4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?end_before=nul&per_page=50>; rel=\"last\" ```  ## Direct pagination  For methods that support direct pagination Voicegain has standardized on using the following query parameters: + page={page number}  + per_page={number items per page}  `page` is the page number starting from 1 (i.e. first page is 1). This is not an item offset.  This also implies that `per_page` should be kept constant for a set of related requests.  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 786 Link: <https://api.voicegain.ai/v1/sa/call?pager=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=7&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=8&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=16&per_page=50>; rel=\"last\" ```   # PCI-DSS Compliance (Cloud)  The PCI-DSS compliant endpoint on the Voicegain Cloud is https://sapi.voicegain.ai/v1/ </br> Do not submit requests that may contain CHD data to the standard endpoint at https://api.voicegain.ai/v1/  Here is a list of all API Methods that are PCI-DSS compliant: + `/asr/transcribe`: [POST](#operation/asrTranscribePost) + `/asr/transcribe/async`: [POST](#operation/asrTranscribeAsyncPost) - we support OFF-LINE and REAL-TIME + `/asr/transcribe/{sessionId}`: [GET](#operation/asrTranscribeAsyncGet) [PUT](#operation/asrTranscribeAsyncPut) [DELETE](#operation/asrTranscribeAsyncDelete)  Note that the /data API is not yet PCI-DSS compliant on the Cloud. This means that the only PCI-DSS compliant ways to submit the audio are: + `fromUrl` - use `authConf` for authenticated access or use signed short-lived URLs + `inline` + `stream` - only `WSS` (old `WEBSOCKET`) and `TWIML` protocols are supported right now  https://sapi.voicegain.ai/v1/ endpoint does not support API methods that would store data, either the audio or the transcription results.   https://sapi.voicegain.ai/v1/ endpoint does support audio redaction. Redacted audio is not stored but submitted directly to the URL specified in the request `audio.callback`.   # PCI-DSS Compliance (Edge)  Because the Edge deployment happens ultimately in the customer's environment, it will the customer's responsibility to certify their Edge depoyment of the Voicegain platform as PCI-DSS compliant.  Voicegain can provide Attestation of Compliance (AoC) for the following PCI-DSS sections as far as they releate to Voicegain Software that will be deployed on Edge: + 5. Use and regularly update anti-virus software or programs + 6. Develop and maintain secure systems and applications + 11. Regularly test security systems and processes + 12. Maintain a policy that addresses information security for all personnel  For the following PCI-DSS sections we will provide detailed data regarding implementation: + 3. Protect stored cardholder data   # noqa: E501

    The version of the OpenAPI document: 1.122.0 - updated July 24, 2025
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from voicegain_speech.api_client import ApiClient
from voicegain_speech.exceptions import (
    ApiTypeError,
    ApiValueError
)


class SaOfflineApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def sa_offline_call_post(self, call_id, **kwargs):  # noqa: E501
        """Speech Analytics of a Call  # noqa: E501

        Start offline transcription and speech analytics of provided call.</br> (See [POST /sa/call](#tag/sa-internal/operation/saCallPost) for how a call is created.)  At the end of processing some of the SA session results will be stored in the call for fast access.  Input audio can be mono or stereo.</br> If input is stereo then Left channel is assumed to be the external participant and Right the internal.</br> If input audio is mono then automatic diarization will be performed.  Virtual-stereo audio file will be created.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_call_post(call_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str call_id: Voice Call Id. (required)
        :param OfflineSpeechAnalyticsBaseRequestWithoutSpeakers offline_speech_analytics_base_request_without_speakers: Body of the offline speech analytics request
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: OfflineSpeechAnalyticsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_call_post_with_http_info(call_id, **kwargs)  # noqa: E501

    def sa_offline_call_post_with_http_info(self, call_id, **kwargs):  # noqa: E501
        """Speech Analytics of a Call  # noqa: E501

        Start offline transcription and speech analytics of provided call.</br> (See [POST /sa/call](#tag/sa-internal/operation/saCallPost) for how a call is created.)  At the end of processing some of the SA session results will be stored in the call for fast access.  Input audio can be mono or stereo.</br> If input is stereo then Left channel is assumed to be the external participant and Right the internal.</br> If input audio is mono then automatic diarization will be performed.  Virtual-stereo audio file will be created.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_call_post_with_http_info(call_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str call_id: Voice Call Id. (required)
        :param OfflineSpeechAnalyticsBaseRequestWithoutSpeakers offline_speech_analytics_base_request_without_speakers: Body of the offline speech analytics request
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(OfflineSpeechAnalyticsResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['call_id', 'offline_speech_analytics_base_request_without_speakers']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_call_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'call_id' is set
        if self.api_client.client_side_validation and ('call_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['call_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `call_id` when calling `sa_offline_call_post`")  # noqa: E501

        if self.api_client.client_side_validation and ('call_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['call_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `call_id` when calling `sa_offline_call_post`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('call_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['call_id']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `call_id` when calling `sa_offline_call_post`, length must be greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'call_id' in local_var_params:
            path_params['callId'] = local_var_params['call_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'offline_speech_analytics_base_request_without_speakers' in local_var_params:
            body_params = local_var_params['offline_speech_analytics_base_request_without_speakers']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline/call/{callId}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OfflineSpeechAnalyticsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_delete(self, sa_session_id, **kwargs):  # noqa: E501
        """Delete SA Session  # noqa: E501

        Delete all data for offline Speech Analytics Session   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_delete(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_delete_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_offline_delete_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """Delete SA Session  # noqa: E501

        Delete all data for offline Speech Analytics Session   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_delete_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(object, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_offline_delete`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_delete`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_delete`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline/{saSessionId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_get(self, sa_session_id, **kwargs):  # noqa: E501
        """Get SA Session  # noqa: E501

        Get Offline Speech Analytics Session. This is the method that should be used to **poll** an /sa/offline session to see its `progress.phase` </br> Note: until the session is in `progress.phase` of `DONE`, the session data will not be complete. </br> The following fields will be missing: `numIncidents`, `shortSummary`, `topExtendedSummary`, `topKeywords`, `speakers`, `objectFileName`.</br>   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_get(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: OfflineSpeechAnalyticsCoreResultResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_get_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_offline_get_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """Get SA Session  # noqa: E501

        Get Offline Speech Analytics Session. This is the method that should be used to **poll** an /sa/offline session to see its `progress.phase` </br> Note: until the session is in `progress.phase` of `DONE`, the session data will not be complete. </br> The following fields will be missing: `numIncidents`, `shortSummary`, `topExtendedSummary`, `topKeywords`, `speakers`, `objectFileName`.</br>   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_get_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(OfflineSpeechAnalyticsCoreResultResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_offline_get`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_get`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_get`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline/{saSessionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OfflineSpeechAnalyticsCoreResultResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_get_data(self, sa_session_id, **kwargs):  # noqa: E501
        """Speech Analytics Data  # noqa: E501

        Retrieve speech analitics data (**after** transcription and ML steps are **complete**).</br> Data may include:</br> - transcript itself - in the `words` field,</br> - speech analytics results.</br>  Note: Do not use this method to merely poll an /sa/offline session for its status (`progress.phase`), use the [GET /sa/offline/{saSessionId}](#tag/sa-offline/operation/saOfflineGet) instead for polling.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_get_data(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param bool words: If transcript words (with timing and confidences) should be included.
        :param bool audio: If `true` then original and combined audio will be returned.
        :param bool meta: If `true` then metadata for the transcript session will be returned
        :param bool word_cloud: If `true` then word cloud data for the transcript will be returned
        :param bool summary: If `true` then summary data for the transcript will be returned
        :param bool keywords: If `true` then keywords spotted in the text will be returned
        :param bool entities: If `true` then named entities spotted in the text will be returned
        :param bool phrases: If `true` then phrases spotted in the text will be returned
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: OfflineSpeechAnalyticsResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_get_data_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_offline_get_data_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """Speech Analytics Data  # noqa: E501

        Retrieve speech analitics data (**after** transcription and ML steps are **complete**).</br> Data may include:</br> - transcript itself - in the `words` field,</br> - speech analytics results.</br>  Note: Do not use this method to merely poll an /sa/offline session for its status (`progress.phase`), use the [GET /sa/offline/{saSessionId}](#tag/sa-offline/operation/saOfflineGet) instead for polling.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_get_data_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param bool words: If transcript words (with timing and confidences) should be included.
        :param bool audio: If `true` then original and combined audio will be returned.
        :param bool meta: If `true` then metadata for the transcript session will be returned
        :param bool word_cloud: If `true` then word cloud data for the transcript will be returned
        :param bool summary: If `true` then summary data for the transcript will be returned
        :param bool keywords: If `true` then keywords spotted in the text will be returned
        :param bool entities: If `true` then named entities spotted in the text will be returned
        :param bool phrases: If `true` then phrases spotted in the text will be returned
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(OfflineSpeechAnalyticsResult, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id', 'words', 'audio', 'meta', 'word_cloud', 'summary', 'keywords', 'entities', 'phrases']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_get_data" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_offline_get_data`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_get_data`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_get_data`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []
        if 'words' in local_var_params and local_var_params['words'] is not None:  # noqa: E501
            query_params.append(('words', local_var_params['words']))  # noqa: E501
        if 'audio' in local_var_params and local_var_params['audio'] is not None:  # noqa: E501
            query_params.append(('audio', local_var_params['audio']))  # noqa: E501
        if 'meta' in local_var_params and local_var_params['meta'] is not None:  # noqa: E501
            query_params.append(('meta', local_var_params['meta']))  # noqa: E501
        if 'word_cloud' in local_var_params and local_var_params['word_cloud'] is not None:  # noqa: E501
            query_params.append(('wordCloud', local_var_params['word_cloud']))  # noqa: E501
        if 'summary' in local_var_params and local_var_params['summary'] is not None:  # noqa: E501
            query_params.append(('summary', local_var_params['summary']))  # noqa: E501
        if 'keywords' in local_var_params and local_var_params['keywords'] is not None:  # noqa: E501
            query_params.append(('keywords', local_var_params['keywords']))  # noqa: E501
        if 'entities' in local_var_params and local_var_params['entities'] is not None:  # noqa: E501
            query_params.append(('entities', local_var_params['entities']))  # noqa: E501
        if 'phrases' in local_var_params and local_var_params['phrases'] is not None:  # noqa: E501
            query_params.append(('phrases', local_var_params['phrases']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline/{saSessionId}/data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OfflineSpeechAnalyticsResult',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_post(self, **kwargs):  # noqa: E501
        """Offline Speech Analytics  # noqa: E501

        Start offline transcription and speech analytics of provided audio.  Example of the **speakers** and **audio** fields for the typical use case with stereo audio and Agent in the left channel and Customer in the right channel.  Note 1: **speaker.id** values must be integers, but any integer is allowed, e.g. it could match some externnal speaker id. Agent and Customer speaker ids need to be different.</br> ```json {   \"optimizeForWebUi\": \"level1\",   \"speakers\": [     {       \"id\": <a number representing agent id>,       \"name\": \"Agent\",       \"is_agent\": true     },     {       \"id\": <a number representing customer id>,       \"name\": \"Customer\",       \"is_agent\": false     }   ],   \"audio\": [     {       \"source\": {         \"dataObjectUuid\" : \"<Data Object UUID>\",\"       },       \"audioChannelSelector\" : \"left\",       \"mergedStereoChannel\" : \"left\",       \"vadMode\" : \"total_music_reject\"       \"speakers\": [         <id of the Agent speaker, see above>,       ]     },     {       \"source\": {         \"dataObjectUuid\" : \"<Data Object UUID - same as above - single audio input is used>\",\"       },       \"audioChannelSelector\" : \"right\",       \"mergedStereoChannel\" : \"right\",       \"speakers\": [         <id of the Customer speaker, see above>,       ]     },   ] } ```  About **Agent detection**:</br> It's on when + language is English + AND there are two channels, either from two audio source or from diarization + AND is_agent boolean is not specified on any audio source          Note about **output audio**:</br> The output of processing will contain mergedAudio if `optimizeForWebUi` is set to at least `level1`.</br> In certain cases mergedAudioId will be a virtual DualChannel (virtual stereo): + if no diarization   + if 2 input audio were provided then 1st will be in the left channel (after audio selector is applied) and 2nd will be in the right channel (after audio selector is applied) of the merged audio   + if more than 3 input audio was provided, then all audio with speakers marked as Agent will go to left channel, and remaining audio will got to the right channel + with diarization   + if 1 input audio was provided, and diarizaton was into 2 speakers, then 1st speaker will be in the left channel and 2nd speaker will be in the right channel + with voice signatures (with or w/o diarization)   + all audio from recognized speakers marked as Agent will go to left channel and remaining speakers will got to the right channel  About **PII Redaction**:</br> `saConfig` had `piiRedaction` parameter that can be used to configure the PII redaction.</br> The redaction will be aplied to the output transcript and audio. (It is not applied to the source audio.)   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param OfflineSpeechAnalyticsRequest offline_speech_analytics_request: Body of the offline speech analytics request
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: OfflineSpeechAnalyticsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_post_with_http_info(**kwargs)  # noqa: E501

    def sa_offline_post_with_http_info(self, **kwargs):  # noqa: E501
        """Offline Speech Analytics  # noqa: E501

        Start offline transcription and speech analytics of provided audio.  Example of the **speakers** and **audio** fields for the typical use case with stereo audio and Agent in the left channel and Customer in the right channel.  Note 1: **speaker.id** values must be integers, but any integer is allowed, e.g. it could match some externnal speaker id. Agent and Customer speaker ids need to be different.</br> ```json {   \"optimizeForWebUi\": \"level1\",   \"speakers\": [     {       \"id\": <a number representing agent id>,       \"name\": \"Agent\",       \"is_agent\": true     },     {       \"id\": <a number representing customer id>,       \"name\": \"Customer\",       \"is_agent\": false     }   ],   \"audio\": [     {       \"source\": {         \"dataObjectUuid\" : \"<Data Object UUID>\",\"       },       \"audioChannelSelector\" : \"left\",       \"mergedStereoChannel\" : \"left\",       \"vadMode\" : \"total_music_reject\"       \"speakers\": [         <id of the Agent speaker, see above>,       ]     },     {       \"source\": {         \"dataObjectUuid\" : \"<Data Object UUID - same as above - single audio input is used>\",\"       },       \"audioChannelSelector\" : \"right\",       \"mergedStereoChannel\" : \"right\",       \"speakers\": [         <id of the Customer speaker, see above>,       ]     },   ] } ```  About **Agent detection**:</br> It's on when + language is English + AND there are two channels, either from two audio source or from diarization + AND is_agent boolean is not specified on any audio source          Note about **output audio**:</br> The output of processing will contain mergedAudio if `optimizeForWebUi` is set to at least `level1`.</br> In certain cases mergedAudioId will be a virtual DualChannel (virtual stereo): + if no diarization   + if 2 input audio were provided then 1st will be in the left channel (after audio selector is applied) and 2nd will be in the right channel (after audio selector is applied) of the merged audio   + if more than 3 input audio was provided, then all audio with speakers marked as Agent will go to left channel, and remaining audio will got to the right channel + with diarization   + if 1 input audio was provided, and diarizaton was into 2 speakers, then 1st speaker will be in the left channel and 2nd speaker will be in the right channel + with voice signatures (with or w/o diarization)   + all audio from recognized speakers marked as Agent will go to left channel and remaining speakers will got to the right channel  About **PII Redaction**:</br> `saConfig` had `piiRedaction` parameter that can be used to configure the PII redaction.</br> The redaction will be aplied to the output transcript and audio. (It is not applied to the source audio.)   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param OfflineSpeechAnalyticsRequest offline_speech_analytics_request: Body of the offline speech analytics request
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(OfflineSpeechAnalyticsResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['offline_speech_analytics_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'offline_speech_analytics_request' in local_var_params:
            body_params = local_var_params['offline_speech_analytics_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OfflineSpeechAnalyticsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_put(self, sa_session_id, **kwargs):  # noqa: E501
        """Modify SA Session  # noqa: E501

        Modify offline Speech Analytics session. Currently the following may be modified: + persistence duration - how long the session data will be kept before it expires and is deleted + context - this allows for moving speech analytics session data from one context to another   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_put(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param ModifiableOfflineSAData modifiable_offline_sa_data: Body with speech analytics data to be modified
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ModifiableOfflineSADataResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_put_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_offline_put_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """Modify SA Session  # noqa: E501

        Modify offline Speech Analytics session. Currently the following may be modified: + persistence duration - how long the session data will be kept before it expires and is deleted + context - this allows for moving speech analytics session data from one context to another   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_put_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param ModifiableOfflineSAData modifiable_offline_sa_data: Body with speech analytics data to be modified
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ModifiableOfflineSADataResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id', 'modifiable_offline_sa_data']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_offline_put`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_put`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_put`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'modifiable_offline_sa_data' in local_var_params:
            body_params = local_var_params['modifiable_offline_sa_data']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline/{saSessionId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ModifiableOfflineSADataResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_query(self, **kwargs):  # noqa: E501
        """Query SA Data (offline)  # noqa: E501

        Get Speech Analytics data from /sa/offline that matches filters.</br> This method returns the bare-bones Speech Analytics data, to get the detail for each one of those  use [GET /sa/offline/{saSessionId}](#operation/saDataGet) with the parameters that it offers.</br> By default only results from specified context are returned. This can be overridden by using `fromAllContexts` parameter.</br> You can limit number of results returned by using the `limit` parameter. If `limit` is used then the most recent results will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param bool from_all_contexts: If `true` then results from all contexts will be retrieved
        :param int limit: set the maximum number of returned results
        :param bool detailed: If `true` then detailed results will be returned including per channel data. Set to `false` if you need the results for just the table of available results w/o detail. 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: OneOfarrayarray
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_query_with_http_info(**kwargs)  # noqa: E501

    def sa_offline_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query SA Data (offline)  # noqa: E501

        Get Speech Analytics data from /sa/offline that matches filters.</br> This method returns the bare-bones Speech Analytics data, to get the detail for each one of those  use [GET /sa/offline/{saSessionId}](#operation/saDataGet) with the parameters that it offers.</br> By default only results from specified context are returned. This can be overridden by using `fromAllContexts` parameter.</br> You can limit number of results returned by using the `limit` parameter. If `limit` is used then the most recent results will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param bool from_all_contexts: If `true` then results from all contexts will be retrieved
        :param int limit: set the maximum number of returned results
        :param bool detailed: If `true` then detailed results will be returned including per channel data. Set to `false` if you need the results for just the table of available results w/o detail. 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(OneOfarrayarray, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'from_all_contexts', 'limit', 'detailed']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `sa_offline_query`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `sa_offline_query`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and 'limit' in local_var_params and local_var_params['limit'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `limit` when calling `sa_offline_query`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'from_all_contexts' in local_var_params and local_var_params['from_all_contexts'] is not None:  # noqa: E501
            query_params.append(('fromAllContexts', local_var_params['from_all_contexts']))  # noqa: E501
        if 'limit' in local_var_params and local_var_params['limit'] is not None:  # noqa: E501
            query_params.append(('limit', local_var_params['limit']))  # noqa: E501
        if 'detailed' in local_var_params and local_var_params['detailed'] is not None:  # noqa: E501
            query_params.append(('detailed', local_var_params['detailed']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OneOfarrayarray',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def sa_offline_spk_put(self, sa_session_id, **kwargs):  # noqa: E501
        """Mod. SA Speaker  # noqa: E501

        Modify speaker names for a Speech Analytics session.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_spk_put(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param list[NamedSpeaker] named_speaker: Modifications to Speech Analytics speaker - either set name or associate with [Speaker](#tag/speaker)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[OfflineSASpeakerResultBase]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.sa_offline_spk_put_with_http_info(sa_session_id, **kwargs)  # noqa: E501

    def sa_offline_spk_put_with_http_info(self, sa_session_id, **kwargs):  # noqa: E501
        """Mod. SA Speaker  # noqa: E501

        Modify speaker names for a Speech Analytics session.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.sa_offline_spk_put_with_http_info(sa_session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str sa_session_id: Session ID for Speech Analytics (required)
        :param list[NamedSpeaker] named_speaker: Modifications to Speech Analytics speaker - either set name or associate with [Speaker](#tag/speaker)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[OfflineSASpeakerResultBase], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sa_session_id', 'named_speaker']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method sa_offline_spk_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'sa_session_id' is set
        if self.api_client.client_side_validation and ('sa_session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['sa_session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `sa_session_id` when calling `sa_offline_spk_put`")  # noqa: E501

        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_spk_put`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('sa_session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['sa_session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `sa_session_id` when calling `sa_offline_spk_put`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'sa_session_id' in local_var_params:
            path_params['saSessionId'] = local_var_params['sa_session_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'named_speaker' in local_var_params:
            body_params = local_var_params['named_speaker']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/sa/offline/{saSessionId}/spk', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[OfflineSASpeakerResultBase]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
