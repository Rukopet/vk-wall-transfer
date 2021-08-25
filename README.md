# vk-wall-transfer

Перенаправляет все посты на стене из ВК в телеграмм, отлавливаются только эвенты стены.

У ВК есть свои приколы с АПИ, Вк не очень любит делиться музыкой и видео, поэтому вытащить этот контент проблематично


#### Демонстрация работы, стена ВК:

<img width="350" alt="Screen Shot 2021-08-25 at 10 46 02 AM" src="https://user-images.githubusercontent.com/69805852/130756652-ca7ac149-d720-4306-8769-7824ed1c5af7.png">


#### Как можно заметить, если эвент - коммент, то происходит простой reply на пост, сохранненый в базе

<img width="350" alt="Screen Shot 2021-08-25 at 10 46 35 AM" src="https://user-images.githubusercontent.com/69805852/130756712-96d33c55-3204-4a16-a012-cd4df0c0b0a9.png">

Для создании нужных таблиц есть отдельный [скрипт](https://github.com/Rukopet/vk-wall-transfer/blob/main/data/create_tables.py)
дефолтный порт 5432
#### Поля базы с постами:

<img width="800" alt="Screen Shot 2021-08-25 at 10 47 13 AM" src="https://user-images.githubusercontent.com/69805852/130756727-3697f904-7218-408f-9d90-032a31705fc1.png">

#### Поля базы с комментами:

<img width="800" alt="Screen Shot 2021-08-25 at 10 47 27 AM" src="https://user-images.githubusercontent.com/69805852/130756746-bb5c919f-2adf-4212-bef6-d2be871326da.png">



