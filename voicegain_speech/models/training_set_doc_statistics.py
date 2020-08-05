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


class TrainingSetDocStatistics(object):
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
        'coverage': 'float',
        'processed_audio_count': 'int',
        'processed_audio_total_seconds': 'int',
        'raw_audio_count': 'int',
        'raw_audio_total_seconds': 'int'
    }

    attribute_map = {
        'coverage': 'coverage',
        'processed_audio_count': 'processedAudioCount',
        'processed_audio_total_seconds': 'processedAudioTotalSeconds',
        'raw_audio_count': 'rawAudioCount',
        'raw_audio_total_seconds': 'rawAudioTotalSeconds'
    }

    def __init__(self, coverage=None, processed_audio_count=None, processed_audio_total_seconds=None, raw_audio_count=None, raw_audio_total_seconds=None, local_vars_configuration=None):  # noqa: E501
        """TrainingSetDocStatistics - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._coverage = None
        self._processed_audio_count = None
        self._processed_audio_total_seconds = None
        self._raw_audio_count = None
        self._raw_audio_total_seconds = None
        self.discriminator = None

        if coverage is not None:
            self.coverage = coverage
        if processed_audio_count is not None:
            self.processed_audio_count = processed_audio_count
        if processed_audio_total_seconds is not None:
            self.processed_audio_total_seconds = processed_audio_total_seconds
        if raw_audio_count is not None:
            self.raw_audio_count = raw_audio_count
        if raw_audio_total_seconds is not None:
            self.raw_audio_total_seconds = raw_audio_total_seconds

    @property
    def coverage(self):
        """Gets the coverage of this TrainingSetDocStatistics.  # noqa: E501

        shows what fraction of the raw data set has been found suitable for training  # noqa: E501

        :return: The coverage of this TrainingSetDocStatistics.  # noqa: E501
        :rtype: float
        """
        return self._coverage

    @coverage.setter
    def coverage(self, coverage):
        """Sets the coverage of this TrainingSetDocStatistics.

        shows what fraction of the raw data set has been found suitable for training  # noqa: E501

        :param coverage: The coverage of this TrainingSetDocStatistics.  # noqa: E501
        :type: float
        """
        if (self.local_vars_configuration.client_side_validation and
                coverage is not None and coverage > 1.0):  # noqa: E501
            raise ValueError("Invalid value for `coverage`, must be a value less than or equal to `1.0`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                coverage is not None and coverage < 0.0):  # noqa: E501
            raise ValueError("Invalid value for `coverage`, must be a value greater than or equal to `0.0`")  # noqa: E501

        self._coverage = coverage

    @property
    def processed_audio_count(self):
        """Gets the processed_audio_count of this TrainingSetDocStatistics.  # noqa: E501

        number of processed audio files (input for training)  # noqa: E501

        :return: The processed_audio_count of this TrainingSetDocStatistics.  # noqa: E501
        :rtype: int
        """
        return self._processed_audio_count

    @processed_audio_count.setter
    def processed_audio_count(self, processed_audio_count):
        """Sets the processed_audio_count of this TrainingSetDocStatistics.

        number of processed audio files (input for training)  # noqa: E501

        :param processed_audio_count: The processed_audio_count of this TrainingSetDocStatistics.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                processed_audio_count is not None and processed_audio_count < 0):  # noqa: E501
            raise ValueError("Invalid value for `processed_audio_count`, must be a value greater than or equal to `0`")  # noqa: E501

        self._processed_audio_count = processed_audio_count

    @property
    def processed_audio_total_seconds(self):
        """Gets the processed_audio_total_seconds of this TrainingSetDocStatistics.  # noqa: E501

        total duration of processed audio files in seconds (input for training)  # noqa: E501

        :return: The processed_audio_total_seconds of this TrainingSetDocStatistics.  # noqa: E501
        :rtype: int
        """
        return self._processed_audio_total_seconds

    @processed_audio_total_seconds.setter
    def processed_audio_total_seconds(self, processed_audio_total_seconds):
        """Sets the processed_audio_total_seconds of this TrainingSetDocStatistics.

        total duration of processed audio files in seconds (input for training)  # noqa: E501

        :param processed_audio_total_seconds: The processed_audio_total_seconds of this TrainingSetDocStatistics.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                processed_audio_total_seconds is not None and processed_audio_total_seconds < 0):  # noqa: E501
            raise ValueError("Invalid value for `processed_audio_total_seconds`, must be a value greater than or equal to `0`")  # noqa: E501

        self._processed_audio_total_seconds = processed_audio_total_seconds

    @property
    def raw_audio_count(self):
        """Gets the raw_audio_count of this TrainingSetDocStatistics.  # noqa: E501

        number of raw audio files  # noqa: E501

        :return: The raw_audio_count of this TrainingSetDocStatistics.  # noqa: E501
        :rtype: int
        """
        return self._raw_audio_count

    @raw_audio_count.setter
    def raw_audio_count(self, raw_audio_count):
        """Sets the raw_audio_count of this TrainingSetDocStatistics.

        number of raw audio files  # noqa: E501

        :param raw_audio_count: The raw_audio_count of this TrainingSetDocStatistics.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                raw_audio_count is not None and raw_audio_count < 0):  # noqa: E501
            raise ValueError("Invalid value for `raw_audio_count`, must be a value greater than or equal to `0`")  # noqa: E501

        self._raw_audio_count = raw_audio_count

    @property
    def raw_audio_total_seconds(self):
        """Gets the raw_audio_total_seconds of this TrainingSetDocStatistics.  # noqa: E501

        total duration of all raw audio files in seconds  # noqa: E501

        :return: The raw_audio_total_seconds of this TrainingSetDocStatistics.  # noqa: E501
        :rtype: int
        """
        return self._raw_audio_total_seconds

    @raw_audio_total_seconds.setter
    def raw_audio_total_seconds(self, raw_audio_total_seconds):
        """Sets the raw_audio_total_seconds of this TrainingSetDocStatistics.

        total duration of all raw audio files in seconds  # noqa: E501

        :param raw_audio_total_seconds: The raw_audio_total_seconds of this TrainingSetDocStatistics.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                raw_audio_total_seconds is not None and raw_audio_total_seconds < 0):  # noqa: E501
            raise ValueError("Invalid value for `raw_audio_total_seconds`, must be a value greater than or equal to `0`")  # noqa: E501

        self._raw_audio_total_seconds = raw_audio_total_seconds

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
        if not isinstance(other, TrainingSetDocStatistics):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TrainingSetDocStatistics):
            return True

        return self.to_dict() != other.to_dict()
