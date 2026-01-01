import sys
from PySide6.QtWidgets import (QApplication,QWidget,QLineEdit,QPushButton,QGridLayout,QVBoxLayout)
from PySide6.QtCore import Qt
#Create application 
app=QApplication(sys.argv)
#MAIN WINDOW
window=QWidget()
window.setWindowTitle("MY LORD")
window.resize(1200,700)
##OUTPUT
display=QLineEdit()
display.setReadOnly(True)
display.setText("0")
display.setAlignment(Qt.AlignRight)
grid=QGridLayout()
#INPUTS
def clicks(text):
    current=display.text()
    if current=="0":
        display.setText(text)
    else: display.setText(current+text)
button=[("1",0,0),("2",0,1),("3",0,2),
        ("4",1,0),("5",1,1),("6",1,2),
        ("7",2,0),("8",2,1),("9",2,2),
        ("x",0,3),("0",0,4),("+",0,5),
        ("4",1,3),("5",1,4),("6",1,5),
        ("4",2,3),("5",2,4),("6",2,5)
        ]
for text,row,col in button:
    btn=QPushButton(text)
    btn.clicked.connect(lambda _,t=text:clicks(t))
    grid.addWidget(btn,row,col)
#Main layout
main_layout=QVBoxLayout()
main_layout.addWidget(display)
main_layout.addLayout(grid)
window.setLayout(main_layout)

window.show()

app.exec()