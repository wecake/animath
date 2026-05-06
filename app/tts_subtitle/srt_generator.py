import os

class SrtGenerator:
    @staticmethod
    def sec(t):
        h = int(t//3600)
        m = int((t%3600)//60)
        s = int(t%60)
        ms = int((t-int(t))*1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    @staticmethod
    def generate_srt(board, scripts, path):
        lines = []
        start = 0
        for i, item in enumerate(board):
            d = item["duration"]
            txt = scripts[i]
            end = start + d
            lines.append(str(i+1))
            lines.append(f"{SrtGenerator.sec(start)} --> {SrtGenerator.sec(end)}")
            lines.append(txt)
            lines.append("")
            start = end
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))