"""
AI 内容处理模块 - 调用 Claude API 对原始新闻进行筛选、摘要、结构化
"""
import json
import logging
import re
from datetime import datetime

import anthropic

from config import ANTHROPIC_API_KEY, ANTHROPIC_BASE_URL, CLAUDE_MODEL

logger = logging.getLogger(__name__)


def _get_client() -> anthropic.Anthropic:
    kwargs = {"api_key": ANTHROPIC_API_KEY}
    if ANTHROPIC_BASE_URL:
        kwargs["base_url"] = ANTHROPIC_BASE_URL
    return anthropic.Anthropic(**kwargs)


def _extract_json(text: str) -> dict:
    """从 Claude 回复中提取 JSON，多重容错策略"""
    text = text.strip()

    # 1. 去掉 ```json ... ``` 包裹
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    if match:
        text = match.group(1).strip()

    # 2. 提取最外层 { ... }
    brace = re.search(r"\{[\s\S]+\}", text)
    if brace:
        text = brace.group(0)

    # 3. 清理常见格式问题
    # 替换中文全角逗号/冒号
    text = text.replace("，", ",").replace("：", ":")
    # 去掉尾随逗号（JSON 不允许）
    text = re.sub(r",\s*([}\]])", r"\1", text)
    # 去掉控制字符（换行除外）
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    # 4. 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 5. 最后尝试：修复字符串内的非法换行
    text = re.sub(r'(?<=: ")(.*?)(?=")', lambda m: m.group(0).replace("\n", " "), text, flags=re.DOTALL)
    return json.loads(text)


def _call_claude(prompt: str, max_tokens: int = 2000) -> str:
    client = _get_client()
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system="你必须只输出合法的 JSON，不要输出任何其他内容。不要使用中文标点，JSON 字符串内只用英文标点。",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


# ─────────────────────────────────────────────────────────
# 日报 - 中美 AI 行业新闻
# ─────────────────────────────────────────────────────────
def process_main_news(raw: dict) -> dict:
    today = datetime.now().strftime("%Y年%m月%d日")

    cn_text = "\n".join(
        f"- 标题: {r.get('title','')}\n  内容: {r.get('content','')[:350]}"
        for r in raw.get("china_ai", [])
    )
    us_text = "\n".join(
        f"- Title: {r.get('title','')}\n  Content: {r.get('content','')[:350]}"
        for r in raw.get("us_ai", [])
    )

    prompt = f"""你是一位专业的AI行业编辑，负责制作每日简报。今天是 {today}。

请从以下原始新闻中，筛选最重要的条目并整理成日报。

要求：
- 中国AI新闻：选 3~4 条，每条写 60~80 字摘要
- 美国AI新闻：选 3~4 条，每条写 60~80 字摘要（标题翻译为中文）
- 优先选择有实质内容的新闻（产品发布、重大融资、政策、突破性技术）
- 摘要客观简洁，说明事件本质和行业影响
- 如原始新闻中有重复或低质量内容，直接跳过

=== 中国AI原始新闻 ===
{cn_text}

=== 美国AI原始新闻 ===
{us_text}

严格按以下 JSON 格式输出，不要输出任何其他内容：
{{
  "date": "{today}",
  "china_news": [
    {{"title": "标题", "summary": "摘要", "source": "来源媒体名"}}
  ],
  "us_news": [
    {{"title": "中文标题", "summary": "摘要", "source": "来源媒体名"}}
  ]
}}"""

    try:
        result = _extract_json(_call_claude(prompt, max_tokens=2500))
        result.setdefault("date", today)
        result.setdefault("china_news", [])
        result.setdefault("us_news", [])
        logger.info(f"日报主报处理完成：中国{len(result['china_news'])}条，美国{len(result['us_news'])}条")
        return result
    except Exception as e:
        logger.error(f"处理主报新闻失败: {e}")
        return {"date": today, "china_news": [], "us_news": [], "error": str(e)}


# ─────────────────────────────────────────────────────────
# 日报 - 时尚/零售 AI 专项
# ─────────────────────────────────────────────────────────
def process_fashion_news(raw: dict) -> dict:
    today = datetime.now().strftime("%Y年%m月%d日")

    fashion_text = "\n".join(
        f"- 标题: {r.get('title','')}\n  内容: {r.get('content','')[:400]}\n  来源: {r.get('url','')}"
        for r in raw.get("fashion_ai", [])
    )

    prompt = f"""你是时尚零售行业的AI应用专家编辑。今天是 {today}。

请从以下新闻中整理时尚/零售行业 AI 应用动态。

要求：
- 选 4~5 条最有行业价值的新闻
- 每条写 70~100 字摘要，重点说明：AI 如何被应用、哪个品牌/公司、对行业的影响
- 方向涵盖：AI 设计、智能供应链、个性化推荐、虚拟试穿/试妆、智能客服、趋势预测等
- 若原始新闻不足，可补充近期重要的行业 AI 应用事件

=== 原始新闻 ===
{fashion_text}

严格按以下 JSON 格式输出，不要输出其他内容：
{{
  "date": "{today}",
  "fashion_news": [
    {{"title": "标题", "summary": "摘要", "category": "AI设计/供应链/个性化/虚拟试穿/趋势预测等", "source": "来源"}}
  ]
}}"""

    try:
        result = _extract_json(_call_claude(prompt, max_tokens=2000))
        result.setdefault("date", today)
        result.setdefault("fashion_news", [])
        logger.info(f"时尚日报处理完成：{len(result['fashion_news'])}条")
        return result
    except Exception as e:
        logger.error(f"处理时尚新闻失败: {e}")
        return {"date": today, "fashion_news": [], "error": str(e)}


# ─────────────────────────────────────────────────────────
# 周报汇总
# ─────────────────────────────────────────────────────────
def process_weekly_summary(week_cache: dict) -> dict:
    """将一周的缓存新闻汇总成30条精选周报"""
    today = datetime.now().strftime("%Y年%m月%d日")

    # 整理所有新闻
    all_main, all_fashion = [], []
    for date_str, day_data in week_cache.items():
        main = day_data.get("main", {})
        all_main.extend(
            [f"[{date_str}] {n['title']}：{n['summary']}" for n in main.get("china_news", [])]
        )
        all_main.extend(
            [f"[{date_str}] {n['title']}：{n['summary']}" for n in main.get("us_news", [])]
        )
        fashion = day_data.get("fashion", {})
        all_fashion.extend(
            [f"[{date_str}] 【{n.get('category','')}】{n['title']}：{n['summary']}"
             for n in fashion.get("fashion_news", [])]
        )

    main_text    = "\n".join(all_main)
    fashion_text = "\n".join(all_fashion)

    # 周报起止日期
    dates = sorted(week_cache.keys())
    week_start = dates[0] if dates else ""
    week_end   = dates[-1] if dates else today

    prompt = f"""你是AI行业资深编辑，负责制作每周精选周报。本周（{week_start} ~ {week_end}）。

请从本周所有日报中精选最重要、最有价值的新闻，组成周报。

要求：
- 中美AI行业：各选 10~12 条本周最重要新闻，去重并提炼，每条 80~120 字
- 时尚零售AI：选 6~8 条本周最值得关注的应用案例，每条 80~120 字
- 总条数控制在 28~32 条
- 突出本周最重大的行业趋势和事件
- 每个板块最后加一句"本周小结"（50字内）

=== 本周中美AI新闻汇总 ===
{main_text}

=== 本周时尚零售AI新闻汇总 ===
{fashion_text}

严格按以下 JSON 格式输出：
{{
  "week_range": "{week_start} ~ {week_end}",
  "china_news": [
    {{"title": "标题", "summary": "摘要"}}
  ],
  "us_news": [
    {{"title": "标题", "summary": "摘要"}}
  ],
  "fashion_news": [
    {{"title": "标题", "summary": "摘要", "category": "类别"}}
  ],
  "china_summary": "中国AI本周小结",
  "us_summary": "美国AI本周小结",
  "fashion_summary": "时尚零售AI本周小结"
}}"""

    try:
        result = _extract_json(_call_claude(prompt, max_tokens=5000))
        logger.info(
            f"周报处理完成：中国{len(result.get('china_news',[]))}条，"
            f"美国{len(result.get('us_news',[]))}条，"
            f"时尚{len(result.get('fashion_news',[]))}条"
        )
        return result
    except Exception as e:
        logger.error(f"处理周报失败: {e}")
        return {"week_range": f"{week_start} ~ {week_end}", "error": str(e)}
