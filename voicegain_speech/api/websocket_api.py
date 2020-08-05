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

from voicegain_speech.api_client import ApiClient
from voicegain_speech.exceptions import (
    ApiTypeError,
    ApiValueError
)


class WebsocketApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def websocket_delete(self, name, **kwargs):  # noqa: E501
        """Delete websocket  # noqa: E501

        Delete websocket object identified by a name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_delete(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Websocket
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.websocket_delete_with_http_info(name, **kwargs)  # noqa: E501

    def websocket_delete_with_http_info(self, name, **kwargs):  # noqa: E501
        """Delete websocket  # noqa: E501

        Delete websocket object identified by a name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_delete_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Websocket, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method websocket_delete" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in local_var_params or  # noqa: E501
                                                        local_var_params['name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `name` when calling `websocket_delete`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in local_var_params:
            path_params['name'] = local_var_params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/websocket/{name}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Websocket',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def websocket_get(self, name, **kwargs):  # noqa: E501
        """Get websocket  # noqa: E501

        Get websocket object by its unique name. Note, this method does not require JWT Token, but if JWT token is missing and websocket is not public it will return error response.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_get(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param str msg_dates: Date or Dates of events. Values are in UTC time.
        :param int msg_count: Max number of messages to return
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Websocket
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.websocket_get_with_http_info(name, **kwargs)  # noqa: E501

    def websocket_get_with_http_info(self, name, **kwargs):  # noqa: E501
        """Get websocket  # noqa: E501

        Get websocket object by its unique name. Note, this method does not require JWT Token, but if JWT token is missing and websocket is not public it will return error response.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_get_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param str msg_dates: Date or Dates of events. Values are in UTC time.
        :param int msg_count: Max number of messages to return
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Websocket, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name', 'msg_dates', 'msg_count']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method websocket_get" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in local_var_params or  # noqa: E501
                                                        local_var_params['name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `name` when calling `websocket_get`")  # noqa: E501

        if self.api_client.client_side_validation and 'msg_count' in local_var_params and local_var_params['msg_count'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `msg_count` when calling `websocket_get`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}
        if 'name' in local_var_params:
            path_params['name'] = local_var_params['name']  # noqa: E501

        query_params = []
        if 'msg_dates' in local_var_params and local_var_params['msg_dates'] is not None:  # noqa: E501
            query_params.append(('msgDates', local_var_params['msg_dates']))  # noqa: E501
        if 'msg_count' in local_var_params and local_var_params['msg_count'] is not None:  # noqa: E501
            query_params.append(('msgCount', local_var_params['msg_count']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/websocket/{name}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Websocket',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def websocket_message_post(self, name, **kwargs):  # noqa: E501
        """Add websocket msg  # noqa: E501

        Adds a new message to the named websocket.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_message_post(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param WebsocketMsg websocket_msg: Body of websocket message request. Note that time is optional in the message.  The default message insertion time is the current time of the request. 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Websocket
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.websocket_message_post_with_http_info(name, **kwargs)  # noqa: E501

    def websocket_message_post_with_http_info(self, name, **kwargs):  # noqa: E501
        """Add websocket msg  # noqa: E501

        Adds a new message to the named websocket.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_message_post_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param WebsocketMsg websocket_msg: Body of websocket message request. Note that time is optional in the message.  The default message insertion time is the current time of the request. 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Websocket, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name', 'websocket_msg']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method websocket_message_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in local_var_params or  # noqa: E501
                                                        local_var_params['name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `name` when calling `websocket_message_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in local_var_params:
            path_params['name'] = local_var_params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'websocket_msg' in local_var_params:
            body_params = local_var_params['websocket_msg']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/websocket/{name}/message', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Websocket',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def websocket_post(self, websocket_modifiable, **kwargs):  # noqa: E501
        """Create websocket  # noqa: E501

        Create websocket object with unique name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_post(websocket_modifiable, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param WebsocketModifiable websocket_modifiable: Body of websocket creation request.  Note: contextId will generally be extracted from the JWT, so it is optional.  (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Websocket
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.websocket_post_with_http_info(websocket_modifiable, **kwargs)  # noqa: E501

    def websocket_post_with_http_info(self, websocket_modifiable, **kwargs):  # noqa: E501
        """Create websocket  # noqa: E501

        Create websocket object with unique name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_post_with_http_info(websocket_modifiable, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param WebsocketModifiable websocket_modifiable: Body of websocket creation request.  Note: contextId will generally be extracted from the JWT, so it is optional.  (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Websocket, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['websocket_modifiable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method websocket_post" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'websocket_modifiable' is set
        if self.api_client.client_side_validation and ('websocket_modifiable' not in local_var_params or  # noqa: E501
                                                        local_var_params['websocket_modifiable'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `websocket_modifiable` when calling `websocket_post`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'websocket_modifiable' in local_var_params:
            body_params = local_var_params['websocket_modifiable']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON', 'application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth', 'macSignature']  # noqa: E501

        return self.api_client.call_api(
            '/websocket', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Websocket',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def websocket_put(self, name, **kwargs):  # noqa: E501
        """Modify websocket  # noqa: E501

        Modify websocket object identified by a name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_put(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param WebsocketModifiable websocket_modifiable: Body of websocket modification request.  Fields not included in request mody will not be modified. 
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Websocket
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.websocket_put_with_http_info(name, **kwargs)  # noqa: E501

    def websocket_put_with_http_info(self, name, **kwargs):  # noqa: E501
        """Modify websocket  # noqa: E501

        Modify websocket object identified by a name.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.websocket_put_with_http_info(name, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str name: name of an object (only select objects have unique names) (required)
        :param WebsocketModifiable websocket_modifiable: Body of websocket modification request.  Fields not included in request mody will not be modified. 
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Websocket, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['name', 'websocket_modifiable']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method websocket_put" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'name' is set
        if self.api_client.client_side_validation and ('name' not in local_var_params or  # noqa: E501
                                                        local_var_params['name'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `name` when calling `websocket_put`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'name' in local_var_params:
            path_params['name'] = local_var_params['name']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'websocket_modifiable' in local_var_params:
            body_params = local_var_params['websocket_modifiable']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/JSON'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerJWTAuth']  # noqa: E501

        return self.api_client.call_api(
            '/websocket/{name}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='Websocket',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
