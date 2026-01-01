import sys
from PySide6.QtWidgets import QApplication,QLabel 
#CREAT APPLICATION
app=QApplication(sys.argv)
#CREATE SIMPLE LABEL 
label=QLabel("Hello, PySide6!")
label.show()
#EXECUTE APPLICATION 
sys.exit(app.exec())
