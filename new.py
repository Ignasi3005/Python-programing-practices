import sys 
import math
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QWidget,QGridLayout,QVBoxLayout,QLineEdit,QPushButton
from PySide6.QtGui import QFont

#APP
app=QApplication(sys.argv)
font=QFont("Arial",34,QFont.Bold)
#Main window
window=QWidget()
window.setWindowTitle("MECHANICS")
window.resize(1200,700)
expression=""

#Display
display=QLineEdit()
display.setReadOnly(True)
display.setText("0")
display.setAlignment(Qt.AlignRight)
display.setFixedHeight(100)

#Buttons
grid=QGridLayout()
grid.addWidget(display,0,0,1,4)
button=[("1",0,0),("0",0,1),("5",0,2),
        ("tan",1,0),("cos",1,1),("sin",1,2),
        ("1",2,0),("log",2,1),("C",2,2),
        ("sqrt",3,0),("x",3,1),("=",3,2)]
def click(text):
    global expression,last_was_function
    if text=="C":
        expression=""
        display.clear()
    elif text=="=":
        try:
            result=eval(expression)
            display.setText(str(result))
            expression=str(result)
        except:
            display.setText("Error")
            expression=""
    elif text in ["sin","cos","tan","sqrt","log"]:
        expression +=text + "("
        last_was_function=True
        display.setText(expression)
        if text=="=":
            while expression.count("(") > expression.count(")"):
                expression +=")"
                try:
                    result=str(eval(expression,{"__builtins__": None},math.__dict__))
                    display.setText(result)
                    expression=result
                except:
                    display.setText("ERROR")
                    expression=""
    elif text=="x":
        value="*"
        expression +=value
        display.setText(str(expression))
    else:
        expression +=text
        display.setText(expression)
for text,row,col in button:
    btn=QPushButton(text)
    btn.setFont(font)
    btn.setFixedSize(400,100)
    btn.clicked.connect(lambda checked,t=text:click(t))
    grid.addWidget(btn,row,col)

#Main layout
main_layout=QVBoxLayout()
main_layout.addWidget(display)
main_layout.addLayout(grid)
window.setLayout(main_layout)
#Run
window.show()
app.exec()