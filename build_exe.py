import subprocess
import shutil
import zipfile
import os

print("=== Ripleytia Windows Optimizer V2.1 EXE Derlemesi Başlıyor ===")
base_dir = os.path.dirname(os.path.abspath(__file__))
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
output_name = "Ripleytia Optimizer V2"
ico_path = os.path.join(base_dir, "assets", "icon.ico")
version_path = os.path.join(base_dir, "version_info.txt")

cmd = [
    "pyinstaller",
    "--noconfirm",
    "--clean",
    "--onefile",
    "--windowed",
    "--uac-admin",
    f"--name={output_name}",
    f"--icon={ico_path}",
    f"--version-file={version_path}",
    "--collect-all=customtkinter",
    "--add-data=engine;engine",
    "--add-data=assets;assets",
    os.path.join(base_dir, "main.py")
]

print("PyInstaller Çalıştırılıyor:")
print(" ".join(cmd))
res = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True)
print("Return code:", res.returncode)

built_exe = os.path.join(base_dir, "dist", f"{output_name}.exe")
if os.path.exists(built_exe):
    dest_exe = os.path.join(desktop_path, f"{output_name}.exe")
    shutil.copy2(built_exe, dest_exe)
    print("BAŞARILI: Masaüstüne kopyalandı ->", dest_exe)

    # ZIP Arşivi oluştur
    zip_dest = os.path.join(desktop_path, f"{output_name}.zip")
    with zipfile.ZipFile(zip_dest, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(dest_exe, f"{output_name}.exe")
    print("BAŞARILI: Masaüstü ZIP oluşturuldu ->", zip_dest)
else:
    print("HATA: dist içinde exe bulunamadı!")
    print("STDOUT:", res.stdout[-1500:])
    print("STDERR:", res.stderr[-1500:])
