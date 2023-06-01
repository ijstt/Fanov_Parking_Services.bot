import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def set_time_sub(self, user_id, time):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time, user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def get_balance(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                balance = int(row[0])
            return balance

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = str(row[0])
            return time_sub

    def book_parking(self, user_id):
        with self.connection:
            how_match = self.cursor.execute("SELECT `balance` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in how_match:
                how_match = int(row[0])
            if how_match < 150:
                return "Мало денег"
            else:
                balance = how_match - 150
                return self.cursor.execute("UPDATE `users` SET `balance` = ? WHERE `user_id` = ?", (balance, user_id,))

