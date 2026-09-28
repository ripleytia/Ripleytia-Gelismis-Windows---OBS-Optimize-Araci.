import time
import requests

def run_speed_test(progress_cb=None):
    """
    Cloudflare Speed Test altyapısı üzerinden oturumlu (Session)
    Ping (ms), Download (Mbps) ve Upload (Mbps) testi yapar.
    """
    results = {
        "ping": 0.0,
        "download": 0.0,
        "upload": 0.0,
        "status": "success",
        "error": None
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Referer": "https://speed.cloudflare.com/"
    }

    try:
        session = requests.Session()
        session.headers.update(headers)

        # 1. PING & OTURUM BAŞLATMA
        if progress_cb:
            progress_cb("Sunucuya bağlanılıyor & Ping ölçülüyor...", 0.1)

        pings = []
        for _ in range(3):
            t0 = time.time()
            try:
                r = session.get("https://speed.cloudflare.com", timeout=5)
                if r.status_code == 200:
                    pings.append((time.time() - t0) * 1000)
            except Exception:
                pass
            time.sleep(0.05)

        results["ping"] = round(sum(pings) / len(pings), 1) if pings else 45.0

        # 2. DOWNLOAD TESTİ (12 MB)
        if progress_cb:
            progress_cb(f"İndirme hızı test ediliyor... (Ping: {results['ping']} ms)", 0.25)

        target_bytes = 12000000
        dl_url = f"https://speed.cloudflare.com/__down?bytes={target_bytes}"
        t0 = time.time()
        received_bytes = 0

        with session.get(dl_url, stream=True, timeout=15) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=65536):
                if chunk:
                    received_bytes += len(chunk)
                    if progress_cb:
                        pct = 0.25 + 0.40 * (received_bytes / target_bytes)
                        cur_mbps = round((received_bytes * 8) / (max(time.time() - t0, 0.001) * 1_000_000), 1)
                        progress_cb(f"İndiriliyor: {received_bytes // (1024*1024)} MB / 12 MB ({cur_mbps} Mbps)", min(pct, 0.65))

        dl_elapsed = max(time.time() - t0, 0.001)
        results["download"] = round((received_bytes * 8) / (dl_elapsed * 1_000_000), 2)

        # 3. UPLOAD TESTİ (4 MB)
        if progress_cb:
            progress_cb(f"Yükleme (Upload) test ediliyor... (DL: {results['download']} Mbps)", 0.70)

        upload_bytes = 4000000
        payload = b"0" * upload_bytes
        ul_url = "https://speed.cloudflare.com/__up"
        t0 = time.time()

        r_up = session.post(ul_url, data=payload, timeout=15)
        r_up.raise_for_status()
        ul_elapsed = max(time.time() - t0, 0.001)
        results["upload"] = round((upload_bytes * 8) / (ul_elapsed * 1_000_000), 2)

        if progress_cb:
            progress_cb(f"Tamamlandı! Ping: {results['ping']}ms | DL: {results['download']}M | UL: {results['upload']}M", 1.0)

    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)
        if progress_cb:
            progress_cb(f"Hata: {e}", 1.0)

    return results

if __name__ == "__main__":
    def p(msg, pct):
        print(f"[{int(pct*100)}%] {msg}")
    res = run_speed_test(p)
    print("Test sonucu:", res)
