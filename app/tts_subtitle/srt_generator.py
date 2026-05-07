import os

def generate_srt(scripts, sec=3):
    sub_dir = "output/subtitle"
    os.makedirs(sub_dir, exist_ok=True)
    srt_path = os.path.join(sub_dir, "auto.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, line in enumerate(scripts):
            s = i * sec
            e = (i + 1) * sec
            f.write(f"{i+1}\n00:00:{s:02d},000 --> 00:00:{e:02d},000\n{line}\n\n")