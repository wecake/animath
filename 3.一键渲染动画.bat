@echo off
chcp 65001
call .venv\Scripts\activate
manim -pql output/manim_code.py MathAnimation
pause