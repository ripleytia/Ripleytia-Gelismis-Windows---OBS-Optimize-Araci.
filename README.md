# ⚡ Ripleytia Gelişmiş Windows Tweak & Yayıncı Ekosistem Aracı (V2)

<p align="center">
  <img src="assets/logo.png" width="160" alt="Ripleytia Logo" />
</p>

<p align="center">
  <b>Canlı Yayıncılar ve Rekabetçi Oyuncular İçin Gelişmiş Windows 11 & OBS Studio Optimizasyon Merkezi</b><br>
  <i>Sıfır Giriş Gecikmesi • %1 Low FPS Kararlılığı • Yapay Zeka Destekli OBS Profili</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--bit)-blue?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-blueviolet?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/UI-CustomTkinter-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/VirusTotal-Temiz%20(Clean)-brightgreen?style=for-the-badge&logo=virustotal" />
  <img src="https://img.shields.io/badge/Sürüm-V2.0%20Final-purple?style=for-the-badge" />
</p>

---

## 📖 Genel Bakış

**Ripleytia Gelişmiş Windows Tweak & Yayıncı Ekosistem Aracı (V2)**, oyun oynarken aynı anda OBS Studio, Discord, müzik ve ses yönlendirme yazılımları kullanan yayıncıların karşılaştığı performans darboğazlarını ortadan kaldırmak için tasarlanmış bağımsız bir optimizasyon ekosistemidir.

Standart "kör debloat" araçlarının aksine, bu uygulama ses sürücülerini veya güvenlik servislerini bozmaz. **Her ayarın yanında ne işe yaradığı, sisteme ne gibi somut avantajlar sağladığı açıkça listelenmiştir** ve her ayar tek tıkla orijinal haline **Geri Alınabilir**.

---

## 🎯 Temel Özellikler

### 1. ⚡ Güç & İşlemci Kalibrasyonu
* **Nihai Performans (Ultimate Performance) Planı:** Windows'un gizli güç profilini açarak saat frekansı dalgalanmalarını ve çekirdek uyku gecikmelerini engeller.
* **Ryzen Soğutma & Frekans Koruma (Min %0 / Max %100):** AMD Ryzen işlemcilerin masaüstünde serin çalışmasını (38-42°C) sağlar, fan sesini keser ve ağır yükte %100 boostlayarak 80°C+ thermal throttling droplarını bitirir.
* **Aktif Soğutma Politikası (SysCoolPol = 1):** Fanları erken hızlandırarak ani çatışmalarda ısı kaynaklı FPS kayıplarını sönümler.
* **USB Seçmeli Askıya Alma Kapatma:** Fare ve klavyede anlık yoklama gecikmesini sıfırlar; yayında USB mikrofon ve kamera kopmalarını/gecikmelerini önler.
* **PCIe Link State Güç Yönetimi Kapatma (ASPM Off):** GPU ve NVMe SSD veri yolunun uykuya girmesini kapatarak açık dünya oyunlarındaki doku (texture streaming) takılmalarını yok eder.

### 2. 🎮 Grafik & Görüntü Optimizasyonu
* **HAGS (Donanım Hızlandırmalı GPU Zamanlaması):** Grafik belleği ve kare kuyruğu yönetimini CPU'dan RTX/GTX ekran kartına aktarır; OBS NVENC donanım kodlama gecikmesini düşürür.
* **Pencereli Oyun İyileştirmeleri (SwapEffectUpgrade):** Çerçevesiz pencereli (borderless) oyunları modern DXGI Independent Flip sunum modeline yükselterek tam ekran gibi 0 ms DWM gecikmesi sağlar.
* **Küresel Değişken Yenileme Hızı (VRR Global):** Yüksek Hz (144Hz, 200Hz, 240Hz, G-Sync) monitörlerde pencere geçişlerinde yırtılma ve takılmaları önler.
* **GameDVR & Arka Plan Kaydı İptali:** Windows'un arkada sürekli 30 FPS video kaydetmesini engelleyerek NVENC çipini ve VRAM'i %100 OBS Studio'ya bırakır.
* **Windows Oyun Modu (Game Mode) Entegrasyonu.**

### 3. 🧠 Bellek & NVMe Disk İyileştirmeleri
* **16 GB Bellek Çökme Koruması (DisablePagingExecutive = 0):** FiveM, GTA V ve OBS eş zamanlı çalışırken `OUT_OF_MEMORY` kilitlenmelerini engeller.
* **IoPageLockLimit (8 MB):** Disk okuma/yazma I/O arabelleğini 8 megabayta çıkararak harita ve özel araç yüklemelerini hızlandırır.
* **NTFS 8.3 & Son Erişim Zamanı Kapatma:** Gereksiz dosya sistemi loglamasını durdurur.
* **Hazırda Bekletmeyi Kapatma (`powercfg -h off`):** C: diskinde anında 16 GB - 32 GB arası boş depolama alanı açar.

### 4. 🌐 Ağ & Düşük Ping (Yayın Güvenliği)
* **Nagle Algoritmasını Kapatma (TcpAckFrequency & TCPNoDelay):** TCP paket biriktirme mekanizmasını kapatır; CS2, Valorant, FiveM gibi oyunlarda pingi düşürür, mermi kaydını (hitreg) anlık hale getirir.
* **Multimedya Ağ Kısıtlamasını Kaldırma (`NetworkThrottlingIndex = 0xFFFFFFFF`):** Oyun veya müzik açıkken Windows'un ağ paket hızını sınırlamasını kaldırır; yayında bitrate dalgalanmalarını engeller.
* **Sistem Multimedya Tepkiselliği (`SystemResponsiveness = 0`):** CPU gücünün %100'ünü ön plandaki oyuna verir.
* **MMCSS Yüksek Ses Önceliği (High Priority):** Yayın, Discord ve oyun aynı anda çalışırken seste patlama, cızırtı ve gecikmeleri tamamen yok eder.
* **TCP CUBIC & Delivery Optimization LAN Modu:** İnternet upload bant genişliğinin Windows güncellemeleri tarafından çalınmasını engeller.

### 5. 🎯 FiveM & Oyun Özel Ayarları
* **FiveM Bellek Havuzu Artırımı (CitizenFX.ini):** `TxdStore` (32000), `DrmStore` (32000), `FragStore` (16000) havuzlarını genişleterek modlu sunucularda harita altının kaybolmasını engeller.
* **GTA V `commandline.txt`:** `-ignoreDifferentVideoCard` ve `-novblank` parametrelerini oluşturur.
* **Windows Defender Oyun & Yayın Dışlamaları:** FiveM, GTA V, OBS ve Discord için gerçek zamanlı tarama darboğazını engeller (Antivirüs kapatılmaz, yalnızca oyun klasörleri taranırken drop yememeniz için resmi dışlama tanımlanır).

---

## 🛡️ Anti-Cheat & Whitelist Güvenlik Garantisi (PC Check Uyumlu)

Bu araç, rekabetçi FiveM ve espor sunucularındaki en katı **Anti-Cheat ve PC Check (Bilgisayar Kontrol)** kurallarına %100 uyumlu olarak geliştirilmiştir:

* 🚫 **Windows Hizmetleri Devre Dışı Bırakılmaz:** Windows'un hiçbir dahili sistem servisi (`services.msc`) kapatılmaz, askıya alınmaz veya bozulmaz. Custom OS gerektirmez.
* 🚫 **Defender Kapatılmaz:** Windows Defender / Gerçek Zamanlı Virüs ve Tehdit Koruması ASLA devre dışı bırakılmaz. `Defender Control` veya benzeri yasaklı yazılımlar kesinlikle bulunmaz ve kullanılmaz.
* 🚫 **Genel Uninstaller & Cleaner Değildir:** CCleaner veya şüpheli cleaner/uninstaller yazılımlarının aksine sistem loglarını veya kayıt defterini körlemesine silmez.
* 🚫 **Makro / Strafe / Key Mapping Bulunmaz:** `Keys2XInput`, `Strafe Macro`, klavye giriş hızını yapay düşüren veya tekrarlayan hiçbir donanım/yazılım emülasyonu içermez.
* 🚫 **Oyun İçi Avantaj RPF / Mod İçermez:** `No roll`, `No recoil`, `No bush`, `Mini no bush` gibi oyun bütünlüğünü bozan hiçbir RPF dosyası veya bellek enjeksiyonu barındırmaz.
* 🚫 **Yasaklı AI / Bot Kodları İçermez:** Uygulamadaki yapay zeka modülü sadece OBS bitrate ve yayın ayarlarını hesaplamak içindir; oyun süreçlerine müdahale etmez.
* ✅ **Gönül Rahatlığıyla Kullanım:** Sunucu yetkilileri veya kontrol ekibi bilgisayarınızı incelediğinde 3. Parti Kapsamında Değerlendirilen hiçbir kuralı ihlal etmez.

---

## 🎥 OBS Stüdyo & Yapay Zeka Merkezi

Uygulamanın en güçlü yanlarından biri, canlı yayıncılar için sunduğu özel OBS Stüdyo araç takımıdır:

1. **Canlı İnternet Hız Testi (Cloudflare CDN):**
   * Canlı Ping (ms), Download (Mbps) ve yayın için en kritik olan Upload (Mbps) testi.
   * Canlı ilerleme çubuğu, donmayan asenkron arka plan mimarisi.
2. **Otomatik Donanım Tespiti:**
   * İşlemci, ekran kartı mimarisi, RAM ve monitör yenileme hızını (Hz) otomatik tarar.
3. **Yapay Zeka Destekli Otomatik OBS Profil Oluşturucu:**
   * Twitch, Kick, YouTube veya Özel RTMP seçimi.
   * Gemini API anahtarı desteği (isteğe bağlı).
   * **Önemli:** API anahtarı olmasa dahi dahili **Deep Gaming AI Rule-Engine** devreye girer; upload hızınıza ve GPU mimarinize en uygun bitrate (örn. 8000 kbps), NVENC P6/P5, Tuning HQ ve çözünürlük ayarlarını hesaplar.
   * Profili doğrudan `%APPDATA%\obs-studio\basic\profiles\<ProfilAdı>\` klasörüne yazar; OBS'i açtığınızda profil seçilmeye hazırdır.
4. **Manuel OBS Profil Oluşturucu:**
   * Kodlayıcı, Bitrate, Preset (P1-P7), Tuning, Multipass, Çıkış Çözünürlüğü ve FPS değerlerini elle seçip tek tıkla OBS profili olarak kaydetme imkanı.
5. **5'li Profesyonel Yayıncı Sahne Koleksiyonu:**
   * Tek tıkla 5 sahneyi (`🎮 1 - Oyun & FiveM`, `💬 2 - Sohbet`, `⏳ 3 - Yayın Başlıyor`, `☕ 4 - Mola`, `👋 5 - Yayın Bitti`) OBS'e ekler.
   * **ReShade Güvenliği:** Oyun sahnesindeki Oyun Yakalama (Game Capture) kaynağında `capture_overlays = false` yapılmıştır; böylece ReShade ve QuantV ile OBS DXGI kancası asla çakışmaz ve oyun çökmez!

---

## 🛡️ Güvenlik & VirusTotal Taraması

Uygulama açık kaynak kodludur, hiçbir harici reklam veya zararlı kod içermez. Windows Defender ve güvenlik yazılımlarıyla tam uyumludur.

* **Dosya Adı:** `Ripleytia ST Opti V2.exe`
* **SHA-256 Dijital Parmak İzi:**
  ```text
  012d6dc2cc97c21011ca6f940857859a6d3c582307904ae709b629e108978fe8
  ```
* **VirusTotal Raporu:** [VirusTotal Doğrulama Bağlantısı](https://www.virustotal.com/gui/file/012d6dc2cc97c21011ca6f940857859a6d3c582307904ae709b629e108978fe8)

---

## 🚀 Kurulum ve Çalıştırma

### Yöntem 1: Hazır `.exe` İle Çalıştırma (Önerilen)
1. [Releases](../../releases) bölümünden **`Ripleytia ST Opti V2.exe`** veya **`Ripleytia ST Opti V2.zip`** dosyasını indirin.
2. Dosyaya çift tıklayarak çalıştırın (Uygulama otomatik olarak Yönetici UAC yetkisi isteyecektir).
3. İstediğiniz ayarları tek tek veya üstteki **"🚀 Tüm Önerilenleri Uygula"** butonuyla saniyeler içinde uygulayın.

### Yöntem 2: Kaynak Koddan Çalıştırma
```powershell
# Depoyu klonlayın
git clone https://github.com/ripleytia/ripleytia-optimizasyon.git
cd ripleytia-optimizasyon

# Gerekli bağımlılıkları yükleyin
pip install customtkinter pillow requests

# Uygulamayı başlatın (Yönetici terminalinde)
python main.py
```

### Yöntem 3: Kendi `.exe` Dosyanızı Derleme
```powershell
python build_exe.py
```

---

## 📁 Proje Dizin Yapısı

```text
Ripleytia_ST_Opti_V2/
├── assets/
│   ├── icon.ico            # Windows .ico simgesi (16x16 - 256x256)
│   ├── logo.png            # 512x512 yüksek çözünürlüklü R logosu
│   ├── logo_64.png         # Pencere başlık çubuğu için 64x64 logo
│   └── bg_dark.png         # Düşük opaklıklı gothic mor arka plan
├── engine/
│   ├── hardware.py         # CIMInstance donanım tarama motoru
│   ├── speedtest.py        # Cloudflare CDN canlı hız testi motoru
│   ├── obs_engine.py       # OBS profil ve sahne koleksiyonu üreticisi
│   └── tweaks.py           # Windows Registry, BCD ve Güç ayar motoru
├── main.py                 # CustomTkinter modern grafik arayüzü
├── build_exe.py            # PyInstaller derleme betiği
├── process_assets.py       # Varlık ve ikon işleme betiği
└── README.md               # Detaylı dokümantasyon
```

---

## ⚠️ Sorumluluk Reddi (Disclaimer)

Bu uygulama sistem dosyalarını silmez veya bozmaz. Yalnızca Windows'un resmi API'lerini, Kayıt Defteri (Registry) anahtarlarını ve `powercfg` parametrelerini kullanır. Olası her duruma karşı uygulama içerisindeki **"💾 Geri Yükleme Noktası"** butonunu kullanarak sisteme müdahale etmeden önce geri yükleme noktası almanız önerilir.

---

## 👤 Geliştirici & Lisans

* **Geliştirici:** Ripleytia
* **Lisans:** [MIT License](LICENSE)
* **Destek & Geri Bildirim:** Her türlü öneri, hata bildirimi veya katkı için lütfen bir [Issue](../../issues) veya [Pull Request](../../pulls) açmaktan çekinmeyin!
