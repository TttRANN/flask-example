# -*- coding: utf-8 -*-
"""
-------------------------------
@Project :Python_Flask  
@File    :User_login.py
@IDE     :PyCharm
@Author  :YZ
@Date    :2024/1/6 21:30
-------------------------------
"""
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


@api.route('/')
def index():
    return 'Welcome to my Flask app!'
    
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

@api.route('/api/post/add', methods=['POST'])
def add_task():
    data = request.get_data()
    data = json.loads(data)
    title = data.get('title')
    #print(title)
    content = data.get('content')
    #print(content)
    user_id = int(data.get('userId'))
    #print(title,content,user_id)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        sql = "INSERT INTO post (title, content, userId, createTime) VALUES (%s, %s, %s, %s)"
        mysql_connect.execute_sql(sql, (title, content, user_id, current_time))
        return jsonify({"code": 0, "message": "添加任务成功"})
    except Exception as e:
        print(e)
        return jsonify({"code": 1, "message": str(e)})

# 删除任务接口
@api.route('/api/post/delete', methods=['POST'])
def delete_task():
    data = request.get_json()
    post_id = data.get('id')

    try:
        sql = "DELETE FROM post WHERE id = %s"
        mysql_connect.execute_sql(sql, (post_id,))
        return jsonify({"code": 0, "message": "删除任务成功"})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})

@api.route('/api/post/update', methods=['POST'])
def update_task():
    data = request.get_json()
    post_id = data.get('id')
    title = data.get('title')
    content = data.get('content')

    try:
        sql = "UPDATE post SET title = %s, content = %s WHERE id = %s"
        mysql_connect.execute_sql(sql, (title, content, post_id))
        return jsonify({"code": 0, "message": "修改任务成功"})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})

@api.route('/api/post/getByUserId', methods=['POST'])
def get_tasks_by_user_id():
    data = request.get_data()
    data = json.loads(data)
    user_id = data.get('userId')
    print(user_id)
    try:
        sql = "SELECT * FROM post WHERE userId = %s"

        posts = mysql_connect.execute_sql(sql, (user_id,))
        #print(posts)
        tasks_list = []
        for task in posts:
            task_dict = {
                "id": task[0],
                "title": task[6],
                "user_id": task[2],
                "createTime": task[3].strftime('%Y-%m-%d %H:%M:%S'),
                "updateTime": task[4].strftime('%Y-%m-%d %H:%M:%S'),
                "status": task[5],
                "content": task[1]
            }
            tasks_list.append(task_dict)

        return jsonify({"code": 0, "data": tasks_list})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})

@api.route('/api/daydata/getByUserId', methods=['POST'])
def get_daydata_by_user_id():
    data = request.get_json()
    user_id = data.get('userId')
    try:
        sql = "SELECT * FROM daydata WHERE userId = %s"
        posts = mysql_connect.execute_sql(sql, (user_id,))
        #print(posts)
        tasks_list = []
        for task in posts:
            task_dict = {
                "id": task[0],
                "title": task[6],
                "user_id": task[2],
                "createTime": task[3].strftime('%Y-%m-%d %H:%M:%S'),
                "updateTime": task[4].strftime('%Y-%m-%d %H:%M:%S'),
                "status": task[5],
                "content": task[1]
            }
            tasks_list.append(task_dict)
        return jsonify({"code": 0, "data": tasks_list})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})

# 添加记录接口
@api.route('/api/daydata/add', methods=['POST'])
def add_daydata():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('userId')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        sql = "INSERT INTO daydata (title, content, userId, createTime) VALUES (%s, %s, %s, %s)"
        mysql_connect.execute_sql(sql, (title, content, user_id, current_time))
        return jsonify({"code": 0, "message": "添加记录成功"})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})

# 删除记录接口
@api.route('/api/daydata/delete', methods=['POST'])
def delete_daydata():
    data = request.get_json()
    daydata_id = data.get('id')

    try:
        sql = "DELETE FROM daydata WHERE id = %s"
        mysql_connect.execute_sql(sql, (daydata_id,))
        return jsonify({"code": 0, "message": "删除记录成功"})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})

# 修改记录接口
@api.route('/api/daydata/update', methods=['POST'])
def update_daydata():
    data = request.get_json()
    daydata_id = data.get('id')
    title = data.get('title')
    content = data.get('content')

    try:
        sql = "UPDATE daydata SET title = %s, content = %s WHERE id = %s"
        mysql_connect.execute_sql(sql, (title, content, daydata_id))
        return jsonify({"code": 0, "message": "修改记录成功"})
    except Exception as e:
        return jsonify({"code": 1, "message": str(e)})


@api.route('/api/user/update', methods=['POST'])
def update_user():
    try:
        # 获取请求中的用户信息
        data = request.get_json()
        print(data)
        # 更新用户信息的 SQL 语句
        sql = "UPDATE user SET address=%s, email=%s, gender=%s, idCardNumber=%s, phoneNumber=%s,postalCode=%s, userName=%s WHERE id=%s"

        # 执行 SQL 语句
        mysql_connect.execute_sql(sql, (
            data['address'],
            data['email'],
            data['gender'],
            data['idCardNumber'],
            data['phoneNumber'],
            data['postalCode'],
            data['userName'],
            data['id']
        ))

        # 返回成功响应
        return jsonify({'code': 0, 'message': '更新成功','data':data})
    except Exception as e:
        return jsonify({'code': 1, 'message': f'更新失败: {str(e)}'})


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=8080, debug=True)