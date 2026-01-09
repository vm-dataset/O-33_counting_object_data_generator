# 推送到 GitHub 仓库指南

## 仓库信息

- **仓库名称**: `O-33_counting_object_data-generator`
- **组织**: `vm-dataset`
- **完整URL**: `https://github.com/vm-dataset/O-33_counting_object_data-generator`

## 准备工作

### 1. 确保已清理临时文件

```bash
# 已自动清理以下内容：
# - __pycache__/
# - *.pyc
# - test_output_*/
# - *.mp4 (临时生成的视频)
```

### 2. 检查文件结构

确保以下文件存在：
- ✅ `.gitignore` - Git忽略文件配置
- ✅ `README.md` - 项目说明文档
- ✅ `LICENSE` - MIT许可证
- ✅ `requirements.txt` - 依赖列表
- ✅ `setup.py` - 安装配置
- ✅ `core/` - 核心框架代码（不要修改）
- ✅ `src/` - 任务实现代码
- ✅ `examples/generate.py` - 生成脚本

## 推送步骤

### 方法1: 通过GitHub CLI (推荐)

```bash
# 1. 初始化Git仓库（如果还没有）
cd -75-counting_objects_task-data-generator-main
git init

# 2. 添加所有文件
git add .

# 3. 提交
git commit -m "Initial commit: Counting Objects Task Data Generator"

# 4. 添加远程仓库（需要先在GitHub上创建仓库）
git remote add origin https://github.com/vm-dataset/O-33_counting_object_data-generator.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

### 方法2: 通过GitHub Web界面

1. **创建仓库**:
   - 访问 https://github.com/organizations/vm-dataset/repositories/new
   - 仓库名称: `O-33_counting_object_data-generator`
   - 描述: `Data generator for counting objects reasoning tasks for VMEvalKit`
   - 选择 Public 或 Private
   - **不要**初始化README、.gitignore或LICENSE（我们已经有了）

2. **推送代码**:
   ```bash
   cd -75-counting_objects_task-data-generator-main
   git init
   git add .
   git commit -m "Initial commit: Counting Objects Task Data Generator"
   git branch -M main
   git remote add origin https://github.com/vm-dataset/O-33_counting_object_data-generator.git
   git push -u origin main
   ```

### 方法3: 使用GitHub Desktop

1. 在GitHub Desktop中，点击 `File` -> `Add Local Repository`
2. 选择 `-75-counting_objects_task-data-generator-main` 目录
3. 点击 `Publish repository`
4. 选择组织 `vm-dataset`
5. 仓库名称: `O-33_counting_object_data-generator`
6. 点击 `Publish Repository`

## 验证

推送完成后，访问以下URL验证：

https://github.com/vm-dataset/O-33_counting_object_data-generator

## 后续更新

如果需要更新代码：

```bash
git add .
git commit -m "Update: [描述你的更改]"
git push origin main
```

## 注意事项

1. **不要提交生成的测试数据**: `.gitignore` 已配置忽略 `test_output_*/`, `*.mp4`, `__pycache__/` 等
2. **保护核心框架代码**: `core/` 目录是框架代码，不应该被修改
3. **遵循模板格式**: 确保代码遵循 `template-data-generator` 的格式规范

## 仓库设置建议

创建仓库后，建议在GitHub上设置：

1. **Topics**: 添加标签如 `vm-dataset`, `video-reasoning`, `data-generator`, `counting-objects`
2. **Description**: "Data generator for counting objects reasoning tasks for VMEvalKit"
3. **Website**: 可以链接到 VMEvalKit 主项目
4. **README预览**: 确保README.md在GitHub上正确显示

