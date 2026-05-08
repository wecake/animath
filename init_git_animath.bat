@echo off
chcp 65001
echo ==============================================
echo  初始化 Git 仓库
echo  main = SaaS 新版架构
echo  legacy-gradio = 旧Gradio单文件版本
echo ==============================================

echo.
echo 1. 初始化Git仓库
git init

echo.
echo 2. 创建 .gitignore (自动忽略缓存/视频/虚拟环境)
echo __pycache__/ > .gitignore
echo .env >> .gitignore
echo media/ >> .gitignore
echo *.mp4 >> .gitignore
echo *.pyc >> .gitignore
echo .uv/ >> .gitignore
echo venv/ >> .gitignore
echo .venv/ >> .gitignore
echo output/ >> .gitignore
echo batch_output/ >> .gitignore
echo .next/ >> .gitignore
echo node_modules/ >> .gitignore

echo.
echo 3. 提交当前SaaS架构到 main 分支
git add .
git commit -m "feat: initial SaaS architecture (main)"

echo.
echo 4. 创建旧版分支 legacy-gradio 并切换
git checkout -b legacy-gradio
echo 已切换到旧版分支 legacy-gradio
echo 请把旧Gradio项目文件放进来后执行：
echo git add .
echo git commit -m "legacy: gradio standalone version"

echo.
echo 5. 切回 main 分支
git checkout main

echo.
echo ==============================================
echo ✅ Git 分支创建完成！
echo 🟢 主分支：main      (SaaS新版)
echo 🟡 旧分支：legacy-gradio (Gradio单文件版)
echo ==============================================
pause