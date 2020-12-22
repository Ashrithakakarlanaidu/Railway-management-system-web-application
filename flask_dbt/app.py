from flask import Flask, request, render_template
from flask_cors import cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pyodbc


#connection to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-D1R0QFA;'
                      'Database=railway_train_reservation;'
                      'Trusted_Connection=yes;');

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/datareport", methods = ["GET", "POST"])
@cross_origin()
def data():
    option = request.form['exampleRadios']
    if option == 'option1':
        data = pd.read_sql("SELECT * FROM train5", conn)
        result=data.to_html()
        sns.countplot(x='train_class',data=data,palette="BuPu")
        plt.xlabel('train_class')
        plt.ylabel('count of each class')
        plt.title('countplot on train class')
        result=append_html(result,['trainclass.png'])
        plt.savefig('static/trainclass.png')

        sns.countplot(x='train_type',data=data,palette="RdBu")
        plt.xlabel('train_type')
        plt.ylabel('count of each train type')
        plt.title('countplot on train type')
        result=append_html(result,['traintype.png'])
        plt.savefig('static/traintype.png')

        #result=append_html(result,['t.jpg','p.jpg'])
    

    elif option == 'option2':
        data = pd.read_sql("SELECT * FROM station5", conn)
        result=data.to_html()
        sns.countplot(x='train_name',data=data,palette="RdPu")
        plt.xlabel('train_name')
        plt.ylabel('count of each train name')
        plt.title('countplot on train name')
        result=append_html(result,['trainname.png'])
        plt.savefig('static/trainname.png')

    elif option == 'option3':
        data = pd.read_sql("SELECT * FROM reserve_status5", conn)
        result=data.to_html()
        

    elif option == 'option4':
        data = pd.read_sql("SELECT * FROM passenger5 ", conn)
        result=data.to_html()
        sns.barplot(x='p_id', y='age',data=data)
        plt.xlabel('passenger_id')
        plt.ylabel('age of passengers')
        plt.title('barplot of passenger id and age ')
        plt.savefig('static/passenger.png')
        result=append_html(result,['passenger.png'])

    elif option == 'option5':
        data = pd.read_sql("SELECT * FROM ticket5", conn)
        result=data.to_html()
        
        sns.kdeplot(data=data['train_amt'])
        plt.xlabel('train_amt')
        plt.title('kdeplot of train_amt')
        plt.savefig('static/train_amt.jpg')
        result=append_html(result,['train_amt.jpg'])

    elif option == 'option6':
        data = pd.read_sql("SELECT * FROM ticket_checker5", conn)
        result=data.to_html()
        sns.barplot(x='tc_name',y='tc_age',data=data,palette="BuPu")
        plt.xlabel('tc_name')
        plt.ylabel('tc_age')
        plt.title('barplot of tc_name and tc_age')
        plt.savefig('static/check.jpg')
        result=append_html(result,['check.jpg'])
    return result



def append_html(result,image_names):
    for i in image_names:
        result=result+" <img src=\"static/"+i+"\" width=\"600\" height=\"500\">"
    return result


if __name__ == "__main__":
    app.run(debug=True)


