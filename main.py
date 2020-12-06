import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("coffee.sqlite")
        uic.loadUi('main.ui', self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                              'описание вкуса', 'цена', 'объем упаковки'])
        self.inck_click()

    def inck_click(self):
        cur = self.connection.cursor()
        result = cur.execute("""SELECT * FROM varieties""").fetchall()
        result = map(lambda x: map(str, x), result)
        for i, row in enumerate(result):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(elem))

        self.table.resizeRowsToContents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
