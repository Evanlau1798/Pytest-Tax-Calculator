from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QWidget, QApplication, QShortcut, QMainWindow,QSystemTrayIcon
from PyQt5.QtGui import QIntValidator
from qdarktheme import load_stylesheet
import sys


class Calc():
    def __init__(self):
        super().__init__()
        self.Exemptions = {"一般":92000,
                           "年滿70歲之納稅義務人、配偶及受納稅義務人扶養之直系尊親屬":138000}
        self.standard_Deductions = {"單身":124000,
                                    "有配偶者":248000}
        self.special_Deductions = {"薪資特別扣除額/薪資必要費用":207000,
                                   "身心障礙特別扣除額":207000,
                                   "幼兒學前特別扣除額":120000,
                                   "教育學費特別扣除額":25000,
                                   "儲蓄投資特別扣除額":270000,
                                   "長期照顧特別扣除額":120000}
        self.tax_percents = {(0.05,560000,0):"TWD 0~560,000", #(稅率,所得淨額,累進差額)
                             (0.12,1260000,37800):"TWD 560,001~1,260,000",
                             (0.20,2520000,134600):"TWD 1,260,001~2,520,000",
                             (0.30,4720000,376600):"TWD 2,520,001~4,720,000",
                             (0.40,4720001,829600):"TWD 4,720,001以上",}
        
    def calc(self,input):
        exemptions = self.Exemptions[input[0]]
        standard_Deductions = self.standard_Deductions[input[1]]
        special_Deductions = self.special_Deductions[input[2]]
        total_income = int(input[3])
        for percents, name in self.tax_percents.items():
            if total_income <= int(percents[1]) or total_income > 4720000:
                tax_percents = percents
                break
        net_comprehensive_income = total_income - exemptions - standard_Deductions - special_Deductions #綜合淨所得
        output = net_comprehensive_income * tax_percents[0] - tax_percents[2]
        if output <= 0:
            msg_box.warning("錯誤","請確保您輸入的所有資訊是正確的\n錯誤原因:所得稅小於0")
            return 0
        return output

class pyqt_ui(object):
    def __init__(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.MainWindow.show()
        sys.exit(app.exec_())

    def _init_calc(self):
        calc = Calc()
        exemptions = self.exemptions_comboBox.currentText()
        standard_Deductions = self.standard_deduction_combobox.currentText()
        special_Deductions = self.special_deduction_comboBox.currentText()
        total_income = self.total_income_lineEdit.text()
        input = (exemptions, standard_Deductions, special_Deductions, total_income)
        output = str(int(calc.calc(input=input)))
        self.output_label.setText(output)

    def change_total_income_lable(self, value):
        try:
            value = int(value)
            if value >= 0 and value <= 560000:
                self.tax_percents_range.setText("5%   TWD 0~560,000")
            elif value > 560000 and value <= 1260000:
                self.tax_percents_range.setText("12%   TWD 560,001~1,260,000")
            elif value > 1260000 and value <= 2520000:
                self.tax_percents_range.setText("20%   TWD 1,260,001~2,520,000")
            elif value > 2520000 and value <= 4720000:
                self.tax_percents_range.setText("30%   TWD 2,520,001~4,720,000")
            elif value > 4720000:
                self.tax_percents_range.setText("40%   TWD 4,720,001以上")
            self.calc_Button.setEnabled(True)
            return
        except Exception:
            self.calc_Button.setEnabled(False)
            if value != "":
                msg_box.warning("錯誤","請輸入正確的數字")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(QtCore.QSize(600, 400))
        MainWindow.setMaximumSize(QtCore.QSize(600, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(17)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setText("第一步:選擇綜合淨所得之細項")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.verticalLayout_6)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.exemptions_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.exemptions_comboBox.setObjectName("exemptions_comboBox")
        self.exemptions_comboBox.addItem("")
        self.exemptions_comboBox.addItem("")
        self.gridLayout.addWidget(self.exemptions_comboBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.standard_deduction_combobox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.standard_deduction_combobox.sizePolicy().hasHeightForWidth())
        self.standard_deduction_combobox.setSizePolicy(sizePolicy)
        self.standard_deduction_combobox.setObjectName("standard_deduction_combobox")
        self.standard_deduction_combobox.addItem("")
        self.standard_deduction_combobox.addItem("")
        self.gridLayout.addWidget(self.standard_deduction_combobox, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.special_deduction_comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.special_deduction_comboBox.setObjectName("special_deduction_comboBox")
        self.special_deduction_comboBox.addItem("")
        self.special_deduction_comboBox.addItem("")
        self.special_deduction_comboBox.addItem("")
        self.special_deduction_comboBox.addItem("")
        self.special_deduction_comboBox.addItem("")
        self.special_deduction_comboBox.addItem("")
        self.gridLayout.addWidget(self.special_deduction_comboBox, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setText("第二步:請輸入您的所得總額")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_7.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.verticalLayout_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.total_income_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.total_income_lineEdit.setText("")
        self.total_income_lineEdit.setCursorPosition(0)
        self.total_income_lineEdit.setObjectName("total_income_lineEdit")
        self.horizontalLayout.addWidget(self.total_income_lineEdit)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout.addWidget(self.label_7)
        self.tax_percents_range = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tax_percents_range.sizePolicy().hasHeightForWidth())
        self.tax_percents_range.setSizePolicy(sizePolicy)
        self.tax_percents_range.setObjectName("tax_percents_range")
        self.horizontalLayout.addWidget(self.tax_percents_range)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_2.addWidget(self.label_10)
        self.calc_Button = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calc_Button.sizePolicy().hasHeightForWidth())
        self.calc_Button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.calc_Button.setFont(font)
        self.calc_Button.setObjectName("calc_Button")
        self.horizontalLayout_2.addWidget(self.calc_Button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, -1, 300, 0)
        self.gridLayout_2.setSpacing(7)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 0, 0, 1, 1)
        self.output_label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output_label.sizePolicy().hasHeightForWidth())
        self.output_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.output_label.setFont(font)
        self.output_label.setText("")
        self.output_label.setObjectName("output_label")
        self.gridLayout_2.addWidget(self.output_label, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.calc_Button.clicked.connect(self._init_calc)
        self.total_income_lineEdit.textChanged.connect(self.change_total_income_lable)
        onlyInt = QIntValidator()
        onlyInt.setRange(0,2147483647)
        self.total_income_lineEdit.setValidator(onlyInt)
        self.calc_Button.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "所得稅計算機"))
        self.exemptions_comboBox.setItemText(0, _translate("MainWindow", "一般"))
        self.exemptions_comboBox.setItemText(1, _translate("MainWindow", "年滿70歲之納稅義務人、配偶及受納稅義務人扶養之直系尊親屬"))
        self.label_2.setText(_translate("MainWindow", "標準/列舉扣除額"))
        self.label_3.setText(_translate("MainWindow", "特別扣除額"))
        self.standard_deduction_combobox.setItemText(0, _translate("MainWindow", "單身"))
        self.standard_deduction_combobox.setItemText(1, _translate("MainWindow", "有配偶者"))
        self.label.setText(_translate("MainWindow", "免稅額"))
        self.special_deduction_comboBox.setItemText(0, _translate("MainWindow", "薪資特別扣除額/薪資必要費用"))
        self.special_deduction_comboBox.setItemText(1, _translate("MainWindow", "身心障礙特別扣除額"))
        self.special_deduction_comboBox.setItemText(2, _translate("MainWindow", "幼兒學前特別扣除額"))
        self.special_deduction_comboBox.setItemText(3, _translate("MainWindow", "教育學費特別扣除額"))
        self.special_deduction_comboBox.setItemText(4, _translate("MainWindow", "儲蓄投資特別扣除額"))
        self.special_deduction_comboBox.setItemText(5, _translate("MainWindow", "長期照顧特別扣除額"))
        self.label_6.setText(_translate("MainWindow", "年所得總額："))
        self.total_income_lineEdit.setPlaceholderText(_translate("MainWindow", "請輸入金額"))
        self.label_7.setText(_translate("MainWindow", "課稅級距:"))
        self.tax_percents_range.setText(_translate("MainWindow", "5%   TWD 0~560,000"))
        self.label_10.setText(_translate("MainWindow", "第三步：開始計算"))
        self.calc_Button.setText(_translate("MainWindow", "計算!"))
        self.label_11.setText(_translate("MainWindow", "您本次需要繳納的所得稅為："))

class msg_window(QWidget):
    def information(self,title:str,message):
        message = str(message)
        QMessageBox.information(self,title,message)

    def warning(self,title:str,message):
        message = str(message)
        QMessageBox.warning(self,title,message)

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setStyleSheet(load_stylesheet())
    msg_box = msg_window()
    main_app = pyqt_ui()