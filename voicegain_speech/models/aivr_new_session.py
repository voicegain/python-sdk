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


class AIVRNewSession(object):
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
        'ani': 'str',
        'dnis': 'str',
        'estimated_queue_wait_seconds': 'EstimatedQueueWait',
        'logic_type': 'AIVRLogicType',
        'media': 'AIVRLogicMedia',
        'sequence': 'int',
        'sid': 'str',
        'start_time': 'datetime',
        'user_app_data': 'str',
        'vars': 'object'
    }

    attribute_map = {
        'ani': 'ani',
        'dnis': 'dnis',
        'estimated_queue_wait_seconds': 'estimatedQueueWaitSeconds',
        'logic_type': 'logicType',
        'media': 'media',
        'sequence': 'sequence',
        'sid': 'sid',
        'start_time': 'startTime',
        'user_app_data': 'userAppData',
        'vars': 'vars'
    }

    def __init__(self, ani=None, dnis=None, estimated_queue_wait_seconds=None, logic_type=None, media=None, sequence=None, sid=None, start_time=None, user_app_data=None, vars=None, local_vars_configuration=None):  # noqa: E501
        """AIVRNewSession - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._ani = None
        self._dnis = None
        self._estimated_queue_wait_seconds = None
        self._logic_type = None
        self._media = None
        self._sequence = None
        self._sid = None
        self._start_time = None
        self._user_app_data = None
        self._vars = None
        self.discriminator = None

        if ani is not None:
            self.ani = ani
        if dnis is not None:
            self.dnis = dnis
        if estimated_queue_wait_seconds is not None:
            self.estimated_queue_wait_seconds = estimated_queue_wait_seconds
        if logic_type is not None:
            self.logic_type = logic_type
        if media is not None:
            self.media = media
        self.sequence = sequence
        self.sid = sid
        self.start_time = start_time
        if user_app_data is not None:
            self.user_app_data = user_app_data
        if vars is not None:
            self.vars = vars

    @property
    def ani(self):
        """Gets the ani of this AIVRNewSession.  # noqa: E501

        (only if session originated over phone) Caller phone number or sip address   # noqa: E501

        :return: The ani of this AIVRNewSession.  # noqa: E501
        :rtype: str
        """
        return self._ani

    @ani.setter
    def ani(self, ani):
        """Sets the ani of this AIVRNewSession.

        (only if session originated over phone) Caller phone number or sip address   # noqa: E501

        :param ani: The ani of this AIVRNewSession.  # noqa: E501
        :type: str
        """

        self._ani = ani

    @property
    def dnis(self):
        """Gets the dnis of this AIVRNewSession.  # noqa: E501

        (only if session originated over phone) Called phone number or sip address  # noqa: E501

        :return: The dnis of this AIVRNewSession.  # noqa: E501
        :rtype: str
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """Sets the dnis of this AIVRNewSession.

        (only if session originated over phone) Called phone number or sip address  # noqa: E501

        :param dnis: The dnis of this AIVRNewSession.  # noqa: E501
        :type: str
        """

        self._dnis = dnis

    @property
    def estimated_queue_wait_seconds(self):
        """Gets the estimated_queue_wait_seconds of this AIVRNewSession.  # noqa: E501


        :return: The estimated_queue_wait_seconds of this AIVRNewSession.  # noqa: E501
        :rtype: EstimatedQueueWait
        """
        return self._estimated_queue_wait_seconds

    @estimated_queue_wait_seconds.setter
    def estimated_queue_wait_seconds(self, estimated_queue_wait_seconds):
        """Sets the estimated_queue_wait_seconds of this AIVRNewSession.


        :param estimated_queue_wait_seconds: The estimated_queue_wait_seconds of this AIVRNewSession.  # noqa: E501
        :type: EstimatedQueueWait
        """

        self._estimated_queue_wait_seconds = estimated_queue_wait_seconds

    @property
    def logic_type(self):
        """Gets the logic_type of this AIVRNewSession.  # noqa: E501


        :return: The logic_type of this AIVRNewSession.  # noqa: E501
        :rtype: AIVRLogicType
        """
        return self._logic_type

    @logic_type.setter
    def logic_type(self, logic_type):
        """Sets the logic_type of this AIVRNewSession.


        :param logic_type: The logic_type of this AIVRNewSession.  # noqa: E501
        :type: AIVRLogicType
        """

        self._logic_type = logic_type

    @property
    def media(self):
        """Gets the media of this AIVRNewSession.  # noqa: E501


        :return: The media of this AIVRNewSession.  # noqa: E501
        :rtype: AIVRLogicMedia
        """
        return self._media

    @media.setter
    def media(self, media):
        """Sets the media of this AIVRNewSession.


        :param media: The media of this AIVRNewSession.  # noqa: E501
        :type: AIVRLogicMedia
        """

        self._media = media

    @property
    def sequence(self):
        """Gets the sequence of this AIVRNewSession.  # noqa: E501

        sequential number within session of this callback  # noqa: E501

        :return: The sequence of this AIVRNewSession.  # noqa: E501
        :rtype: int
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this AIVRNewSession.

        sequential number within session of this callback  # noqa: E501

        :param sequence: The sequence of this AIVRNewSession.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and sequence is None:  # noqa: E501
            raise ValueError("Invalid value for `sequence`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sequence is not None and sequence < 1):  # noqa: E501
            raise ValueError("Invalid value for `sequence`, must be a value greater than or equal to `1`")  # noqa: E501

        self._sequence = sequence

    @property
    def sid(self):
        """Gets the sid of this AIVRNewSession.  # noqa: E501

        AIVR session id on Voicegain platform  # noqa: E501

        :return: The sid of this AIVRNewSession.  # noqa: E501
        :rtype: str
        """
        return self._sid

    @sid.setter
    def sid(self, sid):
        """Sets the sid of this AIVRNewSession.

        AIVR session id on Voicegain platform  # noqa: E501

        :param sid: The sid of this AIVRNewSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and sid is None:  # noqa: E501
            raise ValueError("Invalid value for `sid`, must not be `None`")  # noqa: E501

        self._sid = sid

    @property
    def start_time(self):
        """Gets the start_time of this AIVRNewSession.  # noqa: E501

        Start time of the AIVR session  # noqa: E501

        :return: The start_time of this AIVRNewSession.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this AIVRNewSession.

        Start time of the AIVR session  # noqa: E501

        :param start_time: The start_time of this AIVRNewSession.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_time is None:  # noqa: E501
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def user_app_data(self):
        """Gets the user_app_data of this AIVRNewSession.  # noqa: E501

        (optional) App specific data that was associated in the AIVR portal with this AIVR number/application.</br> It is a string that is not interpreted by the AIVR and only passed to Customer dialog engine.   # noqa: E501

        :return: The user_app_data of this AIVRNewSession.  # noqa: E501
        :rtype: str
        """
        return self._user_app_data

    @user_app_data.setter
    def user_app_data(self, user_app_data):
        """Sets the user_app_data of this AIVRNewSession.

        (optional) App specific data that was associated in the AIVR portal with this AIVR number/application.</br> It is a string that is not interpreted by the AIVR and only passed to Customer dialog engine.   # noqa: E501

        :param user_app_data: The user_app_data of this AIVRNewSession.  # noqa: E501
        :type: str
        """

        self._user_app_data = user_app_data

    @property
    def vars(self):
        """Gets the vars of this AIVRNewSession.  # noqa: E501

        (optional) Map with variables to initate the new session.   # noqa: E501

        :return: The vars of this AIVRNewSession.  # noqa: E501
        :rtype: object
        """
        return self._vars

    @vars.setter
    def vars(self, vars):
        """Sets the vars of this AIVRNewSession.

        (optional) Map with variables to initate the new session.   # noqa: E501

        :param vars: The vars of this AIVRNewSession.  # noqa: E501
        :type: object
        """

        self._vars = vars

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
        if not isinstance(other, AIVRNewSession):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AIVRNewSession):
            return True

        return self.to_dict() != other.to_dict()
