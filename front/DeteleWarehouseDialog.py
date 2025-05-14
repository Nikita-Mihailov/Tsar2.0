from itertools import product

from PyQt5 import QtWidgets
import requests
from PyQt5.QtWidgets import QMessageBox


class DeleteWarehouseDialog(QtWidgets.QDialog):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Удаление")
        self.setFixedSize(300, 150)
        self.api_url = "http://127.0.0.1:8000/api"
        layout = QtWidgets.QVBoxLayout()

        # Информация о товаре
        self.product_label = QtWidgets.QLabel(
            f"Товар: {self.product_data.get('product_name')}"
        )

        # Кнопки
        self.save_btn = QtWidgets.QPushButton("Удалить")
        self.save_btn.clicked.connect(self.delete_warehouse)

        self.cancel_btn = QtWidgets.QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        # Добавление элементов в layout
        layout.addWidget(self.product_label)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)
    def delete_warehouse(self):
        if self.accept:
            try:
                response = requests.delete(f"{self.api_url}/warehouse/?product_name={self.product_data.get('product_name')}")
                if response.status_code == 204:
                    QtWidgets.QMessageBox.information(self, "Успех", f"Товар {self.product_data.get('product_name')} удален")
                    self.accept()
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", f"Товар {self.product_data.get('product_name')} не найден")
                    self.show_error(f"Ошибка: {response.status_code}")
            except Exception as e:
                self.show_error(f"Не удалось подключиться к серверу: {str(e)}")
