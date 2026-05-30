"""Capture full-page screenshots of all phishing training system pages."""
import os
import sys
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(OUT_DIR, exist_ok=True)

BASE_URL = "http://127.0.0.1:5000"

pages_to_capture = [
    # (url, filename, description)
    (f"{BASE_URL}/admin/login", "01_login_page.png", "后台登录页"),
    (f"{BASE_URL}/static/warning_cyberpunk.html", "02_warning_cyberpunk.png", "警示页-赛博朋克风格"),
    (f"{BASE_URL}/static/warning_clean.html", "03_warning_clean.png", "警示页-简洁风格"),
    (f"{BASE_URL}/static/warning_corporate.html", "04_warning_corporate.png", "警示页-企业风格"),
    (f"{BASE_URL}/static/warning_education.html", "05_warning_education.png", "警示页-教育风格"),
    (f"{BASE_URL}/static/warning_minimal.html", "06_warning_minimal.png", "警示页-极简风格"),
    (f"{BASE_URL}/static/warning_tech.html", "07_warning_tech.png", "警示页-科技风格"),
]


def capture_login_and_admin(browser):
    """Capture admin panel after login"""
    print("Capturing: 后台登录后管理面板...")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    # Navigate to login page
    page.goto(f"{BASE_URL}/admin/login")
    page.wait_for_timeout(1000)

    # Fill in credentials and login
    page.fill("#username", "admin")
    page.fill("#password", "admin")
    page.click("#btn-login")
    page.wait_for_timeout(2000)

    # Take full-page screenshot of admin panel
    page.goto(f"{BASE_URL}/admin")
    page.wait_for_timeout(3000)
    page.screenshot(
        path=os.path.join(OUT_DIR, "08_admin_panel.png"),
        full_page=True
    )
    print("  -> 08_admin_panel.png")

    # Capture campaign list area (scroll into view)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(1000)

    context.close()


def capture_tracking_page(browser):
    """Capture the fake login tracking page"""
    print("Capturing: 钓鱼跟踪页面（仿冒登录页）...")
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    # Access tracking page with mock params
    page.goto(f"{BASE_URL}/track/demo123?campaign=1&email=user@rinnai.com.cn")
    page.wait_for_timeout(2000)
    page.screenshot(
        path=os.path.join(OUT_DIR, "09_tracking_page.png"),
        full_page=True
    )
    print("  -> 09_tracking_page.png")
    context.close()


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for url, filename, desc in pages_to_capture:
            print(f"Capturing: {desc}...")
            context = browser.new_context(viewport={"width": 1440, "height": 900})
            page = context.new_page()
            page.goto(url)
            page.wait_for_timeout(1500)
            page.screenshot(
                path=os.path.join(OUT_DIR, filename),
                full_page=True
            )
            print(f"  -> {filename}")
            context.close()

        # Admin panel requires login
        capture_login_and_admin(browser)

        # Tracking page
        capture_tracking_page(browser)

        browser.close()

    print(f"\nAll screenshots saved to: {OUT_DIR}")

    # Print file list
    for f in sorted(os.listdir(OUT_DIR)):
        fpath = os.path.join(OUT_DIR, f)
        size_kb = os.path.getsize(fpath) / 1024
        print(f"  {f} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
