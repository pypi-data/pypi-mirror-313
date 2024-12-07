import datetime
import time

import requests
from MZAPI.APM import APMClient
from MZAPI.KVS import LogHandler
from MZAPI.LOG import PublicIPTracker
from MZAPI.headers import CustomRequestHeaders


class WenAnSou:
    def __init__(self, client_name):
        self.ip = PublicIPTracker()
        self.log = LogHandler()
        M = CustomRequestHeaders()
        self.headers = M.reset_headers()
        self.apm_client = APMClient(
            client_name=client_name,
            host_name="http://ap-shanghai.apm.tencentcs.com:4317",
            token="kCrxvCIYEzhZfAHETXEB",
            peer_service="龙珠API",
            peer_instance="111.229.214.169:443",
            peer_address="111.229.214.169",
            peer_ipv6="-",
            http_host="https://www.hhlqilongzhu.cn/api/wenan_sou.php",
            server_name="米粥API",
        )
        self.tracer = self.apm_client.get_tracer()

    def get_response(self, Content):
        with self.tracer.start_as_current_span("wenansou") as span:
            url = f"https://www.hhlqilongzhu.cn/api/wenan_sou.php?msg={Content}"
            response = requests.get(url, headers=self.headers)
            current_timestamp = int(time.time())
            dt_object = datetime.datetime.fromtimestamp(current_timestamp)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            span.set_attribute("id", current_timestamp)
            span.set_attribute("url", url)
            span.set_attribute("response", response.text)
            span.set_attribute("HTTP_status_code", response.status_code)
            span.set_attribute("HTTP_response_content", response.text)
            span.set_attribute("HTTP_response_size", len(response.text))
            span.set_attribute(
                "http.response_time", response.elapsed.total_seconds() * 1000
            )
            self.log.start_process_log(response.text, "WenAnSou")
            self.ip.start_track_log()
            M = response.text
            W = {
                "id": current_timestamp,
                "time": formatted_time,
                "response": M,
            }
            return W
