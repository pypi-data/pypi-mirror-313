import json
import logging
import mimetypes
import os

from is3_python_sdk.domain.task_data import TaskDataDef
from is3_python_sdk.utils import Logging
from is3_python_sdk.utils.fileUtil import FileUtil
from is3_python_sdk.utils.is3_request_util import RequestUtil

Logging()


class iS3PythonApi:
    def __init__(self, headers, iS3Addr, prjId):
        self.prjId = prjId
        self.headers = headers
        self.server_url = iS3Addr

    '''
            根据自定义编码查询任务流编码。

            参数:
            customCode (str): 自定义任务流编码。
    '''

    def getProcessCode(self, customCode):

        url = f'{self.server_url}/is3-modules-open/scheduling/process-definition-code/custom?customCode={customCode}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            通过自定义编码运行任务流

            参数:
            json (dict)
                示例 json:
                {
                    "customCode"(str),  # 自定义编码
                    "data"(array(dict)),  # 数据列表
                }
    '''

    def startTaskSchedulingByCustomCode(self, jsonData):
        url = f'{self.server_url}/is3-modules-open/scheduling/start/process-instance/custom-code'

        try:
            response = RequestUtil.post(url=url, json=jsonData, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询metatable列表数据。

            参数:
            jsonData (dict):
    '''

    def getMetaTableList(self, jsonData):
        url = f'{self.server_url}/data-main/operation/getDataByCondition'
        jsonData['prjId'] = self.prjId
        try:
            response = RequestUtil.post(url, jsonData, self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            Minio 文件上传。

            参数:
            filePath (str): 需要上传的文件路径，包括文件名和扩展名。例如 'E:/uploads/myfile.png'。
    '''

    def uploadFile(self, filePath):
        content_type, _ = mimetypes.guess_type(filePath)
        content_type = content_type or 'application/octet-stream'
        file_name = filePath.split('\\')[-1]
        files = {'file': (file_name, open(filePath, 'rb'), content_type)}
        self.headers.pop('Content-Type', None)
        url = f'{self.server_url}/is3-modules-file/inner/upload'

        try:
            response = RequestUtil.post_with_file(url=url, headers=self.headers, files=files)  # 检查请求是否成功
            if response['code'] == 200:
                logging.info('文件上传成功')
                return response  # 返回响应的 JSON 数据
            else:
                logging.error('文件上传失败，状态码：' + str(response['code']))
                return None
        except Exception as e:
            logging.error(f'请求异常: {e}')

    """
            上传目录下文件到指定目录minio（递归调用并根据递归目录设置返回url）

            :param path: 自定义存储文件路径
            :param filePaths: 需要上传的文件路径目录
    """

    def uploadFilesByPathByRecursion(self, path, base_dir):
        all_data = []
        """递归遍历目录，并处理每个文件夹"""

        try:
            response = self.uploadFilesByPath(path, base_dir)
            if response.get('success'):
                all_data.extend(response.get('data', []))
            # 遍历当前目录中的所有文件和文件夹
            for entry in os.listdir(base_dir):
                entry_path = os.path.join(base_dir, entry)
                if os.path.isdir(entry_path):
                    # 处理文件夹
                    relative_path = os.path.relpath(entry_path, base_dir)
                    relative_path = f'{path}/{relative_path}'
                    print(relative_path)
                    response = self.uploadFilesByPath(relative_path, entry_path)
                    all_data.extend(response.get('data', []))
                    # 递归进入子目录
                    self.uploadFilesByPathByRecursion(path, entry_path)
        except Exception as e:
            logging.error(f"处理异常: {e}")
        return all_data

    """
            上传目录下文件到指定目录minio
        
            :param path: 自定义存储文件路径
            :param filePaths: 需要上传的文件路径目录
    """

    def uploadFilesByPath(self, path, dir_path):

        url = f'{self.server_url}/is3-modules-file/inner/uploadByPath'
        files = []
        file_objects = []  # 追踪打开的文件对象
        self.headers.pop('Content-Type', None)
        if not os.path.isdir(dir_path):
            logging.error(f"提供的路径不是有效目录: {dir_path}")
            return None
        # 遍历目录中的所有文件
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            if os.path.isfile(file_path):
                # 获取文件的 MIME 类型
                content_type, _ = mimetypes.guess_type(file_path)
                content_type = content_type or 'application/octet-stream'
                file_object = open(file_path, 'rb')
                file_objects.append(file_object)
                # 将文件添加到 files 列表中
                files.append(('files', (file_name, file_object, content_type)))
        data = {'path': path}
        try:
            # 发送 POST 请求
            response = RequestUtil.post_with_file_path(url, files=files, data=data, headers=self.headers)
            return response
        except Exception as e:
            # 捕获请求异常并打印错误信息
            logging.error(f"请求异常: {e}")
            return None
        finally:
            # 关闭所有打开的文件
            for file_obj in file_objects:
                file_obj.close()

    '''
            查询对象组列表 (查询iS3PythonAPi实例化时项目下的数据)
    '''

    def getObjectList(self):
        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsList?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询对象组的对象实例列表。

            参数:
            objsCode (str): 对象组编码。
    '''

    def getObjsInstanceList(self, objsCode):

        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsInstanceList/{objsCode}?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询子类型列表

            参数:
            objsCode (str): 对象组编码。
    '''

    def getObjsSubTypeList(self, objsCode):

        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsSubTypeList/{objsCode}?prjId={self.prjId}'
        try:
            response = RequestUtil.get(url=url, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            查询子类型数据
            参数:
                objsCode (str): 对象组代码。
                objCode (str): 对象编码。
                subMetaCode (str): 子类型元数据编码。
                jsonData (dict): 额外的请求参数，以 JSON 格式传递。包括分页、时间范围、比较条件等。
    
                示例 json:
                {
                    "pageNumber": 1,  # 当前页码
                    "pageSize": 10,  # 每页显示的数据条数
                    "startTime": "2024-07-01 15:53:32",  # 查询开始时间
                    "endTime": "2024-09-01 15:53:32",  # 查询结束时间
                    "keyValueCompareEnum": [],  # 关键值比较条件
                    "desc": True  # 是否按降序排列
                }
    '''

    def getObjsSubDataList(self, objsCode, objCode, subMetaCode, jsonData):
        url = f'{self.server_url}/is3-modules-engine/api/objs/getObjsSubDataList/{objsCode}/{objCode}?prjId={self.prjId}&subMetaCode={subMetaCode}'
        try:
            response = RequestUtil.post(url=url, json=jsonData, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            创建本地临时文件夹
    '''

    def preDirectory(self):
        # 构建输出文件夹路径
        output_folder_path = os.path.join(FileUtil.basePath(), 'temp', FileUtil.generateTempDir())

        # 检查目录是否存在，如果不存在则创建
        os.makedirs(output_folder_path, exist_ok=True)

        return output_folder_path

    '''
            文件预下载到指定目录，local进行copy，online进行下载。
    
            :param jsonData: 要处理的 JSON 数据，应该是字典或列表。
            :param outputFolderPath: 输出文件夹路径。
    '''

    def preDownload(self, jsonData, outputFolderPath):
        task_data_def = TaskDataDef(**jsonData)
        file_def = task_data_def.files
        if file_def:
            for file in file_def.urls:
                date_type = file.type
                full_path = os.path.join(outputFolderPath, file.name)

                # 根据url里面的type判断
                if date_type:
                    if date_type == "local":
                        FileUtil.copyFile(file.url, full_path)
                    elif date_type == "online":
                        FileUtil.downloadFile(file.url, full_path)
                    else:
                        logging.error(f"未知的 fileType: {date_type}")
                # 根据files中的type判断
                else:
                    if file_def.type == "local":
                        FileUtil.copyFile(file.url, full_path)
                    elif file_def.type == "online":
                        FileUtil.downloadFile(file.url, full_path)
                    else:
                        logging.error(f"未知的 fileType: {file_def.type}")
        else:
            logging.error("files is None")

    '''
            将 JSON 字符串保存到指定的文件中。
    
            :param jsonString: 要保存到文件的 JSON 字符串。
            :param filePath: 保存 JSON 数据的文件路径。
     '''

    def saveJsonToFile(self, jsonString: str, filePath: str):
        try:
            # 确保文件所在目录存在
            directory = os.path.dirname(filePath)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 将字符串解析为 Python 对象（列表或字典）
            json_object = json.loads(jsonString)

            with open(filePath, 'w') as file:
                json.dump(json_object, file, indent=4)

        except json.JSONDecodeError as e:
            logging.error("JSON 解析异常:", e)
            # 处理 JSON 解析异常

        except IOError as e:
            logging.error("文件写入异常:", e)

    '''数据插入-支持批量'''

    def addData(self, jsonData):
        url = f'{self.server_url}/data-main/operation/addData'
        try:
            response = RequestUtil.post(url=url, headers=self.headers, json=jsonData)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''数据删除-支持批量'''

    def deleteDataByCondition(self, jsonData):
        url = f'{self.server_url}/data-main/operation/deleteDataByCondition'
        try:
            response = RequestUtil.post(url=url, headers=self.headers, json=jsonData)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response['code'])
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')

    '''
            发送心跳

            参数:
            json (dict)
                示例 json:
                {
                    "customCode"(str),  # 自定义编码
                    "data"(array(dict)),  # 数据列表
                }
    '''

    def sendHeartbeat(self, jsonData):
        url = f'{self.server_url}/is3-platform-manager/heart/management/send/heartbeat'
        try:
            response = RequestUtil.post(url=url, json=jsonData, headers=self.headers)
            if response['code'] != 200:
                logging.error(f'请求失败，状态码：', response.get('code'))
            return response
        except Exception as e:
            logging.error(f'请求异常：{e}')
