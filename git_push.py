"""
Git 自动推送模块 - 生成文件后推送到 GitHub
"""
import logging
import subprocess
from pathlib import Path
from config import GIT_REPO_PATH

logger = logging.getLogger(__name__)


def _run(cmd: list, cwd: str) -> tuple[int, str]:
    result = subprocess.run(
        cmd, cwd=cwd,
        capture_output=True, text=True, encoding="utf-8"
    )
    return result.returncode, result.stdout + result.stderr


def git_push(commit_msg: str = "auto: 更新日报") -> bool:
    """将 output/ 目录的变更提交并推送到 GitHub"""
    repo = GIT_REPO_PATH
    if not repo or not Path(repo).exists():
        logger.warning("GIT_REPO_PATH 未配置或不存在，跳过 Git 推送")
        return False

    steps = [
        (["git", "add", "docs/", "data/"], "git add"),
        (["git", "commit", "-m", commit_msg], "git commit"),
        (["git", "push"], "git push"),
    ]

    for cmd, label in steps:
        code, out = _run(cmd, repo)
        if code != 0 and "nothing to commit" not in out:
            logger.error(f"{label} 失败:\n{out}")
            # commit 没变化时继续 push
            if label != "git commit":
                return False
        else:
            logger.info(f"{label} 成功")

    return True
