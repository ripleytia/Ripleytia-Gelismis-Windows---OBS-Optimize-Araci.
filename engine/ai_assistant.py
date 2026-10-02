import os
import json
import winreg
from google import genai
from google.genai import types

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

def ask_ai_tweaks(user_prompt: str, hardware_info: dict, all_tweaks: list, api_key: str):
    if not api_key:
        raise ValueError("Lütfen ayarlardan (OBS Stüdyo & AI sekmesi) Gemini API anahtarınızı girin.")
        
    client = genai.Client(api_key=api_key)
    
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
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=sys_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        raise ValueError("Yapay Zeka düzgün bir yanıt veremedi. Lütfen tekrar deneyin.")

