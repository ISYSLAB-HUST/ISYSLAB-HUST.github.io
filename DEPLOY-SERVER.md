# 部署到自有 web 服务器

> **读者**：把这套站点放到自己服务器上的人（站长本人或运维同事）。
> **前提**：站点是**纯静态**的（11 个 HTML + CSS/JS + 图片），**不需要 PHP、数据库、Node、Python**，
> 服务器上只要有个能跑 Nginx / Apache / IIS 的网站环境就行。
>
> 一句话原理：**把 `_site/` 里的文件传到网站目录，部署就完成了。**

---

## 0. 先分清「源码」和「要上传的东西」

| | 目录 | 要不要传服务器 |
|---|---|---|
| **源码**（内容数据、构建脚本、模板） | `content/` `tools/` `*.html` `*.bat` `README.md` `DEPLOY-*.md` | ❌ **不传**，那是本地维护用的 |
| **构建产物**（真正要发布的网站） | `_site/` | ✅ **传这个** |

上传用的包已经打好了：**`isyslab-site-www-<日期>.zip`**

- 里面就是 `_site/` 的内容，**不含外层目录**：解压出来直接是 `index.html` + `assets/`
- 32 个文件、约 3 MB、全英文文件名、**全部相对路径**（已核验）

> 你自己重新出包的完整命令：
> ```bash
> cd <站点根> && python tools/build.py            # 构建到 _site/
> python ~/.workbuddy/skills/isyslab-site-maintain/scripts/pack_deploy.py
> ```

---

## 快速通道：Linux + SSH + 独立域名根目录

> 如果服务器是 **Linux、能 SSH 登录、网站放在独立域名根目录**，照着这四步走，约 15 分钟。

### 第 1 步：域名解析 + 端口放行

1. 域名加一条 **A 记录**指向服务器公网 IP（学校域名通常找信息中心加；自己的域名在服务商控制台加）；
2. 服务器放行 **80 / 443**：云服务器在控制台「安全组」放行；服务器本机防火墙也要放
   （`sudo firewall-cmd --add-service=http --add-service=https --permanent && sudo firewall-cmd --reload`，
   或 Ubuntu 的 `sudo ufw allow 80,443/tcp`）。

### 第 2 步：一条命令把站点推上去

在本机（Windows）执行 —— 会依次完成 **构建 → 打包 → 上传 → 远程解压**：

```bash
cd C:/Users/zdxue/Documents/isyslab-site

# 先试跑（只在本地构建打包，不上传）
python tools/deploy.py --dry-run

# 正式部署（换成你的服务器地址）
python tools/deploy.py --host root@你的服务器IP --path /var/www/isyslab
```

把服务器信息存进 `deploy.config.json`（照 `deploy.config.example.json` 改），以后就只要一句：

```bash
python tools/deploy.py          # --clean 可顺带清掉服务器上的旧文件
```

> 每条命令都要输密码很烦？先配免密登录：
> `ssh-keygen -t ed25519`（一路回车）→ 把 `~/.ssh/id_ed25519.pub` 内容追加到服务器
> `~/.ssh/authorized_keys`，或用 `ssh-copy-id user@服务器`。

**不想用脚本的心智模型**也很简单：本机 `python tools/build.py` 产出 `_site/`，
再把 `_site/` 的**内容**传进 `/var/www/isyslab/` 就行（FTP 工具传也行）。

### 第 3 步：配 Nginx

服务器上建好站点目录后，把仓库里的 **`deploy/nginx-isyslab.conf.example`** 拿过去改三处：

```bash
# 在服务器上
sudo cp nginx-isyslab.conf.example /etc/nginx/conf.d/isyslab.conf
sudo vi /etc/nginx/conf.d/isyslab.conf     # 改 server_name（域名）、root（/var/www/isyslab）、按需调整
sudo nginx -t && sudo systemctl reload nginx
```

顺手把权限理顺（不改的话 Nginx 可能读不到文件，报 403）：

```bash
sudo chown -R www-data:www-data /var/www/isyslab    # CentOS 用 nginx:nginx
sudo find /var/www/isyslab -type d -exec chmod 755 {} \;
sudo find /var/www/isyslab -type f -exec chmod 644 {} \;
```

> Debian/Ubuntu 的 Nginx 习惯把站点放 `/etc/nginx/sites-available/` 再软链到 `sites-enabled/`，
> 两种放法都行，看服务器现有习惯。

### 第 4 步：上 HTTPS + 核对

```bash
sudo apt install certbot python3-certbot-nginx    # CentOS: sudo dnf install certbot python3-certbot-nginx
sudo certbot --nginx -d 你的域名                   # 自动签证书并改好 Nginx 配置，自动续期
```

然后按本文第 4 节的**核对清单**过一遍（样式、双语切换、图片、手机宽度）。

---

## 1. 放到哪里：根目录还是子目录

**两种都支持**（因为全站都用相对路径，没有写死的 `/assets/...`）：

| 想要的效果 | 操作 |
|---|---|
| `https://域名/` 直接是网站 | 解压到**网站根目录** |
| `https://域名/isyslab/` | 在网站根目录下建 `isyslab/`，解压进去 |

---

## 2. 三种上传方式，挑一种

### 路线 A：面板 / 虚拟主机（最省事，不用命令行）

适用宝塔面板、cPanel、阿里云/腾讯云虚拟主机等。

1. 面板 → **文件** → 打开网站根目录（宝塔通常是 `/www/wwwroot/<域名>/`）；
2. 点**上传**，把 `isyslab-site-www-<日期>.zip` 传上去；
3. 右键压缩包 → **解压到当前目录**（解压后确认 `index.html` 与 `assets/` 同级）；
4. 删掉 zip 包，收工。

### 路线 B：FTP / SFTP 客户端

适用任何服务器，推荐 [FileZilla](https://filezilla-project.org/) 或 [WinSCP](https://winscp.net/)（Windows）。

1. 用 FTP/SFTP 账号连上服务器（主机、端口 21 或 22、账号、密码）；
2. 左侧进本地解压后的目录，右侧进网站目录；
3. 全选拖过去。**注意要连同 `assets/` 整个目录一起传**——
   只传 HTML 是最常见的翻车原因（页面能开但样式全丢）。

### 路线 C：命令行（Linux 服务器，最快，也最适合日后更新）

在本地把 `_site/` 同步上去：

```bash
# 增量同步（推荐）：只传变动的文件，几秒钟完成
rsync -avz --delete _site/ user@服务器IP:/var/www/isyslab/

# 没有 rsync 就用 scp（每次全量，慢一些）
scp -r _site/* user@服务器IP:/var/www/isyslab/
```

`--delete` 会把服务器上多余的文件删掉，让两边完全一致。**首次部署若目标目录已有其他内容，先去掉 `--delete`。**

传完把属主和权限理顺（Nginx/Apache 需要可读）：

```bash
sudo chown -R www-data:www-data /var/www/isyslab    # CentOS 用 nginx:nginx
sudo find /var/www/isyslab -type d -exec chmod 755 {} \;
sudo find /var/www/isyslab -type f -exec chmod 644 {} \;
```

---

## 3. 服务器配置要点

### Nginx

```nginx
server {
    listen 80;
    server_name isyslab.example.edu.cn;

    root /var/www/isyslab;        # index.html 所在的目录
    index index.html;

    location / { try_files $uri $uri/ =404; }

    # HTML 不缓存，改了内容立刻生效
    location ~* \.html$ {
        add_header Cache-Control "no-cache, must-revalidate";
    }
    # 静态资源长缓存（改名才失效，本站资源不常变）
    location ~* \.(css|js|svg|png|jpe?g|webp|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    gzip on;
    gzip_types text/css application/javascript image/svg+xml text/html;
    gzip_min_length 1024;
}
```

**三个必须确认的点**：`root` 指向 `index.html` 所在目录、`index index.html`、Nginx 对目录有读权限。

HTTPS 用 `certbot --nginx` 一条命令签发即可（Let's Encrypt）。

### Apache

网站根目录放一个 `.htaccess`：

```apache
DirectoryIndex index.html

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css        "access plus 30 days"
  ExpiresByType application/javascript "access plus 30 days"
  ExpiresByType image/svg+xml   "access plus 30 days"
  ExpiresByType image/png       "access plus 30 days"
  ExpiresByType image/jpeg      "access plus 30 days"
</IfModule>

# 禁用目录列表（防止目录名被猜到时列出文件）
Options -Indexes
```

### IIS（Windows Server）

1. 站点根目录指向解压后的文件夹，**默认文档**加 `index.html`（放在首位）；
2. **必须给 IIS 补 `.svg` 的 MIME 类型**：扩展名 `.svg`、类型 `image/svg+xml`
   （不加的话 Logo 和图标不显示，这是 IIS 最常见的坑）；
3. 顺手把 `.webp` → `image/webp`、`.woff2` → `font/woff2` 也加上。

---

## 4. 部署后核对清单

- [ ] 首页能打开，**样式正常**（导航、配色都在）→ 说明 `assets/` 传全了
- [ ] 右上角**中英文切换**正常
- [ ] 成员照片、Logo、招生页地图都显示（图片路径没问题）
- [ ] 随便点几个栏目页（研究方向 / 团队成员 / 论文），都能开
- [ ] **手机宽度**下排版正常（浏览器窗口拉窄试试）
- [ ] 强制刷新一次（Ctrl+F5），确认不是浏览器缓存的旧内容

---

## 5. 以后的更新

**内容改动 → 重新构建 → 覆盖上传**，就这三步：

```bash
cd C:/Users/zdxue/Documents/isyslab-site
python tools/deploy.py                      # 构建 + 上传一条命令搞定（Linux + SSH 场景）
```

其他方式：

```bash
python tools/build.py                                        # 只构建
rsync -avz --delete _site/ user@服务器:/var/www/isyslab/      # Linux/macOS 本机，增量同步
```

用面板/FTP 的话，就是把新的 `isyslab-site-www-<日期>.zip` 重新解压覆盖一遍。

> 站点没有后台、没有数据库，**更新只发生在你重新上传的那一刻**——
> 不会自己变，也不需要服务器上装任何运行环境。

---

## 6. 常见问题

| 现象 | 原因与处理 |
|---|---|
| 打开是文件列表 / 403 / 404 | 默认文档没配 `index.html`，或 `root` 指错了目录 |
| **页面能开但样式全丢**（白底黑字） | `assets/` 目录没上传完整——只传了 HTML 是最常见的原因 |
| Logo / 图标不显示，其他图片正常 | SVG 的 MIME 类型没配（IIS 必现），补 `image/svg+xml` |
| 子目录部署后样式丢 | 本站已全用相对路径，正常不会发生；若出现，检查是否用工具改写过路径 |
| 改了内容但页面没变 | 浏览器缓存（Ctrl+F5）→ 再看有没有 CDN / 反向代理缓存 HTML |
| 中文显示成乱码 | 服务器别强制 `charset=gbk`；页面本身是 UTF-8 |
| 图片 404，文件名看着一样 | Linux 区分大小写，确认上传时没被工具改成 `Assets` 之类 |

---

## 7. 顺带一提：和 GitHub 那条路的关系

两种上线方式不冲突，可以并存：

- **GitHub Pages**（见 `DEPLOY-GITHUB.md`）：源码放 GitHub，改 markdown 自动发布，适合日常小改；
- **自有服务器**：数据在自己手里、可控性更强，适合正式对外域名。

比较省事的组合是：**源码托管在 GitHub 做版本管理，服务器上用 `rsync` 从本地同步 `_site/`**；
服务器如果有 git 和 Python，也可以直接在服务器上 `git pull && python tools/build.py` 自动更新。
