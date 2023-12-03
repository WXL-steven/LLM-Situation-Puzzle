import os
import shutil
import sys

# tts_library.py
import azure.cognitiveservices.speech as speechsdk

# 尝试导入SECRET.py中的AZURE_TTS_SECRET类
try:
    from Modules.SECRET import AZURE_TTS_SECRET
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


class TextToSpeech:
    def __init__(self):
        # 使用指定的订阅密钥和服务区域创建语音配置实例
        # 请替换为你自己的订阅密钥和服务区域（例如，"westus"）
        self.speech_key = AZURE_TTS_SECRET.SPEECH_KEY
        self.service_region = AZURE_TTS_SECRET.SERVICE_REGION
        self.speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)

        # 设置语音名称，参照 https://aka.ms/speech/voices/neural 查看完整列表
        self.speech_config.speech_synthesis_voice_name = "zh-CN-YunxiNeural"

        # 使用默认扬声器作为音频输出创建语音合成器
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def synthesize(self, text):
        # 将接收到的文本合成为语音
        # 执行此行时，合成的语音应该通过扬声器听到
        print("正在合成语音...")
        result = self.speech_synthesizer.speak_text_async(text).get()

        # 检查结果
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"文本已合成为语音并通过扬声器播放，用量:{len(text)}字")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("语音合成已取消: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("错误详情: {}".format(cancellation_details.error_details))
            print("你是否更新了订阅信息？")


# 下面是如何使用这个库的示例
if __name__ == "__main__":
    tts = TextToSpeech()
    print("请输入你想要合成的文本...")
    text_to_synthesize = input()
    tts.synthesize(text_to_synthesize)
