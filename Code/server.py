from flask import Flask, url_for, flash, redirect, render_template, request, session
from io import TextIOWrapper
import Controller as control
import os, glob
import csv, sqlite3
import collections
import os.path


app = Flask(__name__, static_url_path = "/static", static_folder = "static")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

filelist = glob.glob(os.path.join("static/images/", "*.png"))
for f in filelist: os.remove(f)

os.remove("database.db")
open("database.db", "x")

con = sqlite3.connect("database.db")
cur = con.cursor()
for device in control.device:
    cur.execute("DROP TABLE IF EXISTS '%s';" % (str(device)))
    cur.execute("CREATE TABLE '%s' (Household_Id, Date, Time, Watt)" % (str(device)))
con.commit()
con.close()


@app.route('/', methods=['GET', 'POST'])
def Dashboard():
    getInsertedList = control.checkInsertedTable()
    if request.form.get('action') == 'Select':
        numSim = ''
        onlyAll = needAll = False
        specifyDevice = []
        ### Deal with iteration
        checkIteration = list(request.form.getlist('device'))[len(list(request.form.getlist('device')))-1]
        if control.checkInt(checkIteration) == True:
            numSim = list(request.form.getlist('device')).pop()
            deviceList = list(request.form.getlist('device'))[:len(list(request.form.getlist('device')))-1]
        else: deviceList = list(request.form.getlist('device'))[:len(list(request.form.getlist('device')))-1]
        
        ### Give out error message if press the "select" button without select any device
        if len(deviceList) == 0: 
            flash("You have not selected any device !!")
            return redirect(request.url)

        ### Take account the case if only selecting "All"
        if 'All' in deviceList and len(deviceList) == 1: 
            onlyAll = needAll = True
            deviceList = getInsertedList

        ### Take account the case if selecting "All" and other devices
        elif 'All' in deviceList and len(deviceList) > 1: 
            needAll = True
            deviceList.remove('All')
            specifyDevice = deviceList
            deviceList = getInsertedList
        
        session['select_device'] = deviceList

        ### Check avavilable data of selected device
        ### Deal with "All", check database
        if len(deviceList) == int(0):
            flash("You have not inserted any data in the table of selected device !!")
            return redirect(request.url)
        ### Deal with devices without "All"
        for device in deviceList:
            if device not in control.checkInsertedTable():
                flash("You have not inserted any data in the table of selected device !!")
                return redirect(request.url)
        ### Deal with devices with "All"
        if len(specifyDevice) != int(0):
            for device in specifyDevice:
                if device not in control.checkInsertedTable():
                    flash("You have not inserted any data in the table of selected device !!")
                    return redirect(request.url)


        filelist = glob.glob(os.path.join("static/images/", "*.png"))
        for f in filelist: os.remove(f)
        WD_AVGfigure, WE_AVGfigure, getImageList = control.runSystem(deviceList, needAll, numSim, onlyAll, specifyDevice)
        session['WD_AVGfigure'] = WD_AVGfigure
        session['WE_AVGfigure'] = WE_AVGfigure


        for i in range(len(getImageList)):
            if i < len(getImageList)/2: 
                day = "WDPD"
                device = i
            else: 
                day = "WEPD"
                device = i - int(len(getImageList)/2)
            
            session[str(day)+str(session.get('select_device')[int(device)])] = str(getImageList[i])
        return render_template('main.html', select_sentence = "Success!!", insertedTable=getInsertedList, selectedDevices=session.get('select_device'), figure='images/' +  WD_AVGfigure, prob_density='images/' + session.get(str("WDPD")+str(session.get('select_device')[0])))
    
    if request.form.get('action') == 'Upload File':
        ### read csv file
        csv_file = request.files['file']

        ### no file imported
        if csv_file.filename == '':
            flash('No selected file !!')
            return redirect(request.url)
        
        ### only allow csv file uploaded
        if str("text/csv") != str(str(csv_file)[len(str(csv_file))-11:len(str(csv_file))-3]): 
            flash('Only csv file can be uploaded !!')
            return redirect(request.url)

        csv_reader = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'), delimiter=',')
        next(csv_reader)
        getInsertedList = control.insertValeu(csv_file, csv_reader)

        ### Give Error if the file name is not following the guideline
        if getInsertedList == "NULL":
            flash('Unkown Device Data !!')
            return redirect(request.url)

        return render_template('main.html', upload_sentence="Uploaded !!", insertedTable=getInsertedList, selectedDevices=0, figure='images/result.jpg', prob_density='images/result.jpg')
    
    if request.form.get('action') == 'Clean Table':
        ### Giving error if the user has not selected any table
        if len(request.form.getlist('table')) == int(0): 
            flash('You have not selected which table you would like to clean !!')
            return redirect(request.url)

        getInsertedList = control.dropTable(request.form.getlist('table'))
        return render_template('main.html', database_sentence="Cleaned !!", insertedTable=getInsertedList, selectedDevices=0, figure='images/result.jpg', prob_density='images/result.jpg')
    
    if request.form.get('action') == 'Choose Result':
        ### Giving error if the result have not been displayed
        if request.form.getlist('pd')[0] == "No Device":
            flash('No device can be displayed !!')
            return redirect(request.url)
        device = str(request.form.getlist('pd')[0])
        if "workingday" in request.form.getlist('day'): 
            return render_template('main.html', insertedTable=getInsertedList, selectedDevices=session.get('select_device'), figure='images/' + session.get('WD_AVGfigure'), prob_density='images/' + session.get(str("WDPD")+str(device)))
        if "weekend" in request.form.getlist('day'): 
            return render_template('main.html', insertedTable=getInsertedList, selectedDevices=session.get('select_device'), figure='images/' + session.get('WE_AVGfigure'), prob_density='images/' + session.get(str("WEPD")+str(device)))

    return render_template('main.html', insertedTable=getInsertedList, selectedDevices=0, figure='images/result.jpg', prob_density='images/result.jpg')


@app.route('/Guideline', methods=['GET', 'POST'])
def Guideline():
    if request.method == 'POST':
        return redirect(url_for('Dashboard'))
    return render_template('Guideline.html')




if __name__ == '__main__':
    app.run()

