import sys 
import math
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import QPushButton,QVBoxLayout,QApplication,QGridLayout,QWidget,QLineEdit
from PySide6.QtGui import QFont

#APP
app=QApplication(sys.argv)
font=QFont("Arial",34,QFont.Bold)

#Main window
window=QWidget()
window.setWindowTitle("MASTERMIND")
window.resize(1200,600)
expression=""


#Display
display=QLineEdit()
display.setReadOnly(True)
display.setText("0")
display.setAlignment(Qt.AlignRight)
display.setFixedHeight(100)

##Buttons
grid=QGridLayout()
grid.addWidget(display,0,0,1,4)


button=[("1",0,0),("x",0,1),("1",0,2),
        ("=",1,0),("C",1,1),("sin",1,2),
        ("1",2,0),("1",2,1),("1",2,2),
        ("1",3,0),("x",3,1),("1",3,2),
        ("😂",4,0),("∭",4,1),("C",4,2),
        ("1",5,0),("1",5,1),("1",5,2),
        ("1",6,0),("x",6,1),("1",6,2)]
def clicks(text):
    global expression
    if text=="C":
        expression=""
        display.clear()
    elif text == "=":
        try:
            result=str(eval(expression))
            display.setText(str(result))
            expression=str(result)
        except:
            display.setText("error")
            expression="" 
    else:
        expression +=text
        display.setText(expression)
for text,row,col in button:
    btn=QPushButton(text)
    btn.setFont(font)
    btn.setFixedSize(400,100)
    btn.clicked.connect(lambda checked,t=text:clicks(t))
    grid.addWidget(btn,row,col)


##Main layout
main_layout=QVBoxLayout()
main_layout.addWidget(display)
main_layout.addLayout(grid)
window.setLayout(main_layout)

##Run
window.show()
app.exec()
