# API Document

url => "/"

"Hello chatbot API!"
___

### Sign up user
* URL => "/api/signup" 
* Methord = POST
~~~json
{
    "username": "user",
    "email": "user@example.com",
    "password": "securepassword"
}
~~~

___

### Login
* URL => "/api/login"
* Methord = POST
~~~json
{
    "username": "user",
    "password": "securepassword"
}
~~~

___

### Logout
* URL => "/api/logout"
* Methord = GET

___

### Foget Password
* URL => "/api/fogetpassword"
* Methord = POST
~~~json
{
    "email": "user@example.com",
    "password": "securepassword",
    "conform_password": "securepassword"
}
~~~

___

### Serch
* URL => "/api/serch"
* Methord = POST
~~~json

~~~