# Flask Mongo RESTapi Example - with jwt-authentication

### Installation
```sh
$ virtualenv auth
$ cd auth && source bin/active
$ git clone https://github.com/sectasy0/Python-REST
$ pip install -r src/REQUIREMENTS.txt
```

### Configure database
```
Open __init__.py and change 'host' value to your mongo database and db to your database name.
```

### Requests to api
#### Register user
```sh
$ http POST :5000/api/v1.0/auth/register username=testuser password=testuserpassword email=test@email.com
```
#### Login user
```sh
$ http POST :5000/api/v1.0/auth/login username=testuser password=testuserpassword
```
#### Get all users
```sh
$ http GET :5000/api/v1.0/users Autorization:"Bearer <JWT-AccesToken>"
```
#### Get one user
```sh
$ http GET :5000/api/v1.0/users/<userName> Autorization:"Bearer <JWT-AccesToken>"
```
#### Update user
```sh
$ http PUT :5000/api/v1.0/users/<userName> Autorization:"Bearer <JWT-AccesToken>" username=newusername ...
```

#### delete user
```sh
$ http DELETE :5000/api/v1.0/users/<userName> Autorization:"Bearer <JWT-AccesToken>"
```

#### Refresh access-token
```sh
$ http PUT :5000/api/v1.0/users/<userName> Autorization:"Bearer <JWT-RefreshToken>"
```