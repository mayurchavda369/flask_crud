from flask import Flask, request, render_template,flash, url_for, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = "mayur369"


# # MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mayur369'
app.config['MYSQL_DB'] = 'flask_crud'
mysql = MySQL(app)


@app.route("/")
def home():
    return render_template('home.html')

@app.route('/adddata', methods=['POST'])
def adddata():
    if request.method == 'POST':
        flash('DATA ADDED SUCCESFULLY','success')
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']

        try:
            # Establish a database connection and execute the query
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student(name,email,gender,password,address,city,phone) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                        (name, email, gender, password, address, city, phone))
            
            # Commit the changes to the database
            mysql.connection.commit()

            # Close the cursor
            cur.close()

            return redirect(url_for('home'))
        except Exception as e:
            # Print the error if something goes wrong
            print("Error:", str(e))
            return "An error occurred while adding data."
        
@app.route('/showdata')
def showdata():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student")
    
    # Commit the changes to the database
    data=cur.fetchall()

    cur.close()
    return render_template('showdata.html',student=data)
# Your imports and configuration remain the same


@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        password = request.form['password']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']

        cur.execute('UPDATE student SET name = %s, email = %s, gender = %s, password = %s, address = %s, city = %s, phone = %s WHERE id = %s',
                    (name, email, gender, password, address, city, phone, id))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('showdata'))
    else:
        cur.execute('SELECT * FROM student WHERE id = %s', (id,))
        item = cur.fetchone()
        
        cur.close()
        return render_template('update.html', student=item)
@app.route('/delete/<int:id>')
def delete(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM student WHERE id=%s',(id,))
    mysql.connection.commit()
    cur.close()
    flash('DATA DELETED SUCCESSFULLY', 'success')
    return redirect(url_for('showdata'))



if __name__ == "__main__":
    app.run(debug=True, port=9999)
