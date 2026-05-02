# main.py - 钓鱼邮件培训系统启动入口
import os
import sys
import time
import threading
import webbrowser

from config_manager import load_config, get_base_dir
from tracker_server import app


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def run_server():
    """启动 Flask 跟踪服务器"""
    cfg = load_config()
    host = cfg.get('server_host', '0.0.0.0')
    port = int(cfg.get('server_port', 5000))
    print(f"启动管理服务器: http://{host}:{port}")
    app.run(host=host, port=port, debug=False)


def open_browser():
    """延迟打开浏览器到管理面板"""
    time.sleep(2)
    cfg = load_config()
    port = int(cfg.get('server_port', 5000))
    url = f"http://127.0.0.1:{port}/admin"
    print(f"打开管理面板: {url}")
    webbrowser.open(url)


def main():
    cfg = load_config()
    port = int(cfg.get('server_port', 5000))

    print("=" * 50)
    print("  钓鱼邮件安全意识培训系统")
    print("  上海林内有限公司 · IT室")
    print("=" * 50)
    print(f"  配置来源: {os.path.join(get_base_dir(), 'config.json')}")
    print(f"  管理面板: http://127.0.0.1:{port}/admin")
    print(f"  maillist.xlsx: {os.path.join(get_base_dir(), 'maillist.xlsx')}")
    print("=" * 50)
    print()

    # 启动浏览器线程
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # 启动服务器（阻塞）
    run_server()


if __name__ == "__main__":
    main()
