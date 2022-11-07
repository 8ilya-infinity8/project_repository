import sys
from math import *
import pyqtgraph as pg

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QFont

from main_ui import Ui_Form

class MainWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedWidth(353)
        self.setFixedHeight(572)
        self.table.setFixedWidth(338)
        self.beta = Beta(self)

        [i.clicked.connect(self.run) for i in self.buttonGroup_digits.buttons()]
        [i.clicked.connect(self.calc) for i in self.buttonGroup_binary.buttons()]
        [i.clicked.connect(self.change_notation) for i in self.buttonGroup_not.buttons()]
        self.btn_dec.setDisabled(True)

        self.btn_dot.clicked.connect(self.run)

        self.btn_eq.clicked.connect(self.pre_res)

        self.btn_clear.clicked.connect(self.clear)
        self.btn_clear_s.clicked.connect(self.clear_s)

        self.btn_sqrt.clicked.connect(self.sqrt)
        self.btn_fact.clicked.connect(self.fact)

        self.graphics_btn.clicked.connect(self.open_graphics)
        self.beta_btn.clicked.connect(self.check_beta)
        self.calc_combo.currentTextChanged.connect(self.transform)

        self.pushButton_2.clicked.connect(self.create_chart)
        self.ref_btn.clicked.connect(self.info)

        self.tryg = {'sin': sin, 'cos': cos, 'tg': tan,
                     'ctg': lambda x: cos(x) / sin(x)}
        self.more = {'ln': log, 'log': log10, 'log2': log2, 'rnd': round}
        self.nots = {'bin': self.btn_bin, 'oct': self.btn_oct,
                     'dec': self.btn_dec, 'hex': self.btn_hex}

        # Переменная, в которой хранится последнее введённое число/результат вычисленного выражения
        self.data = ''
        self.disp = ''
        # Переменная, в которой хранится выражение, которое нужно подсчитать
        self.data_eval = ''
        # Переменная, в которой записана текущая система счисления
        self.notation = ['-', 'dec']

        self.flag1 = False
        self.flag2 = False

    def info(self):
        info_box = QMessageBox(self)
        info_box.setWindowTitle('Справка по графикам')
        info_box.setIcon(QMessageBox.Information)
        info_box.setText(
            """  Введите уравнение функции,
где в роли переменной стоит x.

  Поле "от": с какой точки (включительно)
по оси x начнется построение графика.
  Поле "до": до какой точки (включительно)
по оси x будет построен график.
  Поле "шаг": расстояние между
соседними точками по оси x.""")
        info_box.show()

    def open_graphics(self):
        if self.graphics_btn.isChecked():
            self.setFixedHeight(700)
        else:
            self.setFixedHeight(570)

    def check_beta(self):
        if self.beta_btn.isChecked():
            self.open_beta()
        else:
            self.close_beta()

    def transform(self):
        if self.flag1:
            self.table.setFixedWidth(338)
            self.table.setDigitCount(8)
            self.setFixedWidth(353)
        else:
            self.table.setFixedWidth(596)
            self.table.setDigitCount(15)
            self.setFixedWidth(614)
        self.flag1 = not self.flag1

    def real_fact(self, n):
        if n < 0:
            return -1
        if n == 0:
            return 1
        else:
            return n * self.real_fact(n - 1)

    def fact(self):
        if self.data:
            self.extreme()
            self.data = self.real_fact(int(float(self.data)))
            self.custom_display(str(self.data))

    ## Сброс всех данных, очистка экрана
    def clear(self):
        self.data = ''
        self.data_eval = ''
        self.disp = ''
        self.table.display('')

    def clear_s(self):
        self.data = ''
        self.table.display('')

    def run(self):
        ## Формируется число с помощью нажатий кнопок и отображается на дисплее
        if self.sender().text() == '.':
            if '.' in self.data:
                return
        if self.data != '0' or (self.data == '0' and self.sender().text() == '.'):
            self.data = self.data + self.sender().text()
            self.table.display(self.data)
        else:
            self.data = self.sender().text()
            self.table.display(self.data)
        self.flag2 = True

    def sqrt(self):
        if self.data:
            self.extreme()
            self.data = float(self.data)**0.5
            self.custom_display(str(self.data))

    def extreme(self):
        return
        print('active')
        if self.data:
            self.data = self.convert_from(self.data)


    def change_notation(self):
        lst = self.buttonGroup_digits.buttons()
        if self.sender().text() == 'dec':
            self.btn_dot.setDisabled(False)
        else:
            self.btn_dot.setDisabled(True)
        if self.sender().text() == 'oct':
            self.btn8.setDisabled(True)
            self.btn9.setDisabled(True)
        elif self.sender().text() == 'bin':
            del lst[4]
            del lst[7]
            [i.setDisabled(True) for i in lst]
        else:
            [i.setDisabled(False) for i in lst]
        self.nots[self.notation[1]].setDisabled(False)
        self.sender().setDisabled(True)
        self.notation[0] = self.notation[1]
        self.notation[1] = self.sender().text()
        if self.data:
            self.data = self.convert_into(self.data)
            self.data = self.convert_from(self.data)
            self.extreme()
            self.custom_display(self.data)

    def convert_from(self, n):
        conv = {'bin': 2, 'oct': 8, 'hex': 16}
        if self.notation[1] == 'dec':
            return str(float(n))
        return str(int(n, conv[self.notation[1]]))

    def convert_into(self, n):
        conv = {'bin': bin, 'oct': oct, 'hex': hex}
        if self.notation[1] == 'dec':
            if self.notation[0] != 'dec':
                self.notation[1], self.notation[0] = self.notation[0], self.notation[1]
                n = self.convert_from(str(int(float(n))))
                self.notation[1], self.notation[0] = self.notation[0], self.notation[1]
            return n
        n = int(float(n))
        return conv[self.notation[1]](n)[2:]

    def custom_display(self, data):
        print(data, self.notation)
        if self.notation[1] == 'dec' and self.notation[0] != 'dec':
            print('stop')
        else:
            data = self.convert_into(data)
        try:
            data = float(data)
            if data == int(data):
                self.table.display(int(data))
            else:
                self.table.display(data)
        except:
            self.table.display(data)

    def pre_res(self):
        if self.flag2:
            self.extreme()
            self.data_eval += self.data
            self.data = ''
            self.result()
        self.flag2 = False

    def result(self):
        ## Происходит попытка вычисления выражения, в случае попытки деления на 0 выводится ошибка
        try:
            float(self.data_eval)
        except:
            try:
                self.data = str(eval(self.data_eval))
                self.data_eval = ''
                self.custom_display(self.data)
            except ZeroDivisionError:
                self.table.display('Error')
            except:
                pass
        # self.disp = str(self.data)

    def calc(self):
        ## Происходит вычисление текущего выражения и дописывается новый знак. Если последним был уже знак действия, то он менятся.
        print('1|', self.data_eval, '|', self.data, '|')
        self.extreme()
        self.data_eval += self.data
        self.data = ''
        print('2|', self.data_eval, '|', self.data, '|')
        if self.data_eval:
            self.result()
            if not self.data_eval:
                self.data_eval += self.data
                self.data = ''
            if (self.data_eval[-1] not in ['+', '-', '/', '*']):
                self.data_eval += self.sender().text()
            else:
                self.data_eval = self.data_eval[:-1] + self.sender().text()
            self.data_eval = self.data_eval.replace('^', '**')
        self.flag2 = True

    def create_chart(self):
        def create_line(chart, start, points, pen):
            chart.graphWidget.plot(start, points, pen=pen)

        f = self.graphic_line.text()
        a, b = float(self.x1_line.text()), float(self.x2_line.text())
        step = float(self.step_line.text())
        a_x, b_x = a, b
        start = []
        while a < b:
            start += [round(a, 8)]
            a += step
        start += [b]

        chart = Chart(self)
        chart.show()
        chart.graphWidget = pg.PlotWidget()
        chart.setCentralWidget(chart.graphWidget)
        chart.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0), width=2)

        points = []
        b_p = 0
        min_y, max_y = -1, 1
        for i in range(len(start)):
            x = start[i]
            try:
                points += [float(eval(f))]
            except Exception:
                if points:
                    y1, y2 = min(points), max(points)
                    if y1 < min_y:
                        min_y = y1
                    if y2 > max_y:
                        max_y = y2
                    create_line(chart, start[b_p:i], points, pen)
                points.clear()
                b_p = i + 1
        if points:
            y1, y2 = min(points), max(points)
            if y1 < min_y:
                min_y = y1
            if y2 > max_y:
                max_y = y2
            create_line(chart, start[b_p:], points, pen)

        pen = pg.mkPen(color=(0, 0, 0), width=1)
        chart.graphWidget.plot([min((-1, a_x)), max((1, b_x))], [0, 0], pen=pen)
        chart.graphWidget.plot([0, 0], [min_y, max_y], pen=pen)

    def open_beta(self):
        self.beta.show()

    def close_beta(self):
        self.beta.close()


class Chart(QMainWindow):
    def __init__(self, parent=None):
        super(Chart, self).__init__(parent)
        self.setWindowTitle('График')
        self.setGeometry(300, 300, 600, 500)


class Beta(QMainWindow):
    def __init__(self, parent=None):
        super(Beta, self).__init__(parent)
        self.setWindowTitle('Бета калькулятор')
        self.setFixedSize(500, 100)

        self.line = QLineEdit(self)
        self.line.move(35, 10)
        self.line.resize(455, 30)
        self.line.setFont(QFont('Arial', 15))
        self.line.textEdited.connect(self.display)

        self.btn = QPushButton('C', self)
        self.btn.resize(30, 32)
        self.btn.move(3, 9)
        self.btn.clicked.connect(self.clear)

        self.label = QLabel(self)
        self.label.move(35, 40)
        self.label.resize(455, 30)
        self.label.setFont(QFont('New Times Roman', 10))

    def display(self):
        self.line.setText(self.line.text().replace('=', ''))
        try:
            s = self.line.text().replace('^', '**')
            self.label.setText('= ' + str(eval(s)))
        except:
            self.label.setText('error')

    def clear(self):
        self.line.clear(), self.label.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.exit(app.exec())
