# Store-Manager-API

An app to manage store operations

[![Build Status](https://travis-ci.org/KMaina/Store-Manager-API.svg?branch=develop)](https://travis-ci.org/KMaina/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/KMaina/Store-Manager-API/badge.svg)](https://coveralls.io/github/KMaina/Store-Manager-API)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c279fc6f6b9340248a8cba7bb8096841)](https://www.codacy.com/app/KMaina/Store-Manager-API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KMaina/Store-Manager-API&amp;utm_campaign=Badge_Grade)

## Installation

- clone the repo locally in a terminal using `git clone https://github.com/KMaina/Store-Manager-API.git`
- cd into the `Store-Manager-API folder`
- Create a virtual environmnet using the command `virtualenv -p python3 venv`
- On Linux and OS X activate using
```
source venv/bin/activate
```
- On windows activate using 
```
cd venv\Script\activate
```
- Set the following environment variables on Linux and OS X using
```
export FLASK_APP=run.py
export FLASK_ENV=development
export SECRET_KEY=verysecret #change-this!
```
- Set the following environment variables on Windows using
```
set FLASK_APP=run.py
set FLASK_ENV=development
set SECRET_KEY=verysecret #change-this!
```
- Install all dependencies by running `pip install -r requirements.txt` while at the root of the directory
- For unit tests and coverage run the command `coverage run --source=app -m pytest && coverage report`
- Once done, deactivate the virtual environment by running `deactivate` in the terminal


## Example Usage
- In Postman, add the address `127.0.0.1:5000/api/v1/auth/login` to the `POST` method
- Add the JSON body to login into the app
```
{
  "name":"admin",
  "password":"passadmin"
}
```
- In Postman, add the address `127.0.0.1:5000/api/v1/auth/signup` to the `POST` method
- Add a JSON body to register into the app and grab the token from the login.
```
{
  "name":"Ken Maina",
  "password":"mysecret",
  "confirm":"mysecret"
}
```
- To add a product, add `127.0.0.1:5000/api/v1/products` to the `POST` method
- Use the following JSON body
```
{
  "name":"eggs",
  "quantity":50,
  "price":20,
  "reorder":10
}
```
- To edit a product, add `127.0.0.1:5000/api/v1/products/<int:productId>` to the `PUT` method
```
{
  "name":"eggs",
  "quantity":50,
  "price":20,
  "reorder":10
}
```
- To delete a product, add `127.0.0.1:5000/api/v1/products/<int:productId>` to the `DELETE` method
- To create a product, add `127.0.0.1:5000/api/v1/sales` to the `POST` method
- Use the following JSON body
```
{
  "name":"eggs",
  "quantity":50
}
```
## Release History
* Version 2 - Store Manager API with database persistence using POSTGREsql
* Version 1 - Store Manager API with memory persistence
## Meta
Ken Maina - maina.ken0@gmail.com
https://github.com/KMaina

## Contributing

1. Fork it (https://github.com/Kmaina/Store-Manager-API/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request
