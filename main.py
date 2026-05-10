import sys
import os
import shutil
from datetime import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# 🔥 YE HAI WO FIX: Jo exe ke andar files ka rasta dhoondta hai
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller ek temporary folder banata hai jiska rasta sys._MEIPASS hota hai
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class FileOrganizerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(FileOrganizerApp, self).__init__()
        
        # 🔥 Yahan humne resource_path function use kiya hai
        ui_path = resource_path('ui_main.ui')
        uic.loadUi(ui_path, self)

        # Buttons connection (Wahi purane names)
        self.browse_btn.clicked.connect(self.get_path)
        self.organize_btn.clicked.connect(self.start_organizing)

        self.DIRECTORIES = {
            "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
            "Images": [".jpg", ".jpeg", ".png", ".gif"],
            "Videos": [".mp4", ".mkv"],
            "Music": [".mp3", ".wav"],
            "Archives": [".zip", ".rar"]
        }

    def get_path(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_selected:
            self.path_input.setText(folder_selected)
            self.status_label.setText("Folder Ready!")

    def start_organizing(self):
        target_path = self.path_input.text()
        if not target_path or not os.path.exists(target_path):
            QMessageBox.warning(self, "Error", "Invalid Path!")
            return

        self.status_label.setText("Working...")
        QtWidgets.QApplication.processEvents()

        try:
            files = [f for f in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, f))]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                dest_folder = "Others"
                for folder, extensions in self.DIRECTORIES.items():
                    if ext in extensions:
                        dest_folder = folder
                        break
                
                dest_path = os.path.join(target_path, dest_folder)
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path)
                shutil.move(os.path.join(target_path, file), os.path.join(dest_path, file))

            self.status_label.setText("Done!")
            QMessageBox.information(self, "Success", "Organization Complete!")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())