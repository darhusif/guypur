from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import *
import pygame  

class HamsterClicker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hamster Clicker')
        self.resize(700, 500)
        
        
        pygame.mixer.init()

        
        self.click_sound = pygame.mixer.Sound("click_sound.mp3") 
        
        self.score = 0
        self.upgrade_cost = 100
        self.auto_click_increase = 1
        self.auto_click_active = False
        self.end_cost = 1500  

        self.shop_items = [
            {"name": "Кепка", "message": "Кепка добавлена!", "cost": 150},
            {"name": "Очки", "message": "Очки добавлены!", "cost": 150},
            {"name": "Золотая цепочка", "message": "Цепочка добавлена!", "cost": 150},
        ]

        # Основное изображение
        self.label_p = QLabel(self)
        pixmapimage = QPixmap('hamster.jpeg').scaled(300, 300, Qt.KeepAspectRatio)
        self.label_p.setPixmap(pixmapimage)
        self.label_p.setAlignment(Qt.AlignCenter)
        self.label_p.mousePressEvent = self.increase_score

        # Текущий счёт
        self.score_label = QLabel(f"Монеты: {self.score}")
        self.score_label.setAlignment(Qt.AlignCenter)

        # Кнопки
        self.shop_button = QPushButton("Магазин")
        self.upgrade_button = QPushButton("Улучшения")
        self.end_button = QPushButton(f"Конец - {self.end_cost} монет")
        self.shop_button.clicked.connect(self.open_shop)
        self.upgrade_button.clicked.connect(self.open_upgrade)
        self.end_button.clicked.connect(self.end_game)

        # Таймер для автоматического заработка монет
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_click)

        # Размещение элементов
        layout = QVBoxLayout()
        layout.addWidget(self.score_label)
        layout.addWidget(self.label_p)
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.shop_button)
        buttons_layout.addWidget(self.upgrade_button)
        buttons_layout.addWidget(self.end_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def increase_score(self, event):
        self.score += 1
        self.update_score()
        self.play_click_sound()  # Воспроизведение звука при клике

    def play_click_sound(self):
        """Проигрывание звука клика"""
        self.click_sound.play()

    def update_score(self):
        self.score_label.setText(f"Монеты: {self.score}")

    def open_shop(self):
        shop_window = QDialog(self)
        shop_window.setWindowTitle("Магазин")
        shop_window.resize(300, 200)

        layout = QVBoxLayout()
        for item in self.shop_items[:]:  # Используем копию списка, чтобы избежать проблем с удалением
            button = QPushButton(f"{item['name']} - {item['cost']} монет")
            button.clicked.connect(lambda _, item=item: self.buy_item(item, shop_window))
            layout.addWidget(button)

        shop_window.setLayout(layout)
        shop_window.exec()

    def buy_item(self, item, shop_window):
        if self.score >= item["cost"]:
            self.score -= item["cost"]
            self.update_score()
            QMessageBox.information(self, "Успех", item["message"])
            self.shop_items.remove(item)  # Удаляем купленный предмет из списка
            shop_window.close()  # Закрываем окно магазина, чтобы обновить список
            self.open_shop()  # Открываем магазин снова с обновлённым списком
        else:
            QMessageBox.warning(self, "Ошибка", "Недостаточно денег!")

    def open_upgrade(self):
        upgrade_window = QDialog(self)
        upgrade_window.setWindowTitle("Улучшения")
        upgrade_window.resize(300, 200)

        layout = QVBoxLayout()
        upgrade_button = QPushButton(f"Увеличить автоклик - {self.upgrade_cost} монет")
        upgrade_button.clicked.connect(lambda: self.buy_upgrade(upgrade_button))
        layout.addWidget(upgrade_button)

        upgrade_window.setLayout(layout)
        upgrade_window.exec()

    def buy_upgrade(self, button):
        if self.score >= self.upgrade_cost:
            self.score -= self.upgrade_cost
            self.update_score()
            self.auto_click_increase += 4
            self.upgrade_cost += 50
            button.setText(f"Увеличить автоклик - {self.upgrade_cost} монет")
            if not self.auto_click_active:
                self.timer.start(1000)
                self.auto_click_active = True
        else:
            QMessageBox.warning(self, "Ошибка", "Недостаточно денег!")

    def auto_click(self):
        self.score += self.auto_click_increase
        self.update_score()

    def end_game(self):
        if self.score >= self.end_cost:
            self.score -= self.end_cost
            self.update_score()
            end_window = QDialog(self)
            end_window.setWindowTitle("Конец игры")
            end_window.resize(200, 100)

            layout = QVBoxLayout()
            label = QLabel("Вы победили!")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            end_window.setLayout(layout)
            end_window.exec()
            self.close()
        else:
            QMessageBox.warning(self, "Ошибка", "Недостаточно денег для завершения игры!")


if __name__ == "__main__":
    app = QApplication([])
    window = HamsterClicker()
    window.show()
    app.exec()
