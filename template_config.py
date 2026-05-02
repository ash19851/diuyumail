# template_config.py — template text customization management
import json
import os
import sys

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

TEMPLATES_CONFIG_PATH = os.path.join(get_base_dir(), 'templates_config.json')

# ── Default editable text fields per email template ──
EMAIL_DEFAULTS = {
    "hr_bonus": {
        "company_name": "上海林内有限公司",
        "department": "人力资源部",
        "title": "2026年度绩效奖金确认通知",
        "greeting": "您好：",
        "body_text": "2026年度绩效评估工作已结束，您的<strong>年度绩效奖金方案</strong>已生成。请于<strong>7个工作日内</strong>登录员工自助平台查看并确认。",
        "button_text": "进入员工自助平台",
        "note_title": "提示：",
        "note_text": "逾期未确认视为默认同意方案内容。如有疑问，请联系部门负责人或HRBP。",
        "footer_info": "人力资源部 | 上海林内有限公司\n邮箱：hr@shrinnai.com\n© 2026 上海林内有限公司 版权所有",
    },
    "it_maintenance": {
        "company_name": "上海林内有限公司",
        "department": "IT室 · 系统运维组",
        "title": "企业邮箱系统升级维护通知",
        "greeting": "您好：",
        "body_text": "为提升企业邮箱系统的安全性与稳定性，IT室计划于<strong>2026年5月1日（周四）22:00 至 5月2日（周五）06:00</strong>进行系统升级维护。升级期间企业邮箱将暂停服务。为确保升级后邮箱正常使用，请提前完成<strong>账户兼容性验证</strong>：",
        "button_text": "验证邮箱账户",
        "note_title": "重要：",
        "note_text": "未完成验证的账户可能在升级后出现收发异常，请在升级前完成验证操作。",
        "footer_info": "IT室 · 系统运维组 | 上海林内有限公司\n如有疑问请联系IT帮助台：IT@rinnai.com.cn\n© 2026 上海林内有限公司 版权所有",
    },
    "shared_document": {
        "company_name": "上海林内有限公司",
        "department": "企业信息共享平台",
        "title": "文件共享通知",
        "greeting": "您好：",
        "body_text": "<strong>wang.lei@rinnai.com.cn</strong> 通过企业信息共享平台与您分享了以下文件：",
        "button_text": "查看文件",
        "note_title": "备注：",
        "note_text": "此文件包含敏感业务数据，请勿转发给未经授权的人员。此共享链接在 7天 内有效，过期后请重新向分享人申请访问权限。",
        "footer_info": "企业信息共享平台 | 上海林内有限公司\n此为自动通知邮件，请勿回复\n© 2026 上海林内有限公司 版权所有",
    },
    "ceo_message": {
        "company_name": "上海林内有限公司",
        "department": "首席执行官办公室",
        "title": "CEO重要通知：关于组织架构优化调整的公告",
        "greeting": "您好：",
        "body_text": "经董事会审议通过，为适应市场变化、提升运营效率，公司将于近期启动<strong>组织架构优化调整计划</strong>。本次调整涉及部分部门合并与职能重组，详细方案已通过内部系统发布。请登录查看您所在部门的调整方案，并于<strong>2026年5月10日前</strong>完成意见反馈。",
        "button_text": "查看组织架构调整方案",
        "note_title": "机密：",
        "note_text": "本通知内容属于公司内部机密信息，严禁外传。请在规定时间内完成查阅与反馈，逾期将视为默认同意调整方案。",
        "footer_info": "首席执行官办公室 | 上海林内有限公司\n如有疑问请联系CEO办公室：ceo-office@shrinnai.com\n© 2026 上海林内有限公司 版权所有",
    },
    "invoice_notice": {
        "company_name": "上海林内有限公司",
        "department": "财务部",
        "title": "关于2026年度差旅费用报销审核的通知",
        "greeting": "您好：",
        "body_text": "财务部已完成<strong>2026年度第1季度差旅费用报销</strong>的初步审核工作。您的报销申请已进入终审阶段，请登录财务系统核对报销明细金额，确认无误后提交。<strong>报销款项预计于审核完成后3个工作日内到账</strong>。",
        "button_text": "进入财务报销系统",
        "note_title": "注意：",
        "note_text": "如报销明细与实际费用不符，请于收到通知后48小时内联系财务部进行更正。逾期未确认将按初审金额安排付款。",
        "footer_info": "财务部 | 上海林内有限公司\n邮箱：finance@shrinnai.com | 电话：021-xxxx-xxxx\n© 2026 上海林内有限公司 版权所有",
    },
    "meeting_invite": {
        "company_name": "上海林内有限公司",
        "department": "总经办",
        "title": "关于召开2026年度战略规划会议的通知",
        "greeting": "您好：",
        "body_text": "兹定于<strong>2026年5月15日（周五）14:00-17:30</strong>召开2026年度战略规划会议。本次会议将审议公司年度经营目标、重大项目立项及资源配置方案，要求各部门负责人及相关骨干人员参加。请点击下方按钮确认您的参会资格并查看会议议程。",
        "button_text": "确认参会 & 查看议程",
        "note_title": "重要提醒：",
        "note_text": "本次会议内容涉及公司战略决策，所有参会人员需签署保密协议。请携带工牌入场，会议室地点将在确认参会后短信通知。",
        "footer_info": "总经办 | 上海林内有限公司\n会议联系人：总经办秘书处 | 电话：021-xxxx-xxxx\n© 2026 上海林内有限公司 版权所有",
    },
    "security_compliance": {
        "company_name": "上海林内有限公司",
        "department": "信息安全部",
        "title": "关于开展年度信息安全合规自查的紧急通知",
        "greeting": "您好：",
        "body_text": "根据<strong>《网络安全法》及ISO 27001信息安全管理体系</strong>年度审核要求，所有在职员工须于<strong>2026年5月20日前</strong>完成信息安全合规自查。本次自查为强制性要求，未完成者将影响信息系统访问权限。",
        "button_text": "立即开始合规自查",
        "note_title": "合规要求：",
        "note_text": "请务必使用企业邮箱账号登录自查系统。自查内容包括密码安全、权限复核、数据保护等6项，预计耗时8-10分钟。逾期未完成将按公司信息安全管理制度处理。",
        "footer_info": "信息安全部 | 上海林内有限公司\n如有疑问请联系：CERT@rinnai.com.cn\n© 2026 上海林内有限公司 版权所有",
    },
}

# ── Default editable text fields per warning template ──
WARNING_DEFAULTS = {
    "cyberpunk": {
        "page_title": "安全意识培训 — 上海林内",
        "alert_title": "您刚刚点击了一封模拟钓鱼邮件中的链接",
        "alert_body": "这是一次由公司 <strong>IT室</strong> 组织的内部安全意识培训测试，<strong>您并未受到真正的攻击</strong>。但本次测试结果表明：在实际工作中，您可能会对真实的钓鱼邮件放松警惕。",
        "footer_info": "IT室 · 信息安全组 | 上海林内有限公司\n报告可疑邮件：IT@rinnai.com.cn",
    },
    "corporate": {
        "page_title": "安全意识培训 — 上海林内",
        "alert_title": "您刚刚点击了一封模拟钓鱼邮件中的链接",
        "alert_body": "这是一次由公司 IT室 组织的内部安全意识培训测试，您并未受到真正的攻击。但这次测试说明：在日常工作中，您可能同样会点击真实的钓鱼邮件。",
        "footer_info": "IT室 · 信息安全组 | 上海林内有限公司",
    },
    "clean": {
        "page_title": "安全通知 — 上海林内",
        "alert_title": "这是一次模拟钓鱼攻击测试",
        "alert_body": "您刚才点击的链接来自一封模拟钓鱼邮件。这是公司 IT室 组织的安全意识培训的一部分。您没有真的受到攻击，但希望您通过这次经历，提高对真实钓鱼邮件的警惕。",
        "footer_info": "上海林内有限公司 · IT室",
    },
    "minimal": {
        "page_title": "安全培训通知 — 上海林内",
        "alert_title": "这是一次钓鱼邮件模拟测试",
        "alert_body": "您点击的链接来自公司IT室发送的模拟钓鱼邮件，这是一次安全意识培训演习。您没有受到真实攻击，但请警惕——真实的钓鱼邮件往往更加隐蔽。",
        "footer_info": "上海林内有限公司 · 信息安全",
    },
    "education": {
        "page_title": "安全意识教育培训 — 上海林内",
        "alert_title": "模拟钓鱼测试 — 您中招了",
        "alert_body": "您刚刚点击了一封模拟钓鱼邮件中的链接。别担心，这是公司IT室组织的一次内部安全培训测试。但在真实场景中，类似的点击可能导致数据泄露或系统被入侵。请认真阅读下方的安全教育内容。",
        "footer_info": "上海林内有限公司 · IT室 · 信息安全组",
    },
    "tech": {
        "page_title": "SECURITY ALERT — 上海林内",
        "alert_title": "[ 模拟攻击 ] 您点击了钓鱼链接",
        "alert_body": ">> 事件类型：模拟钓鱼邮件攻击演习\n>> 发起单位：IT室 · 信息安全组\n>> 威胁等级：本演习中 - N/A；真实场景中 - CRITICAL\n>> 结论：您在本演习中未能识别钓鱼邮件，在真实攻击中您的账户和设备可能已遭受入侵。",
        "footer_info": "IT-SEC | 上海林内有限公司 | 报告可疑活动: CERT@rinnai.com.cn",
    },
}


def load_templates_config():
    """加载模板文本配置，合并默认值"""
    overrides = {}
    if os.path.exists(TEMPLATES_CONFIG_PATH):
        try:
            with open(TEMPLATES_CONFIG_PATH, 'r', encoding='utf-8') as f:
                overrides = json.load(f)
        except (json.JSONDecodeError, IOError):
            overrides = {}
    return overrides


def save_templates_config(cfg):
    with open(TEMPLATES_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def get_template_text(template_type, template_id):
    """Get editable text fields for a template, merged with any overrides"""
    defaults = EMAIL_DEFAULTS if template_type == 'email' else WARNING_DEFAULTS
    overrides = load_templates_config()
    key = f"{template_type}:{template_id}"
    base = dict(defaults.get(template_id, {}))
    if key in overrides:
        base.update(overrides[key])
    return base


def update_template_text(template_type, template_id, fields):
    """Save text overrides for a template"""
    defaults = EMAIL_DEFAULTS if template_type == 'email' else WARNING_DEFAULTS
    default_fields = defaults.get(template_id, {})
    key = f"{template_type}:{template_id}"
    cfg = load_templates_config()

    # Only store fields that differ from defaults
    overrides = {}
    for k, v in fields.items():
        if k in default_fields and str(v) != str(default_fields[k]):
            overrides[k] = v

    if overrides:
        cfg[key] = overrides
    else:
        cfg.pop(key, None)

    save_templates_config(cfg)
    return {"status": "ok"}


def reset_template_text(template_type, template_id):
    """Reset template text to defaults"""
    key = f"{template_type}:{template_id}"
    cfg = load_templates_config()
    cfg.pop(key, None)
    save_templates_config(cfg)
    return {"status": "ok"}


def get_template_overrides_map(template_type, template_id):
    """Get just the overrides dict for use in template generation (no defaults merged)"""
    key = f"{template_type}:{template_id}"
    cfg = load_templates_config()
    return cfg.get(key, {})
