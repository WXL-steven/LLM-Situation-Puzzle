import sys

# 尝试导入模块中的类
try:
    from Modules.Azure_TTS import TextToSpeech
    from Modules.json_template_reader import JSONTemplateReader
    from Modules.OpenAI_GPT import OpenAIChatAPI
except ImportError:
    # 如果导入失败，打印错误信息并退出
    print("An error occurred while importing Azure_TTS.py. "
          "Please make sure the file exists and try again.")
    sys.exit(1)

if __name__ == "__main__":
    print("正在初始化...")
    azure_tts = TextToSpeech()
    chat_api = OpenAIChatAPI()

    variables_dict = {
        "Title": "Variable missing",
        'Soup_Table': 'Loaded failed',
        'Soup_Base': 'Loaded failed',
        # 'Compressed_Context': 0,
        # 'Previous_Context' 没有提供，将使用默认值 "Variable missing"
    }
    story_reader = JSONTemplateReader(r'configs/stories.json')
    prompt_reader = JSONTemplateReader(r'configs/prompts.json')
    variables_dict["Title"] = story_reader.get_replaced_json({})["Stories"][0]["Title"]
    variables_dict["Soup_Table"] = story_reader.get_replaced_json({})["Stories"][0]["Soup_Table"]
    variables_dict["Soup_Base"] = story_reader.get_replaced_json({})["Stories"][0]["Soup_Base"]
    system_prompt = prompt_reader.get_replaced_json(variables_dict)["System_Prompt"]
    initial_prompt = prompt_reader.get_replaced_json(variables_dict)["System_Prompt_Initial"]
    processed_prompt = prompt_reader.get_replaced_json(variables_dict)["System_Prompt_Proceed"]

    chat_context = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": initial_prompt}
    ]

    print("初始化完成...")

    print("正在启动聊天...")
    response = chat_api.request_chat_completion(chat_context)
    response_content = response["choices"][-1]["message"]["content"]
    print(f"\n主持人: {response_content}")
    if response:
        azure_tts.synthesize(response["choices"][-1]["message"]["content"])
    chat_context.append(response["choices"][-1]["message"])
    while True:
        user_input = input("\n玩家:")
        if user_input == "exit":
            break
        chat_context.append({"role": "user", "content": user_input})
        response = chat_api.request_chat_completion(chat_context)
        response_content = response["choices"][-1]["message"]["content"]
        print(f"\n主持人: {response_content}")
        if response:
            azure_tts.synthesize(response["choices"][-1]["message"]["content"])
        chat_context.append(response["choices"][-1]["message"])
    print("聊天结束...")
