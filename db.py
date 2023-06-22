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

    def get_name_park(self, callback):
        with self.connection:
            result = self.cursor.execute("SELECT `name` FROM `lipetsk` WHERE `callback` = ?", (callback,)).fetchall()
            for row in result:
                name_park = str(row[0])
            return name_park

    def get_lat(self, callback):
        with self.connection:
            result = self.cursor.execute("SELECT `lat` FROM `lipetsk` WHERE `callback` = ?", (callback,)).fetchall()
            for row in result:
                lat = str(row[0])
            return float(lat)

    def get_lon(self, callback):
        with self.connection:
            result = self.cursor.execute("SELECT `lon` FROM `lipetsk` WHERE `callback` = ?", (callback,)).fetchall()
            for row in result:
                lon = str(row[0])
            return float(lon)

    def get_mest(self, callback):
        with self.connection:
            result = self.cursor.execute("SELECT `mest` FROM `lipetsk` WHERE `callback` = ?", (callback,)).fetchall()
            for row in result:
                mest = str(row[0])
            return mest

    def get_sv_mest(self, callback):
        with self.connection:
            result = self.cursor.execute("SELECT `sv_mest` FROM `lipetsk` WHERE `callback` = ?", (callback,)).fetchall()
            for row in result:
                mest = str(row[0])
            return mest

    def set_car_number(self, user_id, car_number):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `car_number` = ? WHERE `user_id` = ?",
                                       (car_number, user_id,))

    def set_date_booking(self, user_id, time):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `date_booking` = ? WHERE `user_id` = ?",
                                       (time, user_id,))

    def set_sv_mest(self, callback, mode=2):
        with self.connection:
            sv = self.get_sv_mest(callback)
            if mode == 0:
                sv = int(self.get_sv_mest(callback)) - 1
            elif mode == 1:
                sv = int(self.get_sv_mest(callback)) + 1
            return self.cursor.execute("UPDATE `lipetsk` SET `sv_mest` = ? WHERE `callback` = ?",
                                       (sv, callback,))

    def set_name_city(self, user_id, city):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name_city` = ? WHERE `user_id` = ?", (city, user_id,))

    def set_name_parking(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `name_parking` = ? WHERE `user_id` = ?",
                                       (name, user_id,))

    def get_park(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name_parking` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                park = str(row[0])
            return park

    def get_date_booking(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `date_booking` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                date_booking = str(row[0])
            return date_booking

    def set_last_callback(self, user_id, callback):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `last_callback` = ? WHERE `user_id` = ?",
                                       (callback, user_id,))

    def get_last_callback(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `last_callback` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                callb = str(row[0])
            return callb

    def get_name_sity(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `name_city` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                city = str(row[0])
            return city

    def set_flag_book(self, user_id, flag):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `flag_book` = ? WHERE `user_id` = ?",
                                       (flag, user_id,))

    def get_flag_book(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `flag_book` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                flag = int(row[0])
            return bool(flag)

    def set_last_city(self, user_id, city: str):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `last_city` = ? WHERE `user_id` = ?",
                                       (city, user_id,))

    def get_last_city(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `last_city` FROM `users` WHERE `user_id` = ?",
                                         (user_id,)).fetchall()
            for row in result:
                last_city = str(row[0])
            return last_city
