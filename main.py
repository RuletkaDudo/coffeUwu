import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget, QLineEdit, QTextEdit


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("coffee.sqlite")
        uic.loadUi('main.ui', self)
        self.addEdit_window = None
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                              'описание вкуса', 'цена', 'объем упаковки'])
        self.inck_click()
        self.reset_btn.clicked.connect(self.inck_click)
        self.create_btn.clicked.connect(self.create_click)
        self.change_btn.clicked.connect(self.change_click)

    def inck_click(self):
        cur = self.connection.cursor()
        self.table.setRowCount(0)
        result = cur.execute("""SELECT * FROM varieties""").fetchall()
        result = map(lambda x: map(str, x), result)
        for i, row in enumerate(result):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(elem))

        self.table.resizeRowsToContents()

    def create_click(self):

        self.addEdit_window = ExampleTwo()

        self.addEdit_window.title.setText('')
        self.addEdit_window.roasting.setText('')
        self.addEdit_window.type.setText('')
        self.addEdit_window.description.setText('')
        self.addEdit_window.price.setText('')
        self.addEdit_window.package_volume.setText('')

        self.addEdit_window.btn.setText('Создать')
        self.addEdit_window.show()

    def change_click(self):
        if len(self.table.selectedItems()) == 0:
            return

        self.addEdit_window = ExampleTwo()
        row, col = self.table.selectedItems()[0].row(), self.table.selectedItems()[0].column()

        self.addEdit_window.selectedID = int(self.table.item(row, 0).text())

        self.addEdit_window.title.setText(self.table.item(row, 1).text())
        self.addEdit_window.roasting.setText(self.table.item(row, 2).text())
        self.addEdit_window.type.setText(self.table.item(row, 3).text())
        self.addEdit_window.description.setText(self.table.item(row, 4).text())
        self.addEdit_window.price.setText(self.table.item(row, 5).text())
        self.addEdit_window.package_volume.setText(self.table.item(row, 6).text())

        self.addEdit_window.btn.setText('Изменить')
        self.addEdit_window.show()

    def closeEvent(self, event):
        if self.addEdit_window is not None:
            self.addEdit_window.close()


class ExampleTwo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.btn.clicked.connect(self.inck_click)
        self.selectedID = None


    def inck_click(self):
        try:
            connection = sqlite3.connect("coffee.sqlite")
            cur = connection.cursor()
            data = [self.title.text(), self.roasting.text(), self.type.text(),
                    self.description.text(), self.price.text(), self.package_volume.text()]
            if self.btn.text() == 'Создать':
                cur.execute('''INSERT INTO varieties(title, roasting, type, description, price, package_volume)
                 VALUES(?, ?, ?, ?, ?, ?)''', data)
            elif self.btn.text() == 'Изменить':
                cur.execute('''UPDATE varieties
                SET title=?, roasting=?, type=?, description=?, price=?, package_volume=?
                WHERE id=?''', data + [self.selectedID])
            connection.commit()
            self.error.setText('')
            self.close()
        except Exception as e:
            self.error.setText('Ошибка')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
