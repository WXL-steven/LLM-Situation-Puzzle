import json
import re


class JSONTemplateReader:
    def __init__(self, filepath):
        # 初始化时加载JSON文件
        self.filepath = filepath
        self.template_data = self._load_json_file(filepath)

    def _load_json_file(self, filepath):
        # 尝试加载JSON文件，如果失败则抛出异常
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"未找到文件 '{filepath}'。")
        except json.JSONDecodeError:
            raise Exception(f"文件 '{filepath}' 不是有效的JSON文件。")

    def _replace_placeholders(self, text, variables):
        # 内部函数，用于替换文本中的占位符
        def replacement(match):
            placeholder = match.group(1)
            # 从字典中获取对应的值，如果不存在则返回 "Variable missing"
            # 这里使用 str() 函数确保所有的值都被转换为字符串
            return str(variables.get(placeholder, "Variable missing"))

        # 正则表达式，用于查找形式为 {placeholder} 的占位符
        pattern = re.compile(r'\{([^}]+)\}')
        return pattern.sub(replacement, text)

    def get_replaced_json(self, variables):
        # 获取替换后的JSON数据
        replaced_data = {}
        for key, value in self.template_data.items():
            if isinstance(value, str):
                replaced_data[key] = self._replace_placeholders(value, variables)
            else:
                replaced_data[key] = value
        return replaced_data
