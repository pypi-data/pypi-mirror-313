from chaiverse.http_client import PrometheusClient
from chaiverse import config

from datetime import datetime

DEFAULT_QUERY_RANGE = 36000

class PrometheusService():
    def __init__(self,
            submission_id: str,
            start_epoch_time: int = None,
            end_epoch_time: int = None,
            step: str = "10m",
            developer_key: str = None):
        self.submission_id = submission_id
        self.start_epoch_time = start_epoch_time
        self.end_epoch_time = end_epoch_time
        self.step = step
        self.developer_key = developer_key

    @property
    def query_params(self):
        params = {
                "start": self.start_epoch_time,
                "end": self.end_epoch_time,
                "step": self.step
                }
        return params

    def get_metrics(self, endpoint):
        return self._make_prometheus_client_requests(endpoint)

    def get_usage_metrics(self):
        return self.get_metrics(config.USAGE_METRICS_ENDPOINT)

    def get_latency_metrics(self):
        return self.get_metrics(config.LATENCY_METRICS_ENDPOINT)

    def _make_prometheus_client_requests(self, endpoint):
        http_client = PrometheusClient(developer_key=self.developer_key)
        response = http_client.get(endpoint=endpoint, params=self.query_params, submission_id=self.submission_id)
        return response

