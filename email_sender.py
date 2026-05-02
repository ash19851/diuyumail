# email_sender.py
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
from dataconfig import DatabaseManager

class PhishingEmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, password, base_url):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password
        self.base_url = base_url  # 跟踪服务器的基本URL
        self.db = DatabaseManager()
    
    def generate_tracking_id(self, email, campaign_id):
        """为每个目标生成唯一的跟踪ID"""
        import hashlib
        import time
        
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        unique_str = f"{email}{campaign_id}{time.time()}{random_str}"
        tracking_id = hashlib.md5(unique_str.encode()).hexdigest()[:16]
        return tracking_id
    
    def create_tracking_link(self, email, campaign_id):
        """创建跟踪链接"""
        tracking_id = self.generate_tracking_id(email, campaign_id)
        tracking_link = f"{self.base_url}/track/{tracking_id}?campaign={campaign_id}&email={email}"
        return tracking_link
    
    def send_phishing_email(self, campaign_id, target_email, subject, html_template):
        """发送钓鱼邮件"""
        # 创建跟踪链接
        tracking_link = self.create_tracking_link(target_email, campaign_id)
        
        # 替换模板中的占位符
        email_content = html_template.replace("{{tracking_link}}", tracking_link)
        email_content = email_content.replace("{{target_email}}", target_email)
        
        # 创建邮件
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = target_email
        
        # 添加HTML版本
        html_part = MIMEText(email_content, "html")
        message.attach(html_part)
        
        try:
            # 发送邮件
            #context = ssl.create_default_context()
           # with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, target_email, message.as_string())
            
            print(f"邮件已发送至: {target_email}")
            return True
            
        except Exception as e:
            print(f"发送邮件失败 {target_email}: {str(e)}")
            return False
    
    def launch_campaign(self, campaign_name, subject, html_template, target_emails, warning_template='cyberpunk', config_snapshot=''):
        """创建钓鱼活动（不发送邮件，发送由 tracker_server 的 SSE 循环完成）"""
        campaign_id = self.db.create_campaign(campaign_name, subject, html_template, target_emails, warning_template, config_snapshot)
        print(f"钓鱼活动已创建: {campaign_name} (ID={campaign_id}, 目标数量: {len(target_emails)})")
        return campaign_id