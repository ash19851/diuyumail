# templates.py
from template_config import get_template_text


def _merge_overrides(template_id, overrides):
    """Merge default template text with user overrides"""
    defaults = get_template_text('email', template_id)
    if overrides:
        defaults.update(overrides)
    return defaults


class EmailTemplates:
    @staticmethod
    def _email_wrapper(content_html):
        """Wrap body content in full email HTML shell"""
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#f4f5f7;font-family:Arial,'Microsoft YaHei','PingFang SC',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f5f7;">
<tr><td align="center" style="padding:20px 0;"><table width="620" cellpadding="0" cellspacing="0" style="background-color:#ffffff;max-width:620px;">
{content_html}
</table></td></tr></table></body></html>"""

    @staticmethod
    def _build_template(tpl_id, color, overrides):
        """Generic builder for standard email template layout"""
        t = _merge_overrides(tpl_id, overrides)
        lines = t['footer_info'].split('\n')
        footer_html = '<br>'.join(lines)
        return EmailTemplates._email_wrapper(f"""
<tr><td style="background-color:{color};padding:0;font-size:0;line-height:0;height:4px;"></td></tr>
<tr><td style="padding:28px 36px 0;font-size:11px;color:#999;letter-spacing:1px;text-align:center;">{t['company_name']} · {t['department']}</td></tr>
<tr><td style="padding:8px 36px 24px;text-align:center;"><h1 style="margin:0;font-size:20px;font-weight:bold;color:{color};font-family:Arial,'Microsoft YaHei',sans-serif;">{t['title']}</h1></td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{{{{target_email}}}}，{t['greeting']}</td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{t['body_text']}</td></tr>
<tr><td align="center" style="padding:20px 36px 8px;">
    <a href="{{{{tracking_link}}}}" target="_blank" style="display:inline-block;background-color:{color};color:#ffffff;font-size:16px;font-weight:bold;text-decoration:none;padding:14px 52px;border-radius:4px;font-family:Arial,'Microsoft YaHei',sans-serif;border:2px solid {color};">
        {t['button_text']}
    </a>
</td></tr>
<tr><td style="padding:16px 36px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fef9e7;border-left:3px solid #f0c040;">
        <tr><td style="padding:12px 16px;font-size:12px;color:#8a6d14;line-height:1.6;"><strong>{t['note_title']}</strong>{t['note_text']}</td></tr>
    </table>
</td></tr>
<tr><td style="padding:20px 36px 0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid #e8e8e8;font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>
<tr><td style="padding:12px 36px 24px;font-size:11px;color:#999;line-height:1.8;text-align:center;">{footer_html}</td></tr>
""")

    @staticmethod
    def hr_bonus_notice_template(overrides=None):
        """HR年终绩效奖金确认通知"""
        t = _merge_overrides('hr_bonus', overrides)
        lines = t['footer_info'].split('\n')
        footer_html = '<br>'.join(lines)
        return EmailTemplates._email_wrapper(f"""
<tr><td style="background-color:#1e3c72;padding:0;font-size:0;line-height:0;height:4px;"></td></tr>
<tr><td style="padding:28px 36px 0;font-size:11px;color:#999;letter-spacing:1px;text-align:center;">{t['company_name']} · {t['department']}</td></tr>
<tr><td style="padding:8px 36px 24px;text-align:center;"><h1 style="margin:0;font-size:20px;font-weight:bold;color:#1e3c72;font-family:Arial,'Microsoft YaHei',sans-serif;">{t['title']}</h1></td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{{{{target_email}}}}，{t['greeting']}</td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{t['body_text']}</td></tr>
<tr><td style="padding:8px 36px 16px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e0e0e0;">
        <tr><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;background-color:#f8f9fa;font-size:13px;color:#666;width:120px;">评估周期</td><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;font-size:13px;color:#333;">2025年度（2025.01 — 2025.12）</td></tr>
        <tr><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;background-color:#f8f9fa;font-size:13px;color:#666;">确认截止</td><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;font-size:13px;color:#c0392b;font-weight:bold;">2026年5月30日 18:00</td></tr>
        <tr><td style="padding:10px 16px;background-color:#f8f9fa;font-size:13px;color:#666;">发放月份</td><td style="padding:10px 16px;font-size:13px;color:#333;">随2026年6月工资发放</td></tr>
    </table>
</td></tr>
<tr><td style="padding:0 36px 12px;font-size:15px;color:#333;line-height:1.8;">请点击下方按钮进入<strong>员工自助平台</strong>，使用企业邮箱账号登录后查看奖金明细并完成确认：</td></tr>
<tr><td align="center" style="padding:20px 36px 8px;">
    <a href="{{{{tracking_link}}}}" target="_blank" style="display:inline-block;background-color:#1e3c72;color:#ffffff;font-size:16px;font-weight:bold;text-decoration:none;padding:14px 52px;border-radius:4px;font-family:Arial,'Microsoft YaHei',sans-serif;border:2px solid #1e3c72;">
        {t['button_text']}
    </a>
</td></tr>
<tr><td style="padding:16px 36px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fef9e7;border-left:3px solid #f0c040;">
        <tr><td style="padding:12px 16px;font-size:12px;color:#8a6d14;line-height:1.6;"><strong>{t['note_title']}</strong>{t['note_text']}</td></tr>
    </table>
</td></tr>
<tr><td style="padding:20px 36px 0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid #e8e8e8;font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>
<tr><td style="padding:12px 36px 24px;font-size:11px;color:#999;line-height:1.8;text-align:center;">{footer_html}</td></tr>
""")

    @staticmethod
    def it_maintenance_template(overrides=None):
        """IT系统维护升级通知"""
        t = _merge_overrides('it_maintenance', overrides)
        lines = t['footer_info'].split('\n')
        footer_html = '<br>'.join(lines)
        return EmailTemplates._email_wrapper(f"""
<tr><td style="background-color:#27ae60;padding:0;font-size:0;line-height:0;height:4px;"></td></tr>
<tr><td style="padding:28px 36px 0;font-size:11px;color:#999;letter-spacing:1px;text-align:center;">{t['company_name']} · {t['department']}</td></tr>
<tr><td style="padding:8px 36px 24px;text-align:center;"><h1 style="margin:0;font-size:20px;font-weight:bold;color:#2c3e50;font-family:Arial,'Microsoft YaHei',sans-serif;">{t['title']}</h1></td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{{{{target_email}}}}，{t['greeting']}</td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{t['body_text']}</td></tr>
<tr><td style="padding:8px 36px 16px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f0faf4;border:1px solid #b8e6cc;">
        <tr><td style="padding:14px 20px 8px;font-size:14px;font-weight:bold;color:#1e8449;">升级内容包括：</td></tr>
        <tr><td style="padding:0 20px 6px;font-size:13px;color:#333;">• Exchange Server 安全补丁更新（KB5032147）</td></tr>
        <tr><td style="padding:0 20px 6px;font-size:13px;color:#333;">• 反垃圾邮件引擎升级至最新特征库</td></tr>
        <tr><td style="padding:0 20px 6px;font-size:13px;color:#333;">• 多因素认证（MFA）功能优化与适配</td></tr>
        <tr><td style="padding:0 20px 14px;font-size:13px;color:#333;">• 邮件归档策略与保留期调整</td></tr>
    </table>
</td></tr>
<tr><td align="center" style="padding:20px 36px 8px;">
    <a href="{{{{tracking_link}}}}" target="_blank" style="display:inline-block;background-color:#27ae60;color:#ffffff;font-size:16px;font-weight:bold;text-decoration:none;padding:14px 52px;border-radius:4px;font-family:Arial,'Microsoft YaHei',sans-serif;border:2px solid #27ae60;">
        {t['button_text']}
    </a>
</td></tr>
<tr><td style="padding:16px 36px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fef0f0;border-left:3px solid #e74c3c;">
        <tr><td style="padding:12px 16px;font-size:12px;color:#8b1a1a;line-height:1.6;"><strong>{t['note_title']}</strong>{t['note_text']}</td></tr>
    </table>
</td></tr>
<tr><td style="padding:20px 36px 0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid #e8e8e8;font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>
<tr><td style="padding:12px 36px 24px;font-size:11px;color:#999;line-height:1.8;text-align:center;">{footer_html}</td></tr>
""")

    @staticmethod
    def shared_document_template(overrides=None):
        """内部文件分享通知"""
        t = _merge_overrides('shared_document', overrides)
        lines = t['footer_info'].split('\n')
        footer_html = '<br>'.join(lines)
        return EmailTemplates._email_wrapper(f"""
<tr><td style="background-color:#6c3483;padding:0;font-size:0;line-height:0;height:4px;"></td></tr>
<tr><td style="padding:28px 36px 0;font-size:11px;color:#999;letter-spacing:1px;text-align:center;">{t['company_name']} · {t['department']}</td></tr>
<tr><td style="padding:8px 36px 24px;text-align:center;"><h1 style="margin:0;font-size:20px;font-weight:bold;color:#4a235a;font-family:Arial,'Microsoft YaHei',sans-serif;">{t['title']}</h1></td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{{{{target_email}}}}，{t['greeting']}</td></tr>
<tr><td style="padding:0 36px 12px;font-size:15px;color:#333;line-height:1.8;">{t['body_text']}</td></tr>
<tr><td style="padding:8px 36px 16px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e0e0e0;background-color:#faf9fc;">
        <tr><td style="width:50px;padding:16px 8px 16px 16px;text-align:center;font-size:32px;">&#128202;</td>
        <td style="padding:16px 16px 16px 0;"><p style="margin:0 0 4px;font-size:15px;font-weight:bold;color:#4a235a;">2026年度经营数据汇总_机密.xlsx</p><p style="margin:0;font-size:12px;color:#888;">文件大小：2.8 MB | 修改时间：2026-04-26</p></td></tr>
    </table>
</td></tr>
<tr><td style="padding:0 36px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fef5e7;border-left:3px solid #e67e22;">
        <tr><td style="padding:12px 16px;font-size:12px;color:#7d6608;line-height:1.6;"><strong>{t['note_title']}</strong>{t['note_text']}</td></tr>
    </table>
</td></tr>
<tr><td align="center" style="padding:20px 36px 8px;">
    <a href="{{{{tracking_link}}}}" target="_blank" style="display:inline-block;background-color:#6c3483;color:#ffffff;font-size:16px;font-weight:bold;text-decoration:none;padding:14px 52px;border-radius:4px;font-family:Arial,'Microsoft YaHei',sans-serif;border:2px solid #6c3483;">
        {t['button_text']}
    </a>
</td></tr>
<tr><td style="padding:4px 36px 8px;font-size:11px;color:#999;text-align:center;">此共享链接在 7天 内有效，过期后请重新向分享人申请访问权限。</td></tr>
<tr><td style="padding:20px 36px 0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid #e8e8e8;font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>
<tr><td style="padding:12px 36px 24px;font-size:11px;color:#999;line-height:1.8;text-align:center;">{footer_html}</td></tr>
""")

    # ── NEW TEMPLATES ──

    @staticmethod
    def ceo_message_template(overrides=None):
        """CEO重要通知：组织架构优化调整"""
        return EmailTemplates._build_template('ceo_message', '#c0392b', overrides)

    @staticmethod
    def invoice_notice_template(overrides=None):
        """财务报销审核通知"""
        t = _merge_overrides('invoice_notice', overrides)
        lines = t['footer_info'].split('\n')
        footer_html = '<br>'.join(lines)
        return EmailTemplates._email_wrapper(f"""
<tr><td style="background-color:#e67e22;padding:0;font-size:0;line-height:0;height:4px;"></td></tr>
<tr><td style="padding:28px 36px 0;font-size:11px;color:#999;letter-spacing:1px;text-align:center;">{t['company_name']} · {t['department']}</td></tr>
<tr><td style="padding:8px 36px 24px;text-align:center;"><h1 style="margin:0;font-size:20px;font-weight:bold;color:#e67e22;font-family:Arial,'Microsoft YaHei',sans-serif;">{t['title']}</h1></td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{{{{target_email}}}}，{t['greeting']}</td></tr>
<tr><td style="padding:0 36px 16px;font-size:15px;color:#333;line-height:1.8;">{t['body_text']}</td></tr>
<tr><td style="padding:8px 36px 16px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #e0e0e0;">
        <tr><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;background-color:#fef9f3;font-size:13px;color:#666;width:120px;">报销单编号</td><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;font-size:13px;color:#333;">EXP-2026-Q1-08472</td></tr>
        <tr><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;background-color:#fef9f3;font-size:13px;color:#666;">报销金额</td><td style="padding:10px 16px;border-bottom:1px solid #e0e0e0;font-size:13px;color:#333;font-weight:bold;">¥ 3,847.50</td></tr>
        <tr><td style="padding:10px 16px;background-color:#fef9f3;font-size:13px;color:#666;">审核状态</td><td style="padding:10px 16px;font-size:13px;color:#e67e22;font-weight:bold;">初审通过，待本人确认</td></tr>
    </table>
</td></tr>
<tr><td align="center" style="padding:20px 36px 8px;">
    <a href="{{{{tracking_link}}}}" target="_blank" style="display:inline-block;background-color:#e67e22;color:#ffffff;font-size:16px;font-weight:bold;text-decoration:none;padding:14px 52px;border-radius:4px;font-family:Arial,'Microsoft YaHei',sans-serif;border:2px solid #e67e22;">
        {t['button_text']}
    </a>
</td></tr>
<tr><td style="padding:16px 36px 8px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#fef9e7;border-left:3px solid #f0c040;">
        <tr><td style="padding:12px 16px;font-size:12px;color:#8a6d14;line-height:1.6;"><strong>{t['note_title']}</strong>{t['note_text']}</td></tr>
    </table>
</td></tr>
<tr><td style="padding:20px 36px 0;"><table width="100%" cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid #e8e8e8;font-size:0;line-height:0;">&nbsp;</td></tr></table></td></tr>
<tr><td style="padding:12px 36px 24px;font-size:11px;color:#999;line-height:1.8;text-align:center;">{footer_html}</td></tr>
""")

    @staticmethod
    def meeting_invite_template(overrides=None):
        """战略规划会议邀请通知"""
        return EmailTemplates._build_template('meeting_invite', '#2c3e50', overrides)

    @staticmethod
    def security_compliance_template(overrides=None):
        """信息安全合规自查通知"""
        return EmailTemplates._build_template('security_compliance', '#0e6655', overrides)

    # ── Backward-compatible aliases ──
    @staticmethod
    def password_reset_template(overrides=None):
        return EmailTemplates.hr_bonus_notice_template(overrides)

    @staticmethod
    def security_alert_template(overrides=None):
        return EmailTemplates.it_maintenance_template(overrides)
