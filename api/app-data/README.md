# API Document

url => "/"

"Hello chatbot API!"
___

### Sign up user
url => "/signup"
~~~json
{
    "userName": "user",
    "email": "user@example.com",
    "password": "securepassword"
}
~~~

___

### Login
url => "/login"
~~~json
{
    "email": "user@example.com",
    "password": "securepassword"
}
~~~