import requests
import json
import traceback
import os
from dotenv import load_dotenv

load_dotenv()

### time costs
from functools import wraps
def ISZ_main_exception_report_args(msg):
    def main_exception_report(function):
        @wraps(function)
        def function_main_exception_report(*args, **kwargs):
            try:
                person_msgreport = ISZMsgReport(webhook=os.getenv("ISZ_MSGRERPORT_WEBHOOK"))
                baselogger = function(*args, **kwargs)
            except Exception as e:
                person_msgreport.chatbot_text(title=f"{msg}",content=f"{msg}:<br>{e}<br><br>{traceback.format_exc()}")
            else:
                ### 原始
                # # 通过遍历handlers列表来找到名为'counting_handler'的handler
                # for handler in baselogger.logger.handlers:
                #     if handler.get_name() == 'counting_handler':
                #         if handler.error_count == 0 and handler.warning_count == 0:
                #             ## 无需通知
                #             None
                #         else:
                #             content = f"Run pass But have something : Error:{handler.error_count},Error_message:{handler.error_messages}; Warning:{handler.warning_count},Warning_message:{handler.warning_messages}"
                #             person_msgreport.chatbot_text(title=f"Run pass",content=content)
                
                """
                检查是否存在名为'counting_handler'且错误计数或警告计数不为零的处理程序，如果存在，则生成相应的消息并发送。
                第二个版本使得一旦找到符合条件的处理程序就立即停止搜索，对于大量处理程序的情况可能更有效率。
                """
                ### 版本一
                # content = "\n".join(
                #     f"Run pass But have something : Error:{handler.error_count},Error_message:{handler.error_messages}; Warning:{handler.warning_count},Warning_message:{handler.warning_messages}" 
                #     for handler in baselogger.logger.handlers 
                #     if handler.get_name() == 'counting_handler' and (handler.error_count != 0 or handler.warning_count != 0)
                # )
                # if content:
                #     person_msgreport.chatbot_text(title=f"Run pass", content=content)

                ### 版本二
                handler = next((h for h in baselogger.logger.handlers if h.get_name() == 'counting_handler'), None)
                if handler and (handler.error_count != 0 or handler.warning_count != 0):
                    content = f"Run pass But have something : Error:{handler.error_count},Error_message:{handler.error_messages}; Warning:{handler.warning_count},Warning_message:{handler.warning_messages}"
                    person_msgreport.chatbot_text(title=f"Run pass", content=content)
            return None
        return function_main_exception_report
    return main_exception_report

class ISZMsgReport():
    def __init__(self,webhook) -> None:
        self.webhook = webhook
        pass
    def chatbot_text(self, code=None, touser:list = [], title:str = None, 
                     content:str = None,content_type="sampleMarkdown"):
        """
        Description:
            ISZ chatbot send message to user persions 
        Args:
            code (str): robot code 
            touser (list): users_id
            title (str): message title
            content (str): message content
            content_type (str): [sampleText/sampleMarkdown] message content_type
        Returns:
            reponse: api repose
        Example:
            
        Raises:
            Exception: error
        """
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "code": code,
            "userIds": 
                touser
            ,
            "content": content,
            "title": title,
            "type":content_type
        }
        result = requests.post(self.webhook, json=data, headers=headers)
        return result
    
    def send_group_markdown(self,code = os.getenv('ISZ_MSGRRRPORT_GROUP_CODE'), conversation_id =os.getenv('ISZ_MSGRRRPORT_GROUP_CONVERSATION_ID'), content = None, title = None):
        payload = json.dumps({
            "code": code,
            "conversationId": conversation_id,
            "content": content,
            "title": title
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.webhook, headers=headers, data=payload)
        return response




class DFS():
    ###上传文件，包含图片
    def __init__(self,tracker_conf_file="client-test.conf",file_base_url=os.getenv('ISZ_MSGRERPORT_FILE_URL')) -> None:
        """__init__ _summary_

        update issyzone dfs

        Args:
            tracker_conf_file (str, optional): confine file . Defaults to "client-test.conf".
            file_base_url (str, optional): url. Defaults to "http://ip".
        """
        self.tracker_conf =tracker_conf_file
        self.file_base_url = file_base_url
        from fdfs_client.client import get_tracker_conf, Fdfs_client
        tracker_conf = get_tracker_conf(self.tracker_conf)
        self.client = Fdfs_client(tracker_conf)
        pass
    def uploadDfs(self, local_path, file_name=None):
        """
        Description:
            upload file with dfs
        Args:
            local_path (str): file abspath

            file_name [option](str) : file name
        Returns:
            None
        Example:
        Raises:
            Exception: error
        """
        
        ext = ''
        if local_path.rindex('.') + 2 < len(local_path):
            ext = local_path[local_path.rindex('.') + 1:]
        if file_name is None:
            file_name = 'auto.' + ext
        meta = {'fileExt': ext, 'fileLength': str(os.path.getsize(local_path)), 'fileName': file_name}
        result = self.client.upload_by_filename(local_path, meta)
        if result["Status"] == "Upload successed.":
          remote_file = result["Remote file_id"]
          file_path = str(remote_file, encoding="utf-8")
          return file_path
        else:
            return None
    def get_absolute_path(self, relative_path):
      return os.path.abspath(relative_path) if os.path.exists(relative_path) else None
    

    def upload_file_remote_id(self,picture_path):
        result_remote_file_id = self.uploadDfs(local_path=picture_path)
        if not result_remote_file_id:
            self.logger.error(f"{picture_path}, result_remote_file_id:None, please check!")
            return (None,None)
        file_down = self.file_base_url + "/system/file/origin?filePath=" + result_remote_file_id
        return (os.path.split(picture_path)[-1] , file_down)