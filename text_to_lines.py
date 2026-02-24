import re

class TextToLines:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"文本": ("STRING", {"multiline": True, "default": ""})},
            "optional": {
                "分隔符": ("STRING", {"default": "。"}),
                "保留分隔符": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("文本行", "总行数", "每行字数")
    FUNCTION = "process_text"
    CATEGORY = "Text/Operations"

    def process_text(self, 文本, 分隔符="。", 保留分隔符=True):
        if not 文本 or not 文本.strip(): return ("", 0, "0") [cite: 21]
        
        lines = []
        if 分隔符:
            if 保留分隔符:
                pattern = f"({re.escape(分隔符)})"
                parts = re.split(pattern, 文本)
                for i in range(0, len(parts) - 1, 2):
                    combined = (parts[i] + parts[i+1]).strip()
                    if combined: lines.append(combined) [cite: 21]
                if len(parts) % 2 == 1 and parts[-1].strip():
                    lines.append(parts[-1].strip()) [cite: 21]
            else:
                lines = [l.strip() for l in 文本.split(分隔符) if l.strip()] [cite: 21]
        else:
            lines = [l.strip() for l in 文本.splitlines() if l.strip()] [cite: 21]

        char_pattern = re.compile(r'[\u4e00-\u9fffA-Za-z0-9]')
        count_list = [str(len(char_pattern.findall(line))) for line in lines] [cite: 21]
            
        return ("\n".join(lines), len(lines), "\n".join(count_list)) [cite: 21]

NODE_CLASS_MAPPINGS = {"TextToLines": TextToLines}
NODE_DISPLAY_NAME_MAPPINGS = {"TextToLines": "📝 Text to Lines (文本分行)"}