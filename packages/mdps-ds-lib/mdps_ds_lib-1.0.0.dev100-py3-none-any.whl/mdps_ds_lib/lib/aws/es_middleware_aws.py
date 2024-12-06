import logging

from requests_aws4auth import AWS4Auth

from mdps_ds_lib.lib.aws.aws_cred import AwsCred
from mdps_ds_lib.lib.aws.es_middleware import ESMiddleware
from elasticsearch import Elasticsearch, RequestsHttpConnection

LOGGER = logging.getLogger(__name__)


class EsMiddlewareAws(ESMiddleware):

    def __init__(self, index, base_url, port=443) -> None:
        super().__init__(index, base_url, port)
        base_url = base_url.replace('https://', '')  # hide https
        self._index = index
        aws_cred = AwsCred()
        service = 'es'
        credentials = aws_cred.get_session().get_credentials()
        aws_auth = AWS4Auth(credentials.access_key, credentials.secret_key, aws_cred.region, service,
                            session_token=credentials.token)
        self._engine = Elasticsearch(
            hosts=[{'host': base_url, 'port': port}],
            http_auth=aws_auth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
