import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from detail_dialog_ui import Ui_Dialog  # UI faylindan generate edilmis .py fayl
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from pathlib import Path




pr = 'page1.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class DetailDialog(QDialog):
    def __init__(self, parent=None, room_index=0, existing_data=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.room_index = room_index
        self.result = None

        # Əvvəlki məlumat varsa, spinbox və doubleSpinbox-lara yüklə
        if existing_data:
            self.ui.spinBox_qapi_sayi.setValue(existing_data.get("qapi_sayi", 0))
            self.ui.doubleSpinBox_qapi_eni.setValue(existing_data.get("qapi_eni", 0.0))
            self.ui.doubleSpinBox_qapi_uzun.setValue(existing_data.get("qapi_uzun", 0.0))
            self.ui.spinBox_pencere_sayi.setValue(existing_data.get("pencere_sayi", 0))
            self.ui.doubleSpinBox_pencere_eni.setValue(existing_data.get("pencere_eni", 0.0))
            self.ui.doubleSpinBox_pencere_uzun.setValue(existing_data.get("pencere_uzun", 0.0))

        self.ui.pushButton.clicked.connect(self.confirm_clicked)

    def confirm_clicked(self):
        self.result = {
            "qapi_sayi": self.ui.spinBox_qapi_sayi.value(),
            "qapi_eni": self.ui.doubleSpinBox_qapi_eni.value(),
            "qapi_uzun": self.ui.doubleSpinBox_qapi_uzun.value(),
            "pencere_sayi": self.ui.spinBox_pencere_sayi.value(),
            "pencere_eni": self.ui.doubleSpinBox_pencere_eni.value(),
            "pencere_uzun": self.ui.doubleSpinBox_pencere_uzun.value()
        }
        self.accept()


class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.next.clicked.connect(self.OK2)
        self.ui.print.clicked.connect(self.print_to_pdf)
        self.checkboxes = []
        self.combo_boxes = []
        self.width_inputs = []
        self.length_inputs = []
        self.dot_buttons = []
        self.room_details = {}

        for i in range(1, 11):
            chk = self.findChild(QCheckBox, f"checkBox_{i}")
            cmb = self.findChild(QComboBox, f"comboBox_{i}")
            width = self.findChild(QDoubleSpinBox, f"doubleSpinBox_en_{i}")
            length = self.findChild(QDoubleSpinBox, f"doubleSpinBox_uzunluq_{i}")
            btn = self.findChild(QPushButton, f"pushButton_detail_{i}")

            self.checkboxes.append(chk)
            self.combo_boxes.append(cmb)
            self.width_inputs.append(width)
            self.length_inputs.append(length)
            self.dot_buttons.append(btn)

            if chk:
                chk.stateChanged.connect(self.checkbox_changed)

            if btn:
                btn.clicked.connect(lambda _, index=i - 1: self.open_detail_dialog(index))

        self.init_rows()
    def print_to_pdf(self):
        # ✅ Fontu qeydiyyatdan keçirt
        font_path = "C:/Windows/Fonts/times.ttf"  # Windows üçün Times New Roman
        if not os.path.exists(font_path):
            QMessageBox.warning(self, "Font tapılmadı", "Times New Roman font faylı tapılmadı.")
            return

        pdfmetrics.registerFont(TTFont("TimesNewRoman", font_path))

        # ✅ Hündürlüyü oxu
        height_text = self.ui.h.text()
        try:
            height = float(height_text)
        except ValueError:
            QMessageBox.warning(self, "Xəta", "Zəhmət olmasa düzgün hündürlük (h) dəyəri daxil edin.")
            return

        # ✅ Documents qovluğunda fayl yarat
        documents_path = Path.home() / "Documents"
        base_name = "menzil_melumatlari"
        n = 1
        pdf_path = documents_path / f"{base_name}_{n}.pdf"
        while pdf_path.exists():
            n += 1
            pdf_path = documents_path / f"{base_name}_{n}.pdf"

        # ✅ PDF faylını yarat
        c = canvas.Canvas(str(pdf_path), pagesize=A4)
        width, height_pdf = A4
        y = height_pdf - 50
        c.setFont("TimesNewRoman", 12)

        c.drawString(50, y, f"Hündürlük (h): {height_text} m")
        y -= 30

        for i in range(10):
            if self.checkboxes[i].isChecked():
                room_name = self.combo_boxes[i].currentText()
                eni = self.width_inputs[i].value()
                uzunluq = self.length_inputs[i].value()

                detail = self.room_details.get(i, {
                    "qapi_sayi": 0,
                    "qapi_eni": 0,
                    "qapi_uzun": 0,
                    "pencere_sayi": 0,
                    "pencere_eni": 0,
                    "pencere_uzun": 0
                })

                qapi_sahesi = detail["qapi_sayi"] * detail["qapi_eni"] * detail["qapi_uzun"]
                pencere_sahesi = detail["pencere_sayi"] * detail["pencere_eni"] * detail["pencere_uzun"]
                tavan_sahesi = eni * uzunluq
                doseme_sahesi = eni * uzunluq
                divar_sahesi = (2 * (eni * height + uzunluq * height)) - qapi_sahesi - pencere_sahesi

                c.drawString(50, y, f"{i+1}. Otaq: {room_name}")
                y -= 20
                c.drawString(70, y, f"Eni: {eni} m, Uzunluğu: {uzunluq} m")
                y -= 20
                c.drawString(70, y, f"Tavan sahəsi: {tavan_sahesi:.2f} m²")
                y -= 20
                c.drawString(70, y, f"Döşəmə sahəsi: {doseme_sahesi:.2f} m²")
                y -= 20
                c.drawString(70, y, f"Divar sahəsi: {divar_sahesi:.2f} m²")
                y -= 20
                c.drawString(70, y, f"Qapılar: Sayı={detail['qapi_sayi']}, Ölçü={detail['qapi_eni']}m x {detail['qapi_uzun']}m")
                y -= 20
                c.drawString(70, y, f"Pəncərələr: Sayı={detail['pencere_sayi']}, Ölçü={detail['pencere_eni']}m x {detail['pencere_uzun']}m")
                y -= 30

                if y < 100:
                    c.showPage()
                    y = height_pdf - 50
                    c.setFont("TimesNewRoman", 12)

        c.save()

        QMessageBox.information(self, "Uğur", f"PDF yaradıldı:\n{pdf_path}")
   
    def init_rows(self):
        for i in range(10):
            if i == 0:
                self.checkboxes[i].setEnabled(True)
                self.checkboxes[i].setChecked(True)
                self.set_row_enabled(i, combo=True, others=True)
            elif i == 1:
                self.checkboxes[i].setEnabled(True)
                self.checkboxes[i].setChecked(False)
                self.set_row_enabled(i, combo=False, others=False)
            else:
                self.checkboxes[i].setEnabled(False)
                self.checkboxes[i].setChecked(False)
                self.set_row_enabled(i, combo=False, others=False)

    def set_row_enabled(self, index, combo, others):
        self.combo_boxes[index].setEnabled(combo)
        self.width_inputs[index].setEnabled(others)
        self.length_inputs[index].setEnabled(others)
        self.dot_buttons[index].setEnabled(others)

    def checkbox_changed(self):
        for i in range(10):
            if self.checkboxes[i].isChecked():
                self.set_row_enabled(i, combo=True, others=True)
                if i + 1 < 10:
                    self.checkboxes[i + 1].setEnabled(True)
                    self.set_row_enabled(i + 1, combo=False, others=False)
            else:
                self.set_row_enabled(i, combo=False, others=False)
                for j in range(i + 1, 10):
                    self.checkboxes[j].setChecked(False)
                    self.checkboxes[j].setEnabled(False)
                    self.set_row_enabled(j, combo=False, others=False)

    def open_detail_dialog(self, index):
        existing_data = self.room_details.get(index)
        dialog = DetailDialog(self, room_index=index, existing_data=existing_data)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.result
            print(f"{index+1}-ci otaq ucun daxil edilmis melumatlar:", data)
            self.room_details[index] = data

    def OK2(self):
        from subprocess import call
        call(["python", "page_2.py"])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(app.exec())
























# import sys
# from PyQt5 import uic
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from detail_dialog_ui import Ui_Dialog  # UI faylindan generate edilmis .py fayl

# pr = 'page1.ui'
# Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


# class DetailDialog(QDialog):
#     def __init__(self, parent=None, room_index=0):
#         super().__init__(parent)
#         self.ui = Ui_Dialog()
#         self.ui.setupUi(self)

#         self.room_index = room_index
#         self.result = None

#         self.ui.pushButton.clicked.connect(self.confirm_clicked)

#     def confirm_clicked(self):
#         self.result = {
#             "qapi_sayi": self.ui.spinBox_qapi_sayi.value(),
#             "qapi_eni": self.ui.doubleSpinBox_qapi_eni.value(),
#             "qapi_uzun": self.ui.doubleSpinBox_qapi_uzun.value(),
#             "pencere_sayi": self.ui.spinBox_pencere_sayi.value(),
#             "pencere_eni": self.ui.doubleSpinBox_pencere_eni.value(),
#             "pencere_uzun": self.ui.doubleSpinBox_pencere_uzun.value()
#         }
#         self.accept()


# class mywindow(QMainWindow):
#     def __init__(self):
#         super(mywindow, self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.pb2.clicked.connect(self.OK2)

#         self.checkboxes = []
#         self.combo_boxes = []
#         self.width_inputs = []
#         self.length_inputs = []
#         self.dot_buttons = []
#         self.room_details = {}

#         for i in range(1, 11):
#             chk = self.findChild(QCheckBox, f"checkBox_{i}")
#             cmb = self.findChild(QComboBox, f"comboBox_{i}")
#             width = self.findChild(QDoubleSpinBox, f"doubleSpinBox_en_{i}")
#             length = self.findChild(QDoubleSpinBox, f"doubleSpinBox_uzunluq_{i}")
#             btn = self.findChild(QPushButton, f"pushButton_detail_{i}")

#             self.checkboxes.append(chk)
#             self.combo_boxes.append(cmb)
#             self.width_inputs.append(width)
#             self.length_inputs.append(length)
#             self.dot_buttons.append(btn)

#             if chk:
#                 chk.stateChanged.connect(self.checkbox_changed)

#             if btn:
#                 btn.clicked.connect(lambda _, index=i - 1: self.open_detail_dialog(index))

#         self.init_rows()

#     def init_rows(self):
#         for i in range(10):
#             if i == 0:
#                 self.checkboxes[i].setEnabled(True)
#                 self.checkboxes[i].setChecked(True)
#                 self.set_row_enabled(i, combo=True, others=True)
#             elif i == 1:
#                 self.checkboxes[i].setEnabled(True)
#                 self.checkboxes[i].setChecked(False)
#                 self.set_row_enabled(i, combo=False, others=False)
#             else:
#                 self.checkboxes[i].setEnabled(False)
#                 self.checkboxes[i].setChecked(False)
#                 self.set_row_enabled(i, combo=False, others=False)

#     def set_row_enabled(self, index, combo, others):
#         self.combo_boxes[index].setEnabled(combo)
#         self.width_inputs[index].setEnabled(others)
#         self.length_inputs[index].setEnabled(others)
#         self.dot_buttons[index].setEnabled(others)

#     def checkbox_changed(self):
#         for i in range(10):
#             if self.checkboxes[i].isChecked():
#                 self.set_row_enabled(i, combo=True, others=True)
#                 if i + 1 < 10:
#                     self.checkboxes[i + 1].setEnabled(True)
#                     self.set_row_enabled(i + 1, combo=False, others=False)
#             else:
#                 self.set_row_enabled(i, combo=False, others=False)
#                 for j in range(i + 1, 10):
#                     self.checkboxes[j].setChecked(False)
#                     self.checkboxes[j].setEnabled(False)
#                     self.set_row_enabled(j, combo=False, others=False)

#     def open_detail_dialog(self, index):
#         dialog = DetailDialog(self, room_index=index)
#         if dialog.exec_() == QDialog.Accepted:
#             data = dialog.result
#             print(f"{index+1}-ci otaq ucun daxil edilmis melumatlar:", data)
#             self.room_details[index] = data

#     def OK2(self):
#         from subprocess import call
#         call(["python", "page_2.py"])


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = mywindow()
#     win.show()
#     sys.exit(app.exec())




