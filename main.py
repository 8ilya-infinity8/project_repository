import sys
from math import *
import pyqtgraph as pg

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QFont, QIcon

from main_ui import Ui_Form


class MainWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #D1DFDB;")
        self.setFixedWidth(353)
        self.setFixedHeight(572)
        self.table.setFixedWidth(338)
        self.beta = Beta(self)

        [i.clicked.connect(self.run) for i in self.buttonGroup_digits.buttons()]
        [i.clicked.connect(self.calc) for i in self.buttonGroup_binary.buttons()]
        [i.clicked.connect(self.change_notation) for i in self.buttonGroup_not.buttons()]
        [i.clicked.connect(self.func) for i in self.buttonGroup_more.buttons()]
        [i.clicked.connect(self.trygonometric) for i in self.buttonGroup_tryg.buttons()]

        self.btn_dec.setDisabled(True)

        self.btn_dot.clicked.connect(self.run)

        self.btn_eq.clicked.connect(self.pre_res)

        self.btn_clear.clicked.connect(self.clear)
        self.btn_clear_s.clicked.connect(self.clear_s)

        self.btn_sqrt.clicked.connect(self.sqrt)
        self.btn_fact.clicked.connect(self.fact)
        self.btn_pi.clicked.connect(self.pi)
        self.btn_e.clicked.connect(self.exp)

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

        # Переменная, в которой хранится введенное число
        self.data = ''
        # Переменная, в которой хранится выражение, которое нужно подсчитать
        self.data_eval = ''
        # Переменная, в которой записана прошлая и текущая система счисления
        self.notation = ['-', 'dec']

        self.flag1 = False
        self.flag2 = False
        self.xtrime = False

    def info(self):
        # Окно справки по посторойке графиков
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
        # Открытие панели для постройки графиков
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
        # трансформация основного окна для расширения калькулятора
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
        # функция для кнопки факториала
        if self.data:
            self.data = str(self.real_fact(int(float(self.data))))
            self.custom_display(self.data)

    def exp(self):
        # функция для кнопки числа е
        self.data = str(e)
        self.custom_display(self.data)

    def pi(self):
        # функция для кнопки числа pi
        self.data = str(pi)
        self.custom_display(self.data)

    def func(self):
        # функция для кнопок дополнительных операций над числом
        if self.data:
            self.data = str(self.more[self.sender().text()](float(self.data)))
            self.custom_display(self.data)

    def trygonometric(self):
        # функция для кнопок тригонометрии
        if self.data:
            self.data = str(self.tryg[self.sender().text()](radians(float(self.data))))
            self.custom_display(self.data)

    def clear(self):
        # Сброс всех данных, очистка экрана
        self.data = ''
        self.data_eval = ''
        self.table.display('')

    def clear_s(self):
        # Сброс последнего числа (не доработано)
        self.data = ''
        self.table.display('')

    def run(self):
        # Формируется число с помощью нажатий кнопок и отображается на дисплее
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
        self.xtrime = True

    def sqrt(self):
        # функция для кнопки квадратного корня
        if self.data:
            self.data = str(float(self.data)**0.5)
            self.custom_display(self.data)

    def extreme(self):
        # перевод введенных чисел в десятеричную систему счисления
        if self.xtrime:
            self.data = self.convert_from(self.data)
        self.xtrime = False

    def change_notation(self):
        # смена системы счисления, блокирование определенных кнопок
        self.extreme()
        lst = self.buttonGroup_digits.buttons()
        if self.sender().text() == 'dec':
            var = False
        else:
            var = True
        [i.setDisabled(var) for i in self.buttonGroup_tryg.buttons()]
        [i.setDisabled(var) for i in self.buttonGroup_more.buttons()]
        self.btn_sqrt.setDisabled(var)
        self.btn_fact.setDisabled(var)
        self.btn_pi.setDisabled(var)
        self.btn_e.setDisabled(var)
        self.btn_dot.setDisabled(var)
        self.btn_pow.setDisabled(var)
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
            self.custom_display(self.data)
        elif self.data_eval:
            self.custom_display(self.data_eval)

    def convert_from(self, n):
        # перевод в десятеричную систему счисления
        conv = {'bin': 2, 'oct': 8, 'hex': 16}
        if self.notation[1] == 'dec':
            return n
        return str(int(n, conv[self.notation[1]]))

    def convert_into(self, n):
        # перевод из десятеричной системы счисления
        conv = {'bin': bin, 'oct': oct, 'hex': hex}
        if self.notation[1] == 'dec':
            return n
        n = int(float(n))
        return conv[self.notation[1]](n)[2:]

    def custom_display(self, data):
        # вывод в нужной системе счисления и без лишнего
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
        # функция кнопки равно
        if self.flag2:
            self.extreme()
            self.data_eval += self.data
            self.data = ''
            self.result()
        self.flag2 = False

    def result(self):
        # Попытка вычисления выражения, в случае деления на 0 выводится ошибка
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

    def calc(self):
        # Происходит вычисление текущего выражения и дописывается новый знак.
        # Если последним был уже знак действия, то он менятся.
        self.extreme()
        self.data_eval += self.data
        self.data = ''
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
        # алгоритм построения графиков
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
    # класс окна графика
    def __init__(self, parent=None):
        super(Chart, self).__init__(parent)
        self.setWindowTitle('График')
        self.setGeometry(300, 300, 600, 500)


class Beta(QMainWindow):
    # класс окна калькулятора в строке
    def __init__(self, parent=None):
        super(Beta, self).__init__(parent)
        self.setWindowTitle('Простой калькулятор')
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
        # попытка вывода ответа
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
