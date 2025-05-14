from PyQt5 import QtWidgets


class EditQuantityDialog(QtWidgets.QDialog):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Редактирование количества")
        self.setFixedSize(300, 150)

        layout = QtWidgets.QVBoxLayout()

        # Информация о товаре
        self.product_label = QtWidgets.QLabel(
            f"Товар: {self.product_data.get('product_name', 'Без названия')}"
        )

        # Поле для ввода количества
        self.quantity_spinbox = QtWidgets.QSpinBox()
        self.quantity_spinbox.setRange(0, 10000)
        self.quantity_spinbox.setValue(self.product_data.get('quantity', 0))

        # Кнопки
        self.save_btn = QtWidgets.QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.accept)

        self.cancel_btn = QtWidgets.QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        # Добавление элементов в layout
        layout.addWidget(self.product_label)
        layout.addWidget(QtWidgets.QLabel("Новое количество:"))
        layout.addWidget(self.quantity_spinbox)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

    def get_data(self):
        """Возвращает обновленные данные"""
        return {
            "product_name": self.product_data["product_name"],
            "quantity": self.quantity_spinbox.value()
        }