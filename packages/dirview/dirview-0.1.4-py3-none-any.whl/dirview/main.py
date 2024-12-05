import os
import argparse
import fnmatch
import json
from pathlib import Path
from typing import List, Optional, Set

CONFIG_FILE = '.dirviewrc'


class DirViewConfig:
    def __init__(self):
        self.default_exclude = {
            ".venv", ".git", "__pycache__", "node_modules",
            "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll"
        }
        self.default_include = {"*.py", "*.ipynb"}  # 默认只显示Python相关文件
        self.load_config()

    def load_config(self):
        """从配置文件加载设置"""
        config_path = Path.home() / CONFIG_FILE
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                    self.default_exclude = set(config.get('exclude', self.default_exclude))
                    self.default_include = set(config.get('include', self.default_include))
            except Exception as e:
                print(f"配置文件加载失败: {e}")


def should_exclude(name: str, path: Path, exclude_patterns: Set[str]) -> bool:
    """检查是否应该排除某个文件或目录"""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(str(path), pattern):
            return True
    return False


def should_include(name: str, include_patterns: Set[str]) -> bool:
    """检查文件是否应该包含"""
    # 如果没有指定包含模式，则包含所有文件
    if not include_patterns:
        return True
    return any(fnmatch.fnmatch(name, pattern) for pattern in include_patterns)


def print_tree(
        directory: Path,
        exclude_patterns: Set[str],
        include_patterns: Set[str],
        prefix: str = "",
        level: int = 0,
        max_level: Optional[int] = None,
        show_size: bool = False
) -> tuple[int, int, int]:
    """
    打印目录树结构并返回统计信息

    Returns:
        tuple: (目录数, 文件数, 总大小)
    """
    if max_level is not None and level > max_level:
        return 0, 0, 0

    try:
        entries = list(directory.iterdir())
    except PermissionError:
        print(f"{prefix}[访问被拒绝]")
        return 0, 0, 0
    except FileNotFoundError:
        print(f"错误: 目录 '{directory}' 不存在")
        return 0, 0, 0

    entries.sort(key=lambda x: x.name.lower())
    dirs = []
    files = []

    # 分类文件和目录
    for entry in entries:
        if should_exclude(entry.name, entry, exclude_patterns):
            continue
        if entry.is_dir():
            dirs.append(entry)
        elif entry.is_file() and should_include(entry.name, include_patterns):
            files.append(entry)

    total_dirs = len(dirs)
    total_files = len(files)
    total_size = 0

    # 处理目录
    for i, entry in enumerate(dirs):
        is_last = (i == len(dirs) - 1 and len(files) == 0)
        branch = "└──" if is_last else "├──"
        new_prefix = prefix + "    " if is_last else prefix + "│   "

        print(f"{prefix}{branch} 📁 {entry.name}/")
        sub_dirs, sub_files, sub_size = print_tree(
            entry, exclude_patterns, include_patterns,
            new_prefix, level + 1, max_level, show_size
        )
        total_dirs += sub_dirs
        total_files += sub_files
        total_size += sub_size

    # 处理文件
    for i, entry in enumerate(files):
        is_last = (i == len(files) - 1)
        branch = "└──" if is_last else "├──"
        size = entry.stat().st_size
        total_size += size

        size_info = f" ({format_size(size)})" if show_size else ""
        print(f"{prefix}{branch} 📄 {entry.name}{size_info}")

    return total_dirs, total_files, total_size


def format_size(size: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def main():
    config = DirViewConfig()

    parser = argparse.ArgumentParser(description="显示目录树结构")
    parser.add_argument('path', nargs='?', default='.', help='要显示的目录路径')
    parser.add_argument('-e', '--exclude', nargs='+', help='要排除的文件或目录模式（追加到默认排除规则）')
    parser.add_argument('-i', '--include', nargs='+', help='要包含的文件模式')
    parser.add_argument('-L', '--level', type=int, help='最大显示深度')
    parser.add_argument('-s', '--size', action='store_true', help='显示文件大小')
    parser.add_argument('--no-default-exclude', action='store_true',
                        help='不使用默认排除规则')
    parser.add_argument('--version', action='store_true', help='显示版本信息')

    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"DirView version {__version__}")
        return

    # 处理排除和包含规则
    exclude_patterns = set()
    if not args.no_default_exclude:
        exclude_patterns.update(config.default_exclude)  # 首先添加默认排除规则
    if args.exclude:
        exclude_patterns.update(args.exclude)  # 追加用户指定的排除规则

    include_patterns = set(args.include) if args.include else config.default_include

    # 打印当前使用的排除规则（可选，用于调试）
    print("当前排除规则:", sorted(exclude_patterns))

    directory = Path(args.path).absolute()
    print(f"目录树 for {directory}")
    print("=" * 50)

    total_dirs, total_files, total_size = print_tree(
        directory,
        exclude_patterns,
        include_patterns,
        max_level=args.level,
        show_size=args.size
    )

    print("\n统计信息:")
    print(f"目录数: {total_dirs}")
    print(f"文件数: {total_files}")
    if args.size:
        print(f"总大小: {format_size(total_size)}")


if __name__ == "__main__":
    main()
