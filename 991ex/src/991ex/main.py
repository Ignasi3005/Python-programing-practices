"""Minimal PySide6 app for 991Ex scaffold with SymPy integration.

Run: python src/991ex/main.py
"""
import sys
import re
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QSplitter, QGridLayout, QSizePolicy
)
from PySide6.QtCore import Qt

import sympy as sp


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("991Ex — Scientific & Symbolic Calculator")
        self.resize(900, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Expression bar
        expr_layout = QHBoxLayout()
        self.expr_edit = QLineEdit()
        self.expr_edit.setPlaceholderText("Enter expression or symbolic command, e.g. simplify(x^2 + 2*x + 1) or integrate(sin(x), (x,0,pi))")
        expr_layout.addWidget(QLabel("Expression:"))
        expr_layout.addWidget(self.expr_edit)

        btn_eval = QPushButton("Evaluate (Numeric)")
        btn_sym = QPushButton("Symbolic")
        btn_eval.clicked.connect(self.on_evaluate)
        btn_sym.clicked.connect(self.on_symbolic)
        expr_layout.addWidget(btn_eval)
        expr_layout.addWidget(btn_sym)

        layout.addLayout(expr_layout)

        # Keep last answer
        self.last_ans = ''
        self.expr_edit.returnPressed.connect(self.on_evaluate)

        # Button grid (calculator keypad)
        keypad = QWidget()
        grid = QGridLayout(keypad)
        buttons = [
            ('7','7'),('8','8'),('9','9'),('/','/'),('sqrt','sqrt('),
            ('4','4'),('5','5'),('6','6'),('*','*'),('^','**'),
            ('1','1'),('2','2'),('3','3'),('-','-'),('(','('),
            ('0','0'),('.','.'),('ANS','ANS'),('+','+'),(')',')'),
            ('sin','sin('),('cos','cos('),('tan','tan('),('log','log('),('ln','ln('),
            ('pi','pi'),('e','E'),('!','factorial('),('DEL','DEL'),('CLR','CLR')
        ]
        cols = 5
        r = 0
        c = 0
        for text, insert in buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(lambda checked, ins=insert, t=text: self.on_button_pressed(ins, t))
            grid.addWidget(btn, r, c)
            c +=1
            if c >= cols:
                c = 0
                r +=1

        layout.addWidget(keypad)

        # Splitter: history | result
        splitter = QSplitter(Qt.Horizontal)

        self.history = QListWidget()
        self.history.setMaximumWidth(350)
        splitter.addWidget(self.history)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        self.result_view = QTextEdit()
        self.result_view.setReadOnly(True)
        right_layout.addWidget(QLabel("Result"))
        right_layout.addWidget(self.result_view)
        self.ans_label = QLabel("ANS: ")
        right_layout.addWidget(self.ans_label)

        splitter.addWidget(right)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)

    def add_history(self, expr, out):
        item = QListWidgetItem(f"> {expr}\n= {out}")
        self.history.insertItem(0, item)
        # update ANS label
        try:
            self.last_ans = str(out)
            self.ans_label.setText(f"ANS: {self.last_ans}")
        except Exception:
            pass

    def on_button_pressed(self, insert, text):
        if insert == 'DEL':
            cur = self.expr_edit.text()
            self.expr_edit.setText(cur[:-1])
        elif insert == 'CLR':
            self.expr_edit.clear()
        elif insert == 'ANS':
            # insert last answer literal
            cur = self.expr_edit.text()
            self.expr_edit.setText(cur + (self.last_ans or ''))
        else:
            # insert at cursor position
            pos = self.expr_edit.cursorPosition()
            cur = self.expr_edit.text()
            new = cur[:pos] + insert + cur[pos:]
            self.expr_edit.setText(new)
            self.expr_edit.setCursorPosition(pos + len(insert))

    def keyPressEvent(self, event):
        # Enter to evaluate, Ctrl+S for symbolic, Esc to clear, Backspace handled by default
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.on_evaluate()
            return
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.on_symbolic()
            return
        if event.key() == Qt.Key_Escape:
            self.expr_edit.clear()
            return
        super().keyPressEvent(event)

    def _parse_symbolic_command(self, expr: str):
        # Matches name(inner) optionally with extra args
        m = re.match(r"^(\w+)\((.*)\)\s*$", expr.strip(), re.S)
        if not m:
            return None
        name = m.group(1)
        inner = m.group(2)
        return name, inner

    def on_symbolic(self):
        expr = self.expr_edit.text().strip()
        if not expr:
            return
        try:
            cmd = self._parse_symbolic_command(expr)
            if cmd:
                name, inner = cmd
                if name == "simplify":
                    res = sp.simplify(sp.sympify(inner))
                elif name == "factor":
                    res = sp.factor(sp.sympify(inner))
                elif name == "diff":
                    # diff(expr, var) or diff(expr)
                    args = [a.strip() for a in inner.split(",")]
                    if len(args) == 1:
                        res = sp.diff(sp.sympify(args[0]))
                    else:
                        res = sp.diff(sp.sympify(args[0]), sp.symbols(args[1]))
                elif name == "integrate":
                    # integrate(expr, (x, a, b)) or integrate(expr, x)
                    if "," in inner and inner.strip().startswith("(") is False:
                        # try to evaluate tuple pattern
                        res = sp.integrate(*[sp.sympify(s) for s in [i.strip() for i in inner.split(",")]])
                    else:
                        res = sp.integrate(sp.sympify(inner))
                elif name == "solve":
                    args = [a.strip() for a in inner.split(",")]
                    if len(args) == 1:
                        res = sp.solve(sp.sympify(args[0]))
                    else:
                        res = sp.solve(sp.sympify(args[0]), sp.sympify(args[1]))
                else:
                    # Fallback: attempt to sympify and show
                    res = sp.sympify(expr)
            else:
                res = sp.sympify(expr)

            out = str(res)
            self.result_view.setPlainText(out)
            self.add_history(expr, out)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Symbolic evaluation error:\n{exc}")

    def on_evaluate(self):
        expr = self.expr_edit.text().strip()
        if not expr:
            return
        try:
            sym = sp.sympify(expr)
            num = sym.evalf()
            out = str(num)
            self.result_view.setPlainText(out)
            self.add_history(expr, out)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Numeric evaluation error:\n{exc}")


def main():
    app = QApplication(sys.argv)

    # Basic dark palette
    palette = app.palette()
    from PySide6.QtGui import QPalette, QColor
    dark = QPalette()
    dark.setColor(QPalette.Window, QColor(53, 53, 53))
    dark.setColor(QPalette.WindowText, Qt.white)
    dark.setColor(QPalette.Base, QColor(35, 35, 35))
    dark.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark.setColor(QPalette.ToolTipBase, Qt.white)
    dark.setColor(QPalette.ToolTipText, Qt.white)
    dark.setColor(QPalette.Text, Qt.white)
    dark.setColor(QPalette.Button, QColor(53, 53, 53))
    dark.setColor(QPalette.ButtonText, Qt.white)
    dark.setColor(QPalette.BrightText, Qt.red)
    app.setPalette(dark)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
