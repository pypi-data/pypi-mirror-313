import datetime
import json
import time
import requests
from MZAPI.APM import APMClient
from MZAPI.KVS import LogHandler
from MZAPI.LOG import PublicIPTracker
from MZAPI.headers import CustomRequestHeaders


class BAIDU:
    def __init__(self, client_name):
        self.ip = PublicIPTracker()
        self.log = LogHandler()
        M = CustomRequestHeaders()
        self.headers = M.reset_headers()
        self.apm_client = APMClient(
            client_name=client_name,
            host_name="http://ap-shanghai.apm.tencentcs.com:4317",
            token="kCrxvCIYEzhZfAHETXEB",
            peer_service="小冰API",
            peer_instance="111.229.214.169:443",
            peer_address="111.229.214.169",
            peer_ipv6="-",
            http_host="https://xiaobapi.top/api/xb/api/baidu_icp.php",
            server_name="米粥API",
        )
        self.tracer = self.apm_client.get_tracer()

    def get_response(self, Content):
        """
        发送HTTP GET请求到百度ICP查询接口，并获取响应数据。
        该方法主要功能是：
        1. 构造查询URL，包含域名参数。
        2. 发送HTTP GET请求到指定URL。
        3. 记录请求和响应的详细信息到APM系统。
        4. 获取客户端公网IP的详细信息。
        5. 将响应数据和相关信息封装成字典返回。
        参数:
        Content (str): 需要查询的域名。
        返回:
        dict: 包含请求ID、时间戳和响应内容的字典。
        异常:
        requests.RequestException: 如果请求过程中发生异常，则抛出此异常。
        """
        with self.tracer.start_as_current_span("bdbeian") as span:
            url = f"https://xiaobapi.top/api/xb/api/baidu_icp.php?domain={Content}"
            response = requests.get(url, headers=self.headers)
            current_timestamp = int(time.time())
            dt_object = datetime.datetime.fromtimestamp(current_timestamp)
            formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
            IP = self.ip.get_public_ip()
            span.set_attribute("id", current_timestamp)
            span.set_attribute("url", url)
            span.set_attribute(
                "response", json.dumps(response.json(), ensure_ascii=False)
            )
            span.set_attribute("HTTP_status_code", response.status_code)
            M = response.json()
            span.set_attribute("HTTP_response_size", len(json.dumps(M)))
            span.set_attribute("HTTP_response_content_type", "application/json")
            span.set_attribute("HTTP_request_size", len(json.dumps(Content)))
            span.set_attribute("Method", "GET")
            span.set_attribute("HTTP_request_headers", json.dumps(self.headers))
            span.set_attribute("client_ip", IP)
            self.log.start_process_log(response.json(), "baidubeian")
            self.ip.start_track_log()
            M = response.json()
            W = {
                "id": current_timestamp,
                "time": formatted_time,
                "response": M,
            }
            return W
