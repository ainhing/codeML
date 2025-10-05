import base64
import traceback
import mysql.connector
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox

from blog49.MainUiBlog49 import Ui_MainWindow


class MainWindowBlog49Ex(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.default_avatar="images/images.png"
        self.id = None
        self.code = None
        self.name = None
        self.age = None
        self.avatar = None
        self.intro = None
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.tableWidgetstudents.itemSelectionChanged.connect(self.processItemSelection)
        self.pushButtonavatar.clicked.connect(self.pickAvatar)
        self.pushButtonremoveavatar.clicked.connect(self.removeAvatar)
        self.pushButtoninsert.clicked.connect(self.processInsert)
        self.pushButtonupdate.clicked.connect(self.processUpdate)
        self.pushButtonremove.clicked.connect(self.processRemove)
        try:
            self.labelavatar.setPixmap(QPixmap(self.default_avatar))
        except Exception:
            pass
    def show(self):
        self.MainWindow.show()
    def connectMySQL(self):
        server = 'localhost'
        port = 3306
        database = 'studentmanagement'
        username = "root"
        password = "123456789"

        self.conn = mysql.connector.connect(
            host=server,
            port=port,
            database=database,
            user=username,
            password=password)
    def selectAllStudent(self):
        cursor = self.conn.cursor()
        # query all students
        sql = "select * from student"
        cursor.execute(sql)
        dataset = cursor.fetchall()
        self.tableWidgetstudents.setRowCount(0)
        row=0
        for item in dataset:
            row = self.tableWidgetstudents.rowCount()
            self.tableWidgetstudents.insertRow(row)

            self.id = item[0]
            self.code = item[1]
            self.name = item[2]
            self.age = item[3]
            self.avatar = item[4]
            self.intro = item[5]

            self.tableWidgetstudents.setItem(row, 0, QTableWidgetItem(str(self.id)))
            self.tableWidgetstudents.setItem(row, 1, QTableWidgetItem(self.code))
            self.tableWidgetstudents.setItem(row, 2, QTableWidgetItem(self.name))
            self.tableWidgetstudents.setItem(row, 3, QTableWidgetItem(str(self.age)))

        cursor.close()

    def processItemSelection(self):
        row=self.tableWidgetstudents.currentRow()
        if row ==-1:
            return
        try:
            code = self.tableWidgetstudents.item(row, 1).text()
            cursor = self.conn.cursor()
            # query all students
            sql = "select * from student where code=%s"
            val = (code,)
            cursor.execute(sql, val)
            item = cursor.fetchone()
            if item != None:
                self.id = item[0]
                self.code = item[1]
                self.name = item[2]
                self.age = item[3]
                self.avatar = item[4]
                self.intro = item[5]
                self.lineEditid.setText(str(self.id))
                self.lineEditcode.setText(self.code)
                self.lineEditname.setText(self.name)
                self.lineEditage.setText(str(self.age))
                self.lineEditintro.setText(self.intro)
                # self.labelAvatar.setPixmap(None)
                if self.avatar != None:
                    imgdata = base64.b64decode(self.avatar)
                    pixmap = QPixmap()
                    pixmap.loadFromData(imgdata)
                    self.labelavatar.setPixmap(pixmap)
                else:
                    pixmap = QPixmap("images/images.png")

                    self.labelavatar.setPixmap(pixmap)
            else:
                print("Not Found")
            cursor.close()
        except:
            traceback.print_exc()

    def pickAvatar(self):
        filters = "Picture PNG (*.png);;All files (*)"
        filename, selected_filter = QFileDialog.getOpenFileName(
            self.MainWindow,
            filter=filters,
        )
        if filename=='':
            return
        pixmap = QPixmap(filename)
        self.labelavatar.setPixmap(pixmap)

        with open(filename, "rb") as image_file:
            self.avatar = base64.b64encode(image_file.read())
            print(self.avatar)
        pass
    def removeAvatar(self):
        self.avatar=None
        pixmap = QPixmap(self.default_avatar)
        self.labelavatar.setPixmap(pixmap)
    def processInsert(self):

            try:
                cursor = self.conn.cursor()
                sql = "insert into student(Code,Name,Age,Avatar,Intro) values(%s,%s,%s,%s,%s)"

                code = self.lineEditcode.text()
                name = self.lineEditname.text()
                age = int(self.lineEditage.text())
                intro = self.lineEditintro.text() or None  # <-- dùng biến cục bộ

                val = (code, name, age, self.avatar, intro)  # <-- truyền đúng
                cursor.execute(sql, val)
                self.conn.commit()

                self.lineEditid.setText(str(cursor.lastrowid))
                cursor.close()
                self.selectAllStudent()
            except:
                traceback.print_exc()

    def processUpdate(self):
        cursor = self.conn.cursor()
        # query all students
        sql = "update student set Code=%s,Name=%s,Age=%s,Avatar=%s,Intro=%s" \
              " where Id=%s"
        self.id=int(self.lineEditid.text())
        self.code = self.lineEditcode.text()
        self.name = self.lineEditname.text()
        self.age = int(self.lineEditage.text())
        if not hasattr(self, 'avatar'):
            self.avatar = None
        self.intro = self.lineEditintro.text()

        val = (self.code,self.name,self.age,self.avatar ,self.intro,self.id )

        cursor.execute(sql, val)

        self.conn.commit()

        print(cursor.rowcount, " record updated")
        cursor.close()
        self.selectAllStudent()
    def processRemove(self):
        dlg = QMessageBox(self.MainWindow)
        dlg.setWindowTitle("Confirmation Deleting")
        dlg.setText("Are you sure you want to delete?")
        dlg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        dlg.setStandardButtons(buttons)
        button = dlg.exec()
        if button == QMessageBox.StandardButton.No:
            return
        cursor = self.conn.cursor()
        # query all students
        sql = "delete from student "\
              " where Id=%s"

        val = (self.lineEditid.text(),)

        cursor.execute(sql, val)

        self.conn.commit()

        print(cursor.rowcount, " record removed")

        cursor.close()
        self.selectAllStudent()
        self.clearData()
    def clearData(self):
        self.lineEditid.setText("")
        self.lineEditcode.setText("")
        self.lineEditname.setText("")
        self.lineEditage.setText("")
        self.lineEditintro.setText("")
        self.avatar=None

