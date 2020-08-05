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


class TrainingSetDoc(object):
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
        'acoustic_model_used': 'str',
        'creator': 'CreatingEntity',
        'defaults': 'TrainingSetDocDefaults',
        'name': 'str',
        'processed_data_location': 'FileLocation',
        'raw_data_location': 'FileLocation',
        'set_id': 'str',
        'statistics': 'TrainingSetDocStatistics',
        'status': 'TrainingSetStatus',
        'status_msg': 'str',
        'store_type': 'TrainingSetStoreType'
    }

    attribute_map = {
        'acoustic_model_used': 'acousticModelUsed',
        'creator': 'creator',
        'defaults': 'defaults',
        'name': 'name',
        'processed_data_location': 'processedDataLocation',
        'raw_data_location': 'rawDataLocation',
        'set_id': 'setId',
        'statistics': 'statistics',
        'status': 'status',
        'status_msg': 'statusMsg',
        'store_type': 'storeType'
    }

    def __init__(self, acoustic_model_used=None, creator=None, defaults=None, name=None, processed_data_location=None, raw_data_location=None, set_id=None, statistics=None, status=None, status_msg=None, store_type=None, local_vars_configuration=None):  # noqa: E501
        """TrainingSetDoc - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._acoustic_model_used = None
        self._creator = None
        self._defaults = None
        self._name = None
        self._processed_data_location = None
        self._raw_data_location = None
        self._set_id = None
        self._statistics = None
        self._status = None
        self._status_msg = None
        self._store_type = None
        self.discriminator = None

        if acoustic_model_used is not None:
            self.acoustic_model_used = acoustic_model_used
        if creator is not None:
            self.creator = creator
        if defaults is not None:
            self.defaults = defaults
        self.name = name
        self.processed_data_location = processed_data_location
        self.raw_data_location = raw_data_location
        self.set_id = set_id
        if statistics is not None:
            self.statistics = statistics
        self.status = status
        if status_msg is not None:
            self.status_msg = status_msg
        self.store_type = store_type

    @property
    def acoustic_model_used(self):
        """Gets the acoustic_model_used of this TrainingSetDoc.  # noqa: E501

        Id of the Acoustic Model used to process this training set  # noqa: E501

        :return: The acoustic_model_used of this TrainingSetDoc.  # noqa: E501
        :rtype: str
        """
        return self._acoustic_model_used

    @acoustic_model_used.setter
    def acoustic_model_used(self, acoustic_model_used):
        """Sets the acoustic_model_used of this TrainingSetDoc.

        Id of the Acoustic Model used to process this training set  # noqa: E501

        :param acoustic_model_used: The acoustic_model_used of this TrainingSetDoc.  # noqa: E501
        :type: str
        """

        self._acoustic_model_used = acoustic_model_used

    @property
    def creator(self):
        """Gets the creator of this TrainingSetDoc.  # noqa: E501


        :return: The creator of this TrainingSetDoc.  # noqa: E501
        :rtype: CreatingEntity
        """
        return self._creator

    @creator.setter
    def creator(self, creator):
        """Sets the creator of this TrainingSetDoc.


        :param creator: The creator of this TrainingSetDoc.  # noqa: E501
        :type: CreatingEntity
        """

        self._creator = creator

    @property
    def defaults(self):
        """Gets the defaults of this TrainingSetDoc.  # noqa: E501


        :return: The defaults of this TrainingSetDoc.  # noqa: E501
        :rtype: TrainingSetDocDefaults
        """
        return self._defaults

    @defaults.setter
    def defaults(self, defaults):
        """Sets the defaults of this TrainingSetDoc.


        :param defaults: The defaults of this TrainingSetDoc.  # noqa: E501
        :type: TrainingSetDocDefaults
        """

        self._defaults = defaults

    @property
    def name(self):
        """Gets the name of this TrainingSetDoc.  # noqa: E501

        name of the set - has to be unique within account. no spaces allowed  # noqa: E501

        :return: The name of this TrainingSetDoc.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TrainingSetDoc.

        name of the set - has to be unique within account. no spaces allowed  # noqa: E501

        :param name: The name of this TrainingSetDoc.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def processed_data_location(self):
        """Gets the processed_data_location of this TrainingSetDoc.  # noqa: E501


        :return: The processed_data_location of this TrainingSetDoc.  # noqa: E501
        :rtype: FileLocation
        """
        return self._processed_data_location

    @processed_data_location.setter
    def processed_data_location(self, processed_data_location):
        """Sets the processed_data_location of this TrainingSetDoc.


        :param processed_data_location: The processed_data_location of this TrainingSetDoc.  # noqa: E501
        :type: FileLocation
        """
        if self.local_vars_configuration.client_side_validation and processed_data_location is None:  # noqa: E501
            raise ValueError("Invalid value for `processed_data_location`, must not be `None`")  # noqa: E501

        self._processed_data_location = processed_data_location

    @property
    def raw_data_location(self):
        """Gets the raw_data_location of this TrainingSetDoc.  # noqa: E501


        :return: The raw_data_location of this TrainingSetDoc.  # noqa: E501
        :rtype: FileLocation
        """
        return self._raw_data_location

    @raw_data_location.setter
    def raw_data_location(self, raw_data_location):
        """Sets the raw_data_location of this TrainingSetDoc.


        :param raw_data_location: The raw_data_location of this TrainingSetDoc.  # noqa: E501
        :type: FileLocation
        """
        if self.local_vars_configuration.client_side_validation and raw_data_location is None:  # noqa: E501
            raise ValueError("Invalid value for `raw_data_location`, must not be `None`")  # noqa: E501

        self._raw_data_location = raw_data_location

    @property
    def set_id(self):
        """Gets the set_id of this TrainingSetDoc.  # noqa: E501

        uuid for this training set  # noqa: E501

        :return: The set_id of this TrainingSetDoc.  # noqa: E501
        :rtype: str
        """
        return self._set_id

    @set_id.setter
    def set_id(self, set_id):
        """Sets the set_id of this TrainingSetDoc.

        uuid for this training set  # noqa: E501

        :param set_id: The set_id of this TrainingSetDoc.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and set_id is None:  # noqa: E501
            raise ValueError("Invalid value for `set_id`, must not be `None`")  # noqa: E501

        self._set_id = set_id

    @property
    def statistics(self):
        """Gets the statistics of this TrainingSetDoc.  # noqa: E501


        :return: The statistics of this TrainingSetDoc.  # noqa: E501
        :rtype: TrainingSetDocStatistics
        """
        return self._statistics

    @statistics.setter
    def statistics(self, statistics):
        """Sets the statistics of this TrainingSetDoc.


        :param statistics: The statistics of this TrainingSetDoc.  # noqa: E501
        :type: TrainingSetDocStatistics
        """

        self._statistics = statistics

    @property
    def status(self):
        """Gets the status of this TrainingSetDoc.  # noqa: E501


        :return: The status of this TrainingSetDoc.  # noqa: E501
        :rtype: TrainingSetStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TrainingSetDoc.


        :param status: The status of this TrainingSetDoc.  # noqa: E501
        :type: TrainingSetStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def status_msg(self):
        """Gets the status_msg of this TrainingSetDoc.  # noqa: E501

        Message providing additional info related to the status  # noqa: E501

        :return: The status_msg of this TrainingSetDoc.  # noqa: E501
        :rtype: str
        """
        return self._status_msg

    @status_msg.setter
    def status_msg(self, status_msg):
        """Sets the status_msg of this TrainingSetDoc.

        Message providing additional info related to the status  # noqa: E501

        :param status_msg: The status_msg of this TrainingSetDoc.  # noqa: E501
        :type: str
        """

        self._status_msg = status_msg

    @property
    def store_type(self):
        """Gets the store_type of this TrainingSetDoc.  # noqa: E501


        :return: The store_type of this TrainingSetDoc.  # noqa: E501
        :rtype: TrainingSetStoreType
        """
        return self._store_type

    @store_type.setter
    def store_type(self, store_type):
        """Sets the store_type of this TrainingSetDoc.


        :param store_type: The store_type of this TrainingSetDoc.  # noqa: E501
        :type: TrainingSetStoreType
        """
        if self.local_vars_configuration.client_side_validation and store_type is None:  # noqa: E501
            raise ValueError("Invalid value for `store_type`, must not be `None`")  # noqa: E501

        self._store_type = store_type

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
        if not isinstance(other, TrainingSetDoc):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TrainingSetDoc):
            return True

        return self.to_dict() != other.to_dict()
