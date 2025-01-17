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


class SpeechAnalyticsConfigModifiable(object):
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
        'age': 'bool',
        'call_resolution_criteria': 'list[str]',
        'call_resolution_question_id': 'str',
        'competitor_keyword_groups': 'list[str]',
        'context_id': 'str',
        'criteria': 'list[CriterionConfig]',
        'entities': 'list[NamedEntityType]',
        'gender': 'bool',
        'keyword_groups': 'list[KeywordSpotGroup]',
        'keywords': 'list[KeywordSpotItem]',
        'llm_copilot_notes_prompt': 'str',
        'llm_summary_prompt': 'str',
        'meeting_minutes': 'SpeechAnalyticsConfigModifiableBaseMeetingMinutes',
        'moods': 'list[MoodType]',
        'overtalk_single_duration_maximum_threshold': 'float',
        'overtalk_total_percentage_threshold': 'float',
        'phrase_groups': 'list[PhraseSpotGroup]',
        'phrases': 'list[PhraseSpotItem]',
        'pii_redaction': 'list[PIIRedactionConf]',
        'profanity': 'bool',
        'published': 'bool',
        'sentiment': 'bool',
        'silence_single_duration_maximum_threshold': 'float',
        'silence_total_percentage_threshold': 'float',
        'summary': 'bool',
        'word_cloud': 'bool',
        'name': 'str'
    }

    attribute_map = {
        'age': 'age',
        'call_resolution_criteria': 'callResolutionCriteria',
        'call_resolution_question_id': 'callResolutionQuestionId',
        'competitor_keyword_groups': 'competitorKeywordGroups',
        'context_id': 'contextId',
        'criteria': 'criteria',
        'entities': 'entities',
        'gender': 'gender',
        'keyword_groups': 'keywordGroups',
        'keywords': 'keywords',
        'llm_copilot_notes_prompt': 'llmCopilotNotesPrompt',
        'llm_summary_prompt': 'llmSummaryPrompt',
        'meeting_minutes': 'meetingMinutes',
        'moods': 'moods',
        'overtalk_single_duration_maximum_threshold': 'overtalkSingleDurationMaximumThreshold',
        'overtalk_total_percentage_threshold': 'overtalkTotalPercentageThreshold',
        'phrase_groups': 'phraseGroups',
        'phrases': 'phrases',
        'pii_redaction': 'piiRedaction',
        'profanity': 'profanity',
        'published': 'published',
        'sentiment': 'sentiment',
        'silence_single_duration_maximum_threshold': 'silenceSingleDurationMaximumThreshold',
        'silence_total_percentage_threshold': 'silenceTotalPercentageThreshold',
        'summary': 'summary',
        'word_cloud': 'wordCloud',
        'name': 'name'
    }

    def __init__(self, age=False, call_resolution_criteria=None, call_resolution_question_id=None, competitor_keyword_groups=None, context_id=None, criteria=None, entities=None, gender=False, keyword_groups=None, keywords=None, llm_copilot_notes_prompt='Generate brief notes for the record of this call in the CRM.', llm_summary_prompt='Generate a one-sentence summary of the call.', meeting_minutes=None, moods=None, overtalk_single_duration_maximum_threshold=1000, overtalk_total_percentage_threshold=2.5, phrase_groups=None, phrases=None, pii_redaction=None, profanity=False, published=False, sentiment=False, silence_single_duration_maximum_threshold=10000, silence_total_percentage_threshold=10.0, summary=False, word_cloud=False, name=None, local_vars_configuration=None):  # noqa: E501
        """SpeechAnalyticsConfigModifiable - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._age = None
        self._call_resolution_criteria = None
        self._call_resolution_question_id = None
        self._competitor_keyword_groups = None
        self._context_id = None
        self._criteria = None
        self._entities = None
        self._gender = None
        self._keyword_groups = None
        self._keywords = None
        self._llm_copilot_notes_prompt = None
        self._llm_summary_prompt = None
        self._meeting_minutes = None
        self._moods = None
        self._overtalk_single_duration_maximum_threshold = None
        self._overtalk_total_percentage_threshold = None
        self._phrase_groups = None
        self._phrases = None
        self._pii_redaction = None
        self._profanity = None
        self._published = None
        self._sentiment = None
        self._silence_single_duration_maximum_threshold = None
        self._silence_total_percentage_threshold = None
        self._summary = None
        self._word_cloud = None
        self._name = None
        self.discriminator = None

        if age is not None:
            self.age = age
        if call_resolution_criteria is not None:
            self.call_resolution_criteria = call_resolution_criteria
        if call_resolution_question_id is not None:
            self.call_resolution_question_id = call_resolution_question_id
        if competitor_keyword_groups is not None:
            self.competitor_keyword_groups = competitor_keyword_groups
        if context_id is not None:
            self.context_id = context_id
        if criteria is not None:
            self.criteria = criteria
        if entities is not None:
            self.entities = entities
        if gender is not None:
            self.gender = gender
        if keyword_groups is not None:
            self.keyword_groups = keyword_groups
        if keywords is not None:
            self.keywords = keywords
        if llm_copilot_notes_prompt is not None:
            self.llm_copilot_notes_prompt = llm_copilot_notes_prompt
        if llm_summary_prompt is not None:
            self.llm_summary_prompt = llm_summary_prompt
        if meeting_minutes is not None:
            self.meeting_minutes = meeting_minutes
        if moods is not None:
            self.moods = moods
        if overtalk_single_duration_maximum_threshold is not None:
            self.overtalk_single_duration_maximum_threshold = overtalk_single_duration_maximum_threshold
        if overtalk_total_percentage_threshold is not None:
            self.overtalk_total_percentage_threshold = overtalk_total_percentage_threshold
        if phrase_groups is not None:
            self.phrase_groups = phrase_groups
        if phrases is not None:
            self.phrases = phrases
        if pii_redaction is not None:
            self.pii_redaction = pii_redaction
        if profanity is not None:
            self.profanity = profanity
        if published is not None:
            self.published = published
        if sentiment is not None:
            self.sentiment = sentiment
        if silence_single_duration_maximum_threshold is not None:
            self.silence_single_duration_maximum_threshold = silence_single_duration_maximum_threshold
        if silence_total_percentage_threshold is not None:
            self.silence_total_percentage_threshold = silence_total_percentage_threshold
        if summary is not None:
            self.summary = summary
        if word_cloud is not None:
            self.word_cloud = word_cloud
        if name is not None:
            self.name = name

    @property
    def age(self):
        """Gets the age of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(future functionality)_ Set to true to enable speaker age estimation  # noqa: E501

        :return: The age of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._age

    @age.setter
    def age(self, age):
        """Sets the age of this SpeechAnalyticsConfigModifiable.

        _(future functionality)_ Set to true to enable speaker age estimation  # noqa: E501

        :param age: The age of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._age = age

    @property
    def call_resolution_criteria(self):
        """Gets the call_resolution_criteria of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(beta)_  list of tags of the Criteria used to determine if the call was resolved. If *any* of these criteria are satisfied then the call will be considered as resolved.   # noqa: E501

        :return: The call_resolution_criteria of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[str]
        """
        return self._call_resolution_criteria

    @call_resolution_criteria.setter
    def call_resolution_criteria(self, call_resolution_criteria):
        """Sets the call_resolution_criteria of this SpeechAnalyticsConfigModifiable.

        _(beta)_  list of tags of the Criteria used to determine if the call was resolved. If *any* of these criteria are satisfied then the call will be considered as resolved.   # noqa: E501

        :param call_resolution_criteria: The call_resolution_criteria of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[str]
        """

        self._call_resolution_criteria = call_resolution_criteria

    @property
    def call_resolution_question_id(self):
        """Gets the call_resolution_question_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(beta)_ id of the `crQuestionId` in Call Review that identifies question and answer regarding Call Resolution  # noqa: E501

        :return: The call_resolution_question_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._call_resolution_question_id

    @call_resolution_question_id.setter
    def call_resolution_question_id(self, call_resolution_question_id):
        """Sets the call_resolution_question_id of this SpeechAnalyticsConfigModifiable.

        _(beta)_ id of the `crQuestionId` in Call Review that identifies question and answer regarding Call Resolution  # noqa: E501

        :param call_resolution_question_id: The call_resolution_question_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                call_resolution_question_id is not None and len(call_resolution_question_id) > 48):
            raise ValueError("Invalid value for `call_resolution_question_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                call_resolution_question_id is not None and len(call_resolution_question_id) < 16):
            raise ValueError("Invalid value for `call_resolution_question_id`, length must be greater than or equal to `16`")  # noqa: E501

        self._call_resolution_question_id = call_resolution_question_id

    @property
    def competitor_keyword_groups(self):
        """Gets the competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(internal use - for Speech Analytics UI)_ Set of one or more keyword group tags that should be interpreted as identifying competitor mentions.    # noqa: E501

        :return: The competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[str]
        """
        return self._competitor_keyword_groups

    @competitor_keyword_groups.setter
    def competitor_keyword_groups(self, competitor_keyword_groups):
        """Sets the competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.

        _(internal use - for Speech Analytics UI)_ Set of one or more keyword group tags that should be interpreted as identifying competitor mentions.    # noqa: E501

        :param competitor_keyword_groups: The competitor_keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[str]
        """

        self._competitor_keyword_groups = competitor_keyword_groups

    @property
    def context_id(self):
        """Gets the context_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        (Needed only if making a request using MAC Authentication. Otherwise will be taken from JWT.)  # noqa: E501

        :return: The context_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._context_id

    @context_id.setter
    def context_id(self, context_id):
        """Sets the context_id of this SpeechAnalyticsConfigModifiable.

        (Needed only if making a request using MAC Authentication. Otherwise will be taken from JWT.)  # noqa: E501

        :param context_id: The context_id of this SpeechAnalyticsConfigModifiable.  # noqa: E501
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
    def criteria(self):
        """Gets the criteria of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Criteria to be detected</br> Each Criterion cofiguration contains a list of SubCriteria that need to be satisfied.  **All** SubCriteria within the list must be satisfied for the list to return true.</br> Empty SubCriteria list is considered true (satisfies all SubCriteria).</br> Within each SubCriteria all __specified__ properties must return true for the SubCriteria to be true (AND). Except for `dialogElements` all properties are assumed to must match within the same sentence.   # noqa: E501

        :return: The criteria of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[CriterionConfig]
        """
        return self._criteria

    @criteria.setter
    def criteria(self, criteria):
        """Sets the criteria of this SpeechAnalyticsConfigModifiable.

        Criteria to be detected</br> Each Criterion cofiguration contains a list of SubCriteria that need to be satisfied.  **All** SubCriteria within the list must be satisfied for the list to return true.</br> Empty SubCriteria list is considered true (satisfies all SubCriteria).</br> Within each SubCriteria all __specified__ properties must return true for the SubCriteria to be true (AND). Except for `dialogElements` all properties are assumed to must match within the same sentence.   # noqa: E501

        :param criteria: The criteria of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[CriterionConfig]
        """

        self._criteria = criteria

    @property
    def entities(self):
        """Gets the entities of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Selection of Named Entity types to detect. </br> Entities are different from keywords in that an entity may have a large number of possible values  which do not have to be enumerated in order to be detected. </br> Types of Named Entities: + ADDRESS - Postal address. + CARDINAL - Numerals that do not fall under another type. + CC - Credit Card + CVV - Credit Card CVV + DATE - Absolute or relative dates or periods. + DMY - Full date including all of day, month and year.           + EMAIL - Email address + EVENT - Named hurricanes, battles, wars, sports events, etc. + FAC - Buildings, airports, highways, bridges, etc. + GPE - Countries, cities, states. + LANGUAGE - Any named language. + LAW - Named documents made into laws. + NORP - Nationalities or religious or political groups. + MONEY - Monetary values, including unit. + ORDINAL - \"first\", \"second\", etc. + ORG - Companies, agencies, institutions, etc. + PERCENT - Percentage, including \"%\". + PERSON - People, including fictional. + PHONE - Phone number. + PRODUCT - Objects, vehicles, foods, etc. (Not services.) + QUANTITY - Measurements, as of weight or distance. + SSN - Social Security number + TIME - Times smaller than a day. + WORK_OF_ART - Titles of books, songs, etc. + ZIP - Zip Code (if not part of an Address)  Default is no NERs selected.    # noqa: E501

        :return: The entities of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[NamedEntityType]
        """
        return self._entities

    @entities.setter
    def entities(self, entities):
        """Sets the entities of this SpeechAnalyticsConfigModifiable.

        Selection of Named Entity types to detect. </br> Entities are different from keywords in that an entity may have a large number of possible values  which do not have to be enumerated in order to be detected. </br> Types of Named Entities: + ADDRESS - Postal address. + CARDINAL - Numerals that do not fall under another type. + CC - Credit Card + CVV - Credit Card CVV + DATE - Absolute or relative dates or periods. + DMY - Full date including all of day, month and year.           + EMAIL - Email address + EVENT - Named hurricanes, battles, wars, sports events, etc. + FAC - Buildings, airports, highways, bridges, etc. + GPE - Countries, cities, states. + LANGUAGE - Any named language. + LAW - Named documents made into laws. + NORP - Nationalities or religious or political groups. + MONEY - Monetary values, including unit. + ORDINAL - \"first\", \"second\", etc. + ORG - Companies, agencies, institutions, etc. + PERCENT - Percentage, including \"%\". + PERSON - People, including fictional. + PHONE - Phone number. + PRODUCT - Objects, vehicles, foods, etc. (Not services.) + QUANTITY - Measurements, as of weight or distance. + SSN - Social Security number + TIME - Times smaller than a day. + WORK_OF_ART - Titles of books, songs, etc. + ZIP - Zip Code (if not part of an Address)  Default is no NERs selected.    # noqa: E501

        :param entities: The entities of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[NamedEntityType]
        """

        self._entities = entities

    @property
    def gender(self):
        """Gets the gender of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(not available for real-time mode yet)_ Set to true to enable voice gender classifcation  # noqa: E501

        :return: The gender of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._gender

    @gender.setter
    def gender(self, gender):
        """Sets the gender of this SpeechAnalyticsConfigModifiable.

        _(not available for real-time mode yet)_ Set to true to enable voice gender classifcation  # noqa: E501

        :param gender: The gender of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._gender = gender

    @property
    def keyword_groups(self):
        """Gets the keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Keyword groups - Group tags must be different from the tags used for keywords. One use for keyword groups is that the GET /sa/call-stats API supports reporting stats of keywords within a Group.</br> Default - there are no keyword groups.   # noqa: E501

        :return: The keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[KeywordSpotGroup]
        """
        return self._keyword_groups

    @keyword_groups.setter
    def keyword_groups(self, keyword_groups):
        """Sets the keyword_groups of this SpeechAnalyticsConfigModifiable.

        Keyword groups - Group tags must be different from the tags used for keywords. One use for keyword groups is that the GET /sa/call-stats API supports reporting stats of keywords within a Group.</br> Default - there are no keyword groups.   # noqa: E501

        :param keyword_groups: The keyword_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[KeywordSpotGroup]
        """

        self._keyword_groups = keyword_groups

    @property
    def keywords(self):
        """Gets the keywords of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Configuration that specifies keywords to be detected. The keyword detection algorithm uses text matching with simple text manipulations like e.g. stemming.</br> Keywords are different in that respect from phrases - phrase detection uses NLU algorithm with neural networks which allows for matching based on approximate meaning.</br> Default is not keyword detection.   # noqa: E501

        :return: The keywords of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[KeywordSpotItem]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """Sets the keywords of this SpeechAnalyticsConfigModifiable.

        Configuration that specifies keywords to be detected. The keyword detection algorithm uses text matching with simple text manipulations like e.g. stemming.</br> Keywords are different in that respect from phrases - phrase detection uses NLU algorithm with neural networks which allows for matching based on approximate meaning.</br> Default is not keyword detection.   # noqa: E501

        :param keywords: The keywords of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[KeywordSpotItem]
        """

        self._keywords = keywords

    @property
    def llm_copilot_notes_prompt(self):
        """Gets the llm_copilot_notes_prompt of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(internal use)_ LLM Prompt that is used to generate the copilot notes.  These are the notes that the Agent would normally enter into the CRM system at the end of the call. They ignore anything that is not relevant for the future record on the caller account. The copilot notes are generated immediately after the call ends.   # noqa: E501

        :return: The llm_copilot_notes_prompt of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._llm_copilot_notes_prompt

    @llm_copilot_notes_prompt.setter
    def llm_copilot_notes_prompt(self, llm_copilot_notes_prompt):
        """Sets the llm_copilot_notes_prompt of this SpeechAnalyticsConfigModifiable.

        _(internal use)_ LLM Prompt that is used to generate the copilot notes.  These are the notes that the Agent would normally enter into the CRM system at the end of the call. They ignore anything that is not relevant for the future record on the caller account. The copilot notes are generated immediately after the call ends.   # noqa: E501

        :param llm_copilot_notes_prompt: The llm_copilot_notes_prompt of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: str
        """

        self._llm_copilot_notes_prompt = llm_copilot_notes_prompt

    @property
    def llm_summary_prompt(self):
        """Gets the llm_summary_prompt of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(internal use)_ LLM Prompt that is used to generate the summary. This is the offline summary of the call, to be distionguished from the copilot notes.   # noqa: E501

        :return: The llm_summary_prompt of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._llm_summary_prompt

    @llm_summary_prompt.setter
    def llm_summary_prompt(self, llm_summary_prompt):
        """Sets the llm_summary_prompt of this SpeechAnalyticsConfigModifiable.

        _(internal use)_ LLM Prompt that is used to generate the summary. This is the offline summary of the call, to be distionguished from the copilot notes.   # noqa: E501

        :param llm_summary_prompt: The llm_summary_prompt of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: str
        """

        self._llm_summary_prompt = llm_summary_prompt

    @property
    def meeting_minutes(self):
        """Gets the meeting_minutes of this SpeechAnalyticsConfigModifiable.  # noqa: E501


        :return: The meeting_minutes of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: SpeechAnalyticsConfigModifiableBaseMeetingMinutes
        """
        return self._meeting_minutes

    @meeting_minutes.setter
    def meeting_minutes(self, meeting_minutes):
        """Sets the meeting_minutes of this SpeechAnalyticsConfigModifiable.


        :param meeting_minutes: The meeting_minutes of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: SpeechAnalyticsConfigModifiableBaseMeetingMinutes
        """

        self._meeting_minutes = meeting_minutes

    @property
    def moods(self):
        """Gets the moods of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Choose the moods to report.</br> Default no moods are reported.   # noqa: E501

        :return: The moods of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[MoodType]
        """
        return self._moods

    @moods.setter
    def moods(self, moods):
        """Sets the moods of this SpeechAnalyticsConfigModifiable.

        Choose the moods to report.</br> Default no moods are reported.   # noqa: E501

        :param moods: The moods of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[MoodType]
        """

        self._moods = moods

    @property
    def overtalk_single_duration_maximum_threshold(self):
        """Gets the overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Duration-based threshold (in milliseconds) used to determine if an overtalk incident has occured.  Applies to maximun duration of single/individual cases of overtalk.   # noqa: E501

        :return: The overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._overtalk_single_duration_maximum_threshold

    @overtalk_single_duration_maximum_threshold.setter
    def overtalk_single_duration_maximum_threshold(self, overtalk_single_duration_maximum_threshold):
        """Sets the overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.

        Duration-based threshold (in milliseconds) used to determine if an overtalk incident has occured.  Applies to maximun duration of single/individual cases of overtalk.   # noqa: E501

        :param overtalk_single_duration_maximum_threshold: The overtalk_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                overtalk_single_duration_maximum_threshold is not None and overtalk_single_duration_maximum_threshold > 60000):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_single_duration_maximum_threshold`, must be a value less than or equal to `60000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                overtalk_single_duration_maximum_threshold is not None and overtalk_single_duration_maximum_threshold < 1):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_single_duration_maximum_threshold`, must be a value greater than or equal to `1`")  # noqa: E501

        self._overtalk_single_duration_maximum_threshold = overtalk_single_duration_maximum_threshold

    @property
    def overtalk_total_percentage_threshold(self):
        """Gets the overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Percentage-based threshold used to determine if an overtalk incident has occured.  Applies to total overtalk expressed as percentage of the call duration.   # noqa: E501

        :return: The overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._overtalk_total_percentage_threshold

    @overtalk_total_percentage_threshold.setter
    def overtalk_total_percentage_threshold(self, overtalk_total_percentage_threshold):
        """Sets the overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.

        Percentage-based threshold used to determine if an overtalk incident has occured.  Applies to total overtalk expressed as percentage of the call duration.   # noqa: E501

        :param overtalk_total_percentage_threshold: The overtalk_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                overtalk_total_percentage_threshold is not None and overtalk_total_percentage_threshold > 100.0):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_total_percentage_threshold`, must be a value less than or equal to `100.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                overtalk_total_percentage_threshold is not None and overtalk_total_percentage_threshold < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `overtalk_total_percentage_threshold`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._overtalk_total_percentage_threshold = overtalk_total_percentage_threshold

    @property
    def phrase_groups(self):
        """Gets the phrase_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Group of phrases/intents. Can be used to detect combinations of phrases in the caller.</br> By default there are no phrase groups.   # noqa: E501

        :return: The phrase_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[PhraseSpotGroup]
        """
        return self._phrase_groups

    @phrase_groups.setter
    def phrase_groups(self, phrase_groups):
        """Sets the phrase_groups of this SpeechAnalyticsConfigModifiable.

        Group of phrases/intents. Can be used to detect combinations of phrases in the caller.</br> By default there are no phrase groups.   # noqa: E501

        :param phrase_groups: The phrase_groups of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[PhraseSpotGroup]
        """

        self._phrase_groups = phrase_groups

    @property
    def phrases(self):
        """Gets the phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Phrases/Intents detected in the text. Phrase detection uses NLU algorithm with neural networks which allows for matching based on approximate meaning. Phrase matching is applied to one sentence at a time. To match multiple sentences in a row please use phraseGroups.</br> If you want to match individual words or 2- or 3-word phrases it may be better to use keywords.</br> Default is no phrase detection.   # noqa: E501

        :return: The phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[PhraseSpotItem]
        """
        return self._phrases

    @phrases.setter
    def phrases(self, phrases):
        """Sets the phrases of this SpeechAnalyticsConfigModifiable.

        Phrases/Intents detected in the text. Phrase detection uses NLU algorithm with neural networks which allows for matching based on approximate meaning. Phrase matching is applied to one sentence at a time. To match multiple sentences in a row please use phraseGroups.</br> If you want to match individual words or 2- or 3-word phrases it may be better to use keywords.</br> Default is no phrase detection.   # noqa: E501

        :param phrases: The phrases of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[PhraseSpotItem]
        """

        self._phrases = phrases

    @property
    def pii_redaction(self):
        """Gets the pii_redaction of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(optional, not for real-time mode yet)_ List specifying the types of entities to be redacted from the transctipt and/or audio</br> Default no PII redaction is performed.   # noqa: E501

        :return: The pii_redaction of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: list[PIIRedactionConf]
        """
        return self._pii_redaction

    @pii_redaction.setter
    def pii_redaction(self, pii_redaction):
        """Sets the pii_redaction of this SpeechAnalyticsConfigModifiable.

        _(optional, not for real-time mode yet)_ List specifying the types of entities to be redacted from the transctipt and/or audio</br> Default no PII redaction is performed.   # noqa: E501

        :param pii_redaction: The pii_redaction of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: list[PIIRedactionConf]
        """

        self._pii_redaction = pii_redaction

    @property
    def profanity(self):
        """Gets the profanity of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Set to true to enable detection of profanity. Will be output together with spotted keywords  # noqa: E501

        :return: The profanity of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._profanity

    @profanity.setter
    def profanity(self, profanity):
        """Sets the profanity of this SpeechAnalyticsConfigModifiable.

        Set to true to enable detection of profanity. Will be output together with spotted keywords  # noqa: E501

        :param profanity: The profanity of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._profanity = profanity

    @property
    def published(self):
        """Gets the published of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Specifies if Speech Analytics configuration can be used outside its context.</br> For built-in configurations, specifies if the configuration is visible to end-users of Voicegain. Only user with \"cmp\" role is able to see built-in configurations that are not published.   # noqa: E501

        :return: The published of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._published

    @published.setter
    def published(self, published):
        """Sets the published of this SpeechAnalyticsConfigModifiable.

        Specifies if Speech Analytics configuration can be used outside its context.</br> For built-in configurations, specifies if the configuration is visible to end-users of Voicegain. Only user with \"cmp\" role is able to see built-in configurations that are not published.   # noqa: E501

        :param published: The published of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._published = published

    @property
    def sentiment(self):
        """Gets the sentiment of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Set to true to enable sentiment analytics  # noqa: E501

        :return: The sentiment of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """Sets the sentiment of this SpeechAnalyticsConfigModifiable.

        Set to true to enable sentiment analytics  # noqa: E501

        :param sentiment: The sentiment of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._sentiment = sentiment

    @property
    def silence_single_duration_maximum_threshold(self):
        """Gets the silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Duration-based threshold (in milliseconds) used to determine if a silence incident has occured.  Applies to maximun duration of single/individual cases of silence.   # noqa: E501

        :return: The silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._silence_single_duration_maximum_threshold

    @silence_single_duration_maximum_threshold.setter
    def silence_single_duration_maximum_threshold(self, silence_single_duration_maximum_threshold):
        """Sets the silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.

        Duration-based threshold (in milliseconds) used to determine if a silence incident has occured.  Applies to maximun duration of single/individual cases of silence.   # noqa: E501

        :param silence_single_duration_maximum_threshold: The silence_single_duration_maximum_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                silence_single_duration_maximum_threshold is not None and silence_single_duration_maximum_threshold > 60000):  # noqa: E501
            raise ValueError("Invalid value for `silence_single_duration_maximum_threshold`, must be a value less than or equal to `60000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                silence_single_duration_maximum_threshold is not None and silence_single_duration_maximum_threshold < 1):  # noqa: E501
            raise ValueError("Invalid value for `silence_single_duration_maximum_threshold`, must be a value greater than or equal to `1`")  # noqa: E501

        self._silence_single_duration_maximum_threshold = silence_single_duration_maximum_threshold

    @property
    def silence_total_percentage_threshold(self):
        """Gets the silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        Percentage-based threshold used to determine if a silence incident has occured.  Applies to total silence expressed as percentage of the call duration.   # noqa: E501

        :return: The silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: float
        """
        return self._silence_total_percentage_threshold

    @silence_total_percentage_threshold.setter
    def silence_total_percentage_threshold(self, silence_total_percentage_threshold):
        """Sets the silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.

        Percentage-based threshold used to determine if a silence incident has occured.  Applies to total silence expressed as percentage of the call duration.   # noqa: E501

        :param silence_total_percentage_threshold: The silence_total_percentage_threshold of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                silence_total_percentage_threshold is not None and silence_total_percentage_threshold > 100.0):  # noqa: E501
            raise ValueError("Invalid value for `silence_total_percentage_threshold`, must be a value less than or equal to `100.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                silence_total_percentage_threshold is not None and silence_total_percentage_threshold < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `silence_total_percentage_threshold`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._silence_total_percentage_threshold = silence_total_percentage_threshold

    @property
    def summary(self):
        """Gets the summary of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(not available for real-time mode yet)_ Set to true to enable output of summary of the transcript (summary is always accross all channels)  # noqa: E501

        :return: The summary of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """Sets the summary of this SpeechAnalyticsConfigModifiable.

        _(not available for real-time mode yet)_ Set to true to enable output of summary of the transcript (summary is always accross all channels)  # noqa: E501

        :param summary: The summary of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._summary = summary

    @property
    def word_cloud(self):
        """Gets the word_cloud of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        _(not for real-time mode)_ Set to true to enable output of word cloud data  # noqa: E501

        :return: The word_cloud of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: bool
        """
        return self._word_cloud

    @word_cloud.setter
    def word_cloud(self, word_cloud):
        """Sets the word_cloud of this SpeechAnalyticsConfigModifiable.

        _(not for real-time mode)_ Set to true to enable output of word cloud data  # noqa: E501

        :param word_cloud: The word_cloud of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: bool
        """

        self._word_cloud = word_cloud

    @property
    def name(self):
        """Gets the name of this SpeechAnalyticsConfigModifiable.  # noqa: E501

        A **unique**, human friendly, name to identify the Speech Analytics configuration.</br> May contain only us-asci letters, digits, and following symbols `.` `-` `_`  </br> Consecutive symbols are not allowed. Must start and end with a digit or letter.    # noqa: E501

        :return: The name of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SpeechAnalyticsConfigModifiable.

        A **unique**, human friendly, name to identify the Speech Analytics configuration.</br> May contain only us-asci letters, digits, and following symbols `.` `-` `_`  </br> Consecutive symbols are not allowed. Must start and end with a digit or letter.    # noqa: E501

        :param name: The name of this SpeechAnalyticsConfigModifiable.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 128):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

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
        if not isinstance(other, SpeechAnalyticsConfigModifiable):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SpeechAnalyticsConfigModifiable):
            return True

        return self.to_dict() != other.to_dict()
