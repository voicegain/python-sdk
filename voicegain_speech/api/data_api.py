# coding: utf-8

"""
    Voicegain Speech Recognition API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain API This API is provided by [Voicegain](https://www.voicegain.ai) to its registered customers.  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Speech-to-Text: Recognition vs Transcription Voicegain web api provides two types of methods for speech recognition.   + **/asr/recognize** - where the purpose is to identify what was said in a context of a more constrained set of choices.   This web api uses grammars as both a language model and a way to attach semantic meaning to spoken utterances. + **/asr/transcribe** - where the purpose is to **transcribe** speech audio word for word, no meaning is attached to transcribed text.   This web api uses large vocabulary language model.      The result of transcription can be returned in three formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second.  For the transcription API, real-time incremental results will be sent back with about 2 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30 seconds (or earlier for shorter audio). Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes.  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.   # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.11.0 - updated July 31, 2020
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ascalon_web_api_client.api_client import ApiClient
from ascalon_web_api_client.exceptions import (
    ApiTypeError,
    ApiValueError
)


class DataApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def data_audio_post(self, **kwargs):  # noqa: E501
        """Create from audio  # noqa: E501

        Upload audio data to simple object store. Creates a new DataObject and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_audio_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param bool reuse: If set to true, then will not create a new object if an object already exists with the same data content and metadata  (specifically, the metadata fields that were included in the request - the other metadata fields do not matter when determining a match).  If that's the case then the id of matching already-existing object will be returned. 
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param DataObjectWithAudio data_object_with_audio: Request body with info about the audio data source.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_audio_post_with_http_info(**kwargs)  # noqa: E501

    def data_audio_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create from audio  # noqa: E501

        Upload audio data to simple object store. Creates a new DataObject and returns its ID   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_audio_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param bool reuse: If set to true, then will not create a new object if an object already exists with the same data content and metadata  (specifically, the metadata fields that were included in the request - the other metadata fields do not matter when determining a match).  If that's the case then the id of matching already-existing object will be returned. 
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param DataObjectWithAudio data_object_with_audio: Request body with info about the audio data source.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'reuse', 'transcode', 'data_object_with_audio']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_audio_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'reuse' in local_var_params and local_var_params['reuse'] is not None:  # noqa: E501
            query_params.append(('reuse', local_var_params['reuse']))  # noqa: E501
        if 'transcode' in local_var_params and local_var_params['transcode'] is not None:  # noqa: E501
            query_params.append(('transcode', local_var_params['transcode']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data_object_with_audio' in local_var_params:
            body_params = local_var_params['data_object_with_audio']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data/audio', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_audio_put(self, uuid, **kwargs):  # noqa: E501
        """Modify audio data  # noqa: E501

        Modify data object.  This method modifies the metdata. Can also modify the audio content.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_audio_put(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool append: How should lists be modified. If true then new data will be appended to old, if false then old data will be replace by new.
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param DataObjectWithAudio data_object_with_audio:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_audio_put_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_audio_put_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Modify audio data  # noqa: E501

        Modify data object.  This method modifies the metdata. Can also modify the audio content.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_audio_put_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool append: How should lists be modified. If true then new data will be appended to old, if false then old data will be replace by new.
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param DataObjectWithAudio data_object_with_audio:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'append', 'transcode', 'data_object_with_audio']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_audio_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_audio_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []
        if 'append' in local_var_params and local_var_params['append'] is not None:  # noqa: E501
            query_params.append(('append', local_var_params['append']))  # noqa: E501
        if 'transcode' in local_var_params and local_var_params['transcode'] is not None:  # noqa: E501
            query_params.append(('transcode', local_var_params['transcode']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data_object_with_audio' in local_var_params:
            body_params = local_var_params['data_object_with_audio']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data/{uuid}/audio', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_delete(self, uuid, **kwargs):  # noqa: E501
        """Delete data object  # noqa: E501

        Delete data object.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_delete(uuid, async_req=True)
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
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_delete_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_delete_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Delete data object  # noqa: E501

        Delete data object.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_delete_with_http_info(uuid, async_req=True)
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
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
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
                    " to method data_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_delete`")  # noqa: E501

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
            '/data/{uuid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_file_delete(self, uuid, **kwargs):  # noqa: E501
        """Delete data file  # noqa: E501

        Delete association with the raw data represented by the data object. Does not delete the object itself.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_delete(uuid, async_req=True)
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
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_file_delete_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_file_delete_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Delete data file  # noqa: E501

        Delete association with the raw data represented by the data object. Does not delete the object itself.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_delete_with_http_info(uuid, async_req=True)
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
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
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
                    " to method data_file_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_file_delete`")  # noqa: E501

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
            '/data/{uuid}/file', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_file_get(self, uuid, **kwargs):  # noqa: E501
        """Get data file  # noqa: E501

        Get data object.  Raw (file) object data will be returned from simple object store.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_get(uuid, async_req=True)
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
        return self.data_file_get_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_file_get_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Get data file  # noqa: E501

        Get data object.  Raw (file) object data will be returned from simple object store.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_get_with_http_info(uuid, async_req=True)
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
                    " to method data_file_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_file_get`")  # noqa: E501

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
            ['audio/*, text/*, */*', 'application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data/{uuid}/file', 'GET',
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

    def data_file_post(self, **kwargs):  # noqa: E501
        """Create from file  # noqa: E501

        Upload data as **multipart/form-data** to simple object store.  Creates a new DataObject and returns its ID. Suitable for uploads of files.   There are two form keys: 'file' and 'objectdata'. objectdata is optional.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param bool reuse: If set to true, then will not create a new object if an object already exists with the same data content and metadata  (specifically, the metadata fields that were included in the request - the other metadata fields do not matter when determining a match).  If that's the case then the id of matching already-existing object will be returned. 
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param file file: Part of the form labeled 'file' contains file to be uploaded
        :param file objectdata: Second, optional, part of the form containing accompanying metadata.  Labeled 'objectdata'.  Payload contained in this part of the form has to be valid JSON following the Data object schema 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_file_post_with_http_info(**kwargs)  # noqa: E501

    def data_file_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create from file  # noqa: E501

        Upload data as **multipart/form-data** to simple object store.  Creates a new DataObject and returns its ID. Suitable for uploads of files.   There are two form keys: 'file' and 'objectdata'. objectdata is optional.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param bool reuse: If set to true, then will not create a new object if an object already exists with the same data content and metadata  (specifically, the metadata fields that were included in the request - the other metadata fields do not matter when determining a match).  If that's the case then the id of matching already-existing object will be returned. 
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param file file: Part of the form labeled 'file' contains file to be uploaded
        :param file objectdata: Second, optional, part of the form containing accompanying metadata.  Labeled 'objectdata'.  Payload contained in this part of the form has to be valid JSON following the Data object schema 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'reuse', 'transcode', 'file', 'objectdata']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_file_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'reuse' in local_var_params and local_var_params['reuse'] is not None:  # noqa: E501
            query_params.append(('reuse', local_var_params['reuse']))  # noqa: E501
        if 'transcode' in local_var_params and local_var_params['transcode'] is not None:  # noqa: E501
            query_params.append(('transcode', local_var_params['transcode']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in local_var_params:
            local_var_files['file'] = local_var_params['file']  # noqa: E501
        if 'objectdata' in local_var_params:
            local_var_files['objectdata'] = local_var_params['objectdata']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data/file', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_file_put(self, uuid, **kwargs):  # noqa: E501
        """Modify data file  # noqa: E501

        Modify data object.  This modifies the raw data (i.e. content type is multipart/form-data).  In multipart/form-data, there are two form keys: 'file' and 'objectdata'. objectdata is optional.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_put(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool append: How should lists be modified. If true then new data will be appended to old, if false then old data will be replace by new.
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param file file: Part of the form labeled 'file' contains file to be uploaded
        :param file objectdata: Second, optional, part of the form containing accompanying metadata.  Labeled 'objectdata'.  Payload contained in this part of the form has to be valid JSON following the Data object schema 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_file_put_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_file_put_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Modify data file  # noqa: E501

        Modify data object.  This modifies the raw data (i.e. content type is multipart/form-data).  In multipart/form-data, there are two form keys: 'file' and 'objectdata'. objectdata is optional.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_file_put_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool append: How should lists be modified. If true then new data will be appended to old, if false then old data will be replace by new.
        :param str transcode: Controls transcode of audio data. By default audio transcode is enabled.
        :param file file: Part of the form labeled 'file' contains file to be uploaded
        :param file objectdata: Second, optional, part of the form containing accompanying metadata.  Labeled 'objectdata'.  Payload contained in this part of the form has to be valid JSON following the Data object schema 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'append', 'transcode', 'file', 'objectdata']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_file_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_file_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []
        if 'append' in local_var_params and local_var_params['append'] is not None:  # noqa: E501
            query_params.append(('append', local_var_params['append']))  # noqa: E501
        if 'transcode' in local_var_params and local_var_params['transcode'] is not None:  # noqa: E501
            query_params.append(('transcode', local_var_params['transcode']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'file' in local_var_params:
            local_var_files['file'] = local_var_params['file']  # noqa: E501
        if 'objectdata' in local_var_params:
            local_var_files['objectdata'] = local_var_params['objectdata']  # noqa: E501

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data/{uuid}/file', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_get(self, uuid, **kwargs):  # noqa: E501
        """Get data object.  # noqa: E501

        Get data object.  JSON metadata for the given ObjectData will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_get(uuid, async_req=True)
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
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_get_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_get_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Get data object.  # noqa: E501

        Get data object.  JSON metadata for the given ObjectData will be returned.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_get_with_http_info(uuid, async_req=True)
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
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
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
                    " to method data_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_get`")  # noqa: E501

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
            '/data/{uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_post(self, **kwargs):  # noqa: E501
        """Create data object  # noqa: E501

        Creates a new DataObject and returns its ID  Note that the body of application/json can be empty, i.e. {},   in which case an empty Data Object will be created that can be modified later using PUT method.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_post(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param DataObjectModifiable data_object_modifiable:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_post_with_http_info(**kwargs)  # noqa: E501

    def data_post_with_http_info(self, **kwargs):  # noqa: E501
        """Create data object  # noqa: E501

        Creates a new DataObject and returns its ID  Note that the body of application/json can be empty, i.e. {},   in which case an empty Data Object will be created that can be modified later using PUT method.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_post_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param DataObjectModifiable data_object_modifiable:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'data_object_modifiable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_post" % key
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
        if 'data_object_modifiable' in local_var_params:
            body_params = local_var_params['data_object_modifiable']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_put(self, uuid, **kwargs):  # noqa: E501
        """Modify data object  # noqa: E501

        Modify the metadata of the Data Object.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_put(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool append: How should lists be modified. If true then new data will be appended to old, if false then old data will be replace by new.
        :param DataObjectModifiable data_object_modifiable:
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: DataObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_put_with_http_info(uuid, **kwargs)  # noqa: E501

    def data_put_with_http_info(self, uuid, **kwargs):  # noqa: E501
        """Modify data object  # noqa: E501

        Modify the metadata of the Data Object.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_put_with_http_info(uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str uuid: UUID of an object. **Note** - attempt to access objects outside of the Account will return an Error. (required)
        :param bool append: How should lists be modified. If true then new data will be appended to old, if false then old data will be replace by new.
        :param DataObjectModifiable data_object_modifiable:
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(DataObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['uuid', 'append', 'data_object_modifiable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'uuid' is set
        if self.api_client.client_side_validation and ('uuid' not in local_var_params or  # noqa: E501
                                                        local_var_params['uuid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `uuid` when calling `data_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'uuid' in local_var_params:
            path_params['uuid'] = local_var_params['uuid']  # noqa: E501

        query_params = []
        if 'append' in local_var_params and local_var_params['append'] is not None:  # noqa: E501
            query_params.append(('append', local_var_params['append']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'data_object_modifiable' in local_var_params:
            body_params = local_var_params['data_object_modifiable']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/data/{uuid}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='DataObject',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def data_query(self, **kwargs):  # noqa: E501
        """Query data objects.  # noqa: E501

        Query data objects that satisfy given criteria.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_query(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param str tags_incl: Tag or tags to match in results, multiple tags should be separated by comma `,`  Assumes an OR if multiple tags provided. 
        :param str tags_excl: Tag or tags to not include in results, multiple tags should be separated by comma `,` Assumes an OR if multiple tags provided. 
        :param str name: Name to match. If the provided name ends with a star `*` then a prefix match will be performed.</br> Note - the star is allowed only in the last position (arbitrary wildcard matching is not supported). 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[DataObject]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.data_query_with_http_info(**kwargs)  # noqa: E501

    def data_query_with_http_info(self, **kwargs):  # noqa: E501
        """Query data objects.  # noqa: E501

        Query data objects that satisfy given criteria.    # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.data_query_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str context_id: Context Id. Only needed if making a request without JWT but using MAC Access Authentication instead.
        :param str tags_incl: Tag or tags to match in results, multiple tags should be separated by comma `,`  Assumes an OR if multiple tags provided. 
        :param str tags_excl: Tag or tags to not include in results, multiple tags should be separated by comma `,` Assumes an OR if multiple tags provided. 
        :param str name: Name to match. If the provided name ends with a star `*` then a prefix match will be performed.</br> Note - the star is allowed only in the last position (arbitrary wildcard matching is not supported). 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[DataObject], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['context_id', 'tags_incl', 'tags_excl', 'name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method data_query" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'context_id' in local_var_params and local_var_params['context_id'] is not None:  # noqa: E501
            query_params.append(('contextId', local_var_params['context_id']))  # noqa: E501
        if 'tags_incl' in local_var_params and local_var_params['tags_incl'] is not None:  # noqa: E501
            query_params.append(('tagsIncl', local_var_params['tags_incl']))  # noqa: E501
        if 'tags_excl' in local_var_params and local_var_params['tags_excl'] is not None:  # noqa: E501
            query_params.append(('tagsExcl', local_var_params['tags_excl']))  # noqa: E501
        if 'name' in local_var_params and local_var_params['name'] is not None:  # noqa: E501
            query_params.append(('name', local_var_params['name']))  # noqa: E501

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
            '/data', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[DataObject]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)