import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from main_window1 import Ui_MainWindow
from diagnose import Ui_Dialog
from result import Ui_Dialog_Result
from profile import Ui_Dialog_Profile
from home import Ui_Dialog_Home
from forum import Ui_Dialog_Forum
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Med_Diagnotion.settings")
django.setup()
from Med_Diagnotion_app.models import CustomUser, Diagnosis
from utils.ANN import user_symptoms_utils
from utils.description import get_decs_utils


diseases = {
    "Select an option": "",
    "Muscle wasting": "muscle_wasting",
    "Patches in throat": "patches_in_throat",
    "Dark urine": "dark_urine",
    "Stomach pain": "stomach_pain",
    "Acidity": "acidity",
    "Ulcers on tongue": "ulcers_on_tongue",
    "Vomiting": "vomiting",
    "High fever": "high_fever",
    "Weight loss": "weight_loss"
}


class AppController:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.predicted_disease = ''
        self.email_user = ''

        self.mainwindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mainwindow)

        self.diagnose_dialog = QtWidgets.QDialog()
        self.diagnose_ui = Ui_Dialog()
        self.diagnose_ui.setupUi(self.diagnose_dialog)

        self.result_dialog = QtWidgets.QDialog()
        self.result_ui = Ui_Dialog_Result()
        self.result_ui.setupUi(self.result_dialog)

        self.profile_dialog = QtWidgets.QDialog()
        self.profile_ui = Ui_Dialog_Profile()
        self.profile_ui.setupUi(self.profile_dialog)

        self.home_dialog = QtWidgets.QDialog()
        self.home_ui = Ui_Dialog_Home()
        self.home_ui.setupUi(self.home_dialog)

        self.forum_dialog = QtWidgets.QDialog()
        self.forum_ui = Ui_Dialog_Forum()
        self.forum_ui.setupUi(self.forum_dialog)

        self.ui.login.clicked.connect(self.handle_login)
        self.diagnose_ui.pushButton_3.clicked.connect(self.diagnose_handler)
        self.result_ui.pushButton_2.clicked.connect(self.show_diagnose_dialog)
        self.result_ui.pro_button.clicked.connect(self.show_profile_dialog)
        self.home_ui.pushButton.clicked.connect(self.show_diagnose_dialog)
        self.home_ui.pushButton_2.clicked.connect(self.show_forum_dialog)
        self.home_ui.pushButton_3.clicked.connect(self.show_profile_dialog)







    def handle_login(self):
        email = self.ui.email.text()
        self.email_user = email
        password = self.ui.password.text()
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            print(f"Login successful! Welcome, {email}")
            self.show_home_dialog()
        else:
            QMessageBox.warning(self.mainwindow, "Login Failed", "Invalid email or password.")
            return


    def diagnose_handler(self):
        symptom1 = self.diagnose_ui.comboBox.currentText()
        symptom2 = self.diagnose_ui.comboBox_2.currentText()
        symptom3 = self.diagnose_ui.comboBox_3.currentText()
        symptom4 = self.diagnose_ui.comboBox_4.currentText()
        symptom5 = self.diagnose_ui.comboBox_5.currentText()

        value1 = diseases.get(symptom1, "")
        value2 = diseases.get(symptom2, "")
        value3 = diseases.get(symptom3, "")
        value4 = diseases.get(symptom4, "")
        value5 = diseases.get(symptom5, "")

        self.predicted_disease = user_symptoms_utils(value1, value2, value3, value4, value5)
        self.show_result_dialog()


    def show_MainWindow(self):
        self.mainwindow.show()

    def show_diagnose_dialog(self):
        self.diagnose_dialog.exec_()


    def show_profile_dialog(self):
        self.profile_dialog.exec_()


    def show_result_dialog(self):
        decs = get_decs_utils(self.predicted_disease)
        self.result_ui.desease_label.setText(self.predicted_disease)
        self.result_ui.disc_label.setText(decs)
        self.result_dialog.exec_()


    def show_home_dialog(self):
        self.home_dialog.exec_()


    def show_forum_dialog(self):
        self.forum_dialog.exec_()


    def run(self):
        sys.exit(self.app.exec_())



if __name__ == "__main__":
    app_controller = AppController()
    app_controller.show_MainWindow()
    app_controller.run()
