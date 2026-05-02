# config.py
import os
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="phishing_tracker.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建活动表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                template TEXT NOT NULL,
                target_list TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                warning_template TEXT DEFAULT 'cyberpunk',
                config_snapshot TEXT DEFAULT ''
            )
        ''')
        # 兼容旧表结构：尝试添加缺失的列
        try:
            cursor.execute('ALTER TABLE campaigns ADD COLUMN warning_template TEXT DEFAULT "cyberpunk"')
        except:
            pass
        try:
            cursor.execute('ALTER TABLE campaigns ADD COLUMN config_snapshot TEXT DEFAULT ""')
        except:
            pass
        
        # 创建点击记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER,
                target_email TEXT NOT NULL,
                click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                country TEXT,
                city TEXT,
                browser TEXT,
                platform TEXT,
                FOREIGN KEY (campaign_id) REFERENCES campaigns (id)
            )
        ''')
        
        # 创建管理员表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # 初始化默认管理员
        from werkzeug.security import generate_password_hash
        cursor.execute('SELECT COUNT(*) FROM admins')
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                           ('admin', generate_password_hash('admin')))
            print("已创建默认管理员: admin / admin")

        conn.commit()
        conn.close()

    # ── 管理员 CRUD ──
    def verify_admin(self, username, password):
        """验证管理员登录，成功返回用户信息，失败返回None"""
        from werkzeug.security import check_password_hash
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute('SELECT * FROM admins WHERE username=?', (username,)).fetchone()
        conn.close()
        if row and check_password_hash(row['password_hash'], password):
            return dict(row)
        return None

    def get_all_admins(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = [dict(r) for r in conn.execute('SELECT id, username, created_at FROM admins ORDER BY id').fetchall()]
        conn.close()
        return rows

    def add_admin(self, username, password):
        from werkzeug.security import generate_password_hash
        conn = sqlite3.connect(self.db_path)
        try:
            conn.execute('INSERT INTO admins (username, password_hash) VALUES (?, ?)',
                         (username, generate_password_hash(password)))
            conn.commit()
            ok = True
        except sqlite3.IntegrityError:
            ok = False
        conn.close()
        return ok

    def delete_admin(self, admin_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # 不允许删除最后一个管理员
        count = cursor.execute('SELECT COUNT(*) FROM admins').fetchone()[0]
        if count <= 1:
            conn.close()
            return False
        cursor.execute('DELETE FROM admins WHERE id=?', (admin_id,))
        conn.commit()
        conn.close()
        return True

    def create_campaign(self, name, subject, template, target_list, warning_template='cyberpunk', config_snapshot=''):
        """创建新的钓鱼活动"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO campaigns (name, subject, template, target_list, warning_template, config_snapshot)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, subject, template, ','.join(target_list), warning_template, config_snapshot))

        campaign_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return campaign_id
    
    def record_click(self, campaign_id, target_email, ip_address, user_agent):
        """记录点击事件"""
        # 解析用户代理信息
        browser, platform = self.parse_user_agent(user_agent)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clicks (campaign_id, target_email, ip_address, user_agent, browser, platform)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (campaign_id, target_email, ip_address, user_agent, browser, platform))
        
        conn.commit()
        conn.close()

    def update_active(self,campaign_id):
        """关闭活动"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE campaigns 
        SET status = ?
        WHERE id = ?
        """, ('close', campaign_id))
    
        conn.commit()
        conn.close()
        print(f"活动 {campaign_id} 已经关闭")


    def parse_user_agent(self, user_agent):
        """解析用户代理字符串"""
        browser = "Unknown"
        platform = "Unknown"
        
        user_agent = user_agent.lower()
        
        # 检测浏览器
        if 'chrome' in user_agent and 'edg' not in user_agent:
            browser = "Chrome"
        elif 'firefox' in user_agent:
            browser = "Firefox"
        elif 'safari' in user_agent and 'chrome' not in user_agent:
            browser = "Safari"
        elif 'edg' in user_agent:
            browser = "Edge"
        elif 'opera' in user_agent:
            browser = "Opera"
        
        # 检测平台
        if 'windows' in user_agent:
            platform = "Windows"
        elif 'mac' in user_agent:
            platform = "Mac"
        elif 'linux' in user_agent:
            platform = "Linux"
        elif 'android' in user_agent:
            platform = "Android"
        elif 'iphone' in user_agent or 'ipad' in user_agent:
            platform = "iOS"
        
        return browser, platform
    
    def get_all_campaigns(self):
        """获取所有活动列表"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''SELECT id, name, subject, template, warning_template, target_list,
                          created_at, status FROM campaigns ORDER BY created_at DESC''')
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_all_victims(self, campaign_id=None):
        """获取受害者详情列表，可按活动筛选"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        if campaign_id:
            cursor.execute('''SELECT cl.*, c.name as campaign_name
                              FROM clicks cl JOIN campaigns c ON cl.campaign_id = c.id
                              WHERE cl.campaign_id = ? ORDER BY cl.click_time DESC''', (campaign_id,))
        else:
            cursor.execute('''SELECT cl.*, c.name as campaign_name
                              FROM clicks cl JOIN campaigns c ON cl.campaign_id = c.id
                              ORDER BY cl.click_time DESC''')
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_repeat_victims(self):
        """获取多次中招的用户（跨活动点击>=2次）"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT target_email, COUNT(*) as click_count,
                   GROUP_CONCAT(DISTINCT campaign_id) as campaign_ids,
                   MAX(click_time) as last_click
            FROM clicks
            GROUP BY target_email
            HAVING COUNT(*) >= 2
            ORDER BY click_count DESC
        ''')
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def get_overall_stats(self):
        """获取全局统计数据"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        total_campaigns = cursor.execute('SELECT COUNT(*) FROM campaigns').fetchone()[0]
        total_targets = 0
        for row in cursor.execute('SELECT target_list FROM campaigns').fetchall():
            total_targets += len(row[0].split(','))

        total_clicks = cursor.execute('SELECT COUNT(*) FROM clicks').fetchone()[0]
        unique_clickers = cursor.execute('SELECT COUNT(DISTINCT target_email) FROM clicks').fetchone()[0]
        conn.close()
        return {
            'total_campaigns': total_campaigns,
            'total_targets': total_targets,
            'total_clicks': total_clicks,
            'unique_clickers': unique_clickers,
            'overall_click_rate': round((unique_clickers / total_targets * 100), 2) if total_targets > 0 else 0
        }

    def get_campaign_stats(self, campaign_id):
        """获取活动统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取总目标和点击数量
        cursor.execute('''
            SELECT c.target_list, COUNT(cl.id) as click_count
            FROM campaigns c
            LEFT JOIN clicks cl ON c.id = cl.campaign_id
            WHERE c.id = ?
            GROUP BY c.id
        ''', (campaign_id,))
        
        result = cursor.fetchone()
        if result:
            target_list = result[0].split(',')
            total_targets = len(target_list)
            click_count = result[1]
            
            # 获取点击率
            click_rate = (click_count / total_targets) * 100 if total_targets > 0 else 0
            
            # 获取浏览器和设备统计
            cursor.execute('''
                SELECT browser, platform, COUNT(*) as count
                FROM clicks
                WHERE campaign_id = ?
                GROUP BY browser, platform
            ''', (campaign_id,))
            
            browser_stats = cursor.fetchall()
            
            return {
                'total_targets': total_targets,
                'click_count': click_count,
                'click_rate': round(click_rate, 2),
                'browser_stats': browser_stats
            }
        
        conn.close()
        return None