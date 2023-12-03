import os
import shutil
import sys

import requests

# 尝试导入SECRET.py中的AZURE_TTS_SECRET类
try:
    from Modules.SECRET import OPENAI_SECRET
except ImportError:
    # 如果导入失败，尝试复制SECRET_TEMPLATE.py为SECRET.py
    try:
        shutil.copy('Modules/SECRET_TEMPLATE.py', 'Modules/SECRET.py')
        print("SECRET.py was not found. "
              "A template has been copied to SECRET.py. "
              "Please fill in the blanks and try again.")
        # 打开SECRET.py
        os.system('notepad SECRET.py')
        sys.exit(0)
    except Exception as e:
        # 如果复制失败或者再次导入失败，打印错误信息并退出
        print(f"An error occurred: {e}")
        sys.exit(1)


class OpenAIChatAPI:
    def __init__(self):
        self.api_key = OPENAI_SECRET.KEY
        self.endpoint = OPENAI_SECRET.PORTAL

    def request_chat_completion(self, messages, model="gpt-4-1106-preview", temperature=0.5, stream=False):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }

        try:
            print("正在请求聊天...")
            response = requests.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()  # Raises a HTTPError if the HTTP request returned an unsuccessful status code
            print("请求完成...")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Python 3.6+
        except Exception as err:
            print(f"An error occurred: {err}")
        return None


# 使用示例
if __name__ == "__main__":
    chat_api = OpenAIChatAPI()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
    response = chat_api.request_chat_completion(messages)
    if response:
        print(response)
