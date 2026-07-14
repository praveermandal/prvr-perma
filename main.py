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
MESSAGE_BASE = "Yᴀsʜ - Hᴀʀɪsʜ - Mᴇᴍᴀx Ƭяу мσм кє ѕαтн вєᴅ ᴍᴀỉɴ  ᴍᴀsᴛỉ кᴀяυggα"
NAME_UPDATE_COOLDOWN = 300  # 5 minutes cooldown for name changes

# --- 🛡️ NAME GUARDIAN (Background API Monitor) ---
async def run_name_guardian(sid, tid, sig):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-IG-App-ID": "936619743392459",
    })
    session.cookies.set("sessionid", sid, domain=".instagram.com")
    
    last_update = 0
    print("[GUARDIAN] Thread name monitor started...")
    while True:
        try:
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/")
            if resp.status_code == 200:
                current_name = resp.json().get("thread", {}).get("thread_title", "")
                if current_name != sig and (time.time() - last_update > NAME_UPDATE_COOLDOWN):
                    print(f"[GUARDIAN] Breach detected! '{current_name}' -> Reverting to signature...")
                    csrf = session.cookies.get("csrftoken", "")
                    session.post(
                        f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/update_title/",
                        data={"title": sig, "_csrftoken": csrf, "_uuid": str(uuid.uuid4())},
                        headers={"X-CSRFToken": csrf}
                    )
                    last_update = time.time()
        except Exception as e:
            print(f"[GUARDIAN] Monitor error: {e}")
        await asyncio.sleep(60) # Check every 60 seconds

# --- 🔥 STRIKE ENGINE (Playwright Bot) ---
async def run_strike(cookie, target_id):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="n_1", 
            headless=True,
            channel="chrome", 
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
            viewport={'width': 375, 'height': 667},
            ignore_default_args=["--enable-automation"],
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-gpu",
                "--excludeSwitches=enable-automation"
            ]
        )
        
        await Stealth().apply_stealth_async(context)

        stealth_js = """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
            const getParameter = WebGLRenderingContext.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) return 'Apple Inc.';
                if (parameter === 37446) return 'Apple GPU';
                return getParameter(parameter);
            };
        """
        await context.add_init_script(stealth_js)

        # STRIKE SCRIPT: 2m reload, 4msg/60s rest, Multiline fix
        strike_script = f"""
            ((config) => {{
                const msgText = config.msg;
                const sigText = config.sig;
                const RELOAD_INTERVAL = 120000; // 2 minutes
                const startTime = Date.now();
                window._isPulseRunning = false;
                
                const baseEmojis = ["🛌", "💤", "🥱", "🔥", "✨", "💫", "🌟", "🌙"];
                let messageSequenceCount = 0;

                const sendText = (text) => {{
                    const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                    if (box) {{
                        box.innerText = text;
                        box.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        setTimeout(() => {{
                            const btn = Array.from(document.querySelectorAll('div[role="button"], button'))
                                .find(el => el.innerText === 'Send' || el.getAttribute('aria-label') === 'Send');
                            if (btn) btn.click();
                            else box.dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true}}));
                        }}, 600);
                    }}
                }};

                const runLoop = () => {{
                    const bodyText = document.body.innerText.toLowerCase();
                    if (bodyText.includes("security") || bodyText.includes("verify") || bodyText.includes("captcha")) {{
                        window._isPulseRunning = false;
                        setTimeout(runLoop, 10000);
                        return;
                    }}

                    if (Date.now() - startTime > RELOAD_INTERVAL) {{
                        window.location.reload();
                        return;
                    }}

                    if (messageSequenceCount >= 4) {{
                        messageSequenceCount = 0;
                        setTimeout(runLoop, 60000); // 60s rest after 4 messages
                        return;
                    }}

                    window._isPulseRunning = true;
                    if (Math.random() < 0.70) {{
                        let lines = Array(7).fill(msgText + " " + baseEmojis[Math.floor(Math.random() * baseEmojis.length)]);
                        sendText(lines.join("\\n\\n"));
                    }} else {{
                        sendText(sigText);
                    }}
                    
                    messageSequenceCount++;
                    setTimeout(runLoop, 15000 + Math.random() * 10000);
                }};

                setInterval(() => {{ if (!window._isPulseRunning) runLoop(); }}, 5000);
                runLoop();
            }})({{'msg': '{MESSAGE_BASE}', 'sig': '{SIGNATURE}'}})
        """
        await context.add_init_script(strike_script)

        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com', 'path': '/', 'secure': True}])

        page = await context.new_page()
        page.on("console", lambda msg: print(f"[BROWSER] {msg.text}"))
        await page.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="domcontentloaded")
        
        await asyncio.sleep(45000) # Keep tab alive
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
