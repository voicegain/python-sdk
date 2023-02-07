# coding: utf-8

"""
    Voicegain API v1

    # New  [Telephony Bot API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + Telephony Bot APIs which in addition to speech-to-text allow for control of real-time communications (RTC) session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Speech Analytics APIs (currently in **beta**) + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Web Console](https://console.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  When making Web APi request the JWT has to be included in the \"Authorization: Bearer\" header. For example, when using curl to make a request:  <pre>   curl -i -X POST \\   -H \"Content-Type: application/json\" \\   -H \"Accept: application/json\" \\   -H \"Authorization: Bearer eyJh......BOGCO70w\" \\   -d @data1.json \\   https://api.voicegain.ai/v1/asr/transcribe/async </pre>  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).  # Edge Deployment API URLs  When you are using Voicegain plaform deployed on Edge, the Web API urls will be different from those that are used in the Cloud (and given in the examples).  For example: * a Web API URL in the Cloud may be: https://api.voicegain.ai/v1/asr/transcribe/async  * but when deployed on Edge which e.g. has this IP:port 10.137.16.7:31680 and does not have SSL configured   * the URL for the same API will be http://10.137.16.7:31680/ascalon-web-api/asr/transcribe/async  * if deployed on Edge with SSL cert and IP:port 10.137.16.7:31443   * the URL for the same API will be https://10.137.16.7:31443/ascalon-web-api/asr/transcribe/async  The reason for this is that in the Cloud, the Web API service is on its own hostname, but on the Edge it has to share the hostname/IP with the Web Console  (which would e.g. have this URL: https://10.137.16.7:31443/customer-portal/)  # Context Defaults  Most of the API requests are made within a specific Context identified by the JWT being used. Each Context has some API (mainly ASR API) related settings which can be set from the Web Console, see image below: ![Context Settings](https://github.com/voicegain/platform/raw/master/images/Context-Speech-Recognition-Settings.PNG)  These settings override the corresponding API default values.  For example, if `noInputTimeout` default is 15000, but the Context 'No Input Timeout' setting is 30000,  and no value is provided in the API request for `noInputTimeout` field, then the API request will run with `noInputTimeout` of 30000.    # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes. + 2x REAL-TIME - for example for separately transcribing left and right channels of stereo audio  Other combinations of session types, including more than 2 sessions, are currently not supported.  Specifically, 2x OFF-LINE use case is not supported because of how the task queue processor is implemented. To transcribe 2-channels separately in OFF-LINE mode you will need to make 2 separate OFF-LINE transcription requests. Please, let us know if you think you have a valid use case for other combinations.  # Telephony Bot API  (previously called RTC Callback API, where RTC stands for Real Time Communications)   Voicegain Telephony Bot APIs allows you to build conversational voice-enabled applications (e.g. IVRs, Voicebots) over an RTC session (a telephone call for example).  See this blog post for an overview of how this API works: [Voicegain releases Telephony Bot APIs for telephony IVRs and bots](https://www.voicegain.ai/post/rtc-callback-api-released)  Telephony Bot API is a callback API - Voicegain platform makes HTTP request to your app with information about the result of e.g. latest recognition and in response you provide instruction for the next step of the conversation. See the spec of these requests [here](#tag/aivr-callback).  # Speech Analytics API  Voicegain Speech Analytics analyzes both the transcript and the audio (typically of a telephone call).  The results are returned per channel (real or diarized) except where the recognized entities span more than one channel. For entities where it is applicable we return the location in the audio (start and end time) and the transcript (index of the words).  ## Capabilities of Speech Analytics  Voicegain Speech Analytics can identify/compute the following: + **named entities** - (NER i.e. named entity recognition) - the following entities are recognized:   + ADDRESS - Postal address.   + CARDINAL - Numerals that do not fall under another type.   + CC - Credit Card   + DATE - Absolute or relative dates or periods.   + EMAIL - Email address   + EVENT - Named hurricanes, battles, wars, sports events, etc.   + FAC - Buildings, airports, highways, bridges, etc.   + GPE - Countries, cities, states.   + LANGUAGE - Any named language.   + LAW - Named documents made into laws.   + NORP - Nationalities or religious or political groups.   + MONEY - Monetary values, including unit.   + ORDINAL - \"first\", \"second\", etc.   + ORG - Companies, agencies, institutions, etc.   + PERCENT - Percentage, including \"%\".   + PERSON - People, including fictional.   + PHONE - Phone number.   + PRODUCT - Objects, vehicles, foods, etc. (Not services.)   + QUANTITY - Measurements, as of weight or distance.   + SSN - Social Security number   + TIME - Times smaller than a day.   + WORK_OF_ART - Titles of books, songs, etc.   + ZIP - Zip Code (if not part of an Address)    In addition to returning the named entity itself, we return the sub-concepts within entity, e.g. for ADDRESs we will return state (e.g. TX) and zip code if found.  + **keywords** - these are single words or short phrases e.g. company or product names.    Currently, keywords are detected using simple matching using stemming - so e.g. a keyword \"cancel\" will match \"cancellation\".    In near future we will support \"smart expansion\" which will also match synonyms while paying attention to the correct meaning of the word.     In addition to keywords we return keyword groups, e.g. several company name keywords can be combined into a `Competition` keyword group.  + **phrases (intent)** - allows for detection of phrases/intents that match the meaning of the phrases specified in the example training Sections).</br>   For each detected phrase/intent the system will also return entities and keywords contained in the phrase, if configured to do so.   For example, transcript \"Hello, my name is Lucy\" may match phrase/intent \"INTRODUCTION\" with the NER of PERSON and value \"Lucy\".       The configuration for phrase/intent detection takes the following parameters:   + _list_ of example phrases - each phrase has a sensitivity value which determines how close it has to match (sensitivity of 1.0 requires the closest match, sensitivity of 0.0 allows for vague matches).   + _regex_ - optional regex phrases to augment the examples - these require exact match   + _slots_ - types on named entities and keywords to be recognized within the phrase/intent</br>     Note: support for slots of same type but different meaning will be added in the future.     Currently it is possible e.g. to recognize places (GPE) but not possible to distinguish e.g. between types of them, like departure or destination place.   + _location_ - this narrows down where the phrase/match must occur - the options are:     + channel - agent or caller      + time in the call - from the start or from the end     + dialogue act - require the phrase to be part of a specified dialogue act, see https://web.stanford.edu/~jurafsky/ws97/manual.august1.html, first table, column SWBD    + **phrase groups** - computed across all channels - this is more powerful than keyword groups as it can be configured to require all phrases/intents in the groups to be present in any or fixed order.   One use case would be to detect a pair of a question and a confirming answer - for example to determine call resolution: \"Have I answered all your question?\", \"Yes\". + **criteria** - computed by rules/conditions looking at the following parameters:   + _call metrics_   + _regex_ - match of the text of the transcript   + _keywords_ - any keywords or keyword groups   + _NER_ - any named entities   + _phrases_ - any phrases/intents or phrase groups   + _dialogElements_ - selection of custom hardcoded rules that may accomplish tasks not possible with other conditions    The individual rules/conditions can be further narrowed down using filters like:   + _channel_ - agent or caller    + _time in the call_ - from the start or from the end    Multiple rules can be combined to form a logical AND expression.   Finally, the individual rules can be negated so that the absence of certain events is considered as a positive match.    When Criteria are satisfied then the system provides a detailed justification information. + **topics** - computed from text across all channels - assigns to the call a set of likely topics with their scores.    A topic classifier is built in a separate step using a corpus. The build process requires manual labeling of the topics.    For each call, the entire transcript is fed to the topic classifier and we get back the set of detected topics and their scores (in the 0..1 range).   It is useful e.g. for separating Billing calls from Troubleshooting calls from Account Change calls, etc.  + **summary** - computed from text across all channels - provides a summary of the call in a form of a set of sentences.   These may either be key sentences directly pulled from the transcript, or sentences generated by summarizing entire call or sections of the call.  + **sentiment** - computed from text - standard call sentiment as used in Call Center Speech Analytics.   Returns sentiment values from -1.0 (negative/mad/angry) to +1.0 (positive/happy/satisfied) + **mood** - computed from text - can distinguish 6 moods:   + neutral    + anger    + disgust    + fear    + happiness   + sadness   + surprise     Values are returned as a map from mood enum values to a number in (0.0, 1.0) range - multiple moods can be detected in the same place in the transcript in varying degrees. + **gender** - computed to audio - Estimates the gender of the speaker as far as it is possible to do it from the voice alone. + **word cloud** - returns word cloud data (map from words/phrases to frequencies) - the algorithm uses: stop word removal, stemming, frequent phrase detection. + **call metrics** - these are simple metrics computed from the audio and the transcript    + _silence_ - amount of silence in the call   + _talk_ - talk streaks for each of the channels   + _overtalk_ - amount of time when call participants talk over ove another   + _energy_ - the volume of the call and the variation   + _pitch_ - the pitch (frequency of the voice) and the variation  Voicegain allows for configuring Speech Analytics processing by preparing a Speech Analytics Configuration which is basically a selection of the capabilities mentioned above plus configuration of variable elements like keywords, phrases, etc.  </br> You can configure Speech Analytics using **[/sa/config API](#operation/saConfigPost)**   Once the configuration is complete you can launch speech transcription and analytics session using the **[/sa API](#operation/saPost)**   ### Offline vs Real-Time Speech Analytics  Speech audio can be transcribed and the analyzed in one of two modes: + **OFF-LINE** - audio will be queued for transcription, then transcribed, and both the audio and transcript will pass through various speech analytics algorithms according to the specified configuration.   The results of transcription and speech analytics can be retrieved using the [GET **/sa/{sid}/data** API](#operation/saDataGet)   + **REAL-TIME** - audio will immediately be submitted to real-time transcription and the stream of transcribed words will be fed to real-time speech analytics.    The results of transcription and speech analytics will be returned over websocket as soon as they are available.    The format of the returned messages is defined [here](#operation/saWebsocketPayload).     The results will also be available afterwards using the [GET **/sa/{sid}/data** API](#operation/saDataGet)  ## Agent Review Form  Data computed by Speech Analytics can be used to automatically fill/answer questions of the Call/Agent Review Form.   The automatic answers can be obtained based on previously defined Criteria (see above).  When Criteria are satisfied then the system provides a detailed justification information so it is easily possible to verify that the automated answer on a Review Form was correct.  ## PII Redaction  Being able to recognize occurrence of certain elements in the transcript allows us to remove them from both the text and the audio - this is called PII Redaction where PII stands for Personally Identifiable Information.  Currently, PII Redaction is limited to named entities (NER).  User can select any NER type detected by [Speech Analytics](#section/Speech-Analytics-API/Capabilities-of-Speech-Analytics) to be replaced by a specified placeholder in the text and by silence in the audio.  If your Enterprise account with Voicegain is setup with PCI-DSS compliance option, then PII Redaction of credit card numbers is enabled by default and cannot be disabled.    # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Rate Limiting  Access to Voicegain resources is controlled using the following limit settings on the account.  Newly created accounts get the limit values listed below.  If you need higher limits please contact us at support@voicegain.ai  The limits apply to the use of the Voicegain Platform in the Cloud.  On the Edge, the limits will be determined by the type of license you will purchase.  ## Types of Rate Limits  | Limit | default value | description | |---|---|---| | apiRequestLimitPerMinute | 75 | Basic rate limit with a fixed window of 1 minute applying to all API requests. Requests to /data API will be counted at 10x other requests. | | apiRequestLimitPerHour | 2000 | Basic rate limit with a fixed window of 1 hour applying to all API requests. Requests to /data API will be counted at 10x other requests. | | asrConcurrencyLimit | 4 | Limit on number of concurrent ASR requests. Does not apply to OFF-LINE requests. | | offlineQueueSizeLimit | 10 | Maximum number of OFF-LINE transcription jobs that may be submitted to the queue. | | offlineThroughputLimitPerHour | 4 | Maximum number of hours of audio that can be processed by OFF-LINE transcription within 1 hour. Note: For Edge deployment the limit interval is per day instead of per hour. | | offlineWorkerLimit | 2 | Maximum number of OFF-LINE transcription job workers that will be used to process the account audio. |  For API requests running longer that the rate limit window length, the request count will be applied to both the window when the request started and the window when the request finished.   Every HTTP API request will return several rate-limit related headers in its response.  The header values show the applicable limit, the remaining request count in the current window, and the number of seconds to when the limit resets. For example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 1 RateLimit-Reset: 7 ```  ## When Rate Limits are Hit  If a rate-limit is hit then [429 Too Many Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) HTTP error code will be returned. The response headers will additionally include Retry-After value, for example:  ``` RateLimit-Limit: 75, 75;window=60, 2000;window=3600 RateLimit-Remaining: 0 RateLimit-Reset: 6 Retry-After: 6 ``` If `asrConcurrencyLimit` is hit then the response headers will contain:  ``` X-ResourceLimit-Type: ASR-Concurrency X-ResourceLimit-Limit: 4 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ``` Note that we return a superset of values that are returned for a basic API request limit.  This will allow a client code that was written to handle basic rate limiting to be able to handle concurrency limiting too.  Note also that for the concurrency limit the Retry-After value is approximate and is not guaranteed - so client code may have to retry multiple times. (We will return increasing back-off Retry-After values in case of the limit being hit multiple times.)   In case of `offlineQueueSizeLimit` limit we will return, for example:  ``` X-ResourceLimit-Type: Offline-Queue-Size X-ResourceLimit-Limit: 10 RateLimit-Limit: 0 RateLimit-Remaining: 0 RateLimit-Reset: 120 Retry-After: 120 ```   # Pagination  For methods that support pagination Voicegain has standardized on using the following query parameters: + page={page number} + per_page={number items per page}  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?page=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=2&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=3&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"last\" ```   # PCI-DSS Compliance (Cloud)  The PCI-DSS compliant endpoint on the Voicegain Cloud is https://sapi.voicegain.ai/v1/ </br> Do not submit requests that may contain CHD data to the standard endpoint at https://api.voicegain.ai/v1/  Here is a list of all API Methods that are PCI-DSS compliant: + `/asr/transcribe`: [POST](#operation/asrTranscribePost) + `/asr/transcribe/async`: [POST](#operation/asrTranscribeAsyncPost) - we support OFF-LINE and REAL-TIME + `/asr/transcribe/{sessionId}`: [GET](#operation/asrTranscribeAsyncGet) [PUT](#operation/asrTranscribeAsyncPut) [DELETE](#operation/asrTranscribeAsyncDelete)  Note that the /data API is not yet PCI-DSS compliant on the Cloud. This means that the only PCI-DSS compliant ways to submit the audio are: + `fromUrl` - use `authConf` for authenticated access or use signed short-lived URLs + `inline` + `stream` - only `WEBSOCKET` is supported right now  # PCI-DSS Compliance (Edge)  Because the Edge deployment happens ultimately in the customer's environment, it will the customer's responsibility to certify their Edge depoyment of the Voicegain platform as PCI-DSS compliant.  Voicegain can provide Attestation of Compliance (AoC) for the following PCI-DSS sections as far as they releate to Voicegain Software that will be deployed on Edge: + 5. Use and regularly update anti-virus software or programs + 6. Develop and maintain secure systems and applications + 11. Regularly test security systems and processes + 12. Maintain a policy that addresses information security for all personnel  For the following PCI-DSS sections we will provide detailed data regarding implementation: + 3. Protect stored cardholder data   # noqa: E501

    The version of the OpenAPI document: 1.77.0 - updated February 3, 2023
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


class TranscribeApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def asr_transcribe_async_delete(self, session_id, **kwargs):  # noqa: E501
        """Delete Transcript  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  Delete transcript and any captured audio (if applicable). Currently it can only be used to delete transcription that has been completed. Calling this method when transcription is in progress will return a 409 (Conflict) error.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_delete(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SessionSuccessResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_async_delete_with_http_info(session_id, **kwargs)  # noqa: E501

    def asr_transcribe_async_delete_with_http_info(self, session_id, **kwargs):  # noqa: E501
        """Delete Transcript  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  Delete transcript and any captured audio (if applicable). Currently it can only be used to delete transcription that has been completed. Calling this method when transcription is in progress will return a 409 (Conflict) error.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_delete_with_http_info(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SessionSuccessResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['session_id', 'context_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_async_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'session_id' is set
        if self.api_client.client_side_validation and ('session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `session_id` when calling `asr_transcribe_async_delete`")  # noqa: E501

        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_async_delete`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_async_delete`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `asr_transcribe_async_delete`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `asr_transcribe_async_delete`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'session_id' in local_var_params:
            path_params['sessionId'] = local_var_params['session_id']  # noqa: E501

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

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
            '/asr/transcribe/{sessionId}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SessionSuccessResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def asr_transcribe_async_get(self, session_id, **kwargs):  # noqa: E501
        """Poll Transcript  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  Poll results of speech transcription.  Note - the exact url returned from the [/asr/transcribe/async](/#operation/asrTranscribeAsyncPost) method  in sessions[].poll.url field should be used to make polling request.  Response will contain the intermediate or the full content of the transcription.   The \"full\" query parameter controls what is returned.  + if **full=false**, then all returned content will be incremental, and the content will reflect audio transcribed since a previous poll request.  + if **full=true**, then all returned content will be full/complete, and the content will reflect transcription since the start of audio (time 0).  Note that the schemas for full vs incremental transcription results are different - see the Response Schema for 200 result below.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_get(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param bool full: Controls whether full or incremental results should be returned.  If **full=true**, and the results are not final yet, no words nor transcript will be included in the result. 
        :param bool rms_include: If true then the response will include encoded RMS data. Not returned with incremental result responses.
        :param str stop: Can be used to immediately stop processing of the current session.  + if **stop=retainResults** then available results up to that moment will be returned in the response. Results will be persisted according with the session settings. + if **stop=discardResults** then no results will be returned nor persisted.  
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncTranscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_async_get_with_http_info(session_id, **kwargs)  # noqa: E501

    def asr_transcribe_async_get_with_http_info(self, session_id, **kwargs):  # noqa: E501
        """Poll Transcript  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  Poll results of speech transcription.  Note - the exact url returned from the [/asr/transcribe/async](/#operation/asrTranscribeAsyncPost) method  in sessions[].poll.url field should be used to make polling request.  Response will contain the intermediate or the full content of the transcription.   The \"full\" query parameter controls what is returned.  + if **full=false**, then all returned content will be incremental, and the content will reflect audio transcribed since a previous poll request.  + if **full=true**, then all returned content will be full/complete, and the content will reflect transcription since the start of audio (time 0).  Note that the schemas for full vs incremental transcription results are different - see the Response Schema for 200 result below.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_get_with_http_info(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param bool full: Controls whether full or incremental results should be returned.  If **full=true**, and the results are not final yet, no words nor transcript will be included in the result. 
        :param bool rms_include: If true then the response will include encoded RMS data. Not returned with incremental result responses.
        :param str stop: Can be used to immediately stop processing of the current session.  + if **stop=retainResults** then available results up to that moment will be returned in the response. Results will be persisted according with the session settings. + if **stop=discardResults** then no results will be returned nor persisted.  
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncTranscriptionResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['session_id', 'full', 'rms_include', 'stop']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_async_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'session_id' is set
        if self.api_client.client_side_validation and ('session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `session_id` when calling `asr_transcribe_async_get`")  # noqa: E501

        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_async_get`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_async_get`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'session_id' in local_var_params:
            path_params['sessionId'] = local_var_params['session_id']  # noqa: E501

        query_params = []
        if 'full' in local_var_params and local_var_params['full'] is not None:  # noqa: E501
            query_params.append(('full', local_var_params['full']))  # noqa: E501
        if 'rms_include' in local_var_params and local_var_params['rms_include'] is not None:  # noqa: E501
            query_params.append(('rmsInclude', local_var_params['rms_include']))  # noqa: E501
        if 'stop' in local_var_params and local_var_params['stop'] is not None:  # noqa: E501
            query_params.append(('stop', local_var_params['stop']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/asr/transcribe/{sessionId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncTranscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def asr_transcribe_async_get_by_ws_name(self, ws_name, **kwargs):  # noqa: E501
        """Poll by WS name  # noqa: E501

        Poll speech transcription in async mode using the **Websocket name**.  This method is equivalent to [/asr/transcribe/{sessionId}](/#operation/asrTranscribeAsyncGet) except that session is identified by websocket name and not by sessionId.  If no session matching the websocket is found then error will be returned.  If more than one matching websocket sessions with the given name, then the most recent will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_get_by_ws_name(ws_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str ws_name: Name of the websocket (required)
        :param bool full: Controls whether full or incremental results should be returned.  If **full=true**, and the results are not final yet, no words nor transcript will be included in the result. 
        :param str stop: Can be used to immediately stop processing of the current session.  + if **stop=retainResults** then available results up to that moment will be returned in the response. Results will be persisted according with the session settings. + if **stop=discardResults** then no results will be returned nor persisted.  
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncTranscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_async_get_by_ws_name_with_http_info(ws_name, **kwargs)  # noqa: E501

    def asr_transcribe_async_get_by_ws_name_with_http_info(self, ws_name, **kwargs):  # noqa: E501
        """Poll by WS name  # noqa: E501

        Poll speech transcription in async mode using the **Websocket name**.  This method is equivalent to [/asr/transcribe/{sessionId}](/#operation/asrTranscribeAsyncGet) except that session is identified by websocket name and not by sessionId.  If no session matching the websocket is found then error will be returned.  If more than one matching websocket sessions with the given name, then the most recent will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_get_by_ws_name_with_http_info(ws_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str ws_name: Name of the websocket (required)
        :param bool full: Controls whether full or incremental results should be returned.  If **full=true**, and the results are not final yet, no words nor transcript will be included in the result. 
        :param str stop: Can be used to immediately stop processing of the current session.  + if **stop=retainResults** then available results up to that moment will be returned in the response. Results will be persisted according with the session settings. + if **stop=discardResults** then no results will be returned nor persisted.  
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncTranscriptionResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['ws_name', 'full', 'stop']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_async_get_by_ws_name" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'ws_name' is set
        if self.api_client.client_side_validation and ('ws_name' not in local_var_params or  # noqa: E501
                                                        local_var_params['ws_name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `ws_name` when calling `asr_transcribe_async_get_by_ws_name`")  # noqa: E501

        if self.api_client.client_side_validation and ('ws_name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['ws_name']) > 128):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `ws_name` when calling `asr_transcribe_async_get_by_ws_name`, length must be less than or equal to `128`")  # noqa: E501
        if self.api_client.client_side_validation and ('ws_name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['ws_name']) < 2):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `ws_name` when calling `asr_transcribe_async_get_by_ws_name`, length must be greater than or equal to `2`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ws_name' in local_var_params and local_var_params['ws_name'] is not None:  # noqa: E501
            query_params.append(('wsName', local_var_params['ws_name']))  # noqa: E501
        if 'full' in local_var_params and local_var_params['full'] is not None:  # noqa: E501
            query_params.append(('full', local_var_params['full']))  # noqa: E501
        if 'stop' in local_var_params and local_var_params['stop'] is not None:  # noqa: E501
            query_params.append(('stop', local_var_params['stop']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/asr/transcribe', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncTranscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def asr_transcribe_async_post(self, **kwargs):  # noqa: E501
        """Async Transcribe  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  Start speech transcription in asynchronous mode. Obtain results later.  This request will return as soon as access to resources is verified.  The response will contain session id, but will not contain the result of transcription.  Session id can be used to [poll](#operation/asrTranscribeAsyncGet) for intermediate and final results.  If a [callback](#operation/asrTranscribeCallback) URI was registered in the initial request, then the incremental and final result will be delivered to that URI. See [here](#operation/asrTranscribeCallback) for details of the payload of the callback request.  NOTE 1: Data fields in the polling response, and the fields in the default callback request will be the same.   NOTE 2: If you are using asyncMode:OFF-LINE with audioChannelSelector:two-channel then as long as the sum of the speech duration from both channels  is within 110% of the duration of the audio, you will be billed just the normal duration of the audio.  If the sum of speech duration is more than 110%, you will be billed for the sum of speech duration on both channels.   See our Zendesk knowledge-base for examples of using this method: + [Examples of requests for OFF-LINE transcription - various audio channels and diarization](https://support.voicegain.ai/hc/en-us/articles/4410070239380-Examples-of-requests-for-OFF-LINE-transcription-various-audio-channels-and-diarization) + [Example of word-tree output from async real-time transcription](https://support.voicegain.ai/hc/en-us/articles/360045632531-Example-of-word-tree-output-from-async-real-time-transcription) + [Example of streaming audio via websocket and receiving text via websocket](https://support.voicegain.ai/hc/en-us/articles/360050460931-Example-of-streaming-audio-via-websocket-and-receiving-text-via-websocket) + [Websocket STOMP payload for real-time transcription results](https://support.voicegain.ai/hc/en-us/articles/360045569592-Websocket-STOMP-payload-for-real-time-transcription-results)   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param AsyncTranscriptionRequest async_transcription_request: Request transcription in Async Mode.  
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AsyncTranscPostResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_async_post_with_http_info(**kwargs)  # noqa: E501

    def asr_transcribe_async_post_with_http_info(self, **kwargs):  # noqa: E501
        """Async Transcribe  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  Start speech transcription in asynchronous mode. Obtain results later.  This request will return as soon as access to resources is verified.  The response will contain session id, but will not contain the result of transcription.  Session id can be used to [poll](#operation/asrTranscribeAsyncGet) for intermediate and final results.  If a [callback](#operation/asrTranscribeCallback) URI was registered in the initial request, then the incremental and final result will be delivered to that URI. See [here](#operation/asrTranscribeCallback) for details of the payload of the callback request.  NOTE 1: Data fields in the polling response, and the fields in the default callback request will be the same.   NOTE 2: If you are using asyncMode:OFF-LINE with audioChannelSelector:two-channel then as long as the sum of the speech duration from both channels  is within 110% of the duration of the audio, you will be billed just the normal duration of the audio.  If the sum of speech duration is more than 110%, you will be billed for the sum of speech duration on both channels.   See our Zendesk knowledge-base for examples of using this method: + [Examples of requests for OFF-LINE transcription - various audio channels and diarization](https://support.voicegain.ai/hc/en-us/articles/4410070239380-Examples-of-requests-for-OFF-LINE-transcription-various-audio-channels-and-diarization) + [Example of word-tree output from async real-time transcription](https://support.voicegain.ai/hc/en-us/articles/360045632531-Example-of-word-tree-output-from-async-real-time-transcription) + [Example of streaming audio via websocket and receiving text via websocket](https://support.voicegain.ai/hc/en-us/articles/360050460931-Example-of-streaming-audio-via-websocket-and-receiving-text-via-websocket) + [Websocket STOMP payload for real-time transcription results](https://support.voicegain.ai/hc/en-us/articles/360045569592-Websocket-STOMP-payload-for-real-time-transcription-results)   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param AsyncTranscriptionRequest async_transcription_request: Request transcription in Async Mode.  
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AsyncTranscPostResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'async_transcription_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_async_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `asr_transcribe_async_post`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `asr_transcribe_async_post`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'async_transcription_request' in local_var_params:
            body_params = local_var_params['async_transcription_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/asr/transcribe/async', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AsyncTranscPostResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def asr_transcribe_async_put(self, session_id, **kwargs):  # noqa: E501
        """Modify Transcribe Sess.  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  **Modify existing Transcription session**</br> This method should be invoked using the url returned in `sessions[].sessionUrl` field in the response to [POST /asr/transcribe/async](#operation/asrTranscribeAsyncPost) </br>  All parameters in this method are optional. If not provided then the corresponding property will not be modified.  This command may be used to **pause** or **mute** the audio. (Note that you cannot mix mute and pause, i.e., you cannot pause if session is muted not mute when session is paused.)</br> </br> Using **pause** is simple: you issue the pause action:start command and about the same time you stop sending the audio. When you want to end the pause you re-start sending the audio and issue a pause action:stop command. The key factor that makes the pause work is stopping the audio stream, the pause command just instructs the recognizer to not terminate  the recognition due to no audio being sent.</br> </br> **Mute** is more complicated. In order to use it you have to keep track of the amount of audio data sent to Voicegain. + To **start** mute you have to stop streaming the audio bytes and note the audio time in milliseconds when you stopped.  Then you issue `mute action:start` command which requires the audio stop time in milliseconds in the `atTime` field.</br> Note: the method returns immediately but the mute actually starts when then last byte of audio corresponding to the value of `atTime` field is received. If you send too few bytes then the session will timeout before mute starts. If you send too many bytes, they will be ignored.   + To **finish** mute you have to send `mute action:stop` command and set `atTime` to a value which is a sum of the audio time at mute start  plus mute duration. Immediately after that you should start streaming the audio bytes.   Note: If you stream audio before between `mute action:start` and `mute action:stop` then it will be ignored (replaced with silence).   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_put(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param TranscribeSessionModifyRequest transcribe_session_modify_request: Parameters to modify
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SessionSuccessResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_async_put_with_http_info(session_id, **kwargs)  # noqa: E501

    def asr_transcribe_async_put_with_http_info(self, session_id, **kwargs):  # noqa: E501
        """Modify Transcribe Sess.  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  **Modify existing Transcription session**</br> This method should be invoked using the url returned in `sessions[].sessionUrl` field in the response to [POST /asr/transcribe/async](#operation/asrTranscribeAsyncPost) </br>  All parameters in this method are optional. If not provided then the corresponding property will not be modified.  This command may be used to **pause** or **mute** the audio. (Note that you cannot mix mute and pause, i.e., you cannot pause if session is muted not mute when session is paused.)</br> </br> Using **pause** is simple: you issue the pause action:start command and about the same time you stop sending the audio. When you want to end the pause you re-start sending the audio and issue a pause action:stop command. The key factor that makes the pause work is stopping the audio stream, the pause command just instructs the recognizer to not terminate  the recognition due to no audio being sent.</br> </br> **Mute** is more complicated. In order to use it you have to keep track of the amount of audio data sent to Voicegain. + To **start** mute you have to stop streaming the audio bytes and note the audio time in milliseconds when you stopped.  Then you issue `mute action:start` command which requires the audio stop time in milliseconds in the `atTime` field.</br> Note: the method returns immediately but the mute actually starts when then last byte of audio corresponding to the value of `atTime` field is received. If you send too few bytes then the session will timeout before mute starts. If you send too many bytes, they will be ignored.   + To **finish** mute you have to send `mute action:stop` command and set `atTime` to a value which is a sum of the audio time at mute start  plus mute duration. Immediately after that you should start streaming the audio bytes.   Note: If you stream audio before between `mute action:start` and `mute action:stop` then it will be ignored (replaced with silence).   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_async_put_with_http_info(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param TranscribeSessionModifyRequest transcribe_session_modify_request: Parameters to modify
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SessionSuccessResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['session_id', 'context_id', 'transcribe_session_modify_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_async_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'session_id' is set
        if self.api_client.client_side_validation and ('session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `session_id` when calling `asr_transcribe_async_put`")  # noqa: E501

        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_async_put`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_async_put`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `asr_transcribe_async_put`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('context_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['context_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `context_id` when calling `asr_transcribe_async_put`, length must be greater than or equal to `16`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'session_id' in local_var_params:
            path_params['sessionId'] = local_var_params['session_id']  # noqa: E501

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'transcribe_session_modify_request' in local_var_params:
            body_params = local_var_params['transcribe_session_modify_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/asr/transcribe/{sessionId}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SessionSuccessResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def asr_transcribe_get_transcript(self, session_id, **kwargs):  # noqa: E501
        """Transcript Content  # noqa: E501

        Retrieve transcript  (after transcription is complete) in one of several possible formats.</br> The response will contain the final content of the transcription of the provided audio.</br> Note, if the transcription is still in progress then 400 error will be returned.</br> Transcript data is available for the `session.poll.persist` period as specified in the initial POST request.</br>  NOTE: for this method to work the transcription needs to be started with content.full[\"words\"] option, e.g.: <pre>   \"content\": {     \"incremental\": [\"progress\"],     \"full\" : [\"transcript\", \"words\"]     } </pre>   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_get_transcript(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param str format: Format of the transcript to be returned: + json - complete transcript data with all detail for each word (`numColumns` and `columnPos` **not** present in output) + json-mc - multi-column version of the json output with `numColumns` and `columnPos` + text - plain text transcript with optional timing information + srt - transcript in SRT caption format + vtt - transcript in WebVTT caption format + ttml - transcript in TTML (XML) caption format 
        :param float width: Applicable only to captions. Determines max caption width in number of characters.
        :param float interval: Applicable only to plain text transcript. Determines interval (in seconds) between time stamps.</br> If absent, no time stamps will be provided.<br> 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[WordsSection]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_get_transcript_with_http_info(session_id, **kwargs)  # noqa: E501

    def asr_transcribe_get_transcript_with_http_info(self, session_id, **kwargs):  # noqa: E501
        """Transcript Content  # noqa: E501

        Retrieve transcript  (after transcription is complete) in one of several possible formats.</br> The response will contain the final content of the transcription of the provided audio.</br> Note, if the transcription is still in progress then 400 error will be returned.</br> Transcript data is available for the `session.poll.persist` period as specified in the initial POST request.</br>  NOTE: for this method to work the transcription needs to be started with content.full[\"words\"] option, e.g.: <pre>   \"content\": {     \"incremental\": [\"progress\"],     \"full\" : [\"transcript\", \"words\"]     } </pre>   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_get_transcript_with_http_info(session_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str session_id: ID of the session (required)
        :param str format: Format of the transcript to be returned: + json - complete transcript data with all detail for each word (`numColumns` and `columnPos` **not** present in output) + json-mc - multi-column version of the json output with `numColumns` and `columnPos` + text - plain text transcript with optional timing information + srt - transcript in SRT caption format + vtt - transcript in WebVTT caption format + ttml - transcript in TTML (XML) caption format 
        :param float width: Applicable only to captions. Determines max caption width in number of characters.
        :param float interval: Applicable only to plain text transcript. Determines interval (in seconds) between time stamps.</br> If absent, no time stamps will be provided.<br> 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[WordsSection], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['session_id', 'format', 'width', 'interval']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_get_transcript" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'session_id' is set
        if self.api_client.client_side_validation and ('session_id' not in local_var_params or  # noqa: E501
                                                        local_var_params['session_id'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `session_id` when calling `asr_transcribe_get_transcript`")  # noqa: E501

        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) > 48):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_get_transcript`, length must be less than or equal to `48`")  # noqa: E501
        if self.api_client.client_side_validation and ('session_id' in local_var_params and  # noqa: E501
                                                        len(local_var_params['session_id']) < 16):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `session_id` when calling `asr_transcribe_get_transcript`, length must be greater than or equal to `16`")  # noqa: E501
        if self.api_client.client_side_validation and 'width' in local_var_params and local_var_params['width'] > 120:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `width` when calling `asr_transcribe_get_transcript`, must be a value less than or equal to `120`")  # noqa: E501
        if self.api_client.client_side_validation and 'width' in local_var_params and local_var_params['width'] < 10:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `width` when calling `asr_transcribe_get_transcript`, must be a value greater than or equal to `10`")  # noqa: E501
        if self.api_client.client_side_validation and 'interval' in local_var_params and local_var_params['interval'] < 5:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `interval` when calling `asr_transcribe_get_transcript`, must be a value greater than or equal to `5`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'session_id' in local_var_params:
            path_params['sessionId'] = local_var_params['session_id']  # noqa: E501

        query_params = []
        if 'format' in local_var_params and local_var_params['format'] is not None:  # noqa: E501
            query_params.append(('format', local_var_params['format']))  # noqa: E501
        if 'width' in local_var_params and local_var_params['width'] is not None:  # noqa: E501
            query_params.append(('width', local_var_params['width']))  # noqa: E501
        if 'interval' in local_var_params and local_var_params['interval'] is not None:  # noqa: E501
            query_params.append(('interval', local_var_params['interval']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/plain', 'text/srt', 'text/vtt', 'text/xml'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/asr/transcribe/{sessionId}/transcript', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[WordsSection]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def asr_transcribe_post(self, **kwargs):  # noqa: E501
        """Sync Transcribe  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  **Synchronous Transcription API Method.**  Do speech transcription of **short** audio in a single request.  `/asr/transcribe` request will return only after processing of the audio is completed. The returned response will contain the result of transcription (possibly several alternatives).  Maximum length of audio is 60 seconds. For longer audio please use [/asr/transcribe/async](#operation/asrTranscribeAsyncPost).  This method always uses the more accurate off-line Acoustic Model.  See our Zendesk knowledge-base for examples of using this method: + [End-to-end \"Hello World\" API use example](https://support.voicegain.ai/hc/en-us/articles/360046261472-End-to-end-Hello-World-API-use-example) + [Use Example of Synchronous /asr/transcribe API (inline data)](https://support.voicegain.ai/hc/en-us/articles/360029137391-Use-Example-of-Synchronous-asr-transcribe-API-inline-data-) + [Use Example of Synchronous /asr/transcribe API (data from URL)](https://support.voicegain.ai/hc/en-us/articles/360029139271-Use-Example-of-Synchronous-asr-transcribe-API-data-from-URL-) + [Example of invoking Voicegain API from node.js (/asr/transcribe)](https://support.voicegain.ai/hc/en-us/articles/360044631632-Example-of-invoking-Voicegain-API-from-node-js-asr-transcribe-)   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SyncTranscriptionRequest sync_transcription_request: body of transcription request
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: SyncTranscriptionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.asr_transcribe_post_with_http_info(**kwargs)  # noqa: E501

    def asr_transcribe_post_with_http_info(self, **kwargs):  # noqa: E501
        """Sync Transcribe  # noqa: E501

        [**PCI-DSS Compliant**](#section/PCI-DSS-Compliance)  **Synchronous Transcription API Method.**  Do speech transcription of **short** audio in a single request.  `/asr/transcribe` request will return only after processing of the audio is completed. The returned response will contain the result of transcription (possibly several alternatives).  Maximum length of audio is 60 seconds. For longer audio please use [/asr/transcribe/async](#operation/asrTranscribeAsyncPost).  This method always uses the more accurate off-line Acoustic Model.  See our Zendesk knowledge-base for examples of using this method: + [End-to-end \"Hello World\" API use example](https://support.voicegain.ai/hc/en-us/articles/360046261472-End-to-end-Hello-World-API-use-example) + [Use Example of Synchronous /asr/transcribe API (inline data)](https://support.voicegain.ai/hc/en-us/articles/360029137391-Use-Example-of-Synchronous-asr-transcribe-API-inline-data-) + [Use Example of Synchronous /asr/transcribe API (data from URL)](https://support.voicegain.ai/hc/en-us/articles/360029139271-Use-Example-of-Synchronous-asr-transcribe-API-data-from-URL-) + [Example of invoking Voicegain API from node.js (/asr/transcribe)](https://support.voicegain.ai/hc/en-us/articles/360044631632-Example-of-invoking-Voicegain-API-from-node-js-asr-transcribe-)   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.asr_transcribe_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param SyncTranscriptionRequest sync_transcription_request: body of transcription request
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(SyncTranscriptionResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['sync_transcription_request']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method asr_transcribe_post" % key
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
        if 'sync_transcription_request' in local_var_params:
            body_params = local_var_params['sync_transcription_request']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/asr/transcribe', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SyncTranscriptionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def ws_transcribe_words(self, ws_name, **kwargs):  # noqa: E501
        """Words via websocket  # noqa: E501

        Access the word stream via a websocket.  This will provide access to websocket stream containing words (with optional corrections).      NOTE, the websocket messages will be encoded in application/json        # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ws_transcribe_words(ws_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str ws_name: Name of the websocket (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.ws_transcribe_words_with_http_info(ws_name, **kwargs)  # noqa: E501

    def ws_transcribe_words_with_http_info(self, ws_name, **kwargs):  # noqa: E501
        """Words via websocket  # noqa: E501

        Access the word stream via a websocket.  This will provide access to websocket stream containing words (with optional corrections).      NOTE, the websocket messages will be encoded in application/json        # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.ws_transcribe_words_with_http_info(ws_name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str ws_name: Name of the websocket (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['ws_name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method ws_transcribe_words" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'ws_name' is set
        if self.api_client.client_side_validation and ('ws_name' not in local_var_params or  # noqa: E501
                                                        local_var_params['ws_name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `ws_name` when calling `ws_transcribe_words`")  # noqa: E501

        if self.api_client.client_side_validation and ('ws_name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['ws_name']) > 128):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `ws_name` when calling `ws_transcribe_words`, length must be less than or equal to `128`")  # noqa: E501
        if self.api_client.client_side_validation and ('ws_name' in local_var_params and  # noqa: E501
                                                        len(local_var_params['ws_name']) < 2):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `ws_name` when calling `ws_transcribe_words`, length must be greater than or equal to `2`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'ws_name' in local_var_params and local_var_params['ws_name'] is not None:  # noqa: E501
            query_params.append(('wsName', local_var_params['ws_name']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuthOptional']  # noqa: E501

        return self.api_client.call_api(
            '/nats-websocket/port', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
