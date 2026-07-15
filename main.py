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

# --- 📁 PROXY LIST ---
# Added all provided proxies for rotation[cite: 1]
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

def get_random_proxy():
    p = random.choice(PROXIES)
    return f"http://{p}"

def get_payload():
    base_text = "ᴘʀᴀᴛɪᴋ-ᴠᴇᴇʀ-ꜱᴜʀᴀᴊ-ɴᴇᴍᴇꜱɪs ᴛʀʏ. ᴍᴀ ғʟᴏᴡᴇʀ."
    fire_part = "ʏᴀ ғɪʀᴇ 🔥??"
    flowers = ["🌸", "🌹", "🌺", "🌻", "🌼", "🌷"]
    line = f"{base_text} {random.choice(flowers)} {fire_part}"
    return ("\n" * 50).join([line] * 3)

async def block_media(route):
    if route.request.resource_type in ["image", "media", "font"]:
        await route.abort()
    else:
        await route.continue_()

# --- 🛡️ API NAME GUARDIAN ---
async def run_name_guardian(sid, tid, sig):
    print("🛡️ [GUARDIAN] Initializing...", flush=True)
    session = requests.Session()
    session.proxies = {"http": get_random_proxy(), "https": get_random_proxy()}
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", 
        "X-IG-App-ID": "936619743392459"
    })
    session.cookies.set("sessionid", sid, domain=".instagram.com")
    
    while True:
        try:
            resp = session.get(f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/")
            if resp.status_code == 200:
                current_title = resp.json().get("thread", {}).get("thread_title")
                if current_title != sig:
                    csrf = session.cookies.get("csrftoken", "")
                    session.post(
                        f"https://www.instagram.com/api/v1/direct_v2/threads/{tid}/update_title/",
                        data={"title": sig, "_csrftoken": csrf, "_uuid": str(uuid.uuid4())},
                        headers={"X-CSRFToken": csrf}
                    )
        except Exception as e: print(f"⚠️ [GUARDIAN] Error: {e}", flush=True)
        await asyncio.sleep(60)

# --- 🔥 STRIKE ENGINE ---
async def run_engine(engine_id, sid, url):
    user_data_dir = f"./session_data_{engine_id}"
    print(f"💥 [Engine {engine_id}] Starting...", flush=True)
    
    while True:
        if time.time() - START_TIME > 18000: sys.exit(0)
        proxy = get_random_proxy()
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch_persistent_context(
                    user_data_dir, headless=True,
                    proxy={"server": proxy},
                    args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]
                )
                await browser.add_cookies([{"name": "sessionid", "value": sid, "domain": ".instagram.com", "path": "/", "secure": True, "httpOnly": True}])
                page = await browser.new_page()
                await page.route("**/*", block_media)
                await page.goto(url, wait_until='domcontentloaded', timeout=60000)
                msg_box = page.locator('div[role="textbox"], div[aria-label="Message"]').first
                
                msg_count = 0
                while msg_count < 150: 
                    if msg_count > 0 and msg_count % 30 == 0: await page.reload(wait_until='domcontentloaded')
                    await msg_box.focus()
                    await msg_box.fill(SIGNATURE if random.random() < SIGNATURE_CHANCE else get_payload())
                    await page.keyboard.press("Enter")
                    msg_count += 1
                    print(f"🚀 [Engine {engine_id}] {msg_count}/150 sent via {proxy.split('@')[-1]}", flush=True)
                    await asyncio.sleep(0.3)
            except Exception as e: print(f"⚠️ [Engine {engine_id}] Error: {e}", flush=True)
            
            await browser.close()
            if os.path.exists(user_data_dir): shutil.rmtree(user_data_dir, ignore_errors=True)

async def main():
    sid = os.environ.get("SESSION_ID")
    url = os.environ.get("GROUP_URL")
    tid = url.strip('/').split('/')[-1] if url else ""
    tasks = [run_engine(i+1, sid, url) for i in range(2)]
    if tid: tasks.append(run_name_guardian(sid, tid, SIGNATURE))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
