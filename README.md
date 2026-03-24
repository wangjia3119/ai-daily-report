# AI 日报自动化系统

每日自动抓取中美AI行业热点 + 时尚零售AI应用动态，生成精美HTML日报，推送到微信并发布到 GitHub Pages。

---

## 功能

| 报告类型 | 内容 | 触发时间 |
|----------|------|---------|
| AI 行业日报 | 中国AI 3-4条 + 美国AI 3-4条 | 周一至周四 08:00 |
| 时尚零售专报 | 时尚/零售AI应用 4-5条 | 同上 |
| AI 行业周报 | 精选30条 + 三大板块小结 | 周五 08:00 |

---

## 快速开始

### 第一步：安装

```bash
# 双击运行（或在终端执行）
setup.bat
```

### 第二步：填写 API Keys

用记事本打开 `.env` 文件：

```env
# 必填
ANTHROPIC_API_KEY=你的Claude_API_Key
TAVILY_API_KEY=你的Tavily_API_Key

# 推荐填写（微信推送）
SERVER_CHAN_KEY=你的Server酱SendKey

# 可选（GitHub Pages 分享链接）
GITHUB_PAGES_URL=https://你的用户名.github.io/ai-daily-report
GIT_REPO_PATH=C:\Users\jiawa\ai-daily-report
```

**如何获取各 API Key：**

| API | 地址 | 价格 |
|-----|------|------|
| Tavily | https://app.tavily.com | 免费 1000次/月 |
| Server酱 | https://sct.ftqq.com | 免费（扫码绑定微信） |
| Claude | https://console.anthropic.com | 按用量计费，每日约 ¥0.3-0.8 |

### 第三步：配置 GitHub Pages（分享用）

1. 在 GitHub 创建仓库 `ai-daily-report`
2. 在项目目录运行：
   ```bash
   git remote add origin https://github.com/你的用户名/ai-daily-report.git
   git push -u origin main
   ```
3. 进入 GitHub 仓库 → Settings → Pages → Source 选 `main` 分支，目录选 `/output`
4. 将生成的 Pages 地址填入 `.env` 的 `GITHUB_PAGES_URL`

### 第四步：设置定时任务

```bash
# 以管理员身份运行
setup_scheduler.bat
```

---

## 手动运行

```bash
# 生成今日日报
python main.py daily

# 生成本周周报
python main.py weekly
```

---

## 项目结构

```
ai-daily-report/
├── main.py              # 主入口
├── fetch_news.py        # Tavily 新闻抓取
├── process_news.py      # Claude 内容处理
├── render_html.py       # HTML 渲染
├── cache.py             # 新闻缓存（供周报使用）
├── notify.py            # Server酱微信推送
├── git_push.py          # GitHub 自动推送
├── config.py            # 配置读取
├── templates/
│   ├── daily_main.html    # 日报模板（中美AI）
│   ├── daily_fashion.html # 时尚专报模板
│   └── weekly.html        # 周报模板
├── output/              # 生成的HTML（推送到GitHub Pages）
│   ├── index.html
│   ├── daily/
│   └── weekly/
├── data/
│   └── news_cache.json  # 缓存文件
├── logs/                # 运行日志
├── .env                 # API Keys（不上传）
├── setup.bat            # 一键安装
└── setup_scheduler.bat  # 配置定时任务
```

---

## 如果使用 Claude 代理服务

在 `.env` 中额外配置：

```env
ANTHROPIC_BASE_URL=https://你的代理地址.com
```

---

## 常见问题

**Q: Tavily 搜不到最新新闻？**
A: Tavily 免费版有延迟，可升级到 paid 计划获得实时搜索。

**Q: 微信没收到推送？**
A: 检查 Server酱 官网是否已绑定微信，注意每日推送有频次限制。

**Q: Git push 失败？**
A: 需先在 GitHub 创建仓库并设置好 remote，参考第三步。
