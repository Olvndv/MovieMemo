import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QFormLayout, QInputDialog, QFileDialog, QDialog, QDialogButtonBox, QScrollArea, QGridLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os

class CustomMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("color: white; background-color: maroon;")

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Login Page")
        self.resize(800, 700)
        
        layout = QVBoxLayout()

        self.image_label = QLabel(self)
        pixmap = QPixmap('LOGOSDA.png')
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        
        self.username_label = QLabel("Username:")
        self.username_label.setStyleSheet("color: white;")
        self.username_entry = QLineEdit()
        self.username_entry.setStyleSheet("color: white;")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)

        self.password_label = QLabel("Password:")
        self.password_label.setStyleSheet("color: white;")
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("color: white;")
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        self.login_button.setStyleSheet("color: white;")
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.setStyleSheet("background-color: maroon;")

        self.admin_page = None

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if username == "admin" and password == "admin":
            success_message = CustomMessageBox()
            QMessageBox.information(success_message, "Login Successful", "Admin login successful!")
            self.admin_page = AdminPage()
            self.admin_page.show()
            self.close()
        elif username == "user" and password == "user":
            success_message = CustomMessageBox()
            QMessageBox.information(success_message, "Login Successful", "User login successful!")
        else:
            error_message = CustomMessageBox()
            QMessageBox.warning(error_message, "Login Failed", "Invalid username or password.")

class AdminPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Admin Page")
        self.resize(800, 800)
        
        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.title_label = QLabel("Title:")
        self.title_label.setStyleSheet("color: white;")
        self.title_entry = QLineEdit()
        self.title_entry.setStyleSheet("color: white;")
        form_layout.addRow(self.title_label, self.title_entry)

        self.year_label = QLabel("Year:")
        self.year_label.setStyleSheet("color: white;")
        self.year_entry = QLineEdit()
        self.year_entry.setStyleSheet("color: white;")
        form_layout.addRow(self.year_label, self.year_entry)

        self.rating_label = QLabel("Rating:")
        self.rating_label.setStyleSheet("color: white;")
        self.rating_entry = QLineEdit()
        self.rating_entry.setStyleSheet("color: white;")
        form_layout.addRow(self.rating_label, self.rating_entry)

        self.genre_label = QLabel("Genre:")
        self.genre_label.setStyleSheet("color: white;")
        self.genre_entry = QLineEdit()
        self.genre_entry.setStyleSheet("color: white;")
        form_layout.addRow(self.genre_label, self.genre_entry)

        self.synopsis_label = QLabel("Synopsis:")
        self.synopsis_label.setStyleSheet("color: white;")
        self.synopsis_entry = QTextEdit()
        self.synopsis_entry.setStyleSheet("color: white;")
        self.synopsis_entry.setFixedHeight(100)
        form_layout.addRow(self.synopsis_label, self.synopsis_entry)

        self.image_label = QLabel("Image:")
        self.image_label.setStyleSheet("color: white;")
        self.image_entry = QLineEdit()
        self.image_entry.setReadOnly(True)
        self.image_entry.setStyleSheet("color: white;")
        self.image_button = QPushButton("Select Image")
        self.image_button.clicked.connect(self.select_image)
        self.image_button.setStyleSheet("color: white;")
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_entry)
        image_layout.addWidget(self.image_button)
        form_layout.addRow(self.image_label, image_layout)

        layout.addLayout(form_layout)

        self.movie_list_layout = QGridLayout()
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area_widget.setLayout(self.movie_list_layout)
        layout.addWidget(scroll_area)

        self.search_label = QLabel("Search Movie:")
        self.search_label.setStyleSheet("color: white;")
        self.search_entry = QLineEdit()
        self.search_entry.setStyleSheet("color: white;")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_movie)
        self.search_button.setStyleSheet("color: white;")
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_entry)
        search_layout.addWidget(self.search_button)
        layout.addWidget(self.search_label)
        layout.addLayout(search_layout)

        button_layout = QHBoxLayout()

        self.add_movie_button = QPushButton("Add Movie")
        self.add_movie_button.clicked.connect(self.add_movie)
        self.add_movie_button.setStyleSheet("color: white;")
        button_layout.addWidget(self.add_movie_button)

        self.delete_movie_button = QPushButton("Delete Movie")
        self.delete_movie_button.clicked.connect(self.delete_movie)
        self.delete_movie_button.setStyleSheet("color: white;")
        button_layout.addWidget(self.delete_movie_button)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Sort by", "Title", "Year", "Rating", "Genre"])
        self.sort_combo.currentIndexChanged.connect(self.sort_movies)
        self.sort_combo.setStyleSheet("color: white;")
        button_layout.addWidget(self.sort_combo)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.setStyleSheet("background-color: maroon;")

        self.movies = []
        self.load_movies()
        self.display_movies()

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.image_entry.setText(file_path)

    def add_movie(self):
        title = self.title_entry.text()
        year = self.year_entry.text()
        rating = self.rating_entry.text()
        genre = self.genre_entry.text()
        synopsis = self.synopsis_entry.toPlainText()
        image_path = self.image_entry.text()

        if title and year and rating and genre and image_path:
            movie_info = {
                "title": title,
                "year": year,
                "rating": rating,
                "genre": genre,
                "synopsis": synopsis,
                "image_path": image_path
            }
            self.movies.append(movie_info)
            self.save_movies()
            self.display_movies()
        else:
            QMessageBox.warning(self, "Incomplete Information", "Please fill in all fields.")

    def delete_movie(self):
        input_dialog = QInputDialog(self)
        input_dialog.setWindowTitle("Delete Movie")
        input_dialog.setLabelText("Enter the title of the movie to delete:")
        input_dialog.setStyleSheet("QLabel { color: white; } QPushButton { color: white; } QLineEdit { color: white; } QDialogButtonBox { color: white; } background-color: maroon;")
        
        if input_dialog.exec_() == QDialog.Accepted:
            title_to_delete = input_dialog.textValue().strip()

            if title_to_delete:
                deleted = False
                for movie_info in self.movies:
                    if movie_info["title"].lower() == title_to_delete.lower():
                        self.movies.remove(movie_info)
                        deleted = True
                        break

                message_box = CustomMessageBox()
                if deleted:
                    self.save_movies()
                    message_box.setIcon(QMessageBox.Information)
                    message_box.setWindowTitle("Success")
                    message_box.setText(f"Movie '{title_to_delete}' deleted successfully.")
                    self.display_movies()
                else:
                    message_box.setIcon(QMessageBox.Warning)
                    message_box.setWindowTitle("Not Found")
                    message_box.setText(f"Movie '{title_to_delete}' not found.")
                message_box.exec_()
        else:
            message_box = CustomMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setWindowTitle("No Input")
            message_box.setText("No title entered.")
            message_box.exec_()

    def display_movies(self):
        for i in reversed(range(self.movie_list_layout.count())):
            widget = self.movie_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        row = col = 0
        for movie_info in self.movies:
            movie_layout = QVBoxLayout()

            image_button = QPushButton()
            pixmap = QPixmap(movie_info['image_path'])
            image_button.setIcon(QIcon(pixmap))
            image_button.setIconSize(pixmap.size())
            image_button.clicked.connect(lambda checked, movie=movie_info: self.show_movie_details(movie))

            title_label = QLabel(f"Title: {movie_info['title']}")
            title_label.setStyleSheet("color: white;")
            title_label.setAlignment(Qt.AlignCenter)

            rating_label = QLabel(f"Rating: {movie_info['rating']}")
            rating_label.setStyleSheet("color: white;")
            rating_label.setAlignment(Qt.AlignCenter)

            genre_label = QLabel(f"Genre: {movie_info['genre']}")
            genre_label.setStyleSheet("color: white;")
            genre_label.setAlignment(Qt.AlignCenter)

            year_label = QLabel(f"Year: {movie_info['year']}")
            year_label.setStyleSheet("color: white;")
            year_label.setAlignment(Qt.AlignCenter)

            movie_layout.addWidget(image_button)
            movie_layout.addWidget(title_label)
            movie_layout.addWidget(rating_label)
            movie_layout.addWidget(genre_label)
            movie_layout.addWidget(year_label)

            movie_widget = QWidget()
            movie_widget.setLayout(movie_layout)

            self.movie_list_layout.addWidget(movie_widget, row, col)

            col += 1
            if col == 3:
                col = 0
                row += 1

    def show_synopsis_and_image(self, synopsis, image_path):
        dialog = QDialog(self)
        dialog.setWindowTitle("Movie Details")
        dialog.setFixedSize(500, 550)

        layout = QVBoxLayout()
        
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap.scaled(250, 375, Qt.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        synopsis_label = QLabel(synopsis)
        synopsis_label.setWordWrap(True)
        synopsis_label.setStyleSheet("color: white;")
        layout.addWidget(synopsis_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: maroon; color: white;")
        dialog.exec_()

    def show_movie_details(self, movie):
        dialog = QDialog(self)
        dialog.setWindowTitle("Movie Details")
        dialog.setFixedSize(500, 700)

        layout = QVBoxLayout()
        
        image_label = QLabel()
        pixmap = QPixmap(movie['image_path'])
        image_label.setPixmap(pixmap.scaled(250, 375, Qt.KeepAspectRatio))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        form_layout = QFormLayout()
        form_layout.setSpacing(10) 

        title_label = QLabel(f"{movie['title']}")
        title_label.setStyleSheet("color: white;")
        form_layout.addRow("Title:", title_label)

        rating_label = QLabel(f"{movie['rating']}")
        rating_label.setStyleSheet("color: white;")
        form_layout.addRow("Rating:", rating_label)

        genre_label = QLabel(f"{movie['genre']}")
        genre_label.setStyleSheet("color: white;")
        form_layout.addRow("Genre:", genre_label)

        year_label = QLabel(f"{movie['year']}")
        year_label.setStyleSheet("color: white;")
        form_layout.addRow("Year:", year_label)

        synopsis_label = QLabel(movie['synopsis'])
        synopsis_label.setWordWrap(True)
        synopsis_label.setStyleSheet("color: white;")
        form_layout.addRow("Synopsis:", synopsis_label)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        button_box.setStyleSheet("color: white;") 
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: maroon; color: white;") 
        dialog.exec_()

    def sort_movies(self):
        sort_option = self.sort_combo.currentText()
        if sort_option == "Title":
            self.movies.sort(key=lambda x: x["title"])
        elif sort_option == "Year":
            self.movies.sort(key=lambda x: int(x["year"]))
        elif sort_option == "Rating":
            self.movies.sort(key=lambda x: float(x["rating"]), reverse=True)
        elif sort_option == "Genre":
            self.movies.sort(key=lambda x: x["genre"])
        self.display_movies()

    def load_movies(self):
        if os.path.exists("movies.txt"):
            with open("movies.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(";")
                    if len(parts) == 6:
                        movie_info = {
                            "title": parts[0],
                            "year": parts[1],
                            "rating": parts[2],
                            "genre": parts[3],
                            "synopsis": parts[4],
                            "image_path": parts[5]
                        }
                        self.movies.append(movie_info)

    def save_movies(self):
        with open("movies.txt", "w") as file:
            for movie in self.movies:
                line = f"{movie['title']};{movie['year']};{movie['rating']};{movie['genre']};{movie['synopsis']};{movie['image_path']}\n"
                file.write(line)

    def search_movie(self):
        search_text = self.search_entry.text().strip().lower()
        if not search_text:
            self.load_movies()
            self.display_movies()
            return

        matching_movies = [movie for movie in self.movies if search_text in movie['title'].lower()]
        if matching_movies:
            self.show_movie_details(matching_movies[0])
        else:
            QMessageBox.warning(self, "No Match", "No movies found matching the search criteria.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
