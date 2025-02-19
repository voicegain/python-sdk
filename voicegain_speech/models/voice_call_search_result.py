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


class VoiceCallSearchResult(object):
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
        'agent': 'Agent',
        'aivr_app_id': 'str',
        'aivr_session_id': 'str',
        'call_center_call_id': 'str',
        'daily_repeat_calls': 'int',
        'direction': 'str',
        'dtmf_events': 'list[DtmfEventWithChannel]',
        'end_time': 'datetime',
        'external_endpoint': 'str',
        'internal_endpoint': 'str',
        'language': 'Language',
        'markers': 'list[CallMarker]',
        'num_audio_channels': 'int',
        'num_spk_channels': 'int',
        'originating_call_id': 'str',
        'queue': 'Queue',
        'recording': 'str',
        'start_time': 'datetime',
        'tags': 'list[str]',
        'account_id': 'str',
        'aivr_transfer_dest_type': 'str',
        'call_id': 'str',
        'call_resolved': 'bool',
        'context_id': 'str',
        'cr_answers_id': 'str',
        'duration': 'int',
        'incidents': 'float',
        'keywords': 'list[str]',
        'last_recompute_time': 'datetime',
        'notes': 'str',
        'progress_phase': 'ProgressPhase',
        'recompute_phase': 'str',
        'review_notes': 'str',
        'review_status': 'str',
        'sa_session_id': 'str',
        'score': 'float',
        'sentiment': 'float',
        'spawned_calls': 'list[str]',
        'topics': 'list[str]',
        'version': 'int',
        'word_cloud': 'list[WordCloudItem]',
        'headline': 'str'
    }

    attribute_map = {
        'agent': 'agent',
        'aivr_app_id': 'aivrAppId',
        'aivr_session_id': 'aivrSessionId',
        'call_center_call_id': 'callCenterCallId',
        'daily_repeat_calls': 'dailyRepeatCalls',
        'direction': 'direction',
        'dtmf_events': 'dtmfEvents',
        'end_time': 'endTime',
        'external_endpoint': 'externalEndpoint',
        'internal_endpoint': 'internalEndpoint',
        'language': 'language',
        'markers': 'markers',
        'num_audio_channels': 'numAudioChannels',
        'num_spk_channels': 'numSpkChannels',
        'originating_call_id': 'originatingCallId',
        'queue': 'queue',
        'recording': 'recording',
        'start_time': 'startTime',
        'tags': 'tags',
        'account_id': 'accountId',
        'aivr_transfer_dest_type': 'aivrTransferDestType',
        'call_id': 'callId',
        'call_resolved': 'callResolved',
        'context_id': 'contextId',
        'cr_answers_id': 'crAnswersId',
        'duration': 'duration',
        'incidents': 'incidents',
        'keywords': 'keywords',
        'last_recompute_time': 'lastRecomputeTime',
        'notes': 'notes',
        'progress_phase': 'progressPhase',
        'recompute_phase': 'recomputePhase',
        'review_notes': 'reviewNotes',
        'review_status': 'reviewStatus',
        'sa_session_id': 'saSessionId',
        'score': 'score',
        'sentiment': 'sentiment',
        'spawned_calls': 'spawnedCalls',
        'topics': 'topics',
        'version': 'version',
        'word_cloud': 'wordCloud',
        'headline': 'headline'
    }

    def __init__(self, agent=None, aivr_app_id=None, aivr_session_id=None, call_center_call_id=None, daily_repeat_calls=None, direction=None, dtmf_events=None, end_time=None, external_endpoint=None, internal_endpoint=None, language=None, markers=None, num_audio_channels=2, num_spk_channels=2, originating_call_id=None, queue=None, recording=None, start_time=None, tags=None, account_id=None, aivr_transfer_dest_type=None, call_id=None, call_resolved=None, context_id=None, cr_answers_id=None, duration=None, incidents=None, keywords=None, last_recompute_time=None, notes=None, progress_phase=None, recompute_phase=None, review_notes=None, review_status=None, sa_session_id=None, score=None, sentiment=None, spawned_calls=None, topics=None, version=1, word_cloud=None, headline=None, local_vars_configuration=None):  # noqa: E501
        """VoiceCallSearchResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._agent = None
        self._aivr_app_id = None
        self._aivr_session_id = None
        self._call_center_call_id = None
        self._daily_repeat_calls = None
        self._direction = None
        self._dtmf_events = None
        self._end_time = None
        self._external_endpoint = None
        self._internal_endpoint = None
        self._language = None
        self._markers = None
        self._num_audio_channels = None
        self._num_spk_channels = None
        self._originating_call_id = None
        self._queue = None
        self._recording = None
        self._start_time = None
        self._tags = None
        self._account_id = None
        self._aivr_transfer_dest_type = None
        self._call_id = None
        self._call_resolved = None
        self._context_id = None
        self._cr_answers_id = None
        self._duration = None
        self._incidents = None
        self._keywords = None
        self._last_recompute_time = None
        self._notes = None
        self._progress_phase = None
        self._recompute_phase = None
        self._review_notes = None
        self._review_status = None
        self._sa_session_id = None
        self._score = None
        self._sentiment = None
        self._spawned_calls = None
        self._topics = None
        self._version = None
        self._word_cloud = None
        self._headline = None
        self.discriminator = None

        if agent is not None:
            self.agent = agent
        if aivr_app_id is not None:
            self.aivr_app_id = aivr_app_id
        if aivr_session_id is not None:
            self.aivr_session_id = aivr_session_id
        if call_center_call_id is not None:
            self.call_center_call_id = call_center_call_id
        if daily_repeat_calls is not None:
            self.daily_repeat_calls = daily_repeat_calls
        if direction is not None:
            self.direction = direction
        if dtmf_events is not None:
            self.dtmf_events = dtmf_events
        if end_time is not None:
            self.end_time = end_time
        if external_endpoint is not None:
            self.external_endpoint = external_endpoint
        if internal_endpoint is not None:
            self.internal_endpoint = internal_endpoint
        if language is not None:
            self.language = language
        if markers is not None:
            self.markers = markers
        if num_audio_channels is not None:
            self.num_audio_channels = num_audio_channels
        if num_spk_channels is not None:
            self.num_spk_channels = num_spk_channels
        if originating_call_id is not None:
            self.originating_call_id = originating_call_id
        if queue is not None:
            self.queue = queue
        if recording is not None:
            self.recording = recording
        if start_time is not None:
            self.start_time = start_time
        if tags is not None:
            self.tags = tags
        if account_id is not None:
            self.account_id = account_id
        if aivr_transfer_dest_type is not None:
            self.aivr_transfer_dest_type = aivr_transfer_dest_type
        if call_id is not None:
            self.call_id = call_id
        if call_resolved is not None:
            self.call_resolved = call_resolved
        if context_id is not None:
            self.context_id = context_id
        if cr_answers_id is not None:
            self.cr_answers_id = cr_answers_id
        if duration is not None:
            self.duration = duration
        if incidents is not None:
            self.incidents = incidents
        if keywords is not None:
            self.keywords = keywords
        if last_recompute_time is not None:
            self.last_recompute_time = last_recompute_time
        if notes is not None:
            self.notes = notes
        if progress_phase is not None:
            self.progress_phase = progress_phase
        if recompute_phase is not None:
            self.recompute_phase = recompute_phase
        if review_notes is not None:
            self.review_notes = review_notes
        if review_status is not None:
            self.review_status = review_status
        if sa_session_id is not None:
            self.sa_session_id = sa_session_id
        if score is not None:
            self.score = score
        if sentiment is not None:
            self.sentiment = sentiment
        if spawned_calls is not None:
            self.spawned_calls = spawned_calls
        if topics is not None:
            self.topics = topics
        if version is not None:
            self.version = version
        if word_cloud is not None:
            self.word_cloud = word_cloud
        if headline is not None:
            self.headline = headline

    @property
    def agent(self):
        """Gets the agent of this VoiceCallSearchResult.  # noqa: E501


        :return: The agent of this VoiceCallSearchResult.  # noqa: E501
        :rtype: Agent
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this VoiceCallSearchResult.


        :param agent: The agent of this VoiceCallSearchResult.  # noqa: E501
        :type: Agent
        """

        self._agent = agent

    @property
    def aivr_app_id(self):
        """Gets the aivr_app_id of this VoiceCallSearchResult.  # noqa: E501

        Id of the AIVR application that handled the call. Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :return: The aivr_app_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._aivr_app_id

    @aivr_app_id.setter
    def aivr_app_id(self, aivr_app_id):
        """Sets the aivr_app_id of this VoiceCallSearchResult.

        Id of the AIVR application that handled the call. Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :param aivr_app_id: The aivr_app_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._aivr_app_id = aivr_app_id

    @property
    def aivr_session_id(self):
        """Gets the aivr_session_id of this VoiceCallSearchResult.  # noqa: E501

        Id of the AIVR session that handled the call. Will be absent if the call did not come from an AIVR Session.     # noqa: E501

        :return: The aivr_session_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._aivr_session_id

    @aivr_session_id.setter
    def aivr_session_id(self, aivr_session_id):
        """Sets the aivr_session_id of this VoiceCallSearchResult.

        Id of the AIVR session that handled the call. Will be absent if the call did not come from an AIVR Session.     # noqa: E501

        :param aivr_session_id: The aivr_session_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._aivr_session_id = aivr_session_id

    @property
    def call_center_call_id(self):
        """Gets the call_center_call_id of this VoiceCallSearchResult.  # noqa: E501

        Id of the call in the call center system, e.g., Aircall. </br>  This is used to correlate the call with the call center system.   # noqa: E501

        :return: The call_center_call_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._call_center_call_id

    @call_center_call_id.setter
    def call_center_call_id(self, call_center_call_id):
        """Sets the call_center_call_id of this VoiceCallSearchResult.

        Id of the call in the call center system, e.g., Aircall. </br>  This is used to correlate the call with the call center system.   # noqa: E501

        :param call_center_call_id: The call_center_call_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                call_center_call_id is not None and len(call_center_call_id) > 48):
            raise ValueError("Invalid value for `call_center_call_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                call_center_call_id is not None and len(call_center_call_id) < 1):
            raise ValueError("Invalid value for `call_center_call_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._call_center_call_id = call_center_call_id

    @property
    def daily_repeat_calls(self):
        """Gets the daily_repeat_calls of this VoiceCallSearchResult.  # noqa: E501

        Number of repeat calls. A repeat call is a call between the same `externalEndpoint` and the same `internalEndpoint` within a 24 hour window. We compute it while inserting the new call record - we do a count of other calls with the same endpoints in the period between `startTime` and `startTime - 24h`.  Note this is a repeat call count, so if there is only one call between the same endpoints within 24 hours then this will be 0.   # noqa: E501

        :return: The daily_repeat_calls of this VoiceCallSearchResult.  # noqa: E501
        :rtype: int
        """
        return self._daily_repeat_calls

    @daily_repeat_calls.setter
    def daily_repeat_calls(self, daily_repeat_calls):
        """Sets the daily_repeat_calls of this VoiceCallSearchResult.

        Number of repeat calls. A repeat call is a call between the same `externalEndpoint` and the same `internalEndpoint` within a 24 hour window. We compute it while inserting the new call record - we do a count of other calls with the same endpoints in the period between `startTime` and `startTime - 24h`.  Note this is a repeat call count, so if there is only one call between the same endpoints within 24 hours then this will be 0.   # noqa: E501

        :param daily_repeat_calls: The daily_repeat_calls of this VoiceCallSearchResult.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                daily_repeat_calls is not None and daily_repeat_calls < 0):  # noqa: E501
            raise ValueError("Invalid value for `daily_repeat_calls`, must be a value greater than or equal to `0`")  # noqa: E501

        self._daily_repeat_calls = daily_repeat_calls

    @property
    def direction(self):
        """Gets the direction of this VoiceCallSearchResult.  # noqa: E501

        direction of the call  # noqa: E501

        :return: The direction of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """Sets the direction of this VoiceCallSearchResult.

        direction of the call  # noqa: E501

        :param direction: The direction of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        allowed_values = ["inbound", "outbound"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and direction not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `direction` ({0}), must be one of {1}"  # noqa: E501
                .format(direction, allowed_values)
            )

        self._direction = direction

    @property
    def dtmf_events(self):
        """Gets the dtmf_events of this VoiceCallSearchResult.  # noqa: E501

        List of DTMF events detected in the call  # noqa: E501

        :return: The dtmf_events of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[DtmfEventWithChannel]
        """
        return self._dtmf_events

    @dtmf_events.setter
    def dtmf_events(self, dtmf_events):
        """Sets the dtmf_events of this VoiceCallSearchResult.

        List of DTMF events detected in the call  # noqa: E501

        :param dtmf_events: The dtmf_events of this VoiceCallSearchResult.  # noqa: E501
        :type: list[DtmfEventWithChannel]
        """

        self._dtmf_events = dtmf_events

    @property
    def end_time(self):
        """Gets the end_time of this VoiceCallSearchResult.  # noqa: E501

        end time of the call (UTC)  # noqa: E501

        :return: The end_time of this VoiceCallSearchResult.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this VoiceCallSearchResult.

        end time of the call (UTC)  # noqa: E501

        :param end_time: The end_time of this VoiceCallSearchResult.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def external_endpoint(self):
        """Gets the external_endpoint of this VoiceCallSearchResult.  # noqa: E501

        Caller (for inbound) or callee (for outbound) identifier. For phone calls it will be a caller id (ANI) in E.164 format. For WebRTC it will be some TBD identifier.   # noqa: E501

        :return: The external_endpoint of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._external_endpoint

    @external_endpoint.setter
    def external_endpoint(self, external_endpoint):
        """Sets the external_endpoint of this VoiceCallSearchResult.

        Caller (for inbound) or callee (for outbound) identifier. For phone calls it will be a caller id (ANI) in E.164 format. For WebRTC it will be some TBD identifier.   # noqa: E501

        :param external_endpoint: The external_endpoint of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._external_endpoint = external_endpoint

    @property
    def internal_endpoint(self):
        """Gets the internal_endpoint of this VoiceCallSearchResult.  # noqa: E501

        Identifier of the internal endpoint that received inbound call or originated outbound call. For phone calls it will be DNIS or caller id. For WebRTC it will be some TBD identifier.   # noqa: E501

        :return: The internal_endpoint of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._internal_endpoint

    @internal_endpoint.setter
    def internal_endpoint(self, internal_endpoint):
        """Sets the internal_endpoint of this VoiceCallSearchResult.

        Identifier of the internal endpoint that received inbound call or originated outbound call. For phone calls it will be DNIS or caller id. For WebRTC it will be some TBD identifier.   # noqa: E501

        :param internal_endpoint: The internal_endpoint of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._internal_endpoint = internal_endpoint

    @property
    def language(self):
        """Gets the language of this VoiceCallSearchResult.  # noqa: E501


        :return: The language of this VoiceCallSearchResult.  # noqa: E501
        :rtype: Language
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this VoiceCallSearchResult.


        :param language: The language of this VoiceCallSearchResult.  # noqa: E501
        :type: Language
        """

        self._language = language

    @property
    def markers(self):
        """Gets the markers of this VoiceCallSearchResult.  # noqa: E501

        Call timeline markers attached to the call  # noqa: E501

        :return: The markers of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[CallMarker]
        """
        return self._markers

    @markers.setter
    def markers(self, markers):
        """Sets the markers of this VoiceCallSearchResult.

        Call timeline markers attached to the call  # noqa: E501

        :param markers: The markers of this VoiceCallSearchResult.  # noqa: E501
        :type: list[CallMarker]
        """

        self._markers = markers

    @property
    def num_audio_channels(self):
        """Gets the num_audio_channels of this VoiceCallSearchResult.  # noqa: E501

        Number of audio channels in the `recording`. 1 is mono, 2 is stereo  # noqa: E501

        :return: The num_audio_channels of this VoiceCallSearchResult.  # noqa: E501
        :rtype: int
        """
        return self._num_audio_channels

    @num_audio_channels.setter
    def num_audio_channels(self, num_audio_channels):
        """Sets the num_audio_channels of this VoiceCallSearchResult.

        Number of audio channels in the `recording`. 1 is mono, 2 is stereo  # noqa: E501

        :param num_audio_channels: The num_audio_channels of this VoiceCallSearchResult.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                num_audio_channels is not None and num_audio_channels > 2):  # noqa: E501
            raise ValueError("Invalid value for `num_audio_channels`, must be a value less than or equal to `2`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                num_audio_channels is not None and num_audio_channels < 1):  # noqa: E501
            raise ValueError("Invalid value for `num_audio_channels`, must be a value greater than or equal to `1`")  # noqa: E501

        self._num_audio_channels = num_audio_channels

    @property
    def num_spk_channels(self):
        """Gets the num_spk_channels of this VoiceCallSearchResult.  # noqa: E501

        Number of speaker channels in the `recording`. 1 means that there is only one speaker, 2 means that there are 2 speakers. Note that: + if `numSpkChannels` is 1 then we will need to mix the recording down to mono if `numAudioChannels` is 2 (that is not a normal scenario) + if `numSpkChannels` is 2 then we will need to use diarization if `numAudioChannels` is 1   # noqa: E501

        :return: The num_spk_channels of this VoiceCallSearchResult.  # noqa: E501
        :rtype: int
        """
        return self._num_spk_channels

    @num_spk_channels.setter
    def num_spk_channels(self, num_spk_channels):
        """Sets the num_spk_channels of this VoiceCallSearchResult.

        Number of speaker channels in the `recording`. 1 means that there is only one speaker, 2 means that there are 2 speakers. Note that: + if `numSpkChannels` is 1 then we will need to mix the recording down to mono if `numAudioChannels` is 2 (that is not a normal scenario) + if `numSpkChannels` is 2 then we will need to use diarization if `numAudioChannels` is 1   # noqa: E501

        :param num_spk_channels: The num_spk_channels of this VoiceCallSearchResult.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                num_spk_channels is not None and num_spk_channels > 2):  # noqa: E501
            raise ValueError("Invalid value for `num_spk_channels`, must be a value less than or equal to `2`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                num_spk_channels is not None and num_spk_channels < 1):  # noqa: E501
            raise ValueError("Invalid value for `num_spk_channels`, must be a value greater than or equal to `1`")  # noqa: E501

        self._num_spk_channels = num_spk_channels

    @property
    def originating_call_id(self):
        """Gets the originating_call_id of this VoiceCallSearchResult.  # noqa: E501

        Id of the originating call.  For now this applies in scenario of a Warm Call Transfer. The call that launched the warm transfer will be the originating call.   # noqa: E501

        :return: The originating_call_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._originating_call_id

    @originating_call_id.setter
    def originating_call_id(self, originating_call_id):
        """Sets the originating_call_id of this VoiceCallSearchResult.

        Id of the originating call.  For now this applies in scenario of a Warm Call Transfer. The call that launched the warm transfer will be the originating call.   # noqa: E501

        :param originating_call_id: The originating_call_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                originating_call_id is not None and len(originating_call_id) > 48):
            raise ValueError("Invalid value for `originating_call_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                originating_call_id is not None and len(originating_call_id) < 1):
            raise ValueError("Invalid value for `originating_call_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._originating_call_id = originating_call_id

    @property
    def queue(self):
        """Gets the queue of this VoiceCallSearchResult.  # noqa: E501


        :return: The queue of this VoiceCallSearchResult.  # noqa: E501
        :rtype: Queue
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this VoiceCallSearchResult.


        :param queue: The queue of this VoiceCallSearchResult.  # noqa: E501
        :type: Queue
        """

        self._queue = queue

    @property
    def recording(self):
        """Gets the recording of this VoiceCallSearchResult.  # noqa: E501

        Data UUID - reference to original call recording in Voicegain Data Store.  # noqa: E501

        :return: The recording of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._recording

    @recording.setter
    def recording(self, recording):
        """Sets the recording of this VoiceCallSearchResult.

        Data UUID - reference to original call recording in Voicegain Data Store.  # noqa: E501

        :param recording: The recording of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._recording = recording

    @property
    def start_time(self):
        """Gets the start_time of this VoiceCallSearchResult.  # noqa: E501

        start time of the call (UTC)  # noqa: E501

        :return: The start_time of this VoiceCallSearchResult.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this VoiceCallSearchResult.

        start time of the call (UTC)  # noqa: E501

        :param start_time: The start_time of this VoiceCallSearchResult.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def tags(self):
        """Gets the tags of this VoiceCallSearchResult.  # noqa: E501

        Tags attached to the call  # noqa: E501

        :return: The tags of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this VoiceCallSearchResult.

        Tags attached to the call  # noqa: E501

        :param tags: The tags of this VoiceCallSearchResult.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def account_id(self):
        """Gets the account_id of this VoiceCallSearchResult.  # noqa: E501

        Voicegain Account  # noqa: E501

        :return: The account_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this VoiceCallSearchResult.

        Voicegain Account  # noqa: E501

        :param account_id: The account_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                account_id is not None and len(account_id) > 48):
            raise ValueError("Invalid value for `account_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                account_id is not None and len(account_id) < 16):
            raise ValueError("Invalid value for `account_id`, length must be greater than or equal to `16`")  # noqa: E501

        self._account_id = account_id

    @property
    def aivr_transfer_dest_type(self):
        """Gets the aivr_transfer_dest_type of this VoiceCallSearchResult.  # noqa: E501

        Short string describing the type of destination for the AIVR transfer. Will be absent if the call did not come from an AIVR App. Example values are: + Internal - if the transfer was done to internal call center + Agency - if the transfer was done to an external agency   # noqa: E501

        :return: The aivr_transfer_dest_type of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._aivr_transfer_dest_type

    @aivr_transfer_dest_type.setter
    def aivr_transfer_dest_type(self, aivr_transfer_dest_type):
        """Sets the aivr_transfer_dest_type of this VoiceCallSearchResult.

        Short string describing the type of destination for the AIVR transfer. Will be absent if the call did not come from an AIVR App. Example values are: + Internal - if the transfer was done to internal call center + Agency - if the transfer was done to an external agency   # noqa: E501

        :param aivr_transfer_dest_type: The aivr_transfer_dest_type of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                aivr_transfer_dest_type is not None and len(aivr_transfer_dest_type) > 32):
            raise ValueError("Invalid value for `aivr_transfer_dest_type`, length must be less than or equal to `32`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                aivr_transfer_dest_type is not None and len(aivr_transfer_dest_type) < 1):
            raise ValueError("Invalid value for `aivr_transfer_dest_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._aivr_transfer_dest_type = aivr_transfer_dest_type

    @property
    def call_id(self):
        """Gets the call_id of this VoiceCallSearchResult.  # noqa: E501

        Unique Id of the call  # noqa: E501

        :return: The call_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._call_id

    @call_id.setter
    def call_id(self, call_id):
        """Sets the call_id of this VoiceCallSearchResult.

        Unique Id of the call  # noqa: E501

        :param call_id: The call_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                call_id is not None and len(call_id) > 48):
            raise ValueError("Invalid value for `call_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                call_id is not None and len(call_id) < 1):
            raise ValueError("Invalid value for `call_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._call_id = call_id

    @property
    def call_resolved(self):
        """Gets the call_resolved of this VoiceCallSearchResult.  # noqa: E501

        Set to true if Call Review determined that the call successfully resolved/handled the problem/issues of the call.  # noqa: E501

        :return: The call_resolved of this VoiceCallSearchResult.  # noqa: E501
        :rtype: bool
        """
        return self._call_resolved

    @call_resolved.setter
    def call_resolved(self, call_resolved):
        """Sets the call_resolved of this VoiceCallSearchResult.

        Set to true if Call Review determined that the call successfully resolved/handled the problem/issues of the call.  # noqa: E501

        :param call_resolved: The call_resolved of this VoiceCallSearchResult.  # noqa: E501
        :type: bool
        """

        self._call_resolved = call_resolved

    @property
    def context_id(self):
        """Gets the context_id of this VoiceCallSearchResult.  # noqa: E501

        Voicegain Account Context  # noqa: E501

        :return: The context_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._context_id

    @context_id.setter
    def context_id(self, context_id):
        """Sets the context_id of this VoiceCallSearchResult.

        Voicegain Account Context  # noqa: E501

        :param context_id: The context_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                context_id is not None and len(context_id) > 48):
            raise ValueError("Invalid value for `context_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                context_id is not None and len(context_id) < 16):
            raise ValueError("Invalid value for `context_id`, length must be greater than or equal to `16`")  # noqa: E501

        self._context_id = context_id

    @property
    def cr_answers_id(self):
        """Gets the cr_answers_id of this VoiceCallSearchResult.  # noqa: E501

        unique id referencing the call review answers - these are initially populated by speech analytics  # noqa: E501

        :return: The cr_answers_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._cr_answers_id

    @cr_answers_id.setter
    def cr_answers_id(self, cr_answers_id):
        """Sets the cr_answers_id of this VoiceCallSearchResult.

        unique id referencing the call review answers - these are initially populated by speech analytics  # noqa: E501

        :param cr_answers_id: The cr_answers_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                cr_answers_id is not None and len(cr_answers_id) > 48):
            raise ValueError("Invalid value for `cr_answers_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                cr_answers_id is not None and len(cr_answers_id) < 16):
            raise ValueError("Invalid value for `cr_answers_id`, length must be greater than or equal to `16`")  # noqa: E501

        self._cr_answers_id = cr_answers_id

    @property
    def duration(self):
        """Gets the duration of this VoiceCallSearchResult.  # noqa: E501

        duration of the call in seconds  # noqa: E501

        :return: The duration of this VoiceCallSearchResult.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this VoiceCallSearchResult.

        duration of the call in seconds  # noqa: E501

        :param duration: The duration of this VoiceCallSearchResult.  # noqa: E501
        :type: int
        """

        self._duration = duration

    @property
    def incidents(self):
        """Gets the incidents of this VoiceCallSearchResult.  # noqa: E501

        Number of silence and overtalk incidents on a call  # noqa: E501

        :return: The incidents of this VoiceCallSearchResult.  # noqa: E501
        :rtype: float
        """
        return self._incidents

    @incidents.setter
    def incidents(self, incidents):
        """Sets the incidents of this VoiceCallSearchResult.

        Number of silence and overtalk incidents on a call  # noqa: E501

        :param incidents: The incidents of this VoiceCallSearchResult.  # noqa: E501
        :type: float
        """

        self._incidents = incidents

    @property
    def keywords(self):
        """Gets the keywords of this VoiceCallSearchResult.  # noqa: E501

        All keywords detected in the call. Complete set of keywords and all details can be retrieved using `saSessionId`   # noqa: E501

        :return: The keywords of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """Sets the keywords of this VoiceCallSearchResult.

        All keywords detected in the call. Complete set of keywords and all details can be retrieved using `saSessionId`   # noqa: E501

        :param keywords: The keywords of this VoiceCallSearchResult.  # noqa: E501
        :type: list[str]
        """

        self._keywords = keywords

    @property
    def last_recompute_time(self):
        """Gets the last_recompute_time of this VoiceCallSearchResult.  # noqa: E501

        finish time of the last recompute (UTC)  # noqa: E501

        :return: The last_recompute_time of this VoiceCallSearchResult.  # noqa: E501
        :rtype: datetime
        """
        return self._last_recompute_time

    @last_recompute_time.setter
    def last_recompute_time(self, last_recompute_time):
        """Sets the last_recompute_time of this VoiceCallSearchResult.

        finish time of the last recompute (UTC)  # noqa: E501

        :param last_recompute_time: The last_recompute_time of this VoiceCallSearchResult.  # noqa: E501
        :type: datetime
        """

        self._last_recompute_time = last_recompute_time

    @property
    def notes(self):
        """Gets the notes of this VoiceCallSearchResult.  # noqa: E501

        Brief notes about the call. Will often be also submitted to the CRM.</br> Can be generated by copilot logic using LLM. May also be entered and/or modified by an Agent.   # noqa: E501

        :return: The notes of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this VoiceCallSearchResult.

        Brief notes about the call. Will often be also submitted to the CRM.</br> Can be generated by copilot logic using LLM. May also be entered and/or modified by an Agent.   # noqa: E501

        :param notes: The notes of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._notes = notes

    @property
    def progress_phase(self):
        """Gets the progress_phase of this VoiceCallSearchResult.  # noqa: E501


        :return: The progress_phase of this VoiceCallSearchResult.  # noqa: E501
        :rtype: ProgressPhase
        """
        return self._progress_phase

    @progress_phase.setter
    def progress_phase(self, progress_phase):
        """Sets the progress_phase of this VoiceCallSearchResult.


        :param progress_phase: The progress_phase of this VoiceCallSearchResult.  # noqa: E501
        :type: ProgressPhase
        """

        self._progress_phase = progress_phase

    @property
    def recompute_phase(self):
        """Gets the recompute_phase of this VoiceCallSearchResult.  # noqa: E501

        Phase of the recompute process. Recompute uses existing transcript to recompute things like sentiment, keywords, etc. Also is used to reapply PII redaction to text and audio. + `requested` - recompute has been requested + `queued` - recompute is in the queue (ready to be processed) + `processing` - recompute is being processed + `completed` - recompute has been completed + `error` - recompute has failed   # noqa: E501

        :return: The recompute_phase of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._recompute_phase

    @recompute_phase.setter
    def recompute_phase(self, recompute_phase):
        """Sets the recompute_phase of this VoiceCallSearchResult.

        Phase of the recompute process. Recompute uses existing transcript to recompute things like sentiment, keywords, etc. Also is used to reapply PII redaction to text and audio. + `requested` - recompute has been requested + `queued` - recompute is in the queue (ready to be processed) + `processing` - recompute is being processed + `completed` - recompute has been completed + `error` - recompute has failed   # noqa: E501

        :param recompute_phase: The recompute_phase of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        allowed_values = ["requested", "queued", "processing", "completed", "error"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and recompute_phase not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `recompute_phase` ({0}), must be one of {1}"  # noqa: E501
                .format(recompute_phase, allowed_values)
            )

        self._recompute_phase = recompute_phase

    @property
    def review_notes(self):
        """Gets the review_notes of this VoiceCallSearchResult.  # noqa: E501

        Notes about the call taken during a review.</br> TODO: make them structured   # noqa: E501

        :return: The review_notes of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._review_notes

    @review_notes.setter
    def review_notes(self, review_notes):
        """Sets the review_notes of this VoiceCallSearchResult.

        Notes about the call taken during a review.</br> TODO: make them structured   # noqa: E501

        :param review_notes: The review_notes of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._review_notes = review_notes

    @property
    def review_status(self):
        """Gets the review_status of this VoiceCallSearchResult.  # noqa: E501

        Call goes through 5 human review stages: + `selected` to be reviewed + `reviewed` i.e. notes complete + Notes are `communicated` to the agent + Agent `viewed` the notes + Agent `acknowledged` the notes  If reviewStatus is missing or null then the call has not been selected for review.   # noqa: E501

        :return: The review_status of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._review_status

    @review_status.setter
    def review_status(self, review_status):
        """Sets the review_status of this VoiceCallSearchResult.

        Call goes through 5 human review stages: + `selected` to be reviewed + `reviewed` i.e. notes complete + Notes are `communicated` to the agent + Agent `viewed` the notes + Agent `acknowledged` the notes  If reviewStatus is missing or null then the call has not been selected for review.   # noqa: E501

        :param review_status: The review_status of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """
        allowed_values = ["selected", "reviewed", "communicated", "viewed", "acknowledged"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and review_status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `review_status` ({0}), must be one of {1}"  # noqa: E501
                .format(review_status, allowed_values)
            )

        self._review_status = review_status

    @property
    def sa_session_id(self):
        """Gets the sa_session_id of this VoiceCallSearchResult.  # noqa: E501

        Reference to Speech Analytics session. Can be used to retrieve the Speech Analytics data (which in turn has references to audio and transcripts).    # noqa: E501

        :return: The sa_session_id of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._sa_session_id

    @sa_session_id.setter
    def sa_session_id(self, sa_session_id):
        """Sets the sa_session_id of this VoiceCallSearchResult.

        Reference to Speech Analytics session. Can be used to retrieve the Speech Analytics data (which in turn has references to audio and transcripts).    # noqa: E501

        :param sa_session_id: The sa_session_id of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._sa_session_id = sa_session_id

    @property
    def score(self):
        """Gets the score of this VoiceCallSearchResult.  # noqa: E501

        Call score - computed from Call Review  # noqa: E501

        :return: The score of this VoiceCallSearchResult.  # noqa: E501
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this VoiceCallSearchResult.

        Call score - computed from Call Review  # noqa: E501

        :param score: The score of this VoiceCallSearchResult.  # noqa: E501
        :type: float
        """

        self._score = score

    @property
    def sentiment(self):
        """Gets the sentiment of this VoiceCallSearchResult.  # noqa: E501

        Computed call sentiment value  # noqa: E501

        :return: The sentiment of this VoiceCallSearchResult.  # noqa: E501
        :rtype: float
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """Sets the sentiment of this VoiceCallSearchResult.

        Computed call sentiment value  # noqa: E501

        :param sentiment: The sentiment of this VoiceCallSearchResult.  # noqa: E501
        :type: float
        """

        self._sentiment = sentiment

    @property
    def spawned_calls(self):
        """Gets the spawned_calls of this VoiceCallSearchResult.  # noqa: E501

        List of callIds of calls that were spawned from this call. This is used in scenarios of Warm Call Transfer. Currently we only have 1 single warm transfer call per originating call, but in the future we may have multiple.    # noqa: E501

        :return: The spawned_calls of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._spawned_calls

    @spawned_calls.setter
    def spawned_calls(self, spawned_calls):
        """Sets the spawned_calls of this VoiceCallSearchResult.

        List of callIds of calls that were spawned from this call. This is used in scenarios of Warm Call Transfer. Currently we only have 1 single warm transfer call per originating call, but in the future we may have multiple.    # noqa: E501

        :param spawned_calls: The spawned_calls of this VoiceCallSearchResult.  # noqa: E501
        :type: list[str]
        """

        self._spawned_calls = spawned_calls

    @property
    def topics(self):
        """Gets the topics of this VoiceCallSearchResult.  # noqa: E501

        All topics discovered from the call. Complete set of topics and all details can be retrieved using `saSessionId`   # noqa: E501

        :return: The topics of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[str]
        """
        return self._topics

    @topics.setter
    def topics(self, topics):
        """Sets the topics of this VoiceCallSearchResult.

        All topics discovered from the call. Complete set of topics and all details can be retrieved using `saSessionId`   # noqa: E501

        :param topics: The topics of this VoiceCallSearchResult.  # noqa: E501
        :type: list[str]
        """

        self._topics = topics

    @property
    def version(self):
        """Gets the version of this VoiceCallSearchResult.  # noqa: E501

        Version of the call. Version 1 uses `/sa` API for processing audio and version 2 uses `/sa/offline` API.  # noqa: E501

        :return: The version of this VoiceCallSearchResult.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this VoiceCallSearchResult.

        Version of the call. Version 1 uses `/sa` API for processing audio and version 2 uses `/sa/offline` API.  # noqa: E501

        :param version: The version of this VoiceCallSearchResult.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                version is not None and version > 2):  # noqa: E501
            raise ValueError("Invalid value for `version`, must be a value less than or equal to `2`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                version is not None and version < 1):  # noqa: E501
            raise ValueError("Invalid value for `version`, must be a value greater than or equal to `1`")  # noqa: E501

        self._version = version

    @property
    def word_cloud(self):
        """Gets the word_cloud of this VoiceCallSearchResult.  # noqa: E501

        Top 100 words from the transcript with their frequencies. Complete wordcloud can be retrieved using `saSessionId`   # noqa: E501

        :return: The word_cloud of this VoiceCallSearchResult.  # noqa: E501
        :rtype: list[WordCloudItem]
        """
        return self._word_cloud

    @word_cloud.setter
    def word_cloud(self, word_cloud):
        """Sets the word_cloud of this VoiceCallSearchResult.

        Top 100 words from the transcript with their frequencies. Complete wordcloud can be retrieved using `saSessionId`   # noqa: E501

        :param word_cloud: The word_cloud of this VoiceCallSearchResult.  # noqa: E501
        :type: list[WordCloudItem]
        """

        self._word_cloud = word_cloud

    @property
    def headline(self):
        """Gets the headline of this VoiceCallSearchResult.  # noqa: E501

        sample from the cal transcript that matches the query  # noqa: E501

        :return: The headline of this VoiceCallSearchResult.  # noqa: E501
        :rtype: str
        """
        return self._headline

    @headline.setter
    def headline(self, headline):
        """Sets the headline of this VoiceCallSearchResult.

        sample from the cal transcript that matches the query  # noqa: E501

        :param headline: The headline of this VoiceCallSearchResult.  # noqa: E501
        :type: str
        """

        self._headline = headline

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
        if not isinstance(other, VoiceCallSearchResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VoiceCallSearchResult):
            return True

        return self.to_dict() != other.to_dict()
