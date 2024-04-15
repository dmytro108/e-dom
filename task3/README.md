## Завдання 3
1. Створити docker-compose файл який би підняв веб сервер на php. Він складатиметься з двух images: nginx та php-fpm. Налаштувати його так, щоб була можливість вести розробку цього веб серверу локально.
2. Створити docker-compose для цього ж серверу для прод оточення. І описати флоу як буде вестись розробка і ci/cd процес для цього серверу.  

## Рішення
### Розробка
Типовим рішенням для локальної розробки буде підключення робочого каталогу розробника як тому контейнера, а також мапінг портів стандартних сервісів контейнера на довільні порти локальної станції.
```yaml
version: "3.8"

services:
  php-fpm:
    image: php:8.0-fpm
    volumes:
      - ./src:/var/www/html:rw
    networks:
      - app-network

  nginx:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./src:/var/www/html:ro
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - php-fpm
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```
### Прод
Для прод середовища я пропоную додати ще один контейнер у конфігурацію, який буде легким образом, який міститиме тільки файли веб-застосунку - статичні сторінки, стилі, мультимедіа та php-шаблони. Цей контейнер розділятиме свій каталог із додатком між усіма контейнерами. Таким чином будуть дотримані основні принципи поділу робочого і допоміжного коду, а також дасть нам змогу мінімізувати час простою під час оновлення.
Також буде відокремлено файли конфігурації від коду програми.
Для забезпечення стабільності роботи буде проводитися автоматична перевірка роботоздатності контейнерів. У разі негативного результату - автоматичне перевантаження контейнера. Також вказуються обмеження щодо використання ресурсів, які можуть бути змінені з часом.

Оскільки не задано додаткових умов для прод середовища, то вважатимемо, що бойовий сервер безпосередньо під'єднаний до Інтернету, без балансувальника або зворотного проксі.

```yaml
name: task3-prod

services:
# ************************** Web app
  web-app:
    image: myregistry.com/myapp:1.0.1 
    container_name: src
    volumes:
      - web_root:/var/www/html

# ************************** PHP-FPM service
  php-fpm:
    image: php-fpm:latest
    container_name: php_fpm
    # Volumes
    volumes:
      - web_root:/var/www/html    
    # Resource limits
    cpus: "1.0"
    mem_limit: "256M"
    shm_size: "256M"
    # Healtcheck and restart policy
    healthcheck:
      test: ["CMD", "SCRIPT_NAME=/ping", "SCRIPT_FILENAME=/ping", 
            "REQUEST_METHOD=GET", "cgi-fcgi", "-bind", "-connect", 
            "127.0.0.1:9000"]
      interval: 1m30s
      timeout: 30s
      retries: 5
      start_period: 30s
    restart: on-failure

    depends_on:
      - web-app
    networks:
      - app-network

# ************************ Nginx server
  nginx:
    image: nginx:latest
    container_name: nginx
    networks:
      - app-network
    # Volumes
    volumes:
      - web_root:/var/www/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf    
    # Resource limits
    cpus: "0.5"
    mem_limit: "256M"
    shm_size: "256M"

    # Healtcheck and restart policy 
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/ping.php"]
      interval: 1m30s
      timeout: 30s
      retries: 5
      start_period: 30s
    restart: on-failure

    depends_on:
      - web-app
      - php-fpm

# ************************** Network 
networks:
  app-network:
    driver: bridge

# *************************** Volumes
volumes:
  web_root:    
```

### CI/CD workflow
Для прод оточення розглянемо процес Continious Deployment, оскільки процеси Continious Integration / Delivery у цьому випадку не такі важливі. Пайплайни Continious Integration / Delivery можуть варіюватися. Головне, що в разі успішного проходження CI/CD пайплайну ми отримуємо артефакт у вигляді релізнї версій образа контейнера, який містить код застосунку.

Припустимо, у нас є успішно зібраний образ контейнера з релізом застосунку у нашому реєстрі. Після ухвалення рішення про розгортання нової версії на прод запускається паплайн, який:
- оновлює номер весії образа контейнера з застосунком у docker-compose файлі
- оновлює docker-compose файл на прод
- завантажує нову версію образа застосунку
- перевантажує тільки контейнер із кодом застосунку

#### Downtime
Цей процес оновлення передбачає мінімальний час простою прод сервераб тільки на час перевантаження контейнера з кодом застосунка. Для того, щоб уникнути і цього, необхідно використовувати засоби оркестрації контейнерів, такі як Kubernetes або Docker Swarm.

#### Файли конфігурації
Файли конфігурації, наприклад, сервера Nginx, також мають бути відокремлені від коду застосунку. Найімовірніше, немає потреби їх змінювати під час кожного оновлення, тому зміна цих файлів не входить у паплайн оновлення застосунку. 
Файли конфігурації можуть генеруватися окремими пайплайнами або скриптами і підключатися як окремі томи.