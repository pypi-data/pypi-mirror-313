# import os
# import socket
# import threading
# import time
#
# from nacos import NacosClient
#
#
# class NacosService:
#     def __init__(self):
#         self.server_addresses = os.getenv('NACOS_SERVER_ADDR')
#         self.namespace = os.getenv('NACOS_CONFIG_NAMESPACE')
#         self.service_name = "is3-python-sdk"
#         self.username = os.getenv('NACOS_CONFIG_USERNAME')
#         self.password = os.getenv('NACOS_CONFIG_PASSWORD')
#         self.port = 70
#         try:
#             self.client = NacosClient(server_addresses=self.server_addresses, namespace=self.namespace,
#                                       username=self.username, password=self.password)
#             self.ip = self.get_ip()
#             self.register_server()
#             self.thread = threading.Thread(target=self.ref_nacos_listener, daemon=True)
#             self.thread.start()
#         except Exception as e:
#             print("Nacos service failed to start", e)
#
#     def get_ip(self):
#         hostname = socket.gethostname()
#         ip = socket.gethostbyname(hostname)
#         return ip
#
#     def ref_nacos_listener(self):
#         while True:
#             self.client.send_heartbeat(service_name=self.service_name, ip=self.ip, port=self.port)
#             time.sleep(3)
#
#     def register_server(self):
#         self.client.add_naming_instance(service_name=self.service_name, ip=self.ip, port=self.port)
