import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from EditQuantityDialog import EditQuantityDialog
from Front.AddWarehouseDialog import AddWarehouseDialog
from Front.DeteleWarehouseDialog import DeleteWarehouseDialog
from login_window import LoginWindow
from buy_window import OrderDialog


# Ваш сгенерированный класс UI (можно оставить как есть)
class Ui_TsarCannon(object):
    def setupUi(self, TsarCannon):
        TsarCannon.setObjectName("TsarCannon")
        TsarCannon.resize(1127, 904)
        self.layoutWidget = QtWidgets.QWidget(TsarCannon)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 90, 1011, 91))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(150, 60))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(150, 60))
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(150, 60))
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_2.addWidget(self.pushButton_7)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(150, 60))
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_2.addWidget(self.pushButton_8)
        self.label = QtWidgets.QLabel(TsarCannon)
        self.label.setGeometry(QtCore.QRect(210, 10, 711, 41))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(TsarCannon)
        self.widget.setGeometry(QtCore.QRect(59, 199, 1011, 651))
        self.widget.setObjectName("widget")
        self.scrollArea = QtWidgets.QScrollArea(self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(39, 49, 931, 611))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 929, 609))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(TsarCannon)
        QtCore.QMetaObject.connectSlotsByName(TsarCannon)
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.setLayout(self.scrollLayout)
        self.retranslateUi(TsarCannon)
        QtCore.QMetaObject.connectSlotsByName(TsarCannon)

    def retranslateUi(self, TsarCannon):
        _translate = QtCore.QCoreApplication.translate
        TsarCannon.setWindowTitle(_translate("TsarCannon", "TsarCannon"))
        self.pushButton_5.setText(_translate("TsarCannon", "products"))
        self.pushButton_6.setText(_translate("TsarCannon", "Warehouse"))
        self.pushButton_7.setText(_translate("TsarCannon", "Order"))
        self.pushButton_8.setText(_translate("TsarCannon", "clients"))
        self.label.setText(_translate("TsarCannon", "Царь Пушка"))


# Главный класс приложения
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_window = LoginWindow()
        self.api_url = "http://127.0.0.1:8000/api"
        if self.login_window.exec_() != QtWidgets.QDialog.accept:
            self.is_admin = self.login_window.is_admin
        else:
            self.close()
        # Создаем экземпляр UI и настраиваем его
        self.ui = Ui_TsarCannon()
        self.ui.setupUi(self)
        self.setup_buttons()
        # # Подключаем кнопки к обработчикам
        # self.ui.pushButton_6.clicked.setVisible(self.is_admin)
        # self.ui.pushButton_8.clicked.setVisible(self.is_admin)
        # self.ui.pushButton_5.clicked.connect(self.load_products)
        # self.ui.pushButton_6.clicked.connect(self.load_warehouse)
        # self.ui.pushButton_8.clicked.connect(self.on_clients_click)
        # self.ui.pushButton_7.clicked.connect(self.on_order_click)

    def setup_buttons(self):
        """Настройка видимости и обработчиков кнопок"""
        # Общие кнопки
        self.ui.pushButton_5.clicked.connect(self.load_products)
        self.ui.pushButton_7.clicked.connect(self.on_order_click)

        # Админские кнопки
        self.ui.pushButton_6.setVisible(self.is_admin)
        self.ui.pushButton_8.setVisible(self.is_admin)

        if self.is_admin:
            self.ui.pushButton_6.clicked.connect(self.load_warehouse)
            self.ui.pushButton_8.clicked.connect(self.on_clients_click)

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)

    # Обработчики кнопок (можно заменить на свою логику)
    def load_products(self):
        self.clear_scroll_area()
        name = QtWidgets.QLineEdit()
        name.setPlaceholderText("Название продукта")
        add_product_btn = QtWidgets.QPushButton("фильтровать")
        add_product_btn.clicked.connect(lambda: self.filter(name=name.text()))
        self.ui.scrollLayout.addWidget(name)
        self.ui.scrollLayout.addWidget(add_product_btn)
        try:
            response = requests.get(f"{self.api_url}/product/list/?skip=0&limit=100")
            if response.status_code == 200:
                data = response.json()
                if not isinstance(data, list):
                    self.show_error("Некорректный формат данных от сервера")
                    return

                for product in data:
                    if not product.get("name") or not product.get("price"):
                        continue
                    self.add_product_to_list(product)
        except Exception as e:
            self.show_error(f"Не удалось подключиться к серверу: {str(e)}")

    def filter(self, name):
        self.clear_scroll_area()
        try:
            response = requests.get(f"{self.api_url}/product/?product_name={name}")
            if response.status_code == 200:
                product = response.json()
                self.add_product_to_list(product)
        except Exception as e:
            self.show_error(f"Не удалось подключиться к серверу: {str(e)}")

    def clear_scroll_area(self):
        # Удаляем все элементы из scrollArea
        while self.ui.scrollLayout.count():
            item = self.ui.scrollLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_product_to_list(self, product):
        # Создаем виджет для одного товара
        product_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(product_widget)
        name = str(product.get("name", "Без названия"))
        price = str(product.get("price", "N/A"))

        # Добавляем элементы (название, цена, кнопка и т. д.)
        name_label = QtWidgets.QLabel(name)
        price_label = QtWidgets.QLabel(f"{price} $.")
        buy_button = QtWidgets.QPushButton("Подробнее")
        buy_button.clicked.connect(
            lambda _, p=name: self.load_product_detail(p)
        )

        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(buy_button)

        # Добавляем виджет товара в scrollArea
        self.ui.scrollLayout.addWidget(product_widget)

    def load_product_detail(self, product_name):
        self.clear_scroll_area()
        try:
            # Первый запрос - информация о товаре
            product_response = requests.get(
                f"{self.api_url}/product/?product_name={product_name}"
            )

            if product_response.status_code != 200:
                self.show_error(f"Ошибка получения данных товара: {product_response.status_code}")
                return

            product_data = product_response.json()
            if not product_data or "id" not in product_data:
                self.show_error("Некорректные данные товара")
                return

            # Второй запрос - информация о складе
            warehouse_response = requests.get(
                f"{self.api_url}/warehouse/?product_name={product_data['name']}"
            )

            if warehouse_response.status_code != 200:
                self.show_error(f"Ошибка получения данных склада: {warehouse_response.status_code}")
                return

            warehouse_data = warehouse_response.json()
            self.add_product_widget(product_data, warehouse_data)

        except Exception as e:
            self.show_error(f"Ошибка при загрузке деталей: {str(e)}")

    def add_product_widget(self, product, warehouse_data):
        product_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(product_widget)

        name_label = QtWidgets.QLabel(product["name"])
        price_label = QtWidgets.QLabel(f"{product['price']} $")
        quantity_label = QtWidgets.QLabel(f"{warehouse_data['quantity']} шт.")

        order_btn = QtWidgets.QPushButton("Заказать")


        # Подключаем кнопки
        order_btn.clicked.connect(lambda: self.create_order(product, warehouse_data))


        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(quantity_label)
        layout.addWidget(order_btn)


        self.ui.scrollLayout.addWidget(product_widget)

    def create_order(self, product, warehouse_data):
        dialog = OrderDialog(product, warehouse_data, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.process_order(dialog.order_data, warehouse_data, dialog.quantity_input)

    def process_order(self, order_data, warehouse_data, quantity_input):
        try:
            # Отправляем заказ на сервер
            response = requests.post(
                f"{self.api_url}/order/",
                json=order_data
            )
            print(quantity_input.value())
            print(warehouse_data.get("quantity"))
            if response.status_code == 201:
                update_data = {
                    "product_name": order_data["product_name"],
                    "quantity": int(warehouse_data.get("quantity")) - int(quantity_input.value())
                }
                print(update_data["quantity"])
                update_response = requests.patch(
                    f"{self.api_url}/warehouse/?product_name={update_data["product_name"]}",
                    json=update_data
                )

                if update_response.status_code == 200:
                    QtWidgets.QMessageBox.information(self, "Успех", "Заказ оформлен!")
                    self.load_products()  # Обновляем список
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось обновить склад")
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Не удалось создать заказ")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Ошибка соединения: {str(e)}")


    def load_warehouse(self):
        self.clear_scroll_area()
        add_product_btn = QtWidgets.QPushButton("Добавить продукт")
        add_product_btn.clicked.connect(self.open_add_product_dialog)  # Привязываем к функции
        self.ui.scrollLayout.addWidget(add_product_btn)  # Добавляем в scrollLayout
        try:
            response = requests.get(f"{self.api_url}/warehouse/list/")
            if response.status_code == 200:
                data = response.json()
                for product in data:
                    self.patch_product_to_list(product)
            else:
                self.show_error(f"Ошибка: {response.status_code}")
        except Exception as e:
            self.show_error(f"Не удалось подключиться к серверу: {str(e)}")

    def open_add_product_dialog(self):
        dialog = AddWarehouseDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_warehouse()

    def patch_product_to_list(self, product):
        # Создаем виджет для одного товара
        product_widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(product_widget)

        # Добавляем элементы (название, цена, кнопка и т. д.)
        name_label = QtWidgets.QLabel(str(product["product_name"]))
        price_label = QtWidgets.QLabel(f"{product['quantity']} шт.")
        buy_button = QtWidgets.QPushButton("Редактировать")
        delete_button = QtWidgets.QPushButton("Удалить")
        buy_button.clicked.connect(lambda: self.edit_quantity_warehouse(product))
        delete_button.clicked.connect(lambda: self.delete_warehouse_dialog(product))

        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(buy_button)
        layout.addWidget(delete_button)

        # Добавляем виджет товара в scrollArea
        self.ui.scrollLayout.addWidget(product_widget)

    def edit_quantity_warehouse(self, product):
        # Создаем словарь с объединенными данными
        product_data = {
            "product_name": product["product_name"],
            "quantity": product["quantity"]
        }

        dialog = EditQuantityDialog(product_data, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            update_data = dialog.get_data()
            self.update_warehouse_quantity(update_data)

    def delete_warehouse_dialog(self, product):
        dialog = DeleteWarehouseDialog(product, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_warehouse()


    def update_warehouse_quantity(self, update_data):
        try:
            response = requests.patch(
                f"{self.api_url}/warehouse/?product_name={update_data["product_name"]}",
                json={
                    "product_name": update_data["product_name"],
                    "quantity": update_data["quantity"]
                }
            )

            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Успех", "Количество обновлено!")
                self.load_warehouse()  # Обновляем список
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Ошибка",
                    f"Не удалось обновить: {response.text}"
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка соединения: {str(e)}"
            )

    def on_order_click(self):
        print("Кнопка Order нажата")

    def on_clients_click(self):
        print("Кнопка Clients нажата")


# Запуск приложения
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())