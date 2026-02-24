import re

class TextLineBalancer:
    # 预编译优先级断句正则
    # 优先级1：强终止标点 (句号、感叹号、问号、分号)
    STRONG_PUNCT = re.compile(r'[.!?;。！？；]')
    # 优先级2：弱停顿标点 (逗号、冒号、顿号、空格)
    WEAK_PUNCT = re.compile(r'[,，:：、\s]')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文本": ("STRING", {"multiline": True, "default": ""}),
                "目标字数": ("INT", {"default": 50, "min": 10, "max": 500, "step": 1}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("均衡文本", "总行数", "每行字数")
    FUNCTION = "balance_text"
    CATEGORY = "Text/Operations"

    def balance_text(self, 文本, 目标字数):
        if not 文本 or not isinstance(文本, str):
            return ("", 0, "0")

        # 1. 预处理：将原有换行符清理掉，合并为单行文本流
        clean_text = " ".join(文本.split())
        
        lines = []
        text_data = clean_text
        
        while text_data:
            # 如果剩余文本已经少于目标字数，直接结束
            if len(text_data) <= 目标字数:
                lines.append(text_data.strip())
                break
            
            # 设定智能搜索区间：在目标位置的前后浮动 (80% - 125%)
            start_search = int(目标字数 * 0.8)
            end_search = min(int(目标字数 * 1.25), len(text_data))
            
            segment = text_data[start_search:end_search]
            split_point = 目标字数 # 默认硬切分点
            
            # 尝试寻找强标点
            matches = list(self.STRONG_PUNCT.finditer(segment))
            if not matches:
                # 尝试寻找弱标点
                matches = list(self.WEAK_PUNCT.finditer(segment))
            
            if matches:
                # 取区间内最后一个匹配点，让每一行尽可能饱满
                split_point = start_search + matches[-1].end()
            
            # 切分并清理
            current_line = text_data[:split_point].strip()
            if current_line:
                lines.append(current_line)
            
            text_data = text_data[split_point:].lstrip()

        # 2. 统计每行字符数（仅统计汉字、字母、数字）
        char_pattern = re.compile(r'[\u4e00-\u9fffA-Za-z0-9]')
        counts = [str(len(char_pattern.findall(line))) for line in lines]
        
        return ("\n".join(lines), len(lines), "\n".join(counts))

NODE_CLASS_MAPPINGS = {"TextLineBalancer": TextLineBalancer}
NODE_DISPLAY_NAME_MAPPINGS = {"TextLineBalancer": "⚖️ Text Balancer (智能行均衡)"}