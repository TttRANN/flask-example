import json
import time
from flask import Flask,request,jsonify
from flask_cors import CORS
import select_mysql
import insert_mysql
import pymysql
import mysql_connect
from datetime import datetime

api = Flask(__name__)
CORS(api)

@api.route('/api/user/login',methods=['POST'])
def user_select():
    user_info = request.get_data()
    data = json.loads(user_info)
    print(data)
    userAccount = data["userAccount"]
    userPassword = data['userPassword']
    # print(userAccount,userPassword)
    result = select_mysql.select_user(userAccount,userPassword)
    if result is not None:
        res,id,res_data = result
        gender = res_data[0]['gender']
        userName = res_data[0]['userName']
        email =  res_data[0]['email']
        phoneNumber = res_data[0]['phoneNumber']
        address = res_data[0]['address']
        idCardNumber = res_data[0]['idCardNumber']
        postalCode = res_data[0]['postalCode']
        print(gender,userName,email,phoneNumber,address,idCardNumber)
        #print(res)
        #if res == 0:
        response_data = {
            'code': 0,
            'message': '登录成功',
            'user_id': f'{id}',  # 替换为实际用户ID
            'userAccount': f'{userAccount}',  # 替换为实际用户名
            'gender': f'{gender}',
            'userName': f'{userName}',
            'email': f'{email}',
            'phoneNumber': f'{phoneNumber}',
            'address': f'{address}',
            'idCardNumber': f'{idCardNumber}',
            'postalCode': f'{postalCode}'
        }
        print(response_data)
        return response_data
    else:
        response_data = {
            'code': 1,
            'message': '登录失败',
            'user_id': 'NULL',  # 替换为实际用户ID
            'userAccount': f'{userAccount}'  # 替换为实际用户名
        }
        print(response_data)
        return response_data

@api.route('/api/user/register',methods=['POST'])
def user_register():
    user_info = request.get_data()
    data = json.loads(user_info)
    user_account = data['userAccount']
    user_password = data['userPassword']
    res = insert_mysql.insert_user(user_account,user_password)

    if res == 0:
        response_data = {
            'code': 0,
            'message': '注册成功',
        }
        return response_data
    else:
        response_data = {
            'code': 1,
            'message': '注册失败',
        }
        return response_data
