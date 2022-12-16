
from PyQt5.QtWidgets import *

def message_box_error_string():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)

    # setting message for Message Box
    msg.setText("Digite apenas caracteres alfanuméricos.")

    # setting Message box window title
    msg.setWindowTitle("Mensagem de erro.")

    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok)

    # start the app
    retval = msg.exec_()


def message_box_error_numeric():
    msg = QMessageBox()

    # setting message for Message Box
    msg.setText("O campo deve conter apenas valores númericos.")

    # setting Message box window title
    msg.setWindowTitle("Mensagem de erro.")

    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok)

    # start the app
    retval = msg.exec_()


def message_box_error_max_limit(n):
    msg = QMessageBox()

    # setting message for Message Box
    msg.setText(f"O usuário excedeu o limite: ({n})")

    # setting Message box window title
    msg.setWindowTitle("Mensagem de erro.")

    # declaring buttons on Message Box
    msg.setStandardButtons(QMessageBox.Ok)

    # start the app
    retval = msg.exec_()