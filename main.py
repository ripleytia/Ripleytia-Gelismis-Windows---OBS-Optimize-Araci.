import os
import sys
import threading
import time
import ctypes
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

# Kendi modüllerimizi import ediyoruz
def get_resource_path(relative_path):
    """PyInstaller --onefile uyumlu dosya yolu çözümleyici"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.hardware import get_system_hardware
from engine.speedtest import run_speed_test
from engine.obs_engine import (
    generate_smart_profile,
    save_obs_profile,
    generate_smart_scenes,
    get_obs_profiles_dir,
    get_obs_scenes_dir
)
from engine.tweaks import (
    TWEAKS,
    ALL_RECOMMENDED,
    is_admin,
    create_restore_point,
    restart_explorer
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RipleytiaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Ripleytia — Gelişmiş Yayıncı & Oyuncu Sistemi")
        self.geometry("1120x800")
        self.minsize(1000, 700)
        self.configure(fg_color="#0b0612")

        # Global State
        self.hw_data = {}
        self.speed_data = {"ping": 0.0, "download": 0.0, "upload": 0.0}
        self.is_admin_user = is_admin()

        # Logo ve İkon Tanımlamaları
        self._set_app_icons()

        # Arka Plan Resmi (Düşük Opaklıklı Gothic Ripleytia Görseli)
        self._build_background()

        # Ana Grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_tabs()
        self._build_console()

        # Başlangıçta donanımı tara
        threading.Thread(target=self._initial_hw_scan, daemon=True).start()

    # --------------------------------------------------------------------------
    # İKON VE LOGO YÖNETİMİ
    # --------------------------------------------------------------------------
    def _set_app_icons(self):
        ico_file = get_resource_path(os.path.join("assets", "icon.ico"))
        logo_file = get_resource_path(os.path.join("assets", "logo_64.png"))

        try:
            if os.path.exists(ico_file):
                self.iconbitmap(ico_file)
        except Exception:
            pass

        try:
            if os.path.exists(logo_file):
                self.icon_photo = ImageTk.PhotoImage(Image.open(logo_file))
                self.wm_iconphoto(True, self.icon_photo)
        except Exception:
            pass

    # --------------------------------------------------------------------------
    # ARKA PLAN GÖRSELİ (DÜŞÜK OPAKLIKLI GOTHIC RIPLEYTIA WATERMARK)
    # --------------------------------------------------------------------------
    def _build_background(self):
        bg_file = get_resource_path(os.path.join("assets", "bg_dark.png"))
        if os.path.exists(bg_file):
            try:
                pil_bg = Image.open(bg_file)
                self.bg_ctk_img = ctk.CTkImage(light_image=pil_bg, dark_image=pil_bg, size=(1120, 800))
                self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_ctk_img)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            except Exception:
                pass

    # --------------------------------------------------------------------------
    # 1. BAŞLIK VE ÜST PANEL
    # --------------------------------------------------------------------------
    def _build_header(self):
        self.header_frame = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color="#150d22",
            border_width=1,
            border_color="#451e6b"
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 6))
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Logo & Başlık Kutusu
        title_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=12, pady=10, sticky="w")

        # R Logo Görseli (Sol Üst)
        logo_file = get_resource_path(os.path.join("assets", "logo_64.png"))
        if os.path.exists(logo_file):
            try:
                pil_logo = Image.open(logo_file)
                self.logo_header_img = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(46, 46))
                lbl_logo_img = ctk.CTkLabel(title_box, text="", image=self.logo_header_img)
                lbl_logo_img.pack(side="left", padx=(0, 10))
            except Exception:
                pass

        text_sub_box = ctk.CTkFrame(title_box, fg_color="transparent")
        text_sub_box.pack(side="left")

        lbl_title = ctk.CTkLabel(
            text_sub_box,
            text="RIPLEYTIA GELİŞMİŞ WINDOWS TWEAK & YAYINCI EKOSİSTEM ARACI",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#e0aaff"
        )
        lbl_title.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(
            text_sub_box,
            text="Gelişmiş Yayıncı & Oyuncu Sistemi | AMD Ryzen 5 5600 + NVIDIA RTX 4060 + 16GB RAM Özel Kalibrasyon",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#b39ddb"
        )
        lbl_sub.pack(anchor="w")

        # Sağ Hızlı Aksiyon Butonları
        actions_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        actions_box.grid(row=0, column=2, padx=12, pady=10, sticky="e")

        # Yönetici Rozeti
        if self.is_admin_user:
            adm_badge = ctk.CTkLabel(
                actions_box,
                text="🛡️ YÖNETİCİ MODU AKTİF",
                fg_color="#133820",
                text_color="#00e676",
                corner_radius=8,
                border_width=1,
                border_color="#1b5e20",
                font=ctk.CTkFont(size=11, weight="bold"),
                padx=10, pady=5
            )
            adm_badge.pack(side="left", padx=4)
        else:
            adm_btn = ctk.CTkButton(
                actions_box,
                text="⚠️ Yönetici Olarak Yeniden Başlat",
                fg_color="#3b1419",
                hover_color="#5c1d25",
                text_color="#ff5252",
                border_width=1,
                border_color="#b71c1c",
                corner_radius=8,
                font=ctk.CTkFont(size=11, weight="bold"),
                command=self._restart_as_admin
            )
            adm_btn.pack(side="left", padx=4)

        btn_all = ctk.CTkButton(
            actions_box,
            text="🚀 Tüm Önerilenleri Uygula",
            fg_color="#7b2cbf",
            hover_color="#9d4edd",
            text_color="#ffffff",
            border_width=1,
            border_color="#c77dff",
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._apply_all_recommended
        )
        btn_all.pack(side="left", padx=4)

        btn_restore = ctk.CTkButton(
            actions_box,
            text="💾 Geri Yükleme Noktası",
            fg_color="#241438",
            hover_color="#3a1e5c",
            text_color="#d8b4fe",
            border_width=1,
            border_color="#54288a",
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self._create_restore_point
        )
        btn_restore.pack(side="left", padx=4)

        btn_expl = ctk.CTkButton(
            actions_box,
            text="🔄 Explorer Yenile",
            width=90,
            fg_color="#1e1130",
            hover_color="#321b4f",
            text_color="#d8b4fe",
            border_width=1,
            border_color="#451e6b",
            corner_radius=8,
            font=ctk.CTkFont(size=11),
            command=self._restart_explorer
        )
        btn_expl.pack(side="left", padx=4)

    # --------------------------------------------------------------------------
    # 2. SEKMELER (TÜRKÇE VE GOTHIC VİOLET TASARIM)
    # --------------------------------------------------------------------------
    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(
            self,
            corner_radius=12,
            fg_color="#120a1d",
            segmented_button_fg_color="#1b102c",
            segmented_button_selected_color="#7b2cbf",
            segmented_button_selected_hover_color="#9d4edd",
            segmented_button_unselected_color="#24143a",
            segmented_button_unselected_hover_color="#361e57",
            text_color="#ffffff",
            border_width=1,
            border_color="#3d1a5e"
        )
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=14, pady=4)

        # Sekme İsimleri (Hepsi Türkçe - Anti-Cheat Uyumlu)
        self.tab_dash = self.tabview.add("📊 Gösterge Paneli")
        self.tab_power = self.tabview.add("⚡ Güç & İşlemci")
        self.tab_gpu = self.tabview.add("🎮 Grafik & Ekran")
        self.tab_mem = self.tabview.add("🧠 Bellek & Disk")
        self.tab_net = self.tabview.add("🌐 Ağ & Düşük Gecikme")
        self.tab_fivem = self.tabview.add("🎯 FiveM & Oyunlar")
        self.tab_obs = self.tabview.add("🎥 OBS Stüdyo & Yapay Zeka")

        # Sekmeleri Doldur
        self._build_dashboard_tab()
        self._build_tweak_tab(self.tab_power, "power")
        self._build_tweak_tab(self.tab_gpu, "gpu")
        self._build_tweak_tab(self.tab_mem, "memory")
        self._build_tweak_tab(self.tab_net, "network")
        self._build_tweak_tab(self.tab_fivem, "fivem")
        self._build_obs_tab()

    # --------------------------------------------------------------------------
    # 3. GÖSTERGE PANELİ (DASHBOARD)
    # --------------------------------------------------------------------------
    def _build_dashboard_tab(self):
        container = ctk.CTkScrollableFrame(self.tab_dash, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        # Donanım Kartı
        hw_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#180f27",
            border_width=1,
            border_color="#451e6b"
        )
        hw_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            hw_card,
            text="🖥️ Tespit Edilen Sistem Donanımı",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#c77dff"
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.lbl_hw_cpu = ctk.CTkLabel(hw_card, text="İşlemci (CPU): Taranıyor...", font=ctk.CTkFont(size=12), text_color="#e0d4f5")
        self.lbl_hw_cpu.pack(anchor="w", padx=18, pady=2)

        self.lbl_hw_gpu = ctk.CTkLabel(hw_card, text="Ekran Kartı (GPU): Taranıyor...", font=ctk.CTkFont(size=12), text_color="#e0d4f5")
        self.lbl_hw_gpu.pack(anchor="w", padx=18, pady=2)

        self.lbl_hw_ram = ctk.CTkLabel(hw_card, text="Bellek (RAM): Taranıyor...", font=ctk.CTkFont(size=12), text_color="#e0d4f5")
        self.lbl_hw_ram.pack(anchor="w", padx=18, pady=2)

        self.lbl_hw_os = ctk.CTkLabel(hw_card, text="İşletim Sistemi: Taranıyor...", font=ctk.CTkFont(size=12), text_color="#e0d4f5")
        self.lbl_hw_os.pack(anchor="w", padx=18, pady=2)

        self.lbl_hw_mon = ctk.CTkLabel(hw_card, text="Monitör: Taranıyor...", font=ctk.CTkFont(size=12), text_color="#e0d4f5")
        self.lbl_hw_mon.pack(anchor="w", padx=18, pady=(2, 12))

        # Ağ & Hız Durum Kartı
        net_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#180f27",
            border_width=1,
            border_color="#451e6b"
        )
        net_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            net_card,
            text="🌐 İnternet & Yayın Bağlantı Durumu",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#00e676"
        ).pack(anchor="w", padx=16, pady=(12, 4))

        self.lbl_net_summary = ctk.CTkLabel(
            net_card,
            text="Hız testi henüz çalıştırılmadı. 'OBS Stüdyo & Yapay Zeka' sekmesinden tek tıkla test yapabilirsiniz.",
            font=ctk.CTkFont(size=12),
            text_color="#b0bec5"
        )
        self.lbl_net_summary.pack(anchor="w", padx=18, pady=(2, 12))

        # Bilgi & Özet Banner
        info_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#201335",
            border_width=1,
            border_color="#5a278c"
        )
        info_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            info_card,
            text="ℹ️ Ripleytia Gelişmiş Ekosistem Motoru Hakkında",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#ffb74d"
        ).pack(anchor="w", padx=16, pady=(12, 4))

        desc = (
            "Bu araç, AMD Ryzen 5 5600 ve NVIDIA GeForce RTX 4060 sisteminizin donanımsal potansiyelini rekabetçi oyunlar "
            "ve canlı yayın sırasında sıfır takılma (0% drop) ve en yüksek %1 Low FPS kararlılığıyla çalıştırmak için kalibre edilmiştir.\n\n"
            "• Her ayarın yanında ne işe yaradığı ve sisteminize sağladığı kesin avantaj listelenmiştir.\n"
            "• Yapılan her değişiklik güvenlidir ve istediğiniz an 'Geri Al' butonuyla varsayılan haline döndürülebilir.\n"
            "• OBS sekmesinde tek tıkla hız testi yaparak donanımınıza ve upload hızınıza en uygun profili otomatik olarak OBS'e gönderebilirsiniz."
        )
        ctk.CTkLabel(info_card, text=desc, font=ctk.CTkFont(size=12), justify="left", wraplength=950, text_color="#e0d4f5").pack(anchor="w", padx=18, pady=(2, 14))

    # --------------------------------------------------------------------------
    # 4. TWEAK KARTLARI ÜRETİCİSİ (AÇIKLAMA + AVANTAJ + KONTROL + UYGULA + GERİ AL)
    # --------------------------------------------------------------------------
    def _build_tweak_tab(self, tab, group_key):
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=6, pady=6)

        items = TWEAKS.get(group_key, [])
        for item in items:
            card = ctk.CTkFrame(
                scroll,
                corner_radius=10,
                fg_color="#180f27",
                border_width=1,
                border_color="#3d1a5e"
            )
            card.pack(fill="x", pady=5, padx=4)
            card.grid_columnconfigure(0, weight=1)

            # Üst Satır: Başlık ve Durum Rozeti
            top_row = ctk.CTkFrame(card, fg_color="transparent")
            top_row.pack(fill="x", padx=14, pady=(10, 4))

            lbl_title = ctk.CTkLabel(
                top_row,
                text=item["title"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#e0aaff"
            )
            lbl_title.pack(side="left")

            st_badge = ctk.CTkLabel(
                top_row,
                text="Kontrol ediliyor...",
                fg_color="#2b1a40",
                text_color="#d8b4fe",
                corner_radius=8,
                border_width=1,
                border_color="#451e6b",
                font=ctk.CTkFont(size=11),
                padx=10, pady=3
            )
            st_badge.pack(side="right")

            # Açıklama Satırı (Ne Yapar?)
            lbl_desc = ctk.CTkLabel(
                card,
                text="📌 " + item["desc"],
                font=ctk.CTkFont(size=12),
                text_color="#d1c4e9",
                justify="left",
                wraplength=950
            )
            lbl_desc.pack(anchor="w", padx=16, pady=2)

            # Avantaj Satırı (Sağladığı Avantaj)
            lbl_adv = ctk.CTkLabel(
                card,
                text="⚡ Kazanılan Avantaj: " + item["advantage"],
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#80cbc4",
                justify="left",
                wraplength=950
            )
            lbl_adv.pack(anchor="w", padx=16, pady=(2, 6))

            # Alt Butonlar Satırı
            btn_row = ctk.CTkFrame(card, fg_color="transparent")
            btn_row.pack(fill="x", padx=14, pady=(4, 10))

            # Durum Kontrolü
            def make_check(it=item, b=st_badge):
                def worker():
                    try:
                        ok, txt = it["check"]()
                        if ok is True:
                            b.configure(text=f"AKTİF ({txt})" if txt else "AKTİF", fg_color="#133820", text_color="#00e676", border_color="#1b5e20")
                        elif ok is False:
                            b.configure(text=f"DEVRE DIŞI ({txt})" if txt else "DEVRE DIŞI", fg_color="#3b1419", text_color="#ff5252", border_color="#b71c1c")
                        else:
                            b.configure(text=txt or "BİLGİ", fg_color="#2b1a40", text_color="#d8b4fe", border_color="#451e6b")
                    except Exception:
                        b.configure(text="KONTROL EDİLEMEDİ", fg_color="#2b1a40", text_color="#9e9e9e", border_color="#451e6b")
                threading.Thread(target=worker, daemon=True).start()

            # Buton Actionları
            def make_apply(it=item, b=st_badge):
                def do():
                    self.log(f"Uygulanıyor: {it['title']}...")
                    try:
                        it["apply"]()
                        self.log(f"BAŞARILI: {it['title']} uygulandı.")
                        make_check(it, b)
                    except Exception as e:
                        self.log(f"HATA ({it['title']}): {e}")
                threading.Thread(target=do, daemon=True).start()

            def make_undo(it=item, b=st_badge):
                def do():
                    self.log(f"Geri alınıyor: {it['title']}...")
                    try:
                        it["undo"]()
                        self.log(f"GERİ ALINDI: {it['title']} varsayılana döndü.")
                        make_check(it, b)
                    except Exception as e:
                        self.log(f"HATA ({it['title']}): {e}")
                threading.Thread(target=do, daemon=True).start()

            btn_apply = ctk.CTkButton(
                btn_row,
                text="Uygula",
                width=100,
                fg_color="#7b2cbf",
                hover_color="#9d4edd",
                text_color="#ffffff",
                border_width=1,
                border_color="#c77dff",
                corner_radius=8,
                font=ctk.CTkFont(size=12, weight="bold"),
                command=make_apply
            )
            btn_apply.pack(side="left", padx=(0, 6))

            btn_undo = ctk.CTkButton(
                btn_row,
                text="Geri Al",
                width=90,
                fg_color="#241438",
                hover_color="#3a1e5c",
                text_color="#d8b4fe",
                border_width=1,
                border_color="#54288a",
                corner_radius=8,
                font=ctk.CTkFont(size=11),
                command=make_undo
            )
            btn_undo.pack(side="left")

            # İlk açılışta durum kontrolü
            make_check()

    # --------------------------------------------------------------------------
    # 5. OBS STÜDYO & YAPAY ZEKA SEKMESİ
    # --------------------------------------------------------------------------
    def _build_obs_tab(self):
        container = ctk.CTkScrollableFrame(self.tab_obs, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=6, pady=6)

        # -------------------------------------------------------------
        # KART 1: CANLI İNTERNET HIZ TESTİ
        # -------------------------------------------------------------
        speed_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#180f27",
            border_width=1,
            border_color="#3d1a5e"
        )
        speed_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            speed_card,
            text="🚀 1. Canlı İnternet Hız Testi (Cloudflare CDN Altyapısı)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#c77dff"
        ).pack(anchor="w", padx=16, pady=(12, 2))

        ctk.CTkLabel(
            speed_card,
            text="Canlı yayın için en hayati değer 'Upload' (Yükleme) hızıdır. Test yüksek hızlı küresel CDN sunucularıyla yapılır.",
            font=ctk.CTkFont(size=11),
            text_color="#b39ddb"
        ).pack(anchor="w", padx=16, pady=(0, 8))

        # Göstergeler Kutusu
        gauges_frame = ctk.CTkFrame(speed_card, fg_color="#10081c", corner_radius=8, border_width=1, border_color="#361754")
        gauges_frame.pack(fill="x", padx=16, pady=6)
        gauges_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Ping
        ping_box = ctk.CTkFrame(gauges_frame, fg_color="transparent")
        ping_box.grid(row=0, column=0, pady=10)
        ctk.CTkLabel(ping_box, text="Gecikme (Ping)", font=ctk.CTkFont(size=12), text_color="#b0bec5").pack()
        self.lbl_ping_val = ctk.CTkLabel(ping_box, text="-- ms", font=ctk.CTkFont(size=20, weight="bold"), text_color="#ffb74d")
        self.lbl_ping_val.pack()

        # Download
        dl_box = ctk.CTkFrame(gauges_frame, fg_color="transparent")
        dl_box.grid(row=0, column=1, pady=10)
        ctk.CTkLabel(dl_box, text="İndirme (Download)", font=ctk.CTkFont(size=12), text_color="#b0bec5").pack()
        self.lbl_dl_val = ctk.CTkLabel(dl_box, text="-- Mbps", font=ctk.CTkFont(size=20, weight="bold"), text_color="#4fc3f7")
        self.lbl_dl_val.pack()

        # Upload
        ul_box = ctk.CTkFrame(gauges_frame, fg_color="transparent")
        ul_box.grid(row=0, column=2, pady=10)
        ctk.CTkLabel(ul_box, text="Yükleme (Upload - Yayın)", font=ctk.CTkFont(size=12), text_color="#b0bec5").pack()
        self.lbl_ul_val = ctk.CTkLabel(ul_box, text="-- Mbps", font=ctk.CTkFont(size=20, weight="bold"), text_color="#00e676")
        self.lbl_ul_val.pack()

        # İlerleme Çubuğu ve Buton
        self.speed_progress = ctk.CTkProgressBar(speed_card, progress_color="#7b2cbf")
        self.speed_progress.pack(fill="x", padx=16, pady=(8, 4))
        self.speed_progress.set(0.0)

        self.lbl_speed_status = ctk.CTkLabel(speed_card, text="Test hazır. 'Hız Testini Başlat' butonuna tıklayın.", font=ctk.CTkFont(size=11), text_color="#b39ddb")
        self.lbl_speed_status.pack(anchor="w", padx=16, pady=2)

        self.btn_run_speed = ctk.CTkButton(
            speed_card,
            text="▶️ Hız Testini Başlat",
            fg_color="#7b2cbf",
            hover_color="#9d4edd",
            text_color="#ffffff",
            border_width=1,
            border_color="#c77dff",
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._start_speed_test
        )
        self.btn_run_speed.pack(anchor="w", padx=16, pady=(6, 12))

        # -------------------------------------------------------------
        # KART 2: YAPAY ZEKA DESTEKLİ OTOMATİK OBS PROFİLİ OLUŞTURUCU
        # -------------------------------------------------------------
        ai_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#180f27",
            border_width=1,
            border_color="#3d1a5e"
        )
        ai_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            ai_card,
            text="🤖 2. Donanım & Hız Uyumlu OBS Profil Oluşturucu (Yapay Zeka Destekli)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#c77dff"
        ).pack(anchor="w", padx=16, pady=(12, 2))

        ctk.CTkLabel(
            ai_card,
            text="Hız testi sonuçları ve RTX 4060 donanımınıza göre en optimum OBS profilini oluşturur ve doğrudan OBS profil klasörüne gönderir.",
            font=ctk.CTkFont(size=11),
            text_color="#b39ddb"
        ).pack(anchor="w", padx=16, pady=(0, 8))

        ai_form = ctk.CTkFrame(ai_card, fg_color="transparent")
        ai_form.pack(fill="x", padx=16, pady=4)
        ai_form.grid_columnconfigure((1, 3), weight=1)

        # Platform Seçimi
        ctk.CTkLabel(ai_form, text="Yayın Platformu:", text_color="#d1c4e9").grid(row=0, column=0, padx=6, pady=6, sticky="w")
        self.combo_platform = ctk.CTkComboBox(ai_form, values=["Twitch", "Kick", "YouTube", "Özel RTMP"], fg_color="#24143a", button_color="#7b2cbf")
        self.combo_platform.set("Twitch")
        self.combo_platform.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

        # Profil Adı
        ctk.CTkLabel(ai_form, text="Profil Adı:", text_color="#d1c4e9").grid(row=0, column=2, padx=6, pady=6, sticky="w")
        self.entry_profile_name = ctk.CTkEntry(ai_form, fg_color="#24143a", border_color="#54288a")
        self.entry_profile_name.insert(0, "Ripleytia AI Pro")
        self.entry_profile_name.grid(row=0, column=3, padx=6, pady=6, sticky="ew")

        # Gemini API Key (Opsiyonel)
        ctk.CTkLabel(ai_form, text="Gemini API Anahtarı (Opsiyonel):", text_color="#d1c4e9").grid(row=1, column=0, padx=6, pady=6, sticky="w")
        self.entry_gemini_key = ctk.CTkEntry(ai_form, placeholder_text="Boş bırakılırsa dahili Akıllı Kural Motoru çalışır", show="*", fg_color="#24143a", border_color="#54288a")
        self.entry_gemini_key.grid(row=1, column=1, columnspan=3, padx=6, pady=6, sticky="ew")

        # AI Butonu
        self.btn_gen_ai_profile = ctk.CTkButton(
            ai_card,
            text="⚡ Yapay Zeka Profilini Hesapla & OBS'e Gönder",
            fg_color="#7b2cbf",
            hover_color="#9d4edd",
            text_color="#ffffff",
            border_width=1,
            border_color="#c77dff",
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._generate_ai_profile
        )
        self.btn_gen_ai_profile.pack(anchor="w", padx=16, pady=(8, 6))

        self.lbl_ai_result = ctk.CTkLabel(
            ai_card,
            text="Henüz profil oluşturulmadı.",
            font=ctk.CTkFont(size=11),
            text_color="#d1c4e9",
            justify="left",
            wraplength=950
        )
        self.lbl_ai_result.pack(anchor="w", padx=16, pady=(2, 12))

        # -------------------------------------------------------------
        # KART 3: MANUEL OBS PROFİL OLUŞTURUCU (BÖLÜM 3.1)
        # -------------------------------------------------------------
        man_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#180f27",
            border_width=1,
            border_color="#3d1a5e"
        )
        man_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            man_card,
            text="🎛️ 3. Manuel OBS Profil Oluşturucu (Çıkış, Video, Gelişmiş Ayarlar)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#ffb74d"
        ).pack(anchor="w", padx=16, pady=(12, 2))

        ctk.CTkLabel(
            man_card,
            text="Tüm parametreleri kendi isteğinize göre seçip doğrudan OBS profili olarak kaydedebilirsiniz.",
            font=ctk.CTkFont(size=11),
            text_color="#b39ddb"
        ).pack(anchor="w", padx=16, pady=(0, 8))

        m_form = ctk.CTkFrame(man_card, fg_color="transparent")
        m_form.pack(fill="x", padx=16, pady=4)
        m_form.grid_columnconfigure((1, 3, 5), weight=1)

        # Satır 1: İsim & Encoder & Bitrate
        ctk.CTkLabel(m_form, text="Profil Adı:", text_color="#d1c4e9").grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.man_name = ctk.CTkEntry(m_form, fg_color="#24143a", border_color="#54288a")
        self.man_name.insert(0, "Ripleytia Özel Profil")
        self.man_name.grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(m_form, text="Kodlayıcı:", text_color="#d1c4e9").grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.man_enc = ctk.CTkComboBox(m_form, values=["obs_nvenc_h264_tex (NVIDIA)", "obs_x264 (İşlemci)", "obs_nvenc_av1_tex (AV1)"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_enc.set("obs_nvenc_h264_tex (NVIDIA)")
        self.man_enc.grid(row=0, column=3, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(m_form, text="Bitrate (kbps):", text_color="#d1c4e9").grid(row=0, column=4, padx=4, pady=4, sticky="w")
        self.man_bitrate = ctk.CTkEntry(m_form, fg_color="#24143a", border_color="#54288a")
        self.man_bitrate.insert(0, "8000")
        self.man_bitrate.grid(row=0, column=5, padx=4, pady=4, sticky="ew")

        # Satır 2: Preset & Tuning & Multipass
        ctk.CTkLabel(m_form, text="Ön Tanım (Preset):", text_color="#d1c4e9").grid(row=1, column=0, padx=4, pady=4, sticky="w")
        self.man_preset = ctk.CTkComboBox(m_form, values=["p6 (Daha Yavaş - Yüksek Kalite)", "p5 (Yavaş - İyi)", "p7 (En Yavaş - Maksimum)", "p4 (Orta)", "p1 (En Hızlı)"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_preset.set("p6 (Daha Yavaş - Yüksek Kalite)")
        self.man_preset.grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(m_form, text="Ayar (Tuning):", text_color="#d1c4e9").grid(row=1, column=2, padx=4, pady=4, sticky="w")
        self.man_tuning = ctk.CTkComboBox(m_form, values=["hq (Yüksek Kalite)", "ll (Düşük Gecikme)", "ull (Ultra Düşük Gecikme)"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_tuning.set("hq (Yüksek Kalite)")
        self.man_tuning.grid(row=1, column=3, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(m_form, text="Çoklu Geçiş:", text_color="#d1c4e9").grid(row=1, column=4, padx=4, pady=4, sticky="w")
        self.man_multipass = ctk.CTkComboBox(m_form, values=["qres (İki Geçişli Çeyrek Çözünürlük)", "fullres (İki Geçişli Tam Çözünürlük)", "disabled (Tek Geçiş)"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_multipass.set("qres (İki Geçişli Çeyrek Çözünürlük)")
        self.man_multipass.grid(row=1, column=5, padx=4, pady=4, sticky="ew")

        # Satır 3: Çıkış Çözünürlüğü & FPS & Renk
        ctk.CTkLabel(m_form, text="Çıkış Çözünürlüğü:", text_color="#d1c4e9").grid(row=2, column=0, padx=4, pady=4, sticky="w")
        self.man_res = ctk.CTkComboBox(m_form, values=["1920x1080 (1080p)", "1664x936 (936p - Keskin)", "1280x720 (720p)", "2560x1440 (2K)"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_res.set("1920x1080 (1080p)")
        self.man_res.grid(row=2, column=1, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(m_form, text="Kare Hızı (FPS):", text_color="#d1c4e9").grid(row=2, column=2, padx=4, pady=4, sticky="w")
        self.man_fps = ctk.CTkComboBox(m_form, values=["60", "59.94", "30", "120"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_fps.set("60")
        self.man_fps.grid(row=2, column=3, padx=4, pady=4, sticky="ew")

        ctk.CTkLabel(m_form, text="Gelişmiş Öncelik:", text_color="#d1c4e9").grid(row=2, column=4, padx=4, pady=4, sticky="w")
        self.man_priority = ctk.CTkComboBox(m_form, values=["AboveNormal", "High", "Normal"], fg_color="#24143a", button_color="#7b2cbf")
        self.man_priority.set("AboveNormal")
        self.man_priority.grid(row=2, column=5, padx=4, pady=4, sticky="ew")

        # Manuel Kaydet Butonu
        btn_save_man = ctk.CTkButton(
            man_card,
            text="💾 Manuel Profili OBS'e Gönder",
            fg_color="#e65100",
            hover_color="#f57c00",
            text_color="#ffffff",
            border_width=1,
            border_color="#ffb74d",
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._save_manual_profile
        )
        btn_save_man.pack(anchor="w", padx=16, pady=(8, 12))

        # -------------------------------------------------------------
        # KART 4: OTOMATİK SAHNE OLUŞTURUCU (BÖLÜM 4)
        # -------------------------------------------------------------
        scene_card = ctk.CTkFrame(
            container,
            corner_radius=10,
            fg_color="#180f27",
            border_width=1,
            border_color="#3d1a5e"
        )
        scene_card.pack(fill="x", pady=6, padx=4)

        ctk.CTkLabel(
            scene_card,
            text="🎬 4. OBS Otomatik Sahne Koleksiyonu Oluşturucu (Yayıncı Şablonu)",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#c77dff"
        ).pack(anchor="w", padx=16, pady=(12, 2))

        ctk.CTkLabel(
            scene_card,
            text="Yayıncılar için 5 profesyonel hazır sahneyi (Oyun/FiveM, Sohbet, Başlıyor, Mola, Bitti) "
                 "ve ReShade çakışması önlenmiş Oyun Yakalama kaynağını tek tıkla OBS'e ekler.",
            font=ctk.CTkFont(size=11),
            text_color="#b39ddb"
        ).pack(anchor="w", padx=16, pady=(0, 8))

        s_box = ctk.CTkFrame(scene_card, fg_color="transparent")
        s_box.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(s_box, text="Sahne Koleksiyonu Adı:", text_color="#d1c4e9").pack(side="left", padx=(0, 6))
        self.entry_scene_name = ctk.CTkEntry(s_box, width=240, fg_color="#24143a", border_color="#54288a")
        self.entry_scene_name.insert(0, "Ripleytia Pro Sahne")
        self.entry_scene_name.pack(side="left", padx=6)

        btn_make_scenes = ctk.CTkButton(
            s_box,
            text="🎬 Sahneleri Oluştur & OBS'e Gönder",
            fg_color="#7b2cbf",
            hover_color="#9d4edd",
            text_color="#ffffff",
            border_width=1,
            border_color="#c77dff",
            corner_radius=8,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._generate_scenes
        )
        btn_make_scenes.pack(side="left", padx=8)

    # --------------------------------------------------------------------------
    # 6. LOG & KONSOL ALANI
    # --------------------------------------------------------------------------
    def _build_console(self):
        console_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
            fg_color="#0e0717",
            border_width=1,
            border_color="#361754"
        )
        console_frame.grid(row=2, column=0, sticky="ew", padx=14, pady=(4, 12))

        lbl_con = ctk.CTkLabel(
            console_frame,
            text="📋 Canlı İşlem Konsolu",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#c77dff"
        )
        lbl_con.pack(anchor="w", padx=12, pady=(4, 2))

        self.txt_console = ctk.CTkTextbox(
            console_frame,
            height=90,
            fg_color="#08040d",
            text_color="#a7f3d0",
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.txt_console.pack(fill="both", expand=True, padx=8, pady=(0, 6))
        self.log("Ripleytia Gelişmiş Windows Tweak & Yayıncı Ekosistem Aracı başlatıldı. Tüm sistem modülleri aktif.")

    def log(self, msg):
        now = time.strftime("%H:%M:%S")
        self.txt_console.insert("end", f"[{now}] {msg}\n")
        self.txt_console.see("end")

    # --------------------------------------------------------------------------
    # 7. ASENKRON İŞLEMLER VE AKSİYONLAR
    # --------------------------------------------------------------------------
    def _initial_hw_scan(self):
        self.log("Donanım bileşenleri taranıyor...")
        hw = get_system_hardware()
        self.hw_data = hw

        self.lbl_hw_cpu.configure(text=f"İşlemci (CPU): {hw['cpu']} ({hw['cores']} Çekirdek / {hw['threads']} Thread)")
        self.lbl_hw_gpu.configure(text=f"Ekran Kartı (GPU): {hw['gpu']}")
        self.lbl_hw_ram.configure(text=f"Bellek (RAM): {hw['ram_total']} GB (Boş: {hw['ram_free']} GB)")
        self.lbl_hw_os.configure(text=f"İşletim Sistemi: {hw['os']} (Build {hw['build']})")
        self.lbl_hw_mon.configure(text=f"Monitör Çözünürlüğü: {hw['res_x']}x{hw['res_y']} @ {hw['hz']} Hz")
        self.log(f"Donanım tespit edildi: {hw['cpu']} | {hw['gpu']} | {hw['ram_total']} GB RAM")

    def _start_speed_test(self):
        self.btn_run_speed.configure(state="disabled", text="Test Ediliyor...")
        self.speed_progress.set(0.0)

        def worker():
            def cb(msg, pct):
                self.speed_progress.set(pct)
                self.lbl_speed_status.configure(text=msg)

            res = run_speed_test(cb)
            self.speed_data = res

            if res["status"] == "success":
                self.lbl_ping_val.configure(text=f"{res['ping']} ms")
                self.lbl_dl_val.configure(text=f"{res['download']} Mbps")
                self.lbl_ul_val.configure(text=f"{res['upload']} Mbps")
                self.lbl_net_summary.configure(
                    text=f"Ping: {res['ping']} ms | Download: {res['download']} Mbps | Upload: {res['upload']} Mbps"
                )
                self.log(f"Hız testi bitti: Ping={res['ping']}ms, DL={res['download']}Mbps, UL={res['upload']}Mbps")
            else:
                self.lbl_speed_status.configure(text=f"Test başarısız: {res.get('error')}")
                self.log(f"Hız testi hatası: {res.get('error')}")

            self.btn_run_speed.configure(state="normal", text="▶️ Hız Testini Başlat")

        threading.Thread(target=worker, daemon=True).start()

    def _generate_ai_profile(self):
        platform = self.combo_platform.get()
        pname = self.entry_profile_name.get().strip() or "Ripleytia AI Pro"
        key = self.entry_gemini_key.get().strip()

        self.btn_gen_ai_profile.configure(state="disabled", text="AI Hesaplanıyor...")
        self.log(f"Yapay Zeka Profili hesaplanıyor ({platform} için)...")

        def worker():
            try:
                cfg = generate_smart_profile(self.hw_data, self.speed_data, platform=platform, profile_name=pname, api_key=key)
                summary_text = (
                    f"✅ '{pname}' OBS Profil Dizinine Başarıyla Gönderildi!\n"
                    f"• Çözünürlük: {cfg.get('out_cx')}x{cfg.get('out_cy')} @ {cfg.get('fps')} FPS\n"
                    f"• Bitrate: {cfg.get('bitrate')} kbps | Kodlayıcı: {cfg.get('encoder')} (Preset: {cfg.get('preset2')})\n"
                    f"• Yapay Zeka Gerekçesi: {cfg.get('ai_explanation', '')}"
                )
                self.lbl_ai_result.configure(text=summary_text, text_color="#a5d6a7")
                self.log(f"BAŞARILI: '{pname}' profili OBS'e kaydedildi. ({cfg.get('bitrate')} kbps, {cfg.get('out_cy')}p60)")
                messagebox.showinfo("Başarılı", f"'{pname}' profili oluşturuldu ve OBS Studio'ya gönderildi!\nOBS Profil menüsünden seçebilirsiniz.")
            except Exception as e:
                self.lbl_ai_result.configure(text=f"Hata: {e}", text_color="#ff8a80")
                self.log(f"Yapay Zeka Profil hatası: {e}")
            finally:
                self.btn_gen_ai_profile.configure(state="normal", text="⚡ Yapay Zeka Profilini Hesapla & OBS'e Gönder")

        threading.Thread(target=worker, daemon=True).start()

    def _save_manual_profile(self):
        pname = self.man_name.get().strip() or "Ripleytia Özel"
        enc_raw = self.man_enc.get().split()[0]
        bitrate_val = int(self.man_bitrate.get().strip() or "8000")
        preset_val = self.man_preset.get().split()[0]
        tuning_val = self.man_tuning.get().split()[0]
        multipass_val = self.man_multipass.get().split()[0]
        res_raw = self.man_res.get().split()[0].split("x")
        fps_val = int(self.man_fps.get().strip() or "60")
        priority_val = self.man_priority.get()

        cfg = {
            "platform": "Özel",
            "encoder": enc_raw,
            "rate_control": "CBR",
            "bitrate": bitrate_val,
            "keyint_sec": 2,
            "preset2": preset_val,
            "tuning": tuning_val,
            "multipass": multipass_val,
            "profile": "high",
            "lookahead": False,
            "psycho_aq": True,
            "base_cx": 1920,
            "base_cy": 1080,
            "out_cx": int(res_raw[0]),
            "out_cy": int(res_raw[1]),
            "fps": fps_val,
            "scale_type": "bicubic",
            "priority": priority_val
        }

        try:
            save_obs_profile(pname, cfg)
            self.log(f"Manuel profil '{pname}' OBS dizinine kaydedildi ({bitrate_val} kbps, {res_raw[1]}p{fps_val}).")
            messagebox.showinfo("Başarılı", f"'{pname}' manuel profili OBS Studio profil klasörüne yazıldı!")
        except Exception as e:
            self.log(f"Manuel profil kayıt hatası: {e}")
            messagebox.showerror("Hata", f"Profil kaydedilemedi: {e}")

    def _generate_scenes(self):
        sname = self.entry_scene_name.get().strip() or "Ripleytia Pro Sahne"
        try:
            path = generate_smart_scenes(sname)
            self.log(f"BAŞARILI: Sahne koleksiyonu '{sname}' OBS'e aktarıldı ({path}).")
            messagebox.showinfo("Başarılı", f"'{sname}' sahne koleksiyonu başarıyla oluşturuldu!\nOBS'i açıp 'Sahne Koleksiyonu' menüsünden seçebilirsiniz.")
        except Exception as e:
            self.log(f"Sahne oluşturma hatası: {e}")
            messagebox.showerror("Hata", f"Sahne koleksiyonu oluşturulamadı: {e}")

    def _apply_all_recommended(self):
        if not messagebox.askyesno("Onay", "Tüm önerilen yayıncı ve oyuncu optimizasyonları tek tıkla uygulanacak. Onaylıyor musunuz?"):
            return

        def worker():
            self.log("=== TOPLU OPTİMİZASYON BAŞLATILDI ===")
            success_count = 0
            for item in ALL_RECOMMENDED:
                try:
                    self.log(f"Uygulanıyor: {item['title']}...")
                    item["apply"]()
                    success_count += 1
                except Exception as e:
                    self.log(f"Atlandı ({item['title']}): {e}")
            self.log(f"=== TAMAMLANDI: {success_count}/{len(ALL_RECOMMENDED)} ayar başarıyla uygulandı ===")
            messagebox.showinfo("Tamamlandı", f"{success_count} adet optimizasyon başarıyla uygulandı!\nDeğişikliklerin tam aktif olması için bilgisayarınızı 1 kez yeniden başlatmanız önerilir.")

        threading.Thread(target=worker, daemon=True).start()

    def _create_restore_point(self):
        def worker():
            self.log("Sistem Geri Yükleme Noktası oluşturuluyor...")
            out = create_restore_point()
            self.log(f"Geri yükleme noktası sonucu: {out or 'Tamamlandı'}")
            messagebox.showinfo("Geri Yükleme", "Sistem Geri Yükleme Noktası başarıyla oluşturuldu.")
        threading.Thread(target=worker, daemon=True).start()

    def _restart_explorer(self):
        def worker():
            self.log("Explorer yeniden başlatılıyor...")
            restart_explorer()
            self.log("Explorer yeniden başlatıldı.")
        threading.Thread(target=worker, daemon=True).start()

    def _restart_as_admin(self):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
            sys.exit(0)
        except Exception as e:
            messagebox.showerror("Hata", f"Yönetici olarak başlatılamadı: {e}")

if __name__ == "__main__":
    app = RipleytiaApp()
    app.mainloop()
