# coding: utf-8

"""
    Voicegain API v1

    # New  [Telephony Bot API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + Telephony Bot APIs which in addition to speech-to-text allow for control of real-time communications (RTC) session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Web Console](https://console.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  When making Web APi request the JWT has to be included in the \"Authorization: Bearer\" header. For example, when using curl to make a request:  <pre>   curl -i -X POST \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Authorization: Bearer eyJh......BOGCO70w\" \\   -d @data1.json \\   https://api.voicegain.ai/v1/asr/transcribe/async </pre>  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).  # Edge Deployment API URLs  When you are using Voicegain plaform deployed on Edge, the Web API urls will be different from those that are used in the Cloud (and given in the examples).  For example: * a Web API URL in the Cloud may be: https://api.voicegain.ai/v1/asr/transcribe/async  * but when deployed on Edge which e.g. has this IP:port 10.137.16.7:31680 and does not have SSL configured   * the URL for the same API will be http://10.137.16.7:31680/ascalon-web-api/asr/transcribe/async  * if deployed on Edge with SSL cert and IP:port 10.137.16.7:31443   * the URL for the same API will be https://10.137.16.7:31443/ascalon-web-api/asr/transcribe/async  The reason for this is that in the Cloud, the Web API service is on its own hostname, but on the Edge it has to share the hostname/IP with the Web Console  (which would e.g. have this URL: https://10.137.16.7:31443/customer-portal/)  # Context Defaults  Most of the API requests are made within a specific Context identified by the JWT being used. Each Context has some API (mainly ASR API) related settings which can be set from the Web Console, see image below: ![Context Settings](https://github.com/voicegain/platform/raw/master/images/Context-Speech-Recognition-Settings.PNG)  These settings override the corresponding API default values.  For example, if `noInputTimeout` default is 15000, but the Context 'No Input Timeout' setting is 30000,  and no value is provided in the API request for `noInputTimeout` field, then the API request will run with `noInputTimeout` of 30000.    # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Specifically, 2x OFF-LINE use case is not supported because of how the task queue processor is implemented. To transcribe 2-channels separately in OFF-LINE mode you will need to make 2 separate OFF-LINE transcription requests. Please, let us know if you think you have a valid use case for other combinations.  # Telephony Bot API  (previously called RTC Callback API, where RTC stands for Real Time Communications)   Voicegain Telephony Bot APIs allows you to build conversational voice-enabled applications (e.g. IVRs, Voicebots) over an RTC session (a telephone call for example).  See this blog post for an overview of how this API works: [Voicegain releases Telephony Bot APIs for telephony IVRs and bots](https://www.voicegain.ai/post/rtc-callback-api-released)  Telephony Bot API is a callback API - Voicegain platform makes HTTP request to your app with information about the result of e.g. latest recognition and in response you provide instruction for the next step of the conversation. See the spec of these requests [here](#tag/aivr-callback).  # Speech Analytics API  Voicegain Speech Analytics analyzes both the transcript and the audio (typically of a telephone call).  The results are returned per channel (real or diarized) except where the recognized entities span more than one channel. For entities where it is applicable we return the location in the audio (start and end time) and the transcript (index of the words).  ## Capabilities of Speech Analytics  Voicegain Speech Analytics can identify/compute the following: + **named entities** - (NER i.e. named entity recognition) - the following entities are recognized:   + ADDRESS - Postal address.   + CARDINAL - Numerals that do not fall under another type.   + CC - Credit Card   + DATE - Absolute or relative dates or periods.   + DMY - Full date including all of day, month and year.         + EMAIL - Email address   + EVENT - Named hurricanes, battles, wars, sports events, etc.   + FAC - Buildings, airports, highways, bridges, etc.   + GPE - Countries, cities, states.   + LANGUAGE - Any named language.   + LAW - Named documents made into laws.   + NORP - Nationalities or religious or political groups.   + MONEY - Monetary values, including unit.   + ORDINAL - \"first\", \"second\", etc.   + ORG - Companies, agencies, institutions, etc.   + PERCENT - Percentage, including \"%\".   + PERSON - People, including fictional.   + PHONE - Phone number.   + PRODUCT - Objects, vehicles, foods, etc. (Not services.)   + QUANTITY - Measurements, as of weight or distance.   + SSN - Social Security number   + TIME - Times smaller than a day.   + WORK_OF_ART - Titles of books, songs, etc.   + ZIP - Zip Code (if not part of an Address)    In addition to returning the named entity itself, we return the sub-concepts within entity, e.g. for ADDRESs we will return state (e.g. TX) and zip code if found.  + **keywords** - these are single words or short phrases e.g. company or product names.    Currently, keywords are detected using simple matching using stemming - so e.g. a keyword \"cancel\" will match \"cancellation\".    In near future we will support \"smart expansion\" which will also match synonyms while paying attention to the correct meaning of the word.     In addition to keywords we return keyword groups, e.g. several company name keywords can be combined into a `Competition` keyword group.  + **phrases (intent)** - allows for detection of phrases/intents that match the meaning of the phrases specified in the example training Sections).</br>   For each detected phrase/intent the system will also return entities and keywords contained in the phrase, if configured to do so.   For example, transcript \"Hello, my name is Lucy\" may match phrase/intent \"INTRODUCTION\" with the NER of PERSON and value \"Lucy\".       The configuration for phrase/intent detection takes the following parameters:   + _list_ of example phrases - each phrase has a sensitivity value which determines how close it has to match (sensitivity of 1.0 requires the closest match, sensitivity of 0.0 allows for vague matches).   + _regex_ - optional regex phrases to augment the examples - these require exact match   + _slots_ - types on named entities and keywords to be recognized within the phrase/intent</br>     Note: support for slots of same type but different meaning will be added in the future.     Currently it is possible e.g. to recognize places (GPE) but not possible to distinguish e.g. between types of them, like departure or destination place.   + _location_ - this narrows down where the phrase/match must occur - the options are:     + channel - agent or caller      + time in the call - from the start or from the end     + dialogue act - require the phrase to be part of a specified dialogue act, see https://web.stanford.edu/~jurafsky/ws97/manual.august1.html, first table, column SWBD    + **phrase groups** - computed across all channels - this is more powerful than keyword groups as it can be configured to require all phrases/intents in the groups to be present in any or fixed order.   One use case would be to detect a pair of a question and a confirming answer - for example to determine call resolution: \"Have I answered all your question?\", \"Yes\". + **criteria** - computed by rules/conditions looking at the following parameters:   + _call metrics_   + _regex_ - match of the text of the transcript   + _keywords_ - any keywords or keyword groups   + _NER_ - any named entities   + _phrases_ - any phrases/intents or phrase groups   + _dialogElements_ - selection of custom hardcoded rules that may accomplish tasks not possible with other conditions    The individual rules/conditions can be further narrowed down using filters like:   + _channel_ - agent or caller    + _time in the call_ - from the start or from the end    Multiple rules can be combined to form a logical AND expression.   Finally, the individual rules can be negated so that the absence of certain events is considered as a positive match.    When Criteria are satisfied then the system provides a detailed justification information. + **topics** - computed from text across all channels - assigns to the call a set of likely topics with their scores.    A topic classifier is built in a separate step using a corpus. The build process requires manual labeling of the topics.    For each call, the entire transcript is fed to the topic classifier and we get back the set of detected topics and their scores (in the 0..1 range).   It is useful e.g. for separating Billing calls from Troubleshooting calls from Account Change calls, etc.  + **summary** - computed from text across all channels - provides a summary of the call in a form of a set of sentences.   These may either be key sentences directly pulled from the transcript, or sentences generated by summarizing entire call or sections of the call.  + **sentiment** - computed from text - standard call sentiment as used in Call Center Speech Analytics.   Returns sentiment values from -1.0 (negative/mad/angry) to +1.0 (positive/happy/satisfied) + **mood** - computed from text - can distinguish 6 moods:   + neutral    + anger    + disgust    + fear    + happiness   + sadness   + surprise     Values are returned as a map from mood enum values to a number in (0.0, 1.0) range - multiple moods can be detected in the same place in the transcript in varying degrees. + **gender** - computed to audio - Estimates the gender of the speaker as far as it is possible to do it from the voice alone. + **word cloud** - returns word cloud data (map from words/phrases to frequencies) - the algorithm uses: stop word removal, stemming, frequent phrase detection. + **call metrics** - these are simple metrics computed from the audio and the transcript    + _silence_ - amount of silence in the call   + _talk_ - talk streaks for each of the channels   + _overtalk_ - amount of time when call participants talk over ove another   + _energy_ - the volume of the call and the variation   + _pitch_ - the pitch (frequency of the voice) and the variation  Voicegain allows for configuring Speech Analytics processing by preparing a Speech Analytics Configuration which is basically a selection of the capabilities mentioned above plus configuration of variable elements like keywords, phrases, etc.  </br> You can configure Speech Analytics using **[/sa/config API](#operation/saConfigPost)**   Once the configuration is complete you can launch speech transcription and analytics session using the **[/sa API](#operation/saPost)**   ## Offline vs Real-Time Speech Analytics  Speech audio can be transcribed and then analyzed in one of two modes: + **OFF-LINE** - use the `/sa/offline/` API for this.    Audio will be queued for transcription, then transcribed, and both the audio and transcript will pass through various speech analytics algorithms according to the specified configuration.   The results of transcription and speech analytics can be retrieved using the [GET **/sa/offline/{sid}/data** API](#tag/sa-offline/operation/saOfflineGetData)   + **REAL-TIME** - use the `/sa` API for this.    Audio will immediately be submitted to real-time transcription and the stream of transcribed words will be fed to real-time speech analytics.    The results of transcription and speech analytics will be returned over websocket as soon as they are available. </br>   The format of the returned messages is defined [here](#operation/saWebsocketPayload).    Note that not all speech analytics features are available in real-time. Features missing in real-time are: criteria, topics, summary, gender, word cloud, and call metrics.</br>   The results will also be available afterwards using the [GET **/sa/{sid}/data** API](#operation/saDataGet)  ## Agent Review Form  Data computed by Speech Analytics can be used to automatically fill/answer questions of the Call/Agent Review Form.   The automatic answers can be obtained based on previously defined Criteria (see above).  When Criteria are satisfied then the system provides a detailed justification information so it is easily possible to verify that the automated answer on a Review Form was correct.  ## PII Redaction  Being able to recognize occurrence of certain elements in the transcript allows us to remove them from both the text and the audio - this is called PII Redaction where PII stands for Personally Identifiable Information.  Currently, PII Redaction is limited to named entities (NER).  User can select any NER type detected by [Speech Analytics](#section/Speech-Analytics-API/Capabilities-of-Speech-Analytics) to be replaced by a specified placeholder in the text and by silence in the audio.  If your Enterprise account with Voicegain is setup with PCI-DSS compliance option, then PII Redaction of credit card numbers is enabled by default and cannot be disabled.    # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Rate Limiting  Access to Voicegain resources is controlled using the following limit settings on the account.  Newly created accounts get the limit values listed below.  If you need higher limits please contact us at support@voicegain.ai  The limits apply to the use of the Voicegain Platform in the Cloud.  On the Edge, the limits will be determined by the type of license you will purchase.  ## Types of Rate Limits  | Limit | default value | description | |---|---|---| | apiRequestLimitPerMinute | 75 | Basic rate limit with a fixed window of 1 minute applying to all API requests. Requests to /data API will be counted at 10x other requests. | | apiRequestLimitPerHour | 2000 | Basic rate limit with a fixed window of 1 hour applying to all API requests. Requests to /data API will be counted at 10x other requests. | | asrConcurrencyLimit | 4 | Limit on number of concurrent ASR requests. Does not apply to OFF-LINE requests. | | offlineQueueSizeLimit | 10 | Maximum number of OFF-LINE transcription jobs that may be submitted to the queue. | | offlineThroughputLimitPerHour | 4 | Maximum number of hours of audio that can be processed by OFF-LINE transcription within 1 hour. Note: For Edge deployment the limit interval is per day instead of per hour. | | offlineWorkerLimit | 2 | Maximum number of OFF-LINE transcription job workers that will be used to process the account audio. |  For API requests running longer that the rate limit window length, the request count will be applied to both the window when the request started and the window when the request finished.   Every HTTP API request will return several rate-limit related headers in its response.  The header values show the applicable limit, the remaining request count in the current window, and the number of seconds to when the limit resets. For example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 1 RateLimit-Reset: 7 ```  ## When Rate Limits are Hit  If a rate-limit is hit then [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) HTTP error code will be returned. The response headers will additionally include Retry-After value, for example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 0 RateLimit-Reset: 6 Retry-After: 6 ``` If `asrConcurrencyLimit` is hit then the response headers will contain:  ``` X-ResourceLimit-Type: ASR-Concurrency X-ResourceLimit-Limit: 4 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ``` Note that we return a superset of values that are returned for a basic API request limit.  This will allow a client code that was written to handle basic rate limiting to be able to handle concurrency limiting too.  Note also that for the concurrency limit the Retry-After value is approximate and is not guaranteed - so client code may have to retry multiple times. (We will return increasing back-off Retry-After values in case of the limit being hit multiple times.)   In case of `offlineQueueSizeLimit` limit we will return, for example:  ``` X-ResourceLimit-Type: Offline-Queue-Size X-ResourceLimit-Limit: 10 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ```   # Pagination  Voicegain API supports 2 methods of pagination.  ## Sequential pagination  For methods that support sequential pagination Voicegain has standardized on using the following query parameters: + start_after={object id OR nul}  + end_before={object id OR nul}  + per_page={number items per page}  If `start_after=nul` then the first page will be retrieved.</br> If `end_before=nul` then the last page will be retrieved.  `start_after` and `end_before` should not be used together.  If neither `start_after` nor `end_before` are provided, then `start_after=nul` will be assumed.  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?start_after=nul&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?end_before=5f7f1f7d67f67ddaa622b68e&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?start_after=5f7f1f7d67f67ddaa622b68d&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?start_after=5f7f1f7d67f67ddaa622b68c4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?end_before=nul&per_page=50>; rel=\"last\" ```  ## Direct pagination  For methods that support direct pagination Voicegain has standardized on using the following query parameters: + page={page number}  + per_page={number items per page}  `page` is the page number starting from 1 (i.e. first page is 1). This is not an item offset.  This also implies that `per_page` should be kept constant for a set of related requests.  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 786 Link: <https://api.voicegain.ai/v1/sa/call?pager=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=7&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=8&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=16&per_page=50>; rel=\"last\" ```   # PCI-DSS Compliance (Cloud)  The PCI-DSS compliant endpoint on the Voicegain Cloud is https://sapi.voicegain.ai/v1/ </br> Do not submit requests that may contain CHD data to the standard endpoint at https://api.voicegain.ai/v1/  Here is a list of all API Methods that are PCI-DSS compliant: + `/asr/transcribe`: [POST](#operation/asrTranscribePost) + `/asr/transcribe/async`: [POST](#operation/asrTranscribeAsyncPost) - we support OFF-LINE and REAL-TIME + `/asr/transcribe/{sessionId}`: [GET](#operation/asrTranscribeAsyncGet) [PUT](#operation/asrTranscribeAsyncPut) [DELETE](#operation/asrTranscribeAsyncDelete)  Note that the /data API is not yet PCI-DSS compliant on the Cloud. This means that the only PCI-DSS compliant ways to submit the audio are: + `fromUrl` - use `authConf` for authenticated access or use signed short-lived URLs + `inline` + `stream` - only `WSS` (old `WEBSOCKET`) and `TWIML` protocols are supported right now  https://sapi.voicegain.ai/v1/ endpoint does not support API methods that would store data, either the audio or the transcription results.   https://sapi.voicegain.ai/v1/ endpoint does support audio redaction. Redacted audio is not stored but submitted directly to the URL specified in the request `audio.callback`.   # PCI-DSS Compliance (Edge)  Because the Edge deployment happens ultimately in the customer's environment, it will the customer's responsibility to certify their Edge depoyment of the Voicegain platform as PCI-DSS compliant.  Voicegain can provide Attestation of Compliance (AoC) for the following PCI-DSS sections as far as they releate to Voicegain Software that will be deployed on Edge: + 5. Use and regularly update anti-virus software or programs + 6. Develop and maintain secure systems and applications + 11. Regularly test security systems and processes + 12. Maintain a policy that addresses information security for all personnel  For the following PCI-DSS sections we will provide detailed data regarding implementation: + 3. Protect stored cardholder data   # noqa: E501

    The version of the OpenAPI document: 1.114.0 - updated January 16, 2025
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from voicegain_speech.configuration import Configuration


class AsrSettingsRecognitionDefaults(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'acoustic_model_non_real_time': 'str',
        'acoustic_model_real_time': 'str',
        'confidence_threshold': 'float',
        'language_detection': 'AsrSettingsCommonLanguageDetection',
        'languages': 'list[Language]',
        'max_alternatives': 'int',
        'sensitivity': 'float',
        'speech_context': 'str',
        'speed_vs_accuracy': 'float',
        'complete_timeout': 'int',
        'incomplete_timeout': 'int',
        'lang_model': 'str',
        'no_input_timeout': 'int'
    }

    attribute_map = {
        'acoustic_model_non_real_time': 'acousticModelNonRealTime',
        'acoustic_model_real_time': 'acousticModelRealTime',
        'confidence_threshold': 'confidenceThreshold',
        'language_detection': 'languageDetection',
        'languages': 'languages',
        'max_alternatives': 'maxAlternatives',
        'sensitivity': 'sensitivity',
        'speech_context': 'speechContext',
        'speed_vs_accuracy': 'speedVsAccuracy',
        'complete_timeout': 'completeTimeout',
        'incomplete_timeout': 'incompleteTimeout',
        'lang_model': 'langModel',
        'no_input_timeout': 'noInputTimeout'
    }

    def __init__(self, acoustic_model_non_real_time=None, acoustic_model_real_time=None, confidence_threshold=0.01, language_detection=None, languages=None, max_alternatives=1, sensitivity=0.5, speech_context=None, speed_vs_accuracy=0.5, complete_timeout=2000, incomplete_timeout=5000, lang_model=None, no_input_timeout=10000, local_vars_configuration=None):  # noqa: E501
        """AsrSettingsRecognitionDefaults - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._acoustic_model_non_real_time = None
        self._acoustic_model_real_time = None
        self._confidence_threshold = None
        self._language_detection = None
        self._languages = None
        self._max_alternatives = None
        self._sensitivity = None
        self._speech_context = None
        self._speed_vs_accuracy = None
        self._complete_timeout = None
        self._incomplete_timeout = None
        self._lang_model = None
        self._no_input_timeout = None
        self.discriminator = None

        if acoustic_model_non_real_time is not None:
            self.acoustic_model_non_real_time = acoustic_model_non_real_time
        if acoustic_model_real_time is not None:
            self.acoustic_model_real_time = acoustic_model_real_time
        if confidence_threshold is not None:
            self.confidence_threshold = confidence_threshold
        if language_detection is not None:
            self.language_detection = language_detection
        if languages is not None:
            self.languages = languages
        if max_alternatives is not None:
            self.max_alternatives = max_alternatives
        if sensitivity is not None:
            self.sensitivity = sensitivity
        if speech_context is not None:
            self.speech_context = speech_context
        if speed_vs_accuracy is not None:
            self.speed_vs_accuracy = speed_vs_accuracy
        if complete_timeout is not None:
            self.complete_timeout = complete_timeout
        if incomplete_timeout is not None:
            self.incomplete_timeout = incomplete_timeout
        if lang_model is not None:
            self.lang_model = lang_model
        if no_input_timeout is not None:
            self.no_input_timeout = no_input_timeout

    @property
    def acoustic_model_non_real_time(self):
        """Gets the acoustic_model_non_real_time of this AsrSettingsRecognitionDefaults.  # noqa: E501

        (Optional) Name of an Acoustic Model that is to be used for offline and semi-real-time processing.  In the Cloud, the currently available offline models are: - **VoiceGain-omega** - the default model - best suited to general transcription tasks, - **VoiceGain-omega-x** - model trained on call-center calls  Only available for **offline [async](#tag/transcribe/operation/asrTranscribeAsyncPost)** transcription: - **whisper:medium**, also may use **whisper** as a shortcut for \"whisper:medium\" - **whisper:small**,  - **whisper:base**    If a model name is not provided (i.e. absent or null), then a model specified on the Context will be used,  and if there is no model specified on the Context then a suitable default will be used.</br> Note, empty string \"\" will be interpreted as a model name and will return an error as there is no model with empty name. </br> In some Edge deployments, may include version number separated by `:` , for example, **VoiceGain-BD_en-us:11**   # noqa: E501

        :return: The acoustic_model_non_real_time of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_non_real_time

    @acoustic_model_non_real_time.setter
    def acoustic_model_non_real_time(self, acoustic_model_non_real_time):
        """Sets the acoustic_model_non_real_time of this AsrSettingsRecognitionDefaults.

        (Optional) Name of an Acoustic Model that is to be used for offline and semi-real-time processing.  In the Cloud, the currently available offline models are: - **VoiceGain-omega** - the default model - best suited to general transcription tasks, - **VoiceGain-omega-x** - model trained on call-center calls  Only available for **offline [async](#tag/transcribe/operation/asrTranscribeAsyncPost)** transcription: - **whisper:medium**, also may use **whisper** as a shortcut for \"whisper:medium\" - **whisper:small**,  - **whisper:base**    If a model name is not provided (i.e. absent or null), then a model specified on the Context will be used,  and if there is no model specified on the Context then a suitable default will be used.</br> Note, empty string \"\" will be interpreted as a model name and will return an error as there is no model with empty name. </br> In some Edge deployments, may include version number separated by `:` , for example, **VoiceGain-BD_en-us:11**   # noqa: E501

        :param acoustic_model_non_real_time: The acoustic_model_non_real_time of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: str
        """

        self._acoustic_model_non_real_time = acoustic_model_non_real_time

    @property
    def acoustic_model_real_time(self):
        """Gets the acoustic_model_real_time of this AsrSettingsRecognitionDefaults.  # noqa: E501

        (Optional) Name of a real-time capable Acoustic Model.  In the Cloud, the currently available real-time models are: - **VoiceGain-kappa** - default model, best accuracy, longer latency - **VoiceGain-rho** - lower latency, somewhat lower accuracy - **VoiceGain-rho-en-us** - lowest (best) latency, lower accuracy than VoiceGain-rho  If a model name is not provided (i.e. absent or null), then a model specified on the Context will be used,  and if there is no model specified on the Context then a suitable default will be used.</br> Note, empty string \"\" will be interpreted as a model name and will return an error as there is no model with empty name. </br> In some Edge deployments, may include version number separated by `:`, for example, **VoiceGain-IVR_en-us:3**   # noqa: E501

        :return: The acoustic_model_real_time of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_real_time

    @acoustic_model_real_time.setter
    def acoustic_model_real_time(self, acoustic_model_real_time):
        """Sets the acoustic_model_real_time of this AsrSettingsRecognitionDefaults.

        (Optional) Name of a real-time capable Acoustic Model.  In the Cloud, the currently available real-time models are: - **VoiceGain-kappa** - default model, best accuracy, longer latency - **VoiceGain-rho** - lower latency, somewhat lower accuracy - **VoiceGain-rho-en-us** - lowest (best) latency, lower accuracy than VoiceGain-rho  If a model name is not provided (i.e. absent or null), then a model specified on the Context will be used,  and if there is no model specified on the Context then a suitable default will be used.</br> Note, empty string \"\" will be interpreted as a model name and will return an error as there is no model with empty name. </br> In some Edge deployments, may include version number separated by `:`, for example, **VoiceGain-IVR_en-us:3**   # noqa: E501

        :param acoustic_model_real_time: The acoustic_model_real_time of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: str
        """

        self._acoustic_model_real_time = acoustic_model_real_time

    @property
    def confidence_threshold(self):
        """Gets the confidence_threshold of this AsrSettingsRecognitionDefaults.  # noqa: E501

        Hypotheses below this threshold will result in NOMATCH  # noqa: E501

        :return: The confidence_threshold of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: float
        """
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, confidence_threshold):
        """Sets the confidence_threshold of this AsrSettingsRecognitionDefaults.

        Hypotheses below this threshold will result in NOMATCH  # noqa: E501

        :param confidence_threshold: The confidence_threshold of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                confidence_threshold is not None and confidence_threshold > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `confidence_threshold`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                confidence_threshold is not None and confidence_threshold < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `confidence_threshold`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._confidence_threshold = confidence_threshold

    @property
    def language_detection(self):
        """Gets the language_detection of this AsrSettingsRecognitionDefaults.  # noqa: E501


        :return: The language_detection of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: AsrSettingsCommonLanguageDetection
        """
        return self._language_detection

    @language_detection.setter
    def language_detection(self, language_detection):
        """Sets the language_detection of this AsrSettingsRecognitionDefaults.


        :param language_detection: The language_detection of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: AsrSettingsCommonLanguageDetection
        """

        self._language_detection = language_detection

    @property
    def languages(self):
        """Gets the languages of this AsrSettingsRecognitionDefaults.  # noqa: E501

        Language that should be recognized - this is important for acoustic Models that support more than one language.</br> This is a list parameter because we support multiple language recognition -  for those cases where the exact language spoken in the audio is not known up-front.  See [this knowledge base article](https://support.voicegain.ai/hc/en-us/articles/6535757706772-Languages-supported-in-Voicegain-Speech-to-Text) for which languages are supported with which models.   # noqa: E501

        :return: The languages of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: list[Language]
        """
        return self._languages

    @languages.setter
    def languages(self, languages):
        """Sets the languages of this AsrSettingsRecognitionDefaults.

        Language that should be recognized - this is important for acoustic Models that support more than one language.</br> This is a list parameter because we support multiple language recognition -  for those cases where the exact language spoken in the audio is not known up-front.  See [this knowledge base article](https://support.voicegain.ai/hc/en-us/articles/6535757706772-Languages-supported-in-Voicegain-Speech-to-Text) for which languages are supported with which models.   # noqa: E501

        :param languages: The languages of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: list[Language]
        """

        self._languages = languages

    @property
    def max_alternatives(self):
        """Gets the max_alternatives of this AsrSettingsRecognitionDefaults.  # noqa: E501

        number of recognition hypotheses to return as result (top N-Best)  # noqa: E501

        :return: The max_alternatives of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: int
        """
        return self._max_alternatives

    @max_alternatives.setter
    def max_alternatives(self, max_alternatives):
        """Sets the max_alternatives of this AsrSettingsRecognitionDefaults.

        number of recognition hypotheses to return as result (top N-Best)  # noqa: E501

        :param max_alternatives: The max_alternatives of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                max_alternatives is not None and max_alternatives > 100):  # noqa: E501
            raise ValueError("Invalid value for `max_alternatives`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_alternatives is not None and max_alternatives < 1):  # noqa: E501
            raise ValueError("Invalid value for `max_alternatives`, must be a value greater than or equal to `1`")  # noqa: E501

        self._max_alternatives = max_alternatives

    @property
    def sensitivity(self):
        """Gets the sensitivity of this AsrSettingsRecognitionDefaults.  # noqa: E501

        Determines the threshold for rejection of low volume background speech (or bleed-through from other channels). </br> 1 is most sensitive (least rejection) and corresponds to -90 dbFS </br> 0 is least sensitive (most rejection) and corresponds to -50 dbFS </br> </br> For real-time speech-to-text, this setting affects start-of-speech and end-of-speech detection. </br> If some background noise/speech is causing a too early start-of-speech try a lower value of sensitivity.   # noqa: E501

        :return: The sensitivity of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: float
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, sensitivity):
        """Sets the sensitivity of this AsrSettingsRecognitionDefaults.

        Determines the threshold for rejection of low volume background speech (or bleed-through from other channels). </br> 1 is most sensitive (least rejection) and corresponds to -90 dbFS </br> 0 is least sensitive (most rejection) and corresponds to -50 dbFS </br> </br> For real-time speech-to-text, this setting affects start-of-speech and end-of-speech detection. </br> If some background noise/speech is causing a too early start-of-speech try a lower value of sensitivity.   # noqa: E501

        :param sensitivity: The sensitivity of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sensitivity is not None and sensitivity > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `sensitivity`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sensitivity is not None and sensitivity < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sensitivity`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sensitivity = sensitivity

    @property
    def speech_context(self):
        """Gets the speech_context of this AsrSettingsRecognitionDefaults.  # noqa: E501


        :return: The speech_context of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: str
        """
        return self._speech_context

    @speech_context.setter
    def speech_context(self, speech_context):
        """Sets the speech_context of this AsrSettingsRecognitionDefaults.


        :param speech_context: The speech_context of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: str
        """
        allowed_values = ["normal", "digits"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and speech_context not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `speech_context` ({0}), must be one of {1}"  # noqa: E501
                .format(speech_context, allowed_values)
            )

        self._speech_context = speech_context

    @property
    def speed_vs_accuracy(self):
        """Gets the speed_vs_accuracy of this AsrSettingsRecognitionDefaults.  # noqa: E501

        Between 0.0 and 1.0 - tradeoff between accuracy and speed/resource use.</br> For Edge deployment use only.   # noqa: E501

        :return: The speed_vs_accuracy of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: float
        """
        return self._speed_vs_accuracy

    @speed_vs_accuracy.setter
    def speed_vs_accuracy(self, speed_vs_accuracy):
        """Sets the speed_vs_accuracy of this AsrSettingsRecognitionDefaults.

        Between 0.0 and 1.0 - tradeoff between accuracy and speed/resource use.</br> For Edge deployment use only.   # noqa: E501

        :param speed_vs_accuracy: The speed_vs_accuracy of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                speed_vs_accuracy is not None and speed_vs_accuracy > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `speed_vs_accuracy`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                speed_vs_accuracy is not None and speed_vs_accuracy < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `speed_vs_accuracy`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._speed_vs_accuracy = speed_vs_accuracy

    @property
    def complete_timeout(self):
        """Gets the complete_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501

        ASR complete timeout (in msec). The length of silence required following user speech before the speech recognizer finalizes a result  (either accepting it or throwing a nomatch event).  The `completeTimeout` is used when the speech is a complete match of an active grammar and no further words can be spoken that would match the grammar. </br>There is an internal minimum of 500ms needed for detection of end-of-speech so setting value between 1 and 500 will result in effectively the value being 500.   # noqa: E501

        :return: The complete_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: int
        """
        return self._complete_timeout

    @complete_timeout.setter
    def complete_timeout(self, complete_timeout):
        """Sets the complete_timeout of this AsrSettingsRecognitionDefaults.

        ASR complete timeout (in msec). The length of silence required following user speech before the speech recognizer finalizes a result  (either accepting it or throwing a nomatch event).  The `completeTimeout` is used when the speech is a complete match of an active grammar and no further words can be spoken that would match the grammar. </br>There is an internal minimum of 500ms needed for detection of end-of-speech so setting value between 1 and 500 will result in effectively the value being 500.   # noqa: E501

        :param complete_timeout: The complete_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                complete_timeout is not None and complete_timeout > 15000):  # noqa: E501
            raise ValueError("Invalid value for `complete_timeout`, must be a value less than or equal to `15000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                complete_timeout is not None and complete_timeout < 1):  # noqa: E501
            raise ValueError("Invalid value for `complete_timeout`, must be a value greater than or equal to `1`")  # noqa: E501

        self._complete_timeout = complete_timeout

    @property
    def incomplete_timeout(self):
        """Gets the incomplete_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501

        ASR incomplete timeout (in msec).  The length of silence required following user speech before the speech recognizer finalizes a result  (by either accepting it or throwing a nomatch event).  In contrast to `completeTimeout`, the `incompleteTimeout` is used when the speech is an incomplete match to an active grammar,  **or** when the speech is a match but it is possible to speak further and match the grammar.</br> A too short incomplete timeout may lead to an utterance being broken up inappropriately, or throwing a nomatch while user has still not finished speaking.  A too long incomplete timeout value delays the result completion and therefore makes the system responses feel slow to the user.  </br>There is an internal minimum of 500ms needed for detection of end-of-speech so setting value between 1 and 500 will result in effectively the value being 500.   # noqa: E501

        :return: The incomplete_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: int
        """
        return self._incomplete_timeout

    @incomplete_timeout.setter
    def incomplete_timeout(self, incomplete_timeout):
        """Sets the incomplete_timeout of this AsrSettingsRecognitionDefaults.

        ASR incomplete timeout (in msec).  The length of silence required following user speech before the speech recognizer finalizes a result  (by either accepting it or throwing a nomatch event).  In contrast to `completeTimeout`, the `incompleteTimeout` is used when the speech is an incomplete match to an active grammar,  **or** when the speech is a match but it is possible to speak further and match the grammar.</br> A too short incomplete timeout may lead to an utterance being broken up inappropriately, or throwing a nomatch while user has still not finished speaking.  A too long incomplete timeout value delays the result completion and therefore makes the system responses feel slow to the user.  </br>There is an internal minimum of 500ms needed for detection of end-of-speech so setting value between 1 and 500 will result in effectively the value being 500.   # noqa: E501

        :param incomplete_timeout: The incomplete_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                incomplete_timeout is not None and incomplete_timeout > 30000):  # noqa: E501
            raise ValueError("Invalid value for `incomplete_timeout`, must be a value less than or equal to `30000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                incomplete_timeout is not None and incomplete_timeout < 1):  # noqa: E501
            raise ValueError("Invalid value for `incomplete_timeout`, must be a value greater than or equal to `1`")  # noqa: E501

        self._incomplete_timeout = incomplete_timeout

    @property
    def lang_model(self):
        """Gets the lang_model of this AsrSettingsRecognitionDefaults.  # noqa: E501

        (Only applicable if large-vocabulary recognition has been enabled by using the special transcribe grammar.) </br>   Name or UUID of the language model to use. If absent then will use default language model.   # noqa: E501

        :return: The lang_model of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: str
        """
        return self._lang_model

    @lang_model.setter
    def lang_model(self, lang_model):
        """Sets the lang_model of this AsrSettingsRecognitionDefaults.

        (Only applicable if large-vocabulary recognition has been enabled by using the special transcribe grammar.) </br>   Name or UUID of the language model to use. If absent then will use default language model.   # noqa: E501

        :param lang_model: The lang_model of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                lang_model is not None and len(lang_model) > 128):
            raise ValueError("Invalid value for `lang_model`, length must be less than or equal to `128`")  # noqa: E501

        self._lang_model = lang_model

    @property
    def no_input_timeout(self):
        """Gets the no_input_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501

        Used to determine if NOINPUT should be returned (in msec)  # noqa: E501

        :return: The no_input_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :rtype: int
        """
        return self._no_input_timeout

    @no_input_timeout.setter
    def no_input_timeout(self, no_input_timeout):
        """Sets the no_input_timeout of this AsrSettingsRecognitionDefaults.

        Used to determine if NOINPUT should be returned (in msec)  # noqa: E501

        :param no_input_timeout: The no_input_timeout of this AsrSettingsRecognitionDefaults.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                no_input_timeout is not None and no_input_timeout > 60000):  # noqa: E501
            raise ValueError("Invalid value for `no_input_timeout`, must be a value less than or equal to `60000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                no_input_timeout is not None and no_input_timeout < 1):  # noqa: E501
            raise ValueError("Invalid value for `no_input_timeout`, must be a value greater than or equal to `1`")  # noqa: E501

        self._no_input_timeout = no_input_timeout

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AsrSettingsRecognitionDefaults):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsrSettingsRecognitionDefaults):
            return True

        return self.to_dict() != other.to_dict()
