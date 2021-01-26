from flask import Flask, request
import psycopg2

app = Flask(__name__)

# creating connection with database
conn = psycopg2.connect('postgres://postgres:helloworld1!@localhost:5432/test')
cursor = conn.cursor()

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.route('/register', methods=['POST'])
def register():
    # first take inputs
    request_json = request.json
    first_name = request_json.get('first_name', None)
    last_name = request_json.get('last_name', None)
    email = request_json.get('email', None)
    password = request_json.get('password', None)
    address = request_json.get('address', None)
    
    # inserting the data into the database
    sql = """
        INSERT INTO users (first_name, last_name, email, password, address)
        VALUES
        ('{first_name}', '{last_name}','{email}','{password}','{address}')
    """.format(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        address=address
    )
    print(sql)
    cursor.execute(sql)
    conn.commit()
    return {
        "success": True,
        "message": "User registered successfully"
    }

@app.route('/login', methods=['POST'])
def login():
    # first take inputs
    request_json = request.json
    email = request_json.get('email', None)
    password = request_json.get('password', None)

    # check if email exists or not
    sql = """
        SELECT * FROM users
        WHERE email = '{email}'
    """.format(email=email)
    print(sql)
    cursor.execute(sql)
    data = cursor.fetchall()
    if len(data) == 0:
        return {
            "success": False,
            "message": "User does not exist"
        }
    else:
        # since this user exits, now check if password is correct
        sql = """
            SELECT * FROM users
            WHERE email = '{email}'
            AND password = '{password}'
        """.format(
            email= email,
            password = password
        )
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 0:
            return {
                "message": "Password Incorrect",
                "success": False
            }
        else:
            return {
                "success": True,
                "message": "Login Successful"
            }

@app.route('/address_search', methods=['POST'])
def address_search():
    # inputs from the user
    request_json = request.json
    address = request_json.get('address', None)

    # write a query
    sql = """
        SELECT id, first_name, last_name, email, address FROM users
        WHERE address = '{address}'
    """.format(address=address)
    print(sql)
    # execute query
    cursor.execute(sql)
    data = cursor.fetchall()

    print(data)
    # final result which be provided to the user
    result = list()
    
    if len(data) == 0:
        return {
            "success": False,
            "message": "There is no data for this address"
        }
    else:
        # there is data
        for item in data:
            user_info = {
                "id": item[0],
                "first_name": item[1],
                "last_name": item[2],
                "email": item[3],
                "address": item[4]
            }
            result.append(user_info)
        return {
            "success": True,
            "data": result
        }

@app.route('/update_address', methods=['POST'])
def update_address():
    # inputs from the user: just id of the user
    request_json = request.json
    id = request_json.get('id', None)
    new_address = request_json.get('new_address', None)

    # write sql for update
    sql = """
        UPDATE users
        SET address = '{new_address}'
        WHERE id = {id}
    """.format(
        id=id,
        new_address=new_address
    )
    print(sql)
    cursor.execute(sql)
    conn.commit()
    return {
        "success": True,
        "message": "Address updated successfully"
    }

@app.route('/delete_user', methods=['POST'])
def delete_user():
    # inputs from the user: just id of the user
    request_json = request.json
    id = request_json.get('id', None)

    # write sql for delete
    sql = """
       delete from users 
        WHERE id = {id}
    """.format(
        id=id,
    )
    print(sql)
    cursor.execute(sql)
    conn.commit()
    return {
        "success": True,
        "message": "user deleted successfully"
    }



if __name__ == '__main__':
    app.run(host='localhost', port=5000)

