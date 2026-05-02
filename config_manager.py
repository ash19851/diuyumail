# config_manager.py
import json
import os
import sys

def get_base_dir():
    """获取可执行文件或脚本所在目录"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(get_base_dir(), 'config.json')

DEFAULT_CONFIG = {
    "smtp_server": "192.168.0.83",
    "smtp_port": 25,
    "sender_email": "hr@shrinnai.com",
    "sender_password": "",
    "base_url": "http://piannide.rinnai.com.cn:5000",
    "email_template": "hr_bonus",
    "warning_template": "cyberpunk",
    "campaign_name": "2026年度安全意识培训",
    "email_subject": "【HR通知】关于2026年度绩效奖金确认的通知",
    "server_host": "0.0.0.0",
    "server_port": 5000
}


def load_config():
    """加载配置，文件不存在时自动创建默认配置"""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            for k, v in DEFAULT_CONFIG.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
        except (json.JSONDecodeError, IOError):
            pass
    save_config(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    """保存配置到文件"""
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def get_config():
    """获取当前配置（只读）"""
    return load_config()


def update_config(updates):
    """部分更新配置并保存"""
    cfg = load_config()
    cfg.update(updates)
    save_config(cfg)
    return cfg
