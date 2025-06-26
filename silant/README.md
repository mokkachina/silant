1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/mokkachina/silant.git
   cd silant/
2. Создайте и активируйте виртуальное окружение:
   py -m venv venv
   venv\Scripts\activate
3. Установите зависимости: pip install -r requirements.txt
4. Настройте базу данных:
   python manage.py makemigrations
   python manage.py migrate
5. Создайте суперпользователя:python manage.py createsuperuser
6. Запустите сервер: python manage.py runserver
   