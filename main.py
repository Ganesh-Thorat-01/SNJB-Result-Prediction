from flask import Flask, render_template, request,send_file, redirect, url_for, flash, jsonify
import pickle
import pandas as pd
from io import BytesIO
import io
from flask import make_response

app=Flask(__name__)

model=pickle.load(open('src/model.pkl','rb'))

from flask_dropzone import Dropzone
app.config.update(
    DROPZONE_MAX_FILE_SIZE = 1024,
    DROPZONE_TIMEOUT = 5*60*1000,
    DROPZONE_REDIRECT_VIEW='multipleresults'
    )
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.ods, .xls, .xlsm, .xlsx'


dropzone = Dropzone(app)

outputDf=pd.DataFrame([["","","","","","","","",""]],columns=["PRN", "DSE",	"Sem1",	"Sem2",	"Sem3",	"Sem4",	"Sem5",	"Sem6",	"Sem7"])

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/prediction')
def prediction():
    return render_template('prediction.html')

@app.route('/prediction/results',methods=['GET','POST'])
def result():
    if request.method == 'POST':
        student_data={}
        dse=request.form["dse"]

        student_data["DSE"]=dse
        

        if dse=="NO":
            semester1 = request.form['semester1-select']
            semester2 = request.form['semester2-select']
            if semester1=="Cleared":
                sgpa1 = float(request.form['semester1-sgpa'])
                student_data["Sem1"]=sgpa1
            elif semester1=="ATKT":
                student_data["Sem1"]=semester1+" "+request.form['atkt1']
            else:
                student_data["Sem1"]=semester1
            if semester2=="Cleared":
                sgpa2 = float(request.form['semester2-sgpa'])
                student_data["Sem2"]=sgpa2
            elif semester2=="ATKT":
                student_data["Sem2"]=semester2+" "+request.form['atkt2']
            else:
                student_data["Sem2"]=semester2
            dse_final=0
            
        else:
            semester1='Cleared'
            semester2='Cleared'
            sgpa1=7.72
            sgpa2=7.72
            dse_final=1
            student_data["Sem1"]="-"
            student_data["Sem2"]="-"

        semester3 = request.form['semester3-select']
        semester4 = request.form['semester4-select']
        semester5 = request.form['semester5-select']
        semester6 = request.form['semester6-select']
        semester7 = request.form['semester7-select']

        
        sgpa3 = request.form['semester3-sgpa']
        if semester3=="Cleared":
            sgpa3=float(sgpa3)
            student_data["Sem3"]=sgpa3
        elif semester3=="ATKT":
                student_data["Sem3"]=semester3+" "+request.form['atkt3']
        else:
            student_data["Sem3"]=semester3

        sgpa4 = request.form['semester4-sgpa']
        if semester4=="Cleared":
            sgpa4=float(sgpa4)
            student_data["Sem4"]=sgpa4
        elif semester4=="ATKT":
                student_data["Sem4"]=semester4+" "+request.form['atkt4']
        else:
            student_data["Sem4"]=semester4

        sgpa5 = request.form['semester5-sgpa']
        if semester5=="Cleared":
            sgpa5=float(sgpa5)
            student_data["Sem5"]=sgpa5
        elif semester5=="ATKT":
                student_data["Sem5"]=semester5+" "+request.form['atkt5']
        else:
            student_data["Sem5"]=semester5

        sgpa6 = request.form['semester6-sgpa']
        if semester6=="Cleared":
            sgpa6=float(sgpa6)
            student_data["Sem6"]=sgpa6
        elif semester6=="ATKT":
                student_data["Sem6"]=semester6+" "+request.form['atkt6']
        else:
            student_data["Sem6"]=semester6

        sgpa7 = request.form['semester7-sgpa']
        if semester7=="Cleared":
            sgpa7=float(sgpa7)
            student_data["Sem7"]=sgpa7
        elif semester7=="ATKT":
                student_data["Sem7"]=semester7+" "+request.form['atkt7']
        else:
            student_data["Sem7"]=semester7

        



        #Intialize ATKT Status as false
        sem1ATKT=0
        sem2ATKT=0
        sem3ATKT=0
        sem4ATKT=0
        sem5ATKT=0
        sem6ATKT=0
        sem7ATKT=0

        #Intialize YD Status as false
        sem1YD=0
        sem2YD=0
        sem3YD=0
        sem4YD=0
        sem5YD=0
        sem6YD=0
        sem7YD=0

        #Intialize Fail Status as false
        sem1Fail=0
        sem2Fail=0
        sem3Fail=0
        sem4Fail=0
        sem5Fail=0
        sem6Fail=0
        sem7Fail=0

        #Initialize ATKTCount as zero
        sem1ATKTCount=0
        sem2ATKTCount=0
        sem3ATKTCount=0
        sem4ATKTCount=0
        sem5ATKTCount=0
        sem6ATKTCount=0
        sem7ATKTCount=0


        #Sem1
        if semester1=="ATKT":
            sgpa1=5
            sem1ATKT=1
            sem1ATKTCount=request.form['atkt1']
        if semester1=="YD":
            sgpa1=4
            sem1YD=1
        if semester1=="Failed":
            sgpa1=3
            sem1Fail=1

        #Sem2
        if semester2=="ATKT":
            sgpa2=5
            sem2ATKT=1
            sem2ATKTCount=request.form['atkt2']
        if semester2=="YD":
            sgpa2=4
            sem2YD=1
        if semester2=="Failed":
            sgpa2=3
            sem2Fail=1

        #Sem3
        if semester3=="ATKT":
            sgpa3=5
            sem3ATKT=1
            sem3ATKTCount=request.form['atkt3']
        if semester3=="YD":
            sgpa3=4
            sem3YD=1
        if semester3=="Failed":
            sgpa3=3
            sem3Fail=1

        #Sem4
        if semester4=="ATKT":
            sgpa4=5
            sem4ATKT=1
            sem4ATKTCount=request.form['atkt4']
        if semester4=="YD":
            sgpa4=4
            sem4YD=1
        if semester4=="Failed":
            sgpa4=3
            sem4Fail=1

        #Sem5
        if semester5=="ATKT":
            sgpa5=5
            sem5ATKT=1
            sem5ATKTCount=request.form['atkt5']
        if semester5=="YD":
            sgpa5=4
            sem5YD=1
        if semester5=="Failed":
            sgpa5=3
            sem5Fail=1

        #Sem6
        if semester6=="ATKT":
            sgpa6=5
            sem6ATKT=1
            sem6ATKTCount=request.form['atkt6']
        if semester6=="YD":
            sgpa6=4
            sem6YD=1
        if semester6=="Failed":
            sgpa6=3
            sem6Fail=1


        #Sem7
        if semester7=="ATKT":
            sgpa7=5
            sem7ATKT=1
            sem7ATKTCount=request.form['atkt7']
        if semester7=="YD":
            sgpa7=4
            sem7YD=1
        if semester7=="Failed":
            sgpa7=3
            sem7Fail=1


        data=[[
            dse_final,sgpa1,sgpa2,sgpa3,sgpa4,sgpa5,sgpa6,sgpa7,
            sem1ATKT,sem1ATKTCount,sem1YD,sem1Fail,
            sem2ATKT,sem2ATKTCount,sem2YD,sem2Fail,
            sem3ATKT,sem3ATKTCount,sem3YD,sem3Fail,
            sem4ATKT,sem4ATKTCount,sem4YD,sem4Fail,
            sem5ATKT,sem5ATKTCount,sem5YD,sem5Fail,
            sem6ATKT,sem6ATKTCount,sem6YD,sem6Fail,
            sem7ATKT,sem7ATKTCount,sem7YD,sem7Fail,
        ]]
        
        columns=[['DSE', 'Sem1', 'Sem2', 'Sem3', 'Sem4', 'Sem5', 'Sem6', 'Sem7',
       'Sem 1 ATKT', 'Sem 1 ATKT Count', 'Sem 1 YD', 'Sem 1 Fail',
       'Sem 2 ATKT', 'Sem 2 ATKT Count', 'Sem 2 YD', 'Sem 2 Fail',
       'Sem 3 ATKT', 'Sem 3 ATKT Count', 'Sem 3 YD', 'Sem 3 Fail',
       'Sem 4 ATKT', 'Sem 4 ATKT Count', 'Sem 4 YD', 'Sem 4 Fail',
       'Sem 5 ATKT', 'Sem 5 ATKT Count', 'Sem 5 YD', 'Sem 5 Fail',
       'Sem 6 ATKT', 'Sem 6 ATKT Count', 'Sem 6 YD', 'Sem 6 Fail',
       'Sem 7 ATKT', 'Sem 7 ATKT Count', 'Sem 7 YD', 'Sem 7 Fail']]
        df=pd.DataFrame(data,columns=columns)

        print(student_data)

        y_pred = model.predict(df)[0]
        
        Output=f"Predicted Result is {y_pred}"
        student_data["output"]=Output

        return render_template('result.html', data=student_data, output=Output)

    return render_template('result.html')

@app.route('/prediction/multipleresults',methods=['GET','POST'])
def multipleresults():
    global outputDf
    if request.method == 'POST':
        f = request.files.get('file')

        outputDf=pd.read_excel(f)

        df=pd.read_excel(f)

        #Transform and create column for ATKT, YD and FAIL
        def is_atkt(value):
            if 'ATKT' in str(value):
                return True
            else:
                return False
            
        def atkt_count(value):
            if 'ATKT' in str(value):
                res=value.split()
                return res[-1]
            else:
                return 0
        
        def is_yd(value):
            if 'YD' in str(value):
                return True
            else:
                return False
        
        def is_fail(value):
            if 'FAIL' in str(value):
                return True
            else:
                return False
        
        df["Sem 1 ATKT"]=df["Sem1"].apply(is_atkt)
        df["Sem 1 ATKT Count"]=df["Sem1"].apply(atkt_count)
        df["Sem 1 YD"]=df["Sem1"].apply(is_yd)
        df["Sem 1 Fail"]=df["Sem1"].apply(is_fail)

        df["Sem 2 ATKT"]=df["Sem2"].apply(is_atkt)
        df["Sem 2 ATKT Count"]=df["Sem2"].apply(atkt_count)
        df["Sem 2 YD"]=df["Sem2"].apply(is_yd)
        df["Sem 2 Fail"]=df["Sem2"].apply(is_fail)

        df["Sem 3 ATKT"]=df["Sem3"].apply(is_atkt)
        df["Sem 3 ATKT Count"]=df["Sem3"].apply(atkt_count)
        df["Sem 3 YD"]=df["Sem3"].apply(is_yd)
        df["Sem 3 Fail"]=df["Sem3"].apply(is_fail)

        df["Sem 4 ATKT"]=df["Sem4"].apply(is_atkt)
        df["Sem 4 ATKT Count"]=df["Sem4"].apply(atkt_count)
        df["Sem 4 YD"]=df["Sem4"].apply(is_yd)
        df["Sem 4 Fail"]=df["Sem4"].apply(is_fail)

        df["Sem 5 ATKT"]=df["Sem5"].apply(is_atkt)
        df["Sem 5 ATKT Count"]=df["Sem5"].apply(atkt_count)
        df["Sem 5 YD"]=df["Sem5"].apply(is_yd)
        df["Sem 5 Fail"]=df["Sem5"].apply(is_fail)

        df["Sem 6 ATKT"]=df["Sem6"].apply(is_atkt)
        df["Sem 6 ATKT Count"]=df["Sem6"].apply(atkt_count)
        df["Sem 6 YD"]=df["Sem6"].apply(is_yd)
        df["Sem 6 Fail"]=df["Sem6"].apply(is_fail)

        df["Sem 7 ATKT"]=df["Sem7"].apply(is_atkt)
        df["Sem 7 ATKT Count"]=df["Sem7"].apply(atkt_count)
        df["Sem 7 YD"]=df["Sem7"].apply(is_yd)
        df["Sem 7 Fail"]=df["Sem7"].apply(is_fail)

        #Replace ATKT, YD and FAIL with minimal Value

        def replace_atkt(value):
            if 'ATKT' in str(value):
                return 5
            else:
                return value

        def replace_yd(value):
            if 'YD' in str(value):
                return 4
            else:
                return value

        def replace_fail(value):
            if 'FAIL' in str(value):
                return 3
            else:
                return value
        
        df["Sem1"]=df["Sem1"].apply(replace_atkt)
        df["Sem1"]=df["Sem1"].apply(replace_yd)
        df["Sem1"]=df["Sem1"].apply(replace_fail)
        df["Sem1"]=df["Sem1"].astype(float)
        df["Sem 1 ATKT Count"]=df["Sem 1 ATKT Count"].astype(float)

        df["Sem2"]=df["Sem2"].apply(replace_atkt)
        df["Sem2"]=df["Sem2"].apply(replace_yd)
        df["Sem2"]=df["Sem2"].apply(replace_fail)
        df["Sem2"]=df["Sem2"].astype(float)
        df["Sem 2 ATKT Count"]=df["Sem 2 ATKT Count"].astype(float)

        df["Sem3"]=df["Sem3"].apply(replace_atkt)
        df["Sem3"]=df["Sem3"].apply(replace_yd)
        df["Sem3"]=df["Sem3"].apply(replace_fail)
        df["Sem3"]=df["Sem3"].astype(float)
        df["Sem 3 ATKT Count"]=df["Sem 3 ATKT Count"].astype(float)

        df["Sem4"]=df["Sem4"].apply(replace_atkt)
        df["Sem4"]=df["Sem4"].apply(replace_yd)
        df["Sem4"]=df["Sem4"].apply(replace_fail)
        df["Sem4"]=df["Sem4"].astype(float)
        df["Sem 4 ATKT Count"]=df["Sem 4 ATKT Count"].astype(float)

        df["Sem5"]=df["Sem5"].apply(replace_atkt)
        df["Sem5"]=df["Sem5"].apply(replace_yd)
        df["Sem5"]=df["Sem5"].apply(replace_fail)
        df["Sem5"]=df["Sem5"].astype(float)
        df["Sem 5 ATKT Count"]=df["Sem 5 ATKT Count"].astype(float)

        df["Sem6"]=df["Sem6"].apply(replace_atkt)
        df["Sem6"]=df["Sem6"].apply(replace_yd)
        df["Sem6"]=df["Sem6"].apply(replace_fail)
        df["Sem6"]=df["Sem6"].astype(float)
        df["Sem 6 ATKT Count"]=df["Sem 6 ATKT Count"].astype(float)

        df["Sem7"]=df["Sem7"].apply(replace_atkt)
        df["Sem7"]=df["Sem7"].apply(replace_yd)
        df["Sem7"]=df["Sem7"].apply(replace_fail)
        df["Sem7"]=df["Sem7"].astype(float)
        df["Sem 7 ATKT Count"]=df["Sem 7 ATKT Count"].astype(float)

        #Replace null values of sem1 and sem2 for dse with avg value

        df["Sem1"].fillna(7.72, inplace = True)
        df["Sem2"].fillna(7.72, inplace = True)

        #Convert categorical data to numerical format
        df["DSE"].replace({'YES':1,"NO":0},inplace=True)

        df["Sem 1 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 1 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 1 Fail"].replace({True:1,False:0},inplace=True)

        df["Sem 2 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 2 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 2 Fail"].replace({True:1,False:0},inplace=True)

        df["Sem 3 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 3 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 3 Fail"].replace({True:1,False:0},inplace=True)

        df["Sem 4 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 4 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 4 Fail"].replace({True:1,False:0},inplace=True)

        df["Sem 5 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 5 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 5 Fail"].replace({True:1,False:0},inplace=True)

        df["Sem 6 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 6 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 6 Fail"].replace({True:1,False:0},inplace=True)

        df["Sem 7 ATKT"].replace({True:1,False:0},inplace=True)
        df["Sem 7 YD"].replace({True:1,False:0},inplace=True)
        df["Sem 7 Fail"].replace({True:1,False:0},inplace=True)

        df.pop("PRN")

        pred=model.predict(df)
        
        outputDf["Result"]=pred

        
        return render_template('multiresult.html')
    
    
    
    return render_template('multiresult.html',column_names=outputDf.columns.values, row_data=list(outputDf.values.tolist()),
                    link_column="PRN", zip=zip)
   
@app.route('/analysis')
def dashboard():
    return render_template('dashboard.html')

@app.route('/sheets/<string:filename>', methods=['GET', 'POST'])
def download(filename):    
    return send_file("sheets/"+filename,as_attachment=True)

@app.route('/outputsheet', methods=['GET', 'POST'])
def downloadoutput():    
    global outputDf
    
    # Creating output and writer (pandas excel writer)
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')

   
    # Export data frame to excel
    outputDf.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    #writer.save()
    writer.close()

    
    # Flask create response 
    r = make_response(out.getvalue())
   

    
    # Defining correct excel headers
    r.headers["Content-Disposition"] = "attachment; filename=Output.xlsx"
    r.headers["Content-type"] = "application/x-xls"
    
    # Finally return response
    return r

    

if __name__=="__main__":
    app.run(debug=False)

