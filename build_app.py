import subprocess
import sys
import os

def build_app():
    """Tự động đóng gói ứng dụng với cấu hình cấp cao."""
    print("Initiating PyInstaller secure build script...")
    
    # Kiểm tra đường dẫn thư mục tài nguyên
    assets_dir = "assets"
    db_dir = "database"
    
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print("Created empty assets directory.")
        
    command = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",         # Xoá dist/ thư mục build cũ
        "--windowed",          # Tắt console cho Win/Mac
        "--name=ECUS_MSDS_Mini_ERP",
        "--add-data=assets;assets",   # Link QSS 
        "--add-data=database;database",
        "main.py"
    ]
    
    try:
        subprocess.run(command, check=True)
        print("Build thành công! Thư mục ứng dụng đóng gói nằm ở: '/dist/ECUS_MSDS_Mini_ERP'")
    except subprocess.CalledProcessError as e:
        print(f"Build lỗi gián đoạn! Vui lòng tra cứu: {e}")

if __name__ == "__main__":
    build_app()
