import asyncio
import os
import random
import sys
import shutil
import time
import requests
import uuid
from playwright.async_api import async_playwright

START_TIME = time.time()
SIGNATURE = "༺ρ 𝕣 ꪜ 𝕣 अब्बू ☽༻"
SIGNATURE_CHANCE = 0.15 

# --- 📁 FULL PROXY LIST ---
PROXIES = [
    "hughmuir2:lisamarie11@us9.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@us9.cactussstp.com:3129",
    "hughmuir2:lisamarie11@us9.cactussstp.com:3129", "bvmbsmie:shibby2511@us9.cactussstp.com:3129",
    "hughmuir2:lisamarie11@us4.cactussstp.com:3129", "uncpjndo:w77Ebc0h2A@us9.cactussstp.com:8080",
    "bvmbsmie:shibby2511@us9.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@us9.cactussstp.com:81",
    "uncpjndo:w77Ebc0h2A@us4.cactussstp.com:8080", "hughmuir2:lisamarie11@us9.cactussstp.com:81",
    "bvmbsmie:shibby2511@us9.cactussstp.com:81", "purevpn0s13924134:%x9A{H{c{vE7@px013304.pointtoserver.com:10780",
    "purevpn0s13811607:Wb%lj!uEc5&a@px014004.pointtoserver.com:10780", "hughmuir2:lisamarie11@us6.cactussstp.com:3129",
    "bvmbsmie:shibby2511@us4.cactussstp.com:81", "uncpjndo:w77Ebc0h2A@us4.cactussstp.com:81",
    "hughmuir2:lisamarie11@us4.cactussstp.com:81", "hughmuir2:lisamarie11@us4.cactussstp.com:8080",
    "uncpjndo:w77Ebc0h2A@us4.cactussstp.com:3129", "purevpn0s8732217:i67s60ep@px013401.pointtoserver.com:10780",
    "purevpn0s13811607:Wb%lj!uEc5&a@px013401.pointtoserver.com:10780", "uncpjndo:w77Ebc0h2A@us6.cactussstp.com:8080",
    "uncpjndo:w77Ebc0h2A@us6.cactussstp.com:3129", "bvmbsmie:shibby2511@us6.cactussstp.com:3129",
    "bvmbsmie:shibby2511@us6.cactussstp.com:81", "hughmuir2:lisamarie11@us6.cactussstp.com:81",
    "purevpn0s8732217:i67s60ep@px014236.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px016104.pointtoserver.com:10780",
    "bvmbsmie:shibby2511@us4.cactussstp.com:3129", "uncpjndo:w77Ebc0h2A@us6.cactussstp.com:81",
    "hughmuir2:lisamarie11@us6.cactussstp.com:8080", "bvmbsmie:shibby2511@us6.cactussstp.com:8080",
    "purevpn0s13924134:%x9A{H{c{vE7@px014236.pointtoserver.com:10780", "purevpn0s8732217:i67s60ep@px041201.pointtoserver.com:10780",
    "purevpn0s13924134:%x9A{H{c{vE7@px041201.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px041201.pointtoserver.com:10780",
    "purevpn0s14009653:yLMFg4SL52Uua7@px041201.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px016104.pointtoserver.com:10780",
    "purevpn0s13811607:Wb%lj!uEc5&a@px041202.pointtoserver.com:10780", "purevpn0s8732217:i67s60ep@px022408.pointtoserver.com:10780",
    "hughmuir2:lisamarie11@us7.cactussstp.com:3129", "purevpn0s14009653:yLMFg4SL52Uua7@px022408.pointtoserver.com:10780",
    "purevpn0s13924134:%x9A{H{c{vE7@px022408.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px022408.pointtoserver.com:10780",
    "uncpjndo:w77Ebc0h2A@us7.cactussstp.com:3129", "bvmbsmie:shibby2511@us7.cactussstp.com:3129",
    "hughmuir2:lisamarie11@us7.cactussstp.com:8080", "bvmbsmie:shibby2511@us7.cactussstp.com:81",
    "uncpjndo:w77Ebc0h2A@us7.cactussstp.com:8080", "hughmuir2:lisamarie11@us7.cactussstp.com:81",
    "bvmbsmie:shibby2511@us7.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@us7.cactussstp.com:81",
    "purevpn0s13811607:Wb%lj!uEc5&a@px040706.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px040706.pointtoserver.com:10780",
    "purevpn0s8732217:i67s60ep@px040706.pointtoserver.com:10780", "purevpn0s8732217:i67s60ep@px014004.pointtoserver.com:10780",
    "purevpn0s13924134:%x9A{H{c{vE7@px040706.pointtoserver.com:10780", "purevpn0s13924134:%x9A{H{c{vE7@px022409.pointtoserver.com:10780",
    "purevpn0s8732217:i67s60ep@px043006.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px043006.pointtoserver.com:10780",
    "purevpn0s13811607:Wb%lj!uEc5&a@px043006.pointtoserver.com:10780", "purevpn0s8732217:i67s60ep@px022409.pointtoserver.com:10780",
    "uncpjndo:w77Ebc0h2A@us8.cactussstp.com:3129", "hughmuir2:lisamarie11@us8.cactussstp.com:81",
    "purevpn0s13924134:%x9A{H{c{vE7@px043006.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px022409.pointtoserver.com:10780",
    "purevpn0s13811607:Wb%lj!uEc5&a@px040805.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px040805.pointtoserver.com:10780",
    "purevpn0s8732217:i67s60ep@px040805.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px022409.pointtoserver.com:10780",
    "purevpn0s13924134:%x9A{H{c{vE7@px040805.pointtoserver.com:10780", "purevpn0s13924134:%x9A{H{c{vE7@px041202.pointtoserver.com:10780",
    "purevpn0s8732217:i67s60ep@px041202.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px041202.pointtoserver.com:10780",
    "bvmbsmie:shibby2511@uk2.cactussstp.com:3129", "bvmbsmie:shibby2511@us2.cactussstp.com:81",
    "uncpjndo:w77Ebc0h2A@uk2.cactussstp.com:3129", "bvmbsmie:shibby2511@uk2.cactussstp.com:8080",
    "uncpjndo:w77Ebc0h2A@uk2.cactussstp.com:8080", "hughmuir2:lisamarie11@uk2.cactussstp.com:3129",
    "hughmuir2:lisamarie11@uk2.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@uk2.cactussstp.com:81",
    "bvmbsmie:shibby2511@uk2.cactussstp.com:81", "purevpn0s14009653:yLMFg4SL52Uua7@px023005.pointtoserver.com:10780",
    "purevpn0s14009653:yLMFg4SL52Uua7@px023004.pointtoserver.com:10780", "hughmuir2:lisamarie11@us2.cactussstp.com:8080",
    "purevpn0s13811607:Wb%lj!uEc5&a@px023004.pointtoserver.com:10780", "purevpn0s13924134:%x9A{H{c{vE7@px023005.pointtoserver.com:10780",
    "purevpn0s13924134:%x9A{H{c{vE7@px023004.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px023005.pointtoserver.com:10780",
    "bvmbsmie:shibby2511@us2.cactussstp.com:3129", "hughmuir2:lisamarie11@us2.cactussstp.com:81",
    "uncpjndo:w77Ebc0h2A@us2.cactussstp.com:81", "bvmbsmie:shibby2511@us2.cactussstp.com:8080",
    "purevpn0s8732217:i67s60ep@px023004.pointtoserver.com:10780", "purevpn0s8732217:i67s60ep@px023005.pointtoserver.com:10780",
    "uncpjndo:w77Ebc0h2A@us2.cactussstp.com:8080", "purevpn0s13924134:%x9A{H{c{vE7@px022507.pointtoserver.com:10780",
    "purevpn0s8732217:i67s60ep@px022507.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px022507.pointtoserver.com:10780",
    "purevpn0s13811607:Wb%lj!uEc5&a@px022505.pointtoserver.com:10780", "purevpn0s14009653:yLMFg4SL52Uua7@px022505.pointtoserver.com:10780",
    "hughmuir2:lisamarie11@us2.cactussstp.com:3129", "purevpn0s8732217:i67s60ep@px022505.pointtoserver.com:10780",
    "uncpjndo:w77Ebc0h2A@us2.cactussstp.com:3129", "bvmbsmie:shibby2511@us8.cactussstp.com:8080",
    "uncpjndo:w77Ebc0h2A@us1.cactussstp.com:8080", "hughmuir2:lisamarie11@us8.cactussstp.com:3129",
    "purevpn0s13811607:Wb%lj!uEc5&a@px022507.pointtoserver.com:10780", "purevpn0s13924134:%x9A{H{c{vE7@px022505.pointtoserver.com:10780",
    "bvmbsmie:shibby2511@us8.cactussstp.com:81", "uncpjndo:w77Ebc0h2A@us8.cactussstp.com:81",
    "uncpjndo:w77Ebc0h2A@us8.cactussstp.com:8080", "bvmbsmie:shibby2511@us8.cactussstp.com:3129",
    "hughmuir2:lisamarie11@us8.cactussstp.com:8080", "purevpn0s13924134:%x9A{H{c{vE7@px019603.pointtoserver.com:10780",
    "purevpn0s14009653:yLMFg4SL52Uua7@px019603.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px019603.pointtoserver.com:10780",
    "purevpn0s8732217:i67s60ep@px019603.pointtoserver.com:10780", "hughmuir2:lisamarie11@uk2.cactussstp.com:81",
    "bvmbsmie:shibby2511@us1.cactussstp.com:81", "uncpjndo:w77Ebc0h2A@us1.cactussstp.com:81",
    "hughmuir2:lisamarie11@us1.cactussstp.com:3129", "bvmbsmie:shibby2511@us1.cactussstp.com:8080",
    "uncpjndo:w77Ebc0h2A@us1.cactussstp.com:3129", "hughmuir2:lisamarie11@us3.cactussstp.com:3129",
    "bvmbsmie:shibby2511@us3.cactussstp.com:8080", "bvmbsmie:shibby2511@us1.cactussstp.com:3129",
    "uncpjndo:w77Ebc0h2A@us3.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@us3.cactussstp.com:81",
    "hughmuir2:lisamarie11@us3.cactussstp.com:8080", "hughmuir2:lisamarie11@us1.cactussstp.com:81",
    "hughmuir2:lisamarie11@us1.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@us3.cactussstp.com:3129",
    "bvmbsmie:shibby2511@us3.cactussstp.com:3129", "bvmbsmie:shibby2511@us3.cactussstp.com:81",
    "hughmuir2:lisamarie11@us3.cactussstp.com:81", "purevpn0s8732217:i67s60ep@px031901.pointtoserver.com:10780",
    "purevpn0s13924134:%x9A{H{c{vE7@px031901.pointtoserver.com:10780", "purevpn0s13811607:Wb%lj!uEc5&a@px031901.pointtoserver.com:10780",
    "uncpjndo:w77Ebc0h2A@ca1.cactussstp.com:8080", "uncpjndo:w77Ebc0h2A@ca1.cactussstp.com:3129",
    "purevpn0s14009653:yLMFg4SL52Uua7@px031901.pointtoserver.com:10780", "hughmuir2:lisamarie11@ca1.cactussstp.com:3129",
    "bvmbsmie:shibby2511@ca1.cactussstp.com:8080", "hughmuir2:lisamarie11@ca1.cactussstp.com:81",
    "bvmbsmie:shibby2511@ca1.cactussstp.com:3129", "uncpjndo:w77Ebc0h2A@ca1.cactussstp.com:81",
    "hughmuir2:lisamarie11@ca1.cactussstp.com:8080", "bvmbsmie:shibby2511@ca1.cactussstp.com:81",
    "purevpn0s13811607:Wb%lj!uEc5&a@px1260303.pointtoserver.com:10780", "purevpn0s13924134:%x9A{H{c{vE7@px1260303.pointtoserver.com:10780",
    "purevpn0s14009653:yLMFg4SL52Uua7@px1260303.pointtoserver.com:10780", "purevpn0s8732217:i67s60ep@px1260303.pointtoserver.com:10780"
]

def get_payload():
    base_text = "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪs ᴛʀʏ. ᴍᴀ ғʟᴏᴡᴇʀ."
    return ("\n" * 50).join([f"{base_text} {random.choice(['🌸', '🌹', '🌺'])} ʏᴀ ғɪʀᴇ 🔥??"] * 3)

def get_fastest_proxy():
    print("⚡ [SYSTEM] Checking latency for a sample of proxies...", flush=True)
    best_proxy = None
    min_latency = float('inf')
    sample = random.sample(PROXIES, min(3, len(PROXIES)))
    
    for p_str in sample:
        try:
            start = time.time()
            requests.get("https://www.google.com", proxies={"http": f"http://{p_str}", "https": f"http://{p_str}"}, timeout=5)
            latency = time.time() - start
            print(f"📡 Proxy {p_str.split('@')[-1]} latency: {latency:.2f}s", flush=True)
            if latency < min_latency:
                min_latency = latency
                best_proxy = p_str
        except: continue
            
    if not best_proxy:
        best_proxy = random.choice(PROXIES)
        print("⚠️ [SYSTEM] Latency check failed. Falling back to random proxy.", flush=True)
    return f"http://{best_proxy}"

async def run_name_guardian(sid, tid, sig):
    while True:
        try:
            session = requests.Session()
            session.cookies.set("sessionid", sid, domain=".instagram.com")
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/")
            if resp.status_code == 200 and resp.json().get("thread", {}).get("thread_title") != sig:
                print("🚨 [GUARDIAN] Breach detected! Re-securing...", flush=True)
                session.post(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/update_title/", 
                             data={"title": sig}, headers={"X-CSRFToken": session.cookies.get("csrftoken", "")})
        except: pass
        await asyncio.sleep(120)

async def run_engine(engine_id, sid, url):
    user_data_dir = f"./session_data_{engine_id}"
    while True:
        if time.time() - START_TIME > 18000: sys.exit(0)
        proxy = get_fastest_proxy()
        print(f"🌍 [Engine {engine_id}] Using: {proxy.split('@')[-1]}", flush=True)
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch_persistent_context(
                    user_data_dir, headless=True, proxy={"server": proxy},
                    args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
                )
                await browser.add_cookies([{"name": "sessionid", "value": sid, "domain": ".instagram.com", "path": "/", "secure": True, "httpOnly": True}])
                page = await browser.new_page()
                
                print(f"🔗 [Engine {engine_id}] Navigating to target...", flush=True)
                await page.goto(url, wait_until='networkidle', timeout=60000)
                
                msg_box = page.locator('div[role="textbox"], div[aria-label="Message"]').first
                if await msg_box.count() == 0:
                    print(f"⚠️ [Engine {engine_id}] Msg box not found. Check if logged in.", flush=True)
                else:
                    for i in range(150):
                        await msg_box.fill(SIGNATURE if random.random() < 0.1 else get_payload())
                        await page.keyboard.press("Enter")
                        print(f"🚀 [Engine {engine_id}] {i+1}/150 sent.", flush=True)
                        await asyncio.sleep(0.5)
            except Exception as e:
                print(f"❌ [Engine {engine_id}] Error: {e}", flush=True)
            
            await browser.close()
            if os.path.exists(user_data_dir): shutil.rmtree(user_data_dir, ignore_errors=True)

async def main():
    sid, url = os.environ.get("SESSION_ID"), os.environ.get("GROUP_URL")
    tid = url.strip('/').split('/')[-1] if url else ""
    tasks = [run_engine(i+1, sid, url) for i in range(2)]
    if tid: tasks.append(run_name_guardian(sid, tid, SIGNATURE))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
