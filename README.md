# User_Auth
Fastapi Big Application

## App Configuration 
For this Appliction you should required to check python --version greater than 3.6
Then create vertual environment for this app with run this commond python3 or python -m venv env or xyz
after create virtual env run this commond pip install -r requirements.txt
required library now process to install and after installation create .env file with given following value

EMAIL = xyz@gmail.com
PASS = xyz123@
EMAIL_FROM = xyz@gmail.com
ALGO = "HS256"

## Run Application 
if you set all value in .env file then after you run commond uvicorn main:app --reload 
else comment the line of code (23 - 33), (52 - 89) and 93, which present in user.py file 
