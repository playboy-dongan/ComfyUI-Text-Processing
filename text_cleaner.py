import re

class TextCleaner:
    # 预编译正则，提高复用性能
    BRACKET_PATTERN = re.compile(r'[（(\[ {【].*?[）)\] }】]')
    TIMESTAMP_PATTERN = re.compile(r'\b\d{1,2}:\d{2}(?::\d{2})?(\.\d+)?\b')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING", {"multiline": True, "default": ""}),
                "保留字符": ("STRING", {"default": "/:_-", "multiline": False}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("清洗后的文本",)
    FUNCTION = "process_text"
    CATEGORY = "Text/Operations"

    def process_text(self, 文本, 保留字符="/:_-"):
        if not 文本 or not isinstance(文本, str): return ("",) [cite: 5, 14, 28]

        # 1. 清理括号及内容与时间戳 [cite: 29, 30]
        text = self.BRACKET_PATTERN.sub('', 文本)
        text = self.TIMESTAMP_PATTERN.sub('', text)
        
        # 2. 动态白名单过滤 [cite: 31]
        safe_chars = re.escape(保留字符)
        pattern = f'[^\u4e00-\u9fa5a-zA-Z0-9\s\.,!\?，。！？\'\"“”‘’{safe_chars}]'
        text = re.sub(pattern, '', text)
        
        # 3. 紧凑行处理 [cite: 32]
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return ("\n".join(lines),)

NODE_CLASS_MAPPINGS = {"TextCleaner": TextCleaner} [cite: 32]
NODE_DISPLAY_NAME_MAPPINGS = {"TextCleaner": "🧼 Text Cleaner (文本清洗)"} [cite: 32]