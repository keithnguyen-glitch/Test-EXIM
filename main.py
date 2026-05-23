import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from database.db_manager import DatabaseManager
from core.utils import get_resource_path

def main():
    app = QApplication(sys.argv)
    
    # 1. Đọc Theme QSS bảo mật offline
    qss_path = get_resource_path("assets/theme.qss")
    if os.path.exists(qss_path):
        with open(qss_path, 'r', encoding='utf-8') as f:
            app.setStyleSheet(f.read())

    # 2. Base Security Init Layer
    # Database tự đồng bô backup ra nhánh temp khi khởi động
    db = DatabaseManager()

    # 3. Main Windows View Builder
    window = MainWindow(db)
    window.show()
    
    # Kết thúc Thread Life Cycle
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
