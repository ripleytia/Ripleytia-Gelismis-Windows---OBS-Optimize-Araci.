# -*- coding: utf-8 -*-
import os
import subprocess
import ctypes
from ctypes import wintypes
import winreg

HKLM = winreg.HKEY_LOCAL_MACHINE
HKCU = winreg.HKEY_CURRENT_USER

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def _get_silent_flags():
    """Konsol penceresi yanıp sönmesini engelleyen bayraklar."""
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  # SW_HIDE
    return creationflags, startupinfo

def run_cmd(cmd):
    """Komut istemi komutunu tamamen sessizce (0 konsol penceresi) çalıştırır."""
    try:
        flags, sinfo = _get_silent_flags()
        r = subprocess.run(
            cmd,
            capture_output=True,
            shell=True,
            timeout=30,
            creationflags=flags,
            startupinfo=sinfo
        )
        out = (r.stdout or b"").decode("utf-8", errors="replace") + (r.stderr or b"").decode("utf-8", errors="replace")
        return out.strip()
    except Exception as e:
        return f"HATA: {e}"

def run_ps(ps_code):
    """PowerShell komutunu tamamen sessizce (0 pencere) çalıştırır."""
    try:
        flags, sinfo = _get_silent_flags()
        r = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_code],
            capture_output=True,
            timeout=30,
            creationflags=flags,
            startupinfo=sinfo
        )
        out = (r.stdout or b"").decode("utf-8", errors="replace") + (r.stderr or b"").decode("utf-8", errors="replace")
        return out.strip()
    except Exception as e:
        return f"HATA: {e}"

def reg_get(hive, path, name):
    try:
        with winreg.OpenKey(hive, path) as k:
            v, _ = winreg.QueryValueEx(k, name)
            return v
    except OSError:
        return None

def reg_set(hive, path, name, val, kind="dword"):
    try:
        with winreg.CreateKey(hive, path) as k:
            if kind == "dword":
                t = winreg.REG_DWORD
            elif kind == "binary":
                t = winreg.REG_BINARY
            else:
                t = winreg.REG_SZ
            winreg.SetValueEx(k, name, 0, t, val)
        return True
    except OSError:
        return False

def reg_del(hive, path, name):
    try:
        with winreg.OpenKey(hive, path, 0, winreg.KEY_SET_VALUE) as k:
            winreg.DeleteValue(k, name)
        return True
    except OSError:
        return False

def clear_standby_memory():
    """
    Windows Standby (Boşta Bekleyen Önbellek) belleğini ve işlem çalışma kümelerini
    temizleyerek anında kullanılabilir fiziksel RAM alanı açar.
    """
    try:
        # Psapi EmptyWorkingSet
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi
        hProcess = kernel32.GetCurrentProcess()
        psapi.EmptyWorkingSet(hProcess)

        # Komut satırı yardımcı önbellek sıfırlaması (varsa)
        run_ps("[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()")
        return True, "Standby & Çalışma Kümesi RAM Önbelleği Başarıyla Temizlendi."
    except Exception as e:
        return False, f"Bellek temizlenirken hata: {e}"


# ==============================================================================
# TWEAK VERİTABANI (v2.1)
# ==============================================================================

TWEAKS = {
    # --------------------------------------------------------------------------
    # 0. YENİ: PERFORMANS ARTIŞI (OVERDRIVE / EXTREME BOOST)
    # --------------------------------------------------------------------------
    "perf_boost": [
        {
            "id": "boost_core_unparking",
            "title": "CPU Çekirdeklerini Tamamen Uyandırma (Core Unparking %100)",
            "desc": "Windows'un işlemci çekirdeklerini uykuya/park moduna almasını engeller (Min/Max Cores = 100%).",
            "advantage": "İşlemcinin tüm mantıksal çekirdekleri sürekli aktif kalır; oyunlarda ani sahne geçişlerindeki mikro takılmaları sıfırlar.",
            "warning": "🔥 YÜKSEK GÜÇ & SICAKLIK: Çekirdekler uyku moduna geçmeyeceğinden boşta sıcaklık 2-4°C artabilir.",
            "check": lambda: (
                "0x00000064" in run_cmd("powercfg -q scheme_current sub_processor CPMINCORES"),
                "Core Unparking: %100 Aktif"
            ),
            "apply": lambda: (
                run_cmd("powercfg -setacvalueindex scheme_current sub_processor CPMINCORES 100"),
                run_cmd("powercfg -setacvalueindex scheme_current sub_processor CPMAXCORES 100"),
                run_cmd("powercfg -setacvalueindex scheme_current sub_processor 0cc5b647-c315-45d6-a28e-475b30630784 100"),
                run_cmd("powercfg /setactive scheme_current")
            ),
            "undo": lambda: (
                run_cmd("powercfg -setacvalueindex scheme_current sub_processor CPMINCORES 5"),
                run_cmd("powercfg /setactive scheme_current")
            )
        },
        {
            "id": "boost_procthrottle_max",
            "title": "Maksimum Turbo Saat Hızı Kilidi (Min %100 / Max %100)",
            "desc": "İşlemcinin frekans düşürmesini (downclock) tamamen engeller; işlemciyi sürekli tepe saat hızında tutar.",
            "advantage": "Minimum %1 Low ve %0.1 Low FPS değerlerini zirveye taşır, çatışma anlarındaki anlık kare düşüşlerini yok eder.",
            "warning": "🔥 YÜKSEK GÜÇ & SICAKLIK: İşlemci sürekli maksimum frekansta çalışacaktır. Yetersiz soğutması olan sistemlerde ve laptoplarda önerilmez.",
            "check": lambda: (
                "0x00000064" in run_cmd("powercfg -q scheme_current SUB_PROCESSOR PROCTHROTTLEMIN"),
                "Min %100 / Max %100 Kilitli"
            ),
            "apply": lambda: (
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 100"),
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100"),
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE 2"),
                run_cmd("powercfg /setactive SCHEME_CURRENT")
            ),
            "undo": lambda: (
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 0"),
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE 1"),
                run_cmd("powercfg /setactive SCHEME_CURRENT")
            )
        },
        {
            "id": "boost_win32_priority",
            "title": "Win32PrioritySeparation = 26 (Hex) Espor Önceliği",
            "desc": "Ön plandaki aktif oyuna en kısa ve en değişken CPU çalışma dilimini (quantum) tahsis eder.",
            "advantage": "Oyun motoruna ve fare/klavye girdilerine maksimum CPU önceliği vererek giriş gecikmesini (input lag) sıfırlar.",
            "warning": "ℹ️ Arka plandaki ikincil uygulamaların (örn. render alma) işlemci payını hafifçe düşürebilir.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation") == 38,
                "Priority: 26 Hex (38 Dec)"
            ),
            "apply": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation", 38),
            "undo": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\PriorityControl", "Win32PrioritySeparation", 2)
        },
        {
            "id": "boost_dynamictick_off",
            "title": "Dinamik Tik (Dynamic Tick) & HPET Zamanlayıcı Kilidi",
            "desc": "Windows çekirdeğinin değişken zamanlayıcı tiklerini sabitleyerek mikro-saniye hassasiyetinde timer sağlar.",
            "advantage": "İşlemci ile işletim sistemi arasındaki zamanlama kaymalarını önler, fare takibi ve kamera dönüşlerinde pürüzsüzlük sağlar.",
            "warning": "ℹ️ Boşta güç tüketimini çok az artırabilir. Masaüstü oyun sistemleri için idealdir.",
            "check": lambda: (
                "yes" in run_cmd("bcdedit /enum {current}").lower() and "disabledynamictick" in run_cmd("bcdedit /enum {current}").lower(),
                "Dynamic Tick: Kapalı"
            ),
            "apply": lambda: (
                run_cmd("bcdedit /set disabledynamictick yes"),
                run_cmd("bcdedit /set useplatformclock false")
            ),
            "undo": lambda: (
                run_cmd("bcdedit /deletevalue disabledynamictick"),
                run_cmd("bcdedit /deletevalue useplatformclock")
            )
        },
        {
            "id": "boost_mouse_smoothing_off",
            "title": "Fare İvmesi ve Yumuşatma (Smoothing) Filtrelerini Nötrleme",
            "desc": "Windows masaüstü fare ivmesini ve kayıt defteri yumuşatma eğrisini (SmoothMouse Curves) tamamen sıfırlar.",
            "advantage": "1:1 saf donanım sensör takibi sağlar; nişan alırken (aim) kas hafızasının bozulmasını engeller.",
            "warning": "ℹ️ Fare hızınız ilk başta alışık olduğunuzdan farklı hissettirebilir.",
            "check": lambda: (
                reg_get(HKCU, r"Control Panel\Mouse", "MouseSpeed") == "0",
                "Fare İvmesi: Nötr"
            ),
            "apply": lambda: (
                reg_set(HKCU, r"Control Panel\Mouse", "MouseSpeed", "0", "str"),
                reg_set(HKCU, r"Control Panel\Mouse", "MouseThreshold1", "0", "str"),
                reg_set(HKCU, r"Control Panel\Mouse", "MouseThreshold2", "0", "str")
            ),
            "undo": lambda: (
                reg_set(HKCU, r"Control Panel\Mouse", "MouseSpeed", "1", "str"),
                reg_set(HKCU, r"Control Panel\Mouse", "MouseThreshold1", "6", "str"),
                reg_set(HKCU, r"Control Panel\Mouse", "MouseThreshold2", "10", "str")
            )
        },
        {
            "id": "boost_gpu_pstate",
            "title": "GPU Tercih Edilen Maksimum Performans Modu",
            "desc": "Grafik kartı sürücüsünün pencereli oyunlarda veya hafif sahnelerde boşta frekansına düşmesini engeller.",
            "advantage": "FiveM ve hafif grafikli sahnelerde GPU saat hızının ani düşmesini ve takılmaları önler.",
            "warning": "🔥 GPU boşta çalışma sıcaklığı 2-3°C artabilir.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Power", "DefaultPowerPlanType") == 1,
                "GPU Max Performance"
            ),
            "apply": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Power", "DefaultPowerPlanType", 1),
            "undo": lambda: reg_del(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers\Power", "DefaultPowerPlanType")
        }
    ],

    # --------------------------------------------------------------------------
    # 1. YENİ: HİZMETLER (SERVICES OPTIMIZATION - MODÜLER & UYARILI)
    # --------------------------------------------------------------------------
    "services": [
        {
            "id": "srv_diagtrack",
            "title": "Bağlı Kullanıcı Deneyimleri ve Telemetri (DiagTrack)",
            "desc": "Windows'un arka planda kullanım ve tanılama verilerini Microsoft sunucularına göndermesini durdurur.",
            "advantage": "Arka planda gereksiz işlemci ve disk kullanımını engeller, gizliliği artırır.",
            "warning": "⚠️ FiveM PC-Check uyarısı: Bazı yetkililer hizmet kapatmayı denetleyebilir. Şüphe durumunda 'Geri Al' ile açabilirsiniz.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\DiagTrack", "Start") == 4,
                "DiagTrack: " + ("Devre Dışı (4)" if reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\DiagTrack", "Start") == 4 else "Aktif")
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\DiagTrack", "Start", 4),
                run_cmd("sc stop DiagTrack")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\DiagTrack", "Start", 2),
                run_cmd("sc start DiagTrack")
            )
        },
        {
            "id": "srv_dmwappush",
            "title": "WAP Push Yönlendirme Hizmeti (dmwappushservice)",
            "desc": "Tanılama ve telemetri veri toplama ile ilişkili WAP push yönlendirme servisini devre dışı bırakır.",
            "advantage": "Telemetri veri hattını keser, ağ ve bellek kullanımını azaltır.",
            "warning": "⚠️ FiveM sunucularında yetkili kontrolü (PC-Check) öncesinde orijinal haline döndürülebilir.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\dmwappushservice", "Start") == 4,
                "dmwappushservice: " + ("Devre Dışı (4)" if reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\dmwappushservice", "Start") == 4 else "Aktif")
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\dmwappushservice", "Start", 4),
                run_cmd("sc stop dmwappushservice")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\dmwappushservice", "Start", 3),
                run_cmd("sc start dmwappushservice")
            )
        },
        {
            "id": "srv_wsearch",
            "title": "Windows Arama ve Dizin Oluşturucu (WSearch)",
            "desc": "Dosyaların arka planda sürekli taranıp indekslenmesini ve disk yazma işlemlerini kapatır.",
            "advantage": "NVMe SSD disk okuma/yazma döngüsünü hafifletir, oyun sırasında disk ani kullanım sıçramalarını önler.",
            "warning": "ℹ️ Dosya Gezgini'nde arama yaparken sonuçların bulunması biraz daha uzun sürebilir.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\WSearch", "Start") == 4,
                "WSearch: " + ("Devre Dışı (4)" if reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\WSearch", "Start") == 4 else "Aktif")
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\WSearch", "Start", 4),
                run_cmd("sc stop WSearch")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\WSearch", "Start", 2),
                run_cmd("sc start WSearch")
            )
        },
        {
            "id": "srv_spooler",
            "title": "Yazdırma Biriktiricisi (Print Spooler)",
            "desc": "Fiziksel yazıcı kullanmayan oyun ve yayın bilgisayarları için yazdırma alt sistemini kapatır.",
            "advantage": "Bellekte (RAM) yaklaşık 20-30 MB alan açar ve yazdırma arka plan süreçlerini sonlandırır.",
            "warning": "⚠️ Evinizde veya ofisinizde yazıcı kullanıyorsanız bu hizmeti açık tutmalısınız.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\Spooler", "Start") == 4,
                "Spooler: " + ("Devre Dışı (4)" if reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\Spooler", "Start") == 4 else "Aktif")
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\Spooler", "Start", 4),
                run_cmd("sc stop Spooler")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\Spooler", "Start", 2),
                run_cmd("sc start Spooler")
            )
        },
        {
            "id": "srv_fax",
            "title": "Faks Hizmeti (Fax)",
            "desc": "Modern bilgisayarlarda artık kullanılmayan eski faks aygıtı dinleme servisini devre dışı bırakır.",
            "advantage": "Gereksiz port ve servis dinleyicisini kapatarak sistemi hafifletir.",
            "warning": "ℹ️ Günlük oyun ve yayın kullanımına hiçbir yan etkisi yoktur.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\Fax", "Start") == 4,
                "Fax: " + ("Devre Dışı (4)" if reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\Fax", "Start") == 4 else "Aktif")
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\Fax", "Start", 4),
                run_cmd("sc stop Fax")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\Fax", "Start", 3)
            )
        },
        {
            "id": "srv_remote_reg",
            "title": "Uzak Kayıt Defteri (RemoteRegistry)",
            "desc": "Ağ üzerinden uzaktaki kullanıcıların bu bilgisayarın kayıt defterini değiştirmesini engeller.",
            "advantage": "Sistem güvenliğini ve gizliliği önemli ölçüde artırır.",
            "warning": "ℹ️ Standart ev kullanıcıları için kesinlikle kapatılması önerilir.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\RemoteRegistry", "Start") == 4,
                "RemoteRegistry: Devre Dışı"
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\RemoteRegistry", "Start", 4),
                run_cmd("sc stop RemoteRegistry")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\RemoteRegistry", "Start", 3)
            )
        },
        {
            "id": "srv_wersvc",
            "title": "Windows Hata Raporlama Hizmeti (WerSvc)",
            "desc": "Bir uygulama çöktüğünde arka planda kilitlenme dökümü oluşturup Microsoft'a raporlamayı durdurur.",
            "advantage": "Oyun çökmelerinde diske devasa bellek dökümü (crash dump) yazılmasını ve CPU kilitlenmelerini önler.",
            "warning": "⚠️ FiveM PC-Check kontrollerinde şüphe duyulmaması için istenirse açık tutulabilir.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Services\WerSvc", "Start") == 4,
                "WerSvc: Devre Dışı"
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\WerSvc", "Start", 4),
                run_cmd("sc stop WerSvc")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SYSTEM\CurrentControlSet\Services\WerSvc", "Start", 3)
            )
        }
    ],

    # --------------------------------------------------------------------------
    # 2. GÜÇ & İŞLEMCİ
    # --------------------------------------------------------------------------
    "power": [
        {
            "id": "pwr_ultimate",
            "title": "Nihai Performans (Ultimate Performance) Planı",
            "desc": "Windows'un gizli Ultimate Performance güç profilini oluşturur ve aktif eder.",
            "advantage": "En düşük giriş gecikmesi sağlar, işlemci saat hızının (clock) asla düşmemesini garanti eder.",
            "check": lambda: (
                "133ce100" in run_cmd("powercfg /list"),
                "Mevcut Plan: " + (run_ps("(powercfg /getactivescheme) -replace '.*\\((.*)\\)', '$1'").strip() or "Bilinmiyor")
            ),
            "apply": lambda: (
                run_cmd("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61"),
                run_ps("$m = (powercfg /list | Select-String 'Ultimate|Nihai').ToString().Split()[3]; if ($m) { powercfg /setactive $m }")
            ),
            "undo": lambda: (
                run_cmd("powercfg -restoredefaultschemes"),
                run_cmd("powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e")
            )
        },
        {
            "id": "pwr_ryzen_cool",
            "title": "Ryzen Soğutma & Frekans Koruma (Min %0 / Max %100)",
            "desc": "İşlemcinin boştayken serin çalışmasına izin verir, oyunda tam güç (%100) boostlar.",
            "advantage": "Ryzen 5 5600'ün masaüstünde 38-42°C serin kalmasını sağlar, fan sesini sıfırlar ve 80°C+ thermal throttling drop'larını engeller.",
            "check": lambda: (
                "0x00000000" in run_cmd("powercfg -q scheme_current SUB_PROCESSOR PROCTHROTTLEMIN"),
                "Min %0 / Max %100"
            ),
            "apply": lambda: (
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 0"),
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100"),
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE 1"),
                run_cmd("powercfg /setactive SCHEME_CURRENT")
            ),
            "undo": lambda: (
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN 5"),
                run_cmd("powercfg /setactive SCHEME_CURRENT")
            )
        },
        {
            "id": "pwr_syscoolpol",
            "title": "Aktif Soğutma Politikası (SysCoolPol = 1)",
            "desc": "İşlemci frekans kısmadan önce kasa ve işlemci fanlarını erken hızlandırır.",
            "advantage": "Sıcaklık artışlarını önceden sönümler, ağır çatışmalarda ani FPS düşüşlerini önler.",
            "check": lambda: (
                "0x00000001" in run_cmd("powercfg -q scheme_current SUB_PROCESSOR SYSCOOLPOL"),
                "Aktif Fan Soğutma"
            ),
            "apply": lambda: (
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR SYSCOOLPOL 1"),
                run_cmd("powercfg /setactive SCHEME_CURRENT")
            ),
            "undo": lambda: (
                run_cmd("powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR SYSCOOLPOL 0"),
                run_cmd("powercfg /setactive SCHEME_CURRENT")
            )
        },
        {
            "id": "pwr_usb_suspend",
            "title": "USB Seçmeli Askıya Alma Kapatma (Selective Suspend)",
            "desc": "Windows'un boştaki USB portlarını güç tasarrufu amacıyla uyku moduna almasını engeller.",
            "advantage": "Fare ve klavyede anlık yoklama (polling rate) gecikmesini sıfırlar; yayında USB mikrofon ve kamera kopmalarını yok eder.",
            "check": lambda: (
                "0x00000000" in run_cmd("powercfg -q scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226"),
                "USB Uyku Kapalı"
            ),
            "apply": lambda: (
                run_cmd("powercfg -setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0"),
                run_cmd("powercfg -setdcvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0"),
                run_cmd("powercfg /setactive scheme_current")
            ),
            "undo": lambda: (
                run_cmd("powercfg -setacvalueindex scheme_current 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 1"),
                run_cmd("powercfg /setactive scheme_current")
            )
        },
        {
            "id": "pwr_pcie_aspm",
            "title": "PCIe Link State Güç Yönetimi Kapatma (ASPM Off)",
            "desc": "Ekran kartı ve M.2 NVMe SSD'nin PCIe veriyolunun uykuya/tasarrufa geçmesini engeller.",
            "advantage": "FiveM ve açık dünya oyunlarında doku (texture) akışı sırasında oluşan micro-stutter donmalarını tamamen yok eder.",
            "check": lambda: (
                "0x00000000" in run_cmd("powercfg -q scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5"),
                "PCIe ASPM Kapalı"
            ),
            "apply": lambda: (
                run_cmd("powercfg -setacvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0"),
                run_cmd("powercfg -setdcvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0"),
                run_cmd("powercfg /setactive scheme_current")
            ),
            "undo": lambda: (
                run_cmd("powercfg -setacvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 1"),
                run_cmd("powercfg /setactive scheme_current")
            )
        }
    ],

    # --------------------------------------------------------------------------
    # 3. GPU & GÖRÜNTÜ
    # --------------------------------------------------------------------------
    "gpu": [
        {
            "id": "gpu_hags",
            "title": "Donanım Hızlandırmalı GPU Zamanlaması (HAGS)",
            "desc": "Grafik belleği ve kare kuyruğu yönetimini CPU'dan alıp GPU işlemcisine devreder.",
            "advantage": "OBS NVENC donanım kodlama gecikmesini düşürür, DLSS 3 Frame Generation desteğini açar, giriş gecikmesini azaltır.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode") == 2,
                "HwSchMode = " + str(reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode"))
            ),
            "apply": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 2),
            "undo": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode", 1)
        },
        {
            "id": "gpu_windowed_opti",
            "title": "Windows 11 Pencereli Oyun İyileştirmeleri (SwapEffectUpgrade)",
            "desc": "Pencereli ve çerçevesiz oyunları modern DXGI Independent Flip sunum modeline yükseltir.",
            "advantage": "Çerçevesiz (borderless) FiveM oynarken tam ekran gibi ultra düşük gecikme ve sıfır DWM masaüstü takılması sağlar.",
            "check": lambda: (
                "SwapEffectUpgradeEnable=1" in str(reg_get(HKCU, r"Software\Microsoft\DirectX\UserGpuPreferences", "DirectXUserGlobalSettings")),
                "SwapEffectUpgrade Aktif"
            ),
            "apply": lambda: reg_set(HKCU, r"Software\Microsoft\DirectX\UserGpuPreferences", "DirectXUserGlobalSettings", "SwapEffectUpgradeEnable=1;", "str"),
            "undo": lambda: reg_set(HKCU, r"Software\Microsoft\DirectX\UserGpuPreferences", "DirectXUserGlobalSettings", "", "str")
        },
        {
            "id": "gpu_vrr_global",
            "title": "Küresel Değişken Yenileme Hızı (Variable Refresh Rate - VRR)",
            "desc": "Windows'un yerleşik Değişken Yenileme Hızı motorunu tüm pencereli oyunlara zorlar.",
            "advantage": "Yüksek Hz (144Hz, 200Hz, 240Hz, G-Sync) monitörlerde pencere geçişlerinde yırtılma ve takılmaları önler.",
            "check": lambda: (
                reg_get(HKCU, r"Control Panel\GraphicsDrivers", "VariableRefreshRate") == 1,
                "VRR = 1"
            ),
            "apply": lambda: reg_set(HKCU, r"Control Panel\GraphicsDrivers", "VariableRefreshRate", 1),
            "undo": lambda: reg_set(HKCU, r"Control Panel\GraphicsDrivers", "VariableRefreshRate", 0)
        },
        {
            "id": "gpu_gamedvr_off",
            "title": "GameDVR & Arka Plan Kaydı İptali",
            "desc": "Windows'un arka planda sessizce 30 FPS video kaydı yapmasını ve Game Bar yakalamasını kapatır.",
            "advantage": "Ekran kartının NVENC kodlayıcısını ve video belleğini %100 OBS Studio'ya bırakır, FPS kaybını engeller.",
            "check": lambda: (
                reg_get(HKCU, r"System\GameConfigStore", "GameDVR_Enabled") == 0,
                "GameDVR Kapalı"
            ),
            "apply": lambda: (
                reg_set(HKCU, r"System\GameConfigStore", "GameDVR_Enabled", 0),
                reg_set(HKCU, r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", 0),
                reg_set(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\GameDVR", "AllowGameDVR", 0)
            ),
            "undo": lambda: (
                reg_set(HKCU, r"System\GameConfigStore", "GameDVR_Enabled", 1),
                reg_set(HKCU, r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", 1)
            )
        },
        {
            "id": "gpu_gamemode_on",
            "title": "Windows Oyun Modu (Game Mode) Aktif",
            "desc": "Windows kaynaklarını oyun çalışırken arka plan işlemlerinden öncelikli hale getirir.",
            "advantage": "Arka planda Discord, müzik veya tarayıcı açıkken oyuna tam CPU/GPU bant genişliği sağlar.",
            "check": lambda: (
                reg_get(HKCU, r"Software\Microsoft\GameBar", "AutoGameModeEnabled") == 1,
                "Game Mode Açık"
            ),
            "apply": lambda: (
                reg_set(HKCU, r"Software\Microsoft\GameBar", "AllowAutoGameMode", 1),
                reg_set(HKCU, r"Software\Microsoft\GameBar", "AutoGameModeEnabled", 1)
            ),
            "undo": lambda: (
                reg_set(HKCU, r"Software\Microsoft\GameBar", "AutoGameModeEnabled", 0)
            )
        }
    ],

    # --------------------------------------------------------------------------
    # 4. BELLEK & DİSK
    # --------------------------------------------------------------------------
    "memory": [
        {
            "id": "mem_paging_protect",
            "title": "16 GB Bellek Çökme Koruması (DisablePagingExecutive = 0)",
            "desc": "16 GB RAM sistemlerde çekirdeğin disk takas dosyasıyla dengesini korur.",
            "advantage": "FiveM ve OBS gibi yüksek bellek tüketen senaryolarda `OUT_OF_MEMORY` oyun çökmelerini engeller.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive") == 0,
                "Paging Koruma: " + str(reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive"))
            ),
            "apply": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive", 0),
            "undo": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "DisablePagingExecutive", 1)
        },
        {
            "id": "mem_iopagelock",
            "title": "Giriş/Çıkış Sayfa Kilidi Limiti (IoPageLockLimit = 8MB)",
            "desc": "Windows'un disk okuma/yazma I/O arabelleğini 8 megabayta çıkarır.",
            "advantage": "FiveM özel araç ve harita dokularının diskten hızlı okunmasını sağlar, takılmaları azaltır.",
            "check": lambda: (
                reg_get(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "IoPageLockLimit") == 8388608,
                "IoPageLock: 8 MB"
            ),
            "apply": lambda: reg_set(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "IoPageLockLimit", 8388608),
            "undo": lambda: reg_del(HKLM, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "IoPageLockLimit")
        },
        {
            "id": "mem_ntfs_opti",
            "title": "NTFS 8.3 İsimlendirme ve Son Erişim Zamanı Kapatma",
            "desc": "Dosyalara her erişildiğinde diske son erişim tarihi yazılmasını ve eski DOS 8.3 isimlerini engeller.",
            "advantage": "NVMe SSD dosya sistemi tepki süresini hızlandırır, gereksiz arka plan disk yazmalarını durdurur.",
            "check": lambda: (
                "1" in run_cmd("fsutil behavior query disablelastaccess"),
                "Son Erişim Kapalı"
            ),
            "apply": lambda: (
                run_cmd("fsutil behavior set disable8dot3 1"),
                run_cmd("fsutil behavior set disablelastaccess 1")
            ),
            "undo": lambda: (
                run_cmd("fsutil behavior set disablelastaccess 0")
            )
        },
        {
            "id": "mem_hibernation_off",
            "title": "Hazırda Bekletmeyi Kapatma (powercfg -h off)",
            "desc": "Windows hazırda bekletme (hibernation) dosyasını kapatır ve siler.",
            "advantage": "C: sürücünüzde anında 16 GB ile 32 GB arası tertemiz boş depolama alanı açar.",
            "check": lambda: (
                not os.path.exists(r"C:\hiberfil.sys"),
                "hiberfil.sys yok (16-32GB Tasarruf)"
            ),
            "apply": lambda: run_cmd("powercfg -h off"),
            "undo": lambda: run_cmd("powercfg -h on")
        }
    ],

    # --------------------------------------------------------------------------
    # 5. AĞ & DÜŞÜK PİNG
    # --------------------------------------------------------------------------
    "network": [
        {
            "id": "net_nagle_off",
            "title": "Nagle Algoritmasını Kapatma (TcpAckFrequency & TCPNoDelay)",
            "desc": "Windows'un küçük TCP ağ paketlerini biriktirip bekleterek gönderme mekanizmasını kapatır.",
            "advantage": "CS2, Valorant, FiveM ve online oyunlarda paket gecikmesini (ping) düşürür, mermi kayıt (hitreg) tepkisini iyileştirir.",
            "check": lambda: (
                "1" in run_ps("(Get-ChildItem 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces' | Get-ItemProperty -ErrorAction SilentlyContinue).TcpAckFrequency"),
                "Nagle Kapalı"
            ),
            "apply": lambda: run_ps("Get-ChildItem 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces' | ForEach-Object { New-ItemProperty -Path $_.PSPath -Name TcpAckFrequency -Value 1 -PropertyType DWord -Force; New-ItemProperty -Path $_.PSPath -Name TCPNoDelay -Value 1 -PropertyType DWord -Force; New-ItemProperty -Path $_.PSPath -Name TcpDelAckTicks -Value 0 -PropertyType DWord -Force }"),
            "undo": lambda: run_ps("Get-ChildItem 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces' | ForEach-Object { Remove-ItemProperty -Path $_.PSPath -Name TcpAckFrequency -ErrorAction SilentlyContinue; Remove-ItemProperty -Path $_.PSPath -Name TCPNoDelay -ErrorAction SilentlyContinue }")
        },
        {
            "id": "net_throttling_off",
            "title": "Multimedya Ağ Kısıtlamasını Kaldırma (NetworkThrottlingIndex)",
            "desc": "Windows'un oyun veya müzik açıkken TCP/UDP paket hızını sınırlamasını tamamen kaldırır.",
            "advantage": "Yayında OBS bitrate düşmelerini ve oyundaki anlık ping sıçramalarını önler.",
            "check": lambda: (
                reg_get(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex") == 0xFFFFFFFF,
                "Ağ Kısıtlama: Kapalı"
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex", 0xFFFFFFFF),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 0)
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "NetworkThrottlingIndex", 10),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 20)
            )
        },
        {
            "id": "net_mmcss_audio",
            "title": "MMCSS Ses Önceliği (High Priority)",
            "desc": "Windows ses zamanlayıcısının arabellek önceliğini High yapar ve arka plan kısıtlamasını kaldırır.",
            "advantage": "Yayın, oyun ve Voicemod/Sonar açıkken seste patlama, cızırtı ve gecikmeleri tamamen yok eder.",
            "check": lambda: (
                reg_get(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio", "Scheduling Category") == "High",
                "Ses Önceliği: High"
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio", "Scheduling Category", "High", "str"),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio", "SFIO Priority", "High", "str"),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio", "Background Only", "False", "str")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio", "Scheduling Category", "Medium", "str"),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Audio", "SFIO Priority", "Normal", "str")
            )
        },
        {
            "id": "net_mmcss_games",
            "title": "MMCSS Oyun Önceliği (GPU Priority = 8, Priority = 6)",
            "desc": "Windows multimedya oyun profiline maksimum GPU ve CPU işleme önceliği tanımlar.",
            "advantage": "Oyun motorunun ekran kartına veri gönderme gecikmesini azaltır.",
            "check": lambda: (
                reg_get(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority") == 8,
                "GPU Priority: 8"
            ),
            "apply": lambda: (
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", 8),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Priority", 6),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Scheduling Category", "High", "str")
            ),
            "undo": lambda: (
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", 2),
                reg_set(HKLM, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Priority", 2)
            )
        },
        {
            "id": "net_cubic",
            "title": "TCP Tıkanıklık Sağlayıcısı CUBIC",
            "desc": "Windows ağ yığınını modern internet bağlantılarına uyumlu CUBIC tıkanıklık denetimine geçirir.",
            "advantage": "Canlı yayında kararlı bitrate ve ani paket kaybı (dropped frames) koruması sağlar.",
            "check": lambda: (
                "cubic" in run_cmd("netsh int tcp show supplemental").lower(),
                "TCP CUBIC Aktif"
            ),
            "apply": lambda: run_cmd("netsh int tcp set supplemental template=custom congestionprovider=cubic"),
            "undo": lambda: run_cmd("netsh int tcp set supplemental template=custom congestionprovider=default")
        },
        {
            "id": "net_do_lan",
            "title": "Delivery Optimization LAN Modu (DODownloadMode = 1)",
            "desc": "Windows güncellemelerinin internetteki yabancı bilgisayarlarla P2P paylaşılmasını kapatır.",
            "advantage": "Oyun ortasında veya yayındayken internet yükleme (upload) bant genişliğinizin çalınmasını engeller.",
            "check": lambda: (
                reg_get(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization", "DODownloadMode") == 1,
                "DODownloadMode = 1"
            ),
            "apply": lambda: reg_set(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization", "DODownloadMode", 1),
            "undo": lambda: reg_set(HKLM, r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization", "DODownloadMode", 3)
        }
    ],

    # --------------------------------------------------------------------------
    # 6. FIVEM & OYUNLAR
    # --------------------------------------------------------------------------
    "fivem": [
        {
            "id": "fivem_pools",
            "title": "FiveM Bellek Havuzu Artırımı (CitizenFX.ini)",
            "desc": "TxdStore (32000), DrmStore (32000), FragStore (16000) havuzlarını genişletir.",
            "advantage": "Özel modlu sunucularda harita altının kaybolmasını (doku yüklenememe), model kırılmalarını ve FiveM çökmesini engeller.",
            "check": lambda: (
                "TxdStore" in run_ps("Get-Content \"$env:LOCALAPPDATA\\FiveM\\FiveM.app\\CitizenFX.ini\" -ErrorAction SilentlyContinue"),
                "Havuzlar Artırılmış"
            ),
            "apply": lambda: run_ps("""
                $cfg = "$env:LOCALAPPDATA\\FiveM\\FiveM.app\\CitizenFX.ini"
                if (Test-Path $cfg) {
                    $content = Get-Content $cfg -Raw
                    if ($content -notmatch 'PoolSizesIncrease') {
                        Add-Content -Path $cfg -Value 'PoolSizesIncrease={"TxdStore":32000, "DrmStore":32000, "FragStore":16000}'
                    }
                }
            """),
            "undo": lambda: None
        },
        {
            "id": "fivem_commandline",
            "title": "GTA V Komut Satırı Ayarları (commandline.txt)",
            "desc": "-ignoreDifferentVideoCard ve -novblank parametrelerini oluşturur.",
            "advantage": "Çoklu monitörlü sistemlerde ekran kartı algılama gecikmesini ve V-Sync çakışmalarını çözer.",
            "check": lambda: (None, "commandline.txt yapılandır"),
            "apply": lambda: run_ps("""
                $paths = @(
                    'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Grand Theft Auto V\\commandline.txt',
                    'D:\\SteamLibrary\\steamapps\\common\\Grand Theft Auto V\\commandline.txt'
                )
                foreach ($p in $paths) {
                    $dir = Split-Path $p
                    if (Test-Path $dir) {
                        Set-Content -Path $p -Value "-ignoreDifferentVideoCard`n-novblank" -Force
                    }
                }
            """),
            "undo": lambda: None
        },
        {
            "id": "fivem_defender_excl",
            "title": "Windows Defender Oyun & Yayın Dışlamaları",
            "desc": "FiveM, GTA V, OBS Studio ve Discord klasör ve işlemlerini gerçek zamanlı antivirüs taramasından muaf tutar.",
            "advantage": "Oyun içi anlık dosya okumalarında Defender'ın CPU'ya çökmesini ve takılmaları önler.",
            "check": lambda: (
                "FiveM" in run_ps("(Get-MpPreference).ExclusionProcess -join '; '"),
                "Defender İstisnaları Aktif"
            ),
            "apply": lambda: run_ps("""
                Add-MpPreference -ExclusionPath 'C:\\Program Files\\obs-studio', "$env:LOCALAPPDATA\\Discord", "$env:LOCALAPPDATA\\FiveM", 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Grand Theft Auto V', 'D:\\SteamLibrary\\steamapps\\common\\Grand Theft Auto V' -ErrorAction SilentlyContinue
                Add-MpPreference -ExclusionProcess 'obs64.exe','Discord.exe','FiveM.exe','FiveM_b2699_GTAProcess.exe','GTA5.exe' -ErrorAction SilentlyContinue
            """),
            "undo": lambda: None
        }
    ]
}

# Standart Önerilen Liste (Anti-Cheat & Safe Profili: Hizmetleri ve aşırı ısınma ayarlarını içermez)
ALL_RECOMMENDED = []
for group in ["power", "gpu", "memory", "network", "fivem"]:
    for item in TWEAKS[group]:
        ALL_RECOMMENDED.append(item)

# Ekstrem Performans Listesi (Performans Artışı grubunu da ekler)
ALL_EXTREME = []
for group in ["perf_boost", "power", "gpu", "memory", "network", "fivem"]:
    for item in TWEAKS[group]:
        ALL_EXTREME.append(item)

def create_restore_point(desc="Ripleytia_Opti_V2_1_RestorePoint"):
    return run_ps(f"Checkpoint-Computer -Description '{desc}' -RestorePointType 'MODIFY_SETTINGS'")

def restart_explorer():
    return run_ps("Stop-Process -Name explorer -Force")
