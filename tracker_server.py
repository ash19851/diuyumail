# tracker_server.py
import json
import sqlite3
import os
import sys
import time
import threading

import secrets

from flask import Flask, request, redirect, jsonify, render_template_string, Response, send_from_directory, session

from dataconfig import DatabaseManager
from config_manager import load_config, save_config, update_config
from getmiallist import read_all_rows_specific_sheet
from template_config import get_template_text, update_template_text, reset_template_text, get_template_overrides_map


def get_resource_path(relative_path):
    """获取打包后资源的正确路径"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


app = Flask(__name__, static_folder=get_resource_path('static'))
app.secret_key = secrets.token_hex(32)
db = DatabaseManager()


# ── 认证装饰器 ──
def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('admin_logged_in'):
            if request.path.startswith('/admin/api/'):
                return jsonify({"error": "未登录", "redirect": "/admin/login"}), 401
            return redirect('/admin/login')
        return fn(*args, **kwargs)
    return wrapper

# 全局发送控制
_stop_flag = threading.Event()
_send_thread = None

# ────────────────────────────────────────────
# 伪造登录页（跟踪中转页）
# ────────────────────────────────────────────
TRACKING_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>上海林内 — 统一身份认证</title>
    <meta http-equiv="refresh" content="4;url={{redirect_url}}">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', 'Microsoft YaHei', Tahoma, sans-serif;
            background: #f0f2f5; min-height: 100vh;
            display: flex; justify-content: center; align-items: center; padding: 20px;
        }
        .login-container {
            width: 100%; max-width: 440px; background: #fff; border-radius: 4px;
            box-shadow: 0 2px 16px rgba(0,0,0,0.12); overflow: hidden;
        }
        .login-header { background: #fff; padding: 28px 32px 0; text-align: center; }
        .login-header h2 { font-size: 20px; font-weight: 600; color: #1b1b1b; margin-bottom: 4px; }
        .login-header p { font-size: 13px; color: #605e5c; }
        .login-body { padding: 20px 32px 28px; }
        .form-group { margin-bottom: 16px; }
        .form-group label { display: block; font-size: 13px; color: #323130; margin-bottom: 4px; font-weight: 500; }
        .form-group input {
            width: 100%; padding: 10px 12px; border: 1px solid #8a8886; border-radius: 2px;
            font-size: 14px; color: #323130; background: #faf9f8; outline: none;
        }
        .form-group input:disabled { background: #f3f2f1; color: #a19f9d; border-color: #c8c6c4; }
        .btn-signin {
            width: 100%; padding: 10px; background: #0078d4; color: #fff; border: none;
            border-radius: 2px; font-size: 14px; font-weight: 500; cursor: pointer; margin-top: 8px;
        }
        .spinner-area { text-align: center; margin: 20px 0; }
        .spinner {
            display: inline-block; width: 24px; height: 24px;
            border: 2px solid #edebe9; border-top-color: #0078d4; border-radius: 50%;
            animation: spin 0.8s linear infinite; vertical-align: middle; margin-right: 8px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
        .spinner-text { font-size: 13px; color: #605e5c; vertical-align: middle; }
        .login-footer {
            background: #faf9f8; padding: 16px 32px; text-align: center;
            font-size: 11px; color: #a19f9d; border-top: 1px solid #edebe9;
        }
        .login-footer a { color: #0078d4; text-decoration: none; }
        .divider { display: flex; align-items: center; margin: 16px 0; color: #a19f9d; font-size: 12px; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #edebe9; }
        .divider span { padding: 0 12px; }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <svg width="160" height="36" viewBox="0 0 160 36" style="margin-bottom:16px;">
                <rect x="0" y="4" width="28" height="28" rx="4" fill="#0078d4"/>
                <text x="7" y="24" font-size="14" font-weight="bold" fill="white">R</text>
                <text x="36" y="24" font-size="16" font-weight="600" fill="#1b1b1b">上海林内</text>
            </svg>
            <h2>统一身份认证</h2>
            <p>请使用企业邮箱账号登录</p>
        </div>
        <div class="login-body">
            <div class="form-group">
                <label>企业邮箱</label>
                <input type="email" disabled value="{{target_email}}" placeholder="user@rinnai.com.cn">
            </div>
            <div class="form-group">
                <label>密码</label>
                <input type="password" disabled value="············" placeholder="输入密码">
            </div>
            <button class="btn-signin" disabled>登录</button>
            <div class="spinner-area">
                <div class="spinner"></div>
                <span class="spinner-text">正在验证身份信息...</span>
            </div>
            <div class="divider"><span>或</span></div>
            <p style="font-size:12px;color:#a19f9d;text-align:center;">使用企业微信 / Microsoft 365 账号快捷登录</p>
        </div>
        <div class="login-footer">
            <p>&copy; 2026 上海林内有限公司 内部系统</p>
            <p><a href="{{redirect_url}}">无法自动跳转？点击此处</a></p>
        </div>
    </div>
    <script>
        setTimeout(function() {
            fetch('/additional_info', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    width: screen.width, height: screen.height,
                    colorDepth: screen.colorDepth, language: navigator.language,
                    timezone: new Date().getTimezoneOffset()
                })
            });
        }, 800);
    </script>
</body>
</html>
"""


# ════════════════════════════════════════════
# 核心路由
# ════════════════════════════════════════════

@app.route('/')
def root():
    """首页重定向到管理面板"""
    return redirect('/admin')


# ═══ 认证路由 ═══
@app.route('/admin/login')
def admin_login_page():
    """登录页面"""
    if session.get('admin_logged_in'):
        return redirect('/admin')
    return send_from_directory(app.static_folder, 'login.html')


@app.route('/admin/login', methods=['POST'])
def admin_login():
    """处理登录"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "msg": "无效请求"}), 400
    admin = db.verify_admin(data.get('username', ''), data.get('password', ''))
    if admin:
        session['admin_logged_in'] = True
        session['admin_username'] = admin['username']
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "msg": "用户名或密码错误"}), 401


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect('/admin/login')


@app.route('/admin')
@login_required
def admin_panel():
    """管理面板"""
    return send_from_directory(app.static_folder, 'admin.html')


@app.route('/track/<tracking_id>')
def track_click(tracking_id):
    """跟踪链接点击"""
    campaign_id = request.args.get('campaign')
    target_email = request.args.get('email')

    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')

    if campaign_id and target_email:
        db.record_click(campaign_id, target_email, ip_address, user_agent)
        print(f"记录点击: {target_email} (活动: {campaign_id})")

    # 根据活动配置选择警示页面
    warning_template = 'cyberpunk'
    if campaign_id:
        conn = sqlite3.connect(db.db_path)
        row = conn.execute('SELECT warning_template FROM campaigns WHERE id=?', (campaign_id,)).fetchone()
        conn.close()
        if row:
            warning_template = row[0]

    cfg = load_config()
    redirect_url = f"{cfg.get('base_url', '')}/static/warning_{warning_template}.html"

    # 使用 trace 参数避免重定向后的页面也被记录
    return render_template_string(TRACKING_PAGE, redirect_url=redirect_url, target_email=target_email)


@app.route('/additional_info', methods=['POST'])
def record_additional_info():
    data = request.json
    print(f"额外信息: {data}")
    return jsonify({"status": "success"})


@app.route('/stats/<campaign_id>')
def get_campaign_stats(campaign_id):
    stats = db.get_campaign_stats(int(campaign_id))
    return jsonify(stats if stats else {"error": "活动不存在"})


@app.route('/dashboard')
def dashboard():
    """旧仪表板（跳转到管理面板）"""
    return redirect('/admin')


# ════════════════════════════════════════════
# 管理 API
# ════════════════════════════════════════════

@app.route('/admin/api/session')
def admin_session():
    """检查当前登录状态"""
    return jsonify({
        "logged_in": session.get('admin_logged_in', False),
        "username": session.get('admin_username', '')
    })


@app.route('/admin/api/config', methods=['GET', 'POST'])
@login_required
def admin_config():
    """读取或更新配置"""
    if request.method == 'GET':
        return jsonify(load_config())

    updates = request.get_json(silent=True)
    if not updates:
        return jsonify({"status": "error", "msg": "无效的请求数据"}), 400

    update_config(updates)
    return jsonify({"status": "ok"})


@app.route('/admin/api/preview-warning/<template_name>')
@login_required
def preview_warning(template_name):
    """预览警示页面模板"""
    filename = f'warning_{template_name}.html'
    path = os.path.join(app.static_folder, filename)
    if not os.path.exists(path):
        return "模板不存在", 404
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/admin/api/targets')
@login_required
def admin_targets():
    """读取目标邮箱列表"""
    try:
        emails = read_all_rows_specific_sheet("maillist.xlsx")
        if emails is None:
            return jsonify({"count": 0, "emails": [], "error": "maillist.xlsx 未找到"})
        emails = [e for e in emails if e and str(e).strip()]
        return jsonify({"count": len(emails), "emails": [str(e) for e in emails]})
    except Exception as e:
        return jsonify({"count": 0, "emails": [], "error": str(e)})


@app.route('/admin/api/campaign/start', methods=['POST'])
@login_required
def admin_start_campaign():
    """启动钓鱼活动（SSE 流式返回进度）"""
    global _stop_flag, _send_thread
    _stop_flag.clear()

    def generate():
        from email_sender import PhishingEmailSender

        cfg = load_config()
        sender = PhishingEmailSender(
            smtp_server=cfg['smtp_server'],
            smtp_port=int(cfg['smtp_port']),
            sender_email=cfg['sender_email'],
            password=cfg['sender_password'],
            base_url=cfg['base_url']
        )

        try:
            targets = read_all_rows_specific_sheet("maillist.xlsx")
            if targets is None or len(targets) == 0:
                yield json.dumps({"error": "无法读取 maillist.xlsx 或列表为空"}, ensure_ascii=False) + '\n'
                return
            targets = [str(e).strip() for e in targets if e and str(e).strip()]
        except Exception as e:
            yield json.dumps({"error": f"读取Excel失败: {e}"}, ensure_ascii=False) + '\n'
            return

        from templates import EmailTemplates
        tpl_map = {
            'hr_bonus': EmailTemplates.hr_bonus_notice_template,
            'it_maintenance': EmailTemplates.it_maintenance_template,
            'shared_document': EmailTemplates.shared_document_template,
            'ceo_message': EmailTemplates.ceo_message_template,
            'invoice_notice': EmailTemplates.invoice_notice_template,
            'meeting_invite': EmailTemplates.meeting_invite_template,
            'security_compliance': EmailTemplates.security_compliance_template,
        }
        tpl_fn = tpl_map.get(cfg.get('email_template', 'hr_bonus'), EmailTemplates.hr_bonus_notice_template)
        # Load template text overrides from template_config
        tpl_overrides = get_template_overrides_map('email', cfg.get('email_template', 'hr_bonus'))
        html_template = tpl_fn(overrides=tpl_overrides) if tpl_overrides else tpl_fn()

        yield json.dumps({"info": f"活动名称: {cfg.get('campaign_name', '')}"}, ensure_ascii=False) + '\n'
        yield json.dumps({"info": f"邮件模板: {cfg.get('email_template', '')}"}, ensure_ascii=False) + '\n'
        yield json.dumps({"info": f"警示模板: {cfg.get('warning_template', 'cyberpunk')}"}, ensure_ascii=False) + '\n'
        yield json.dumps({"info": f"目标数量: {len(targets)}"}, ensure_ascii=False) + '\n'
        yield json.dumps({"info": "━━━━━━━━━━━━━━━━"}, ensure_ascii=False) + '\n'

        import json as _json
        config_snapshot = _json.dumps(cfg, ensure_ascii=False)
        campaign_id = sender.launch_campaign(
            campaign_name=cfg.get('campaign_name', '未命名'),
            subject=cfg.get('email_subject', ''),
            html_template=html_template,
            target_emails=targets,
            warning_template=cfg.get('warning_template', 'cyberpunk'),
            config_snapshot=config_snapshot
        )

        yield json.dumps({"info": f"活动已创建 ID={campaign_id}，开始发送..."}, ensure_ascii=False) + '\n'

        success = 0
        for i, email in enumerate(targets):
            if _stop_flag.is_set():
                yield json.dumps({"info": "用户中止发送"}, ensure_ascii=False) + '\n'
                break
            try:
                ok = sender.send_phishing_email(campaign_id, email, cfg.get('email_subject', ''), html_template)
                if ok:
                    success += 1
                    yield json.dumps({"ok": f"[{i+1}/{len(targets)}] 已发送 → {email}"}, ensure_ascii=False) + '\n'
                else:
                    yield json.dumps({"error": f"[{i+1}/{len(targets)}] 失败 → {email}"}, ensure_ascii=False) + '\n'
            except Exception as e:
                yield json.dumps({"error": f"[{i+1}/{len(targets)}] 异常 → {email}: {e}"}, ensure_ascii=False) + '\n'
            time.sleep(0.3)  # 避免SMTP限流

        db.update_active(campaign_id)
        yield json.dumps({"done": f"发送完成: {success}/{len(targets)} 成功 | 活动ID={campaign_id}"}, ensure_ascii=False) + '\n'

    return Response(generate(), mimetype='text/event-stream')


@app.route('/admin/api/campaign/stop', methods=['POST'])
@login_required
def admin_stop_campaign():
    _stop_flag.set()
    return jsonify({"status": "ok"})


@app.route('/admin/api/campaigns')
@login_required
def admin_campaigns():
    """获取所有活动及其统计"""
    campaigns = db.get_all_campaigns()
    for c in campaigns:
        stats = db.get_campaign_stats(c['id'])
        c['click_count'] = stats['click_count'] if stats else 0
        c['click_rate'] = stats['click_rate'] if stats else 0
        c['browser_stats'] = stats.get('browser_stats', []) if stats else []
    return jsonify(campaigns)


@app.route('/admin/api/overall-stats')
@login_required
def admin_overall_stats():
    return jsonify(db.get_overall_stats())


@app.route('/admin/api/victims')
@login_required
def admin_victims():
    cid = request.args.get('campaign_id', None)
    return jsonify(db.get_all_victims(int(cid) if cid else None))


@app.route('/admin/api/repeat-victims')
@login_required
def admin_repeat_victims():
    return jsonify(db.get_repeat_victims())


# ═══ 模板文本编辑 API ═══
@app.route('/admin/api/template-text', methods=['GET'])
@login_required
def admin_get_template_text():
    """获取模板可编辑文本字段（合并默认值+覆盖值）"""
    tpl_type = request.args.get('type', 'email')
    tpl_id = request.args.get('id', '')
    if tpl_id:
        return jsonify(get_template_text(tpl_type, tpl_id))
    return jsonify({})


@app.route('/admin/api/template-text', methods=['POST'])
@login_required
def admin_update_template_text():
    """保存模板文本覆盖值"""
    data = request.get_json(silent=True)
    if not data or 'type' not in data or 'id' not in data:
        return jsonify({"status": "error", "msg": "缺少必要参数"}), 400
    result = update_template_text(data['type'], data['id'], data.get('fields', {}))
    return jsonify(result)


@app.route('/admin/api/template-text/reset', methods=['POST'])
@login_required
def admin_reset_template_text():
    """重置模板文本为默认值"""
    data = request.get_json(silent=True)
    if not data or 'type' not in data or 'id' not in data:
        return jsonify({"status": "error", "msg": "缺少必要参数"}), 400
    result = reset_template_text(data['type'], data['id'])
    return jsonify(result)


# ═══ 管理员用户管理 API ═══
@app.route('/admin/api/admins')
@login_required
def admin_list_admins():
    return jsonify(db.get_all_admins())


@app.route('/admin/api/admins', methods=['POST'])
@login_required
def admin_add_admin():
    data = request.get_json(silent=True)
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"status": "error", "msg": "用户名和密码不能为空"}), 400
    ok = db.add_admin(data['username'].strip(), data['password'])
    if ok:
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "msg": "用户名已存在"}), 409


@app.route('/admin/api/admins/<int:admin_id>', methods=['DELETE'])
@login_required
def admin_delete_admin(admin_id):
    ok = db.delete_admin(admin_id)
    if ok:
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "msg": "无法删除：至少保留一个管理员"}), 400


if __name__ == '__main__':
    cfg = load_config()
    app.run(host=cfg.get('server_host', '0.0.0.0'), port=int(cfg.get('server_port', 5000)), debug=True)
