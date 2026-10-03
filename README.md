# iSyslab 实验室官网

薛志东课题组（Zhidong's Research Group @ HUST）· 单位信息统一写在 `content/about.md`

纯静态站点，**不需要任何前端框架、不需要 Node.js、不需要联网构建**。
所有内容都放在 `content/` 目录的 markdown 文件里，改完重新构建即可。

> **架构约定**：页面骨架（导航、按钮、栏目名等界面文字）在 HTML/JS 模板里，
> **一切内容更新只动 `content/` 下的 markdown，不改代码**。

---

## 一、日常更新：只改 `content/`

### 三种用法，按省事程度排序

| 方式 | 怎么做 | 适合 |
|---|---|---|
| **① 交给 AI 改**（推荐） | 在 WorkBuddy 里说「**更新实验室网站**：把这篇论文加进论文列表」——这句话会唤醒站点的维护技能，它会自己找到目录、改数据、重新构建、截图核对，你只需看结果 | 一切场景，包括改版式、加栏目、换配色 |
| **② GitHub 网页上改** | 仓库里点开 `content/xxx.md` → 右上角铅笔图标 → 改完 `Commit changes`。1–2 分钟后线上自动更新 | 上线后自己补一条新闻、修个错字 |
| **③ 本机改 + `preview.bat`** | 用记事本改 `content/xxx.md` 保存，浏览器自动刷新；满意后双击 `build.bat` 生成 `_site/` | 想立刻看到效果 |

**改内容永远不用碰 HTML / CSS / JS** —— 那些是骨架，文字只住在下面这些 markdown 里。

| 文件 | 对应页面 | 管什么 |
|---|---|---|
| `content/about.md` | 首页简介 + 站点描述 | 实验室简介、单位信息、`<meta>` 描述 |
| `content/publications.md` | 论文发表 + 首页「代表性论文」 | 中英文论文条目、年份分组、首页精选（`featured: true`）；中文论文写 `title_zh` / `authors_zh` / `venue_zh` 三对字段并标 `lang: zh`，`doi` 会渲染成可点击链接 |
| `content/patents.md` | 专利 | 发明专利与软件著作权，按年份分组 |
| `content/books.md` | 教学与教材（教材部分） | 主编/参编的教材与专著，按出版年月倒序 |
| `content/software.md` | Software & Projects 上半页 | 在线服务器与数据库 |
| `content/projects.md` | Software & Projects 下半页 | GitHub 开源仓库 |
| `content/teaching.md` | 教学与教材（课程部分） | 授课课程（授课教师、层次；不显示课程编号；页面按授课教师分组，组内课程从左到右排列，组序 = 文件段落顺序） |
| `content/people.md` | 团队成员 | 指导教师 / 合作指导教师 / 博士后与专职研究人员 / 在读学生 / 同事与校友（**栏目前后顺序由 `tools/build.py` 的 `PEOPLE_GROUPS` 决定**，不靠文件段落顺序） |
| `content/news.md` | 新闻动态 + 首页新闻区 | 新闻条目（首页只显示最新 4 条，靠后的不露面） |
| `content/research.md` | 研究方向 + 首页研究方向卡片 | 五个研究方向的介绍 |
| `content/join.md` | 招生与联系 | 标题区 / 招生岗位卡 / 联系信息 / 办公室地址 / 地图 |

**每个文件的顶部都有一整段中文注释，写清了有哪些字段、什么意思。**
每条记录用单独一行 `---` 分隔，字段写成 `键: 值`，例如：

```markdown
---
year: 2025
title: Your new paper title goes here
authors: Lei Wang, Zhidong Xue*, Yan Wang*
venue: Bioinformatics
featured: true
links: DOI · PDF
---
```

### 双语规则

- 字段名后面加 `_zh` 就是中文版，例如 `desc` / `desc_zh`、`name` / `name_zh`。
- **没写 `_zh` 就自动用英文**，不会出现空白。
- 论文题目、作者、期刊名保持英文原文（学术惯例，也方便被检索），不翻译。

### 会自动跟着变的东西

不用手改 HTML，下面这些都由数据算出来：

- 首页统计数字（论文数、软件与开源项目数、研究方向数）
- 论文页的年份筛选按钮
- Software 页的「6 个在线工具」「6 个代码仓库」
- 首页研究方向卡片（改 `research.md` 一处，首页和研究方向页同时更新）

---

## 二、本地预览（改完立刻看到效果）

双击 **`preview.bat`**。

它会自动构建、启动本地服务、打开浏览器，然后**盯着 `content/` 目录**——
你保存任何一个 markdown 文件，浏览器里的页面会自己刷新。
关掉那个黑窗口就停止。

> 需要电脑上装了 Python 3（[python.org](https://www.python.org/downloads/) 下载时记得勾选
> “Add python.exe to PATH”）。没有 Python 的话见下面「四、不装 Python 也能改」。

---

## 三、发布上线

> **现状**：本站已在 `C:/Users/zdxue/Documents/isyslab-site` 建立本地 git 仓库，但**尚未关联任何远程**；
> 线上 `isyslab-hust.github.io` 仍跑着旧的 Jekyll 版。准备好后按下面任一种方式替换即可。
>
> 📦 **要把站点交给同事上传 GitHub，直接给他 `DEPLOY-GITHUB.md`**——那是给上传者的逐步操作说明
> （三种上传方式 + 开启自动发布 + 核对清单 + 可直接转发的一段话）。
> 🖥️ **要部署到自有 web 服务器，看 `DEPLOY-SERVER.md`**（面板/FTP/rsync 三种上传 + Nginx/Apache/IIS 配置 + 常见问题）。
> 本节只留给自己看的速查。

### 方式 A：GitHub Actions 自动发布（推荐，一次配置）

仓库里已经放好 `.github/workflows/pages.yml`。在 GitHub 上：

1. 把本目录内容推到仓库（例如 `ISYSLAB-HUST/isyslab-hust.github.io`）
2. 仓库 **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**
3. 之后**只要在 GitHub 网页上编辑 `content/` 里的 markdown 并提交**，
   流水线会自动重新构建并发布，一两分钟后网站就更新了。

> ⚠️ `.github` 是隐藏目录，用网页上传或拷 U 盘时最容易漏掉——漏了自动发布就不会跑。
> 打包/交接的完整流程见 `DEPLOY-GITHUB.md`。

### 方式 B：本地构建后推送

双击 `build.bat`，把生成的 `_site/` 目录内容推到 GitHub Pages 仓库根目录即可。

`_site/` 是构建产物，已加入 `.gitignore`，不需要提交。

### 方式 C：自有 web 服务器

站点是纯静态的，**把 `_site/` 的内容传到网站目录即为部署完成**，服务器上不需要 PHP/数据库/Node/Python。
出包 → 上传 → 核对，完整步骤（含 Nginx/Apache/IIS 配置与常见问题）见 **`DEPLOY-SERVER.md`**。

```bash
python tools/build.py                                          # 构建
python tools/deploy.py --host root@服务器IP --path /var/www/isyslab   # 一键上传（Linux + SSH 场景）
python ~/.workbuddy/skills/isyslab-site-maintain/scripts/pack_deploy.py   # 或出 isyslab-site-www-<日期>.zip 手动传
```

日后的更新就是重复上一步（服务器信息存进 `deploy.config.json` 后，只需 `python tools/deploy.py`）。

---

## 四、不装 Python 也能改

`build.bat` / `preview.bat` 只是在调用 `tools/build.py` 和 `tools/serve.py`。
如果不想装 Python，可以：

1. 只改 `content/*.md` 并提交，靠 GitHub Actions 自动构建（方式 A）；
2. 或者临时在页面上直接改 HTML（不推荐——下次构建会被覆盖）。

---

## 五、目录结构

```
.
├── content/               ← 你只需要动这里
│   ├── about.md           实验室简介与单位信息
│   ├── publications.md
│   ├── patents.md
│   ├── books.md           教材与专著（「教学与教材」页下半部分）
│   ├── software.md
│   ├── projects.md
│   ├── teaching.md        授课课程（「教学与教材」页上半部分）
│   ├── people.md
│   ├── news.md
│   ├── research.md
│   └── join.md            招生与联系页的全部内容
├── assets/
│   ├── css/styles.css     全部设计变量（配色、圆角、间距）都在文件开头的 :root
│   ├── js/i18n.js         中英文案字典 + 语言切换
│   ├── js/main.js         导航栏与页脚的单一模板
│   └── img/               logo、favicon、研究配图、地图、成员照片
├── tools/
│   ├── build.py           构建：把 content/*.md 渲染进 HTML 模板
│   ├── serve.py           本地预览服务（带自动刷新）
│   └── deploy.py          一键部署到 Linux 服务器（构建+打包+scp+远程解压）
├── deploy/
│   └── nginx-isyslab.conf.example   Nginx 站点配置模板（改域名和 root 即可用）
├── index.html …           页面模板，含 <!-- BUILD:xxx --> 标记区
├── build.bat              一键构建
├── preview.bat            一键预览（自动刷新）
├── README.md              本手册
├── DEPLOY-GITHUB.md       交给上传者看的发布说明（GitHub Pages）
├── DEPLOY-SERVER.md       部署到自有 web 服务器的说明
├── .github/workflows/     自动发布流水线（隐藏目录，交接时别漏）
└── _site/                 构建产物（不提交）
```

### 模板里的 `<!-- BUILD:xxx -->` 是什么

HTML 模板里用成对的注释标出了「由 markdown 生成的区域」：

```html
<!-- BUILD:publications -->
  …每次构建都会被重新生成…
<!-- /BUILD:publications -->
```

只改标记区**外面**的手写内容（页头、页脚、按钮文字等）。
标记区**里面**的改动会在下次构建时丢失。

---

## 六、改设计（配色 / 字体 / 圆角）

全部集中在 `assets/css/styles.css` 开头的 `:root`：

```css
--c-blue:   #1E5AA8;   /* 华科蓝 — 主色 */
--c-navy:   #0C2A4A;   /* 深藏青 — 深色底 */
--c-wm-i:   #2E7BF6;   /* 文字标里那个小写 i 的亮蓝色 */
--c-bg:     #F6F8FB;   /* 浅色区块底 */
--r-card:   14px;      /* 卡片圆角 */
```

改一处，全站生效。

---

## 七、内容现状（2026-10-01）

**已填真实数据**（构建时打印的条数，可随时跑一次 `python tools/build.py` 复核）：

| 区块 | 条数 | 备注 |
|---|---|---|
| 论文 | 53 | 含中文期刊（标 `lang: zh`）与 DOI 链接 |
| 专利与软著 | 28 | 按申请年份分组；授权年份从 `note_zh` 的授权公告日里看 |
| 团队成员 | 30 条记录 | 五组：指导教师 / 合作指导教师 / 博士后与专职研究人员 / 在读学生 / 同事与校友 |
| 新闻 | 13 | 首页只取最新 4 条 |
| 研究方向 | 5 | 配图为自绘 SVG（`assets/img/research/0N.svg`） |
| 教材 / 课程 | 4 / 6 | 《大数据技术》词条已注明实验室参与编写 |
| 在线服务 / 开源仓库 | 6 / 6 | 分属「Software & Projects」页上下两部分 |
| 招生与联系 | 8 | 含办公室地址与地图 |

**还缺的**：

- **在读学生邮箱**：黄兆锋、邰馨瑶（等本人提供后再补 `email` 字段；留空不显示，**不要编**）
- Gallery 页：仍是三张分类占位图
- 联系方式里的 Google Scholar 链接参数为空（原站遗留问题）
- `people.md` 里 Zehua LYU / Jingxiang LU 的英文拼写建议核对一次

## 八、安全网：版本管理与上线

**维护最重要的一条：让每一版都能退回去。** 站点已经建好 git 版本库，2026-10-01 存下了第一个快照。

```bash
cd C:/Users/zdxue/Documents/isyslab-site
git log --oneline                     # 看改动历史
git status --short                    # 看有没有还没提交的改动
git checkout -- content/people.md     # 某一处改坏了，退回上一次提交
```

**约定：每次改完提交一次**（`git add -A && git commit -m "说明改了什么"`）。`_site/` 是产物、不入库。

上线方式见「三、发布上线」：仓库里的 `.github/workflows/pages.yml` 已经写好，
**在 GitHub 网页上改 `content/*.md` 并提交，站点会自动重建发布**，不需要在本地装任何东西。

> 📁 **站点固定在这里**：`C:\Users\zdxue\Documents\isyslab-site`
> 迁移前的老副本还留在 `WorkBuddy\2026-10-01-08-41-28\isyslab-site`（当时被占用没能删掉，
> 里面已放了一个「请勿在此编辑」的说明文件）。**以后只改 Documents 这一份**；老副本确认无误后可手动删除。
