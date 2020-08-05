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


class AsrSettingsTranscription(object):
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
        'acoustic_model_non_real_time': 'str',
        'acoustic_model_real_time': 'str',
        'confidence_threshold': 'float',
        'max_alternatives': 'int',
        'sensitivity': 'float',
        'speed_vs_accuracy': 'float',
        'hints': 'list[str]',
        'lang_model': 'str',
        'no_input_timeout': 'int',
        'speech_analytics_config': 'str',
        'topic_discovery_config': 'str'
    }

    attribute_map = {
        'acoustic_model_non_real_time': 'acousticModelNonRealTime',
        'acoustic_model_real_time': 'acousticModelRealTime',
        'confidence_threshold': 'confidenceThreshold',
        'max_alternatives': 'maxAlternatives',
        'sensitivity': 'sensitivity',
        'speed_vs_accuracy': 'speedVsAccuracy',
        'hints': 'hints',
        'lang_model': 'langModel',
        'no_input_timeout': 'noInputTimeout',
        'speech_analytics_config': 'speechAnalyticsConfig',
        'topic_discovery_config': 'topicDiscoveryConfig'
    }

    def __init__(self, acoustic_model_non_real_time=None, acoustic_model_real_time=None, confidence_threshold=0.01, max_alternatives=1, sensitivity=None, speed_vs_accuracy=None, hints=None, lang_model=None, no_input_timeout=15000, speech_analytics_config=None, topic_discovery_config=None, local_vars_configuration=None):  # noqa: E501
        """AsrSettingsTranscription - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._acoustic_model_non_real_time = None
        self._acoustic_model_real_time = None
        self._confidence_threshold = None
        self._max_alternatives = None
        self._sensitivity = None
        self._speed_vs_accuracy = None
        self._hints = None
        self._lang_model = None
        self._no_input_timeout = None
        self._speech_analytics_config = None
        self._topic_discovery_config = None
        self.discriminator = None

        if acoustic_model_non_real_time is not None:
            self.acoustic_model_non_real_time = acoustic_model_non_real_time
        if acoustic_model_real_time is not None:
            self.acoustic_model_real_time = acoustic_model_real_time
        if confidence_threshold is not None:
            self.confidence_threshold = confidence_threshold
        if max_alternatives is not None:
            self.max_alternatives = max_alternatives
        if sensitivity is not None:
            self.sensitivity = sensitivity
        if speed_vs_accuracy is not None:
            self.speed_vs_accuracy = speed_vs_accuracy
        if hints is not None:
            self.hints = hints
        if lang_model is not None:
            self.lang_model = lang_model
        if no_input_timeout is not None:
            self.no_input_timeout = no_input_timeout
        if speech_analytics_config is not None:
            self.speech_analytics_config = speech_analytics_config
        if topic_discovery_config is not None:
            self.topic_discovery_config = topic_discovery_config

    @property
    def acoustic_model_non_real_time(self):
        """Gets the acoustic_model_non_real_time of this AsrSettingsTranscription.  # noqa: E501

        (Optional) Name of an Acoustic Model that is to be used for offline and semi-real-time processing.  May include version number separated by `:` , for example, **Voicegain-BD_en-us:11** </br> If not provided a suitable default will be used.   # noqa: E501

        :return: The acoustic_model_non_real_time of this AsrSettingsTranscription.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_non_real_time

    @acoustic_model_non_real_time.setter
    def acoustic_model_non_real_time(self, acoustic_model_non_real_time):
        """Sets the acoustic_model_non_real_time of this AsrSettingsTranscription.

        (Optional) Name of an Acoustic Model that is to be used for offline and semi-real-time processing.  May include version number separated by `:` , for example, **Voicegain-BD_en-us:11** </br> If not provided a suitable default will be used.   # noqa: E501

        :param acoustic_model_non_real_time: The acoustic_model_non_real_time of this AsrSettingsTranscription.  # noqa: E501
        :type: str
        """

        self._acoustic_model_non_real_time = acoustic_model_non_real_time

    @property
    def acoustic_model_real_time(self):
        """Gets the acoustic_model_real_time of this AsrSettingsTranscription.  # noqa: E501

        (Optional) Name of a real-time capable Acoustic Model.  May include version number separated by `:`, for example, **Voicegain-IVR_en-us:3**</br> If not provided a suitable default will be used.   # noqa: E501

        :return: The acoustic_model_real_time of this AsrSettingsTranscription.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_real_time

    @acoustic_model_real_time.setter
    def acoustic_model_real_time(self, acoustic_model_real_time):
        """Sets the acoustic_model_real_time of this AsrSettingsTranscription.

        (Optional) Name of a real-time capable Acoustic Model.  May include version number separated by `:`, for example, **Voicegain-IVR_en-us:3**</br> If not provided a suitable default will be used.   # noqa: E501

        :param acoustic_model_real_time: The acoustic_model_real_time of this AsrSettingsTranscription.  # noqa: E501
        :type: str
        """

        self._acoustic_model_real_time = acoustic_model_real_time

    @property
    def confidence_threshold(self):
        """Gets the confidence_threshold of this AsrSettingsTranscription.  # noqa: E501

        Hypotheses below this threshold will result in NOMATCH  # noqa: E501

        :return: The confidence_threshold of this AsrSettingsTranscription.  # noqa: E501
        :rtype: float
        """
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, confidence_threshold):
        """Sets the confidence_threshold of this AsrSettingsTranscription.

        Hypotheses below this threshold will result in NOMATCH  # noqa: E501

        :param confidence_threshold: The confidence_threshold of this AsrSettingsTranscription.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                confidence_threshold is not None and confidence_threshold > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `confidence_threshold`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                confidence_threshold is not None and confidence_threshold < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `confidence_threshold`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._confidence_threshold = confidence_threshold

    @property
    def max_alternatives(self):
        """Gets the max_alternatives of this AsrSettingsTranscription.  # noqa: E501

        number of recognition hypotheses to return as result (top N-Best)  # noqa: E501

        :return: The max_alternatives of this AsrSettingsTranscription.  # noqa: E501
        :rtype: int
        """
        return self._max_alternatives

    @max_alternatives.setter
    def max_alternatives(self, max_alternatives):
        """Sets the max_alternatives of this AsrSettingsTranscription.

        number of recognition hypotheses to return as result (top N-Best)  # noqa: E501

        :param max_alternatives: The max_alternatives of this AsrSettingsTranscription.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                max_alternatives is not None and max_alternatives > 100):  # noqa: E501
            raise ValueError("Invalid value for `max_alternatives`, must be a value less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                max_alternatives is not None and max_alternatives < 1):  # noqa: E501
            raise ValueError("Invalid value for `max_alternatives`, must be a value greater than or equal to `1`")  # noqa: E501

        self._max_alternatives = max_alternatives

    @property
    def sensitivity(self):
        """Gets the sensitivity of this AsrSettingsTranscription.  # noqa: E501

        affects separation of speech from background noise level  # noqa: E501

        :return: The sensitivity of this AsrSettingsTranscription.  # noqa: E501
        :rtype: float
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, sensitivity):
        """Sets the sensitivity of this AsrSettingsTranscription.

        affects separation of speech from background noise level  # noqa: E501

        :param sensitivity: The sensitivity of this AsrSettingsTranscription.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                sensitivity is not None and sensitivity > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `sensitivity`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                sensitivity is not None and sensitivity < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `sensitivity`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._sensitivity = sensitivity

    @property
    def speed_vs_accuracy(self):
        """Gets the speed_vs_accuracy of this AsrSettingsTranscription.  # noqa: E501

        between 0.0 and 1.0 - tradeoff between accuracy and speed/resource use  # noqa: E501

        :return: The speed_vs_accuracy of this AsrSettingsTranscription.  # noqa: E501
        :rtype: float
        """
        return self._speed_vs_accuracy

    @speed_vs_accuracy.setter
    def speed_vs_accuracy(self, speed_vs_accuracy):
        """Sets the speed_vs_accuracy of this AsrSettingsTranscription.

        between 0.0 and 1.0 - tradeoff between accuracy and speed/resource use  # noqa: E501

        :param speed_vs_accuracy: The speed_vs_accuracy of this AsrSettingsTranscription.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                speed_vs_accuracy is not None and speed_vs_accuracy > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `speed_vs_accuracy`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                speed_vs_accuracy is not None and speed_vs_accuracy < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `speed_vs_accuracy`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._speed_vs_accuracy = speed_vs_accuracy

    @property
    def hints(self):
        """Gets the hints of this AsrSettingsTranscription.  # noqa: E501

        Can be provided to indicate that given words/phrases are more likely to appear in the audio input. No special characters allowed except for '_'   # noqa: E501

        :return: The hints of this AsrSettingsTranscription.  # noqa: E501
        :rtype: list[str]
        """
        return self._hints

    @hints.setter
    def hints(self, hints):
        """Sets the hints of this AsrSettingsTranscription.

        Can be provided to indicate that given words/phrases are more likely to appear in the audio input. No special characters allowed except for '_'   # noqa: E501

        :param hints: The hints of this AsrSettingsTranscription.  # noqa: E501
        :type: list[str]
        """

        self._hints = hints

    @property
    def lang_model(self):
        """Gets the lang_model of this AsrSettingsTranscription.  # noqa: E501

        Name or UUID of the language model (arpa grammar) to use. If absent then will use default language model.  # noqa: E501

        :return: The lang_model of this AsrSettingsTranscription.  # noqa: E501
        :rtype: str
        """
        return self._lang_model

    @lang_model.setter
    def lang_model(self, lang_model):
        """Sets the lang_model of this AsrSettingsTranscription.

        Name or UUID of the language model (arpa grammar) to use. If absent then will use default language model.  # noqa: E501

        :param lang_model: The lang_model of this AsrSettingsTranscription.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                lang_model is not None and len(lang_model) > 128):
            raise ValueError("Invalid value for `lang_model`, length must be less than or equal to `128`")  # noqa: E501

        self._lang_model = lang_model

    @property
    def no_input_timeout(self):
        """Gets the no_input_timeout of this AsrSettingsTranscription.  # noqa: E501

        Time in milliseconds to wait for speech in audio to start. Any value <= 0 means that the timeout will be ignored.  # noqa: E501

        :return: The no_input_timeout of this AsrSettingsTranscription.  # noqa: E501
        :rtype: int
        """
        return self._no_input_timeout

    @no_input_timeout.setter
    def no_input_timeout(self, no_input_timeout):
        """Sets the no_input_timeout of this AsrSettingsTranscription.

        Time in milliseconds to wait for speech in audio to start. Any value <= 0 means that the timeout will be ignored.  # noqa: E501

        :param no_input_timeout: The no_input_timeout of this AsrSettingsTranscription.  # noqa: E501
        :type: int
        """

        self._no_input_timeout = no_input_timeout

    @property
    def speech_analytics_config(self):
        """Gets the speech_analytics_config of this AsrSettingsTranscription.  # noqa: E501

        Name or UUID of the Speech Analytics configuration to use. If absent then will not perform Speech Analytics.  # noqa: E501

        :return: The speech_analytics_config of this AsrSettingsTranscription.  # noqa: E501
        :rtype: str
        """
        return self._speech_analytics_config

    @speech_analytics_config.setter
    def speech_analytics_config(self, speech_analytics_config):
        """Sets the speech_analytics_config of this AsrSettingsTranscription.

        Name or UUID of the Speech Analytics configuration to use. If absent then will not perform Speech Analytics.  # noqa: E501

        :param speech_analytics_config: The speech_analytics_config of this AsrSettingsTranscription.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                speech_analytics_config is not None and len(speech_analytics_config) > 128):
            raise ValueError("Invalid value for `speech_analytics_config`, length must be less than or equal to `128`")  # noqa: E501

        self._speech_analytics_config = speech_analytics_config

    @property
    def topic_discovery_config(self):
        """Gets the topic_discovery_config of this AsrSettingsTranscription.  # noqa: E501

        Name or UUID of the Topic discovery configuration to use. If absent then will not perform Topic Discovery.  # noqa: E501

        :return: The topic_discovery_config of this AsrSettingsTranscription.  # noqa: E501
        :rtype: str
        """
        return self._topic_discovery_config

    @topic_discovery_config.setter
    def topic_discovery_config(self, topic_discovery_config):
        """Sets the topic_discovery_config of this AsrSettingsTranscription.

        Name or UUID of the Topic discovery configuration to use. If absent then will not perform Topic Discovery.  # noqa: E501

        :param topic_discovery_config: The topic_discovery_config of this AsrSettingsTranscription.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                topic_discovery_config is not None and len(topic_discovery_config) > 128):
            raise ValueError("Invalid value for `topic_discovery_config`, length must be less than or equal to `128`")  # noqa: E501

        self._topic_discovery_config = topic_discovery_config

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
        if not isinstance(other, AsrSettingsTranscription):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsrSettingsTranscription):
            return True

        return self.to_dict() != other.to_dict()