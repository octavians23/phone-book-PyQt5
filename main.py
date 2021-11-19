from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QFont
import csv
import re

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
phonelist = []
header = ['Person Name',  ' Contact Number', ' Email Address']


def read_csv_file(filename):
    global header
    with open(filename) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")
        next(csv_reader)
        for row in csv_reader:
            phonelist.append(row)
    return phonelist


def write_in_csv_file(phonelist, filename):
    global header
    with open(filename, 'w', newline='') as csv_file:
        writeobj = csv.writer(csv_file, delimiter=',')
        writeobj.writerow(header)
        for row in phonelist:
            row[1][0] = " " + row[1][0]
            row[2][0] = " " + row[2][0]
            put = row[0] + row[1] + row[2]
            writeobj.writerow(put)


def make_list(view):
    list = []
    for row in range(view.count()):
        string = view.item(row).text()
        name = re.findall(r'. (\w*\s\w*) ->', string)
        phone = re.findall(r'-> (\d*)', string)
        email = re.findall(r'\| (.*)', string)
        final = [name, phone, email]
        list.append(final)
    return list


class MyGUI(QMainWindow):

    list_tracker = 1

    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.show()

        self.list.clicked.connect(self.item_clicked)
        self.btnAdd.clicked.connect(self.add_contact)
        self.btnEdit.clicked.connect(self.edit_contact)
        self.btnReset.clicked.connect(self.reset_contact)
        self.btnDelete.clicked.connect(self.delete_contact)
        self.btnLoad.clicked.connect(self.load_contacts)
        self.btnSave.clicked.connect(self.save_contacts)

    def item_clicked(self):
        item = self.list.currentItem()
        name = re.findall(r'. (\w*\s\w*) ->', item.text())
        phone = re.findall(r'-> (\d*)', item.text())
        email = re.findall(r'\| (.*)', item.text())
        names = name[0].split(' ')
        self.leName.setText(names[0])
        self.leSurname.setText(names[1])
        self.leTel.setText(phone[0])
        self.leEmail.setText(email[0])

    def add_contact(self):
        if self.leName.text() != "" and self.leSurname.text() != "" and self.leTel.text() != "":
            if re.fullmatch(r'07(\d{8})', self.leTel.text()):
                if re.fullmatch(email_regex, self.leEmail.text()):
                    name = self.leName.text()
                    surname = self.leSurname.text()
                    tel = self.leTel.text()
                    email = self.leEmail.text()
                    self.list.insertItem(self.list_tracker, f'{self.list_tracker}. {name} {surname} -> {tel} | {email}')
                    self.list_tracker += 1
                    self.reset_contact()
                else:
                    message_box = QMessageBox()
                    message_box.setText("Invalid email address!")
                    message_box.exec_()
            else:
                message_box = QMessageBox()
                message_box.setText("Invalid phone number!")
                message_box.exec_()
        else:
            message_box = QMessageBox()
            message_box.setText("Fields cannot be empty!")
            message_box.exec_()

    def edit_contact(self):
        if self.list.currentItem():
            if self.leName.text() != "" and self.leSurname.text() != "" and self.leTel.text() != "" and self.leEmail.text() != "":
                if re.fullmatch(r'07(\d{8})', self.leTel.text()):
                    if re.fullmatch(email_regex, self.leEmail.text()):
                        name = self.leName.text()
                        surname = self.leSurname.text()
                        tel = self.leTel.text()
                        email = self.leEmail.text()
                        row = self.list.currentRow()
                        self.list.takeItem(row)
                        self.list.insertItem(row, f'{row+1}. {name} {surname} -> {tel} | {email}')
                        self.reset_contact()
                    else:
                        message_box = QMessageBox()
                        message_box.setText("Invalid email address!")
                        message_box.exec_()
                else:
                    message_box = QMessageBox()
                    message_box.setText("Invalid phone number!")
                    message_box.exec_()
            else:
                message_box = QMessageBox()
                message_box.setText("Fields cannot be empty!")
                message_box.exec_()
        else:
            message_box = QMessageBox()
            message_box.setText("Select a contact!")
            message_box.exec_()

    def reset_contact(self):
        self.leName.setText("")
        self.leSurname.setText("")
        self.leTel.setText("")
        self.leEmail.setText("")

    def delete_contact(self):
        if self.list.currentItem():
            tracker = self.list.currentRow()
            self.list.takeItem(tracker)
            for row in range(tracker, self.list.count()):
                string = self.list.item(row).text()
                num = int((re.findall(r'(\d+)\. ', string)[0]))
                string = str(num-1) + string[string.find('.'):]
                self.list.takeItem(row)
                self.list.insertItem(row, string)
            self.list_tracker -= 1
            self.reset_contact()
        else:
            message_box = QMessageBox()
            message_box.setText("Select an item to delete!")
            message_box.exec_()

    def load_contacts(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", 'CSV Files (*.csv)',
                                                  options=options)
        if filename != "":
            list = read_csv_file(filename)
            for count, item in enumerate(list):
                names = item[0].split(" ")
                tel = item[1][1:]
                email = item[2][1:]
                self.list.insertItem(count, f'{self.list_tracker}. {names[0]} {names[1]} -> {tel} | {email}')
                self.list_tracker += 1


    def save_contacts(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", 'CSV Files (*.csv)',
                                                  options=options)
        if filename != "":
            list = make_list(self.list)
            write_in_csv_file(list, filename)

    def closeEvent(self, event):
        dialog = QMessageBox()
        dialog.setText('Do you want to save your work?')
        dialog.addButton(QPushButton('Yes'), QMessageBox.YesRole)
        dialog.addButton(QPushButton('No'), QMessageBox.NoRole)
        dialog.addButton(QPushButton('Cancel'), QMessageBox.RejectRole)

        ans = dialog.exec_()

        match ans:
            case 0:
                self.save_contacts()
                event.accept()
            case 2:
                event.ignore()


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()
