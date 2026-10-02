import os
import json
import winreg
from google import genai
from google.genai import types
import urllib.request
import urllib.error

def get_installed_games():
    games = []
    
    # 1. Steam Games
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") as key:
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            apps_path = os.path.join(install_path, "steamapps", "common")
            if os.path.exists(apps_path):
                for folder in os.listdir(apps_path):
                    if os.path.isdir(os.path.join(apps_path, folder)):
                        games.append(f"Steam: {folder}")
    except:
        pass
        
    # 2. Epic Games
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Epic Games\EpicGamesLauncher") as key:
            appdata_path = os.environ.get("PROGRAMDATA", r"C:\ProgramData")
            manifest_path = os.path.join(appdata_path, "Epic", "EpicGamesLauncher", "Data", "Manifests")
            if os.path.exists(manifest_path):
                for f in os.listdir(manifest_path):
                    if f.endswith(".item"):
                        try:
                            with open(os.path.join(manifest_path, f), "r", encoding="utf-8") as json_file:
                                data = json.load(json_file)
                                if "DisplayName" in data:
                                    games.append(f"Epic: {data['DisplayName']}")
                        except:
                            pass
    except:
        pass
        
    # 3. Riot Games
    riot_path = r"C:\Riot Games"
    if os.path.exists(riot_path):
        for folder in os.listdir(riot_path):
            if folder in ["VALORANT", "League of Legends"]:
                games.append(f"Riot: {folder}")
                
    return games

def ask_ai_tweaks(user_prompt: str, hardware_info: dict, all_tweaks: list, provider: str, model: str, api_key: str):
    if not api_key:
        raise ValueError(f"Lütfen {provider} için API anahtarınızı girin.")
        
    games = get_installed_games()
    games_str = ", ".join(games) if games else "Bulunamadı"
    
    tweak_titles = [t["title"] for t in all_tweaks]
    
    sys_prompt = f"""Sen Ripleytia Windows Optimizer uygulamasının yapay zeka asistanısın (Top Level Windows OS Engineer).
Kullanıcının sistem donanımı: {hardware_info}
Yüklü Oyunlar: {games_str}

Mevcut Tweak Listesi:
{json.dumps(tweak_titles, ensure_ascii=False, indent=2)}

Kullanıcının Talebi: "{user_prompt}"

Görevin: Kullanıcının talebine, donanımına ve oynadığı oyunlara göre SADECE GEREKLİ OLAN VE EN YÜKSEK PERFORMANS ARTIŞINI SAĞLAYACAK tweak'leri mevcut listeden seçmek.
Seçtiğin tweak başlıkları listedekilerle birebir AYNISI OLMALIDIR. Aksi halde kod onları bulamaz.

Cevabını SADECE aşağıdaki gibi katı bir JSON formatında döndür, başka hiçbir açıklama yapma:
{{
    "selected_tweaks": ["Tweak 1", "Tweak 2"],
    "explanation": "Neden bu ayarları seçtiğini ve ne kadar fps artışı beklediğini kısaca açıkla.",
    "estimated_fps_boost": "+15-20 FPS",
    "hardware_improvement": "%12 CPU kullanımı düşüşü, %5 daha az gecikme"
}}
"""
    
    if provider == "Google Gemini":
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=sys_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        try:
            return json.loads(response.text)
        except Exception as e:
            raise ValueError(f"Yapay Zeka düzgün bir yanıt veremedi ({model}).\\nYanıt:\\n{response.text}")
            
    elif provider in ["OpenRouter (OpenCode)", "Nvidia NIM"]:
        url = "https://openrouter.ai/api/v1/chat/completions" if provider == "OpenRouter (OpenCode)" else "https://integrate.api.nvidia.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        if provider == "OpenRouter (OpenCode)":
            headers["HTTP-Referer"] = "https://github.com/ripleytia/Ripleytia-Windows-OBS-Optimizer"
            headers["X-Title"] = "Ripleytia Optimizer"
            
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": "Kullanıcının talebi ve sistemi sana iletildi. Lütfen sadece JSON formatında yanıt ver."}
            ]
        }
        
        req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode("utf-8"), method="POST")
        try:
            with urllib.request.urlopen(req) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                content = res_json["choices"][0]["message"]["content"]
                
                content = content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                return json.loads(content)
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise ValueError(f"API Hatası ({e.code}): {err_msg}")
        except Exception as e:
            raise ValueError(f"Bir hata oluştu veya JSON parse edilemedi: {e}")
