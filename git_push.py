"""
GitHub 推送模块 - 通过 GitHub API 上传文件（替代 git push，兼容 GFW 环境）
"""
import base64
import logging
import os
from pathlib import Path

import requests

from config import BASE_DIR, DATA_DIR

logger = logging.getLogger(__name__)

SKIP_NAMES = {".env", "news_cache.json", "run.log"}
SKIP_DIRS  = {"__pycache__", "logs", ".git", "output"}


def _get_cfg():
    from config import GITHUB_PAGES_URL
    token = os.getenv("GITHUB_TOKEN", "")
    owner = os.getenv("GITHUB_OWNER", "")
    repo  = os.getenv("GITHUB_REPO", "")
    return token, owner, repo


def _headers(token):
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def _upload_file(token: str, owner: str, repo: str, rel_path: str, file_path: Path) -> bool:
    """上传单个文件到 GitHub"""
    hdrs = _headers(token)
    api  = f"https://api.github.com/repos/{owner}/{repo}/contents/{rel_path}"

    try:
        content = base64.b64encode(file_path.read_bytes()).decode()
    except Exception as e:
        logger.warning(f"读取文件失败 {rel_path}: {e}")
        return False

    # 获取已有文件的 sha（更新时必须）
    r = requests.get(api, headers=hdrs, timeout=15)
    sha = r.json().get("sha") if r.status_code == 200 else None

    payload = {"message": f"auto: update {rel_path}", "content": content}
    if sha:
        payload["sha"] = sha

    r2 = requests.put(api, headers=hdrs, json=payload, timeout=30)
    if r2.status_code in (200, 201):
        return True
    else:
        logger.error(f"上传失败 {rel_path}: {r2.json().get('message','')}")
        return False


def push_docs(commit_msg: str = "auto: 更新日报") -> bool:
    """将 docs/ 目录推送到 GitHub（通过 API，不依赖 git）"""
    token, owner, repo = _get_cfg()
    if not all([token, owner, repo]):
        logger.warning("GitHub Token/Owner/Repo 未配置，跳过推送")
        return False

    docs_dir = BASE_DIR / "docs"
    if not docs_dir.exists():
        logger.warning("docs/ 目录不存在")
        return False

    files = [f for f in docs_dir.rglob("*") if f.is_file()]
    ok = err = 0
    for f in files:
        rel = f.relative_to(BASE_DIR).as_posix()
        if _upload_file(token, owner, repo, rel, f):
            ok += 1
        else:
            err += 1

    logger.info(f"GitHub 推送完成: 成功 {ok} 个，失败 {err} 个")
    return err == 0
