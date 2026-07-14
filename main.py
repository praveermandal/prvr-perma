# -*- coding: utf-8 -*-
import asyncio
import os
import re
import sys
import time
import requests
import uuid
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# --- ⚙️ CONFIGURATION ---
sys.stdout.reconfigure(encoding='utf-8')
SIGNATURE = "༺ρ 𝕣 ꪜ 𝕣 अब्बू ☽༻"
MESSAGE_BASE = "Yᴀsʜ - Hᴀʀɪsʜ - Mᴇᴍᴀx Ƭяу мσм кє ѕαтн вєᴅ ᴍᴀỉɴ  ᴍᴀsᴛỉ кᴀяυggᴀ"

# --- 🛡️ NAME GUARDIAN (Background API Monitor) ---
async def run_name_guardian(sid, tid, sig):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-IG-App-ID": "936619743392459",
    })
    session.cookies.set("sessionid", sid, domain=".instagram.com")
    
    while True:
        try:
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/")
            if resp.status_code == 200:
                current_name = resp.json().get("thread", {}).get("thread_title", "")
                if current_name != sig:
                    csrf = session.cookies.get("csrftoken", "")
                    session.post(
                        f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/update_title/",
                        data={"title": sig, "_csrftoken": csrf, "_uuid": str(uuid.uuid4())},
                        headers={"X-CSRFToken": csrf}
                    )
        except: pass
        await asyncio.sleep(60)

# --- 🔥 STRIKE ENGINE (Playwright Bot) ---
async def run_strike(cookie, target_id):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="n_1", 
            headless=True,
            channel="chrome", 
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
            viewport={'width': 375, 'height': 667},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu"
            ]
        )
        
        await Stealth().apply_stealth_async(context)

        # PRECISE LOGIC: 4 Main, 1 Sig, 30s rest, 2m reload
        strike_script = f"""
            ((config) => {{
                const msgText = config.msg;
                const sigText = config.sig;
                const RELOAD_INTERVAL = 120000; // 2 minutes
                const startTime = Date.now();
                
                let messagesSentInCycle = 0; 

                const sendText = (text) => {{
                    const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                    if (box) {{
                        box.focus();
                        document.execCommand('insertText', false, text);
                        box.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        setTimeout(() => {{
                            const btn = Array.from(document.querySelectorAll('div[role="button"], button'))
                                .find(el => el.innerText === 'Send' || el.getAttribute('aria-label') === 'Send');
                            if (btn) btn.click();
                            else box.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}}));
                        }}, 500);
                    }}
                }};

                const pulse = () => {{
                    // 1. Forced Reload every 2 minutes
                    if (Date.now() - startTime > RELOAD_INTERVAL) {{ window.location.reload(); return; }}

                    // 2. Cycle Logic: 4 Main + 1 Sig
                    if (messagesSentInCycle >= 5) {{
                        messagesSentInCycle = 0;
                        setTimeout(pulse, 30000); // 30s rest after cycle of 5
                        return;
                    }}

                    // Send 4 main messages, then the signature
                    if (messagesSentInCycle < 4) {{
                        sendText(msgText + " " + ["🛌", "💤", "🔥", "✨"][Math.floor(Math.random()*4)]);
                    }} else {{
                        sendText(sigText);
                    }}

                    messagesSentInCycle++;
                    setTimeout(pulse, 600 + Math.random() * 200);
                }};
                pulse();
            }})({{'msg': '{MESSAGE_BASE}', 'sig': '{SIGNATURE}'}})
        """
        await context.add_init_script(strike_script)

        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com', 'path': '/', 'secure': True}])

        page = await context.new_page()
        await page.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="domcontentloaded")
        
        await asyncio.sleep(86400)
        await context.close()

# --- 🚀 MAIN ENTRY ---
async def main():
    cookie = os.environ.get("INSTA_COOKIE")
    tid = os.environ.get("TARGET_THREAD_ID")
    if cookie and tid:
        await asyncio.gather(
            run_name_guardian(cookie, tid, SIGNATURE),
            run_strike(cookie, tid)
        )

if __name__ == "__main__":
    asyncio.run(main())
