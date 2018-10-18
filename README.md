# Store-Manager-API

An app to manage store operations

[![Build Status](https://travis-ci.org/KMaina/Store-Manager-API.svg?branch=develop)](https://travis-ci.org/KMaina/Store-Manager-API)
[![Coverage Status](https://coveralls.io/repos/github/KMaina/Store-Manager-API/badge.svg)](https://coveralls.io/github/KMaina/Store-Manager-API)
[![Maintainability](https://api.codeclimate.com/v1/badges/48577eef61885d26403e/maintainability)](https://codeclimate.com/github/KMaina/Store-Manager-API/maintainability)

## Installation

- clone the repo locally in a terminal using `git clone https://github.com/KMaina/Store-Manager-API.git`
- cd into the `Store-Manager-API folder`

## Example Usage
- In Postman, add the address `127.0.0.1:5000/api/v1/auth/signup` to the `POST` method
- Add a JSON body to register into the app
```
{
  "name":"Ken Maina",
  "password":"mysecret",
  "confirm":"mysecret"
}
```
- Hit the send button and get the response `{'msg':"User Successfully created"}`
- To add a product, add `127.0.0.1:5000/api/v1/products` to the `POST` method
use the following JSON body
```
{
  "name":"eggs",
  "quantity":50,
  "price":20,
  "reorder":10
}
```
- Hit the send button and get the response `{'msg':"Product Successfully created"}`
## Development Setup
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

## Meta
Ken Maina - maina.ken0@gmail.com
https://github.com/KMaina

## Contributing

1. Fork it (https://github.com/Kmaina/Store-Manager-API/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request
