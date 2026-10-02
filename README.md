# ⚡ Ripleytia Advanced Windows Tweak & Streamer Ecosystem Tool (v2.1)

<p align="center">
  <img src="assets/logo.png" width="160" alt="Ripleytia Logo" />
</p>

<p align="center">
  <b>Canlı Yayıncılar ve Rekabetçi Oyuncular İçin Gelişmiş Windows 11 & OBS Studio Optimizasyon Merkezi</b><br>
  <i>Sıfır Giriş Gecikmesi • %1 Low FPS Kararlılığı • Performans Artışı (Overdrive) • Modüler Hizmetler • Yapay Zeka Destekli OBS Profili</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011%20(64--bit)-blue?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-blueviolet?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/UI-CustomTkinter-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Windows%20Defender-Temiz%20(0%20Tehdit)-brightgreen?style=for-the-badge&logo=windows" />
  <img src="https://img.shields.io/badge/Sürüm-v2.1%20(Overdrive%20Edition)-purple?style=for-the-badge" />
</p>

---

## 📖 Genel Bakış

**Ripleytia Advanced Windows Tweak & Streamer Ecosystem Tool (v2.1)**, oyun oynarken aynı anda OBS Studio, Discord, müzik ve ses yönlendirme yazılımları kullanan yayıncıların ve espor oyuncularının karşılaştığı tüm performans ve gecikme darboğazlarını ortadan kaldırmak için geliştirilmiş bağımsız bir optimizasyon merkezidir.

Standart "kör debloat" araçlarının aksine, bu uygulama ses sürücülerini veya güvenlik katmanlarını bozmaz. **Her ayarın yanında ne işe yaradığı, sisteme sağladığı somut avantaj ve varsa dikkat edilmesi gereken uyarılar açıkça listelenmiştir**. Yapılan her ayar tek tıkla orijinal haline **Geri Alınabilir**.

---

## 🚀 Sürüm 2.1 ile Gelen Temel Yenilikler

### 1. 🔥 Yeni "Performans Artışı" (Performance Boost / Overdrive) Bölümü
Donanımının tüm sınırlarını zorlamak ve oyun içi minimum FPS (%1 Low FPS) değerlerini tavan yaptırmak isteyenler için özel olarak tasarlandı:
* **Çekirdek Parkı Devre Dışı (Core Unparking %100):** İşlemcinin hiçbir çekirdeği uyku moduna geçmez; tüm mantıksal iş parçacıkları her an maksimum frekansta hazır bekler.
* **Maksimum Turbo Saat Hızı Kilidi (Min %100 / Max %100):** İşlemcinin frekans düşürmesini (downclock) kapatır; ani çatışmalardaki mikro takılmaları engeller.
* **Win32PrioritySeparation = 26 (Hex):** Ön plandaki aktif oyuna en kısa ve en değişken CPU dilimini tahsis ederek klavye/fare giriş gecikmesini (input lag) sıfırlar.
* **Dinamik Zamanlayıcı & HPET Sabitleme:** İşlemci ile işletim sistemi arasındaki zamanlama kaymalarını önler, mikro-saniye hassasiyetinde timer sağlar.
* **Fare İvmesi ve Smoothing Filtrelerini Nötrleme:** 1:1 saf donanım sensör takibi sağlar.
* **GPU Maksimum Performans Modu:** Grafik kartının hafif sahnelerde boşta saat hızına düşmesini engeller.

> [!CAUTION]
> **🌡️ Sıcaklık ve Güç Tüketimi Uyarısı:**
> Bu bölümdeki ayarlar donanımın güç tasarrufu durumlarını kısıtladığı için **artan çalışma sıcaklıklarına** ve **daha yüksek güç tüketimine** yol açar. Yetersiz soğutmalı kasalarda veya dizüstü (laptop) bilgisayarlarda donanım sıcaklıklarının takip edilmesi önemle önerilir.

---

### 2. 🛠️ Windows Hizmet (Service) Optimizasyonları Yeniden Eklendi
Topluluk talepleri doğrultusunda Windows'un arka planda boş yere RAM ve işlemci tüketen gereksiz servisleri modüler olarak yönetilebilir hale getirildi:
* **DiagTrack & dmwappushservice:** Telemetri ve arka plan tanılama veri toplayıcıları kapatılır.
* **Windows Search (WSearch):** Sürekli disk indeksleme döngüsünü durdurur, SSD ömrünü ve oyun içi anlık okuma tepkisini korur.
* **Print Spooler:** Yazıcı kullanmayan sistemlerde fazladan bellek ve port kullanımını sonlandırır.
* **Fax, RemoteRegistry ve WerSvc:** Eski ve gereksiz arka plan servislerini durdurur.

> [!WARNING]
> **⚠️ FiveM & Katı Anti-Cheat (PC Check) Uyarı Bildirimi:**
> Rekabetçi FiveM ve espor sunucularındaki manuel yetkili kontrollerinde (PC Check), *"Windows hizmetlerinin devre dışı bırakılması / Tweak"* kural ihlali olarak değerlendirilebilmektedir.
> * Eğer FiveM yetkili kontrolü olan sunucularda oynuyorsanız bu sekmedeki hizmetleri varsayılanda (Açık) bırakmanız veya **"🚀 Önerilenleri Uygula (Safe)"** profilinde kalmanız önemle tavsiye edilir!
> * Genel oyunlar (CS2, Valorant, Apex vb.) için hizmet optimizasyonları tamamen güvenlidir.

---

### 3. 🧹 Standby & Çalışma Kümesi RAM Temizleyici (0 ms)
* Bellek & Disk sekmesine eklenen yerel araç sayesinde, üçüncü parti yazılımlara ihtiyaç duymadan Windows'un önbellekte unuttuğu Standby belleği tek tıkla boşaltabilir ve anında fiziksel RAM alanı açabilirsiniz.

---

### 4. ⚡ Konsolsuz, Sıfır Gecikmeli Saf Win32 Mimarisi
* Uygulamanın tüm donanım tespiti ve süreç denetimleri saf **Win32 API (Kayıt Defteri & Ctypes)** mimarisine geçirilmiştir.
* Başlangıçta veya arka plan taramalarında **hiçbir PowerShell veya CMD siyah penceresi açılmaz / yanıp sönmez**.

---

## 🎯 Diğer Sistem Optimizasyonları

* **Güç & İşlemci:** Nihai Performans Planı, Ryzen Frekans ve Soğutma Modu, Aktif Soğutma Politikası, USB Selective Suspend Kapatma, PCIe ASPM Kapatma.
* **Grafik & Görüntü:** HAGS (Donanım Hızlandırmalı GPU Zamanlaması), Pencereli Oyun İyileştirmeleri (SwapEffectUpgrade), VRR Global, GameDVR İptali, Windows Oyun Modu.
* **Bellek & Disk:** 16 GB Bellek Çökme Koruması (`DisablePagingExecutive = 0`), IoPageLockLimit (8 MB), NTFS 8.3 & Son Erişim Kapatma, Hibernation Kapatma (16-32 GB disk tasarrufu).
* **Ağ & Düşük Gecikme:** Nagle Algoritması Kapatma (`TCPNoDelay` & `TcpAckFrequency`), Multimedya Ağ Kısıtlaması Kaldırma (`NetworkThrottlingIndex`), MMCSS Ses & Oyun Öncelikleri, TCP CUBIC.
* **FiveM Özel:** Bellek Havuzu Artırımı (CitizenFX.ini `TxdStore 32000`), GTA V `commandline.txt`, Windows Defender Oyun & Yayın Dışlamaları.
* **OBS Studio Merkezi:** Cloudflare CDN canlı hız testi (Ping, Jitter, Download, Upload), Yapay Zeka destekli OBS profil üreticisi, 5'li hazır yayıncı sahne paketi.

---

## 🔐 Güvenlik & Dosya Doğrulama

Uygulama açık kaynak kodludur, hiçbir reklam veya zararlı yazılım içermez.

* **Dosya Adı:** `Ripleytia ST Opti V2.exe`
* **SHA-256 Özeti:**
  ```text
  c9ef0a187a0287321aaaffc0127ab0ccce06796f6029475e25f9514d06e8320d
  ```
* **Windows Defender Taraması:** `MpCmdRun.exe` ile taranmış ve **0 Tehdit (Clean - Found no threats)** olarak onaylanmıştır.
* **VirusTotal Raporu:** [VirusTotal Doğrulama Bağlantısı](https://www.virustotal.com/gui/file/c9ef0a187a0287321aaaffc0127ab0ccce06796f6029475e25f9514d06e8320d)

---

## 🚀 Kurulum ve Çalıştırma

### Yöntem 1: Hazır `.exe` İle Çalıştırma (Önerilen)
1. [Releases](../../releases) bölümünden **`Ripleytia ST Opti V2.exe`** veya **`Ripleytia ST Opti V2.zip`** dosyasını indirin.
2. Dosyaya çift tıklayarak çalıştırın (Uygulama otomatik olarak Yönetici UAC yetkisi isteyecektir).
3. Üstteki **"🚀 Önerilenleri Uygula (Safe)"** veya **"🔥 Ekstrem Overdrive"** butonuyla dilediğiniz profili saniyeler içinde uygulayın.

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
│   ├── hardware.py         # Saf Win32 (Ctypes + Registry) donanım motoru (0 ms)
│   ├── speedtest.py        # Cloudflare CDN canlı hız testi motoru
│   ├── obs_engine.py       # OBS profil ve sahne koleksiyonu üreticisi
│   └── tweaks.py           # Overdrive, Hizmetler, Güç ve Ağ ayar motoru
├── main.py                 # CustomTkinter modern grafik arayüzü (v2.1)
├── build_exe.py            # PyInstaller derleme ve ZIP paketleme betiği
├── version_info.txt        # Windows PE binary sürüm bilgisi (v2.1.0)
└── README.md               # Detaylı dokümantasyon
```

---

## 👤 Geliştirici & Lisans

* **Geliştirici:** Ripleytia
* **Lisans:** [MIT License](LICENSE)
* **Destek & Geri Bildirim:** Her türlü öneri, hata bildirimi veya katkı için lütfen bir [Issue](../../issues) açmaktan çekinmeyin!


## 🚀 V2 Büyük Güncellemesi (Ekim 2026)

Bu sürüm ile Ripleytia Optimizer tamamen akıllandı ve kullanıcı deneyimi mükemmelleştirildi!

**Yenilikler:**
- **🤖 Yapay Zeka (AI) Tweak Asistanı:** Yüklü olan oyunlarınızı (Steam, Epic Games, Riot Games) otomatik tespit eden ve istediğiniz performansa göre en doğru, %100 güvenli ayarları listeleyip onayınızla uygulayan devasa bir asistan sekmesi eklendi!
- **🧐 "Otomatik Uygulama" Yanılgısı Giderildi:** Uygulama artık açılışta hiçbir ayarı kendi kendine uygulamaz. "AKTİF" yazan ibareler, sadece o ayarın halihazırda Windows'unuzda yapıldığını gösterir. Artık kontrol tamamen sizde.
- **🛡️ Yeni Servis ve Tweakler:** SysMain (Superfetch) ve gereksiz Xbox Live arka plan servislerini tek tıkla kapatabilme özellikleri eklendi.
- **📝 Detaylı Açıklamalar:** Eklenen tüm yeni tweaklerin teknik açıklamaları, avantajları ve dezavantajları eklendi.
