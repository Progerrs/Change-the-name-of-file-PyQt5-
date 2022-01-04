#!usr/bin/env python3
import os


from datetime import datetime
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox


Form, Window = uic.loadUiType("user_interface.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()

NUMBER = form.spinBox.value()
NOW = datetime.now()
COUNTER = 0
DIRECTORY = ""
RESULT = 0


def open_explorer():
    global DIRECTORY
    DIRECTORY = QFileDialog.getExistingDirectory()
    global COUNTER
    COUNTER = 0
    name_of_files = []
    for root, dirs, files in os.walk(DIRECTORY):
        for name in files:
            COUNTER += 1
            name_of_files.append(name)
    fill_a_table(name_of_files)


def fill_a_table(name_of_files):
    global COUNTER
    form.tableWidget.setRowCount(COUNTER)
    row = 0
    for name_of_file in name_of_files:
        form.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(name_of_file))
        row += 1
    for _ in range(COUNTER):
        new_name_of_file = form.tableWidget.item(_, 0).text()
        form.tableWidget.setItem(_, 1, QtWidgets.QTableWidgetItem(new_name_of_file))


def rename_file_support():
    global COUNTER
    global RESULT
    if COUNTER == 0:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Нету файлов для переименования!")
        msg_box.setDefaultButton(QMessageBox.Cancel)
        msg_box.exec()
    else:
        try:
            for RESULT in range(COUNTER):
                name = form.tableWidget.item(RESULT, 0).text()
                old_path_file = os.path.join(DIRECTORY, name)
                new_name = form.tableWidget.item(RESULT, 1).text()
                new_path_file = os.path.join(DIRECTORY, new_name)
                os.rename(old_path_file, new_path_file)
                form.tableWidget.setItem(RESULT, 2, QtWidgets.QTableWidgetItem("ОК"))

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Файлы успешно переименованы")
            msg_box.setDefaultButton(QMessageBox.Cancel)
            msg_box.exec()

            refresh()
        except:
            form.tableWidget.setItem(RESULT, 2, QtWidgets.QTableWidgetItem("ОШИБКА"))
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText("Произошла ошибка при переименование файлов!")
            msg_box.setDefaultButton(QMessageBox.Cancel)
            msg_box.exec()


def close_event():
    if COUNTER == 0:
        app.quit()
    else:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setText("Вы действительно хотите выйти?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Save)
        ret = msg_box.exec()
        if ret == QMessageBox.Yes:
            app.quit()
        elif ret == QMessageBox.Cancel:
            pass
        else:
            pass


def to_upper_or_to_lower():
    if str(form.comboBox_2.currentText()) == "Без изменений":
        change_text(to_text, COUNTER)
    else:
        if COUNTER == 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("Откройте хотя бы один файл!")
            msg_box.setDefaultButton(QMessageBox.Cancel)
            msg_box.exec()
        else:
            if str(form.comboBox_2.currentText()) == "ВСЕ ЗАГЛАВНЫЕ":
                change_text(to_upper, COUNTER)
            elif str(form.comboBox_2.currentText()) == "все строчные":
                change_text(to_lower, COUNTER)
            elif str(form.comboBox_2.currentText()) == "Первая буква заглавная":
                change_text(to_capitalize, COUNTER)
            else:
                change_text(to_title, COUNTER)


def change_text(func, size):
    for _ in range(size):
        new_name_of_file = form.tableWidget.item(_, 0).text()
        new_name_of_file, extension = os.path.splitext(new_name_of_file)
        form.tableWidget.setItem(_, 1, QtWidgets.QTableWidgetItem(func(new_name_of_file) + change_extension(extension)))


def to_upper(text):
    return text.upper()


def to_lower(text):
    return text.lower()


def to_capitalize(text):
    return text.capitalize()


def to_title(text):
    return text.title()


def to_text(text):
    return text


def get_valid_name(name):
    return name


def refresh():
    global COUNTER
    form.tableWidget.clear()
    form.tableWidget.setRowCount(0)
    COUNTER = 0
    form.tableWidget.setHorizontalHeaderLabels(["Старое имя", "Новое имя", "Результат"])
    name_of_files = []
    for root, dirs, files in os.walk(DIRECTORY):
        for name in files:
            COUNTER += 1
            name_of_files.append(name)
    fill_a_table(name_of_files)


def found_string():
    global COUNTER
    if COUNTER == 0:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Откройте хотя бы один файл!")
        msg_box.setDefaultButton(QMessageBox.Cancel)
        msg_box.exec()
    else:
        files_in_filter = []
        string = str(form.lineEdit_2.text())
        for _ in range(COUNTER):
            if string in str(os.path.splitext(form.tableWidget.item(_, 0).text())[0]):
                files_in_filter.append(str(form.tableWidget.item(_, 0).text()))
            else:
                pass
        form.tableWidget.clear()
        form.tableWidget.setHorizontalHeaderLabels(["Старое имя", "Новое имя", "Результат"])
        form.tableWidget.setRowCount(len(files_in_filter))
        if len(files_in_filter) == 0:
            COUNTER = 0
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText("Не обнаружено ни одного файла!")
            msg_box.setDefaultButton(QMessageBox.Ok)
            msg_box.exec()
        else:
            row = 0
            for name_of_file in files_in_filter:
                form.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(name_of_file))
                form.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(name_of_file))
                row += 1
            COUNTER = len(files_in_filter)


def change_file_name_on_mark():
    global COUNTER
    global NUMBER
    NUMBER = form.spinBox.value()
    if COUNTER == 0:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Откройте хотя бы один файл!")
        msg_box.setDefaultButton(QMessageBox.Cancel)
        msg_box.exec()
    else:
        new_name_of_file = form.lineEdit_4.text()
        for _ in range(COUNTER):
            extend = os.path.splitext(form.tableWidget.item(_, 0).text())[1]
            name = os.path.splitext(form.tableWidget.item(_, 0).text())[0]
            form.tableWidget.setItem(_, 1, QtWidgets.QTableWidgetItem(new_name_of_file.replace("[N]", name).replace(
                "[YMD]", NOW.strftime("%Y-%m-%d")).replace("[hms]", NOW.strftime("%H:%M:%S")).replace("[C]",
                counter().zfill(int(form.comboBox_3.currentText()))) + change_extension(extend)))


def paste_mask_name():
    index = form.lineEdit_4.cursorPosition()
    string = form.lineEdit_4.text()
    form.lineEdit_4.setText(string[0:index] + "[N]" + string[index:])


def paste_mask_hour():
    index = form.lineEdit_4.cursorPosition()
    string = form.lineEdit_4.text()
    form.lineEdit_4.setText(string[0:index] + "[hms]" + string[index:])


def paste_mask_day():
    index = form.lineEdit_4.cursorPosition()
    string = form.lineEdit_4.text()
    form.lineEdit_4.setText(string[0:index] + "[YMD]" + string[index:])


def paste_mask_counter():
    index = form.lineEdit_4.cursorPosition()
    string = form.lineEdit_4.text()
    form.lineEdit_4.setText(string[0:index] + "[C]" + string[index:])


def paste_mask_counter_for_extension():
    index = form.lineEdit.cursorPosition()
    string = form.lineEdit.text()
    form.lineEdit.setText(string[0:index] + "[C]" + string[index:])


def paste_mask_type():
    index = form.lineEdit.cursorPosition()
    string = form.lineEdit.text()
    form.lineEdit.setText(string[0:index] + "[E]" + string[index:])


def counter():
    global NUMBER
    NUMBER += int(form.spinBox_2.value())
    return str(NUMBER - int(form.spinBox_2.value()))  #Костыль


def replace_text():
    global COUNTER
    if COUNTER == 0:
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText("Нету файлов для переименования!")
        msg_box.setDefaultButton(QMessageBox.Cancel)
        msg_box.exec()
    else:
        for _ in range(COUNTER):
            name = os.path.splitext(form.tableWidget.item(_, 0).text())[0]
            extension = os.path.splitext(form.tableWidget.item(_, 0).text())[1]
            name = name.replace(form.lineEdit_2.text(), form.lineEdit_3.text())
            form.tableWidget.setItem(_, 1, QtWidgets.QTableWidgetItem(name + change_extension(extension)))


def change_extension(name):
    global NUMBER
    extension = form.lineEdit.text().replace("[C]",  str(NUMBER - int(form.spinBox_2.value())).zfill(int(form.comboBox_3.currentText()))).replace("[E]", name)
    return extension


form.comboBox_2.currentIndexChanged.connect(to_upper_or_to_lower)
form.comboBox_3.currentIndexChanged.connect(change_file_name_on_mark)

form.spinBox.valueChanged.connect(change_file_name_on_mark)
form.spinBox_2.valueChanged.connect(change_file_name_on_mark)

form.pushButton_2.clicked.connect(open_explorer)
form.pushButton.clicked.connect(paste_mask_name)
form.pushButton_3.clicked.connect(paste_mask_day)
form.pushButton_5.clicked.connect(paste_mask_counter)
form.pushButton_4.clicked.connect(paste_mask_hour)
form.pushButton_6.clicked.connect(close_event)
form.pushButton_15.clicked.connect(replace_text)
form.pushButton_14.clicked.connect(rename_file_support)
form.pushButton_10.clicked.connect(found_string)
form.pushButton_11.clicked.connect(paste_mask_type)
form.pushButton_13.clicked.connect(paste_mask_counter_for_extension)

form.lineEdit_4.textChanged.connect(change_file_name_on_mark)
form.lineEdit.textChanged.connect(change_file_name_on_mark)

form.tableWidget.setColumnWidth(0, 400)
form.tableWidget.setColumnWidth(1, 400)
form.tableWidget.setColumnWidth(1, 150)

app.exec_()
