"""
配置模块 - 读取 .env 文件中的所有配置
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

# 加载 .env 文件
load_dotenv(BASE_DIR / ".env")

# ── API Keys ──────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "").strip() or None
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SERVER_CHAN_KEY = os.getenv("SERVER_CHAN_KEY", "")

# ── 推送 & 分享 ───────────────────────────────────
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "").strip().rstrip("/")
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH", str(BASE_DIR))

# ── 目录 ──────────────────────────────────────────
OUTPUT_DIR   = BASE_DIR / "output"
DAILY_DIR    = OUTPUT_DIR / "daily"
WEEKLY_DIR   = OUTPUT_DIR / "weekly"
DATA_DIR     = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"
LOG_DIR      = BASE_DIR / "logs"

# 确保目录存在
for _d in [OUTPUT_DIR, DAILY_DIR, WEEKLY_DIR, DATA_DIR, LOG_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# ── Claude 模型 ───────────────────────────────────
CLAUDE_MODEL = "claude-opus-4-6"
