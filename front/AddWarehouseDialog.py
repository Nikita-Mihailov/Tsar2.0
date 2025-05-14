from itertools import product

from PyQt5 import QtWidgets
import requests
from PyQt5.QtWidgets import QMessageBox


class AddWarehouseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Добавление")
        self.setFixedSize(300, 150)
        self.api_url = "http://127.0.0.1:8000/api"
        layout = QtWidgets.QVBoxLayout()

        # Информация о товаре
        self.name = QtWidgets.QLineEdit()
        self.name.setPlaceholderText("Название продукта")

        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setRange(1, 1000)
        self.quantity_input.setValue(1)

        # Кнопки
        self.save_btn = QtWidgets.QPushButton("Добавить")
        self.save_btn.clicked.connect(self.add_warehouse)

        self.cancel_btn = QtWidgets.QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        # Добавление элементов в layout
        layout.addWidget(self.name)
        layout.addWidget(self.quantity_input)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)
    def add_warehouse(self):
        if self.accept:
            try:
                data = {
                    "product_name": self.name.text(),
                    "quantity": self.quantity_input.value()
                }
                response = requests.post(
                    f"{self.api_url}/warehouse/",
                    json = data
                )
                if response.status_code == 201:
                    data = response.json()
                    QtWidgets.QMessageBox.information(self, "Успех", f"Товар {data.get('product_name')} добавлен")
                    self.accept()
                else:
                    self.show_error(f"Ошибка: {response.status_code}")
            except Exception as e:
                self.show_error(f"Не удалось подключиться к серверу: {str(e)}")
