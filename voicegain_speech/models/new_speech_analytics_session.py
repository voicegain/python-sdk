# coding: utf-8

"""
    Voicegain API v1

    # New  [Telephony Bot API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + Telephony Bot APIs which in addition to speech-to-text allow for control of real-time communications (RTC) session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Web Console](https://console.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).  # Context Defaults  Most of the API requests are made within a specific Context identified by the JWT being used. Each Context has some API (mainly ASR API) related settings which can be set from the Web Console, see image below: ![Context Settings](https://github.com/voicegain/platform/raw/master/images/Context-Speech-Recognition-Settings.PNG)  These settings override the corresponding API default values.  For example, if `noInputTimeout` default is 15000, but the Context 'No Input Timeout' setting is 30000,  and no value is provided in the API request for `noInputTimeout` field, then the API request will run with `noInputTimeout` of 30000.    # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Specifically, 2x OFF-LINE use case is not supported because of how the task queue processor is implemented. To transcribe 2-channels separately in OFF-LINE mode you will need to make 2 separate OFF-LINE transcription requests. Please, let us know if you think you have a valid use case for other combinations.  # Telephony Bot API  (previously called RTC Callback API, where RTC stands for Real Time Communications)   Voicegain Telephony Bot APIs allows you to build conversational voice-enabled applications (e.g. IVRs, Voicebots) over an RTC session (a telephone call for example).  See this blog post for an overview of how this API works: [Voicegain releases Telephony Bot APIs for telephony IVRs and bots](https://www.voicegain.ai/post/rtc-callback-api-released)  Telephony Bot API is a callback API - Voicegain platform makes HTTP request to your app with information about the result of e.g. latest recognition and in response you provide instruction for the next step of the conversation. See the spec of these requests [here](#tag/aivr-callback).  # Speech Analytics API  Voicegain Speech Analytics analyzes both the transcript and the audio (typically of a telephone call).  The results are returned per channel (real or diarized) except where the recognized entities span more than one channel. For entities where it is applicable we return the location in the audio (start and end time) and the transcript (index of the words).  ## Capabilities of Speech Analytics  Voicegain Speech Analytics can identify/compute the following: + **named entities** - (NER i.e. named entity recognition) - the following entities are recognized:   + ADDRESS - Postal address.   + CARDINAL - Numerals that do not fall under another type.   + CC - Credit Card   + DATE - Absolute or relative dates or periods.   + EMAIL - Email address   + EVENT - Named hurricanes, battles, wars, sports events, etc.   + FAC - Buildings, airports, highways, bridges, etc.   + GPE - Countries, cities, states.   + LANGUAGE - Any named language.   + LAW - Named documents made into laws.   + NORP - Nationalities or religious or political groups.   + MONEY - Monetary values, including unit.   + ORDINAL - \"first\", \"second\", etc.   + ORG - Companies, agencies, institutions, etc.   + PERCENT - Percentage, including \"%\".   + PERSON - People, including fictional.   + PHONE - Phone number.   + PRODUCT - Objects, vehicles, foods, etc. (Not services.)   + QUANTITY - Measurements, as of weight or distance.   + SSN - Social Security number   + TIME - Times smaller than a day.   + WORK_OF_ART - Titles of books, songs, etc.   + ZIP - Zip Code (if not part of an Address)    In addition to returning the named entity itself, we return the sub-concepts within entity, e.g. for ADDRESs we will return state (e.g. TX) and zip code if found.  + **keywords** - these are single words or short phrases e.g. company or product names.    Currently, keywords are detected using simple matching using stemming - so e.g. a keyword \"cancel\" will match \"cancellation\".    In near future we will support \"smart expansion\" which will also match synonyms while paying attention to the correct meaning of the word.     In addition to keywords we return keyword groups, e.g. several company name keywords can be combined into a `Competition` keyword group.  + **phrases (intent)** - allows for detection of phrases/intents that match the meaning of the phrases specified in the example training Sections).</br>   For each detected phrase/intent the system will also return entities and keywords contained in the phrase, if configured to do so.   For example, transcript \"Hello, my name is Lucy\" may match phrase/intent \"INTRODUCTION\" with the NER of PERSON and value \"Lucy\".       The configuration for phrase/intent detection takes the following parameters:   + _list_ of example phrases - each phrase has a sensitivity value which determines how close it has to match (sensitivity of 1.0 requires the closest match, sensitivity of 0.0 allows for vague matches).   + _regex_ - optional regex phrases to augment the examples - these require exact match   + _slots_ - types on named entities and keywords to be recognized within the phrase/intent</br>     Note: support for slots of same type but different meaning will be added in the future.     Currently it is possible e.g. to recognize places (GPE) but not possible to distinguish e.g. between types of them, like departure or destination place.   + _location_ - this narrows down where the phrase/match must occur - the options are:     + channel - agent or caller      + time in the call - from the start or from the end     + dialogue act - require the phrase to be part of a specified dialogue act, see https://web.stanford.edu/~jurafsky/ws97/manual.august1.html, first table, column SWBD    + **phrase groups** - computed across all channels - this is more powerful than keyword groups as it can be configured to require all phrases/intents in the groups to be present in any or fixed order.   One use case would be to detect a pair of a question and a confirming answer - for example to determine call resolution: \"Have I answered all your question?\", \"Yes\". + **criteria** - computed by rules/conditions looking at the following parameters:   + _call metrics_   + _regex_ - match of the text of the transcript   + _keywords_ - any keywords or keyword groups   + _NER_ - any named entities   + _phrases_ - any phrases/intents or phrase groups   + _dialogElements_ - selection of custom hardcoded rules that may accomplish tasks not possible with other conditions    The individual rules/conditions can be further narrowed down using filters like:   + _channel_ - agent or caller    + _time in the call_ - from the start or from the end    Multiple rules can be combined to form a logical AND expression.   Finally, the individual rules can be negated so that the absence of certain events is considered as a positive match.    When Criteria are satisfied then the system provides a detailed justification information. + **topics** - computed from text across all channels - assigns to the call a set of likely topics with their scores.    A topic classifier is built in a separate step using a corpus. The build process requires manual labeling of the topics.    For each call, the entire transcript is fed to the topic classifier and we get back the set of detected topics and their scores (in the 0..1 range).   It is useful e.g. for separating Billing calls from Troubleshooting calls from Account Change calls, etc.  + **summary** - computed from text across all channels - provides a summary of the call in a form of a set of sentences.   These may either be key sentences directly pulled from the transcript, or sentences generated by summarizing entire call or sections of the call.  + **sentiment** - computed from text - standard call sentiment as used in Call Center Speech Analytics.   Returns sentiment values from -1.0 (negative/mad/angry) to +1.0 (positive/happy/satisfied) + **mood** - computed from text - can distinguish 6 moods:   + neutral    + anger    + disgust    + fear    + happiness   + sadness   + surprise     Values are returned as a map from mood enum values to a number in (0.0, 1.0) range - multiple moods can be detected in the same place in the transcript in varying degrees. + **gender** - computed to audio - Estimates the gender of the speaker as far as it is possible to do it from the voice alone. + **word cloud** - returns word cloud data (map from words/phrases to frequencies) - the algorithm uses: stop word removal, stemming, frequent phrase detection. + **call metrics** - these are simple metrics computed from the audio and the transcript    + _silence_ - amount of silence in the call   + _talk_ - talk streaks for each of the channels   + _overtalk_ - amount of time when call participants talk over ove another   + _energy_ - the volume of the call and the variation   + _pitch_ - the pitch (frequency of the voice) and the variation  Voicegain allows for configuring Speech Analytics processing by preparing a Speech Analytics Configuration which is basically a selection of the capabilities mentioned above plus configuration of variable elements like keywords, phrases, etc.  </br> You can configure Speech Analytics using **[/sa/config API](#operation/saConfigPost)**   Once the configuration is complete you can launch speech transcription and analytics session using the **[/sa API](#operation/saPost)**   ### Offline vs Real-Time Speech Analytics  Speech audio can be transcribed and the analyzed in one of two modes: + **OFF-LINE** - audio will be queued for transcription, then transcribed, and both the audio and transcript will pass through various speech analytics algorithms according to the specified configuration.   The results of transcription and speech analytics can be retrieved using the [GET **/sa/{sid}/data** API](#operation/saDataGet)   + **REAL-TIME** - audio will immediately be submitted to real-time transcription and the stream of transcribed words will be fed to real-time speech analytics.    The results of transcription and speech analytics will be returned over websocket as soon as they are available.    The format of the returned messages is defined [here](#operation/saWebsocketPayload).     The results will also be available afterwards using the [GET **/sa/{sid}/data** API](#operation/saDataGet)  ## Agent Review Form  Data computed by Speech Analytics can be used to automatically fill/answer questions of the Call/Agent Review Form.   The automatic answers can be obtained based on previously defined Criteria (see above).  When Criteria are satisfied then the system provides a detailed justification information so it is easily possible to verify that the automated answer on a Review Form was correct.  ## PII Redaction  Being able to recognize occurrence of certain elements in the transcript allows us to remove them from both the text and the audio - this is called PII Redaction where PII stands for Personally Identifiable Information.  Currently, PII Redaction is limited to named entities (NER).  User can select any NER type detected by [Speech Analytics](#section/Speech-Analytics-API/Capabilities-of-Speech-Analytics) to be replaced by a specified placeholder in the text and by silence in the audio.  If your Enterprise account with Voicegain is setup with PCI-DSS compliance option, then PII Redaction of credit card numbers is enabled by default and cannot be disabled.    # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Rate Limiting  Access to Voicegain resources is controlled using the following limit settings on the account.  Newly created accounts get the limit values listed below.  If you need higher limits please contact us at support@voicegain.ai  The limits apply to the use of the Voicegain Platform in the Cloud.  On the Edge, the limits will be determined by the type of license you will purchase.  ## Types of Rate Limits  | Limit | default value | description | |---|---|---| | apiRequestLimitPerMinute | 75 | Basic rate limit with a fixed window of 1 minute applying to all API requests. Requests to /data API will be counted at 10x other requests. | | apiRequestLimitPerHour | 2000 | Basic rate limit with a fixed window of 1 hour applying to all API requests. Requests to /data API will be counted at 10x other requests. | | asrConcurrencyLimit | 4 | Limit on number of concurrent ASR requests. Does not apply to OFF-LINE requests. | | offlineQueueSizeLimit | 10 | Maximum number of OFF-LINE transcription jobs that may be submitted to the queue. | | offlineThroughputLimitPerHour | 4 | Maximum number of hours of audio that can be processed by OFF-LINE transcription within 1 hour. Note: For Edge deployment the limit interval is per day instead of per hour. | | offlineWorkerLimit | 2 | Maximum number of OFF-LINE transcription job workers that will be used to process the account audio. |  For API requests running longer that the rate limit window length, the request count will be applied to both the window when the request started and the window when the request finished.   Every HTTP API request will return several rate-limit related headers in its response.  The header values show the applicable limit, the remaining request count in the current window, and the number of seconds to when the limit resets. For example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 1 RateLimit-Reset: 7 ```  ## When Rate Limits are Hit  If a rate-limit is hit then [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) HTTP error code will be returned. The response headers will additionally include Retry-After value, for example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 0 RateLimit-Reset: 6 Retry-After: 6 ``` If `asrConcurrencyLimit` is hit then the response headers will contain:  ``` X-ResourceLimit-Type: ASR-Concurrency X-ResourceLimit-Limit: 4 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ``` Note that we return a superset of values that are returned for a basic API request limit.  This will allow a client code that was written to handle basic rate limiting to be able to handle concurrency limiting too.  Note also that for the concurrency limit the Retry-After value is approximate and is not guaranteed - so client code may have to retry multiple timers. (We will return increasing back-off Retry-After values in case of the limit being hit multiple times.)   In case of `offlineQueueSizeLimit` limit we will return, for example:  ``` X-ResourceLimit-Type: Offline-Queue-Size X-ResourceLimit-Limit: 10 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ```   # Pagination  For methods that support pagination Voicegain has standardized on using the following query parameters: + page={page number} + per_page={number items per page}  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?page=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=2&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=3&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"last\" ```   # noqa: E501

    The version of the OpenAPI document: 1.58.1 - updated May 24, 2022
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from voicegain_speech.configuration import Configuration


class NewSpeechAnalyticsSession(object):
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
        'asr': 'AsrSettingsTranscriptionSA',
        'async_mode': 'AsyncModeSpeechAnalytics',
        'audio': 'AudioInputAsync',
        'call_review_config': 'str',
        'creator': 'str',
        'label': 'str',
        'metadata': 'list[NameValuePair]',
        'notify_stomp_topic': 'str',
        'persist': 'float',
        'sa_config': 'str',
        'speaker_channels': 'list[SpeechAnalyticsChannel]',
        'tags': 'list[str]',
        'topic_discovery_config': 'str',
        'virtual_dual_channel_enabled': 'bool'
    }

    attribute_map = {
        'asr': 'asr',
        'async_mode': 'asyncMode',
        'audio': 'audio',
        'call_review_config': 'callReviewConfig',
        'creator': 'creator',
        'label': 'label',
        'metadata': 'metadata',
        'notify_stomp_topic': 'notifyStompTopic',
        'persist': 'persist',
        'sa_config': 'saConfig',
        'speaker_channels': 'speakerChannels',
        'tags': 'tags',
        'topic_discovery_config': 'topicDiscoveryConfig',
        'virtual_dual_channel_enabled': 'virtualDualChannelEnabled'
    }

    def __init__(self, asr=None, async_mode=None, audio=None, call_review_config=None, creator=None, label=None, metadata=None, notify_stomp_topic=None, persist=3600000, sa_config=None, speaker_channels=None, tags=None, topic_discovery_config=None, virtual_dual_channel_enabled=True, local_vars_configuration=None):  # noqa: E501
        """NewSpeechAnalyticsSession - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._asr = None
        self._async_mode = None
        self._audio = None
        self._call_review_config = None
        self._creator = None
        self._label = None
        self._metadata = None
        self._notify_stomp_topic = None
        self._persist = None
        self._sa_config = None
        self._speaker_channels = None
        self._tags = None
        self._topic_discovery_config = None
        self._virtual_dual_channel_enabled = None
        self.discriminator = None

        if asr is not None:
            self.asr = asr
        if async_mode is not None:
            self.async_mode = async_mode
        if audio is not None:
            self.audio = audio
        if call_review_config is not None:
            self.call_review_config = call_review_config
        if creator is not None:
            self.creator = creator
        if label is not None:
            self.label = label
        if metadata is not None:
            self.metadata = metadata
        if notify_stomp_topic is not None:
            self.notify_stomp_topic = notify_stomp_topic
        if persist is not None:
            self.persist = persist
        self.sa_config = sa_config
        if speaker_channels is not None:
            self.speaker_channels = speaker_channels
        if tags is not None:
            self.tags = tags
        if topic_discovery_config is not None:
            self.topic_discovery_config = topic_discovery_config
        if virtual_dual_channel_enabled is not None:
            self.virtual_dual_channel_enabled = virtual_dual_channel_enabled

    @property
    def asr(self):
        """Gets the asr of this NewSpeechAnalyticsSession.  # noqa: E501


        :return: The asr of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: AsrSettingsTranscriptionSA
        """
        return self._asr

    @asr.setter
    def asr(self, asr):
        """Sets the asr of this NewSpeechAnalyticsSession.


        :param asr: The asr of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: AsrSettingsTranscriptionSA
        """

        self._asr = asr

    @property
    def async_mode(self):
        """Gets the async_mode of this NewSpeechAnalyticsSession.  # noqa: E501


        :return: The async_mode of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: AsyncModeSpeechAnalytics
        """
        return self._async_mode

    @async_mode.setter
    def async_mode(self, async_mode):
        """Sets the async_mode of this NewSpeechAnalyticsSession.


        :param async_mode: The async_mode of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: AsyncModeSpeechAnalytics
        """

        self._async_mode = async_mode

    @property
    def audio(self):
        """Gets the audio of this NewSpeechAnalyticsSession.  # noqa: E501


        :return: The audio of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: AudioInputAsync
        """
        return self._audio

    @audio.setter
    def audio(self, audio):
        """Sets the audio of this NewSpeechAnalyticsSession.


        :param audio: The audio of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: AudioInputAsync
        """

        self._audio = audio

    @property
    def call_review_config(self):
        """Gets the call_review_config of this NewSpeechAnalyticsSession.  # noqa: E501

        (optional) id of the Call Review (Score Card) configuration to use.  The Call Review Config will be used to guide the generation of autopopulated Call Review Answers.   # noqa: E501

        :return: The call_review_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._call_review_config

    @call_review_config.setter
    def call_review_config(self, call_review_config):
        """Sets the call_review_config of this NewSpeechAnalyticsSession.

        (optional) id of the Call Review (Score Card) configuration to use.  The Call Review Config will be used to guide the generation of autopopulated Call Review Answers.   # noqa: E501

        :param call_review_config: The call_review_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                call_review_config is not None and len(call_review_config) > 48):
            raise ValueError("Invalid value for `call_review_config`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                call_review_config is not None and len(call_review_config) < 16):
            raise ValueError("Invalid value for `call_review_config`, length must be greater than or equal to `16`")  # noqa: E501

        self._call_review_config = call_review_config

    @property
    def creator(self):
        """Gets the creator of this NewSpeechAnalyticsSession.  # noqa: E501

        (optional) Id of the user who starts this Speech Analytics session. If invoked from Web UI then we will use identity of the logged-in user.   # noqa: E501

        :return: The creator of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this NewSpeechAnalyticsSession.

        (optional) Id of the user who starts this Speech Analytics session. If invoked from Web UI then we will use identity of the logged-in user.   # noqa: E501

        :param creator: The creator of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                creator is not None and len(creator) > 48):
            raise ValueError("Invalid value for `creator`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                creator is not None and len(creator) < 16):
            raise ValueError("Invalid value for `creator`, length must be greater than or equal to `16`")  # noqa: E501

        self._creator = creator

    @property
    def label(self):
        """Gets the label of this NewSpeechAnalyticsSession.  # noqa: E501

        Short labels to assign to the speech Analytics session. May be displayed in a table to make identifying a session easier.  # noqa: E501

        :return: The label of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this NewSpeechAnalyticsSession.

        Short labels to assign to the speech Analytics session. May be displayed in a table to make identifying a session easier.  # noqa: E501

        :param label: The label of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                label is not None and len(label) > 64):
            raise ValueError("Invalid value for `label`, length must be less than or equal to `64`")  # noqa: E501

        self._label = label

    @property
    def metadata(self):
        """Gets the metadata of this NewSpeechAnalyticsSession.  # noqa: E501

        Metadata passed with the request to async transcription, recognition, or Speech Analytics. Consist of a list of named string values. Names in the list have to be unique. If duplicates are provided then only the last one will be retained. </br> Will be returned in callback. For transcription and Speech Analytics, the metadata will be saved together with the result.   # noqa: E501

        :return: The metadata of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: list[NameValuePair]
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this NewSpeechAnalyticsSession.

        Metadata passed with the request to async transcription, recognition, or Speech Analytics. Consist of a list of named string values. Names in the list have to be unique. If duplicates are provided then only the last one will be retained. </br> Will be returned in callback. For transcription and Speech Analytics, the metadata will be saved together with the result.   # noqa: E501

        :param metadata: The metadata of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: list[NameValuePair]
        """

        self._metadata = metadata

    @property
    def notify_stomp_topic(self):
        """Gets the notify_stomp_topic of this NewSpeechAnalyticsSession.  # noqa: E501

        (optional) STOMP Topic name - if present then the entire POST /sa response will be sent over websocket to the specified STOMP topic.    # noqa: E501

        :return: The notify_stomp_topic of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._notify_stomp_topic

    @notify_stomp_topic.setter
    def notify_stomp_topic(self, notify_stomp_topic):
        """Sets the notify_stomp_topic of this NewSpeechAnalyticsSession.

        (optional) STOMP Topic name - if present then the entire POST /sa response will be sent over websocket to the specified STOMP topic.    # noqa: E501

        :param notify_stomp_topic: The notify_stomp_topic of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                notify_stomp_topic is not None and len(notify_stomp_topic) > 128):
            raise ValueError("Invalid value for `notify_stomp_topic`, length must be less than or equal to `128`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                notify_stomp_topic is not None and len(notify_stomp_topic) < 16):
            raise ValueError("Invalid value for `notify_stomp_topic`, length must be greater than or equal to `16`")  # noqa: E501

        self._notify_stomp_topic = notify_stomp_topic

    @property
    def persist(self):
        """Gets the persist of this NewSpeechAnalyticsSession.  # noqa: E501

        Time (in msec) to retain the result data after processing has completed.  Data can be retained indefinitely if value is -1.  As long as the persist has not expired the data will be available.</br> Note that there are charges for data stored in the Voicegain Cloud.         # noqa: E501

        :return: The persist of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: float
        """
        return self._persist

    @persist.setter
    def persist(self, persist):
        """Sets the persist of this NewSpeechAnalyticsSession.

        Time (in msec) to retain the result data after processing has completed.  Data can be retained indefinitely if value is -1.  As long as the persist has not expired the data will be available.</br> Note that there are charges for data stored in the Voicegain Cloud.         # noqa: E501

        :param persist: The persist of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                persist is not None and persist < -1):  # noqa: E501
            raise ValueError("Invalid value for `persist`, must be a value greater than or equal to `-1`")  # noqa: E501

        self._persist = persist

    @property
    def sa_config(self):
        """Gets the sa_config of this NewSpeechAnalyticsSession.  # noqa: E501

        id of the Speech Analytics configuration to use. If not provided then default SA Config for the context will be used.   # noqa: E501

        :return: The sa_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._sa_config

    @sa_config.setter
    def sa_config(self, sa_config):
        """Sets the sa_config of this NewSpeechAnalyticsSession.

        id of the Speech Analytics configuration to use. If not provided then default SA Config for the context will be used.   # noqa: E501

        :param sa_config: The sa_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and sa_config is None:  # noqa: E501
            raise ValueError("Invalid value for `sa_config`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sa_config is not None and len(sa_config) > 48):
            raise ValueError("Invalid value for `sa_config`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sa_config is not None and len(sa_config) < 16):
            raise ValueError("Invalid value for `sa_config`, length must be greater than or equal to `16`")  # noqa: E501

        self._sa_config = sa_config

    @property
    def speaker_channels(self):
        """Gets the speaker_channels of this NewSpeechAnalyticsSession.  # noqa: E501

        For **stereo** audio this is used to map audio channels to processing sessions and to identify which one is Agent.</br> For **mono** audio, specify just one session.  Diarization will be automatically turned on if `virtualDualChannelEnabled` is true.  Determination of which speaker is Agent will be attempted from the transcript. </br> Note, current version does not handle audio with more than 2 channels.   # noqa: E501

        :return: The speaker_channels of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: list[SpeechAnalyticsChannel]
        """
        return self._speaker_channels

    @speaker_channels.setter
    def speaker_channels(self, speaker_channels):
        """Sets the speaker_channels of this NewSpeechAnalyticsSession.

        For **stereo** audio this is used to map audio channels to processing sessions and to identify which one is Agent.</br> For **mono** audio, specify just one session.  Diarization will be automatically turned on if `virtualDualChannelEnabled` is true.  Determination of which speaker is Agent will be attempted from the transcript. </br> Note, current version does not handle audio with more than 2 channels.   # noqa: E501

        :param speaker_channels: The speaker_channels of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: list[SpeechAnalyticsChannel]
        """

        self._speaker_channels = speaker_channels

    @property
    def tags(self):
        """Gets the tags of this NewSpeechAnalyticsSession.  # noqa: E501

        Tags associated with the Speech Analytics session. Each tag is a string with max length of 64 characters.  # noqa: E501

        :return: The tags of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this NewSpeechAnalyticsSession.

        Tags associated with the Speech Analytics session. Each tag is a string with max length of 64 characters.  # noqa: E501

        :param tags: The tags of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def topic_discovery_config(self):
        """Gets the topic_discovery_config of this NewSpeechAnalyticsSession.  # noqa: E501

        (optional) id of the Topic Discovery configuration to use.  If not provided then default Topic Discovery Config for the context will be used.   # noqa: E501

        :return: The topic_discovery_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: str
        """
        return self._topic_discovery_config

    @topic_discovery_config.setter
    def topic_discovery_config(self, topic_discovery_config):
        """Sets the topic_discovery_config of this NewSpeechAnalyticsSession.

        (optional) id of the Topic Discovery configuration to use.  If not provided then default Topic Discovery Config for the context will be used.   # noqa: E501

        :param topic_discovery_config: The topic_discovery_config of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                topic_discovery_config is not None and len(topic_discovery_config) > 48):
            raise ValueError("Invalid value for `topic_discovery_config`, length must be less than or equal to `48`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                topic_discovery_config is not None and len(topic_discovery_config) < 16):
            raise ValueError("Invalid value for `topic_discovery_config`, length must be greater than or equal to `16`")  # noqa: E501

        self._topic_discovery_config = topic_discovery_config

    @property
    def virtual_dual_channel_enabled(self):
        """Gets the virtual_dual_channel_enabled of this NewSpeechAnalyticsSession.  # noqa: E501

        Applies only if the source audio is mono (1 channel).  This is intended to be used in cases where we want to process a call center call that was recorded in mono.</br> If audio is mono and `virtualDualChannelEnabled` is true then: + diarization will we set to `minSpeakers=2` and `maxSpeakers=2` + simulated (virtual) `multiChannelAudio` will be generated.   If `virtualDualChannelEnabled` is **false** then no matter what the setting of diarization is **no** `multiChannelAudio` will be generated.   # noqa: E501

        :return: The virtual_dual_channel_enabled of this NewSpeechAnalyticsSession.  # noqa: E501
        :rtype: bool
        """
        return self._virtual_dual_channel_enabled

    @virtual_dual_channel_enabled.setter
    def virtual_dual_channel_enabled(self, virtual_dual_channel_enabled):
        """Sets the virtual_dual_channel_enabled of this NewSpeechAnalyticsSession.

        Applies only if the source audio is mono (1 channel).  This is intended to be used in cases where we want to process a call center call that was recorded in mono.</br> If audio is mono and `virtualDualChannelEnabled` is true then: + diarization will we set to `minSpeakers=2` and `maxSpeakers=2` + simulated (virtual) `multiChannelAudio` will be generated.   If `virtualDualChannelEnabled` is **false** then no matter what the setting of diarization is **no** `multiChannelAudio` will be generated.   # noqa: E501

        :param virtual_dual_channel_enabled: The virtual_dual_channel_enabled of this NewSpeechAnalyticsSession.  # noqa: E501
        :type: bool
        """

        self._virtual_dual_channel_enabled = virtual_dual_channel_enabled

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
        if not isinstance(other, NewSpeechAnalyticsSession):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NewSpeechAnalyticsSession):
            return True

        return self.to_dict() != other.to_dict()
