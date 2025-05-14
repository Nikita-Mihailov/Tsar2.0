from PyQt5 import QtWidgets, QtCore


class OrderDialog(QtWidgets.QDialog):
    def __init__(self, product_data, warehouse_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.warehouse_data = warehouse_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Оформление заказа")
        self.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Поля формы
        self.product_name = QtWidgets.QLabel(f"Товар: {self.product_data['name']}")
        self.available_label = QtWidgets.QLabel(f"Доступно: {self.warehouse_data['quantity']} шт.")

        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setRange(1, self.warehouse_data['quantity'])
        self.quantity_input.setValue(1)

        # "client_fio": "string",
        # "product_name": "string",
        # "content": "string",
        # "purchase_price": 0

        self.client_name = QtWidgets.QLineEdit()
        self.client_name.setPlaceholderText("Имя клиента")

        self.address = QtWidgets.QLineEdit()
        self.address.setPlaceholderText("Адрес")

        # Кнопки
        self.submit_btn = QtWidgets.QPushButton("Подтвердить заказ")
        self.submit_btn.clicked.connect(self.submit_order)

        self.cancel_btn = QtWidgets.QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        # Добавляем элементы в layout
        layout.addWidget(self.product_name)
        layout.addWidget(self.available_label)
        layout.addWidget(QtWidgets.QLabel("Количество:"))
        layout.addWidget(self.quantity_input)
        layout.addWidget(QtWidgets.QLabel("Данные клиента:"))
        layout.addWidget(self.client_name)

        layout.addWidget(self.address)
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

    def submit_order(self):
        if not all([self.client_name.text()]):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
            return

        order_data = {
            "client_fio": self.client_name.text(),
            "product_name": self.product_data["name"],
            "content": f"{self.quantity_input.value()} шт",
            "purchase_price": self.quantity_input.value() * self.product_data["price"],
            "address": self.address.text()
        }

        self.order_data = order_data
        self.accept()