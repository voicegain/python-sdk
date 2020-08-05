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


class CoreAIVRSession(object):
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
        'aivr_app_id': 'str',
        'aivr_logic': 'list[AIVRLogic]',
        'audio_server_url': 'str',
        'current_active_logic': 'AIVRLogicType',
        'current_media': 'AIVRLogicMedia',
        'events': 'list[AIVREvent]',
        'ivr_sid': 'str',
        'loop': 'str',
        'prompt': 'dict(str, AIVRPromptPlaying)',
        'recordings': 'list[AIVRRecording]',
        'sequence': 'int',
        'start_time': 'datetime',
        'telco_data': 'CoreAIVRSessionTelcoData',
        'terminated': 'str',
        'user_session_data': 'object',
        'vars': 'object'
    }

    attribute_map = {
        'aivr_app_id': 'aivrAppId',
        'aivr_logic': 'aivrLogic',
        'audio_server_url': 'audioServerUrl',
        'current_active_logic': 'currentActiveLogic',
        'current_media': 'currentMedia',
        'events': 'events',
        'ivr_sid': 'ivrSid',
        'loop': 'loop',
        'prompt': 'prompt',
        'recordings': 'recordings',
        'sequence': 'sequence',
        'start_time': 'startTime',
        'telco_data': 'telcoData',
        'terminated': 'terminated',
        'user_session_data': 'userSessionData',
        'vars': 'vars'
    }

    def __init__(self, aivr_app_id=None, aivr_logic=None, audio_server_url=None, current_active_logic=None, current_media=None, events=None, ivr_sid=None, loop=None, prompt=None, recordings=None, sequence=None, start_time=None, telco_data=None, terminated=None, user_session_data=None, vars=None, local_vars_configuration=None):  # noqa: E501
        """CoreAIVRSession - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._aivr_app_id = None
        self._aivr_logic = None
        self._audio_server_url = None
        self._current_active_logic = None
        self._current_media = None
        self._events = None
        self._ivr_sid = None
        self._loop = None
        self._prompt = None
        self._recordings = None
        self._sequence = None
        self._start_time = None
        self._telco_data = None
        self._terminated = None
        self._user_session_data = None
        self._vars = None
        self.discriminator = None

        self.aivr_app_id = aivr_app_id
        if aivr_logic is not None:
            self.aivr_logic = aivr_logic
        if audio_server_url is not None:
            self.audio_server_url = audio_server_url
        if current_active_logic is not None:
            self.current_active_logic = current_active_logic
        if current_media is not None:
            self.current_media = current_media
        if events is not None:
            self.events = events
        self.ivr_sid = ivr_sid
        if loop is not None:
            self.loop = loop
        if prompt is not None:
            self.prompt = prompt
        if recordings is not None:
            self.recordings = recordings
        if sequence is not None:
            self.sequence = sequence
        self.start_time = start_time
        if telco_data is not None:
            self.telco_data = telco_data
        if terminated is not None:
            self.terminated = terminated
        if user_session_data is not None:
            self.user_session_data = user_session_data
        if vars is not None:
            self.vars = vars

    @property
    def aivr_app_id(self):
        """Gets the aivr_app_id of this CoreAIVRSession.  # noqa: E501

        UUID of the AIVR App to which this AIVR session belongs.  # noqa: E501

        :return: The aivr_app_id of this CoreAIVRSession.  # noqa: E501
        :rtype: str
        """
        return self._aivr_app_id

    @aivr_app_id.setter
    def aivr_app_id(self, aivr_app_id):
        """Sets the aivr_app_id of this CoreAIVRSession.

        UUID of the AIVR App to which this AIVR session belongs.  # noqa: E501

        :param aivr_app_id: The aivr_app_id of this CoreAIVRSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and aivr_app_id is None:  # noqa: E501
            raise ValueError("Invalid value for `aivr_app_id`, must not be `None`")  # noqa: E501

        self._aivr_app_id = aivr_app_id

    @property
    def aivr_logic(self):
        """Gets the aivr_logic of this CoreAIVRSession.  # noqa: E501


        :return: The aivr_logic of this CoreAIVRSession.  # noqa: E501
        :rtype: list[AIVRLogic]
        """
        return self._aivr_logic

    @aivr_logic.setter
    def aivr_logic(self, aivr_logic):
        """Sets the aivr_logic of this CoreAIVRSession.


        :param aivr_logic: The aivr_logic of this CoreAIVRSession.  # noqa: E501
        :type: list[AIVRLogic]
        """

        self._aivr_logic = aivr_logic

    @property
    def audio_server_url(self):
        """Gets the audio_server_url of this CoreAIVRSession.  # noqa: E501

        URL of the AudioServer associated with this session  # noqa: E501

        :return: The audio_server_url of this CoreAIVRSession.  # noqa: E501
        :rtype: str
        """
        return self._audio_server_url

    @audio_server_url.setter
    def audio_server_url(self, audio_server_url):
        """Sets the audio_server_url of this CoreAIVRSession.

        URL of the AudioServer associated with this session  # noqa: E501

        :param audio_server_url: The audio_server_url of this CoreAIVRSession.  # noqa: E501
        :type: str
        """

        self._audio_server_url = audio_server_url

    @property
    def current_active_logic(self):
        """Gets the current_active_logic of this CoreAIVRSession.  # noqa: E501


        :return: The current_active_logic of this CoreAIVRSession.  # noqa: E501
        :rtype: AIVRLogicType
        """
        return self._current_active_logic

    @current_active_logic.setter
    def current_active_logic(self, current_active_logic):
        """Sets the current_active_logic of this CoreAIVRSession.


        :param current_active_logic: The current_active_logic of this CoreAIVRSession.  # noqa: E501
        :type: AIVRLogicType
        """

        self._current_active_logic = current_active_logic

    @property
    def current_media(self):
        """Gets the current_media of this CoreAIVRSession.  # noqa: E501


        :return: The current_media of this CoreAIVRSession.  # noqa: E501
        :rtype: AIVRLogicMedia
        """
        return self._current_media

    @current_media.setter
    def current_media(self, current_media):
        """Sets the current_media of this CoreAIVRSession.


        :param current_media: The current_media of this CoreAIVRSession.  # noqa: E501
        :type: AIVRLogicMedia
        """

        self._current_media = current_media

    @property
    def events(self):
        """Gets the events of this CoreAIVRSession.  # noqa: E501

        List of AIVR events that occurred since start of the session  # noqa: E501

        :return: The events of this CoreAIVRSession.  # noqa: E501
        :rtype: list[AIVREvent]
        """
        return self._events

    @events.setter
    def events(self, events):
        """Sets the events of this CoreAIVRSession.

        List of AIVR events that occurred since start of the session  # noqa: E501

        :param events: The events of this CoreAIVRSession.  # noqa: E501
        :type: list[AIVREvent]
        """

        self._events = events

    @property
    def ivr_sid(self):
        """Gets the ivr_sid of this CoreAIVRSession.  # noqa: E501

        AIVR session id on Voicegain platform  # noqa: E501

        :return: The ivr_sid of this CoreAIVRSession.  # noqa: E501
        :rtype: str
        """
        return self._ivr_sid

    @ivr_sid.setter
    def ivr_sid(self, ivr_sid):
        """Sets the ivr_sid of this CoreAIVRSession.

        AIVR session id on Voicegain platform  # noqa: E501

        :param ivr_sid: The ivr_sid of this CoreAIVRSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and ivr_sid is None:  # noqa: E501
            raise ValueError("Invalid value for `ivr_sid`, must not be `None`")  # noqa: E501

        self._ivr_sid = ivr_sid

    @property
    def loop(self):
        """Gets the loop of this CoreAIVRSession.  # noqa: E501

        State of the processing loop: - new - session was just created and loop has not been started yet - start - request has been placed to start the loop - running - loop has been started and is running - stop - request has been placed to stop the loop - stopped - loop has been stopped - session processing has finished  Note: A single session may execute multiple loops, each corresponding to different Logic defined in AIVR App.</br> When `loop` value is being set to **start** by PUT, `nextActiveLogic` will generally be provided to indicate which logic to run in the loop.</br> If that value is not provided, then the value of `currentActiveLogic` will be used.   # noqa: E501

        :return: The loop of this CoreAIVRSession.  # noqa: E501
        :rtype: str
        """
        return self._loop

    @loop.setter
    def loop(self, loop):
        """Sets the loop of this CoreAIVRSession.

        State of the processing loop: - new - session was just created and loop has not been started yet - start - request has been placed to start the loop - running - loop has been started and is running - stop - request has been placed to stop the loop - stopped - loop has been stopped - session processing has finished  Note: A single session may execute multiple loops, each corresponding to different Logic defined in AIVR App.</br> When `loop` value is being set to **start** by PUT, `nextActiveLogic` will generally be provided to indicate which logic to run in the loop.</br> If that value is not provided, then the value of `currentActiveLogic` will be used.   # noqa: E501

        :param loop: The loop of this CoreAIVRSession.  # noqa: E501
        :type: str
        """
        allowed_values = ["new", "start", "running", "stop", "stopped"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and loop not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `loop` ({0}), must be one of {1}"  # noqa: E501
                .format(loop, allowed_values)
            )

        self._loop = loop

    @property
    def prompt(self):
        """Gets the prompt of this CoreAIVRSession.  # noqa: E501

        map from prompt id to AIVRPromptPlaying object, see example  # noqa: E501

        :return: The prompt of this CoreAIVRSession.  # noqa: E501
        :rtype: dict(str, AIVRPromptPlaying)
        """
        return self._prompt

    @prompt.setter
    def prompt(self, prompt):
        """Sets the prompt of this CoreAIVRSession.

        map from prompt id to AIVRPromptPlaying object, see example  # noqa: E501

        :param prompt: The prompt of this CoreAIVRSession.  # noqa: E501
        :type: dict(str, AIVRPromptPlaying)
        """

        self._prompt = prompt

    @property
    def recordings(self):
        """Gets the recordings of this CoreAIVRSession.  # noqa: E501


        :return: The recordings of this CoreAIVRSession.  # noqa: E501
        :rtype: list[AIVRRecording]
        """
        return self._recordings

    @recordings.setter
    def recordings(self, recordings):
        """Sets the recordings of this CoreAIVRSession.


        :param recordings: The recordings of this CoreAIVRSession.  # noqa: E501
        :type: list[AIVRRecording]
        """

        self._recordings = recordings

    @property
    def sequence(self):
        """Gets the sequence of this CoreAIVRSession.  # noqa: E501

        sequential number within session of next callback to be made  # noqa: E501

        :return: The sequence of this CoreAIVRSession.  # noqa: E501
        :rtype: int
        """
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        """Sets the sequence of this CoreAIVRSession.

        sequential number within session of next callback to be made  # noqa: E501

        :param sequence: The sequence of this CoreAIVRSession.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                sequence is not None and sequence < 1):  # noqa: E501
            raise ValueError("Invalid value for `sequence`, must be a value greater than or equal to `1`")  # noqa: E501

        self._sequence = sequence

    @property
    def start_time(self):
        """Gets the start_time of this CoreAIVRSession.  # noqa: E501

        Start time of the AIVR session  # noqa: E501

        :return: The start_time of this CoreAIVRSession.  # noqa: E501
        :rtype: datetime
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this CoreAIVRSession.

        Start time of the AIVR session  # noqa: E501

        :param start_time: The start_time of this CoreAIVRSession.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_time is None:  # noqa: E501
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def telco_data(self):
        """Gets the telco_data of this CoreAIVRSession.  # noqa: E501


        :return: The telco_data of this CoreAIVRSession.  # noqa: E501
        :rtype: CoreAIVRSessionTelcoData
        """
        return self._telco_data

    @telco_data.setter
    def telco_data(self, telco_data):
        """Sets the telco_data of this CoreAIVRSession.


        :param telco_data: The telco_data of this CoreAIVRSession.  # noqa: E501
        :type: CoreAIVRSessionTelcoData
        """

        self._telco_data = telco_data

    @property
    def terminated(self):
        """Gets the terminated of this CoreAIVRSession.  # noqa: E501

        how the AIVR session was terminated (if it has already been terminated)  # noqa: E501

        :return: The terminated of this CoreAIVRSession.  # noqa: E501
        :rtype: str
        """
        return self._terminated

    @terminated.setter
    def terminated(self, terminated):
        """Sets the terminated of this CoreAIVRSession.

        how the AIVR session was terminated (if it has already been terminated)  # noqa: E501

        :param terminated: The terminated of this CoreAIVRSession.  # noqa: E501
        :type: str
        """
        allowed_values = ["hangup", "disconnect", "error"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and terminated not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `terminated` ({0}), must be one of {1}"  # noqa: E501
                .format(terminated, allowed_values)
            )

        self._terminated = terminated

    @property
    def user_session_data(self):
        """Gets the user_session_data of this CoreAIVRSession.  # noqa: E501

        Map with relevant session data passed at the start of the AIVR Session from the page invoking AIVR.</br> Data is not interpreted by the AIVR and only passed to Customer dialog engine.   # noqa: E501

        :return: The user_session_data of this CoreAIVRSession.  # noqa: E501
        :rtype: object
        """
        return self._user_session_data

    @user_session_data.setter
    def user_session_data(self, user_session_data):
        """Sets the user_session_data of this CoreAIVRSession.

        Map with relevant session data passed at the start of the AIVR Session from the page invoking AIVR.</br> Data is not interpreted by the AIVR and only passed to Customer dialog engine.   # noqa: E501

        :param user_session_data: The user_session_data of this CoreAIVRSession.  # noqa: E501
        :type: object
        """

        self._user_session_data = user_session_data

    @property
    def vars(self):
        """Gets the vars of this CoreAIVRSession.  # noqa: E501

        Map with user reponses collected during this AIVR session.</br> Keys are the `name` values provided in questions.   # noqa: E501

        :return: The vars of this CoreAIVRSession.  # noqa: E501
        :rtype: object
        """
        return self._vars

    @vars.setter
    def vars(self, vars):
        """Sets the vars of this CoreAIVRSession.

        Map with user reponses collected during this AIVR session.</br> Keys are the `name` values provided in questions.   # noqa: E501

        :param vars: The vars of this CoreAIVRSession.  # noqa: E501
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
        if not isinstance(other, CoreAIVRSession):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CoreAIVRSession):
            return True

        return self.to_dict() != other.to_dict()