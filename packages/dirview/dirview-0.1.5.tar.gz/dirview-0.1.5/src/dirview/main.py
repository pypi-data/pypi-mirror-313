import os
import argparse
import fnmatch
import json
from pathlib import Path
from typing import List, Optional, Set, Dict
from datetime import datetime
import concurrent.futures
from colorama import init, Fore, Style

# 初始化 colorama
init()

CONFIG_FILE = '.dirviewrc'

# 文件类型图标映射
FILE_ICONS = {
    # 开发文件
    '.py': '🐍',
    '.js': '📜',
    '.ts': '📜',
    '.html': '🌐',
    '.css': '🎨',
    '.json': '📋',
    '.yml': '📋',
    '.yaml': '📋',
    '.xml': '📋',
    '.md': '📝',
    '.rst': '📝',

    # 文档文件
    '.txt': '📄',
    '.pdf': '📑',
    '.doc': '📘',
    '.docx': '📘',
    '.xls': '📊',
    '.xlsx': '📊',
    '.ppt': '📽️',
    '.pptx': '📽️',

    # 多媒体文件
    '.jpg': '🖼️',
    '.jpeg': '🖼️',
    '.png': '🖼️',
    '.gif': '🖼️',
    '.mp4': '🎥',
    '.mov': '🎥',
    '.mp3': '🎵',
    '.wav': '🎵',

    # 压缩文件
    '.zip': '📦',
    '.rar': '📦',
    '.7z': '📦',
    '.tar': '📦',
    '.gz': '📦',

    # 配置文件
    '.env': '⚙️',
    '.ini': '⚙️',
    '.cfg': '⚙️',
    '.conf': '⚙️',

    # 默认图标
    'default_file': '📄',
    'default_dir': '📁',
    'error_dir': '⚠️',
}


class Colors:
    DIR = Fore.BLUE
    FILE = Fore.WHITE
    PYTHON = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    STATS = Fore.CYAN
    RESET = Style.RESET_ALL


class DirViewConfig:
    def __init__(self):
        self.default_exclude = {
            ".venv", ".git", "__pycache__", "node_modules",
            "*.pyc", "*.pyo", "*.pyd", "*.so", "*.dll", "*.idea",
            ".DS_Store", "*.swp", "*.swo", "*.swn",
            "*.log", "*.tmp", "*.temp"
        }
        self.default_include = set()  # 默认显示所有文件
        self.load_config()

    def load_config(self):
        """从配置文件加载设置"""
        # 按优先级检查多个配置文件位置
        config_locations = [
            Path.cwd() / CONFIG_FILE,  # 当前目录
            Path.home() / CONFIG_FILE,  # 用户主目录
            Path.home() / '.config' / 'dirview' / CONFIG_FILE  # XDG 配置目录
        ]

        for config_path in config_locations:
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        config = json.load(f)
                        self.default_exclude = set(config.get('exclude', self.default_exclude))
                        self.default_include = set(config.get('include', self.default_include))
                        return
                except Exception as e:
                    print(f"{Colors.WARNING}警告: 配置文件 {config_path} 加载失败: {e}{Colors.RESET}")


def get_file_icon(path: Path) -> str:
    """获取文件图标"""
    if path.is_dir():
        return FILE_ICONS['default_dir']
    return FILE_ICONS.get(path.suffix.lower(), FILE_ICONS['default_file'])


def should_exclude(name: str, path: Path, exclude_patterns: Set[str]) -> bool:
    """检查是否应该排除某个文件或目录"""
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(str(path), pattern):
            return True
    return False


def should_include(name: str, include_patterns: Set[str]) -> bool:
    """检查文件是否应该包含"""
    if not include_patterns:
        return True
    return any(fnmatch.fnmatch(name, pattern) for pattern in include_patterns)


def scan_directory(directory: Path, exclude_patterns: Set[str], include_patterns: Set[str]) -> List[Path]:
    """并行扫描目录"""
    results = []
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for entry in directory.iterdir():
                if not should_exclude(entry.name, entry, exclude_patterns):
                    if entry.is_file() and should_include(entry.name, include_patterns):
                        results.append(entry)
                    elif entry.is_dir():
                        futures.append(executor.submit(
                            scan_directory, entry, exclude_patterns, include_patterns
                        ))

            for future in concurrent.futures.as_completed(futures):
                try:
                    results.extend(future.result())
                except Exception as e:
                    print(f"{Colors.ERROR}错误: 扫描目录时发生错误: {e}{Colors.RESET}")
    except PermissionError:
        print(f"{Colors.ERROR}错误: 访问目录 '{directory}' 被拒绝{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.ERROR}错误: 扫描目录 '{directory}' 时发生错误: {e}{Colors.RESET}")

    return results


def print_tree(
        directory: Path,
        exclude_patterns: Set[str],
        include_patterns: Set[str],
        prefix: str = "",
        level: int = 0,
        max_level: Optional[int] = None,
        show_size: bool = False
) -> tuple[int, int, int]:
    """打印目录树结构并返回统计信息"""
    if max_level is not None and level > max_level:
        return 0, 0, 0

    try:
        entries = list(directory.iterdir())
    except PermissionError:
        print(f"{prefix}{Colors.ERROR}[访问被拒绝]{Colors.RESET}")
        return 0, 0, 0
    except FileNotFoundError:
        print(f"{Colors.ERROR}错误: 目录 '{directory}' 不存在{Colors.RESET}")
        return 0, 0, 0

    entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
    total_dirs = total_files = total_size = 0

    for i, entry in enumerate(entries):
        if should_exclude(entry.name, entry, exclude_patterns):
            continue

        is_last = (i == len(entries) - 1)
        branch = "└──" if is_last else "├──"
        new_prefix = prefix + "    " if is_last else prefix + "│   "

        if entry.is_dir():
            print(f"{prefix}{branch} {Colors.DIR}{get_file_icon(entry)} {entry.name}/{Colors.RESET}")
            sub_dirs, sub_files, sub_size = print_tree(
                entry, exclude_patterns, include_patterns,
                new_prefix, level + 1, max_level, show_size
            )
            total_dirs += 1 + sub_dirs
            total_files += sub_files
            total_size += sub_size
        elif should_include(entry.name, include_patterns):
            try:
                size = entry.stat().st_size
                total_size += size
                size_info = f" ({format_size(size)})" if show_size else ""

                # 根据文件类型使用不同的颜色
                color = Colors.PYTHON if entry.suffix == '.py' else Colors.FILE
                print(f"{prefix}{branch} {color}{get_file_icon(entry)} {entry.name}{size_info}{Colors.RESET}")
                total_files += 1
            except (PermissionError, FileNotFoundError):
                print(f"{prefix}{branch} {Colors.ERROR}[无法访问] {entry.name}{Colors.RESET}")

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
    parser.add_argument('--no-color', action='store_true',
                        help='禁用颜色输出')
    parser.add_argument('--version', action='store_true', help='显示版本信息')

    args = parser.parse_args()

    if args.no_color:
        # 禁用颜色
        for key in dir(Colors):
            if not key.startswith('__'):
                setattr(Colors, key, '')

    if args.version:
        from . import __version__
        print(f"DirView version {__version__}")
        return

    # 处理排除和包含规则
    exclude_patterns = set()
    if not args.no_default_exclude:
        exclude_patterns.update(config.default_exclude)
    if args.exclude:
        exclude_patterns.update(args.exclude)

    include_patterns = set(args.include) if args.include else config.default_include

    directory = Path(args.path).absolute()
    print(f"\n{Colors.STATS}目录树 for {directory}{Colors.RESET}")
    print("=" * 50)

    start_time = datetime.now()
    total_dirs, total_files, total_size = print_tree(
        directory,
        exclude_patterns,
        include_patterns,
        max_level=args.level,
        show_size=args.size
    )
    end_time = datetime.now()

    print(f"\n{Colors.STATS}统计信息:{Colors.RESET}")
    print(f"目录数: {total_dirs}")
    print(f"文件数: {total_files}")
    if args.size:
        print(f"总大小: {format_size(total_size)}")
    print(f"扫描时间: {(end_time - start_time).total_seconds():.2f}秒")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}操作被用户中断{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}发生错误: {e}{Colors.RESET}")
