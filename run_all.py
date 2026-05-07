# run_all.py 一键全自动
import os
import time

print("🚀 启动动画渲染...")
os.system("python run_manim.py")
time.sleep(2)

print("🚀 启动配音生成...")
os.system("python run_voice.py")
time.sleep(2)

print("🚀 启动成片合成...")
os.system("python run_artifact.py")

print("\n🎉 全部完成！")