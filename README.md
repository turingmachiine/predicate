# predicate

#### Сервер для нашего проекта по поиску логических ошибок, при реализации были использованы следующие технологии:
1. Python
1. Django
1. NLTK
1. Spacy

хост : https://predicate.herokuapp.com/

### Примеры правильных запросов в формате json


POST /auth/register
```json
{
"username" : "buddak",
"first_name": "baddie",
"last_name": "budaev",
"email": "email@gmail.com",
"password": "password",
"confirm": "password"
}
```

POST /auth/login
```json
{
"username" : "buddak",
"password": "password"
}
```

POST /api/sentences
```json
{
"message" : "more than 5 less than 3"
}
```


POST /api/sentences
```json
{
"message" : "more than 5 less than 3",
"author" : 1
}
```


POST /api/mistakes/<id>/decline
```json
{
}
```
