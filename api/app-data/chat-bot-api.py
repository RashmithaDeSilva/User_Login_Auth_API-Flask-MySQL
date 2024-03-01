from flask import Flask, request, redirect, url_for, jsonify, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xyz123'

app.config['MYSQL_HOST'] = '172.18.0.2'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'chatbot'
mysql = MySQL(app)

bcrypt = Bcrypt(app)


@app.before_request
def before_request():
    if request.cookies.get('session') is None and request.endpoint not in ['index', 'login', 'signup']:
        return jsonify({"auth": False, "status": False, "msg": "Unauthorized access"}), 401
    
    elif request.cookies.get('session') is not None and request.endpoint not in ['index', 'login', 'signup']:
        if session.get('auth') != 'True' or session.get('user_id') is None:
            return jsonify({"auth": False, "status": False, "msg": "Unauthorized access"}), 401


@app.route('/')
def index():
    return "Hello chatbot API!", 200


@app.route('/api')
def api_redirect():
    # Redirect to the 'index' endpoint (root route)
    return redirect(url_for('index'))


@app.route('/api/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()  # Assuming the request contains JSON data
        user_name = data.get('username')
        email = data.get('email')
        password = data.get('password')

        data = {
            "auth": False,
            "status": False,
            "msg": "",
            "inputs": {
                "user_name": user_name,
                "email": email
            }
        }

        if user_name and email and password:
            try:
                # Create a MySQL cursor
                cur = mysql.connection.cursor()

                # Hash the password
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

                # Use parameterized query to prevent SQL injection
                query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s);"
                values = (user_name, email, hashed_password)
                
                # Execute the query with parameters
                cur.execute(query, values)

                # Commit changes to the database
                mysql.connection.commit()

                # Close the cursor
                cur.close()

                data["msg"] = "Successfully signup"
                data["status"] = True

                return jsonify(data), 201
            
            except Exception as e:
                # If an error occurs, rollback the transaction and return an error message
                mysql.connection.rollback()
                return jsonify({"status": False, "msg": f"Error: {str(e)}"}), 500
        
        else:
            # Change the vdata values
            data["msg"] = "Invalid data. Please provide both email and password!"
            return jsonify(data), 400
            
    else:
        return jsonify({"status": False, "msg": "Method Not Allowed"}), 405
    

@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Assuming the request contains JSON data
        user_name = data.get('username')
        password = data.get('password')

        data = {
            "auth": False,
            "status": False,
            "msg": "",
            "inputs": {
                "user_name": user_name,
                "password": password
            }
        }

        if user_name and password:
            try:
                # Create a MySQL cursor
                cur = mysql.connection.cursor()

                # Use parameterized query to prevent SQL injection
                query = "SELECT COUNT(*), id, password FROM users WHERE username = %s;"
                values = (user_name,)
                
                # Execute the query with parameters
                cur.execute(query, values)

                # Fetch the result
                result = cur.fetchall()

                # Check if the username already exists
                if result[0][0] != 1:
                    # Change the vdata values
                    data["msg"] = "Invalid login credentials!"
                    cur.close()
                    return jsonify(data), 401

                if bcrypt.check_password_hash(result[0][2], str(password)) != True:
                    # Change the vdata values
                    data["msg"] = "Invalid login credentials!"
                    cur.close()
                    return jsonify(data), 401

                cur.close()
                session['auth'] = 'True'
                session['user_id'] = str(result[0][1])

                return jsonify({"auth": True, "status": True, "msg": "Login successfully"}), 201
            
            except Exception as e:
                # If an error occurs, rollback the transaction and return an error message
                mysql.connection.rollback()
                return jsonify({"status": False, "msg": f"Error: {str(e)}"}), 500
        
        else:
            return jsonify({"status": False,  "msg": "Invalid data. Please provide both username and password!"}), 400
        
    else:
        return jsonify({"status": False,  "msg": "Method Not Allowed!"}), 405


@app.route('/api/logout')
def logout():
    session.pop('auth_status', None)
    session.pop('user_id', None)
    return jsonify({"auth_status": False, "msg": "Logged out successfully"}), 200


@app.route('/api/fogetpassword', methods=['POST'])
def foget_password():
    if request.method == 'POST':
        data = request.get_json()  # Assuming the request contains JSON data
        email = data.get('email')
        password = data.get('password')
        conform_password = data.get('conform_password')

        data = {
            "auth": False,
            "status": False,
            "msg": "",
            "inputs": {
                "email": email
            }
        }

        if email and password and conform_password:
            try:
                # Create a MySQL cursor
                cur = mysql.connection.cursor()

                # Use parameterized query to prevent SQL injection
                query = "SELECT COUNT(*), id FROM users WHERE email = %s;"
                values = (email,)
                
                # Execute the query with parameters
                cur.execute(query, values)

                # Fetch the result
                result = cur.fetchall()

                # Check if the username already exists
                if result[0][0] != 1:
                    # Change the vdata values
                    data["msg"] = "Invalid login credentials!"
                    cur.close()
                    return jsonify(data), 401

                if password != conform_password:
                    # Change the vdata values
                    data["msg"] = "Invalid login credentials!"
                    cur.close()
                    return jsonify(data), 401
                
                # Hash the password
                hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
                
                # Use parameterized query to prevent SQL injection
                query = "UPDATE users SET password = %s WHERE id = %s;"
                values = (hashed_password, int(result[0][1]))
                
                # Execute the query with parameters
                cur.execute(query, values)

                # Commit changes to the database
                mysql.connection.commit()

                # Close the cursor
                cur.close()

                return jsonify({"auth": False, "status": True, "msg": "Password change successfully"}), 201
            
            except Exception as e:
                # If an error occurs, rollback the transaction and return an error message
                mysql.connection.rollback()
                return jsonify({"status": False, "msg": f"Error: {str(e)}"}), 500
        
        else:
            return jsonify({"status": False,  "msg": "Invalid data. Please provide both username and password!"}), 400
        
    else:
        return jsonify({"status": False,  "msg": "Method Not Allowed!"}), 405
    

@app.route('/api/serch', methods=['POST'])
def serch():
    if request.method == 'POST':
        data = request.get_json()  # Assuming the request contains JSON data
        user_input = data.get('input')

        if user_input == None or user_input == "":
            return "Invalid input !", 404
    
        return user_input, 201

    else:
        return "Method Not Allowed", 405


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
