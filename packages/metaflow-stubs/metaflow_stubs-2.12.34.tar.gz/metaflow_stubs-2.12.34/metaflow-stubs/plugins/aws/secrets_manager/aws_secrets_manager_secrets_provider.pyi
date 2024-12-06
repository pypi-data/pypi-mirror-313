######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.34                                                                                #
# Generated on 2024-12-04T14:12:34.708566                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import abc
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.secrets
    import abc
    import metaflow.exception

from ....exception import MetaflowException as MetaflowException
from ...secrets import SecretsProvider as SecretsProvider

AWS_SECRETS_MANAGER_DEFAULT_REGION: None

class MetaflowAWSSecretsManagerBadResponse(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the response from AWS Secrets Manager is not valid in some way
    """
    ...

class MetaflowAWSSecretsManagerDuplicateKey(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the response from AWS Secrets Manager contains duplicate keys
    """
    ...

class MetaflowAWSSecretsManagerJSONParseError(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the SecretString response from AWS Secrets Manager is not valid JSON
    """
    ...

class MetaflowAWSSecretsManagerNotJSONObject(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the SecretString response from AWS Secrets Manager is not valid JSON object (dictionary)
    """
    ...

class AwsSecretsManagerSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Reads a secret from AWS Secrets Manager and returns it as a dictionary of environment variables.
        
        The secret payload from AWS is EITHER a string OR a binary blob.
        
        If the secret contains a string payload ("SecretString"):
        - if the `parse_secret_string_as_json` option is True (default):
            {SecretString} will be parsed as a JSON. If successfully parsed, AND the JSON contains a
            top-level object, each entry K/V in the object will also be converted to an entry in the result. V will
            always be casted to a string (if not already a string).
        - If `parse_secret_string_as_json` option is False:
            {SecretString} will be returned as a single entry in the result, with the key being the secret_id.
        
        Otherwise, the secret contains a binary blob payload ("SecretBinary"). In this case
        - The result dic contains '{SecretName}': '{SecretBinary}', where {SecretBinary} is a base64-encoded string
        
        All keys in the result are sanitized to be more valid environment variable names. This is done on a best effort
        basis. Further validation is expected to be done by the invoking @secrets decorator itself.
        
        :param secret_id: ARN or friendly name of the secret
        :param options: unused
        :param role: AWS IAM Role ARN to assume before reading the secret
        :return: dict of environment variables. All keys and values are strings.
        """
        ...
    ...

