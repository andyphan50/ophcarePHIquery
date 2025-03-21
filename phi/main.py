import mysql.connector
import mysql
from mysql.connector import Error
import PySimpleGUI as sg

#global variables initialized
username = ''; 
password = ''; 
mycursor = ''; 
loggedIn = False; 


#function that performs query to database based on user input
def querySelect():
    #check input field that contain inputs and search query based on those input priority to ID
    if values['-IN 1-'] != '':
        patient_query = values['-IN 1-']
        mycursor.execute(f"SELECT * FROM phidata WHERE patient_id= {patient_query}")
    elif values['-IN 2-'] != '':
        patient_query = values['-IN 2-']
        mycursor.execute(f"SELECT * FROM phidata WHERE first_name= '{patient_query}'")
    elif values['-IN 3-'] != '':
        patient_query = values['-IN 3-']
        mycursor.execute(f"SELECT * FROM phidata WHERE last_name= '{patient_query}'")
    elif values['-IN 4-'] != '':
        patient_query = values['-IN 4-']
        mycursor.execute(f"SELECT * FROM phidata WHERE dob= '{patient_query}'")
    else:
    #If no inputs are found throw error
        raise Exception("Patient not found")
    #store results obtained from database into myresults
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


#layout for login page
loginLayout = [[sg.Push(),sg.Text("Username"),sg.In(key='-USERNAME-')],
               [sg.Push(),sg.Text("Password:"),sg.In(key='-PASSWORD-')],
               [sg.Button("Login"),sg.Button("Exit")],
               [sg.Text(f"Incorrect credentials", key='-feedback-',visible=False)], 
               ]

#create login window
login_window = sg.Window("Login", loginLayout); 


#create an event loop for both windows
while True:
    #can only have one window being read at a time, starts with the login page 
    login_event, login_values = login_window.read(); 
    #if exit button is pressed, the login page will close
    if login_event == "Exit" or login_event == sg.WIN_CLOSED: 
        login_window.close()
        break
    
    #checks if the login credentials are valid, if so, close the login page and opens
    #the main application 
    if login_event =="Login": 
        #store credentials used by user input 
        username = login_values['-USERNAME-']
        password = login_values['-PASSWORD-']
        #try to connect to aws database server using credentials
        try: 
            mydb = mysql.connector.connect(
            host="ophcare-db.ch84a82emmh3.us-east-1.rds.amazonaws.com",
            user= username,
            password= password,
            database='ophcare-db',
            auth_plugin = 'caching_sha2_password'
            )
            mycursor = mydb.cursor()
            #check if connection has been established to cloud rds
            if mydb.is_connected(): 
                #close login window and open up main application window event loop
                login_window.close()
                window = sg.Window("PHI Query", layout); 
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
                        window.close()
                        break
        #exception to catch incorrect credentials and failure to establish rds connection
        except Error as e:
            login_window['-feedback-'].update(f"Incorrect credentials",visible=True) 
            print(e)

        




