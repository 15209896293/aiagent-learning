#!/usr/bin/env python3
"""
GLM API 本地代理 —— 解决浏览器直连智谱 API 的 CORS 问题

用法：
  1. python glm-proxy.py
  2. 打开 index.html → 设置 → 填入 API Key
  3. 在「本地代理地址」填 http://localhost:8787
  4. 生成功能即可正常使用

按 Ctrl+C 停止。
"""

import http.server
import urllib.request
import json
import sys

PORT = 8787
GLM_BASE = "https://open.bigmodel.cn/api/paas/v4"


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        """转发 POST 请求到智谱 API"""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        url = GLM_BASE + self.path
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", "application/json")

        # 透传 Authorization 头
        auth = self.headers.get("Authorization")
        if auth:
            req.add_header("Authorization", auth)

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                self.send_response(resp.status)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as e:
            self.send_response(502)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def log_message(self, fmt, *args):
        # 简洁日志
        sys.stderr.write(f"[{self.command}] {self.path} -> {args[1]}\n")


if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", PORT), ProxyHandler)
    print(f"GLM 代理已启动: http://localhost:{PORT}")
    print(f"转发目标: {GLM_BASE}")
    print("按 Ctrl+C 停止\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
        server.server_close()
