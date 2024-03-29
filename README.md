# Моделі:
**Бокси:** 
  - ід боксу
  - назва боксу 
  - опис боксу 
  - сума 
  - спроби(кількість відкриттів)
  - (DELETED!) тип розподілу(рандом або рівномірно) - **поле прибрано, так як в даній реалізації нема вибору розподілу при відкритті боксу**
  - сума поточна 
  - спроби поточні
  - (NEW!) Ціна спроби - **поле додано для списання монет з балансу юзера при покупці боксу**
  - (NEW!) Ід монети  - **поле додано для ідентифікації монети, за яку можна купити бокс**
  - статус (активно, не активно)
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Юзер:**
  - (DELETED!) ід юзера в тг - **поле прибрано, так як в тз немає імплементації з Telegram**
  - Ід юзера
  - (DELETED!) юзернейм тг - **поле прибрано, так як в тз немає імплементації з Telegram**
  - юзернейм
  - ім’я
  - номер телефону 
  - пошта
  - мова 
  - країна
  - (DELETED!) код верифікації - **поле прибрано, так як зберігання коду верифікації в БД може бути недоцільним, тому що код постійно має змінюватися**
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Юзер бокси:**
  - ід
  - ід юзера 
  - бокс(id) 
  - (DELETED!) Статус - **поле прибрано для зменшення payload, так як в моделі є бокс_ід**
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Операції:**
  - ід (номер операції)
  - ід юзера
  - сума
  - час виконання 
  - (DELETED!) спосіб(назва боксу) - **поле прибрано для зменшення payload, так як в моделі є бокс_ід**
  - ід боксу 
  - статус(зарахування чи списання)
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Юзер баланс:**
  - юзер ід 
  - ід монети
  - баланс
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Монети:**
  - ід 
  - назва 
  - (DELETED!) курс - **поле прибрано, тому що для даної реалізації нема можливості конвертації монет**
  - (DELETED!) Кількість - **поле прибрано, тому що для даної реалізації нема можливості поповнення рахунку юзером**
  - статус
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Сповіщення (новини):** 
  - ід 
  - (NEW!) дія - **поле додано для короткого опису тексту сповіщення, наприклад 'close_box'**
  - текст 
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

**Сповіщення юзера** 
  - юзер ід 
  - ід сповіщення - **додано код з select_related для того, щоб у payload було не лише ід сповіщення, а і дія сповіщення**
  - (NEW!) дата та час створення -  **поле додано для відстеження часу створення запису**

# Ідеї для додаткової реалізації 
  - Конвертація монет
  - Види випадкового вибору нагороди при відкритті боксів
  - Поповнення рахунку юзерів
  - Реєстрація та логін юзерів

# Інформація щодо реалізації:
  - У папці box_app/fixtures є файл sample_data.json, там знаходиться тестова дата, а саме:
    - Адмін (логін: admin пароль: 12345)
    - 2 Юзери
    - 2 Бокси (один можна купити за монету №1, а інший за монету №2)
    - 2 Монети
    - 2 Юзер Баланси (Юзер №1 має 100 монет №1, Юзер №2 має 200 монет №2)
    - 1 Сповіщення (при закритті боксу, який відкривав юзер)
   
# Посилання на проєкт

Проєкт був задеплоєн на Digital Ocean, тестова дата завантажена

Django Admin - https://box-app-zvnr3.ondigitalocean.app/admin/

Swagger - https://box-app-zvnr3.ondigitalocean.app/swagger/

 
 # Розгортання проєкту локально
   1. Завантажити та запустити [Docker](https://www.docker.com/).
   2. Завантажити репозиторій
   3. Відкрити папку з репозиторієм
   4. Створити .env файл (за приклад можна взяти .env.example файл)
   5. Запустити команду
      ```python
      docker-compose up -d --build
      ```
   6. Потім запустити команди
      
      ``` python
      docker-compose exec web python manage.py makemigrations
      ```

      ```python
      docker-compose exec web python manage.py migrate
      ```
      
  7. Завантажити файл з тестовими даними можна командою
     ```python
     docker-compose exec web python manage.py loaddate sample_data.json
     ```
