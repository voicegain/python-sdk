# coding: utf-8

"""
    Voicegain Speech Recognition API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain API This API is provided by [Voicegain](https://www.voicegain.ai) to its registered customers.  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Speech-to-Text: Recognition vs Transcription Voicegain web api provides two types of methods for speech recognition.   + **/asr/recognize** - where the purpose is to identify what was said in a context of a more constrained set of choices.   This web api uses grammars as both a language model and a way to attach semantic meaning to spoken utterances. + **/asr/transcribe** - where the purpose is to **transcribe** speech audio word for word, no meaning is attached to transcribed text.   This web api uses large vocabulary language model.      The result of transcription can be returned in three formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second.  For the transcription API, real-time incremental results will be sent back with about 2 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30 seconds (or earlier for shorter audio). Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes.  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.   # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.11.0 - updated July 31, 2020
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ascalon_web_api_client.configuration import Configuration


class AsyncResultFullAllOfResult(object):
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
        'captions': 'list[Caption]',
        'final': 'bool',
        'last_event': 'AsrProcessingEvent',
        'rms_data': 'str',
        'status': 'AsrProcessingStatus',
        'transcript': 'str',
        'ttml': 'str',
        'vad_data': 'str',
        'word_tree': 'list[WordTreeItem]',
        'words': 'list[WordItemTimed]'
    }

    attribute_map = {
        'captions': 'captions',
        'final': 'final',
        'last_event': 'lastEvent',
        'rms_data': 'rmsData',
        'status': 'status',
        'transcript': 'transcript',
        'ttml': 'ttml',
        'vad_data': 'vadData',
        'word_tree': 'wordTree',
        'words': 'words'
    }

    def __init__(self, captions=None, final=None, last_event=None, rms_data=None, status=None, transcript=None, ttml=None, vad_data=None, word_tree=None, words=None, local_vars_configuration=None):  # noqa: E501
        """AsyncResultFullAllOfResult - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._captions = None
        self._final = None
        self._last_event = None
        self._rms_data = None
        self._status = None
        self._transcript = None
        self._ttml = None
        self._vad_data = None
        self._word_tree = None
        self._words = None
        self.discriminator = None

        if captions is not None:
            self.captions = captions
        if final is not None:
            self.final = final
        if last_event is not None:
            self.last_event = last_event
        if rms_data is not None:
            self.rms_data = rms_data
        if status is not None:
            self.status = status
        if transcript is not None:
            self.transcript = transcript
        if ttml is not None:
            self.ttml = ttml
        if vad_data is not None:
            self.vad_data = vad_data
        if word_tree is not None:
            self.word_tree = word_tree
        if words is not None:
            self.words = words

    @property
    def captions(self):
        """Gets the captions of this AsyncResultFullAllOfResult.  # noqa: E501

        List of **all** captions.  Only present if captions were requested in the POST using using sessions[].content.full:[captions,...] option.   # noqa: E501

        :return: The captions of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: list[Caption]
        """
        return self._captions

    @captions.setter
    def captions(self, captions):
        """Sets the captions of this AsyncResultFullAllOfResult.

        List of **all** captions.  Only present if captions were requested in the POST using using sessions[].content.full:[captions,...] option.   # noqa: E501

        :param captions: The captions of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: list[Caption]
        """

        self._captions = captions

    @property
    def final(self):
        """Gets the final of this AsyncResultFullAllOfResult.  # noqa: E501

        whether the result is final or if it can still change  # noqa: E501

        :return: The final of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: bool
        """
        return self._final

    @final.setter
    def final(self, final):
        """Sets the final of this AsyncResultFullAllOfResult.

        whether the result is final or if it can still change  # noqa: E501

        :param final: The final of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: bool
        """

        self._final = final

    @property
    def last_event(self):
        """Gets the last_event of this AsyncResultFullAllOfResult.  # noqa: E501


        :return: The last_event of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: AsrProcessingEvent
        """
        return self._last_event

    @last_event.setter
    def last_event(self, last_event):
        """Sets the last_event of this AsyncResultFullAllOfResult.


        :param last_event: The last_event of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: AsrProcessingEvent
        """

        self._last_event = last_event

    @property
    def rms_data(self):
        """Gets the rms_data of this AsyncResultFullAllOfResult.  # noqa: E501

        Encoded data with RMS values of the source audio.</br> (Note: This field will be moved to internal API in next release and will no longer be in public API.)   # noqa: E501

        :return: The rms_data of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: str
        """
        return self._rms_data

    @rms_data.setter
    def rms_data(self, rms_data):
        """Sets the rms_data of this AsyncResultFullAllOfResult.

        Encoded data with RMS values of the source audio.</br> (Note: This field will be moved to internal API in next release and will no longer be in public API.)   # noqa: E501

        :param rms_data: The rms_data of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: str
        """

        self._rms_data = rms_data

    @property
    def status(self):
        """Gets the status of this AsyncResultFullAllOfResult.  # noqa: E501


        :return: The status of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: AsrProcessingStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this AsyncResultFullAllOfResult.


        :param status: The status of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: AsrProcessingStatus
        """

        self._status = status

    @property
    def transcript(self):
        """Gets the transcript of this AsyncResultFullAllOfResult.  # noqa: E501

        final content of the transcript  # noqa: E501

        :return: The transcript of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: str
        """
        return self._transcript

    @transcript.setter
    def transcript(self, transcript):
        """Sets the transcript of this AsyncResultFullAllOfResult.

        final content of the transcript  # noqa: E501

        :param transcript: The transcript of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: str
        """

        self._transcript = transcript

    @property
    def ttml(self):
        """Gets the ttml of this AsyncResultFullAllOfResult.  # noqa: E501

        Link to download the ttml data for all the transcripts of the entire audio.  Only present if captions were requested in the POST using sessions[].content.full:[captions,...] option. How long the data will be available depends on the session.poll.persist setting in the POST request.</br> **deprecated** Use **GET /asr/transcribe/{sessionId}/transcript**   # noqa: E501

        :return: The ttml of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: str
        """
        return self._ttml

    @ttml.setter
    def ttml(self, ttml):
        """Sets the ttml of this AsyncResultFullAllOfResult.

        Link to download the ttml data for all the transcripts of the entire audio.  Only present if captions were requested in the POST using sessions[].content.full:[captions,...] option. How long the data will be available depends on the session.poll.persist setting in the POST request.</br> **deprecated** Use **GET /asr/transcribe/{sessionId}/transcript**   # noqa: E501

        :param ttml: The ttml of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: str
        """

        self._ttml = ttml

    @property
    def vad_data(self):
        """Gets the vad_data of this AsyncResultFullAllOfResult.  # noqa: E501

        Encoded data with VAD values of the source audio.</br> (Note: This field will be moved to internal API in next release and will no longer be in public API.)   # noqa: E501

        :return: The vad_data of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: str
        """
        return self._vad_data

    @vad_data.setter
    def vad_data(self, vad_data):
        """Sets the vad_data of this AsyncResultFullAllOfResult.

        Encoded data with VAD values of the source audio.</br> (Note: This field will be moved to internal API in next release and will no longer be in public API.)   # noqa: E501

        :param vad_data: The vad_data of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: str
        """

        self._vad_data = vad_data

    @property
    def word_tree(self):
        """Gets the word_tree of this AsyncResultFullAllOfResult.  # noqa: E501

        Next incremental list of the transcribed words with details like- tree id and parent id, confidence, timing  # noqa: E501

        :return: The word_tree of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: list[WordTreeItem]
        """
        return self._word_tree

    @word_tree.setter
    def word_tree(self, word_tree):
        """Sets the word_tree of this AsyncResultFullAllOfResult.

        Next incremental list of the transcribed words with details like- tree id and parent id, confidence, timing  # noqa: E501

        :param word_tree: The word_tree of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: list[WordTreeItem]
        """

        self._word_tree = word_tree

    @property
    def words(self):
        """Gets the words of this AsyncResultFullAllOfResult.  # noqa: E501

        List of all the transcribed words with details like confidence and timing  # noqa: E501

        :return: The words of this AsyncResultFullAllOfResult.  # noqa: E501
        :rtype: list[WordItemTimed]
        """
        return self._words

    @words.setter
    def words(self, words):
        """Sets the words of this AsyncResultFullAllOfResult.

        List of all the transcribed words with details like confidence and timing  # noqa: E501

        :param words: The words of this AsyncResultFullAllOfResult.  # noqa: E501
        :type: list[WordItemTimed]
        """

        self._words = words

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
        if not isinstance(other, AsyncResultFullAllOfResult):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsyncResultFullAllOfResult):
            return True

        return self.to_dict() != other.to_dict()