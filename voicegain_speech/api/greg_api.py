# coding: utf-8

"""
    Voicegain Speech-to-Text API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + RTC Callback APIs which in addition to speech-to-text allow for control RTC session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second.  For the transcription API, real-time incremental results will be sent back with about 2 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30 seconds (or earlier for shorter audio). Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes.  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.  # RTC Callback API   Voicegain Real Time Communication (RTC) Callback APIs work on audio data that is part of an RTC session (a telephone call for example).   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.   # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.11.0 - updated July 31, 2020
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


class GregApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def audio_bytes_get_hash(self, hash, **kwargs):  # noqa: E501
        """Audio bytes by hash  # noqa: E501

        Get GREG Audio bytes using the audio hash as identifier in the query  Raw audio data bytes will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.audio_bytes_get_hash(hash, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str hash: Hash of an object stored in SOS (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.audio_bytes_get_hash_with_http_info(hash, **kwargs)  # noqa: E501

    def audio_bytes_get_hash_with_http_info(self, hash, **kwargs):  # noqa: E501
        """Audio bytes by hash  # noqa: E501

        Get GREG Audio bytes using the audio hash as identifier in the query  Raw audio data bytes will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.audio_bytes_get_hash_with_http_info(hash, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str hash: Hash of an object stored in SOS (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(file, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['hash']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method audio_bytes_get_hash" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'hash' is set
        if self.api_client.client_side_validation and ('hash' not in local_var_params or  # noqa: E501
                                                        local_var_params['hash'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `hash` when calling `audio_bytes_get_hash`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'hash' in local_var_params:
            path_params['hash'] = local_var_params['hash']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['audio/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/audio/bytes/{hash}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def audio_bytes_get_id(self, uuid, **kwargs):  # noqa: E501
        """Audio bytes by id  # noqa: E501

        Get GREG Audio bytes using Audio object id as the identifier in the query Raw audio data bytes will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.audio_bytes_get_id(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: file
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.audio_bytes_get_id_with_http_info(uuid, **kwargs)  # noqa: E501

    def audio_bytes_get_id_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Audio bytes by id  # noqa: E501

        Get GREG Audio bytes using Audio object id as the identifier in the query Raw audio data bytes will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.audio_bytes_get_id_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(file, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method audio_bytes_get_id" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `audio_bytes_get_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['audio/*'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/audio/{uuid}/bytes', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='file',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def exp_recog_query(self, uuid, **kwargs):  # noqa: E501
        """Query Recogs for Exp  # noqa: E501

        Retrieve all recognitons for GREG Experiments.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exp_recog_query(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: uuid of a GREG Experiment (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[GregRecognition]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.exp_recog_query_with_http_info(uuid, **kwargs)  # noqa: E501

    def exp_recog_query_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Query Recogs for Exp  # noqa: E501

        Retrieve all recognitons for GREG Experiments.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.exp_recog_query_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: uuid of a GREG Experiment (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[GregRecognition], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method exp_recog_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `exp_recog_query`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

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
            '/greg/experiment/{uuid}/recognition', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GregRecognition]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def experiment_query(self, **kwargs):  # noqa: E501
        """Query Experiments  # noqa: E501

        Retrieve all GREG Experiments.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.experiment_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[GregExperimentResponse]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.experiment_query_with_http_info(**kwargs)  # noqa: E501

    def experiment_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query Experiments  # noqa: E501

        Retrieve all GREG Experiments.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.experiment_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[GregExperimentResponse], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'incl_refs']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method experiment_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'incl_refs' in local_var_params and local_var_params['incl_refs'] is not None:  # noqa: E501
            query_params.append(('inclRefs', local_var_params['incl_refs']))  # noqa: E501

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
            '/greg/experiment', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GregExperimentResponse]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def grammar_query(self, **kwargs):  # noqa: E501
        """Query Grammars  # noqa: E501

        Retrieve all GREG Grammars.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.grammar_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[GregGrammarLight]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.grammar_query_with_http_info(**kwargs)  # noqa: E501

    def grammar_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query Grammars  # noqa: E501

        Retrieve all GREG Grammars.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.grammar_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[GregGrammarLight], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method grammar_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

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
            '/greg/grammar', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GregGrammarLight]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_audio_post(self, **kwargs):  # noqa: E501
        """Create GREG Audio  # noqa: E501

        Upload audio to GREG. Creates a new GREG Audio object and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregAudioBaseWithAudio greg_audio_base_with_audio:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregAudio
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_audio_post_with_http_info(**kwargs)  # noqa: E501

    def greg_audio_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create GREG Audio  # noqa: E501

        Upload audio to GREG. Creates a new GREG Audio object and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregAudioBaseWithAudio greg_audio_base_with_audio:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregAudio, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'greg_audio_base_with_audio']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_audio_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'greg_audio_base_with_audio' in local_var_params:
            body_params = local_var_params['greg_audio_base_with_audio']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/audio', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregAudio',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_audio_set_add(self, uuid, **kwargs):  # noqa: E501
        """Add Audio to Set  # noqa: E501

        Upload Audio to specified GREG AudioSet.  Creates a new GREG Audio object, attaches it to the AudioSet and returns Audio ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_set_add(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: uuid of an AudioSet object (required)
        :param UNKNOWN_BASE_TYPE unknown_base_type:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: OneOfGregAudioarray
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_audio_set_add_with_http_info(uuid, **kwargs)  # noqa: E501

    def greg_audio_set_add_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Add Audio to Set  # noqa: E501

        Upload Audio to specified GREG AudioSet.  Creates a new GREG Audio object, attaches it to the AudioSet and returns Audio ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_set_add_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: uuid of an AudioSet object (required)
        :param UNKNOWN_BASE_TYPE unknown_base_type:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(OneOfGregAudioarray, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'unknown_base_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_audio_set_add" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `greg_audio_set_add`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'unknown_base_type' in local_var_params:
            body_params = local_var_params['unknown_base_type']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/audioset/{uuid}/audio', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OneOfGregAudioarray',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_audio_set_get(self, uuid, **kwargs):  # noqa: E501
        """Get AudioSet.  # noqa: E501

        Get AudioSet.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_set_get(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregAudioSetResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_audio_set_get_with_http_info(uuid, **kwargs)  # noqa: E501

    def greg_audio_set_get_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Get AudioSet.  # noqa: E501

        Get AudioSet.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_set_get_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregAudioSetResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'incl_refs']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_audio_set_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `greg_audio_set_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []
        if 'incl_refs' in local_var_params and local_var_params['incl_refs'] is not None:  # noqa: E501
            query_params.append(('inclRefs', local_var_params['incl_refs']))  # noqa: E501

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
            '/greg/audioset/{uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregAudioSetResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_audio_set_query(self, **kwargs):  # noqa: E501
        """Query AudioSet.  # noqa: E501

        query AudioSet.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_set_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
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
        return self.greg_audio_set_query_with_http_info(**kwargs)  # noqa: E501

    def greg_audio_set_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query AudioSet.  # noqa: E501

        query AudioSet.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_audio_set_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
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

        all_params = ['context_id', 'incl_refs']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_audio_set_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'incl_refs' in local_var_params and local_var_params['incl_refs'] is not None:  # noqa: E501
            query_params.append(('inclRefs', local_var_params['incl_refs']))  # noqa: E501

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
            '/greg/audioset', 'GET',
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

    def greg_exp_post(self, **kwargs):  # noqa: E501
        """Create Experiment  # noqa: E501

        Create Experiment in GREG. Creates a new GREG Experiment object and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_exp_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param bool create_audio_set: Create new AudioSet (rather then using existing).  If both `createAudioSet==true` and `audioSetId` is provided in POST request at the same time, a Bad Request Error will be returned. 
        :param bool importing: Create GREG Experiment with `status=IMPORTING`. This will also create a brand new AudioSet and attach it to the experiment. If both `importing==true` and `audioSetId` is provided in POST request at the same time, a Bad Request Error will be returned. 
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregExperimentBase greg_experiment_base:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregExperiment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_exp_post_with_http_info(**kwargs)  # noqa: E501

    def greg_exp_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create Experiment  # noqa: E501

        Create Experiment in GREG. Creates a new GREG Experiment object and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_exp_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param bool create_audio_set: Create new AudioSet (rather then using existing).  If both `createAudioSet==true` and `audioSetId` is provided in POST request at the same time, a Bad Request Error will be returned. 
        :param bool importing: Create GREG Experiment with `status=IMPORTING`. This will also create a brand new AudioSet and attach it to the experiment. If both `importing==true` and `audioSetId` is provided in POST request at the same time, a Bad Request Error will be returned. 
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregExperimentBase greg_experiment_base:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregExperiment, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['create_audio_set', 'importing', 'context_id', 'greg_experiment_base']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_exp_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'create_audio_set' in local_var_params and local_var_params['create_audio_set'] is not None:  # noqa: E501
            query_params.append(('createAudioSet', local_var_params['create_audio_set']))  # noqa: E501
        if 'importing' in local_var_params and local_var_params['importing'] is not None:  # noqa: E501
            query_params.append(('importing', local_var_params['importing']))  # noqa: E501
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'greg_experiment_base' in local_var_params:
            body_params = local_var_params['greg_experiment_base']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/experiment', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregExperiment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_exp_put(self, uuid, **kwargs):  # noqa: E501
        """Modify Experiment  # noqa: E501

        Modify Experiment in GREG. Modifies GREG Experiment object and returns its modified content   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_exp_put(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool run: If true then the Experiment will start.
        :param GregExperimentModifiable greg_experiment_modifiable:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregExperiment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_exp_put_with_http_info(uuid, **kwargs)  # noqa: E501

    def greg_exp_put_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Modify Experiment  # noqa: E501

        Modify Experiment in GREG. Modifies GREG Experiment object and returns its modified content   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_exp_put_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool run: If true then the Experiment will start.
        :param GregExperimentModifiable greg_experiment_modifiable:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregExperiment, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'run', 'greg_experiment_modifiable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_exp_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `greg_exp_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []
        if 'run' in local_var_params and local_var_params['run'] is not None:  # noqa: E501
            query_params.append(('run', local_var_params['run']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'greg_experiment_modifiable' in local_var_params:
            body_params = local_var_params['greg_experiment_modifiable']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/experiment/{uuid}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregExperiment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_experiment_get(self, uuid, **kwargs):  # noqa: E501
        """Get Experiment  # noqa: E501

        Retrieve GREG Experiment   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_experiment_get(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregExperimentResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_experiment_get_with_http_info(uuid, **kwargs)  # noqa: E501

    def greg_experiment_get_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Get Experiment  # noqa: E501

        Retrieve GREG Experiment   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_experiment_get_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool incl_refs: set to true if referenced objects to be included in JSON in place of just their Ids
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregExperimentResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'incl_refs']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_experiment_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `greg_experiment_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []
        if 'incl_refs' in local_var_params and local_var_params['incl_refs'] is not None:  # noqa: E501
            query_params.append(('inclRefs', local_var_params['incl_refs']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/experiment/{uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregExperimentResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_grammar_post(self, **kwargs):  # noqa: E501
        """Create GREG Grammar  # noqa: E501

        Define new GREG Grammar   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_grammar_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregGrammarBaseLight greg_grammar_base_light:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregGrammar
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_grammar_post_with_http_info(**kwargs)  # noqa: E501

    def greg_grammar_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create GREG Grammar  # noqa: E501

        Define new GREG Grammar   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_grammar_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregGrammarBaseLight greg_grammar_base_light:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregGrammar, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'greg_grammar_base_light']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_grammar_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'greg_grammar_base_light' in local_var_params:
            body_params = local_var_params['greg_grammar_base_light']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/grammar', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregGrammar',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_question_get(self, uuid, **kwargs):  # noqa: E501
        """Get Question  # noqa: E501

        Retrieve GREG Question   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_question_get(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregQuestion
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_question_get_with_http_info(uuid, **kwargs)  # noqa: E501

    def greg_question_get_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Get Question  # noqa: E501

        Retrieve GREG Question   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_question_get_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregQuestion, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_question_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `greg_question_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/question/{uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregQuestion',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_question_post(self, **kwargs):  # noqa: E501
        """Create GREG Question  # noqa: E501

        Define new GREG Question   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_question_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregQuestionBase greg_question_base:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregQuestion
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_question_post_with_http_info(**kwargs)  # noqa: E501

    def greg_question_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create GREG Question  # noqa: E501

        Define new GREG Question   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_question_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param GregQuestionBase greg_question_base:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregQuestion, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'greg_question_base']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_question_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'greg_question_base' in local_var_params:
            body_params = local_var_params['greg_question_base']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/question', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregQuestion',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def greg_recog_post(self, **kwargs):  # noqa: E501
        """Create Recognition  # noqa: E501

        Upload Recogntion to GREG. Creates a new GREG Recognition object and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_recog_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param GregRecogBaseObjOrNlsml greg_recog_base_obj_or_nlsml:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregRecognition
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.greg_recog_post_with_http_info(**kwargs)  # noqa: E501

    def greg_recog_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create Recognition  # noqa: E501

        Upload Recogntion to GREG. Creates a new GREG Recognition object and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.greg_recog_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param GregRecogBaseObjOrNlsml greg_recog_base_obj_or_nlsml:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregRecognition, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['greg_recog_base_obj_or_nlsml']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method greg_recog_post" % key
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
        if 'greg_recog_base_obj_or_nlsml' in local_var_params:
            body_params = local_var_params['greg_recog_base_obj_or_nlsml']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/greg/recognition', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregRecognition',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def question_query(self, **kwargs):  # noqa: E501
        """Query Questions  # noqa: E501

        Retrieve all GREG questions.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.question_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[GregQuestion]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.question_query_with_http_info(**kwargs)  # noqa: E501

    def question_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query Questions  # noqa: E501

        Retrieve all GREG questions.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.question_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: (Optional) Context Id. Only of importance if making request without JWT. If not provided, then response will contain data from all Contexts under the Account.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[GregQuestion], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method question_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

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
            '/greg/question', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[GregQuestion]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def question_truth_put(self, uuid, **kwargs):  # noqa: E501
        """Update Truth  # noqa: E501

        Update True Recognition of Audio for a given Question   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.question_truth_put(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param GregTruthUpdates greg_truth_updates:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: GregQuestion
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.question_truth_put_with_http_info(uuid, **kwargs)  # noqa: E501

    def question_truth_put_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Update Truth  # noqa: E501

        Update True Recognition of Audio for a given Question   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.question_truth_put_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param GregTruthUpdates greg_truth_updates:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(GregQuestion, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'greg_truth_updates']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method question_truth_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `question_truth_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'greg_truth_updates' in local_var_params:
            body_params = local_var_params['greg_truth_updates']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/greg/question/{uuid}/truth', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='GregQuestion',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def recog_to_exp_post(self, uuid, **kwargs):  # noqa: E501
        """Add Recog. to Exp.  # noqa: E501

        Add new Recognition to Experiment.</br> Generally, each recognition will be added to experiment only once. </br> If, however, this method is invoked for an `audioId` that already has a recognition recorded for this Experiment,  the new recognition should overwrite the previous one.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.recog_to_exp_post(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: uuid of a GREG Experiment (required)
        :param UNKNOWN_BASE_TYPE unknown_base_type:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.recog_to_exp_post_with_http_info(uuid, **kwargs)  # noqa: E501

    def recog_to_exp_post_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Add Recog. to Exp.  # noqa: E501

        Add new Recognition to Experiment.</br> Generally, each recognition will be added to experiment only once. </br> If, however, this method is invoked for an `audioId` that already has a recognition recorded for this Experiment,  the new recognition should overwrite the previous one.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.recog_to_exp_post_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: uuid of a GREG Experiment (required)
        :param UNKNOWN_BASE_TYPE unknown_base_type:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[str], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'unknown_base_type']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method recog_to_exp_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `recog_to_exp_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'unknown_base_type' in local_var_params:
            body_params = local_var_params['unknown_base_type']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/greg/experiment/{uuid}/recognition', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[str]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
