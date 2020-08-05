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

from voicegain_speech.configuration import Configuration


class GregExperimentBaseInclusive(object):
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
        'audio_set': 'GregAudioSetInner',
        'date': 'str',
        'grammar': 'GregGrammarInner',
        'name': 'str',
        'platform': 'str',
        'question': 'GregQuestionInner',
        'status': 'GregExperimentStatus'
    }

    attribute_map = {
        'audio_set': 'audioSet',
        'date': 'date',
        'grammar': 'grammar',
        'name': 'name',
        'platform': 'platform',
        'question': 'question',
        'status': 'status'
    }

    def __init__(self, audio_set=None, date=None, grammar=None, name=None, platform=None, question=None, status=None, local_vars_configuration=None):  # noqa: E501
        """GregExperimentBaseInclusive - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._audio_set = None
        self._date = None
        self._grammar = None
        self._name = None
        self._platform = None
        self._question = None
        self._status = None
        self.discriminator = None

        if audio_set is not None:
            self.audio_set = audio_set
        if date is not None:
            self.date = date
        if grammar is not None:
            self.grammar = grammar
        if name is not None:
            self.name = name
        if platform is not None:
            self.platform = platform
        if question is not None:
            self.question = question
        if status is not None:
            self.status = status

    @property
    def audio_set(self):
        """Gets the audio_set of this GregExperimentBaseInclusive.  # noqa: E501


        :return: The audio_set of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: GregAudioSetInner
        """
        return self._audio_set

    @audio_set.setter
    def audio_set(self, audio_set):
        """Sets the audio_set of this GregExperimentBaseInclusive.


        :param audio_set: The audio_set of this GregExperimentBaseInclusive.  # noqa: E501
        :type: GregAudioSetInner
        """

        self._audio_set = audio_set

    @property
    def date(self):
        """Gets the date of this GregExperimentBaseInclusive.  # noqa: E501

        Start date/time of the experiment  # noqa: E501

        :return: The date of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: str
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this GregExperimentBaseInclusive.

        Start date/time of the experiment  # noqa: E501

        :param date: The date of this GregExperimentBaseInclusive.  # noqa: E501
        :type: str
        """

        self._date = date

    @property
    def grammar(self):
        """Gets the grammar of this GregExperimentBaseInclusive.  # noqa: E501


        :return: The grammar of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: GregGrammarInner
        """
        return self._grammar

    @grammar.setter
    def grammar(self, grammar):
        """Sets the grammar of this GregExperimentBaseInclusive.


        :param grammar: The grammar of this GregExperimentBaseInclusive.  # noqa: E501
        :type: GregGrammarInner
        """

        self._grammar = grammar

    @property
    def name(self):
        """Gets the name of this GregExperimentBaseInclusive.  # noqa: E501

        Unique experiment Name  # noqa: E501

        :return: The name of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this GregExperimentBaseInclusive.

        Unique experiment Name  # noqa: E501

        :param name: The name of this GregExperimentBaseInclusive.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def platform(self):
        """Gets the platform of this GregExperimentBaseInclusive.  # noqa: E501

        Identifier of the platform used in the experiment, e.g. \"Nuance 10\"  (for uploaded experiment data), or \"VoiceGain.17\"</br> **(will soon become enum)**   # noqa: E501

        :return: The platform of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this GregExperimentBaseInclusive.

        Identifier of the platform used in the experiment, e.g. \"Nuance 10\"  (for uploaded experiment data), or \"VoiceGain.17\"</br> **(will soon become enum)**   # noqa: E501

        :param platform: The platform of this GregExperimentBaseInclusive.  # noqa: E501
        :type: str
        """

        self._platform = platform

    @property
    def question(self):
        """Gets the question of this GregExperimentBaseInclusive.  # noqa: E501


        :return: The question of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: GregQuestionInner
        """
        return self._question

    @question.setter
    def question(self, question):
        """Sets the question of this GregExperimentBaseInclusive.


        :param question: The question of this GregExperimentBaseInclusive.  # noqa: E501
        :type: GregQuestionInner
        """

        self._question = question

    @property
    def status(self):
        """Gets the status of this GregExperimentBaseInclusive.  # noqa: E501


        :return: The status of this GregExperimentBaseInclusive.  # noqa: E501
        :rtype: GregExperimentStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this GregExperimentBaseInclusive.


        :param status: The status of this GregExperimentBaseInclusive.  # noqa: E501
        :type: GregExperimentStatus
        """

        self._status = status

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
        if not isinstance(other, GregExperimentBaseInclusive):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GregExperimentBaseInclusive):
            return True

        return self.to_dict() != other.to_dict()
