#!/bin/bash
# 快速推送到GitHub的脚本

REPO_NAME="O-33_counting_object_data-generator"
ORG="vm-dataset"
REPO_URL="https://github.com/${ORG}/${REPO_NAME}.git"

echo "=========================================="
echo "推送到 GitHub 仓库"
echo "仓库: ${ORG}/${REPO_NAME}"
echo "=========================================="
echo ""

# 检查是否在正确的目录
if [ ! -f "setup.py" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查远程仓库是否已配置
if git remote | grep -q "^origin$"; then
    CURRENT_URL=$(git remote get-url origin)
    echo "当前远程仓库: ${CURRENT_URL}"
    
    if [ "${CURRENT_URL}" != "${REPO_URL}" ]; then
        echo "更新远程仓库URL..."
        git remote set-url origin "${REPO_URL}"
        echo "✅ 远程仓库URL已更新"
    else
        echo "✅ 远程仓库URL正确"
    fi
else
    echo "添加远程仓库..."
    git remote add origin "${REPO_URL}"
    echo "✅ 远程仓库已添加"
fi

echo ""
echo "推送代码到GitHub..."
echo "仓库URL: ${REPO_URL}"
echo ""

# 推送到main分支
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 推送成功！"
    echo "=========================================="
    echo ""
    echo "仓库地址: https://github.com/${ORG}/${REPO_NAME}"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo ""
    echo "可能的原因:"
    echo "1. GitHub仓库还未创建"
    echo "2. 没有推送权限"
    echo "3. 网络连接问题"
    echo ""
    echo "请先创建仓库:"
    echo "https://github.com/organizations/${ORG}/repositories/new"
    echo "仓库名: ${REPO_NAME}"
    echo "⚠️  不要初始化README、.gitignore或LICENSE"
    echo ""
fi

