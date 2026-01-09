#!/bin/bash
# 准备推送到GitHub的脚本

set -e

echo "=========================================="
echo "准备 Counting Objects Task 推送到 GitHub"
echo "仓库: vm-dataset/O-33_counting_object_data-generator"
echo "=========================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "setup.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 清理临时文件
echo "1. 清理临时文件..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "test_output_*" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.mp4" -path "*/test_output_*/*" -delete 2>/dev/null || true
echo "   ✅ 清理完成"
echo ""

# 检查Git是否已初始化
if [ ! -d ".git" ]; then
    echo "2. 初始化Git仓库..."
    git init
    echo "   ✅ Git仓库已初始化"
else
    echo "2. Git仓库已存在，跳过初始化"
fi
echo ""

# 添加所有文件
echo "3. 添加文件到Git..."
git add .
echo "   ✅ 文件已添加"
echo ""

# 检查是否有未提交的更改
if git diff --cached --quiet; then
    echo "⚠️  没有需要提交的更改"
else
    echo "4. 提交更改..."
    git commit -m "Initial commit: Counting Objects Task Data Generator

- Follows template-data-generator format
- Compatible with VMEvalKit
- Supports generating counting objects tasks with various shapes
- Includes prompt generation, image rendering, and video generation"
    echo "   ✅ 更改已提交"
fi
echo ""

# 设置主分支名称
git branch -M main 2>/dev/null || true

echo "=========================================="
echo "✅ 准备完成！"
echo "=========================================="
echo ""
echo "下一步:"
echo ""
echo "1. 在GitHub上创建仓库 (如果还没有):"
echo "   访问: https://github.com/organizations/vm-dataset/repositories/new"
echo "   仓库名: O-33_counting_object_data-generator"
echo "   ⚠️  不要初始化README、.gitignore或LICENSE（我们已经有了）"
echo ""
echo "2. 添加远程仓库并推送:"
echo "   git remote add origin https://github.com/vm-dataset/O-33_counting_object_data-generator.git"
echo "   git push -u origin main"
echo ""
echo "或者如果远程仓库已存在:"
echo "   git remote set-url origin https://github.com/vm-dataset/O-33_counting_object_data-generator.git"
echo "   git push -u origin main"
echo ""

