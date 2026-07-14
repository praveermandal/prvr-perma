# -*- coding: utf-8 -*-
import asyncio
import os
import re
import sys
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# --- ⚙️ CONFIGURATION ---
sys.stdout.reconfigure(encoding='utf-8')
SIGNATURE = "༺ρ 𝕣 ꪜ 𝕣 अब्बू ☽༻"
MESSAGE_BASE = "Yᴀsʜ - Hᴀʀɪsʜ - Mᴇᴍᴀx \n Ƭяу мσм кє ѕαтн вєᴅ ᴍᴀỉɴ \n ᴍᴀsᴛỉ кᴀяυggᴀ"

async def run_strike(cookie, target_id):
    async with async_playwright() as p:
        # 1. Initialize Context
        context = await p.chromium.launch_persistent_context(
            user_data_dir="n_1", 
            headless=True,
            channel="chrome", 
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15",
            viewport={'width': 375, 'height': 667},
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-gpu", "--excludeSwitches=enable-automation"]
        )
        
        await Stealth().apply_stealth_async(context)
        
        # 2. Add Authentication Cookies BEFORE Navigation (Prevents Crash)
        sid = re.search(r'sessionid=([^;]+)', cookie).group(1) if 'sessionid=' in cookie else cookie
        await context.add_cookies([{'name': 'sessionid', 'value': sid.strip(), 'domain': '.instagram.com', 'path': '/', 'secure': True}])

        # 3. Setup Page and Navigation
        page = await context.new_page()
        page.on("console", lambda msg: print(f"[BROWSER] {msg.text}"))
        page.on("framenavigated", lambda f: f.evaluate("window.addEventListener('message', e => { if(e.data.type==='LOG') console.log(e.data.text); })"))
        
        print("[STRIKER] Navigating to thread...")
        await page.goto(f"https://www.instagram.com/direct/t/{target_id}/", wait_until="networkidle", timeout=60000)
        await page.wait_for_selector('div[role="textbox"], [contenteditable="true"]', timeout=30000)

        # 4. Inject Strike Logic
        strike_script = """
            (config) => {
                const msgText = config.msg;
                const sigText = config.sig;
                const RELOAD_INTERVAL = 120000;
                const startTime = Date.now();
                
                let count = 0;
                const log = (txt) => window.parent.postMessage({ type: 'LOG', text: txt }, '*');

                const sendText = (text) => {
                    const box = document.querySelector('div[role="textbox"], [contenteditable="true"]');
                    if (!box) return false;
                    
                    box.focus();
                    box.innerHTML = '';
                    const dt = new DataTransfer(); dt.setData('text/plain', text);
                    const paste = new ClipboardEvent('paste', {clipboardData: dt, bubbles: true});
                    box.dispatchEvent(paste); 
                    box.dispatchEvent(new Event('input', {bubbles: true}));
                    
                    setTimeout(() => {
                        const btn = Array.from(document.querySelectorAll('div[role="button"], button'))
                            .find(el => el.innerText === 'Send' || el.getAttribute('aria-label') === 'Send');
                        if (btn) btn.click();
                        else box.dispatchEvent(new KeyboardEvent('keydown', {key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true}));
                        log("Action: Message Sent.");
                    }, 800);
                    return true;
                };

                const pulse = () => {
                    if (Date.now() - startTime > RELOAD_INTERVAL) { window.location.reload(); return; }

                    if (count >= 5) {
                        count = 0;
                        log("Status: 30s rest break.");
                        setTimeout(pulse, 30000);
                        return;
                    }

                    const text = (count < 4) ? msgText : sigText;
                    if (sendText(text)) {
                        count++;
                    }
                    setTimeout(pulse, 1500 + Math.random() * 500);
                };
                pulse();
            }
        """
        
        await page.evaluate(strike_script, {"msg": MESSAGE_BASE, "sig": SIGNATURE})
        await asyncio.sleep(86400) # Keep script running
        await context.close()

async def main():
    cookie = os.environ.get("INSTA_COOKIE")
    tid = os.environ.get("TARGET_THREAD_ID")
    if cookie and tid:
        await run_strike(cookie, tid)

if __name__ == "__main__":
    asyncio.run(main())
