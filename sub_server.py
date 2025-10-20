#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote
import requests, os, socket

PORT = int(os.environ.get("PORT", 10096))
NODE_FILE = os.environ.get("NODE_FILE", "./merged_nodes.txt")
CONVERTER_URL = os.environ.get("CONVERTER_URL", "http://192.168.20.237:15400/sub?")
CONFIG_URL = os.environ.get("CONFIG_URL", "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full_NoAuto.ini")

def get_local_ip():
    """获取宿主机在局域网内的IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要真正发送数据，只是用来确定本机IP
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/local":
            if not os.path.exists(NODE_FILE):
                self.send_error(404, f"{NODE_FILE} not found")
                return

            with open(NODE_FILE, encoding="utf-8") as f:
                nodes = [line.strip() for line in f if line.strip()]

            merged_raw = "|".join(nodes)
            encoded_url = quote(merged_raw, safe='')

            params = {
                "target": "clash",
                "url": merged_raw,
                "config": CONFIG_URL
            }

            print("\n========== 订阅请求调试信息 ==========")
            print(f"📄 节点总数: {len(nodes)}")
            print("\nOOO 合并后原始字符串（未编码）:")
            print(merged_raw)
            print("\nOOO 合并后编码后的字符串（可用于拼接URL或调试）:")
            print(encoded_url)
            full_url = f"{CONVERTER_URL}target=clash&url={encoded_url}&config={quote(CONFIG_URL, safe='')}"
            print("\n🚀 拼接完整请求 URL（示例）:")
            print(full_url)
            print("====================================\n")

            try:
                resp = requests.get(CONVERTER_URL, params=params, timeout=10)
                self.send_response(200)
                self.send_header("Content-Type", "text/yaml; charset=utf-8")
                self.end_headers()
                self.wfile.write(resp.text.encode("utf-8"))
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not Found")

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Server running on http://{local_ip}:{PORT}/local")
    print("可尝试更换ip为")
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
