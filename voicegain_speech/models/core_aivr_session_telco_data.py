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


class CoreAIVRSessionTelcoData(object):
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
        'fs_conference_ext': 'str',
        'fs_conference_ext_screen': 'str',
        'fs_conference_ext_video': 'str',
        'fs_conference_name': 'str',
        'fs_uuid': 'str',
        'participants': 'dict(str, AIVRSessionUser)'
    }

    attribute_map = {
        'ani': 'ani',
        'dnis': 'dnis',
        'fs_conference_ext': 'fsConferenceExt',
        'fs_conference_ext_screen': 'fsConferenceExtScreen',
        'fs_conference_ext_video': 'fsConferenceExtVideo',
        'fs_conference_name': 'fsConferenceName',
        'fs_uuid': 'fsUUID',
        'participants': 'participants'
    }

    def __init__(self, ani=None, dnis=None, fs_conference_ext=None, fs_conference_ext_screen=None, fs_conference_ext_video=None, fs_conference_name=None, fs_uuid=None, participants=None, local_vars_configuration=None):  # noqa: E501
        """CoreAIVRSessionTelcoData - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._ani = None
        self._dnis = None
        self._fs_conference_ext = None
        self._fs_conference_ext_screen = None
        self._fs_conference_ext_video = None
        self._fs_conference_name = None
        self._fs_uuid = None
        self._participants = None
        self.discriminator = None

        if ani is not None:
            self.ani = ani
        if dnis is not None:
            self.dnis = dnis
        if fs_conference_ext is not None:
            self.fs_conference_ext = fs_conference_ext
        if fs_conference_ext_screen is not None:
            self.fs_conference_ext_screen = fs_conference_ext_screen
        if fs_conference_ext_video is not None:
            self.fs_conference_ext_video = fs_conference_ext_video
        if fs_conference_name is not None:
            self.fs_conference_name = fs_conference_name
        if fs_uuid is not None:
            self.fs_uuid = fs_uuid
        if participants is not None:
            self.participants = participants

    @property
    def ani(self):
        """Gets the ani of this CoreAIVRSessionTelcoData.  # noqa: E501

        Caller phone number or sip address. Unavailable for Verto session.   # noqa: E501

        :return: The ani of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._ani

    @ani.setter
    def ani(self, ani):
        """Sets the ani of this CoreAIVRSessionTelcoData.

        Caller phone number or sip address. Unavailable for Verto session.   # noqa: E501

        :param ani: The ani of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._ani = ani

    @property
    def dnis(self):
        """Gets the dnis of this CoreAIVRSessionTelcoData.  # noqa: E501

        Called phone number or sip address.</br>  We are no using this for Verto. Verto calls dial into `fsConferenceExt` and `fsConferenceExtScreen`.   # noqa: E501

        :return: The dnis of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._dnis

    @dnis.setter
    def dnis(self, dnis):
        """Sets the dnis of this CoreAIVRSessionTelcoData.

        Called phone number or sip address.</br>  We are no using this for Verto. Verto calls dial into `fsConferenceExt` and `fsConferenceExtScreen`.   # noqa: E501

        :param dnis: The dnis of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._dnis = dnis

    @property
    def fs_conference_ext(self):
        """Gets the fs_conference_ext of this CoreAIVRSessionTelcoData.  # noqa: E501

        Random string used as the Audio Conference Extension. Main extenstion to be used to dial into the conference for audio.</br> Generated when AIVR Session is created.   # noqa: E501

        :return: The fs_conference_ext of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._fs_conference_ext

    @fs_conference_ext.setter
    def fs_conference_ext(self, fs_conference_ext):
        """Sets the fs_conference_ext of this CoreAIVRSessionTelcoData.

        Random string used as the Audio Conference Extension. Main extenstion to be used to dial into the conference for audio.</br> Generated when AIVR Session is created.   # noqa: E501

        :param fs_conference_ext: The fs_conference_ext of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._fs_conference_ext = fs_conference_ext

    @property
    def fs_conference_ext_screen(self):
        """Gets the fs_conference_ext_screen of this CoreAIVRSessionTelcoData.  # noqa: E501

        Random string used as a Conference Extension for ScreenShare. Use it to dial into the conference for screen sharing.  Screen share conference is separate from the main conference - has own canvas and layouts. All users wanting to either share the screen or to view the shared screen need to dial into this conference. There is no audio on this conference.</br> Generated when AIVR Session is created.   # noqa: E501

        :return: The fs_conference_ext_screen of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._fs_conference_ext_screen

    @fs_conference_ext_screen.setter
    def fs_conference_ext_screen(self, fs_conference_ext_screen):
        """Sets the fs_conference_ext_screen of this CoreAIVRSessionTelcoData.

        Random string used as a Conference Extension for ScreenShare. Use it to dial into the conference for screen sharing.  Screen share conference is separate from the main conference - has own canvas and layouts. All users wanting to either share the screen or to view the shared screen need to dial into this conference. There is no audio on this conference.</br> Generated when AIVR Session is created.   # noqa: E501

        :param fs_conference_ext_screen: The fs_conference_ext_screen of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._fs_conference_ext_screen = fs_conference_ext_screen

    @property
    def fs_conference_ext_video(self):
        """Gets the fs_conference_ext_video of this CoreAIVRSessionTelcoData.  # noqa: E501

        Random string used as a prefix for the name of Conference Extension for Video Feed.</br> Each user will submit his own video feed to a conference with name being concatenation of `fsConferenceExtVideo` and the participant's `videoConfIndex`. All other paricipants will not submit any video to this user's conference but will be getting the video feed from it.  There is no audio on this conference.</br> Generated when AIVR Session is created.   # noqa: E501

        :return: The fs_conference_ext_video of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._fs_conference_ext_video

    @fs_conference_ext_video.setter
    def fs_conference_ext_video(self, fs_conference_ext_video):
        """Sets the fs_conference_ext_video of this CoreAIVRSessionTelcoData.

        Random string used as a prefix for the name of Conference Extension for Video Feed.</br> Each user will submit his own video feed to a conference with name being concatenation of `fsConferenceExtVideo` and the participant's `videoConfIndex`. All other paricipants will not submit any video to this user's conference but will be getting the video feed from it.  There is no audio on this conference.</br> Generated when AIVR Session is created.   # noqa: E501

        :param fs_conference_ext_video: The fs_conference_ext_video of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._fs_conference_ext_video = fs_conference_ext_video

    @property
    def fs_conference_name(self):
        """Gets the fs_conference_name of this CoreAIVRSessionTelcoData.  # noqa: E501

        Random string used as a name of the Freeswitch conference. </br> Generated when AIVR Session is created.   # noqa: E501

        :return: The fs_conference_name of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._fs_conference_name

    @fs_conference_name.setter
    def fs_conference_name(self, fs_conference_name):
        """Sets the fs_conference_name of this CoreAIVRSessionTelcoData.

        Random string used as a name of the Freeswitch conference. </br> Generated when AIVR Session is created.   # noqa: E501

        :param fs_conference_name: The fs_conference_name of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._fs_conference_name = fs_conference_name

    @property
    def fs_uuid(self):
        """Gets the fs_uuid of this CoreAIVRSessionTelcoData.  # noqa: E501

        Freeswitch session/channel UUID -- TODO -- how will it work now that we have a conference ??  # noqa: E501

        :return: The fs_uuid of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: str
        """
        return self._fs_uuid

    @fs_uuid.setter
    def fs_uuid(self, fs_uuid):
        """Sets the fs_uuid of this CoreAIVRSessionTelcoData.

        Freeswitch session/channel UUID -- TODO -- how will it work now that we have a conference ??  # noqa: E501

        :param fs_uuid: The fs_uuid of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: str
        """

        self._fs_uuid = fs_uuid

    @property
    def participants(self):
        """Gets the participants of this CoreAIVRSessionTelcoData.  # noqa: E501

        Map from participant name to AIVRSessionUser object, see example.  # noqa: E501

        :return: The participants of this CoreAIVRSessionTelcoData.  # noqa: E501
        :rtype: dict(str, AIVRSessionUser)
        """
        return self._participants

    @participants.setter
    def participants(self, participants):
        """Sets the participants of this CoreAIVRSessionTelcoData.

        Map from participant name to AIVRSessionUser object, see example.  # noqa: E501

        :param participants: The participants of this CoreAIVRSessionTelcoData.  # noqa: E501
        :type: dict(str, AIVRSessionUser)
        """

        self._participants = participants

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
        if not isinstance(other, CoreAIVRSessionTelcoData):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CoreAIVRSessionTelcoData):
            return True

        return self.to_dict() != other.to_dict()