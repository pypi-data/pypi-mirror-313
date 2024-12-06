from kypo.cloud_commons import KypoException


class KypoAwsClientException(KypoException):
    """
    Base exception for all AWS client exceptions
    """

    pass


class ImageDoesNotExist(KypoAwsClientException):
    """
    AWS API did not find Image matching ID
    """

    def __init__(self, image_id: str):
        self.image_id = image_id

    def __str__(self):
        return f'AWS Client: Image with ID="{self.image_id}" does not exist'


class KeyPairDoesNotExist(KypoAwsClientException):
    """
    AWS API did not find key pair matching the name
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'AWS Client: KeyPair with NAME="{self.name}" does not exist'
