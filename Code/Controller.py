import Model as model
import View as view
import datetime
import sqlite3

device = ['TV', 'Kettle', 'Microwave', 'Toaster', 'Washing_Machine', 'Tumble_Dryer', 'Dishwasher', 'Fridge', 'Freezer']
days = ['WorkingDay', 'WeekEnd']
md = model.Model()

### Check which table has been inserted
def checkInsertedTable():
    insertedList = []
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    for i in range(len(device)):
        cur.execute("SELECT * FROM '%s';" % (str(device[i])))
        table = cur.fetchall()
        if table: insertedList.append(device[i])
    con.commit()
    con.close()
    return insertedList


### Function used to insert data into database
def insertValeu(csv_file, csv_reader):
    getInsertedList = []
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    ### choose table base on the file name
    getDevice = " "
    if "TV" in str(csv_file) or "tv" in str(csv_file): getDevice = device[0]
    elif "KT" in str(csv_file) or "kt" in str(csv_file): getDevice = device[1]
    elif "MICRO" in str(csv_file) or "micro" in str(csv_file): getDevice = device[2]
    elif "TER" in str(csv_file) or "ter" in str(csv_file): getDevice = device[3]
    elif "WM" in str(csv_file) or "wm" in str(csv_file): getDevice = device[4]
    elif "TD" in str(csv_file) or "td" in str(csv_file): getDevice = device[5]
    elif "DW" in str(csv_file) or "dw" in str(csv_file): getDevice = device[6]
    elif "FRI" in str(csv_file) or "fri" in str(csv_file): getDevice = device[7]
    elif "FRE" in str(csv_file) or "fre" in str(csv_file): getDevice = device[8]
    else: return "NULL"

    ### insert into database
    for field in csv_reader:
        if field[0] == "" or field[1] == "" or field[2] == "" or field[3] == "": continue
        ### deal with time
        if (len(field[2])) < 5: Time = "0"+str(field[2])
        else: Time = field[2]
        cur.execute("INSERT INTO '%s' VALUES ('%s', '%s', '%s', '%s');" % (str(getDevice), field[0], field[1], Time, field[3]))
    
    con.commit()
    con.close()
    getInsertedList = checkInsertedTable()
    return getInsertedList


### Function used to drop table inside database
def dropTable(tableList):
    getTableName = []
    getInsertedList = []
    if 'All' in tableList: getTableName = device
    else: getTableName = tableList
    
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    for i in range(len(getTableName)):
        cur.execute("DROP TABLE '%s'" % (str(getTableName[i])))
        cur.execute("CREATE TABLE '%s' (Household_Id, Date, Time, Watt)" % (str(getTableName[i])))

    con.commit()
    con.close()
    getInsertedList = checkInsertedTable()
    return getInsertedList

    

### Function used for run the Monte Carlo
def runSystem(deviceList, needAll, numSim, onlyAll, specifyDevice):
    ### Smoothing data
    md.coordinateData(deviceList, days)
    ### Running Monte Carlo
    md.runModel(deviceList, days, numSim)
    WD_AVGfigure, WE_AVGfigure = view.showGraph(md.getTargetTime(), md.getResult(), deviceList, days, needAll, onlyAll, specifyDevice)
    getImageList = view.plotProbDensity(md.getResult(), deviceList, days)
    return WD_AVGfigure, WE_AVGfigure, getImageList


### Function used to check the variable is integer
def checkInt(var):
    try:
        int(var)
        return True
    except ValueError: return False

