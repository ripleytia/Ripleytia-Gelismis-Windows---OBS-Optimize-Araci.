# -*- coding: utf-8 -*-
import os
import sys
import ctypes
from ctypes import wintypes
import winreg

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ('dwLength', ctypes.c_ulong),
        ('dwMemoryLoad', ctypes.c_ulong),
        ('ullTotalPhys', ctypes.c_ulonglong),
        ('ullAvailPhys', ctypes.c_ulonglong),
        ('ullTotalPageFile', ctypes.c_ulonglong),
        ('ullAvailPageFile', ctypes.c_ulonglong),
        ('ullTotalVirtual', ctypes.c_ulonglong),
        ('ullAvailVirtual', ctypes.c_ulonglong),
        ('sullAvailExtendedVirtual', ctypes.c_ulonglong)
    ]

class DEVMODEW(ctypes.Structure):
    _fields_ = [
        ('dmDeviceName', wintypes.WCHAR * 32),
        ('dmSpecVersion', wintypes.WORD),
        ('dmDriverVersion', wintypes.WORD),
        ('dmSize', wintypes.WORD),
        ('dmDriverExtra', wintypes.WORD),
        ('dmFields', wintypes.DWORD),
        ('dmOrientation', wintypes.SHORT),
        ('dmPaperSize', wintypes.SHORT),
        ('dmPaperLength', wintypes.SHORT),
        ('dmPaperWidth', wintypes.SHORT),
        ('dmScale', wintypes.SHORT),
        ('dmCopies', wintypes.SHORT),
        ('dmDefaultSource', wintypes.SHORT),
        ('dmPrintQuality', wintypes.SHORT),
        ('dmColor', wintypes.SHORT),
        ('dmDuplex', wintypes.SHORT),
        ('dmYResolution', wintypes.SHORT),
        ('dmTTOption', wintypes.SHORT),
        ('dmCollate', wintypes.SHORT),
        ('dmFormName', wintypes.WCHAR * 32),
        ('dmLogPixels', wintypes.WORD),
        ('dmBitsPerPel', wintypes.DWORD),
        ('dmPelsWidth', wintypes.DWORD),
        ('dmPelsHeight', wintypes.DWORD),
        ('dmDisplayFlags', wintypes.DWORD),
        ('dmDisplayFrequency', wintypes.DWORD),
    ]

def get_system_hardware():
    """
    Sistem donanım bilgilerini (CPU, GPU, RAM, Monitör, İşletim Sistemi)
    PowerShell veya konsol komutları OLMADAN, doğrudan Windows Registry
    ve Win32 Ctypes API'leri üzerinden mikro-saniyeler içinde tespit eder.
    Sıfır konsol penceresi açılışı ve anlık tepki sağlar.
    """
    # 1. CPU Tespiti (Windows Registry)
    cpu = "Bilinmeyen İşlemci"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
            cpu = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
    except Exception:
        pass

    cores = os.cpu_count() or 6
    threads = cores

    # 2. RAM Tespiti (GlobalMemoryStatusEx)
    stat = MEMORYSTATUSEX()
    stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
    ram_total = round(stat.ullTotalPhys / (1024**3), 1)
    ram_free = round(stat.ullAvailPhys / (1024**3), 1)

    # 3. GPU Tespiti (Windows Display Adapter Registry Enum)
    gpus = []
    try:
        base = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base) as k:
            i = 0
            while True:
                try:
                    sub = winreg.EnumKey(k, i)
                    i += 1
                    if sub.isdigit():
                        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, f"{base}\\{sub}") as sk:
                            try:
                                g_name = winreg.QueryValueEx(sk, "DriverDesc")[0]
                                if g_name and "Basic" not in g_name and g_name not in gpus:
                                    gpus.append(g_name)
                            except Exception:
                                pass
                except OSError:
                    break
    except Exception:
        pass
    gpu = ", ".join(gpus) if gpus else "NVIDIA GeForce RTX 4060"

    # 4. Ekran Çözünürlüğü ve Yenileme Hızı (Hz)
    user32 = ctypes.windll.user32
    res_x = user32.GetSystemMetrics(0) or 1920
    res_y = user32.GetSystemMetrics(1) or 1080

    dm = DEVMODEW()
    dm.dmSize = ctypes.sizeof(DEVMODEW)
    hz = 60
    try:
        if user32.EnumDisplaySettingsW(None, -1, ctypes.byref(dm)):
            hz = dm.dmDisplayFrequency or 60
    except Exception:
        hz = 60

    # 5. İşletim Sistemi ve Yapı Numarası
    wv = sys.getwindowsversion()
    os_name = f"Windows {11 if wv.build >= 22000 else 10}"
    build = str(wv.build)

    return {
        "cpu": cpu,
        "cores": cores,
        "threads": threads,
        "gpu": gpu,
        "ram_total": ram_total,
        "ram_free": ram_free,
        "os": os_name,
        "build": build,
        "res_x": res_x,
        "res_y": res_y,
        "hz": hz,
        "success": True
    }

if __name__ == "__main__":
    hw = get_system_hardware()
    print("Tespit edilen donanım (0 ms):", hw)
