"""
check_env.py - 开课前环境自检脚本
用法：在项目根目录下执行
    uv run python check_env.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

OK = "✅"
FAIL = "❌"

fail_count = 0


def check(passed: bool, name: str, detail: str = "") -> None:
    global fail_count
    mark = OK if passed else FAIL
    print(f"{mark} {name}" + (f" — {detail}" if detail else ""))
    if not passed:
        fail_count += 1


def display_path(path: str) -> str:
    """Display a path as repo-name/relative-path when possible."""

    try:
        cwd = Path.cwd().resolve()
        relative = Path(path).resolve().relative_to(cwd)
        return str(Path(cwd.name) / relative)
    except ValueError:
        return path


load_dotenv()

# 1. Python 版本（需要 3.11 或 3.12）
major, minor = sys.version_info[:2]
ver = f"{major}.{minor}.{sys.version_info.micro}"
check(
    (major, minor) in {(3, 11), (3, 12)},
    "Python 版本",
    f"{ver}" if (major, minor) in {(3, 11), (3, 12)} else f"{ver}（请装 3.11 或 3.12）",
)

# 2. uv 是否可用
uv_path = shutil.which("uv")
if not uv_path:
    local_uv = Path.home() / ".local" / "bin" / "uv"
    if local_uv.exists():
        uv_path = str(local_uv)

if uv_path:
    try:
        out = subprocess.check_output([uv_path, "--version"], text=True).strip()
        check(True, "uv", out)
    except Exception as e:
        check(False, "uv", f"找到但调用失败：{e}")
else:
    check(False, "uv", "未安装，请参考第 2 节")

# 3. 是否在虚拟环境里
in_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
check(
    in_venv,
    "虚拟环境",
    display_path(sys.prefix) if in_venv else "当前不在 venv 里，请用 uv run python check_env.py",
)

# 4. API Key（OpenAI 和 Anthropic 至少有一个）
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
has_key = bool(openai_key or anthropic_key)
found = [
    name
    for name, val in [("OPENAI_API_KEY", openai_key), ("ANTHROPIC_API_KEY", anthropic_key)]
    if val
]
check(
    has_key,
    "API Key",
    f"已检测到：{', '.join(found)}" if has_key else "未检测到任何 API Key",
)

# 5. OPENAI_BASE_URL（可选；如果设置，必须是完整 URL）
base_url = os.getenv("OPENAI_BASE_URL")
if base_url is not None:
    parsed = urlparse(base_url)
    valid_base_url = parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    check(
        valid_base_url,
        "OPENAI_BASE_URL",
        base_url if valid_base_url else "如果设置，必须以 http:// 或 https:// 开头；不用时请删除这一行",
    )

# 总结
print("\n" + "=" * 40)
if fail_count == 0:
    print("🎉 环境检查全部通过，可以开课了！")
else:
    print(f"{FAIL} 有 {fail_count} 项未通过，请按提示修复后重新运行。")
    sys.exit(1)
