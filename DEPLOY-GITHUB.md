# 把本站点发布到 GitHub Pages

> **读者**：拿到本站点压缩包、负责上传到 GitHub 的同事。
> **目标**：把站点源码放进 GitHub 仓库，并让 GitHub 自己把网站构建好、发布上线。
> **耗时**：约 10 分钟。**不需要懂代码，也不需要在电脑上装 Python。**
>
> 有任何一步卡住，把截图发回来即可。

---

## 0. 先搞清楚这个包里是什么

这是一个**纯静态网站**（11 个页面：首页、研究方向、团队成员、论文、项目、软件、专利、
教学、教材、新闻、招生与联系）。它有一个很好的性质：

- **页面骨架**（`*.html`）和**文字内容**（`content/*.md`）是分开的；
- 所有文字都躺在 `content/` 下的 11 个 markdown 文本文件里，记事本就能改；
- **不需要任何构建环境**——GitHub 服务器会读 `content/*.md`，自动把网页拼好发布。

所以上传之后，维护网站只需要在 GitHub 网页上改 markdown、点提交，一两分钟后网站自动更新。
没有人需要在本地装工具。

关键文件速查：

| 路径 | 作用 |
|---|---|
| `content/*.md` | **全部文字内容**，日常只改这里 |
| `*.html` | 页面骨架（含生成标记，不用手改） |
| `assets/` | 样式表、脚本、图片（logo、照片、地图） |
| `tools/build.py` | 构建脚本，把 `content/*.md` 拼成网页（GitHub 上自动调用） |
| `.github/workflows/pages.yml` | **自动发布流水线**，已写好，不用改 |
| `README.md` | 完整的维护手册 |
| `DEPLOY-GITHUB.md` | 本文件 |

> ⚠️ 有个**隐藏目录** `.github`（里面是自动发布流水线）。它决定了网站能否自动构建，
> 上传时**千万别漏**。Windows 上需在文件管理器「查看」里勾上「隐藏的项目」才能看到它。

---

## 1. 前置条件

- [ ] 一个 GitHub 账号
- [ ] 目标仓库的**写权限**（若是实验室组织（Organization）名下的仓库，需要先被邀请加入并接受邀请）
- [ ] 想好仓库名。推荐二选一：
  - **替换现有站点** → 用 `isyslab-hust.github.io`（该仓库已存在则直接往里推）
  - **先做新站、不影响旧站** → 用 `isyslab-site`（上线地址会是 `https://<账号>.github.io/isyslab-site/`）

> 目标仓库里**已经有旧站点内容**的话，直接推会被拒绝——先看 **第 6 节** 的处理办法。

---

## 2. 三条路线，选一条就行

### 路线 A：命令行（最快，推荐给熟 git 的人）

```bash
# 1) 解压后进入目录
cd isyslab-site

# 2) 建仓库并提交（压缩包里不含 .git，所以从零初始化）
git init
git add -A
git commit -m "iSyslab site: initial import"
git branch -M main

# 3) 关联远程仓库（把 <owner>/<repo> 换成实际地址）
git remote add origin https://github.com/<owner>/<repo>.git

# 4) 推送
git push -u origin main
```

如果拿到的是 `isyslab-site-<日期>.bundle`（带完整版本历史的单文件），改用：

```bash
git clone isyslab-site-<日期>.bundle isyslab-site
cd isyslab-site
git remote remove origin
git remote add origin https://github.com/<owner>/<repo>.git
git push -u origin main      # 若提示分支为 master，先执行 git branch -M main
```

> 💡 提交时若出现黄色 `warning: … LF will be replaced by CRLF …`，那是行尾自动统一的提示，
> **不是错误**，也不会影响网站，忽略即可。

### 路线 B：GitHub Desktop（不想敲命令，图形界面）

1. 下载安装 [GitHub Desktop](https://desktop.github.com/)，登录 GitHub 账号；
2. 菜单 **File → Add local repository…**，选中解压出来的 `isyslab-site` 文件夹；
3. 它会提示「这不是一个 Git 仓库」，点 **create a repository** → **Create repository**（不用改任何设置）；
4. 右上角 **Publish repository**：取消勾选 *Keep this code private*（**仓库要设为 Public**，
   免费账号的 Pages 才能用），确认仓库名后点 **Publish repository**；
5. 若实验室已有目标仓库，改成 **Repository → Repository settings → Remote → 填仓库地址** 再 **Push origin**。

### 路线 C：纯网页上传（零安装，但最容易漏文件）

1. 在 GitHub 上新建仓库（Public，**不要**勾选 Add README / .gitignore，保持空仓库）；
2. 进入新仓库页 → **Add file → Upload files**；
3. 打开解压出来的 `isyslab-site` 文件夹，**全选其中的内容**（`assets`、`content`、`tools`、
   `.github`、所有 `.html`、`README.md` 等）拖进网页上传区；
   - 先确认能看见 `.github`（隐藏项目），它必须一起上传；
   - 拖拽超过 100 个文件时 GitHub 会报错，本站点只有 56 个文件，正常一次即可；
   - 隐藏文件除了 `.github/`，还有根目录的 `.gitattributes`、`.gitignore`，一样要跟着传
     （勾了「显示隐藏的项目」后会被一并选中，不用单独处理）；
4. 底部 **Commit changes** 提交。

---

## 3. 开启自动发布（关键一步，只做一次）

推上去之后，仓库里已经有流水线文件，还需要在网页上打开开关：

1. 进入仓库 **Settings → Pages**；
2. **Build and deployment → Source** 选择 **GitHub Actions**（不要选 "Deploy from a branch"）；
3. 打开仓库的 **Actions** 标签页，应能看到一条名为 *Build & deploy site* 的运行记录；
   绿色勾 = 构建发布成功（约 1 分钟），红色叉 = 失败，把日志发回来。

成功后，网站地址是：

- 仓库名为 `<账号>.github.io` → `https://<账号>.github.io/`
- 其他仓库名 → `https://<账号>.github.io/<仓库名>/`

---

## 4. 上传后请核对这三件事

- [ ] **Actions** 里 *Build & deploy site* 是绿勾；
- [ ] **Settings → Pages** 的 Source 已经是 **GitHub Actions**，页面顶部显示 Published 地址；
- [ ] 打开网站地址，确认是**新版**：深色导航栏、右上角中英文切换、
      页脚写的是「智能系统实验室@HUST」。如果看到的是旧版 Jekyll 页面，说明推错了仓库或缓存未刷新（Ctrl+F5 强刷）。

---

## 5. 换绑自定义域名（可选，站长操作）

若实验室有域名（例如 `isyslab.hust.edu.cn`）：

1. 在域名服务商处添加 CNAME 记录指向 `<账号>.github.io`；
2. 仓库 **Settings → Pages → Custom domain** 填入域名并保存，
   勾选 **Enforce HTTPS**；
3. GitHub 会在仓库根目录生成 `CNAME` 文件，**不要删**。

---

## 6. ⚠️ 如果目标仓库里已经有旧站点

`isyslab-hust.github.io` 现在跑的是**旧版 Jekyll 站点**，仓库里已经有文件。
往一个**非空仓库**直接推会被拒绝（提示 `rejected … non-fast-forward`），按情况处理：

| 情况 | 做法 |
|---|---|
| **全新的空仓库**（推荐先这样试） | 按第 2 节的任一路线走，直接推即可 |
| 已有旧站点，要**整站替换** | 先把旧仓库 clone 到别处留底，再推本站点并加 `--force`：<br>`git push -u origin main --force`<br>（GitHub Desktop 用户：**Repository → Push** 勾选 *Force push*）。**这会抹掉旧站点内容，动手前请让负责人确认** |
| 已有旧站点，只想**另开一版并存** | 把本站点文件复制进 clone 下来的仓库（新建一个子目录，如 `new-site/`），再提交推送；<br>上线地址会变成 `https://<账号>.github.io/<仓库名>/new-site/` |

**稳妥顺序**：先推到 `isyslab-site` 这个新仓库名验证效果 → 确认无误 → 再决定是否切换正式仓库。

---

## 7. 日常维护：不用碰本地文件

网站上线后，任何人都可以在 GitHub 网页上更新内容：

1. 打开仓库 → 进入 `content/` → 点开要改的文件（如 `news.md`）；
2. 点右上角**铅笔图标**编辑，改完在页面底部填一句说明，点 **Commit changes**；
3. 等 1–2 分钟，网站自动更新。

双语站点的写法、各文件管什么内容，见 `README.md` 第「一、日常更新」节。

---

## 附：发给负责上传的同事（可直接复制）

> 麻烦帮我把这个网站传到 GitHub 上，包已解压好说明在 `DEPLOY-GITHUB.md` 里：
> 1. 解压 `isyslab-site-<日期>.zip`，里面**有个隐藏目录 `.github`**，上传时不能漏；
> 2. 在 GitHub 建一个 **Public** 仓库（建议先叫 `isyslab-site`，或直接用实验室现有仓库）；
> 3. 把解压出来的全部文件推上去（命令行 / GitHub Desktop / 网页上传三种方式都在说明里）；
> 4. 仓库 **Settings → Pages → Source** 选 **GitHub Actions**；
> 5. 打开仓库 **Actions** 标签，确认构建是绿勾，然后把我网站地址发我。
>
> 全程不用装 Python，网站由 GitHub 自动构建。有报错把截图发我。
