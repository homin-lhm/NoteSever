from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
from common.NoteApi import NoteApi
import threading


class Frame5Btn1F(object):
    def __init__(self):
        self.text1 = "输入sid"
        self.text2 = "输入uid"
        self.text3 = "输入便签生成数量（以200为倍数，最少200，最多不限制）"
        self.text4 = "输入groupId（可选，关联分组）"

    def business(self, QDialog):
        # textbox
        self.label = QLabel(QDialog)
        self.label.setText("批量创建便签，生成的便签内容都是一样的。")
        QDialog.verticalLayoutFrame5Right1.addWidget(self.label)

        self.textbox1 = QLineEdit(QDialog)
        self.textbox1.setText(self.text1)
        QDialog.verticalLayoutFrame5Right1.addWidget(self.textbox1)
        self.textbox1.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox1, self.text1))

        self.textbox2 = QLineEdit(QDialog)
        self.textbox2.setText(self.text2)
        QDialog.verticalLayoutFrame5Right1.addWidget(self.textbox2)
        self.textbox2.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox2, self.text2))

        self.textbox3 = QLineEdit(QDialog)
        self.textbox3.setText(self.text3)
        QDialog.verticalLayoutFrame5Right1.addWidget(self.textbox3)
        self.textbox3.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox3, self.text3))

        self.textbox4 = QLineEdit(QDialog)
        self.textbox4.setText(self.text4)
        QDialog.verticalLayoutFrame5Right1.addWidget(self.textbox4)
        self.textbox4.textEdited[str].connect(lambda: self.textbox_click_color(self.textbox4, self.text4))

        # 第一个按钮事件
        self.btn1 = QPushButton("create", QDialog)
        self.btn1.setGeometry(275, 150, 100, 50)
        QDialog.verticalLayoutFrame5Right1.addWidget(self.btn1)
        self.btn1.clicked.connect(lambda: self.click_btn1())

        # 控制台输出
        self.text_output = QTextBrowser(QDialog)
        QDialog.verticalLayoutFrame5Right1.addWidget(self.text_output)

    def textbox_click_color(self, textbox, text):
        if textbox.text() != text:
            textbox.setStyleSheet(
                "QLineEdit{font:75 15pt '黑体'}"
                "QLineEdit{color:rgb(94,221,224)}")

    def click_btn1(self):
        t = threading.Thread(target=self.click_btn1_thread)
        t.start()

    def click_btn1_thread(self):
        # 点击
        sid = self.textbox1.text()
        uid = self.textbox2.text()
        num = self.textbox3.text()
        groupId = self.textbox4.text()
        if groupId == "" or groupId is None or groupId == self.text4:
            groupId = None
        loop_num = int(num)/200
        try:
            self.text_output.append("start create")
            assert_list = []
            for i in range(1, 201):
                t = threading.Thread(target=NoteApi().note_more_create, args=(i, sid, uid, loop_num, groupId, assert_list))
                t.start()
            while True:
                print(len(assert_list))
                if len(assert_list) == int(num):
                    self.text_output.append("create note sum: {}".format(len(assert_list)))
                    self.text_output.append("success!!")
                    self.text_output.moveCursor(self.text_output.textCursor().End)
                    break
                else:
                    self.text_output.append("create note sum: {}, loading...".format(len(assert_list)))
                    self.text_output.moveCursor(self.text_output.textCursor().End)
                    time.sleep(1)
                    continue
        except:
            self.text_output.append("create fail")