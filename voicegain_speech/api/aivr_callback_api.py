# coding: utf-8

"""
    Voicegain Speech-to-Text API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + RTC Callback APIs which in addition to speech-to-text allow for control of RTC session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second after end of utterance.  For the transcription API, real-time incremental results will be sent back with under 1 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30-45 seconds (or earlier for shorter audio).  Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes.  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.  # RTC Callback API   Voicegain Real Time Communication (RTC) Callback APIs work on audio data that is part of an RTC session (a telephone call for example).   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Pagination  For methods that support pagination Voicegain has standardized on using the following query parameters: + page={page number} + per_page={number items per page}  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?page=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=2&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=3&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"last\" ```  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.15.0 - updated September 15 2020
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


class AivrCallbackApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def aivr_callback_delete(self, csid, seq, **kwargs):  # noqa: E501
        """End RTC Session  # noqa: E501

        Specification of a callback method that Voicegain Platform will use to communicate end of RTC session to the User's dialog control logic.</br> Note: the url provided here is not relevant. Customer can implement this method on any url (consistent with corresponding POST and PUT methods).</br> Request definition specifies what data will be sent from Voicegain to User system.</br> Response definition specifies what data will be sent from User system to Voicegain.     # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.aivr_callback_delete(csid, seq, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str csid: ID of the AIVR session on customer's system.   (required)
        :param int seq: Interaction sequences of the AIVR session on Voicegain system.   (required)
        :param AIVRExistingSession aivr_existing_session: Body of RTC Callback request.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AIVRCallbackResponseFinal
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.aivr_callback_delete_with_http_info(csid, seq, **kwargs)  # noqa: E501

    def aivr_callback_delete_with_http_info(self, csid, seq, **kwargs):  # noqa: E501
        """End RTC Session  # noqa: E501

        Specification of a callback method that Voicegain Platform will use to communicate end of RTC session to the User's dialog control logic.</br> Note: the url provided here is not relevant. Customer can implement this method on any url (consistent with corresponding POST and PUT methods).</br> Request definition specifies what data will be sent from Voicegain to User system.</br> Response definition specifies what data will be sent from User system to Voicegain.     # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.aivr_callback_delete_with_http_info(csid, seq, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str csid: ID of the AIVR session on customer's system.   (required)
        :param int seq: Interaction sequences of the AIVR session on Voicegain system.   (required)
        :param AIVRExistingSession aivr_existing_session: Body of RTC Callback request.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AIVRCallbackResponseFinal, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['csid', 'seq', 'aivr_existing_session']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method aivr_callback_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'csid' is set
        if self.api_client.client_side_validation and ('csid' not in local_var_params or  # noqa: E501
                                                        local_var_params['csid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `csid` when calling `aivr_callback_delete`")  # noqa: E501
        # verify the required parameter 'seq' is set
        if self.api_client.client_side_validation and ('seq' not in local_var_params or  # noqa: E501
                                                        local_var_params['seq'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `seq` when calling `aivr_callback_delete`")  # noqa: E501

        if self.api_client.client_side_validation and ('csid' in local_var_params and  # noqa: E501
                                                        len(local_var_params['csid']) > 256):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `csid` when calling `aivr_callback_delete`, length must be less than or equal to `256`")  # noqa: E501
        if self.api_client.client_side_validation and ('csid' in local_var_params and  # noqa: E501
                                                        len(local_var_params['csid']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `csid` when calling `aivr_callback_delete`, length must be greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and 'seq' in local_var_params and local_var_params['seq'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `seq` when calling `aivr_callback_delete`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'csid' in local_var_params:
            path_params['csid'] = local_var_params['csid']  # noqa: E501

        query_params = []
        if 'seq' in local_var_params and local_var_params['seq'] is not None:  # noqa: E501
            query_params.append(('seq', local_var_params['seq']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'aivr_existing_session' in local_var_params:
            body_params = local_var_params['aivr_existing_session']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/customer/aivr-callback/{csid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AIVRCallbackResponseFinal',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def aivr_callback_existing(self, csid, seq, **kwargs):  # noqa: E501
        """Existing RTC Session  # noqa: E501

        Specification of a callback method that Voicegain Platform will use to communicate events from an existing RTC session to the User's dialog control logic.</br> Note: the url provided here is not relevant. User can implement this method on any url (consistent with corresponding PUT and DELETE methods).  **Request** definition specifies what data will be sent from Voicegain RTC Session to User system.</br>  **Response** definition specifies what data will be sent from User dialog system to Voicegain RTC Session Engine.  Response contains instructions for Voicegain RTC Session Engine (including TTS and ASR) in response to the data received in the Callback request.</br> Possible actions that may be requested from Voicegain are: + prompt + question + disconnect + transfer   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.aivr_callback_existing(csid, seq, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str csid: ID of the AIVR session on customer's system.   (required)
        :param int seq: Interaction sequences of the AIVR session on Voicegain system.   (required)
        :param AIVRExistingSession aivr_existing_session: Body of RTC Callback request.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AIVRCallbackResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.aivr_callback_existing_with_http_info(csid, seq, **kwargs)  # noqa: E501

    def aivr_callback_existing_with_http_info(self, csid, seq, **kwargs):  # noqa: E501
        """Existing RTC Session  # noqa: E501

        Specification of a callback method that Voicegain Platform will use to communicate events from an existing RTC session to the User's dialog control logic.</br> Note: the url provided here is not relevant. User can implement this method on any url (consistent with corresponding PUT and DELETE methods).  **Request** definition specifies what data will be sent from Voicegain RTC Session to User system.</br>  **Response** definition specifies what data will be sent from User dialog system to Voicegain RTC Session Engine.  Response contains instructions for Voicegain RTC Session Engine (including TTS and ASR) in response to the data received in the Callback request.</br> Possible actions that may be requested from Voicegain are: + prompt + question + disconnect + transfer   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.aivr_callback_existing_with_http_info(csid, seq, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str csid: ID of the AIVR session on customer's system.   (required)
        :param int seq: Interaction sequences of the AIVR session on Voicegain system.   (required)
        :param AIVRExistingSession aivr_existing_session: Body of RTC Callback request.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AIVRCallbackResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['csid', 'seq', 'aivr_existing_session']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method aivr_callback_existing" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'csid' is set
        if self.api_client.client_side_validation and ('csid' not in local_var_params or  # noqa: E501
                                                        local_var_params['csid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `csid` when calling `aivr_callback_existing`")  # noqa: E501
        # verify the required parameter 'seq' is set
        if self.api_client.client_side_validation and ('seq' not in local_var_params or  # noqa: E501
                                                        local_var_params['seq'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `seq` when calling `aivr_callback_existing`")  # noqa: E501

        if self.api_client.client_side_validation and ('csid' in local_var_params and  # noqa: E501
                                                        len(local_var_params['csid']) > 256):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `csid` when calling `aivr_callback_existing`, length must be less than or equal to `256`")  # noqa: E501
        if self.api_client.client_side_validation and ('csid' in local_var_params and  # noqa: E501
                                                        len(local_var_params['csid']) < 1):  # noqa: E501
            raise ApiValueError("Invalid value for parameter `csid` when calling `aivr_callback_existing`, length must be greater than or equal to `1`")  # noqa: E501
        if self.api_client.client_side_validation and 'seq' in local_var_params and local_var_params['seq'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `seq` when calling `aivr_callback_existing`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'csid' in local_var_params:
            path_params['csid'] = local_var_params['csid']  # noqa: E501

        query_params = []
        if 'seq' in local_var_params and local_var_params['seq'] is not None:  # noqa: E501
            query_params.append(('seq', local_var_params['seq']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'aivr_existing_session' in local_var_params:
            body_params = local_var_params['aivr_existing_session']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/customer/aivr-callback/{csid}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AIVRCallbackResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def aivr_callback_new(self, **kwargs):  # noqa: E501
        """New RTC Session  # noqa: E501

        Specification of a callback method that Voicegain Platform will invoke to indicate start of new RTC session to the User's dialog control logic.</br> Note: the url provided here is not relevant. User can implement this method on any url (consistent with corresponding PUT and DELETE methods).  **Request** definition specifies what data will be sent from Voicegain RTC Session to User system.</br>  **Response** definition specifies what data will be sent from User dialog system to Voicegain RTC Session Engine.  Response contains instructions for Voicegain RTC Session Engine (including TTS and ASR) in response to the data received in the Callback request.</br> Possible actions that may be requested from Voicegain are: + prompt + question + disconnect + transfer   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.aivr_callback_new(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param AIVRNewSession aivr_new_session: Body of RTC Callback request.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: AIVRCallbackResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.aivr_callback_new_with_http_info(**kwargs)  # noqa: E501

    def aivr_callback_new_with_http_info(self, **kwargs):  # noqa: E501
        """New RTC Session  # noqa: E501

        Specification of a callback method that Voicegain Platform will invoke to indicate start of new RTC session to the User's dialog control logic.</br> Note: the url provided here is not relevant. User can implement this method on any url (consistent with corresponding PUT and DELETE methods).  **Request** definition specifies what data will be sent from Voicegain RTC Session to User system.</br>  **Response** definition specifies what data will be sent from User dialog system to Voicegain RTC Session Engine.  Response contains instructions for Voicegain RTC Session Engine (including TTS and ASR) in response to the data received in the Callback request.</br> Possible actions that may be requested from Voicegain are: + prompt + question + disconnect + transfer   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.aivr_callback_new_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param AIVRNewSession aivr_new_session: Body of RTC Callback request.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(AIVRCallbackResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['aivr_new_session']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method aivr_callback_new" % key
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
        if 'aivr_new_session' in local_var_params:
            body_params = local_var_params['aivr_new_session']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/customer/aivr-callback', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='AIVRCallbackResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
