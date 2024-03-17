import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
import os

class PostViewerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Получение информации о посте")
        self.setGeometry(100, 100, 400, 400)

        self.label = QLabel("Введите ID поста:", self)
        self.label.move(20, 20)

        self.entry = QLineEdit(self)
        self.entry.setGeometry(150, 20, 200, 30)

        self.button = QPushButton("Получить информацию", self)
        self.button.setGeometry(150, 60, 200, 30)
        self.button.clicked.connect(self.show_post_info)

        self.info_text = QTextEdit(self)
        self.info_text.setGeometry(20, 100, 330, 250)
        self.info_text.setReadOnly(True)

    def get_post_by_id(self, post_id):
        url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
        response = requests.get(url)
        if response.status_code == 200:
            post_data = response.json()
            return post_data
        else:
            QMessageBox.critical(self, "Ошибка", f"Не удалось получить данные для поста с id {post_id}.")
            return None

    def save_post_to_file(self, post_id, post_data):
        folder_name = "saved_posts"
        os.makedirs(folder_name, exist_ok=True)
        file_path = os.path.join(folder_name, f"post_{post_id}.json")
        with open(file_path, "w") as file:
            file.write(str(post_data))

    def show_post_info(self):
        post_id = self.entry.text()
        post_data = self.get_post_by_id(post_id)
        if post_data:
            self.info_text.clear()
            self.info_text.append(f"ID: {post_data['id']}\n")
            self.info_text.append(f"Пользователь ID: {post_data['userId']}\n")
            self.info_text.append(f"Заголовок: {post_data['title']}\n")
            self.info_text.append(f"Текст: {post_data['body']}")
            self.save_post_to_file(post_id, post_data)

def main():
    app = QApplication([])
    window = PostViewerApp()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()