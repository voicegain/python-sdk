# coding: utf-8

"""
    Voicegain API v1

    # New  [Telephony Bot API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + Telephony Bot APIs which in addition to speech-to-text allow for control of real-time communications (RTC) session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Web Console](https://console.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  When making Web APi request the JWT has to be included in the \"Authorization: Bearer\" header. For example, when using curl to make a request:  <pre>   curl -i -X POST \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Authorization: Bearer eyJh......BOGCO70w\" \\   -d @data1.json \\   https://api.voicegain.ai/v1/asr/transcribe/async </pre>  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).  # Edge Deployment API URLs  When you are using Voicegain plaform deployed on Edge, the Web API urls will be different from those that are used in the Cloud (and given in the examples).  For example: * a Web API URL in the Cloud may be: https://api.voicegain.ai/v1/asr/transcribe/async  * but when deployed on Edge which e.g. has this IP:port 10.137.16.7:31680 and does not have SSL configured   * the URL for the same API will be http://10.137.16.7:31680/ascalon-web-api/asr/transcribe/async  * if deployed on Edge with SSL cert and IP:port 10.137.16.7:31443   * the URL for the same API will be https://10.137.16.7:31443/ascalon-web-api/asr/transcribe/async  The reason for this is that in the Cloud, the Web API service is on its own hostname, but on the Edge it has to share the hostname/IP with the Web Console  (which would e.g. have this URL: https://10.137.16.7:31443/customer-portal/)  # Context Defaults  Most of the API requests are made within a specific Context identified by the JWT being used. Each Context has some API (mainly ASR API) related settings which can be set from the Web Console, see image below: ![Context Settings](https://github.com/voicegain/platform/raw/master/images/Context-Speech-Recognition-Settings.PNG)  These settings override the corresponding API default values.  For example, if `noInputTimeout` default is 15000, but the Context 'No Input Timeout' setting is 30000,  and no value is provided in the API request for `noInputTimeout` field, then the API request will run with `noInputTimeout` of 30000.    # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Specifically, 2x OFF-LINE use case is not supported because of how the task queue processor is implemented. To transcribe 2-channels separately in OFF-LINE mode you will need to make 2 separate OFF-LINE transcription requests. Please, let us know if you think you have a valid use case for other combinations.  # Telephony Bot API  (previously called RTC Callback API, where RTC stands for Real Time Communications)   Voicegain Telephony Bot APIs allows you to build conversational voice-enabled applications (e.g. IVRs, Voicebots) over an RTC session (a telephone call for example).  See this blog post for an overview of how this API works: [Voicegain releases Telephony Bot APIs for telephony IVRs and bots](https://www.voicegain.ai/post/rtc-callback-api-released)  Telephony Bot API is a callback API - Voicegain platform makes HTTP request to your app with information about the result of e.g. latest recognition and in response you provide instruction for the next step of the conversation. See the spec of these requests [here](#tag/aivr-callback).  # Speech Analytics API  Voicegain Speech Analytics analyzes both the transcript and the audio (typically of a telephone call).  The results are returned per channel (real or diarized) except where the recognized entities span more than one channel. For entities where it is applicable we return the location in the audio (start and end time) and the transcript (index of the words).  ## Capabilities of Speech Analytics  Voicegain Speech Analytics can identify/compute the following: + **named entities** - (NER i.e. named entity recognition) - the following entities are recognized:   + ADDRESS - Postal address.   + CARDINAL - Numerals that do not fall under another type.   + CC - Credit Card   + DATE - Absolute or relative dates or periods.   + DMY - Full date including all of day, month and year.         + EMAIL - Email address   + EVENT - Named hurricanes, battles, wars, sports events, etc.   + FAC - Buildings, airports, highways, bridges, etc.   + GPE - Countries, cities, states.   + LANGUAGE - Any named language.   + LAW - Named documents made into laws.   + NORP - Nationalities or religious or political groups.   + MONEY - Monetary values, including unit.   + ORDINAL - \"first\", \"second\", etc.   + ORG - Companies, agencies, institutions, etc.   + PERCENT - Percentage, including \"%\".   + PERSON - People, including fictional.   + PHONE - Phone number.   + PRODUCT - Objects, vehicles, foods, etc. (Not services.)   + QUANTITY - Measurements, as of weight or distance.   + SSN - Social Security number   + TIME - Times smaller than a day.   + WORK_OF_ART - Titles of books, songs, etc.   + ZIP - Zip Code (if not part of an Address)    In addition to returning the named entity itself, we return the sub-concepts within entity, e.g. for ADDRESs we will return state (e.g. TX) and zip code if found.  + **keywords** - these are single words or short phrases e.g. company or product names.    Currently, keywords are detected using simple matching using stemming - so e.g. a keyword \"cancel\" will match \"cancellation\".    In near future we will support \"smart expansion\" which will also match synonyms while paying attention to the correct meaning of the word.     In addition to keywords we return keyword groups, e.g. several company name keywords can be combined into a `Competition` keyword group.  + **phrases (intent)** - allows for detection of phrases/intents that match the meaning of the phrases specified in the example training Sections).</br>   For each detected phrase/intent the system will also return entities and keywords contained in the phrase, if configured to do so.   For example, transcript \"Hello, my name is Lucy\" may match phrase/intent \"INTRODUCTION\" with the NER of PERSON and value \"Lucy\".       The configuration for phrase/intent detection takes the following parameters:   + _list_ of example phrases - each phrase has a sensitivity value which determines how close it has to match (sensitivity of 1.0 requires the closest match, sensitivity of 0.0 allows for vague matches).   + _regex_ - optional regex phrases to augment the examples - these require exact match   + _slots_ - types on named entities and keywords to be recognized within the phrase/intent</br>     Note: support for slots of same type but different meaning will be added in the future.     Currently it is possible e.g. to recognize places (GPE) but not possible to distinguish e.g. between types of them, like departure or destination place.   + _location_ - this narrows down where the phrase/match must occur - the options are:     + channel - agent or caller      + time in the call - from the start or from the end     + dialogue act - require the phrase to be part of a specified dialogue act, see https://web.stanford.edu/~jurafsky/ws97/manual.august1.html, first table, column SWBD    + **phrase groups** - computed across all channels - this is more powerful than keyword groups as it can be configured to require all phrases/intents in the groups to be present in any or fixed order.   One use case would be to detect a pair of a question and a confirming answer - for example to determine call resolution: \"Have I answered all your question?\", \"Yes\". + **criteria** - computed by rules/conditions looking at the following parameters:   + _call metrics_   + _regex_ - match of the text of the transcript   + _keywords_ - any keywords or keyword groups   + _NER_ - any named entities   + _phrases_ - any phrases/intents or phrase groups   + _dialogElements_ - selection of custom hardcoded rules that may accomplish tasks not possible with other conditions    The individual rules/conditions can be further narrowed down using filters like:   + _channel_ - agent or caller    + _time in the call_ - from the start or from the end    Multiple rules can be combined to form a logical AND expression.   Finally, the individual rules can be negated so that the absence of certain events is considered as a positive match.    When Criteria are satisfied then the system provides a detailed justification information. + **topics** - computed from text across all channels - assigns to the call a set of likely topics with their scores.    A topic classifier is built in a separate step using a corpus. The build process requires manual labeling of the topics.    For each call, the entire transcript is fed to the topic classifier and we get back the set of detected topics and their scores (in the 0..1 range).   It is useful e.g. for separating Billing calls from Troubleshooting calls from Account Change calls, etc.  + **summary** - computed from text across all channels - provides a summary of the call in a form of a set of sentences.   These may either be key sentences directly pulled from the transcript, or sentences generated by summarizing entire call or sections of the call.  + **sentiment** - computed from text - standard call sentiment as used in Call Center Speech Analytics.   Returns sentiment values from -1.0 (negative/mad/angry) to +1.0 (positive/happy/satisfied) + **gender** - computed to audio - Estimates the gender of the speaker as far as it is possible to do it from the voice alone. + **word cloud** - returns word cloud data (map from words/phrases to frequencies) - the algorithm uses: stop word removal, stemming, frequent phrase detection. + **call metrics** - these are simple metrics computed from the audio and the transcript    + _silence_ - amount of silence in the call   + _talk_ - talk streaks for each of the channels   + _overtalk_ - amount of time when call participants talk over ove another   + _energy_ - the volume of the call and the variation   + _pitch_ - the pitch (frequency of the voice) and the variation  Voicegain allows for configuring Speech Analytics processing by preparing a Speech Analytics Configuration which is basically a selection of the capabilities mentioned above plus configuration of variable elements like keywords, phrases, etc.  </br> You can configure Speech Analytics using **[/sa/config API](#operation/saConfigPost)**   Once the configuration is complete you can launch speech transcription and analytics session using the **[/sa API](#operation/saPost)**   ## Offline vs Real-Time Speech Analytics  Speech audio can be transcribed and then analyzed in one of two modes: + **OFF-LINE** - use the `/sa/offline/` API for this.    Audio will be queued for transcription, then transcribed, and both the audio and transcript will pass through various speech analytics algorithms according to the specified configuration.   The results of transcription and speech analytics can be retrieved using the [GET **/sa/offline/{sid}/data** API](#tag/sa-offline/operation/saOfflineGetData)   + **REAL-TIME** - use the `/sa` API for this.    Audio will immediately be submitted to real-time transcription and the stream of transcribed words will be fed to real-time speech analytics.    The results of transcription and speech analytics will be returned over websocket as soon as they are available. </br>   The format of the returned messages is defined [here](#operation/saWebsocketPayload).    Note that not all speech analytics features are available in real-time. Features missing in real-time are: criteria, topics, summary, gender, word cloud, and call metrics.</br>   The results will also be available afterwards using the [GET **/sa/{sid}/data** API](#operation/saDataGet)  ## Agent Review Form  Data computed by Speech Analytics can be used to automatically fill/answer questions of the Call/Agent Review Form.   The automatic answers can be obtained based on previously defined Criteria (see above).  When Criteria are satisfied then the system provides a detailed justification information so it is easily possible to verify that the automated answer on a Review Form was correct.  ## PII Redaction  Being able to recognize occurrence of certain elements in the transcript allows us to remove them from both the text and the audio - this is called PII Redaction where PII stands for Personally Identifiable Information.  Currently, PII Redaction is limited to named entities (NER).  User can select any NER type detected by [Speech Analytics](#section/Speech-Analytics-API/Capabilities-of-Speech-Analytics) to be replaced by a specified placeholder in the text and by silence in the audio.  If your Enterprise account with Voicegain is setup with PCI-DSS compliance option, then PII Redaction of credit card numbers is enabled by default and cannot be disabled.    # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  The supported audio formats are described here: [Supported Audio Formats](https://support.voicegain.ai/hc/en-us/articles/360050477331-Supported-Audio-Formats). Offline transcription supports a very wide set of audio formats, while real-time transcription is limited to a smaller set of formats.  # Geo-Restrictions (HTTP 451)  Accounts with the `MEDICARE` compliance type (see `complianceType` on the Account object) commit to US-only processing. For such accounts, any API method may respond with HTTP error **451 (Unavailable For Legal Reasons)** when accessed from outside the USA.</br> Geo-enforcement is being rolled out method by method: methods where it is active document the `451` response explicitly. As the rollout proceeds, treat any API method as potentially returning `451` for such accounts, depending on the geographic origin of the request.  # Rate Limiting  Access to Voicegain resources is controlled using the following limit settings on the account.  Newly created accounts get the limit values listed below.  If you need higher limits please contact us at support@voicegain.ai  The limits apply to the use of the Voicegain Platform in the Cloud.  On the Edge, the limits will be determined by the type of license you will purchase.  ## Types of Rate Limits  | Limit | default value | description | |---|---|---| | apiRequestLimitPerMinute | 75 | Basic rate limit with a fixed window of 1 minute applying to all API requests. Requests to /data API will be counted at 10x other requests. | | apiRequestLimitPerHour | 2000 | Basic rate limit with a fixed window of 1 hour applying to all API requests. Requests to /data API will be counted at 10x other requests. | | asrConcurrencyLimit | 4 | Limit on number of concurrent ASR requests. Does not apply to OFF-LINE requests. | | offlineQueueSizeLimit | 10 | Maximum number of OFF-LINE transcription jobs that may be submitted to the queue. | | offlineThroughputLimitPerHour | 4 | Maximum number of hours of audio that can be processed by OFF-LINE transcription within 1 hour. Note: For Edge deployment the limit interval is per day instead of per hour. | | offlineWorkerLimit | 2 | Maximum number of OFF-LINE transcription job workers that will be used to process the account audio. |  For API requests running longer that the rate limit window length, the request count will be applied to both the window when the request started and the window when the request finished.   Every HTTP API request will return several rate-limit related headers in its response.  The header values show the applicable limit, the remaining request count in the current window, and the number of seconds to when the limit resets. For example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 1 RateLimit-Reset: 7 ```  ## When Rate Limits are Hit  If a rate-limit is hit then [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) HTTP error code will be returned. The response headers will additionally include Retry-After value, for example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 0 RateLimit-Reset: 6 Retry-After: 6 ``` If `asrConcurrencyLimit` is hit then the response headers will contain:  ``` X-ResourceLimit-Type: ASR-Concurrency X-ResourceLimit-Limit: 4 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ``` Note that we return a superset of values that are returned for a basic API request limit.  This will allow a client code that was written to handle basic rate limiting to be able to handle concurrency limiting too.  Note also that for the concurrency limit the Retry-After value is approximate and is not guaranteed - so client code may have to retry multiple times. (We will return increasing back-off Retry-After values in case of the limit being hit multiple times.)   In case of `offlineQueueSizeLimit` limit we will return, for example:  ``` X-ResourceLimit-Type: Offline-Queue-Size X-ResourceLimit-Limit: 10 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ```   # Pagination  Voicegain API supports 2 methods of pagination.  ## Sequential pagination  For methods that support sequential pagination Voicegain has standardized on using the following query parameters: + start_after={object id OR nul}  + end_before={object id OR nul}  + per_page={number items per page}  If `start_after=nul` then the first page will be retrieved.</br> If `end_before=nul` then the last page will be retrieved.  `start_after` and `end_before` should not be used together.  If neither `start_after` nor `end_before` are provided, then `start_after=nul` will be assumed.  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?start_after=nul&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?end_before=5f7f1f7d67f67ddaa622b68e&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?start_after=5f7f1f7d67f67ddaa622b68d&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?start_after=5f7f1f7d67f67ddaa622b68c4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?end_before=nul&per_page=50>; rel=\"last\" ```  ## Direct pagination  For methods that support direct pagination Voicegain has standardized on using the following query parameters: + page={page number}  + per_page={number items per page}  `page` is the page number starting from 1 (i.e. first page is 1). This is not an item offset.  This also implies that `per_page` should be kept constant for a set of related requests.  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 786 Link: <https://api.voicegain.ai/v1/sa/call?pager=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=7&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=8&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=16&per_page=50>; rel=\"last\" ``` # Date and Time Formats ## string <date-time>  If value is specified as `string <date-time>` then the format is as per [RFC 3339, section 5.6](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6).  A valid RFC3339 date-time string must have:  + ✅ `YYYY-MM-DD` + ✅ `\"T\"` separator + ✅ `hh:mm:ss` + ✅ optional `.fraction` + ✅ one of `Z`, `+hh:mm`, `-hh:mm`, or `-00:00`  Examples of valid date-time strings:  ### ✅ Canonical / “typical” examples  1) UTC using Z  + 1985-04-12T23:20:50Z + 2025-12-23T14:05:33Z  2) With a positive numeric offset (+hh:mm)  + 1996-12-19T16:39:57+00:00 + 2025-12-23T08:05:33+06:00 + 2025-12-23T23:59:59+01:30  3) With a negative numeric offset (-hh:mm)  + 1996-12-19T16:39:57-08:00 + 2025-12-23T04:05:33-10:00 + 2025-12-23T12:00:00-05:30  ### ✅ Fractional seconds (optional, but allowed)  RFC 3339 allows fractional seconds with a dot, using 1+ digits.  + 1985-04-12T23:20:50.52Z + 2025-12-23T14:05:33.1Z + 2025-12-23T14:05:33.123456+02:00 + 2025-12-23T14:05:33.000000000-07:00  ### ✅ Special case: -00:00 (UTC is known, but local offset is unknown)  This is explicitly allowed and has special semantics.  + 2025-12-23T14:05:33-00:00 + 1985-04-12T23:20:50.52-00:00  ### ✅ Boundary-ish but valid examples Midnight / start of day:  + 2025-12-23T00:00:00Z  End of day:  + 2025-12-23T23:59:59Z  ### Time zone not provided  If a date-time value is provided without a time zone offset, the time zone specified on the Context (Project) or Account will be used to interpret the provided time value.  # PCI-DSS Compliance (Cloud)  The PCI-DSS compliant endpoint on the Voicegain Cloud is https://sapi.voicegain.ai/v1/ </br> Do not submit requests that may contain CHD data to the standard endpoint at https://api.voicegain.ai/v1/  Here is a list of all API Methods that are PCI-DSS compliant: + `/asr/transcribe`: [POST](#operation/asrTranscribePost) + `/asr/transcribe/async`: [POST](#operation/asrTranscribeAsyncPost) - we support OFF-LINE and REAL-TIME + `/asr/transcribe/{sessionId}`: [GET](#operation/asrTranscribeAsyncGet) [PUT](#operation/asrTranscribeAsyncPut) [DELETE](#operation/asrTranscribeAsyncDelete)  Note that the /data API is not yet PCI-DSS compliant on the Cloud. This means that the only PCI-DSS compliant ways to submit the audio are: + `fromUrl` - use `authConf` for authenticated access or use signed short-lived URLs + `inline` + `stream` - only `WSS` (old `WEBSOCKET`) and `TWIML` protocols are supported right now  https://sapi.voicegain.ai/v1/ endpoint does not support API methods that would store data, either the audio or the transcription results.   https://sapi.voicegain.ai/v1/ endpoint does support audio redaction. Redacted audio is not stored but submitted directly to the URL specified in the request `audio.callback`.   # PCI-DSS Compliance (Edge)  Because the Edge deployment happens ultimately in the customer's environment, it will the customer's responsibility to certify their Edge depoyment of the Voicegain platform as PCI-DSS compliant.  Voicegain can provide Attestation of Compliance (AoC) for the following PCI-DSS sections as far as they releate to Voicegain Software that will be deployed on Edge: + 5. Use and regularly update anti-virus software or programs + 6. Develop and maintain secure systems and applications + 11. Regularly test security systems and processes + 12. Maintain a policy that addresses information security for all personnel  For the following PCI-DSS sections we will provide detailed data regarding implementation: + 3. Protect stored cardholder data   # noqa: E501

    The version of the OpenAPI document: 1.140.0 - updated September 5, 2026
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from voicegain_speech.configuration import Configuration


class VoiceCallLight(object):
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
        'abandoned': 'bool',
        'account_id': 'str',
        'agent': 'Agent',
        'aivr_app_id': 'str',
        'aivr_platform': 'str',
        'aivr_session_id': 'str',
        'aivr_transfer_dest_type': 'TransferDestType',
        'business_open_state': 'str',
        'call_center_call_id': 'str',
        'call_id': 'str',
        'call_resolved': 'bool',
        'ci_answers_id': 'str',
        'context_id': 'str',
        'copilot_sent': 'float',
        'copilot_un_ack': 'float',
        'cr_answers_id': 'str',
        'csat': 'float',
        'daily_repeat_calls': 'int',
        'direction': 'str',
        'duration': 'int',
        'end_time': 'datetime',
        'expiry_time': 'datetime',
        'external_endpoint': 'str',
        'inbound_rtp_quality': 'RtpQuality',
        'incidents': 'int',
        'internal_endpoint': 'str',
        'keywords': 'list[str]',
        'language': 'Language',
        'last_recompute_time': 'datetime',
        'merged_audio_id': 'str',
        'metadata': 'list[CallMetadataItem]',
        'nps': 'float',
        'num_audio_channels': 'int',
        'num_segments': 'int',
        'num_spk_channels': 'int',
        'originating_call_id': 'str',
        'outbound_rtp_quality': 'RtpQuality',
        'progress_phase': 'ProgressPhase',
        'queue': 'Queue',
        'queue_wait_ms': 'int',
        'recompute_phase': 'str',
        'recording': 'str',
        'reference_number': 'str',
        'sa_session_id': 'str',
        'score': 'float',
        'sentiment': 'float',
        'sentiments': 'list[SpeakerSentimentItem]',
        'spawned_calls': 'list[str]',
        'start_time': 'datetime',
        'tags': 'list[str]',
        'team': 'str',
        'topics': 'list[str]',
        'transfer_time': 'datetime',
        'unaudited_score': 'float',
        'version': 'int',
        'voicebot_duration': 'float',
        'voicebot_vars': 'VoiceCallLightVoicebotVars',
        'voicemail_duration': 'float',
        'voicemail_uuid': 'str',
        'who_hung_up': 'str'
    }

    attribute_map = {
        'abandoned': 'abandoned',
        'account_id': 'accountId',
        'agent': 'agent',
        'aivr_app_id': 'aivrAppId',
        'aivr_platform': 'aivrPlatform',
        'aivr_session_id': 'aivrSessionId',
        'aivr_transfer_dest_type': 'aivrTransferDestType',
        'business_open_state': 'businessOpenState',
        'call_center_call_id': 'callCenterCallId',
        'call_id': 'callId',
        'call_resolved': 'callResolved',
        'ci_answers_id': 'ciAnswersId',
        'context_id': 'contextId',
        'copilot_sent': 'copilotSent',
        'copilot_un_ack': 'copilotUnAck',
        'cr_answers_id': 'crAnswersId',
        'csat': 'csat',
        'daily_repeat_calls': 'dailyRepeatCalls',
        'direction': 'direction',
        'duration': 'duration',
        'end_time': 'endTime',
        'expiry_time': 'expiryTime',
        'external_endpoint': 'externalEndpoint',
        'inbound_rtp_quality': 'inboundRtpQuality',
        'incidents': 'incidents',
        'internal_endpoint': 'internalEndpoint',
        'keywords': 'keywords',
        'language': 'language',
        'last_recompute_time': 'lastRecomputeTime',
        'merged_audio_id': 'mergedAudioId',
        'metadata': 'metadata',
        'nps': 'nps',
        'num_audio_channels': 'numAudioChannels',
        'num_segments': 'numSegments',
        'num_spk_channels': 'numSpkChannels',
        'originating_call_id': 'originatingCallId',
        'outbound_rtp_quality': 'outboundRtpQuality',
        'progress_phase': 'progressPhase',
        'queue': 'queue',
        'queue_wait_ms': 'queueWaitMs',
        'recompute_phase': 'recomputePhase',
        'recording': 'recording',
        'reference_number': 'referenceNumber',
        'sa_session_id': 'saSessionId',
        'score': 'score',
        'sentiment': 'sentiment',
        'sentiments': 'sentiments',
        'spawned_calls': 'spawnedCalls',
        'start_time': 'startTime',
        'tags': 'tags',
        'team': 'team',
        'topics': 'topics',
        'transfer_time': 'transferTime',
        'unaudited_score': 'unauditedScore',
        'version': 'version',
        'voicebot_duration': 'voicebotDuration',
        'voicebot_vars': 'voicebotVars',
        'voicemail_duration': 'voicemailDuration',
        'voicemail_uuid': 'voicemailUuid',
        'who_hung_up': 'whoHungUp'
    }

    def __init__(self, abandoned=None, account_id=None, agent=None, aivr_app_id=None, aivr_platform=None, aivr_session_id=None, aivr_transfer_dest_type=None, business_open_state=None, call_center_call_id=None, call_id=None, call_resolved=None, ci_answers_id=None, context_id=None, copilot_sent=None, copilot_un_ack=None, cr_answers_id=None, csat=None, daily_repeat_calls=None, direction=None, duration=None, end_time=None, expiry_time=None, external_endpoint=None, inbound_rtp_quality=None, incidents=None, internal_endpoint=None, keywords=None, language=None, last_recompute_time=None, merged_audio_id=None, metadata=None, nps=None, num_audio_channels=None, num_segments=None, num_spk_channels=None, originating_call_id=None, outbound_rtp_quality=None, progress_phase=None, queue=None, queue_wait_ms=None, recompute_phase=None, recording=None, reference_number=None, sa_session_id=None, score=None, sentiment=None, sentiments=None, spawned_calls=None, start_time=None, tags=None, team=None, topics=None, transfer_time=None, unaudited_score=None, version=None, voicebot_duration=None, voicebot_vars=None, voicemail_duration=None, voicemail_uuid=None, who_hung_up=None, local_vars_configuration=None):  # noqa: E501
        """VoiceCallLight - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._abandoned = None
        self._account_id = None
        self._agent = None
        self._aivr_app_id = None
        self._aivr_platform = None
        self._aivr_session_id = None
        self._aivr_transfer_dest_type = None
        self._business_open_state = None
        self._call_center_call_id = None
        self._call_id = None
        self._call_resolved = None
        self._ci_answers_id = None
        self._context_id = None
        self._copilot_sent = None
        self._copilot_un_ack = None
        self._cr_answers_id = None
        self._csat = None
        self._daily_repeat_calls = None
        self._direction = None
        self._duration = None
        self._end_time = None
        self._expiry_time = None
        self._external_endpoint = None
        self._inbound_rtp_quality = None
        self._incidents = None
        self._internal_endpoint = None
        self._keywords = None
        self._language = None
        self._last_recompute_time = None
        self._merged_audio_id = None
        self._metadata = None
        self._nps = None
        self._num_audio_channels = None
        self._num_segments = None
        self._num_spk_channels = None
        self._originating_call_id = None
        self._outbound_rtp_quality = None
        self._progress_phase = None
        self._queue = None
        self._queue_wait_ms = None
        self._recompute_phase = None
        self._recording = None
        self._reference_number = None
        self._sa_session_id = None
        self._score = None
        self._sentiment = None
        self._sentiments = None
        self._spawned_calls = None
        self._start_time = None
        self._tags = None
        self._team = None
        self._topics = None
        self._transfer_time = None
        self._unaudited_score = None
        self._version = None
        self._voicebot_duration = None
        self._voicebot_vars = None
        self._voicemail_duration = None
        self._voicemail_uuid = None
        self._who_hung_up = None
        self.discriminator = None

        if abandoned is not None:
            self.abandoned = abandoned
        if account_id is not None:
            self.account_id = account_id
        if agent is not None:
            self.agent = agent
        if aivr_app_id is not None:
            self.aivr_app_id = aivr_app_id
        if aivr_platform is not None:
            self.aivr_platform = aivr_platform
        if aivr_session_id is not None:
            self.aivr_session_id = aivr_session_id
        if aivr_transfer_dest_type is not None:
            self.aivr_transfer_dest_type = aivr_transfer_dest_type
        if business_open_state is not None:
            self.business_open_state = business_open_state
        if call_center_call_id is not None:
            self.call_center_call_id = call_center_call_id
        if call_id is not None:
            self.call_id = call_id
        if call_resolved is not None:
            self.call_resolved = call_resolved
        if ci_answers_id is not None:
            self.ci_answers_id = ci_answers_id
        if context_id is not None:
            self.context_id = context_id
        if copilot_sent is not None:
            self.copilot_sent = copilot_sent
        if copilot_un_ack is not None:
            self.copilot_un_ack = copilot_un_ack
        if cr_answers_id is not None:
            self.cr_answers_id = cr_answers_id
        if csat is not None:
            self.csat = csat
        if daily_repeat_calls is not None:
            self.daily_repeat_calls = daily_repeat_calls
        if direction is not None:
            self.direction = direction
        if duration is not None:
            self.duration = duration
        if end_time is not None:
            self.end_time = end_time
        if expiry_time is not None:
            self.expiry_time = expiry_time
        if external_endpoint is not None:
            self.external_endpoint = external_endpoint
        if inbound_rtp_quality is not None:
            self.inbound_rtp_quality = inbound_rtp_quality
        if incidents is not None:
            self.incidents = incidents
        if internal_endpoint is not None:
            self.internal_endpoint = internal_endpoint
        if keywords is not None:
            self.keywords = keywords
        if language is not None:
            self.language = language
        if last_recompute_time is not None:
            self.last_recompute_time = last_recompute_time
        if merged_audio_id is not None:
            self.merged_audio_id = merged_audio_id
        if metadata is not None:
            self.metadata = metadata
        if nps is not None:
            self.nps = nps
        if num_audio_channels is not None:
            self.num_audio_channels = num_audio_channels
        if num_segments is not None:
            self.num_segments = num_segments
        if num_spk_channels is not None:
            self.num_spk_channels = num_spk_channels
        if originating_call_id is not None:
            self.originating_call_id = originating_call_id
        if outbound_rtp_quality is not None:
            self.outbound_rtp_quality = outbound_rtp_quality
        if progress_phase is not None:
            self.progress_phase = progress_phase
        if queue is not None:
            self.queue = queue
        if queue_wait_ms is not None:
            self.queue_wait_ms = queue_wait_ms
        if recompute_phase is not None:
            self.recompute_phase = recompute_phase
        if recording is not None:
            self.recording = recording
        if reference_number is not None:
            self.reference_number = reference_number
        if sa_session_id is not None:
            self.sa_session_id = sa_session_id
        if score is not None:
            self.score = score
        if sentiment is not None:
            self.sentiment = sentiment
        if sentiments is not None:
            self.sentiments = sentiments
        if spawned_calls is not None:
            self.spawned_calls = spawned_calls
        if start_time is not None:
            self.start_time = start_time
        if tags is not None:
            self.tags = tags
        if team is not None:
            self.team = team
        if topics is not None:
            self.topics = topics
        if transfer_time is not None:
            self.transfer_time = transfer_time
        if unaudited_score is not None:
            self.unaudited_score = unaudited_score
        if version is not None:
            self.version = version
        if voicebot_duration is not None:
            self.voicebot_duration = voicebot_duration
        if voicebot_vars is not None:
            self.voicebot_vars = voicebot_vars
        if voicemail_duration is not None:
            self.voicemail_duration = voicemail_duration
        if voicemail_uuid is not None:
            self.voicemail_uuid = voicemail_uuid
        if who_hung_up is not None:
            self.who_hung_up = who_hung_up

    @property
    def abandoned(self):
        """Gets the abandoned of this VoiceCallLight.  # noqa: E501

        True when the call was abandoned: the caller hung up while waiting in the ACD queue before any agent answered. Absent or false for answered calls.   # noqa: E501

        :return: The abandoned of this VoiceCallLight.  # noqa: E501
        :rtype: bool
        """
        return self._abandoned

    @abandoned.setter
    def abandoned(self, abandoned):
        """Sets the abandoned of this VoiceCallLight.

        True when the call was abandoned: the caller hung up while waiting in the ACD queue before any agent answered. Absent or false for answered calls.   # noqa: E501

        :param abandoned: The abandoned of this VoiceCallLight.  # noqa: E501
        :type: bool
        """

        self._abandoned = abandoned

    @property
    def account_id(self):
        """Gets the account_id of this VoiceCallLight.  # noqa: E501

        Voicegain Account  # noqa: E501

        :return: The account_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this VoiceCallLight.

        Voicegain Account  # noqa: E501

        :param account_id: The account_id of this VoiceCallLight.  # noqa: E501
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
    def agent(self):
        """Gets the agent of this VoiceCallLight.  # noqa: E501


        :return: The agent of this VoiceCallLight.  # noqa: E501
        :rtype: Agent
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this VoiceCallLight.


        :param agent: The agent of this VoiceCallLight.  # noqa: E501
        :type: Agent
        """

        self._agent = agent

    @property
    def aivr_app_id(self):
        """Gets the aivr_app_id of this VoiceCallLight.  # noqa: E501

        Id of the AIVR application that handled the call. Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :return: The aivr_app_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._aivr_app_id

    @aivr_app_id.setter
    def aivr_app_id(self, aivr_app_id):
        """Sets the aivr_app_id of this VoiceCallLight.

        Id of the AIVR application that handled the call. Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :param aivr_app_id: The aivr_app_id of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._aivr_app_id = aivr_app_id

    @property
    def aivr_platform(self):
        """Gets the aivr_platform of this VoiceCallLight.  # noqa: E501

        Platform on which the AIVR App runs.</br> Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :return: The aivr_platform of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._aivr_platform

    @aivr_platform.setter
    def aivr_platform(self, aivr_platform):
        """Sets the aivr_platform of this VoiceCallLight.

        Platform on which the AIVR App runs.</br> Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :param aivr_platform: The aivr_platform of this VoiceCallLight.  # noqa: E501
        :type: str
        """
        allowed_values = ["freeSwitch", "vonageVcca", "five9VoiceStream", "trampoline"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and aivr_platform not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `aivr_platform` ({0}), must be one of {1}"  # noqa: E501
                .format(aivr_platform, allowed_values)
            )

        self._aivr_platform = aivr_platform

    @property
    def aivr_session_id(self):
        """Gets the aivr_session_id of this VoiceCallLight.  # noqa: E501

        Id of the AIVR session that handled the call. Will be absent if the call did not come from an AIVR Session.   # noqa: E501

        :return: The aivr_session_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._aivr_session_id

    @aivr_session_id.setter
    def aivr_session_id(self, aivr_session_id):
        """Sets the aivr_session_id of this VoiceCallLight.

        Id of the AIVR session that handled the call. Will be absent if the call did not come from an AIVR Session.   # noqa: E501

        :param aivr_session_id: The aivr_session_id of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._aivr_session_id = aivr_session_id

    @property
    def aivr_transfer_dest_type(self):
        """Gets the aivr_transfer_dest_type of this VoiceCallLight.  # noqa: E501

        Type of destination for the AIVR transfer. Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :return: The aivr_transfer_dest_type of this VoiceCallLight.  # noqa: E501
        :rtype: TransferDestType
        """
        return self._aivr_transfer_dest_type

    @aivr_transfer_dest_type.setter
    def aivr_transfer_dest_type(self, aivr_transfer_dest_type):
        """Sets the aivr_transfer_dest_type of this VoiceCallLight.

        Type of destination for the AIVR transfer. Will be absent if the call did not come from an AIVR App.   # noqa: E501

        :param aivr_transfer_dest_type: The aivr_transfer_dest_type of this VoiceCallLight.  # noqa: E501
        :type: TransferDestType
        """

        self._aivr_transfer_dest_type = aivr_transfer_dest_type

    @property
    def business_open_state(self):
        """Gets the business_open_state of this VoiceCallLight.  # noqa: E501

        State of the business open/close status, from the business hours defined in the AIVR App (Business Config). Absent if no business hours are defined in the AIVR App. + open - business is open + off-hours - business was closed when the call was placed but was open at other times that day + closed - business is closed the whole day   # noqa: E501

        :return: The business_open_state of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._business_open_state

    @business_open_state.setter
    def business_open_state(self, business_open_state):
        """Sets the business_open_state of this VoiceCallLight.

        State of the business open/close status, from the business hours defined in the AIVR App (Business Config). Absent if no business hours are defined in the AIVR App. + open - business is open + off-hours - business was closed when the call was placed but was open at other times that day + closed - business is closed the whole day   # noqa: E501

        :param business_open_state: The business_open_state of this VoiceCallLight.  # noqa: E501
        :type: str
        """
        allowed_values = ["open", "off-hours", "closed"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and business_open_state not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `business_open_state` ({0}), must be one of {1}"  # noqa: E501
                .format(business_open_state, allowed_values)
            )

        self._business_open_state = business_open_state

    @property
    def call_center_call_id(self):
        """Gets the call_center_call_id of this VoiceCallLight.  # noqa: E501

        Id of the call in the call center system, e.g., Aircall.   # noqa: E501

        :return: The call_center_call_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._call_center_call_id

    @call_center_call_id.setter
    def call_center_call_id(self, call_center_call_id):
        """Sets the call_center_call_id of this VoiceCallLight.

        Id of the call in the call center system, e.g., Aircall.   # noqa: E501

        :param call_center_call_id: The call_center_call_id of this VoiceCallLight.  # noqa: E501
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
    def call_id(self):
        """Gets the call_id of this VoiceCallLight.  # noqa: E501

        Unique Id of the call  # noqa: E501

        :return: The call_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._call_id

    @call_id.setter
    def call_id(self, call_id):
        """Sets the call_id of this VoiceCallLight.

        Unique Id of the call  # noqa: E501

        :param call_id: The call_id of this VoiceCallLight.  # noqa: E501
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
        """Gets the call_resolved of this VoiceCallLight.  # noqa: E501

        Set to true if Call Review determined that the call successfully resolved/handled the problem/issues  # noqa: E501

        :return: The call_resolved of this VoiceCallLight.  # noqa: E501
        :rtype: bool
        """
        return self._call_resolved

    @call_resolved.setter
    def call_resolved(self, call_resolved):
        """Sets the call_resolved of this VoiceCallLight.

        Set to true if Call Review determined that the call successfully resolved/handled the problem/issues  # noqa: E501

        :param call_resolved: The call_resolved of this VoiceCallLight.  # noqa: E501
        :type: bool
        """

        self._call_resolved = call_resolved

    @property
    def ci_answers_id(self):
        """Gets the ci_answers_id of this VoiceCallLight.  # noqa: E501

        Unique id referencing the call insights answers  # noqa: E501

        :return: The ci_answers_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._ci_answers_id

    @ci_answers_id.setter
    def ci_answers_id(self, ci_answers_id):
        """Sets the ci_answers_id of this VoiceCallLight.

        Unique id referencing the call insights answers  # noqa: E501

        :param ci_answers_id: The ci_answers_id of this VoiceCallLight.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                ci_answers_id is not None and len(ci_answers_id) > 48):
            raise ValueError("Invalid value for `ci_answers_id`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                ci_answers_id is not None and len(ci_answers_id) < 16):
            raise ValueError("Invalid value for `ci_answers_id`, length must be greater than or equal to `16`")  # noqa: E501

        self._ci_answers_id = ci_answers_id

    @property
    def context_id(self):
        """Gets the context_id of this VoiceCallLight.  # noqa: E501

        Voicegain Account Context  # noqa: E501

        :return: The context_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._context_id

    @context_id.setter
    def context_id(self, context_id):
        """Sets the context_id of this VoiceCallLight.

        Voicegain Account Context  # noqa: E501

        :param context_id: The context_id of this VoiceCallLight.  # noqa: E501
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
    def copilot_sent(self):
        """Gets the copilot_sent of this VoiceCallLight.  # noqa: E501

        Number of messages sent to Copilot during the call.   # noqa: E501

        :return: The copilot_sent of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._copilot_sent

    @copilot_sent.setter
    def copilot_sent(self, copilot_sent):
        """Sets the copilot_sent of this VoiceCallLight.

        Number of messages sent to Copilot during the call.   # noqa: E501

        :param copilot_sent: The copilot_sent of this VoiceCallLight.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                copilot_sent is not None and copilot_sent < 0):  # noqa: E501
            raise ValueError("Invalid value for `copilot_sent`, must be a value greater than or equal to `0`")  # noqa: E501

        self._copilot_sent = copilot_sent

    @property
    def copilot_un_ack(self):
        """Gets the copilot_un_ack of this VoiceCallLight.  # noqa: E501

        Number of missing acknowledgements from Copilot for the messages sent to Copilot.   # noqa: E501

        :return: The copilot_un_ack of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._copilot_un_ack

    @copilot_un_ack.setter
    def copilot_un_ack(self, copilot_un_ack):
        """Sets the copilot_un_ack of this VoiceCallLight.

        Number of missing acknowledgements from Copilot for the messages sent to Copilot.   # noqa: E501

        :param copilot_un_ack: The copilot_un_ack of this VoiceCallLight.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                copilot_un_ack is not None and copilot_un_ack < 0):  # noqa: E501
            raise ValueError("Invalid value for `copilot_un_ack`, must be a value greater than or equal to `0`")  # noqa: E501

        self._copilot_un_ack = copilot_un_ack

    @property
    def cr_answers_id(self):
        """Gets the cr_answers_id of this VoiceCallLight.  # noqa: E501

        Unique id referencing the call review answers  # noqa: E501

        :return: The cr_answers_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._cr_answers_id

    @cr_answers_id.setter
    def cr_answers_id(self, cr_answers_id):
        """Sets the cr_answers_id of this VoiceCallLight.

        Unique id referencing the call review answers  # noqa: E501

        :param cr_answers_id: The cr_answers_id of this VoiceCallLight.  # noqa: E501
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
    def csat(self):
        """Gets the csat of this VoiceCallLight.  # noqa: E501

        Customer Satisfaction score for the call.   # noqa: E501

        :return: The csat of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._csat

    @csat.setter
    def csat(self, csat):
        """Sets the csat of this VoiceCallLight.

        Customer Satisfaction score for the call.   # noqa: E501

        :param csat: The csat of this VoiceCallLight.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                csat is not None and csat < 0):  # noqa: E501
            raise ValueError("Invalid value for `csat`, must be a value greater than or equal to `0`")  # noqa: E501

        self._csat = csat

    @property
    def daily_repeat_calls(self):
        """Gets the daily_repeat_calls of this VoiceCallLight.  # noqa: E501

        Number of repeat calls: other calls between the same `externalEndpoint` and the same `internalEndpoint` in the 24 hours before `startTime`. It is 0 if this is the only such call.   # noqa: E501

        :return: The daily_repeat_calls of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._daily_repeat_calls

    @daily_repeat_calls.setter
    def daily_repeat_calls(self, daily_repeat_calls):
        """Sets the daily_repeat_calls of this VoiceCallLight.

        Number of repeat calls: other calls between the same `externalEndpoint` and the same `internalEndpoint` in the 24 hours before `startTime`. It is 0 if this is the only such call.   # noqa: E501

        :param daily_repeat_calls: The daily_repeat_calls of this VoiceCallLight.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                daily_repeat_calls is not None and daily_repeat_calls < 0):  # noqa: E501
            raise ValueError("Invalid value for `daily_repeat_calls`, must be a value greater than or equal to `0`")  # noqa: E501

        self._daily_repeat_calls = daily_repeat_calls

    @property
    def direction(self):
        """Gets the direction of this VoiceCallLight.  # noqa: E501

        direction of the call  # noqa: E501

        :return: The direction of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction):
        """Sets the direction of this VoiceCallLight.

        direction of the call  # noqa: E501

        :param direction: The direction of this VoiceCallLight.  # noqa: E501
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
    def duration(self):
        """Gets the duration of this VoiceCallLight.  # noqa: E501

        duration of the call in seconds  # noqa: E501

        :return: The duration of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Sets the duration of this VoiceCallLight.

        duration of the call in seconds  # noqa: E501

        :param duration: The duration of this VoiceCallLight.  # noqa: E501
        :type: int
        """

        self._duration = duration

    @property
    def end_time(self):
        """Gets the end_time of this VoiceCallLight.  # noqa: E501

        end time of the call (UTC)  # noqa: E501

        :return: The end_time of this VoiceCallLight.  # noqa: E501
        :rtype: datetime
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this VoiceCallLight.

        end time of the call (UTC)  # noqa: E501

        :param end_time: The end_time of this VoiceCallLight.  # noqa: E501
        :type: datetime
        """

        self._end_time = end_time

    @property
    def expiry_time(self):
        """Gets the expiry_time of this VoiceCallLight.  # noqa: E501

        Expiration time of the call (UTC). The call and all call associated data will be deleted within 24-48 hours after this date-time.   # noqa: E501

        :return: The expiry_time of this VoiceCallLight.  # noqa: E501
        :rtype: datetime
        """
        return self._expiry_time

    @expiry_time.setter
    def expiry_time(self, expiry_time):
        """Sets the expiry_time of this VoiceCallLight.

        Expiration time of the call (UTC). The call and all call associated data will be deleted within 24-48 hours after this date-time.   # noqa: E501

        :param expiry_time: The expiry_time of this VoiceCallLight.  # noqa: E501
        :type: datetime
        """

        self._expiry_time = expiry_time

    @property
    def external_endpoint(self):
        """Gets the external_endpoint of this VoiceCallLight.  # noqa: E501

        Caller (for inbound) or callee (for outbound) identifier. For phone calls it will be a caller id (ANI) in E.164 format.   # noqa: E501

        :return: The external_endpoint of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._external_endpoint

    @external_endpoint.setter
    def external_endpoint(self, external_endpoint):
        """Sets the external_endpoint of this VoiceCallLight.

        Caller (for inbound) or callee (for outbound) identifier. For phone calls it will be a caller id (ANI) in E.164 format.   # noqa: E501

        :param external_endpoint: The external_endpoint of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._external_endpoint = external_endpoint

    @property
    def inbound_rtp_quality(self):
        """Gets the inbound_rtp_quality of this VoiceCallLight.  # noqa: E501

        RTP quality metrics for inbound audio stream obtained from CDR records.   # noqa: E501

        :return: The inbound_rtp_quality of this VoiceCallLight.  # noqa: E501
        :rtype: RtpQuality
        """
        return self._inbound_rtp_quality

    @inbound_rtp_quality.setter
    def inbound_rtp_quality(self, inbound_rtp_quality):
        """Sets the inbound_rtp_quality of this VoiceCallLight.

        RTP quality metrics for inbound audio stream obtained from CDR records.   # noqa: E501

        :param inbound_rtp_quality: The inbound_rtp_quality of this VoiceCallLight.  # noqa: E501
        :type: RtpQuality
        """

        self._inbound_rtp_quality = inbound_rtp_quality

    @property
    def incidents(self):
        """Gets the incidents of this VoiceCallLight.  # noqa: E501

        Number of silence and overtalk incidents  # noqa: E501

        :return: The incidents of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._incidents

    @incidents.setter
    def incidents(self, incidents):
        """Sets the incidents of this VoiceCallLight.

        Number of silence and overtalk incidents  # noqa: E501

        :param incidents: The incidents of this VoiceCallLight.  # noqa: E501
        :type: int
        """

        self._incidents = incidents

    @property
    def internal_endpoint(self):
        """Gets the internal_endpoint of this VoiceCallLight.  # noqa: E501

        Identifier of the internal endpoint that received inbound call or originated outbound call. For phone calls it will be DNIS or caller id.   # noqa: E501

        :return: The internal_endpoint of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._internal_endpoint

    @internal_endpoint.setter
    def internal_endpoint(self, internal_endpoint):
        """Sets the internal_endpoint of this VoiceCallLight.

        Identifier of the internal endpoint that received inbound call or originated outbound call. For phone calls it will be DNIS or caller id.   # noqa: E501

        :param internal_endpoint: The internal_endpoint of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._internal_endpoint = internal_endpoint

    @property
    def keywords(self):
        """Gets the keywords of this VoiceCallLight.  # noqa: E501

        All keywords detected  # noqa: E501

        :return: The keywords of this VoiceCallLight.  # noqa: E501
        :rtype: list[str]
        """
        return self._keywords

    @keywords.setter
    def keywords(self, keywords):
        """Sets the keywords of this VoiceCallLight.

        All keywords detected  # noqa: E501

        :param keywords: The keywords of this VoiceCallLight.  # noqa: E501
        :type: list[str]
        """

        self._keywords = keywords

    @property
    def language(self):
        """Gets the language of this VoiceCallLight.  # noqa: E501

        Primary language of the call.   # noqa: E501

        :return: The language of this VoiceCallLight.  # noqa: E501
        :rtype: Language
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this VoiceCallLight.

        Primary language of the call.   # noqa: E501

        :param language: The language of this VoiceCallLight.  # noqa: E501
        :type: Language
        """

        self._language = language

    @property
    def last_recompute_time(self):
        """Gets the last_recompute_time of this VoiceCallLight.  # noqa: E501

        finish time of the last recompute (UTC)  # noqa: E501

        :return: The last_recompute_time of this VoiceCallLight.  # noqa: E501
        :rtype: datetime
        """
        return self._last_recompute_time

    @last_recompute_time.setter
    def last_recompute_time(self, last_recompute_time):
        """Sets the last_recompute_time of this VoiceCallLight.

        finish time of the last recompute (UTC)  # noqa: E501

        :param last_recompute_time: The last_recompute_time of this VoiceCallLight.  # noqa: E501
        :type: datetime
        """

        self._last_recompute_time = last_recompute_time

    @property
    def merged_audio_id(self):
        """Gets the merged_audio_id of this VoiceCallLight.  # noqa: E501

        Data UUID - reference to the merged call audio in Voicegain Data Store. If PII redaction was enabled then this audio is redacted. Absent if Speech Analytics has not been run on the call.   # noqa: E501

        :return: The merged_audio_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._merged_audio_id

    @merged_audio_id.setter
    def merged_audio_id(self, merged_audio_id):
        """Sets the merged_audio_id of this VoiceCallLight.

        Data UUID - reference to the merged call audio in Voicegain Data Store. If PII redaction was enabled then this audio is redacted. Absent if Speech Analytics has not been run on the call.   # noqa: E501

        :param merged_audio_id: The merged_audio_id of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._merged_audio_id = merged_audio_id

    @property
    def metadata(self):
        """Gets the metadata of this VoiceCallLight.  # noqa: E501

        Free-form name/value attributes attached to the call, e.g. identifiers of the call on other systems.</br> Unlike `tags` these are key/value pairs and do not show in the tag facet / tag cloud.</br> + Names are unique within a call. They are case-sensitive. + At most 32 entries per call. + Can be set on `POST /sa/call` and modified with   <a href=\"#tag/sa-internal/operation/saCallMetadataPut\">PUT /sa/call/{callId}/metadata</a>. + Searchable in the advanced call search with the `METADATA` field (see `CallField`).  Absent (or empty) for calls without metadata.   # noqa: E501

        :return: The metadata of this VoiceCallLight.  # noqa: E501
        :rtype: list[CallMetadataItem]
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this VoiceCallLight.

        Free-form name/value attributes attached to the call, e.g. identifiers of the call on other systems.</br> Unlike `tags` these are key/value pairs and do not show in the tag facet / tag cloud.</br> + Names are unique within a call. They are case-sensitive. + At most 32 entries per call. + Can be set on `POST /sa/call` and modified with   <a href=\"#tag/sa-internal/operation/saCallMetadataPut\">PUT /sa/call/{callId}/metadata</a>. + Searchable in the advanced call search with the `METADATA` field (see `CallField`).  Absent (or empty) for calls without metadata.   # noqa: E501

        :param metadata: The metadata of this VoiceCallLight.  # noqa: E501
        :type: list[CallMetadataItem]
        """

        self._metadata = metadata

    @property
    def nps(self):
        """Gets the nps of this VoiceCallLight.  # noqa: E501

        Net Promoter Score for the call.   # noqa: E501

        :return: The nps of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._nps

    @nps.setter
    def nps(self, nps):
        """Sets the nps of this VoiceCallLight.

        Net Promoter Score for the call.   # noqa: E501

        :param nps: The nps of this VoiceCallLight.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                nps is not None and nps < 0):  # noqa: E501
            raise ValueError("Invalid value for `nps`, must be a value greater than or equal to `0`")  # noqa: E501

        self._nps = nps

    @property
    def num_audio_channels(self):
        """Gets the num_audio_channels of this VoiceCallLight.  # noqa: E501

        Number of audio channels in the `recording`. 1 is mono, 2 is stereo  # noqa: E501

        :return: The num_audio_channels of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._num_audio_channels

    @num_audio_channels.setter
    def num_audio_channels(self, num_audio_channels):
        """Sets the num_audio_channels of this VoiceCallLight.

        Number of audio channels in the `recording`. 1 is mono, 2 is stereo  # noqa: E501

        :param num_audio_channels: The num_audio_channels of this VoiceCallLight.  # noqa: E501
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
    def num_segments(self):
        """Gets the num_segments of this VoiceCallLight.  # noqa: E501

        Number of segments in this call (bot, agent, or system segments). The segments themselves are not part of this record.   # noqa: E501

        :return: The num_segments of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._num_segments

    @num_segments.setter
    def num_segments(self, num_segments):
        """Sets the num_segments of this VoiceCallLight.

        Number of segments in this call (bot, agent, or system segments). The segments themselves are not part of this record.   # noqa: E501

        :param num_segments: The num_segments of this VoiceCallLight.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                num_segments is not None and num_segments < 0):  # noqa: E501
            raise ValueError("Invalid value for `num_segments`, must be a value greater than or equal to `0`")  # noqa: E501

        self._num_segments = num_segments

    @property
    def num_spk_channels(self):
        """Gets the num_spk_channels of this VoiceCallLight.  # noqa: E501

        Number of speaker channels in the `recording`.  # noqa: E501

        :return: The num_spk_channels of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._num_spk_channels

    @num_spk_channels.setter
    def num_spk_channels(self, num_spk_channels):
        """Sets the num_spk_channels of this VoiceCallLight.

        Number of speaker channels in the `recording`.  # noqa: E501

        :param num_spk_channels: The num_spk_channels of this VoiceCallLight.  # noqa: E501
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
        """Gets the originating_call_id of this VoiceCallLight.  # noqa: E501

        Id of the originating call. Set on a call that was launched by a Warm Call Transfer.   # noqa: E501

        :return: The originating_call_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._originating_call_id

    @originating_call_id.setter
    def originating_call_id(self, originating_call_id):
        """Sets the originating_call_id of this VoiceCallLight.

        Id of the originating call. Set on a call that was launched by a Warm Call Transfer.   # noqa: E501

        :param originating_call_id: The originating_call_id of this VoiceCallLight.  # noqa: E501
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
    def outbound_rtp_quality(self):
        """Gets the outbound_rtp_quality of this VoiceCallLight.  # noqa: E501

        RTP quality metrics for outbound audio stream obtained from CDR records.   # noqa: E501

        :return: The outbound_rtp_quality of this VoiceCallLight.  # noqa: E501
        :rtype: RtpQuality
        """
        return self._outbound_rtp_quality

    @outbound_rtp_quality.setter
    def outbound_rtp_quality(self, outbound_rtp_quality):
        """Sets the outbound_rtp_quality of this VoiceCallLight.

        RTP quality metrics for outbound audio stream obtained from CDR records.   # noqa: E501

        :param outbound_rtp_quality: The outbound_rtp_quality of this VoiceCallLight.  # noqa: E501
        :type: RtpQuality
        """

        self._outbound_rtp_quality = outbound_rtp_quality

    @property
    def progress_phase(self):
        """Gets the progress_phase of this VoiceCallLight.  # noqa: E501


        :return: The progress_phase of this VoiceCallLight.  # noqa: E501
        :rtype: ProgressPhase
        """
        return self._progress_phase

    @progress_phase.setter
    def progress_phase(self, progress_phase):
        """Sets the progress_phase of this VoiceCallLight.


        :param progress_phase: The progress_phase of this VoiceCallLight.  # noqa: E501
        :type: ProgressPhase
        """

        self._progress_phase = progress_phase

    @property
    def queue(self):
        """Gets the queue of this VoiceCallLight.  # noqa: E501


        :return: The queue of this VoiceCallLight.  # noqa: E501
        :rtype: Queue
        """
        return self._queue

    @queue.setter
    def queue(self, queue):
        """Sets the queue of this VoiceCallLight.


        :param queue: The queue of this VoiceCallLight.  # noqa: E501
        :type: Queue
        """

        self._queue = queue

    @property
    def queue_wait_ms(self):
        """Gets the queue_wait_ms of this VoiceCallLight.  # noqa: E501

        Time the caller spent waiting in the ACD queue, in milliseconds (queue only, excluding IVR time). Set for abandoned calls.   # noqa: E501

        :return: The queue_wait_ms of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._queue_wait_ms

    @queue_wait_ms.setter
    def queue_wait_ms(self, queue_wait_ms):
        """Sets the queue_wait_ms of this VoiceCallLight.

        Time the caller spent waiting in the ACD queue, in milliseconds (queue only, excluding IVR time). Set for abandoned calls.   # noqa: E501

        :param queue_wait_ms: The queue_wait_ms of this VoiceCallLight.  # noqa: E501
        :type: int
        """

        self._queue_wait_ms = queue_wait_ms

    @property
    def recompute_phase(self):
        """Gets the recompute_phase of this VoiceCallLight.  # noqa: E501

        Phase of the recompute process. + `requested` - recompute has been requested + `queued` - recompute is in the queue (ready to be processed) + `processing` - recompute is being processed + `completed` - recompute has been completed + `error` - recompute has failed   # noqa: E501

        :return: The recompute_phase of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._recompute_phase

    @recompute_phase.setter
    def recompute_phase(self, recompute_phase):
        """Sets the recompute_phase of this VoiceCallLight.

        Phase of the recompute process. + `requested` - recompute has been requested + `queued` - recompute is in the queue (ready to be processed) + `processing` - recompute is being processed + `completed` - recompute has been completed + `error` - recompute has failed   # noqa: E501

        :param recompute_phase: The recompute_phase of this VoiceCallLight.  # noqa: E501
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
    def recording(self):
        """Gets the recording of this VoiceCallLight.  # noqa: E501

        Data UUID - reference to original (unredacted) call recording in Voicegain Data Store.   # noqa: E501

        :return: The recording of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._recording

    @recording.setter
    def recording(self, recording):
        """Sets the recording of this VoiceCallLight.

        Data UUID - reference to original (unredacted) call recording in Voicegain Data Store.   # noqa: E501

        :param recording: The recording of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._recording = recording

    @property
    def reference_number(self):
        """Gets the reference_number of this VoiceCallLight.  # noqa: E501

        Caller-facing reference number that the voicebot generates and reads out to the caller (e.g. `CASEY2509241520`). If a call produced more than one, they are returned as a single comma-separated string.</br> It is a copy of the `referenceNumber` entry of the call's `aivrVars`. The `aivrVars` themselves are not part of this record.</br> Absent for agent-only calls, which have no voicebot part.   # noqa: E501

        :return: The reference_number of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._reference_number

    @reference_number.setter
    def reference_number(self, reference_number):
        """Sets the reference_number of this VoiceCallLight.

        Caller-facing reference number that the voicebot generates and reads out to the caller (e.g. `CASEY2509241520`). If a call produced more than one, they are returned as a single comma-separated string.</br> It is a copy of the `referenceNumber` entry of the call's `aivrVars`. The `aivrVars` themselves are not part of this record.</br> Absent for agent-only calls, which have no voicebot part.   # noqa: E501

        :param reference_number: The reference_number of this VoiceCallLight.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                reference_number is not None and len(reference_number) > 128):
            raise ValueError("Invalid value for `reference_number`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                reference_number is not None and len(reference_number) < 1):
            raise ValueError("Invalid value for `reference_number`, length must be greater than or equal to `1`")  # noqa: E501

        self._reference_number = reference_number

    @property
    def sa_session_id(self):
        """Gets the sa_session_id of this VoiceCallLight.  # noqa: E501

        Reference to Speech Analytics session.   # noqa: E501

        :return: The sa_session_id of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._sa_session_id

    @sa_session_id.setter
    def sa_session_id(self, sa_session_id):
        """Sets the sa_session_id of this VoiceCallLight.

        Reference to Speech Analytics session.   # noqa: E501

        :param sa_session_id: The sa_session_id of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._sa_session_id = sa_session_id

    @property
    def score(self):
        """Gets the score of this VoiceCallLight.  # noqa: E501

        **Final** QA score from the Call Review. It becomes the human-audited score once a manual audit is completed. Same value as `score` in the Voice Call record.   # noqa: E501

        :return: The score of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this VoiceCallLight.

        **Final** QA score from the Call Review. It becomes the human-audited score once a manual audit is completed. Same value as `score` in the Voice Call record.   # noqa: E501

        :param score: The score of this VoiceCallLight.  # noqa: E501
        :type: float
        """

        self._score = score

    @property
    def sentiment(self):
        """Gets the sentiment of this VoiceCallLight.  # noqa: E501

        **Deprecated** — use `sentiments[speaker=caller].average` instead.</br> Call average sentiment for the Caller channel.   # noqa: E501

        :return: The sentiment of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """Sets the sentiment of this VoiceCallLight.

        **Deprecated** — use `sentiments[speaker=caller].average` instead.</br> Call average sentiment for the Caller channel.   # noqa: E501

        :param sentiment: The sentiment of this VoiceCallLight.  # noqa: E501
        :type: float
        """

        self._sentiment = sentiment

    @property
    def sentiments(self):
        """Gets the sentiments of this VoiceCallLight.  # noqa: E501

        Sentiment values for speakers. Only one value for each speaker type is present.  # noqa: E501

        :return: The sentiments of this VoiceCallLight.  # noqa: E501
        :rtype: list[SpeakerSentimentItem]
        """
        return self._sentiments

    @sentiments.setter
    def sentiments(self, sentiments):
        """Sets the sentiments of this VoiceCallLight.

        Sentiment values for speakers. Only one value for each speaker type is present.  # noqa: E501

        :param sentiments: The sentiments of this VoiceCallLight.  # noqa: E501
        :type: list[SpeakerSentimentItem]
        """

        self._sentiments = sentiments

    @property
    def spawned_calls(self):
        """Gets the spawned_calls of this VoiceCallLight.  # noqa: E501

        List of callIds of calls that were spawned from this call by a Warm Call Transfer.   # noqa: E501

        :return: The spawned_calls of this VoiceCallLight.  # noqa: E501
        :rtype: list[str]
        """
        return self._spawned_calls

    @spawned_calls.setter
    def spawned_calls(self, spawned_calls):
        """Sets the spawned_calls of this VoiceCallLight.

        List of callIds of calls that were spawned from this call by a Warm Call Transfer.   # noqa: E501

        :param spawned_calls: The spawned_calls of this VoiceCallLight.  # noqa: E501
        :type: list[str]
        """

        self._spawned_calls = spawned_calls

    @property
    def start_time(self):
        """Gets the start_time of this VoiceCallLight.  # noqa: E501

        start time of the call (UTC)  # noqa: E501

        :return: The start_time of this VoiceCallLight.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this VoiceCallLight.

        start time of the call (UTC)  # noqa: E501

        :param start_time: The start_time of this VoiceCallLight.  # noqa: E501
        :type: datetime
        """

        self._start_time = start_time

    @property
    def tags(self):
        """Gets the tags of this VoiceCallLight.  # noqa: E501

        Tags attached to the call  # noqa: E501

        :return: The tags of this VoiceCallLight.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this VoiceCallLight.

        Tags attached to the call  # noqa: E501

        :param tags: The tags of this VoiceCallLight.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def team(self):
        """Gets the team of this VoiceCallLight.  # noqa: E501

        Id of the UserGroup of type Team that the call's Agent belongs to.   # noqa: E501

        :return: The team of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._team

    @team.setter
    def team(self, team):
        """Sets the team of this VoiceCallLight.

        Id of the UserGroup of type Team that the call's Agent belongs to.   # noqa: E501

        :param team: The team of this VoiceCallLight.  # noqa: E501
        :type: str
        """

        self._team = team

    @property
    def topics(self):
        """Gets the topics of this VoiceCallLight.  # noqa: E501

        All topics discovered  # noqa: E501

        :return: The topics of this VoiceCallLight.  # noqa: E501
        :rtype: list[str]
        """
        return self._topics

    @topics.setter
    def topics(self, topics):
        """Sets the topics of this VoiceCallLight.

        All topics discovered  # noqa: E501

        :param topics: The topics of this VoiceCallLight.  # noqa: E501
        :type: list[str]
        """

        self._topics = topics

    @property
    def transfer_time(self):
        """Gets the transfer_time of this VoiceCallLight.  # noqa: E501

        Time (UTC) at which the call that the voicebot transferred was answered by the call center: `startTime` plus the time of the `CC_ANSWER` marker of the call.</br> Present only if the call has an `aivrTransferDestType` and a `CC_ANSWER` marker. The markers themselves are not part of this record.   # noqa: E501

        :return: The transfer_time of this VoiceCallLight.  # noqa: E501
        :rtype: datetime
        """
        return self._transfer_time

    @transfer_time.setter
    def transfer_time(self, transfer_time):
        """Sets the transfer_time of this VoiceCallLight.

        Time (UTC) at which the call that the voicebot transferred was answered by the call center: `startTime` plus the time of the `CC_ANSWER` marker of the call.</br> Present only if the call has an `aivrTransferDestType` and a `CC_ANSWER` marker. The markers themselves are not part of this record.   # noqa: E501

        :param transfer_time: The transfer_time of this VoiceCallLight.  # noqa: E501
        :type: datetime
        """

        self._transfer_time = transfer_time

    @property
    def unaudited_score(self):
        """Gets the unaudited_score of this VoiceCallLight.  # noqa: E501

        QA score of the original, pre-audit Call Review Answers. It is never changed by an audit. Same value as `unauditedScore` in the Voice Call record.   # noqa: E501

        :return: The unaudited_score of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._unaudited_score

    @unaudited_score.setter
    def unaudited_score(self, unaudited_score):
        """Sets the unaudited_score of this VoiceCallLight.

        QA score of the original, pre-audit Call Review Answers. It is never changed by an audit. Same value as `unauditedScore` in the Voice Call record.   # noqa: E501

        :param unaudited_score: The unaudited_score of this VoiceCallLight.  # noqa: E501
        :type: float
        """

        self._unaudited_score = unaudited_score

    @property
    def version(self):
        """Gets the version of this VoiceCallLight.  # noqa: E501

        Version of the call. Version 1 uses `/sa` API for processing audio and version 2 uses `/sa/offline` API.  # noqa: E501

        :return: The version of this VoiceCallLight.  # noqa: E501
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this VoiceCallLight.

        Version of the call. Version 1 uses `/sa` API for processing audio and version 2 uses `/sa/offline` API.  # noqa: E501

        :param version: The version of this VoiceCallLight.  # noqa: E501
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
    def voicebot_duration(self):
        """Gets the voicebot_duration of this VoiceCallLight.  # noqa: E501

        Duration of the voicebot part of the call in seconds. It can be a fraction of a second.</br> It is equal to `duration` unless the call was handed off or warm-transferred. In that case it is the time from the start of the call to the hand-off.   # noqa: E501

        :return: The voicebot_duration of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._voicebot_duration

    @voicebot_duration.setter
    def voicebot_duration(self, voicebot_duration):
        """Sets the voicebot_duration of this VoiceCallLight.

        Duration of the voicebot part of the call in seconds. It can be a fraction of a second.</br> It is equal to `duration` unless the call was handed off or warm-transferred. In that case it is the time from the start of the call to the hand-off.   # noqa: E501

        :param voicebot_duration: The voicebot_duration of this VoiceCallLight.  # noqa: E501
        :type: float
        """

        self._voicebot_duration = voicebot_duration

    @property
    def voicebot_vars(self):
        """Gets the voicebot_vars of this VoiceCallLight.  # noqa: E501


        :return: The voicebot_vars of this VoiceCallLight.  # noqa: E501
        :rtype: VoiceCallLightVoicebotVars
        """
        return self._voicebot_vars

    @voicebot_vars.setter
    def voicebot_vars(self, voicebot_vars):
        """Sets the voicebot_vars of this VoiceCallLight.


        :param voicebot_vars: The voicebot_vars of this VoiceCallLight.  # noqa: E501
        :type: VoiceCallLightVoicebotVars
        """

        self._voicebot_vars = voicebot_vars

    @property
    def voicemail_duration(self):
        """Gets the voicemail_duration of this VoiceCallLight.  # noqa: E501

        Present only if a voicemail was left.</br> Duration of the voicemail in seconds.   # noqa: E501

        :return: The voicemail_duration of this VoiceCallLight.  # noqa: E501
        :rtype: float
        """
        return self._voicemail_duration

    @voicemail_duration.setter
    def voicemail_duration(self, voicemail_duration):
        """Sets the voicemail_duration of this VoiceCallLight.

        Present only if a voicemail was left.</br> Duration of the voicemail in seconds.   # noqa: E501

        :param voicemail_duration: The voicemail_duration of this VoiceCallLight.  # noqa: E501
        :type: float
        """

        self._voicemail_duration = voicemail_duration

    @property
    def voicemail_uuid(self):
        """Gets the voicemail_uuid of this VoiceCallLight.  # noqa: E501

        Present only if a voicemail was left.</br> Reference to the data object with the voicemail recording.   # noqa: E501

        :return: The voicemail_uuid of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._voicemail_uuid

    @voicemail_uuid.setter
    def voicemail_uuid(self, voicemail_uuid):
        """Sets the voicemail_uuid of this VoiceCallLight.

        Present only if a voicemail was left.</br> Reference to the data object with the voicemail recording.   # noqa: E501

        :param voicemail_uuid: The voicemail_uuid of this VoiceCallLight.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                voicemail_uuid is not None and len(voicemail_uuid) > 48):
            raise ValueError("Invalid value for `voicemail_uuid`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                voicemail_uuid is not None and len(voicemail_uuid) < 16):
            raise ValueError("Invalid value for `voicemail_uuid`, length must be greater than or equal to `16`")  # noqa: E501

        self._voicemail_uuid = voicemail_uuid

    @property
    def who_hung_up(self):
        """Gets the who_hung_up of this VoiceCallLight.  # noqa: E501

        Who hung up the call  # noqa: E501

        :return: The who_hung_up of this VoiceCallLight.  # noqa: E501
        :rtype: str
        """
        return self._who_hung_up

    @who_hung_up.setter
    def who_hung_up(self, who_hung_up):
        """Sets the who_hung_up of this VoiceCallLight.

        Who hung up the call  # noqa: E501

        :param who_hung_up: The who_hung_up of this VoiceCallLight.  # noqa: E501
        :type: str
        """
        allowed_values = ["us", "other_party"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and who_hung_up not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `who_hung_up` ({0}), must be one of {1}"  # noqa: E501
                .format(who_hung_up, allowed_values)
            )

        self._who_hung_up = who_hung_up

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
        if not isinstance(other, VoiceCallLight):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, VoiceCallLight):
            return True

        return self.to_dict() != other.to_dict()
