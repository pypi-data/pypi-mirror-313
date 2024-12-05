# DirTree

一个简单易用的目录树显示工具。

## 功能特点

- 显示目录的树形结构
- 支持排除指定目录
- 可以限制显示深度
- 可以显示文件大小
- 支持彩色输出和文件/文件夹图标
- 显示统计信息（目录数、文件数、总大小）

## 安装

```shell
pip install dirview
```

## 使用方法

基本用法:

```bash
dirtree [路径] [选项]
```

### 选项说明:

- -h, --help: 显示帮助信息
- -e, --exclude: 要排除的目录列表 (例如: -e node_modules .git)
- -L, --level: 最大显示深度 (例如: -L 2)
- -s, --size: 显示文件大小
- --version: 显示版本信息

### 使用示例:

```bash
# 显示当前目录的树结构
dirtree

# 显示指定目录的树结构
dirtree /path/to/directory

# 显示当前目录的树结构及文件大小
dirtree -s

# 只显示两层深度的目录结构
dirtree -L 2

# 排除指定目录
dirtree -e .git node_modules
```

### 输出示例:

```makefile
目录树 for /your/project/path
==================================================
├── 📁 src/
│   ├── 📄 main.py
│   └── 📄 __init__.py
├── 📄 README.md
└── 📄 pyproject.toml

统计信息:
目录数: 1
文件数: 3
总大小: 2.5KB
```

## 默认排除的目录

工具默认会排除以下目录:

- .git
- __pycache__
- node_modules
- langchain-env

## 许可证

MIT License

## 作者

陈定钢 ([945036663@qq.com](mailto:945036663@qq.com))

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新历史

### 0.1.1

- 初始发布
- 实现基本的目录树显示功能
- 添加文件大小显示功能
- 添加目录排除功能
- 添加深度限制功能