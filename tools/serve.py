#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iSyslab local preview server
============================

Serves the built site from ``_site/`` and watches the sources. Whenever a file
under ``content/``, ``assets/`` or one of the HTML templates changes, the site
is rebuilt and every open browser tab reloads itself.

That is the "edit the markdown, watch the page update" loop.

Usage
-----
    python tools/serve.py                # http://127.0.0.1:8765
    python tools/serve.py --port 9000
    python tools/serve.py --no-open      # do not launch a browser

The live-reload hook is injected into the HTML on the fly, so the files in
``_site/`` stay clean and deployable exactly as built.

Console output is deliberately ASCII-only: Windows consoles default to a
non-UTF-8 code page and would mangle anything else.
"""

import argparse
import importlib
import os
import socketserver
import sys
import threading
import time
import webbrowser
from http.server import SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "_site")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build as _build_module  # noqa: E402  (needs sys.path set above)


def run_build(out_dir, verbose=False):
    """Rebuild the site, reloading ``build.py`` first.

    The preview server can outlive several edits to the builder itself, so the
    module is re-imported on every rebuild. Without this, the watcher would keep
    running whatever version of ``build.py`` was on disk when the server started.
    """
    importlib.reload(_build_module)
    return _build_module.build(out_dir, verbose)

WATCH_DIRS = ("content", "assets")
RELOAD_SNIPPET = (
    "<script>(function(){try{"
    "var s=new EventSource('/__livereload');"
    "s.onmessage=function(m){if(m.data==='reload'){location.reload();}};"
    "}catch(e){}})();</script>\n"
)

state = {"version": 0, "last_error": None}
state_lock = threading.Lock()


# --------------------------------------------------------------- file watching
def snapshot():
    seen = {}
    for folder in WATCH_DIRS:
        base = os.path.join(ROOT, folder)
        for dirpath, _dirnames, filenames in os.walk(base):
            for name in filenames:
                path = os.path.join(dirpath, name)
                try:
                    seen[path] = os.path.getmtime(path)
                except OSError:
                    pass
    for name in os.listdir(ROOT):
        if name.endswith(".html"):
            path = os.path.join(ROOT, name)
            try:
                seen[path] = os.path.getmtime(path)
            except OSError:
                pass
    return seen


def watcher():
    previous = snapshot()
    while True:
        time.sleep(0.7)
        current = snapshot()
        if current == previous:
            continue
        previous = current
        try:
            run_build(OUT_DIR, verbose=False)
        except Exception as exc:                      # noqa: BLE001
            with state_lock:
                state["last_error"] = str(exc)
            print("[watch] build failed: %s" % exc)
            continue
        with state_lock:
            state["last_error"] = None
            state["version"] += 1
            version = state["version"]
        print("[watch] rebuilt (revision %d)" % version)


# ------------------------------------------------------------------- http
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUT_DIR, **kwargs)

    def log_message(self, fmt, *args):               # quieter console
        if "__livereload" in (args[0] if args else ""):
            return
        sys.stderr.write("  %s\n" % (fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def do_GET(self):                                # noqa: N802
        if self.path.startswith("/__livereload"):
            return self._stream()
        path = self.translate_path(self.path)
        if path.endswith((".html", ".htm")) and os.path.isfile(path):
            with open(path, encoding="utf-8") as fh:
                page = fh.read()
            page = page.replace("</body>", RELOAD_SNIPPET + "</body>")
            payload = page.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        return super().do_GET()

    def _stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        with state_lock:
            last = state["version"]
        try:
            while True:
                with state_lock:
                    current = state["version"]
                if current != last:
                    last = current
                    self.wfile.write(b"data: reload\n\n")
                else:
                    self.wfile.write(b": keep-alive\n\n")
                self.wfile.flush()
                time.sleep(1.0)
        except (BrokenPipeError, ConnectionResetError, OSError):
            return


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def handle_error(self, request, client_address):
        # Browsers routinely drop keep-alive connections mid-request; that is
        # noise, not a problem worth a traceback.
        exc_type = sys.exc_info()[0]
        if exc_type in (ConnectionAbortedError, ConnectionResetError,
                        BrokenPipeError, TimeoutError):
            return
        super().handle_error(request, client_address)


def pick_port(preferred):
    for port in range(preferred, preferred + 20):
        try:
            return Server(("127.0.0.1", port), Handler), port
        except OSError:
            continue
    raise SystemExit("no free port in range %d-%d" % (preferred, preferred + 20))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Preview the built site with live reload.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args(argv)

    print("building ...")
    run_build(OUT_DIR, verbose=True)

    httpd, port = pick_port(args.port)
    url = "http://127.0.0.1:%d/" % port

    threading.Thread(target=watcher, daemon=True).start()
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    print("")
    print("  iSyslab preview running")
    print("  %s" % url)
    print("  edit content/*.md and the page reloads by itself")
    print("  press Ctrl+C to stop")
    print("")
    if not args.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
