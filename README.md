# 晨脉 AI×Radar

> 每日自动生成 AI 行业情报 + 时尚零售 AI 应用专报，发布到 GitHub Pages，微信推送通知。

**[查看示例日报 →](https://wangjia3119.github.io/ai-daily-report/)**

---

## 功能特性

- **今日 AI 日报** — 中国 AI + 美国 AI 行业热点，每日精选 6~8 条，附 60~80 字摘要
- **时尚专报** — AI 在时尚/零售行业的应用动态，独立生成
- **AI 行业周报** — 每周五自动汇总本周精选 30 条，含各板块小结
- **自动推送** — GitHub Pages 公开发布 + Server酱微信通知
- **零人工干预** — Windows 任务计划程序定时运行，全程自动化

## 技术栈

| 组件 | 说明 |
|------|------|
| [Tavily API](https://tavily.com) | 新闻搜索抓取 |
| [Claude API](https://anthropic.com) | 内容筛选与摘要生成 |
| [Jinja2](https://jinja.palletsprojects.com) | HTML 模板渲染 |
| [GitHub Pages](https://pages.github.com) | 免费静态站点托管 |
| [Server酱](https://sct.ftqq.com) | 微信推送通知 |
| Windows Task Scheduler | 定时自动运行 |

## 目录结构

```
ai-daily-report/
├── main.py              # 主入口（daily / weekly 两种模式）
├── fetch_news.py        # Tavily 新闻抓取
├── process_news.py      # Claude 内容处理与摘要
├── render_html.py       # Jinja2 HTML 渲染
├── cache.py             # 每日新闻缓存（供周报汇总）
├── notify.py            # Server酱微信推送
├── git_push.py          # GitHub API 文件上传（适配 GFW 环境）
├── config.py            # 配置读取
├── templates/
│   ├── daily_main.html    # 今日 AI 日报模板
│   ├── daily_fashion.html # 时尚专报模板
│   └── weekly.html        # 周报模板
├── docs/                # 生成的 HTML（GitHub Pages 服务目录）
│   ├── index.html
│   ├── daily/
│   └── weekly/
├── data/
│   └── news_cache.json  # 缓存文件（.gitignore 忽略）
├── .env.example         # 配置模板
├── setup.bat            # 一键安装脚本
└── setup_scheduler.bat  # Windows 定时任务配置
```

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/wangjia3119/ai-daily-report.git
cd ai-daily-report
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

或直接运行安装脚本：

```bat
setup.bat
```

### 3. 配置 API Keys

复制配置模板并填写：

```bash
cp .env.example .env
```

编辑 `.env`：

```env
# 必填
ANTHROPIC_API_KEY=sk-ant-...        # Claude API Key
TAVILY_API_KEY=tvly-...             # Tavily API Key（免费 1000次/月）

# 推荐
SERVER_CHAN_KEY=SCT...               # Server酱 微信推送 Key

# 可选（配置后推送通知含链接）
GITHUB_PAGES_URL=https://yourname.github.io/ai-daily-report
GITHUB_TOKEN=ghp_...                # 用于自动推送 HTML 到 GitHub
GITHUB_OWNER=yourname
GITHUB_REPO=ai-daily-report
```

**API Key 申请地址：**

| 服务 | 地址 | 费用 |
|------|------|------|
| Claude | https://console.anthropic.com | 按量计费，每日约 ¥0.3~0.8 |
| Tavily | https://app.tavily.com | 免费 1000次/月 |
| Server酱 | https://sct.ftqq.com | 免费 |

### 4. 手动运行测试

```bash
# 生成今日日报
python main.py daily

# 生成本周周报
python main.py weekly
```

### 5. 配置定时任务（Windows）

以管理员身份运行：

```bat
setup_scheduler.bat
```

自动创建：
- **AI-Daily** — 周一至周四 08:00 生成日报
- **AI-Weekly** — 周五 08:00 生成周报

### 6. 配置 GitHub Pages（公开分享）

1. Fork 本仓库
2. 进入仓库 **Settings → Pages**
3. Source 选择 `main` 分支，目录选 `/docs`
4. 将生成的 Pages URL 填入 `.env` 的 `GITHUB_PAGES_URL`

---

## 自定义

### 修改新闻搜索关键词

编辑 `fetch_news.py` 中的搜索 query：

```python
# 中国 AI 新闻
"中国AI人工智能 大模型 最新动态 {today_cn}"

# 美国 AI 新闻
"OpenAI Google DeepMind Meta AI artificial intelligence news {today_en}"

# 时尚/零售 AI（可改为你关注的行业）
"AI fashion retail luxury brand technology application"
```

### 修改每日条数

编辑 `process_news.py` 中的 Prompt，调整"选 X~X 条"的数字即可。

### 修改页面样式

编辑 `templates/` 下的 HTML 文件，基于原生 CSS + Jinja2 模板，无需构建工具。

---

## 代理说明（中国大陆）

本项目默认通过 GitHub API 上传文件（`git_push.py`），**无需 git push**，适配 GFW 环境下 HTTPS git 连接不稳定的情况。

Claude API 如使用中转代理，在 `.env` 中配置：

```env
ANTHROPIC_BASE_URL=https://你的代理地址
```

---

## License

[MIT](LICENSE) © 2026 wangjia3119
