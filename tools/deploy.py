# -*- coding: utf-8 -*-
"""一键把本站点同步到 Linux 服务器（构建 → 打包 → scp → 远程解压）。

    python tools/deploy.py --host root@1.2.3.4 --path /var/www/isyslab
    python tools/deploy.py                 # 读同目录的 deploy.config.json
    python tools/deploy.py --dry-run       # 只本地构建+打包，不上传（先试跑）
    python tools/deploy.py --clean         # 解压前清空目标目录（会删服务器上的旧文件）

为什么用「打包成一个 tgz 再传」而不是直接 scp 整个目录：
  · 只传一个文件，速度快、不易中断，Windows 下也不用担心通配符展开问题
  · 远程一条命令解压到位，不会出现「传了一半」的中间状态

前置：本机有 scp / ssh（Windows 10+ 自带 OpenSSH 客户端；Git Bash 也有）。
建议先配 SSH 密钥免密登录，否则每条命令都要输密码：
    ssh-keygen -t ed25519                 # 一路回车
    ssh-copy-id user@服务器              # 或手动把 ~/.ssh/id_ed25519.pub 追加到服务器 ~/.ssh/authorized_keys
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 站点根
SITE = os.path.join(ROOT, "_site")
CONF = os.path.join(ROOT, "deploy.config.json")
SKIP = {".nojekyll"}


def load_conf():
    if os.path.isfile(CONF):
        with open(CONF, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def build():
    print("[1/4] 构建站点 ...")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build.py")], cwd=ROOT)
    if r.returncode != 0:
        sys.exit("构建失败，已中止（服务器上的内容没有被改动）")
    if not os.path.isfile(os.path.join(SITE, "index.html")):
        sys.exit("构建产物异常：_site/index.html 不存在")


def make_tgz():
    print("[2/4] 打包上传文件 ...")
    fd, tmp = tempfile.mkstemp(prefix="isyslab-upload-", suffix=".tgz")
    os.close(fd)
    with tarfile.open(tmp, "w:gz") as tar:
        for name in sorted(os.listdir(SITE)):
            if name in SKIP:
                continue
            tar.add(os.path.join(SITE, name), arcname=name)
    print("      包大小 %.2f MB" % (os.path.getsize(tmp) / 1048576.0))
    return tmp


def remote_cmd(host, port, path, remote_tgz, clean):
    steps = ["mkdir -p '%s'" % path]
    if clean:
        steps.append("find '%s' -mindepth 1 -delete" % path)
    steps += ["tar xzf '%s' -C '%s'" % (remote_tgz, path), "rm -f '%s'" % remote_tgz]
    return ["ssh", "-p", str(port), host, " && ".join(steps)]


def main():
    conf = load_conf()
    ap = argparse.ArgumentParser(description="构建并同步站点到 Linux 服务器")
    ap.add_argument("--host", default=conf.get("host"), help="user@服务器地址")
    ap.add_argument("--port", default=conf.get("port", 22), help="SSH 端口，默认 22")
    ap.add_argument("--path", default=conf.get("path"), help="服务器上的网站目录，如 /var/www/isyslab")
    ap.add_argument("--clean", action="store_true", help="解压前清空目标目录")
    ap.add_argument("--dry-run", action="store_true", help="只构建打包，不上传")
    args = ap.parse_args()

    for tool in ("scp", "ssh"):
        if not shutil.which(tool):
            sys.exit("找不到 %s，请先安装 OpenSSH 客户端" % tool)

    build()
    tgz = make_tgz()

    if args.dry_run:
        print("[3/4] --dry-run：跳过上传")
        print("      临时包保留在 %s（可手动试传）" % tgz)
        return

    if not (args.host and args.path):
        sys.exit("缺少 --host / --path（或先建一份 deploy.config.json，见 deploy.config.example.json）")

    remote_tgz = "/tmp/isyslab-upload-%d.tgz" % int(time.time())
    try:
        print("[3/4] 上传到 %s ..." % args.host)
        subprocess.run(["scp", "-P", str(args.port), tgz, "%s:%s" % (args.host, remote_tgz)],
                       check=True)
        print("[4/4] 远程解压到 %s ..." % args.path)
        subprocess.run(remote_cmd(args.host, args.port, args.path, remote_tgz, args.clean),
                       check=True)
    except subprocess.CalledProcessError as e:
        sys.exit("传输/解压失败（退出码 %s）。站点内容未被改动，可重试。" % e.returncode)
    finally:
        if os.path.exists(tgz):
            os.remove(tgz)

    print("\n完成！")
    print("  · 打开网站强刷一次（Ctrl+F5）核对效果")
    print("  · 若权限报错，在服务器上执行：")
    print("      sudo chown -R www-data:www-data %s   # CentOS 用 nginx:nginx" % args.path)
    print("      sudo find %s -type d -exec chmod 755 {} \\;" % args.path)
    print("      sudo find %s -type f -exec chmod 644 {} \\;" % args.path)


if __name__ == "__main__":
    main()
