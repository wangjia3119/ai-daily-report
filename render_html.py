"""
HTML 渲染模块 - 使用 Jinja2 将结构化数据渲染为 HTML 文件
"""
import logging
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from config import TEMPLATE_DIR, DAILY_DIR, WEEKLY_DIR, GITHUB_PAGES_URL

logger = logging.getLogger(__name__)

_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))


def render_daily_main(data: dict) -> Path:
    """渲染中美AI日报 → output/daily/YYYY-MM-DD.html"""
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = DAILY_DIR / f"{today}.html"

    tpl = _env.get_template("daily_main.html")
    html = tpl.render(
        data=data,
        github_url=GITHUB_PAGES_URL or None,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    out_path.write_text(html, encoding="utf-8")
    logger.info(f"日报主报已保存: {out_path}")
    return out_path


def render_daily_fashion(data: dict) -> Path:
    """渲染时尚AI日报 → output/daily/YYYY-MM-DD-fashion.html"""
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = DAILY_DIR / f"{today}-fashion.html"

    tpl = _env.get_template("daily_fashion.html")
    html = tpl.render(
        data=data,
        github_url=GITHUB_PAGES_URL or None,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    out_path.write_text(html, encoding="utf-8")
    logger.info(f"时尚日报已保存: {out_path}")
    return out_path


def render_weekly(data: dict) -> Path:
    """渲染周报 → output/weekly/YYYY-WNN.html"""
    iso = datetime.now().isocalendar()
    filename = f"{iso.year}-W{iso.week:02d}.html"
    out_path = WEEKLY_DIR / filename

    tpl = _env.get_template("weekly.html")
    html = tpl.render(
        data=data,
        github_url=GITHUB_PAGES_URL or None,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
    )
    out_path.write_text(html, encoding="utf-8")
    logger.info(f"周报已保存: {out_path}")
    return out_path


def render_index(all_reports: list) -> Path:
    """渲染首页索引 → output/index.html"""
    # 使用内嵌模板（不单独建文件）
    rows = ""
    for r in all_reports:
        rows += f"""
        <tr>
          <td><a href="{r['url_main']}">{r['date']} 日报</a></td>
          <td><a href="{r['url_fashion']}">时尚专报</a></td>
          <td>{r.get('weekly_url', '—')}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 日报 · 往期归档</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:"PingFang SC","Microsoft YaHei",sans-serif;
       background:#f7f8fc; padding:32px 20px; color:#2d3748; }}
.wrapper {{ max-width:800px; margin:0 auto; }}
h1 {{ font-size:24px; font-weight:800; margin-bottom:6px; }}
p {{ color:#718096; font-size:14px; margin-bottom:28px; }}
table {{ width:100%; border-collapse:collapse; background:#fff;
        border-radius:12px; overflow:hidden;
        box-shadow:0 1px 6px rgba(0,0,0,.07); }}
th {{ background:#2d3748; color:#fff; padding:12px 18px;
     text-align:left; font-size:13px; }}
td {{ padding:12px 18px; border-bottom:1px solid #e2e8f0;
     font-size:14px; }}
tr:last-child td {{ border-bottom:none; }}
a {{ color:#2b6cb0; text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
</style>
</head>
<body>
<div class="wrapper">
  <h1>AI 日报 · 往期归档</h1>
  <p>每日自动生成，每周五汇总周报。由 Claude + Tavily 驱动。</p>
  <table>
    <thead><tr><th>AI 行业日报</th><th>时尚零售专报</th><th>周报</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
</body>
</html>"""

    out_path = Path(DAILY_DIR).parent / "index.html"
    out_path.write_text(html, encoding="utf-8")
    logger.info(f"首页索引已更新: {out_path}")
    return out_path
