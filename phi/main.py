import mysql.connector
import PySimpleGUI as sg
import csv

mydb = mysql.connector.connect(
    host="ophcaredb.ch84a82emmh3.us-east-1.rds.amazonaws.com",
    user="admin",
    password='password',
    database='ophcaredb'
)

mycursor = mydb.cursor()


#function that performs query to database based on user input
def querySelect():
    #check input field that contain inputs and search query based on those input priority to ID
    if values['-IN 1-'] != '':
        patient_query = values['-IN 1-']
        mycursor.execute(f"SELECT * FROM phi WHERE patient_id= {patient_query}")
    elif values['-IN 2-'] != '':
        patient_query = values['-IN 2-']
        mycursor.execute(f"SELECT * FROM phi WHERE first_name= '{patient_query}'")
    elif values['-IN 3-'] != '':
        patient_query = values['-IN 3-']
        mycursor.execute(f"SELECT * FROM phi WHERE last_name= '{patient_query}'")
    elif values['-IN 4-'] != '':
        patient_query = values['-IN 4-']
        mycursor.execute(f"SELECT * FROM phi WHERE dob= '{patient_query}'")
    else:
    #If no inputs are found throw error
        raise Exception("Patient not found")
    myresults = mycursor.fetchall()
    #If query does not find record throw error
    if myresults == []:
        raise Exception("Patient not found")
    return myresults

#clear current query for new query
def clearQuery():
    window['-ID-'].update("", visible=False)
    window['-First-'].update(" ", visible=False)
    window['-Last-'].update("", visible=False)
    window['-Address-'].update("", visible=False)
    window['-dob-'].update("", visible=False)
    window['-diag-'].update("", visible=False)
    window['-med-'].update("", visible=False)
    # clear input fields
    for el in values:
        window[el].update('')

#layout for query application
layout = [[sg.Push(),sg.Text("Patient ID"),sg.In(key='-IN 1-')],
          [sg.Push(),sg.Text("First Name"),sg.In(key='-IN 2-')],
          [sg.Push(),sg.Text("Last Name"),sg.In(key='-IN 3-')],
          [sg.Push(),sg.Text("DOB"),sg.In(key='-IN 4-')],
          [sg.Push(),sg.Button("Search"),sg.Button("Cancel"),sg.Push()],
          [sg.Text(f"Patient ID:", key='-ID-',visible=False)],
          [sg.Text(f"First Name:", key='-First-',visible=False)],
          [sg.Text(f"Last Name:", key='-Last-',visible=False)],
          [sg.Text(f"Address:", key='-Address-',visible=False)],
          [sg.Text(f"DOB:", key='-dob-',visible=False)],
          [sg.Text(f"Diagnosis:", key='-diag-',visible=False)],
          [sg.Text(f"Medication:", key='-med-',visible=False)],
            ]
window = sg.Window("PHI Query", layout)


#craete an event loop
while True:
    event, values = window.read()
    if event == "Search":
        try:
            clearQuery()
            query = querySelect()
            for row in query:
                window['-ID-'].update(f"Patient ID: {row[0]}",visible=True)
                window['-First-'].update(f"First Name: {row[1]}", visible=True)
                window['-Last-'].update(f"Last Name: {row[2]}", visible=True)
                window['-Address-'].update(f"Address: {row[3]}", visible=True)
                window['-dob-'].update(f"DOB: {row[4]}", visible=True)
                window['-diag-'].update(f"Diagnosis: {row[5]}", visible=True)
                window['-med-'].update(f"Medication: {row[6]}", visible=True)
        #displays patient not found when error is thrown
        except:
            window['-ID-'].update("Patient not found",visible=True)


    #End program if user closes window or
    #presses the OK button
    if event == "Cancel" or event == sg.WIN_CLOSED:
        break

window.close()


