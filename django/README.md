## Запуск в кластере Kubernetes
#### Все манифесты по управлению приложениями в моём кластере Kubernetes хранятся в отдельном приватном репозитории

### Postgres
В папке w24ok/postgres с манифестами .yml по развёртыванию

1. В 03_postgres_pv.yml изменить local.path для сохранения БД в Persistent Volume
2. Там же в  03_postgres_pv.yml изменить nodeAffinity
3. Заполнить и применить secret.yml
4. Применить все манифесты попорядку

### Django
В папке w24ok/django с манифестами .yml по развёртыванию

1. Применить все манифесты
2. После создания контейнера - зайти в него и применить все миграции __python manage.py migration__
3. __python3 django/manage.py createsuperuser__ для создания суперпользователя django
4. Зайти на __w24ok/admin__
5. Создать пользователя w24ok-Reports 
6. Создать пользователя ArthurAdmin
7.  В Permissions создать:
   ### Для просмотра данных YP, ZH1, ZH2
   1. Name __view YP__
   2. Content type __main | warehouse__
   3. Codename __can_view_warh_YP__
   4. ...
   ### Для добавления данных
   5. Name __upload YP__
   6. Content type __main | warehouse__
   7. Codename __can_upload_warh_YP__
   8. ...
8.  В Group создать
   1.  Name Upload
   2.  Name View All
9.  Добавить Пользователя w24ok-Reports в Group Upload
10. Добавить пользователя ArthurAdmin в Group View All
11. Добавить склады __YP, ZH1, ZH2__
