# coding: utf-8

"""
    Voicegain Speech-to-Text API v1

    # New  [RTC Callback API](#tag/aivr-callback) for building interactive speech-enabled phone applications  (IVR, Voicebots, etc.).    # Intro to Voicegain APIs The APIs are provided by [Voicegain](https://www.voicegain.ai) to its registered customers. </br> The core APIs are for Speech-to-Text (STT), either transcription or recognition (further described in next Sections).</br> Other available APIs include: + RTC Callback APIs which in addition to speech-to-text allow for control of RTC session (e.g., a telephone call). + Websocket APIs for managing broadcast websockets used in real-time transcription. + Language Model creation and manipulation APIs. + Data upload APIs that help in certain STT use scenarios. + Training Set APIs - for use in preparing data for acoustic model training. + GREG APIs - for working with ASR and Grammar tuning tool - GREG. + Security APIs.   Python SDK for this API is available at [PyPI Repository](https://pypi.org/project/voicegain-speech/)  In addition to this API Spec document please also consult our Knowledge Base Articles: * [Web API Section](https://support.voicegain.ai/hc/en-us/categories/360001288691-Web-API) of our Knowledge Base   * [Authentication for Web API](https://support.voicegain.ai/hc/en-us/sections/360004485831-Authentication-for-Web-API) - how to generate and use JWT   * [Basic Web API Use Cases](https://support.voicegain.ai/hc/en-us/sections/360004660632-Basic-Web-API-Use-Cases)   * [Example applications using Voicegain API](https://support.voicegain.ai/hc/en-us/sections/360009682932-Example-applications-using-Voicegain-API)  **NOTE:** Most of the request and response examples in this API document are generated from schema example annotation. This may result in the response example not matching the request data example.</br> We will be adding specific examples to certain API methods if we notice that this is needed to clarify the usage.  # Transcribe API  **/asr/transcribe**</br> The Transcribe API allows you to submit audio and receive the transcribed text word-for-word from the STT engine.  This API uses our Large Vocabulary language model and supports long form audio in async mode. </br> The API can, e.g., be used to transcribe audio data - whether it is podcasts, voicemails, call recordings, etc.  In real-time streaming mode it can, e.g., be used for building voice-bots (your the application will have to provide NLU capabilities to determine intent from the transcribed text).    The result of transcription can be returned in four formats. These are requested inside session[].content when making initial transcribe request:  + **Transcript** - Contains the complete text of transcription + **Words** - Intermediate results will contain new words, with timing and confidences, since the previous intermediate result. The final result will contain complete transcription. + **Word-Tree** - Contains a tree of all feasible alternatives. Use this when integrating with NL postprocessing to determine the final utterance and its meaning. + **Captions** - Intermediate results will be suitable to use as captions (this feature is in beta).  # Recognize API  **/asr/recognize**</br> This API should be used if you want to constrain STT recognition results to the speech-grammar that is submitted along with the audio  (grammars are used in place of large vocabulary language model).</br> While building grammars can be time-consuming step, they can simplify the development of applications since the semantic  meaning can be extracted along with the text. </br> Voicegain supports grammars in the JSGF and GRXML formats – both grammar standards used by enterprises in IVRs since early 2000s.</br> The recognize API only supports short form audio - no more than 30 seconds.   # Sync/Async Mode  Speech-to-Text APIs can be accessed in two modes:  + **Sync mode:**  This is the default mode that is invoked when a client makes a request for the Transcribe (/asr/transcribe) and Recognize (/asr/recognize) urls.</br> A Speech-to-Text API synchronous request is the simplest method for performing processing on speech audio data.  Speech-to-Text can process up to 1 minute of speech audio data sent in a synchronous request.  After Speech-to-Text processes all of the audio, it returns a response.</br> A synchronous request is blocking, meaning that Speech-to-Text must return a response before processing the next request.  Speech-to-Text typically processes audio faster than realtime.</br> For longer audio please use Async mode.    + **Async Mode:**  This is invoked by adding the /async to the Transcribe and Recognize url (so /asr/transcribe/async and /asr/recognize/async respectively). </br> In this mode the initial HTTP request request will return as soon as the STT session is established.  The response will contain a session id which can be used to obtain either incremental or full result of speech-to-text processing.  In this mode, the Voicegain platform can provide multiple intermediate recognition/transcription responses to the client as they become available before sending a final response.  ## Async Sessions: Real-Time, Semi Real-Time, and Off-Line  There are 3 types of Async ASR session that can be started:  + **REAL-TIME** - Real-time processing of streaming audio. For the recognition API, results are available within less than one second.  For the transcription API, real-time incremental results will be sent back with about 2 seconds delay.  + **OFF-LINE** - offline transcription or recognition. Has higher accuracy than REAL-TIME. Results are delivered once the complete audio has been processed.  Currently, 1 hour long audio is processed in about 10 minutes. + **SEMI-REAL-TIME** - Similar in use to REAL-TIME, but the results are available with a delay of about 30 seconds (or earlier for shorter audio). Same accuracy as OFF-LINE.  It is possible to start up to 2 simultaneous sessions attached to the same audio.   The allowed combinations of the types of two sessions are:  + REAL-TIME + SEMI-REAL-TIME - one possible use case is a combination of live transcription with transcription for online streaming (which may be delayed w.r.t of real time). The benefit of using separate SEMI-REAL-TIME session is that it has higher accuracy. + REAL-TIME + OFF-LINE - one possible use case is combination of live transcription with higher quality off-line transcription for archival purposes.  Other combinations of session types, including more than 2 sessions, are currently not supported.  Please, let us know if you think you have a valid use case for other combinations.  # RTC Callback API   Voicegain Real Time Communication (RTC) Callback APIs work on audio data that is part of an RTC session (a telephone call for example).   # Audio Input  The speech audio can be submitted in variety of ways:  + **Inline** - Short audio data can be encoded inside a request as a base64 string. + **Retrieved from URL** - Audio can be retrieved from a provided URL. The URL can also point to a live stream. + **Streamed via RTP** - Recommended only for Edge use cases (not for Cloud). + **Streamed via proprietary UDP protocol** - We provide a Java utility to do this. The utility can stream directly from an audio device, or from a file. + **Streamed via Websocket** - Can be used, e.g., to do microphone capture directly from the web browser. + **From Object Store** - Currently it works only with files uploaded to Voicegain object store, but will be expanded to support other Object Stores.  # Pagination  For methods that support pagination Voicegain has standardized on using the following query parameters: + page={page number} + per_page={number items per page}  In responses, Voicegain APIs use the [Link Header standard](https://tools.ietf.org/html/rfc5988) to provide the pagination information. The following values of the `rel` field are used: self, first, prev, next, last.  In addition to the `Link` header, the `X-Total-Count` header is used to provide the total count of items matching a query.  An example response header might look like (note: we have broken the Link header in multiple lines for readability )  ``` X-Total-Count: 255 Link: <https://api.voicegain.ai/v1/sa/call?page=1&per_page=50>; rel=\"first\",       <https://api.voicegain.ai/v1/sa/call?page=2&per_page=50>; rel=\"prev\",       <https://api.voicegain.ai/v1/sa/call?page=3&per_page=50>; rel=\"self\",       <https://api.voicegain.ai/v1/sa/call?page=4&per_page=50>; rel=\"next\",       <https://api.voicegain.ai/v1/sa/call?page=6&per_page=50>; rel=\"last\" ```  # JWT Authentication Almost all methods from this API require authentication by means of a JWT Token. A valid token can be obtained from the [Voicegain Portal](https://portal.voicegain.ai).   Each Context within the Account has its own JWT token. The accountId and contextId are encoded inside the token,  that is why API method requests do not require these in their request parameters.  More information about generating and using JWT with Voicegain API can be found in our  [Support Pages](https://support.voicegain.ai/hc/en-us/articles/360028023691-JWT-Authentication).   # noqa: E501

    The version of the OpenAPI document: 1.13.0 - updated August 7, 2020
    Contact: api.support@voicegain.ai
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from voicegain_speech.configuration import Configuration


class AsrSettingsRecognition(object):
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
        'complete_timeout': 'int',
        'grammars': 'list[Grammar]',
        'incomplete_timeout': 'int',
        'no_input_timeout': 'int'
    }

    attribute_map = {
        'acoustic_model_non_real_time': 'acousticModelNonRealTime',
        'acoustic_model_real_time': 'acousticModelRealTime',
        'confidence_threshold': 'confidenceThreshold',
        'max_alternatives': 'maxAlternatives',
        'sensitivity': 'sensitivity',
        'speed_vs_accuracy': 'speedVsAccuracy',
        'complete_timeout': 'completeTimeout',
        'grammars': 'grammars',
        'incomplete_timeout': 'incompleteTimeout',
        'no_input_timeout': 'noInputTimeout'
    }

    def __init__(self, acoustic_model_non_real_time=None, acoustic_model_real_time=None, confidence_threshold=0.01, max_alternatives=1, sensitivity=None, speed_vs_accuracy=None, complete_timeout=2000, grammars=None, incomplete_timeout=5000, no_input_timeout=10000, local_vars_configuration=None):  # noqa: E501
        """AsrSettingsRecognition - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._acoustic_model_non_real_time = None
        self._acoustic_model_real_time = None
        self._confidence_threshold = None
        self._max_alternatives = None
        self._sensitivity = None
        self._speed_vs_accuracy = None
        self._complete_timeout = None
        self._grammars = None
        self._incomplete_timeout = None
        self._no_input_timeout = None
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
        if complete_timeout is not None:
            self.complete_timeout = complete_timeout
        self.grammars = grammars
        if incomplete_timeout is not None:
            self.incomplete_timeout = incomplete_timeout
        if no_input_timeout is not None:
            self.no_input_timeout = no_input_timeout

    @property
    def acoustic_model_non_real_time(self):
        """Gets the acoustic_model_non_real_time of this AsrSettingsRecognition.  # noqa: E501

        (Optional) Name of an Acoustic Model that is to be used for offline and semi-real-time processing.  May include version number separated by `:` , for example, **Voicegain-BD_en-us:11** </br> If not provided a suitable default will be used.   # noqa: E501

        :return: The acoustic_model_non_real_time of this AsrSettingsRecognition.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_non_real_time

    @acoustic_model_non_real_time.setter
    def acoustic_model_non_real_time(self, acoustic_model_non_real_time):
        """Sets the acoustic_model_non_real_time of this AsrSettingsRecognition.

        (Optional) Name of an Acoustic Model that is to be used for offline and semi-real-time processing.  May include version number separated by `:` , for example, **Voicegain-BD_en-us:11** </br> If not provided a suitable default will be used.   # noqa: E501

        :param acoustic_model_non_real_time: The acoustic_model_non_real_time of this AsrSettingsRecognition.  # noqa: E501
        :type: str
        """

        self._acoustic_model_non_real_time = acoustic_model_non_real_time

    @property
    def acoustic_model_real_time(self):
        """Gets the acoustic_model_real_time of this AsrSettingsRecognition.  # noqa: E501

        (Optional) Name of a real-time capable Acoustic Model.  May include version number separated by `:`, for example, **Voicegain-IVR_en-us:3**</br> If not provided a suitable default will be used.   # noqa: E501

        :return: The acoustic_model_real_time of this AsrSettingsRecognition.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_real_time

    @acoustic_model_real_time.setter
    def acoustic_model_real_time(self, acoustic_model_real_time):
        """Sets the acoustic_model_real_time of this AsrSettingsRecognition.

        (Optional) Name of a real-time capable Acoustic Model.  May include version number separated by `:`, for example, **Voicegain-IVR_en-us:3**</br> If not provided a suitable default will be used.   # noqa: E501

        :param acoustic_model_real_time: The acoustic_model_real_time of this AsrSettingsRecognition.  # noqa: E501
        :type: str
        """

        self._acoustic_model_real_time = acoustic_model_real_time

    @property
    def confidence_threshold(self):
        """Gets the confidence_threshold of this AsrSettingsRecognition.  # noqa: E501

        Hypotheses below this threshold will result in NOMATCH  # noqa: E501

        :return: The confidence_threshold of this AsrSettingsRecognition.  # noqa: E501
        :rtype: float
        """
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, confidence_threshold):
        """Sets the confidence_threshold of this AsrSettingsRecognition.

        Hypotheses below this threshold will result in NOMATCH  # noqa: E501

        :param confidence_threshold: The confidence_threshold of this AsrSettingsRecognition.  # noqa: E501
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
        """Gets the max_alternatives of this AsrSettingsRecognition.  # noqa: E501

        number of recognition hypotheses to return as result (top N-Best)  # noqa: E501

        :return: The max_alternatives of this AsrSettingsRecognition.  # noqa: E501
        :rtype: int
        """
        return self._max_alternatives

    @max_alternatives.setter
    def max_alternatives(self, max_alternatives):
        """Sets the max_alternatives of this AsrSettingsRecognition.

        number of recognition hypotheses to return as result (top N-Best)  # noqa: E501

        :param max_alternatives: The max_alternatives of this AsrSettingsRecognition.  # noqa: E501
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
        """Gets the sensitivity of this AsrSettingsRecognition.  # noqa: E501

        affects separation of speech from background noise level  # noqa: E501

        :return: The sensitivity of this AsrSettingsRecognition.  # noqa: E501
        :rtype: float
        """
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, sensitivity):
        """Sets the sensitivity of this AsrSettingsRecognition.

        affects separation of speech from background noise level  # noqa: E501

        :param sensitivity: The sensitivity of this AsrSettingsRecognition.  # noqa: E501
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
        """Gets the speed_vs_accuracy of this AsrSettingsRecognition.  # noqa: E501

        between 0.0 and 1.0 - tradeoff between accuracy and speed/resource use  # noqa: E501

        :return: The speed_vs_accuracy of this AsrSettingsRecognition.  # noqa: E501
        :rtype: float
        """
        return self._speed_vs_accuracy

    @speed_vs_accuracy.setter
    def speed_vs_accuracy(self, speed_vs_accuracy):
        """Sets the speed_vs_accuracy of this AsrSettingsRecognition.

        between 0.0 and 1.0 - tradeoff between accuracy and speed/resource use  # noqa: E501

        :param speed_vs_accuracy: The speed_vs_accuracy of this AsrSettingsRecognition.  # noqa: E501
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
    def complete_timeout(self):
        """Gets the complete_timeout of this AsrSettingsRecognition.  # noqa: E501

        ASR complete timeout (in msec). Kicks in after grammar match has been completed. Not more valid input is possible.  # noqa: E501

        :return: The complete_timeout of this AsrSettingsRecognition.  # noqa: E501
        :rtype: int
        """
        return self._complete_timeout

    @complete_timeout.setter
    def complete_timeout(self, complete_timeout):
        """Sets the complete_timeout of this AsrSettingsRecognition.

        ASR complete timeout (in msec). Kicks in after grammar match has been completed. Not more valid input is possible.  # noqa: E501

        :param complete_timeout: The complete_timeout of this AsrSettingsRecognition.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                complete_timeout is not None and complete_timeout > 15000):  # noqa: E501
            raise ValueError("Invalid value for `complete_timeout`, must be a value less than or equal to `15000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                complete_timeout is not None and complete_timeout < 0):  # noqa: E501
            raise ValueError("Invalid value for `complete_timeout`, must be a value greater than or equal to `0`")  # noqa: E501

        self._complete_timeout = complete_timeout

    @property
    def grammars(self):
        """Gets the grammars of this AsrSettingsRecognition.  # noqa: E501

        Grammars, either GRXML, inline JJSGF grammars, built-in grammar names, or GREG grammar ids. If GREG is used it has to be single and the only one.   # noqa: E501

        :return: The grammars of this AsrSettingsRecognition.  # noqa: E501
        :rtype: list[Grammar]
        """
        return self._grammars

    @grammars.setter
    def grammars(self, grammars):
        """Sets the grammars of this AsrSettingsRecognition.

        Grammars, either GRXML, inline JJSGF grammars, built-in grammar names, or GREG grammar ids. If GREG is used it has to be single and the only one.   # noqa: E501

        :param grammars: The grammars of this AsrSettingsRecognition.  # noqa: E501
        :type: list[Grammar]
        """
        if self.local_vars_configuration.client_side_validation and grammars is None:  # noqa: E501
            raise ValueError("Invalid value for `grammars`, must not be `None`")  # noqa: E501

        self._grammars = grammars

    @property
    def incomplete_timeout(self):
        """Gets the incomplete_timeout of this AsrSettingsRecognition.  # noqa: E501

        ASR incomplete timeout (in msec). Kicks in when start-of-speech was detected. Lasts until grammar allows for move valid input.  # noqa: E501

        :return: The incomplete_timeout of this AsrSettingsRecognition.  # noqa: E501
        :rtype: int
        """
        return self._incomplete_timeout

    @incomplete_timeout.setter
    def incomplete_timeout(self, incomplete_timeout):
        """Sets the incomplete_timeout of this AsrSettingsRecognition.

        ASR incomplete timeout (in msec). Kicks in when start-of-speech was detected. Lasts until grammar allows for move valid input.  # noqa: E501

        :param incomplete_timeout: The incomplete_timeout of this AsrSettingsRecognition.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                incomplete_timeout is not None and incomplete_timeout > 30000):  # noqa: E501
            raise ValueError("Invalid value for `incomplete_timeout`, must be a value less than or equal to `30000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                incomplete_timeout is not None and incomplete_timeout < 0):  # noqa: E501
            raise ValueError("Invalid value for `incomplete_timeout`, must be a value greater than or equal to `0`")  # noqa: E501

        self._incomplete_timeout = incomplete_timeout

    @property
    def no_input_timeout(self):
        """Gets the no_input_timeout of this AsrSettingsRecognition.  # noqa: E501

        Used to determine if NOINPUT should be returned (in msec)  # noqa: E501

        :return: The no_input_timeout of this AsrSettingsRecognition.  # noqa: E501
        :rtype: int
        """
        return self._no_input_timeout

    @no_input_timeout.setter
    def no_input_timeout(self, no_input_timeout):
        """Sets the no_input_timeout of this AsrSettingsRecognition.

        Used to determine if NOINPUT should be returned (in msec)  # noqa: E501

        :param no_input_timeout: The no_input_timeout of this AsrSettingsRecognition.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                no_input_timeout is not None and no_input_timeout > 60000):  # noqa: E501
            raise ValueError("Invalid value for `no_input_timeout`, must be a value less than or equal to `60000`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                no_input_timeout is not None and no_input_timeout < 0):  # noqa: E501
            raise ValueError("Invalid value for `no_input_timeout`, must be a value greater than or equal to `0`")  # noqa: E501

        self._no_input_timeout = no_input_timeout

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
        if not isinstance(other, AsrSettingsRecognition):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AsrSettingsRecognition):
            return True

        return self.to_dict() != other.to_dict()
