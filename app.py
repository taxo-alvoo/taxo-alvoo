from flask import *
import pymysql
from sms import *

app = Flask(__name__)
app.secret_key = 'TAXO_ALVOO2005'
connection=pymysql.connect(host='localhost',user='root',password='',database='alvin')
@app.route('/')
def splash():
    return render_template('my_splash.html')


@app.route('/home')
def home():
    sql1="SELECT * FROM products WHERE product_category='fruit'"
    sql2="SELECT * FROM products WHERE product_category='feed'"
    sql3="SELECT * FROM products WHERE product_category='tool'"
    sql4="SELECT * FROM products WHERE product_category='vegetable'"
    cursor1 = connection.cursor()
    cursor2= connection.cursor()
    cursor3= connection.cursor()
    cursor4=connection.cursor()
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    cursor3.execute(sql3)
    cursor4.execute(sql4)
    # fetch rows
    fruit=cursor1.fetchall()
    feed=cursor2.fetchall()
    tool=cursor3.fetchall()
    vegetable=cursor4.fetchall()
    return render_template('home.html',fruit=fruit,feed=feed,tool=tool,vegetable=vegetable)



@app.route('/viewcomments')
def viewcomments():

    sql1="SELECT * FROM comments WHERE comment_category='positive'"
    sql2="SELECT * FROM comments WHERE comment_category='negative'"
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor1.execute(sql1)
    cursor2.execute(sql2)
    positive=cursor1.fetchall()
    negative=cursor2.fetchall()
    return render_template('viewcomments.html',positive=positive,negative=negative)
    # cursor.execute(sql)
    #   #   check if empty records
    # if cursor.rowcount==0:
    #     return render_template('viewcomments.html',message='NO COMMENTS')
    # else:
    #     return render_template('viewcomments.html')





@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method=='POST':
        # upload here        
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_cost = request.form['product_cost']
        product_category = request.form['product_category']
        image_name = request.files['image_name']
        image_name.save('static/images/' + image_name.filename)
        
        # connct to DB
        # create a cursor 
        cursor=connection.cursor()
        data=(product_name , product_description , product_cost , product_category , image_name.filename)
        sql= 'insert into products(product_name,product_description , product_cost , product_category ,image_name) values(%s,%s,%s,%s,%s)'
        cursor.execute(sql,data)
        connection.commit()
        return render_template('upload.html' ,message="Upload Completed")
    else:
        return render_template('upload.html')
    
@app.route('/vegetables')    
def vegetable():
    sql="SELECT * FROM products WHERE product_category='vegetable'"
    cursor = connection.cursor()
    cursor.execute(sql)
    vegetable=cursor.fetchall()
    return render_template('vegetables.html',vegetable=vegetable)



@app.route('/fruits')    
def fruits():
    sql="SELECT * FROM products WHERE product_category='fruit'"
    cursor = connection.cursor()
    cursor.execute(sql)
    fruit=cursor.fetchall()
    return render_template('fruits.html',fruit=fruit)


@app.route('/feeds')    
def feeds():
    sql="SELECT * FROM products WHERE product_category='feed'"
    cursor = connection.cursor()
    cursor.execute(sql)
    feed=cursor.fetchall()
    return render_template('feeds.html',feed=feed)



# @app.route('/update',methods=['POST','GET'])
# def update():
#     if request.method=='POST':    
#         product_id=request.form['product_id'] 
#         product_name = request.form['product_name']
#         product_cost = request.form['product_cost']
#         image_name = request.files['image_name']
#         image_name.save('static/images/' + image_name.filename)        
#         cursor=connection.cursor()
#         data=(product_id, product_name , product_cost  , image_name.filename)
#         sql= 'insert into products(product_id,product_name, product_cost  ,image_name) values(%s,%s,%s,%s)'
#         cursor.execute(sql,data)
#         connection.commit()
#         return render_template('update.html' ,message="Update Is Completed")
#     else:
#         return render_template('update.html')
@app.route('/profile')
def profile():   
    return render_template("profile.html")

# PROFILE THINGS
# 1.education

@app.route('/education')
def education():   
    return render_template("education.html")
# 2.contacts

@app.route('/contacts')
def contacts():   
    return render_template("contacts.html")
# 3.aboutme

@app.route('/aboutme')
def aboutme():
    return render_template("aboutme.html")

    


@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        phone_no= request.form['phone_no']
        password=request.form['password']
        cursor=connection.cursor()
        sql='SELECT * FROM users WHERE phone_no=%s AND password=%s'
        cursor.execute(sql, (phone_no,password))
        if cursor.rowcount ==0:
            return render_template('login.html',error='invalid password')
        else:
            session['key']=phone_no
            sms 
            send_sms(phone_no,message="Thank You For yourLogIn On Mkulima Mkononi")
            return redirect('/home')
        



@app.route('/help')
def help():   
    return render_template('help.html')



        
@app.route('/logout')
def logout():
  session.clear()
  return redirect('/login') 





@app.route('/tobuy/<product_id>')
def tobuy(product_id):
    cursor1=connection.cursor()
    sql = "SELECT * FROM products WHERE product_id= %s"
    cursor1.execute(sql , (product_id))
    product=cursor1.fetchone()
    return render_template('tobuy.html', product=product) 

@app.route('/comment',methods=['POST','GET'])
def comments():
    if request.method=='POST':
        # comment here        
        username = request.form['username']
        comment_category=request.form['comment_category']
        comment = request.form['comment']        
        # connct to DB
        # create a cursor 
        cursor=connection.cursor()
        data=(username ,comment_category, comment )
        sql= 'insert into comments(username,comment_category,comment) values(%s,%s,%s )'
        cursor.execute(sql,data)
        connection.commit()
        return render_template('comments.html' ,message="Thank You For Your Comment")
    else:
        return render_template('comments.html')



connection=pymysql.connect(host='localhost',user='root',password='',database='alvin')
@app.route('/register',methods=['POST','GET'])
def register():

    if request.method=='GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email=request.form['email']
        phone_no=request.form['phone_no']
        password1=request.form['password1']
        cpassword=request.form['cpassword']
# verify if password is lessthan 8 charctars
        if len(password1) < 8:
            return render_template('register.html', error="the password is not enough")
        elif password1!=cpassword:
            return render_template('register.html',error="the password does not match")
        else:
            cursor=connection.cursor()
            sql='insert into users(username,email,phone_no,password) values(%s,%s,%s,%s)'
            cursor.execute(sql, (username, email, phone_no,password1))
            connection.commit()
            sms
            send_sms(phone_no,message="Thank You For Registering On Mkulima Mkononi")            
            # return render_template('register.html',success='You Are Welcome')
            session['key']=phone_no
            return redirect('/home')
        













 
           







@app.route('/mpesa', methods = ['POST'])
def mpesa():
    # Receive the amount and phone from single item
    phone_no = request.form['phone_no']
    amount = request.form['product_cost']
    # import mpesa.py module
    import mpesa
    # Call the SIM Toolkit(stk) push function present in mpesa.py
    mpesa.stk_push(phone_no, amount)
    # SHow user below message.
    return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
    '<a href="/home" class="btn btn-dark btn-sm">Back to Products</a>'

        




app.run(debug=True)