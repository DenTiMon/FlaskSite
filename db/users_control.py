class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

# Добавление нового пользователя
    def add_user(self, email, login, password):
        try:
            self.__cur.execute(
                f"""SELECT COUNT(*) FROM users WHERE email LIKE '{email}';"""
            )
            res = self.__cur.fetchone()
            if res[0] > 0:
                print('Пользоватеть с таким email уже существует')
                return False

            self.__cur.execute(
                f"""INSERT INTO users (email, user_name, password) VALUES
                ('{email}', '{login}', '{password}');"""
                )
            self.__db.commit()

        except Exception as ex:
            print('Ошибка при добавлении пользователя')
            return False

        return True
