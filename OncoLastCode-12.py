
#import MySQLdb
import getpass
from typing import Text
#import random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime
from PyQt5.QtGui import *
#from PyQt5.QtWidgets import QApplication
import mysql.connector
from mysql.connector import Error
#from mysql.connector.errorcode import ER_PERFSCHEMA_TABLES_INIT_FAILED
#from PyQt5.QtGui import QIntValidatorp
from xlrd import *
from xlsxwriter import *
from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
#from x004design import Ui_MainWindow  #  thomas00design
from PyQt5.uic import loadUiType
#import pymysql
#from PyQt5 import QtWidgets    #######    to centralize checkbox
FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "print_row.ui"))
#FORM_CLASS2, _ = loadUiType(path.join(path.dirname(__file__), "login.ui"))
drug_table=[]
names_list = []
drugs_list = []
id_list = []
ids={}#checked remain number
check_add_drugs = []
LastStateRole = QtCore.Qt.UserRole
loaded=False

 #MainUI, _ = loadUiType('main.ui')
###########################################################   to centralize checkbox
class CheckBoxStyle(QtWidgets.QProxyStyle):
    def subElementRect(self,element,option,widget=None):
        r=super().subElementRect(element,option,widget)
        if element == QtWidgets.QStyle.SE_ItemViewItemCheckIndicator:
            r.moveCenter(option.rect.center())
        return r
###############################################################################
class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if ((1+index.column()) % 3 == 0): # Every third column
            painter.setPen(QPen(Qt.red, 5))
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.DB_Connect()
        self.Handel_Button()
        self.Ui_Changes()
        self.int_vaildator()
        self.d_validator()
        self.Add_fulid_to_combobox()
        self.get_names_from_db()
        self.patient_names_for_main()
        self.get_drug_from_db()
        self.add()
        self.patient_names_for_report()
        self.drug_names_for_report()
        self.set_today_date()
        self.get_patient_number_from_db()
        self.set_patient_number_for_report()
        self.show_daily_statics()
    
        

        # changes are 1. make autoRefresh 2.stop genral_search fun in update_check_status 3. filter4 to search by drug name  with query 4.enlarge the window

        #autoRefresh=QtCore.QTimer(self)
        #autoRefresh.timeout.connect(self.genral_search) 
        #autoRefresh.timeout.connect(self.createTable)
        #autoRefresh.start(300000)  # timer  in millsecond = 5 min

    #############################################  
    def Ui_Changes(self):
       # table1 = self.tableWidget.horizontalHeader()
       # table1.setSectionResizeMode(0, QHeaderView.Stretch)
       # table1.setSectionResizeMode(2, QHeaderView.Stretch)
       # table1.setSectionResizeMode(4, QHeaderView.Stretch)
        #table2 = self.tableWidget_2.horizontalHeader()
        #table2.setSectionResizeMode(0, QHeaderView.Stretch)
        #table2.setSectionResizeMode(2, QHeaderView.Stretch)
        #table2.setSectionResizeMode(4, QHeaderView.Stretch)
        #table3 = self.tableWidget_3.horizontalHeader()
        #table3.setSectionResizeMode(0, QHeaderView.Stretch)
        #table4 = self.tableWidget_4.horizontalHeader()
        #table4.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        #table4.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #table4.setSectionResizeMode(2, QHeaderView.Fixed)  #  drug
        #table4.setSectionResizeMode(3, QHeaderView.Fixed)  # dose
        #table4.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        #table4.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        #table4.setSectionResizeMode(6, QHeaderView.Stretch) # notes
        #table4.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        #table4.setSectionResizeMode(8, QHeaderView.ResizeToContents)

       # self.tableWidget_4.resizeRowsToContents()
        #table5 = self.tableWidget_5.horizontalHeader()
        #table5.setSectionResizeMode(0, QHeaderView.Stretch)
        #table5.setSectionResizeMode(1, QHeaderView.Stretch)
        table6 = self.tableWidget_6.horizontalHeader()
        table6.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        table6.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget_7.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_6.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_3.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_4.setEditTriggers(QAbstractItemView.NoEditTriggers) # to prevent table edit 
        self.tableWidget_8.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_5.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_9.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(5)
        self.tabWidget_3.setCurrentIndex(0)
        self.lineEdit.setFocus()
        self.tabWidget_3.hide()
        self.pushButton_15.hide()
        self.lineEdit_6.setMaxLength(1)
        ###################################################################
        self.tableWidget.setColumnWidth(0,230) # drug
        self.tableWidget.setColumnWidth(1,110)  # dose
        self.tableWidget.setColumnWidth(2,90) # fluid
        self.tableWidget.setColumnWidth(3,60) # volium
        self.tableWidget.setColumnWidth(4,500) # note 

        self.tableWidget_7.setColumnWidth(0,230) # drug
        self.tableWidget_7.setColumnWidth(1,90)  # dose
        self.tableWidget_7.setColumnWidth(2,80) # fluid
        self.tableWidget_7.setColumnWidth(3,50) # volium
        self.tableWidget_7.setColumnWidth(4,560) # note 

        self.tableWidget_2.setColumnWidth(0,220) # drug
        self.tableWidget_2.setColumnWidth(1,85)  # dose
        self.tableWidget_2.setColumnWidth(2,75) # fluid
        self.tableWidget_2.setColumnWidth(3,50) # volium
        self.tableWidget_2.setColumnWidth(4,630) #  note
        self.tableWidget_2.setColumnWidth(5,90)  #  date

        self.tableWidget_3.setColumnWidth(0,270) # drug
        self.tableWidget_3.setColumnWidth(1,200)  # dose

        self.tableWidget_9.setColumnWidth(0,25) # No
        self.tableWidget_9.setColumnWidth(1,220) # p.name
        self.tableWidget_9.setColumnWidth(2,85) #ID
        self.tableWidget_9.setColumnWidth(3,140) # Drug
        self.tableWidget_9.setColumnWidth(4,90) # Dose
        self.tableWidget_9.setColumnWidth(5,80) # fluid
        self.tableWidget_9.setColumnWidth(6,50) # volium
        self.tableWidget_9.setColumnWidth(7,400) # notes
        #self.tableWidget_9.setColumnWidth(8,45)

        self.tableWidget_8.setColumnWidth(4,400) # Note
        self.tableWidget_8.setColumnWidth(1,90)  #pt id
        self.tableWidget_8.setColumnWidth(0,220) # pt name 
        self.tableWidget_8.setColumnWidth(2,160) # drug
        self.tableWidget_8.setColumnWidth(6,40) # check
        self.tableWidget_8.setColumnWidth(5,80)  #  date
        self.tableWidget_8.setColumnWidth(3,80) # dose

        self.tableWidget_5.setColumnWidth(0,300) # drug  
        self.tableWidget_5.setColumnWidth(1,250)  # dose in mg 
        self.tableWidget_5.setColumnWidth(2,100) # NO

        self.tableWidget_4.setColumnWidth(0,220) # name
        self.tableWidget_4.setColumnWidth(1,70) # ID
        self.tableWidget_4.setColumnWidth(2,130) # drug
        self.tableWidget_4.setColumnWidth(3,70) # dose
        self.tableWidget_4.setColumnWidth(4,70) # fluid
        self.tableWidget_4.setColumnWidth(5,50) # volium
        self.tableWidget_4.setColumnWidth(6,390) # note
        self.tableWidget_4.setColumnWidth(7,80) # date
        self.tableWidget_4.setColumnWidth(8,40) # check


        self.tableWidget_10.setColumnWidth(0,10) # No
        self.tableWidget_10.setColumnWidth(1,175) # Name
        self.tableWidget_10.setColumnWidth(2,90) # id

        self.tableWidget_10.setColumnWidth(3,10) # No
        self.tableWidget_10.setColumnWidth(4,175) # Name
        self.tableWidget_10.setColumnWidth(5,90) # id

        self.tableWidget_10.setColumnWidth(6,10) # No
        self.tableWidget_10.setColumnWidth(7,175) # Name
        self.tableWidget_10.setColumnWidth(8,90) # id

        self.tableWidget_10.setColumnWidth(9,10) # No
        self.tableWidget_10.setColumnWidth(10,175) # Name
        self.tableWidget_10.setColumnWidth(11,90) # id

        self.tableWidget_10.setColumnWidth(12,10) # No
        self.tableWidget_10.setColumnWidth(13,175) # Name
        self.tableWidget_10.setColumnWidth(14,90) # id
        
        self.tableWidget_10.setColumnWidth(15,10) # No
        self.tableWidget_10.setColumnWidth(16,175) # Name
        self.tableWidget_10.setColumnWidth(17,90) # id
     

        self.tableWidget_10.setItemDelegate(Delegate(self.tableWidget_10))


        
        
        self.pushButton_17.hide()

        self.lineEdit_19.textChanged.connect(lambda: self.filter (self.lineEdit_19.text(),color = False )) # without query
        self.lineEdit_20.textChanged.connect(lambda: self.filter2 (self.lineEdit_20.text(),color = False ))  # without query
        self.lineEdit_21.textChanged.connect(lambda: self.filter3 (self.lineEdit_21.text(),color = False )) # make color true if we want search highligt name  # without query
        self.lineEdit_23.textChanged.connect(self.filter4)  #  user query
        self.lineEdit_10.textChanged.connect(lambda: self.filter5 (self.lineEdit_10.text(),color = False ))

       

        #self.lineEdit_22.textChanged.connect(
         #       lambda: self.result(self.lineEdit_22.text()))
        #self.lineEdit_23.textChanged.connect(
          #      lambda: self.result(self.lineEdit_23.text(), color=True))
    def DB_Connect(self):
        try:#MySQLdb#
          #  print("connecting to database")
            self.db = mysql.connector.connect(host='localhost',db='hospital',user='root',password='toor', use_unicode='True',charset="utf8")
           # print(self.db)
            # self.cur = self.db.cursor(buffered=True)
            # self.db.autocommit = False
            #self.db.set_character_set('utf8')
            self.cur = self.db.cursor()
           # print(self.cur)
            self.cur.execute('SET NAMES utf8;')
            self.cur.execute('SET CHARACTER SET utf8;')
            self.cur.execute('SET character_set_connection=utf8;')
            self.statusBar().showMessage('Database Connected Successfully',5000)
        except Error as e:
            print("error",e)
            self.statusBar().showMessage('Failed To Connect To Database',5000)


    def Handel_Button(self):
        ##########################################################
        ''' Add Drug'''
        self.pushButton_5.clicked.connect(self.add_drug)
        self.pushButton_29.clicked.connect(self.clear_drug_area)
        self.pushButton_28.clicked.connect(self.get_modify_drug)
        self.pushButton_27.clicked.connect(self.show_daily_statics_costum)
        self.pushButton_25.clicked.connect(self.delete_patient_visit)
        self.pushButton_26.clicked.connect(self.delete_patient_data)
        self.pushButton_24.clicked.connect(self.clear_patient_mang_data)
        self.pushButton_23.clicked.connect(self.get_patient_data_for_mangment)
        self.pushButton_22.clicked.connect(self.clear_database_data)
        self.lineEdit_15.editingFinished.connect(self.search_for_drug_to_update)
        self.pushButton_21.clicked.connect(self.update_drug)
        self.pushButton_18.clicked.connect(self.new_prescription_for_patient_has_old_one)
        self.pushButton_6.clicked.connect(self.save_patient_search)
        self.pushButton_7.clicked.connect(self.save_drug_search)
        self.pushButton_8.clicked.connect(self.save_genral_search)
        self.pushButton_17.clicked.connect(self.update_patient)
        self.pushButton_13.clicked.connect(self.save_all_drug_dose)
        self.pushButton_3.clicked.connect(self.add_Client)
        #self.pushButton.clicked.connect(self.add_drug_to_table)
        self.pushButton.clicked.connect(self.add_drug_to_table)
        self.lineEdit.editingFinished.connect(self.Check_Client_name)
        self.lineEdit.textChanged.connect(self.today_number)
        self.lineEdit_4.editingFinished.connect(self.check_drug_name)
        self.pushButton_4.clicked.connect(self.clear_data)
        self.pushButton_19.clicked.connect(self.clear_data)
        self.pushButton_20.clicked.connect(self.clear_data)
        self.pushButton_2.clicked.connect(self.handel_save_method)
        self.pushButton_9.clicked.connect(self.search_for_patient)
        self.pushButton_10.clicked.connect(self.search_for_drug)
        self.pushButton_11.clicked.connect(self.genral_search)
        self.pushButton_12.clicked.connect(self.genral_drug_dose)
        self.tabWidget.currentChanged.connect(self.tab_change_clear_data)
        self.tabWidget_2.currentChanged.connect(self.tab_change_clear_data_tab2)
        self.tabWidget_3.currentChanged.connect(self.tab_change_clear_data_tab3)
        self.comboBox_2.currentIndexChanged.connect(self.length_setter)
        self.lineEdit_12.returnPressed.connect(self.check_password)
        self.pushButton_14.clicked.connect(self.change_password)
        self.pushButton_15.clicked.connect(self.delete_item_from_table)
        #self.pushButton_16.clicked.connect(self.go_to_today)
        self.tableWidget.itemSelectionChanged.connect(self.get_Selected_row)
        self.tableWidget_6.itemSelectionChanged.connect(self.get_Selected_prescription_no)
        self.tableWidget_4.cellChanged.connect(self.update_check_status)
        self.tableWidget_8.cellChanged.connect(self.update_check_status1)
        self.pushButton_33.clicked.connect(self.Premedication_to_excel)
        self.pushButton_31.clicked.connect(self.premedication_fun)
        self.pushButton_30.clicked.connect(self.checked)
        self.pushButton_16.clicked.connect(self.checked_to_excel)
        self.pushButton_32.clicked.connect(self.number_of_prescription)
        self.pushButton_34.clicked.connect(self.createTable)
        
        self.pushButton_35.clicked.connect(self.print_row)


        

        #self.tableWidget_8.itemClicked.connect(self.ww1) # select rwo to uncheck
        self.tableWidget_4.itemClicked.connect(self.ww) # select rwo to uncheck
        ##########################################################
        ''' Back to Home'''

    def int_vaildator(self):
       # validator = QIntValidator(0, 10000, self)
        validator2 = QIntValidator(0, 9, self)
        self.lineEdit_6.setValidator(validator2)
        #self.lineEdit_11.setValidator(validator)

    def d_validator(self):
        validator = QDoubleValidator(0.0, 99.99, 2)
        self.lineEdit_5.setValidator(validator)

    def get_names_from_db(self):
        names_list.clear()
        self.cur.execute('''SELECT name FROM patient''')
        data = self.cur.fetchall()
        for item in data:
            names_list.append(item[0])

    def patient_names_for_main(self):
        completer = QCompleter(names_list)
        self.lineEdit.setCompleter(completer)

    def get_drug_from_db(self):
        drugs_list.clear()

        self.cur.execute('''SELECT drug_name FROM drugs''')
        data = self.cur.fetchall()
        for item in data:
            drugs_list.append(item[0])

    def add(self):
        completer = QCompleter(drugs_list)
        self.lineEdit_4.setCompleter(completer)

    def patient_names_for_report(self):
        namelist2 =[]
        for name in names_list:
            if name not in namelist2:  ## trying to prevent repeating  Names in general sereach
                namelist2.append(name)
            else:
                namelist2.append('')
                
        completer = QCompleter(namelist2)
        self.lineEdit_8.setCompleter(completer)
        self.lineEdit_17.setCompleter(completer)

    def drug_names_for_report(self):
        completer = QCompleter(drugs_list)
        self.lineEdit_9.setCompleter(completer)
        self.lineEdit_15.setCompleter(completer)

    def get_patient_number_from_db(self):
        names_list.clear()

        self.cur.execute('''SELECT number FROM patient''')
        data = self.cur.fetchall()
        for item in data:
            id_list.append(str(item[0]))

    def set_patient_number_for_report(self):
     #   idlist2 =[]
      #  for id in names_list:
       #     if id not in idlist2:  ## trying to prevent repeating  ID in general sereach
       #         idlist2.append(id)
       #     else:
       #         idlist2.append('')
        completer = QCompleter(id_list)
        self.lineEdit_11.setCompleter(completer)
        self.lineEdit_18.setCompleter(completer)

    def today_number(self):
      #  print("today_number function")
        date = datetime.date.today()
        self.cur.execute('''SELECT  COUNT( distinct patient_id) FROM prescription_no WHERE date= %s ''', (date,))
        data = self.cur.fetchone()
        self.label_25.setText(str(data[0] + 1))

    def tab_change_clear_data(self, i):
        if i == 0:
            self.lineEdit.setFocus()
        elif i == 1:
            self.lineEdit_12.setFocus()
        elif i == 2:
            self.lineEdit_8.setFocus()

        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.plainTextEdit.clear()
        self.lineEdit_7.clear()
        self.lineEdit_12.clear()
        self.set_today_date()
        self.tabWidget_3.hide()
        self.pushButton_17.hide()
        self.statusBar().showMessage('')
        check_add_drugs.clear()
        self.label_32.clear()
        self.label_25.clear()
        self.label_8.clear()

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

    def clear_data(self):#when you click search which function executes?
        self.lineEdit.setFocus()
        self.lineEdit_12.setFocus()
        self.lineEdit.clear()
        self.label_38.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.lineEdit_22.clear()
        self.plainTextEdit.clear()
        self.lineEdit_7.clear()
        self.lineEdit_12.clear()
        self.set_today_date()
        self.tabWidget_3.hide()
        self.pushButton_17.hide()
        self.statusBar().showMessage('')
        check_add_drugs.clear()
        self.label_32.clear()
        self.label_25.clear()
        self.lineEdit.setFocus()
        self.lineEdit_8.clear()
        self.lineEdit_11.clear()
        self.lineEdit_9.clear()
        self.label_8.clear()
        self.label_44.clear()

        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        while self.tableWidget_3.rowCount() > 0:
            self.tableWidget_3.removeRow(0)
      #  while self.tableWidget_4.rowCount() > 0:
       #     self.tableWidget_4.removeRow(0)
      #  while self.tableWidget_5.rowCount() > 0:
      #      self.tableWidget_5.removeRow(0)

        self.set_today_date()
        self.statusBar().showMessage('')

        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)

    def clear_drug_area(self):
        self.label_44.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.plainTextEdit.clear()
        self.lineEdit_6.clear()
        self.label_23.clear()

    def tab_change_clear_data_tab2(self, i):
        if i == 0:
            self.lineEdit_8.setFocus()
        elif i == 1:
            self.lineEdit_9.setFocus()
        #print(i," got focus")
        self.lineEdit_8.clear()
        self.lineEdit_11.clear()
        self.lineEdit_9.clear()
        while self.tableWidget_2.rowCount() > 0:
            self.tableWidget_2.removeRow(0)
        while self.tableWidget_3.rowCount() > 0:
            self.tableWidget_3.removeRow(0)
        #while self.tableWidget_4.rowCount() > 0:
           # self.tableWidget_4.removeRow(0)

       # if i==2:
       #     self.genral_search()
       # if i==3:
        #    self.premedication_fun()
       # if i==0:
       #     self.search_for_patient()
      #  if i==1:
       #     self.search_for_drug()
       # if i==4:
        #    self.genral_drug_dose()
      #  while self.tableWidget_5.rowCount() > 0:
     #       self.tableWidget_5.removeRow(0)
        #self.set_today_date()
        self.statusBar().showMessage('')
        # if i == 2 :
        #     self.get_genral_search_auto()

    def tab_change_clear_data_tab3(self, i):
        if i == 0:
            self.lineEdit_7.setFocus()
        elif i == 1:
            self.lineEdit_15.setFocus()

    def check_password(self):
        user_password = self.lineEdit_12.text()
        self.cur.execute('''SELECT password FROM password ''')
        password = self.cur.fetchone()
        print("password=",password)
        if password:
            if user_password == password[0]:
                self.tabWidget_3.show()
                self.lineEdit_7.setFocus()
                self.lineEdit_12.clear()

            else:
                message = QMessageBox.warning(self, "Log In ", "Password Is Not Valid !                  ",
                                              QMessageBox.Ok)
                self.lineEdit_12.setFocus()
                self.lineEdit_12.clear()

    def change_password(self):
        passwprd_1 = self.lineEdit_13.text()
        passwprd_2 = self.lineEdit_14.text()
        if passwprd_1 == passwprd_2:
            self.cur.execute('''UPDATE password SET password =%s WHERE id=%s ''', (passwprd_1, 1))
            self.db.commit()
            self.lineEdit_13.clear()
            self.lineEdit_14.clear()
            self.statusBar().showMessage("Password Updated Successfuly",5000)
            self.tabWidget_3.setCurrentIndex(0)
        else:
            message = QMessageBox.warning(self, "Change Password ", "Passwords Is Not Equal !                  ",
                                          QMessageBox.Ok)
            self.lineEdit_13.clear()
            self.lineEdit_14.clear()
            self.lineEdit_13.setFocus()

    ##########################################################################################################
    #############################
    '''Add Drug '''

    ############################
    def add_drug(self):
        main_category = self.comboBox_2.currentIndex()
        drug_name = self.lineEdit_7.text()
        if drug_name.strip(" ") != "":
            if drug_name not in drugs_list:
                self.cur.execute('''INSERT INTO drugs (drug_name , main_category ) VALUES (%s,%s)''',
                                 (drug_name, main_category))
                self.db.commit()
                self.statusBar().showMessage("Drug Added Successfuly",5000)
                self.lineEdit_7.clear()
                self.Add_fulid_to_combobox()
                self.get_drug_from_db()
                self.add()
                self.drug_names_for_report()
            else:
                message = QMessageBox.warning(self, "Add Drug ", "Drug Already Exist !                  ",
                                              QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.lineEdit_7.setFocus()
        else:
            self.statusBar().showMessage("Enter Valid Data",5000)

    def search_for_drug_to_update(self):
        drug_name = self.lineEdit_15.text()
        main_category = self.comboBox_4.currentIndex()
        if drug_name.strip(" ") != '':
            try:
                self.cur.execute('''SELECT id FROM drugs WHERE drug_name=%s AND main_category =%s''',
                                 (drug_name, main_category))
                drug_id = self.cur.fetchone()
                self.label_5.setText(str(drug_id[0]))
            except Exception as m:
                pass
                print("error line 422")
    def update_drug(self):
        if self.label_5.text() != '':
            drug_id = self.label_5.text()
            main_category = self.comboBox_5.currentIndex()
            new_drug_name = self.lineEdit_16.text()
            if new_drug_name.strip(" ") != '':
                self.cur.execute('''UPDATE drugs SET drug_name=%s , main_category=%s WHERE id =%s ''',
                                 (new_drug_name, main_category, drug_id))
                self.db.commit()
                self.lineEdit_15.clear()
                self.label_5.clear()
                self.lineEdit_16.clear()
                self.statusBar().showMessage('Drug Updated Successfully',5000)
                self.lineEdit_15.setFocus()
                self.Add_fulid_to_combobox()
                self.get_drug_from_db()
                self.add()
                self.drug_names_for_report()

            else:
                self.statusBar().showMessage('Drug Name Is Not Valid',5000)

    def length_setter(self):

        if self.comboBox_2.currentIndex() == 2:
            self.lineEdit_7.setMaxLength(12)
        else:
            self.lineEdit_7.setMaxLength(25)

    ##########################################################################################################
    #############################
    '''Add Client '''

    ############################
    def add_Client(self):
        if self.label_8.text() == "":
            patient_Name = self.lineEdit.text()
            patient_id = self.lineEdit_2.text()
            phone = self.lineEdit_3.text()
            date = datetime.date.today()
            if patient_Name.strip(" ") == '':
                message = QMessageBox.warning (self, "Add patient ", "patient Name Is Required                  ",
                                              QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.lineEdit.setFocus()
            elif patient_id.strip(" ") == '':
                message = QMessageBox.warning(self, "Add patient ", "patient ID Is Required                  ",
                                              QMessageBox.Ok)
                if message == QMessageBox.Ok:
                    self.lineEdit_2.setFocus()
            else:
                if patient_Name.strip(" ") != "" and patient_id.strip(" ") != "":
                    self.cur.execute('''SELECT name,phone,number from patient where name=%s and phone=%s and number=%s''', (patient_Name, phone, patient_id, ))
                    foundornot=self.cur.fetchone()
                   # print("foundornot=",foundornot)
                    if foundornot:
                        QMessageBox.warning(self, "Add patient ", "patient already in database!", QMessageBox.Ok)
                        return
                    self.cur.execute('''INSERT INTO patient ( name , phone , number,add_date ) VALUES (%s,%s,%s,%s)''',
                                     (patient_Name, phone, patient_id, date))
                    self.db.commit()
                    message = QMessageBox.question(self, "Add patient ", "patient Added Successfuly                 ",
                                                  QMessageBox.Ok)

                    self.pushButton_2.setEnabled(True) # F10
                    self.cur.execute('''SELECT id FROM patient WHERE name = %s AND number =%s ''',
                                     (patient_Name, patient_id))
                    patient_number = self.cur.fetchone()
                    self.label_8.setText(str(patient_number[0]))
                    self.get_names_from_db()
                    self.patient_names_for_main()
                    self.lineEdit_4.setFocus()
                    self.pushButton_17.show()
                    self.lineEdit_6.setText('0')
                    self.show_daily_statics()


                else:
                    self.statusBar().showMessage('Data Is Not Valid',5000)

        ##########################################################################################################
        #############################
        '''Check Client name from database '''

    ############################
    def Check_Client_name(self):
        """  deletes prescription_detail where prescription_no==NULL 
             checks if patient exists 
             if yes sets data labels and calls check_patient_old_prescription
        """
      #  print("Check_Client_name function")
        self.cur.execute('''DELETE FROM prescription_detail WHERE prescription_no IS NUll''')
        self.db.commit()
        patient_Name = self.lineEdit.text()
        self.cur.execute('''SELECT * FROM patient where name =%s ''', (patient_Name,))
        patient = self.cur.fetchone()
        if patient:
          #  print("patient found!")
            patient_id = patient[0]
            patient_Name = patient[1]
            patient_number = patient[2]
            phone = patient[3]
            self.lineEdit.setText(str(patient_Name))
            self.lineEdit_2.setText(str(patient_number))
            self.lineEdit_3.setText(str(phone))
            self.label_8.setText(str(patient_id))
            self.lineEdit_6.setText('0')
            self.pushButton_2.setEnabled(True)
            self.lineEdit_4.setFocus()
            self.pushButton_17.show()
            self.check_patient_old_prescription()
        #else:
           # print("patient not found")
           # self.lineEdit_3.clear()
          #  self.lineEdit_2.clear()
           # self.label_8.clear()
           # self.lineEdit_6.clear()
           # self.label_38.clear()
           # self.pushButton_17.hide()
           # self.pushButton_2.setEnabled(False)
          #  self.tableWidget.clearSelection()
          # while self.tableWidget.rowCount() > 0:
           #     self.tableWidget.removeRow(0)
             #   self.tableWidget.clearSelection()

    def update_patient(self):
        patient_id = self.label_8.text()
        patient_Name = self.lineEdit.text()
        patient_number = self.lineEdit_2.text()
        phone = self.lineEdit_3.text()
        self.cur.execute('''UPDATE patient SET name=%s , number=%s , phone=%s WHERE id =%s ''',
                         (patient_Name, patient_number, phone, patient_id))
        self.db.commit()
        message = QMessageBox.warning(self, "Add patient ", "patient Updated Successfully                 ",
                                      QMessageBox.Ok)

    ##########################################################################################################
    #############################
    '''Add drug to table '''

    ############################
    def add_drug_to_table(self):

        drug = self.lineEdit_4.text()
        dose = self.lineEdit_5.text()
        volume = self.lineEdit_6.text()
        note = self.plainTextEdit.toPlainText()
        fluid_name = self.comboBox.currentText()
        date = datetime.date.today()
        prescription_no = self.label_32.text()
        #check data entry
        if drug.strip(" ") == '':
            message = QMessageBox.warning(self, "Add Drug ", "Drug Field Is Required                  ", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.lineEdit_4.setFocus()
            return
        elif dose.strip(" ") == '':
            message = QMessageBox.warning(self, "Add Drug ", "Dose Field Is Required                  ", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.lineEdit_5.setFocus()
            return
        elif volume.strip(" ") == '':
            message = QMessageBox.warning(self, "Add Drug ", "Volume Field Is Required                  ", QMessageBox.Ok)
            if message == QMessageBox.Ok:
                self.lineEdit_6.setFocus()
                self.lineEdit_5.setFocus()
            return
        #data validates
        a=self.getdrug()
        #print("a---->",a)
        foundValue=False
        if a:
            for index,x in enumerate(a):
                #print("x=",x," drug=",drug)
                if drug == x[0]:
                   # print("exists")
                   # message = QMessageBox.question (self, "Add Drug("+x[0]+") ", "Drug exists do you want to modify?",  QMessageBox.Yes, QMessageBox.No)
                  #  if message == QMessageBox.Yes:
                    temp=([drug,dose,fluid_name,volume,note])
                    a[index]=temp
                    self.statusBar().showMessage("Drug Is Updated. ",5000)
                    foundValue=True
                    break
        if not foundValue:
           # print("does not exist")
            a.append([drug,dose,fluid_name,volume,note])
        self.retrive_prescription_detail(a)
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.plainTextEdit.clear()
        self.lineEdit_6.clear()
        self.label_23.clear()
        self.lineEdit_6.setText('0')
        self.lineEdit_4.setFocus()


    #def add_drug_to_table1(self):
    #    print("add_drug_to_table function")
     #   drug = self.label_23.text()
    #    dose = self.lineEdit_5.text()
    #    volume = self.lineEdit_6.text()
    ##    note = self.plainTextEdit.text()
    #    date = datetime.date.today()
    #    prescription_no = self.label_32.text()
    #    #check data entry
    #    if drug.strip(" ") == '':
    #        message = QMessageBox.warning(self, "Add Drug ", "Drug Field Is Required                  ", QMessageBox.Ok)
    #        if message == QMessageBox.Ok:
    #            self.lineEdit_4.setFocus()
    #    elif dose.strip(" ") == '':
    #        message = QMessageBox.warning(self, "Add Drug ", "Dose Field Is Required                  ", QMessageBox.Ok)
    #        if message == QMessageBox.Ok:
    #            self.lineEdit_5.setFocus()
    #    elif volume.strip(" ") == '':
    #        message = QMessageBox.warning(self, "Add Drug ", "Volume Field Is Required                  ", QMessageBox.Ok)
    #3        if message == QMessageBox.Ok:
    #            self.lineEdit_6.setFocus()
    #            self.lineEdit_5.setFocus()
    #    else:#data validates
    #        if self.label_44.text() != '':#????exists in prescription_detail
    #            print("label44=",self.label_44.text())
    #            if drug in check_add_drugs:#Drug in list in table
    #                message = QMessageBox.warning(self, "Add Drug ", "Drug  Already Exists                   ", QMessageBox.Ok)
    #                if message == QMessageBox.Ok:
    #                    self.lineEdit_4.setFocus()
    #            else:#Drug not is list is not in table
    #                fluid_name = self.comboBox.currentText()
    #                record_id = self.label_44.text()
    #                print("record_id",record_id)
    #                self.cur.execute('''SELECT id FROM drugs WHERE drug_name=%s ''', (fluid_name,))
    #                fluid_id = self.cur.fetchone()
    #                #self.cur.execute('''UPDATE prescription_detail SET drug = %s , dose= %s , fluid= %s , volume= %s , note= %s 
                    #
    #                #                    WHERE id =%s ''', (drug, dose, fluid_id[0], volume, note, record_id))
    #                a=self.getdrug()
    #                print("---a=",a)
    #                a.append([drug,dose,fluid_name,volume,note])
    #                self.retrive_prescription_detail(a)
    #                self.label_44.clear()
    #                self.lineEdit_4.clear()
    #                self.lineEdit_5.clear()
    #                self.plainTextEdit.clear()
    #                self.lineEdit_6.clear()
    #                self.label_23.clear()
                    #self.db.commit()
    #                check_add_drugs.append(drug)
    #                if prescription_no == '':
    #                    self.retrive_prescription_detail()
    #                else:
    #                    self.retrive_old_prescription_detail()
    #                self.statusBar().showMessage("Drug Is Updated. ")
    #                self.lineEdit_4.setFocus()
    #        else:#self.label_44.text()==""  new prescription
    #            print("label44=",self.label_44.text())
    #            if drug in check_add_drugs:#drug in list table
    #                message = QMessageBox.warning(self, "Add Drug ", "Drug is Already Exist                   ",
    #                                              QMessageBox.Ok)
    #                if message == QMessageBox.Ok:
    #                    self.lineEdit_4.setFocus()
    #            else:#drug not in list
    #                fluid_name = self.comboBox.currentText()
    #                self.cur.execute('''SELECT id FROM drugs WHERE drug_name=%s ''', (fluid_name,))
    #                fluid_id = self.cur.fetchone()
    #                if self.label_32.text() != "":#prescription_no exists  add to old prescription ???
    #                    self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,prescription_no ,date)
    #                                        VALUES (%s,%s,%s,%s,%s,%s,%s)
    #                                    ''', (drug, dose, fluid_id[0], volume, note, prescription_no, date))
    #                    self.update_dose(drug, dose, fluid_id[0], volume)
    #                else:
    #                    self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,date)
    #                                        VALUES (%s,%s,%s,%s,%s,%s)
    #                                    ''', (drug, dose, fluid_id[0], volume, note, date))
    #                    self.update_dose(drug, dose, fluid_id[0], volume)
    #                check_add_drugs.append(drug)
    #                self.lineEdit_4.clear()
    #                self.lineEdit_5.clear()
    #                self.plainTextEdit.clear()
    #                self.label_23.clear()
    #                self.lineEdit_6.setText('1')
    #                if self.label_32.text() != "":
    #                    self.retrive_old_prescription_detail()
    #                else:
    #                    self.retrive_prescription_detail()
    #                self.lineEdit_4.setFocus()

    def get_Selected_row(self):
        try:
            if self.tableWidget.rowCount() > 0:
                current_row = self.tableWidget.currentRow()
                item = self.tableWidget.item(current_row, 0).text()
                self.pushButton_15.show()

                return item
            else:
                message = QMessageBox.warning(self, "Drug ", "No Drug Selected                  ",
                                              QMessageBox.Ok)
        except Exception as m:
            print(m,"636")

    def delete_item_from_table(self):
        try:
            prescription_no = self.label_32.text()
            item_name = self.get_Selected_row()
            #print("item_name=",item_name)
            if item_name:
                self.cur.execute('''SELECT id FROM drugs WHERE drug_name =%s ''', (item_name,))
                item_id = self.cur.fetchone()
              #  print("item_id=",item_id)
                if str(item_id[0]) in check_add_drugs:check_add_drugs.remove(str(item_id[0]))
                self.tableWidget.removeRow(self.tableWidget.currentRow())
                #if prescription_no:
                #    self.cur.execute('''DELETE FROM prescription_detail WHERE drug = %s AND prescription_no =%s  ''',
                #                     (item_id[0], prescription_no))
                #    self.retrive_old_prescription_detail()
                #    self.get_drug_from_old_prescription()
                #else:
                #    self.cur.execute(
                #        '''DELETE FROM prescription_detail WHERE drug = %s AND prescription_no IS NULL  ''',
                #        (item_id[0],))
                #    self.retrive_prescription_detail()
                #self.db.commit()
                self.pushButton_15.hide()
                self.statusBar().showMessage("deleted",5000)

            self.tableWidget.clearSelection()

        except Exception as m:
            print(m,"663")

    def retrive_prescription_detail(self,A=[]):
        #self.cur.execute(
        #    '''SELECT drug,dose,fluid,volume,note FROM prescription_detail as p WHERE prescription_no IS NULL''')
        self.tableWidget.clearSelection()
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
            self.tableWidget.clearSelection()
        prescription_detail = A   #self.cur.fetchall()
        for row_number, items in enumerate(prescription_detail):
            self.tableWidget.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 0:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    if drug_name:
                        cell = QTableWidgetItem(str(drug_name[0]))
                    else:
                        cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                elif column_number == 2:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    if drug_name:
                        cell = QTableWidgetItem(str(drug_name[0]))
                    else:
                        cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
    def get_old_prescription(self):#function is not used
       # print("get_old_prescription function")
        prescription_number = self.label_32.text()
        #drug,dose,fluid,volume,note 
        self.cur.execute('''SELECT * FROM prescription_detail WHERE prescription_no = %s ''',
                         (prescription_number,))
        prescription_detail = self.cur.fetchall()
        return prescription_detail

    def show_drugs_on_table(self,prescription_detail):
        #print("show_drugs_on_table")
        #prescription_detail=prescription_detail[1:6] #drug,dose,fluid,volume,note 
        self.tableWidget.clearSelection()
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
            self.tableWidget.clearSelection()
        for row_number, items in enumerate(prescription_detail):
            self.tableWidget.insertRow(row_number)
            for column_number, item in enumerate(items[1:6]):
                if column_number == 0:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                elif column_number == 2:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
        self.statusBar().showMessage(" ")
    
    def store_in_database(self,prescription_det):
       # print("store_database function")
        for drug in prescription_det:#here you add with no  prescription_no id you leave it NULL and here the problem starts
            self.cur.execute('''INSERT IGNORE INTO prescription_detail (id,drug , dose , fluid , volume , note ,date,is_checked,presciption_no)
                                                      VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                                  ''', (drug[0], drug[1], drug[2], drug[3], drug[4], drug[5], drug[6], drug[7], drug[8],))
          

    def retrive_old_prescription_detail(self):
        """
        data--> tablewidget
        """
       # print("retrive_old_prescription_detail function")
        prescription_number = self.label_32.text()
        self.cur.execute('''SELECT drug,dose,fluid,volume,note FROM prescription_detail WHERE prescription_no = %s ''',
                         (prescription_number,))
        self.tableWidget.clearSelection()
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
            self.tableWidget.clearSelection()
        prescription_detail = self.cur.fetchall()
       # print("-------------->prescription_detail=",prescription_detail)
        for row_number, items in enumerate(prescription_detail):
            self.tableWidget.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 0:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                elif column_number == 2:
                    self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                    drug_name = self.cur.fetchone()
                    cell = QTableWidgetItem(str(drug_name[0]))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget.setItem(row_number, column_number, cell)
        self.statusBar().showMessage("last prescription ")

    def Add_drug_with_old_prescription(self):
       # print("Add drug old prescription function")
        if self.tableWidget.rowCount() <= 0:
            self.statusBar().showMessage("There Is Nothing To Save",5000)
        else:
            self.db.commit()
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            self.clear_data()
            self.statusBar().showMessage("Prescription Saved Successfully",5000)
            self.lineEdit.setFocus()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.plainTextEdit.clear()
            self.label_23.clear()
            self.pushButton_17.hide()
            self.lineEdit_6.setText('0')
            self.show_daily_statics()
            check_add_drugs.clear()
            self.label_38.clear()

    def add_drug_with_new_prescription(self):
        #print("add drug with new prescription  function")
        patient_id = self.label_8.text()  # main_prescription
        date = datetime.date.today()  # main_prescription
        if self.tableWidget.rowCount() <= 0:
            self.statusBar().showMessage("There Is No Thing To Save",5000)
        else:
            self.cur.execute('''INSERT INTO prescription_no (patient_id,date) VALUES (%s,%s)''', (patient_id, date))
            prescription_no = self.cur.lastrowid
            self.cur.execute('''UPDATE prescription_detail SET prescription_no =%s WHERE prescription_no IS NULL ''',
                             (prescription_no,))
            self.db.commit()
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            self.clear_data()
            self.statusBar().showMessage("Prescription Saved Successfully",5000)
            self.lineEdit.setFocus()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.plainTextEdit.clear()
            self.label_23.clear()
            self.pushButton_17.hide()
            self.lineEdit_6.setText('0')
            self.show_daily_statics()
            check_add_drugs.clear()
            self.label_38.clear()

    def update_dose(self, drug, dose, fluid, volume):
        self.cur.execute('''UPDATE drugs set drug_outgoing = drug_outgoing +%s WHERE id = %s ''', (dose, drug))
        self.cur.execute('''UPDATE drugs set drug_outgoing = drug_outgoing +%s WHERE id = %s ''', (volume, fluid))
        self.db.commit()

    def check_patient_old_prescription(self):
       # print("check_patient_old+prescription function.................")
        """finds max(id) prescription_no and finds date ,puts date to label 
        puts id to label32  
        calls retrive_old_prescription_detail and get_drug_from_old_prescription
        """
        patient_id = self.label_8.text()
        self.cur.execute('''SELECT MAX(id) FROM prescription_no WHERE patient_id = %s ''', (patient_id,))
        prescription_number = self.cur.fetchone()
        if prescription_number[0] is not None:
            self.cur.execute('''SELECT date FROM prescription_no WHERE id = %s ''', (prescription_number[0],))
            date = self.cur.fetchone()
            self.label_38.setText(str(date[0]))
           # print("label38=",self.label_38.text())
            result = prescription_number[0]
            self.label_32.setText(str(result))
         #   print("labe32=",self.label_32.text())
            self.retrive_old_prescription_detail()#data -->tablewidgets for prescription_no
            self.get_drug_from_old_prescription()#list of drug_ids for drug_names on tablewidget

   # def handel_save_method1(self):#xxxx
    #    prescription_number = self.label_32.text()
   #     if prescription_number:
            #print("if")
    #        self.Add_drug_with_old_prescription()
    #        self.get_names_from_db()
    #        self.patient_names_for_main()
    #        self.patient_names_for_report()
     #   else:
    #        #print("else")
    #        self.add_drug_with_new_prescription()
    #        self.get_names_from_db()
    #        self.patient_names_for_main()
    #        self.patient_names_for_report()
    #    self.lineEdit.setFocus()


    def handel_save_method(self):   # F10 button 
        a=self.getdrug()
        date = datetime.date.today()
        patient_id=self.label_8.text()

        if a and patient_id:
            self.cur.execute('''select id FROM prescription_no where patient_id=%s and date=%s''',(patient_id,date,))
            prescription_det = self.cur.fetchall()
            for x in prescription_det:
                self.cur.execute('''DELETE FROM prescription_detail where prescription_no=%s''',(x[0],))
            self.cur.execute('''DELETE FROM prescription_no where patient_id=%s and date=%s''',(patient_id,date,))
            #insert into prescription_no values
            self.cur.execute('''INSERT INTO prescription_no (patient_id,date) VALUES (%s,%s)''', (patient_id, date))
            prescription_no = self.cur.lastrowid
           # print("prescription_no=",prescription_no)
            for x in a:
               # print(x)
                self.cur.execute('''SELECT id FROM drugs where drug_name =%s ''', (x[0],))
                drug_id = self.cur.fetchone()
               # print(">",drug_id[0])
                dose=x[1]
                self.cur.execute('''SELECT id FROM drugs where drug_name =%s ''', (x[2],))
                fluid_id = self.cur.fetchone()
             #   print(">",fluid_id[0])
                volume=x[3]
                note=x[4]
                #insert into prescription_detail values
                self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,prescription_no ,date) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                                                                                 (drug_id[0], dose, fluid_id[0], volume, note, prescription_no, date,))
            self.db.commit()
            self.lineEdit.setFocus()
            
            self.statusBar().showMessage("prescription saved",5000)

            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            #self.label_32.clear()
            #self.label_38.clear()
            #self.lineEdit_2.clear()
            #self.lineEdit_3.clear()
            #self.lineEdit.clear()
            #self.label_25.clear()
            #self.pushButton_17.hide()
            #self.lineEdit_6.clear()
            self.lineEdit.clear()
            self.label_38.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.plainTextEdit.clear()
            self.lineEdit_7.clear()
            self.lineEdit_12.clear()
            self.set_today_date()
            self.tabWidget_3.hide()
            self.pushButton_17.hide()
            check_add_drugs.clear()
            self.label_32.clear()
            self.label_25.clear()
            self.lineEdit_8.clear()
            self.lineEdit_11.clear()
            self.lineEdit_9.clear()
            self.label_8.clear()
            self.label_44.clear()
            
            #check_add_drugs.clear()
        

    def getdrug(self):
       # print("creates a list of drugs based on tablewidget drug names")
        list_drugs=[]
       # print("get_drug_list function")
        for currentRow in range(self.tableWidget.rowCount()):
            temp=[]
            for currentColumn in range(self.tableWidget.columnCount()):
                temp.append(self.tableWidget.item(currentRow, currentColumn).text())
            list_drugs.append(temp)
        return list_drugs


    def new_prescription_for_patient_has_old_one(self):#keeps in tablewidget old prescription with today date
        message = QMessageBox.question (self, "New prescription  ", "All Drug Will Be Copy?                  ", QMessageBox.Yes, QMessageBox.No)
        if message == QMessageBox.Yes:
            self.statusBar().showMessage("")
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            prescription_number = self.label_32.text()
            date = datetime.date.today()
            self.cur.execute(
                '''SELECT drug , dose , fluid , volume , note FROM prescription_detail WHERE prescription_no =%s ''', (prescription_number,))
            prescription_det = self.cur.fetchall()#you must combine it with te other code to do it at the same time without the update.ok? ok
            for drug in prescription_det:#here you add with no  prescription_no id you leave it NULL and here the problem starts
            #    self.cur.execute('''INSERT INTO prescription_detail (drug , dose , fluid , volume , note ,date)
            #                                          VALUES (%s,%s,%s,%s,%s,%s)
            #                                      ''', (drug[0], drug[1], drug[2], drug[3], drug[4], date))#here you must have prescription_no.after you combine you will have it.ok?ok.happy coding.cu
                # self.update_dose(drug[0], drug[1], drug[2], drug[3], drug[4])
                check_add_drugs.append(drug)
            #self.cur.execute(
            #    '''CREATE TABLE %s SELECT drug , dose , fluid , volume , note FROM prescription_detail WHERE prescription_no =%s ''', (prescription_number,))
           # print("prescription_det=",prescription_det)
            self.retrive_prescription_detail(prescription_det)
            self.getdrug()
          #  print("--->a",ga)
            self.lineEdit_4.setFocus()
            self.label_32.clear()
            self.label_38.clear()

        if message == QMessageBox.No:#deletes tablewidget clears labels data
            self.statusBar().showMessage("")
            self.lineEdit_4.setFocus()
            self.tableWidget.clearSelection()
            while self.tableWidget.rowCount() > 0:
                self.tableWidget.removeRow(0)
                self.tableWidget.clearSelection()
            self.label_32.clear()
            self.label_38.clear()
            check_add_drugs.clear()
        self.lineEdit_4.setFocus()




    def get_drug_from_old_prescription(self):
        """
        creates a list of drug ids based on tablewidget drug names
        """
      #  print("get_drug_from_old_prescription function")
        check_add_drugs.clear()
        for currentRow in range(self.tableWidget.rowCount()):
            for currentColumn in range(self.tableWidget.columnCount()):
                try:
                    if currentColumn == 0:
                        drug_name = str(self.tableWidget.item(currentRow, currentColumn).text())
                        self.cur.execute('''SELECT id FROM drugs where drug_name =%s ''', (drug_name,))
                        drug_id = self.cur.fetchone()
                        check_add_drugs.append(str(drug_id[0]))


                except AttributeError as x:
                    print(x,"855")
                    pass

    ##########################################################################################################
    #############################
    #     '''Check drug name from database '''
    ############################
    def check_drug_name(self):
        drug = self.lineEdit_4.text()
        if drug.strip(" ") != "":
            self.cur.execute('''SELECT id FROM drugs where drug_name =%s ''', (drug,))
            drug_id = self.cur.fetchone()

            try:
                if drug_id[0]:
                    self.label_23.setText(str(drug_id[0]))
            except Exception as m:
                print(m,"872")
                pass

    ##########################################################################################################
    #############################
    '''Add fulid to combobox  '''

    ############################
    def Add_fulid_to_combobox(self):
        sql='''SELECT drug_name FROM drugs WHERE main_category=2 '''
        self.cur.execute(sql)
        drug_name = self.cur.fetchall()
        self.comboBox.clear()
        for drug in drug_name:
            self.comboBox.addItem(drug[0])

    ##########################################################################################################
    #############################
    ''' modify drug '''

    ############################
    def get_modify_drug(self):
       # print("get_modify_drug function")
        drug_name = self.get_Selected_row()
        dose=self.tableWidget.item(self.tableWidget.currentRow(),1).text()
        fluid=self.tableWidget.item(self.tableWidget.currentRow(),2).text()
        volume=self.tableWidget.item(self.tableWidget.currentRow(),3).text()
        note=self.tableWidget.item(self.tableWidget.currentRow(),4).text()
        if drug_name:
            self.cur.execute('''SELECT id FROM drugs WHERE drug_name = %s ''', (drug_name,))
            drug_id = self.cur.fetchone()
            #check_add_drugs.remove(str(drug_id[0]))
            self.label_44.setText(str(datetime.date.today()))
           # print("label44=",self.label_44.text())
            self.lineEdit_4.setText(drug_name)
            self.lineEdit_5.setText(dose)#dose
            self.lineEdit_6.setText(str(volume))#volume
            self.plainTextEdit.setPlainText(note)#note
            self.label_23.setText(drug_name)#drug name
            #self.cur.execute('''SELECT drug_name FROm drugs WHERE id = %s ''', (fluid,))
            #fluid_name = self.cur.fetchone()
            #print("fuild=",fluid)
            #print("fluid name=",fluid_name)
            all_item = {}
            for i in range(self.comboBox.count()):
                all_item[i] = self.comboBox.itemText(i)
            for key, value in all_item.items():
                if value == fluid:
                    self.comboBox.setCurrentIndex(key)


   # def old_get_modify_drug(self):
    #    print("get_modify_drug function.....")
    #    self.get_drug_from_old_prescription()
     #   drug_name = self.get_Selected_row()
    #    prescription_no = self.label_32.text()
    #    if drug_name and prescription_no:
#
    #        self.cur.execute('''SELECT id FROM drugs WHERE drug_name = %s ''', (drug_name,))
     #       drug_id = self.cur.fetchone()
    #        check_add_drugs.remove(str(drug_id[0]))
     #       self.cur.execute('''SELECT id , drug , dose , fluid,volume , note FROM prescription_detail 
    #                            WHERE drug = %s AND prescription_no = %s ''', (drug_id[0], prescription_no))
    #        data = self.cur.fetchone()
    #        self.label_44.setText(str(data[0]))
     #       print("label44=",self.label_44.text())
    #        self.lineEdit_4.setText(drug_name)
    #        self.lineEdit_5.setText(str(data[2]))
    #        self.lineEdit_6.setText(str(data[4]))
    #        self.plainTextEdit.setText(str(data[5]))
     #       self.label_23.setText(str(data[1]))
    #        self.cur.execute('''SELECT drug_name FROm drugs WHERE id = %s ''', (data[3],))
   #         fluid_name = self.cur.fetchone()
   #         all_item = {}
   #         for i in range(self.comboBox.count()):
   #             all_item[i] = self.comboBox.itemText(i)
   #         for key, value in all_item.items():
   #             if value == fluid_name[0]:
   #                 self.comboBox.setCurrentIndex(key)
   #     elif drug_name and prescription_no == '':
   #         self.cur.execute('''SELECT id FROM drugs WHERE drug_name = %s ''', (drug_name,))
   #         drug_id = self.cur.fetchone()
   #         check_add_drugs.remove(str(drug_id[0]))
            #self.cur.execute('''SELECT id , drug , dose , fluid,volume , note FROM prescription_detail 
            #                    WHERE drug = %s AND prescription_no IS NULL ''', (drug_id[0],))
            #data = self.cur.fetchone()
            #self.label_44.setText(str(data[0]))
    #        self.label_44.setText(datetime.date.today())
    #        print("label44=",self.label_44.text())
    #        self.lineEdit_4.setText(drug_name)
    #        self.lineEdit_5.setText(str(data[2]))
    #        self.lineEdit_6.setText(str(data[4]))
     #       self.plainTextEdit.setText(str(data[5]))
    #        self.label_23.setText(str(data[1]))
    #        self.cur.execute('''SELECT drug_name FROm drugs WHERE id = %s ''', (data[3],))
    #        fluid_name = self.cur.fetchone()
    #        all_item = {}
    #        for i in range(self.comboBox.count()):
   #             all_item[i] = self.comboBox.itemText(i)
    #        for key, value in all_item.items():
    #            if value == fluid_name[0]:
     #               self.comboBox.setCurrentIndex(key)

    ##########################################################################################################
    #############################
    ''' Patient Mangement '''

    ############################
    def clear_patient_mang_data(self):
        self.lineEdit_17.clear()
        self.lineEdit_18.clear()
        self.label_41.clear()
        while self.tableWidget_6.rowCount() > 0:
            self.tableWidget_6.removeRow(0)
            self.tableWidget_6.clearSelection()
        while self.tableWidget_7.rowCount() > 0:
            self.tableWidget_7.removeRow(0)
            self.tableWidget_7.clearSelection()

    def get_patient_data_for_mangment(self):
        patient_name = self.lineEdit_17.text()
        patient_num = self.lineEdit_18.text()
        if patient_name.strip(" ") != "":
            self.cur.execute('''SELECT id , number FROM patient WHERE name = %s ''', (patient_name,))
            patient_id = self.cur.fetchone()
            if patient_id is not None:
                self.label_41.setText(str(patient_id[0]))
                self.lineEdit_18.setText(str(patient_id[1]))
                self.get_patient_prescription_no_for_mang()
            else:
                self.statusBar().showMessage("No Data Found For This Name ",5000)

        elif patient_num.strip(" ") != "":
            self.cur.execute('''SELECT id , name FROM patient WHERE number = %s ''', (patient_num,))
            patient_id = self.cur.fetchone()
            if patient_id is not None:
                self.lineEdit_17.setText(str(patient_id[1]))
                self.label_41.setText(str(patient_id[0]))
                self.get_patient_prescription_no_for_mang()

            else:
                self.statusBar().showMessage("No Data Found For This Id",5000)

    def get_patient_prescription_no_for_mang(self):
        patient_id = self.label_41.text()
        if self.label_41.text() != '':
            self.cur.execute('''SELECT id , date FROM prescription_no WHERE patient_id =%s ''', (patient_id,))
            prescription_no = self.cur.fetchall()
            self.tableWidget_6.clearSelection()
            while self.tableWidget_6.rowCount() > 0:
                self.tableWidget_6.removeRow(0)
                self.tableWidget_6.clearSelection()
            for row_number, items in enumerate(prescription_no):
                self.tableWidget_6.insertRow(row_number)
                for column_number, item in enumerate(items):
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_6.setItem(row_number, column_number, cell)

    def get_Selected_prescription_no(self):
        try:
            if self.tableWidget_6.rowCount() > 0:
                current_row = self.tableWidget_6.currentRow()
                item = self.tableWidget_6.item(current_row, 0).text()
                self.cur.execute(
                    '''SELECT drug , dose , fluid,volume,note FROM prescription_detail WHERE prescription_no =%s ''',
                    (item,))
                self.tableWidget_7.clearSelection()
                rescription_detail = self.cur.fetchall()
                self.tableWidget_7.clearSelection()
                while self.tableWidget_7.rowCount() > 0:
                    self.tableWidget_7.removeRow(0)
                    self.tableWidget_7.clearSelection()
                for row_number, items in enumerate(rescription_detail):
                    self.tableWidget_7.insertRow(row_number)
                    for column_number, item in enumerate(items):
                        if column_number == 0:
                            self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                            drug_name = self.cur.fetchone()
                            cell = QTableWidgetItem(str(drug_name[0]))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            self.tableWidget_7.setItem(row_number, column_number, cell)
                        elif column_number == 2:
                            self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                            drug_name = self.cur.fetchone()
                            cell = QTableWidgetItem(str(drug_name[0]))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            self.tableWidget_7.setItem(row_number, column_number, cell)
                        else:

                            cell = QTableWidgetItem(str(item))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            self.tableWidget_7.setItem(row_number, column_number, cell)

        except Exception as m:
            print(m,"1049")

    def delete_patient_visit(self):
        if self.tableWidget_6.rowCount() > 0:
            current_row = self.tableWidget_6.currentRow()
            if current_row != -1:
                item = self.tableWidget_6.item(current_row, 0).text()
                message = QMessageBox.warning(self , "Delete Visit ",
                                              "Are You Sure To Delete Visit !                  ",
                                              QMessageBox.Yes, QMessageBox.No)
                if message == QMessageBox.Yes:
                    self.cur.execute('''DELETE FROM prescription_detail WHERE prescription_no = %s ''', (item,))
                    self.cur.execute('''DELETE FROM prescription_no WHERE id = %s ''', (item,))
                    self.db.commit()
                    self.get_patient_prescription_no_for_mang()
                    self.tableWidget_6.clearSelection()
                    self.statusBar().showMessage("Visit Deleted Successfully !",5000)
                   # message = QMessageBox.warning(self, "Deleted Successfully  ",
                  #                                "Patient Visit Deleted Successfully   !                  ",
                  #                                QMessageBox.Ok)

            else:
                self.statusBar().showMessage("No Thing Selected !",5000)

    def delete_patient_data(self):
        try:
            patient_name = self.lineEdit_17.text()
            patient_num = self.lineEdit_18.text()
            if patient_name.strip(" ") != "" and patient_num.strip(" ") != '':
                message = QMessageBox.warning(self, "Delete ALL PATIENT DATA  ",
                                              "Are You Sure TO Delete All Patient Data  !                  ",
                                              QMessageBox.Yes, QMessageBox.No)
                if message == QMessageBox.Yes:
                    self.cur.execute('''SELECT id FROM patient WHERE name =%s AND number =%s ''',
                                     (patient_name, patient_num))
                    patient_id = self.cur.fetchone()
                    self.cur.execute('''SELECT id FROM prescription_no WHERE patient_id = %s ''', (patient_id[0],))
                    item = self.cur.fetchall()
                    if item:
                        for one in item:
                            self.cur.execute('''DELETE FROM prescription_detail WHERE prescription_no = %s ''',
                                             (one[0],))
                            self.cur.execute('''DELETE FROM prescription_no WHERE id = %s ''', (one[0],))
                    self.cur.execute('''DELETE FROM patient WHERE id = %s ''', (patient_id[0],))
                    self.db.commit()
                    self.get_names_from_db()
                    self.patient_names_for_main()
                    self.patient_names_for_report()
                    self.get_patient_prescription_no_for_mang()
                    self.get_Selected_prescription_no()
                    self.clear_patient_mang_data()
                    self.statusBar().showMessage("All Patient Data Deleted Successfully   !",5000)
                   # message = QMessageBox.warning(self, "Deleted Successfully  ",
                    #                              "All Patient Data Deleted Successfully   !                  ",
                     #                             QMessageBox.Ok)


        except Exception as m:
            print(m,"1105")

    ##########################################################################################################
    #############################
    '''Search For Patient '''

    ############################
    def search_for_patient(self):
        patient_name = self.lineEdit_8.text()
        patient_num = self.lineEdit_11.text()
        #patient_phone=self.lineEdit_22.text()
        date_from = self.dateEdit_2.date().toPyDate()
        date_to = self.dateEdit.date().toPyDate()
        patient_id = 0
        if patient_name.strip(" ") != "":
            self.cur.execute('''SELECT id , number, phone FROM patient WHERE name = %s ''', (patient_name,))
            patient_id = self.cur.fetchone()
            self.lineEdit_11.setText(str(patient_id[1]))
            self.lineEdit_22.setText(str(patient_id[2]))

        elif patient_num.strip(" ") != "":
            self.cur.execute('''SELECT id , name,phone FROM patient WHERE number = %s ''', (patient_num,))
            patient_id = self.cur.fetchone()
            self.lineEdit_8.setText(str(patient_id[1]))
            self.lineEdit_22.setText(str(patient_id[2]))

        else:
            self.statusBar().showMessage("No Data Found For This Name Or Id",5000)
        if patient_id:
            self.cur.execute('''SELECT p.drug,p.dose,p.fluid,p.volume,p.note ,num.date FROM prescription_detail as p   
                                LEFT JOIN prescription_no as num  ON  p.prescription_no =  num.id 
                                WHERE num.patient_id = %s  AND p.date BETWEEN %s AND  %s
                                 ''', (patient_id[0], date_from, date_to))
            patient_data = self.cur.fetchall()
            while self.tableWidget_2.rowCount() > 0:
                self.tableWidget_2.removeRow(0)
                self.tableWidget_2.clearSelection()
            for row_number, items in enumerate(patient_data):
                self.tableWidget_2.insertRow(row_number)
                for column_number, item in enumerate(items):
                    if column_number == 0:
                        self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_2.setItem(row_number, column_number, cell)
                    elif column_number == 2:
                        self.cur.execute('''SELECT drug_name from drugs WHERE id=%s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        self.tableWidget_2.setItem(row_number, column_number, cell)
                    else:
                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                    self.tableWidget_2.setItem(row_number, column_number, cell)

        if self.tableWidget_2.rowCount() <= 0:
            row = self.tableWidget_2.rowCount()
            self.tableWidget_2.setRowCount(row + 1)
            col = 0
            cell = QTableWidgetItem(str(" No Data Found "))
            self.tableWidget_2.setItem(row, col, cell)

        ##########################################################################################################
        #############################
        '''Search For DRUG '''

    ############################
    def search_for_drug(self):
        self.tableWidget_3.setColumnWidth(1,400)
        drug_name = self.lineEdit_9.text()

        if drug_name.strip(" ") != "":
            self.cur.execute('''SELECT id , main_category FROM drugs WHERE drug_name = %s ''', (drug_name,))
            drug_id = self.cur.fetchone()
            date_from = self.dateEdit_4.date().toPyDate()
            date_to = self.dateEdit_3.date().toPyDate()
            drug_data = ""
            if drug_id:
                if drug_id[1] != 2:
                    self.cur.execute('''SELECT d.drug_name ,SUM(p.dose)  FROM drugs as d   
                                        LEFT JOIN prescription_detail as p ON p.drug = d.id
                                        WHERE d.id = %s AND date BETWEEN %s AND  %s
                                         ''', (drug_id[0], date_from, date_to))
                    drug_data = self.cur.fetchall()
                elif drug_id[1] == 2:
                    self.cur.execute('''SELECT d.drug_name ,SUM(p.volume)  FROM drugs as d
                                        LEFT JOIN prescription_detail as p ON p.fluid = d.id
                                        WHERE d.id = %s AND date BETWEEN %s AND  %s
                                         ''', (drug_id[0], date_from, date_to))
                    drug_data = self.cur.fetchall()
                if drug_data:
                    while self.tableWidget_3.rowCount() > 0:
                        self.tableWidget_3.removeRow(0)
                        self.tableWidget_3.clearSelection()
                    for row_number, items in enumerate(drug_data):
                        self.tableWidget_3.insertRow(row_number)
                        for column_number, item in enumerate(items):
                            if column_number == 1:
                                if item is not None:
                                    cell = QTableWidgetItem(str(item))
                                    cell.setTextAlignment(Qt.AlignHCenter)
                                    self.tableWidget_3.setItem(row_number, column_number, cell)

                            else:
                                cell = QTableWidgetItem(str(item))
                                cell.setTextAlignment(Qt.AlignHCenter)
                                self.tableWidget_3.setItem(row_number, column_number, cell)

        if self.tableWidget_3.rowCount() <= 0:
            row = self.tableWidget_2.rowCount()
            self.tableWidget_3.setRowCount(row + 1)
            col = 0
            cell = QTableWidgetItem(str(" No Data Found "))
            self.tableWidget_3.setItem(row, col, cell)

    # def get_genral_search_auto(self):
    #
    #     if self.tabWidget_2.currentIndex() == 2 :
    #         self.db.commit()
    #         self.tableWidget_4.clearSelection()
    #         self.genral_search()
    #         threading.Timer(120.0, self.get_genral_search_auto).start()
    #         self.statusBar().showMessage("Updated")
    # def message_update(self):
    #     self.tableWidget_4.clearSelection()
    #     threading.Timer(10.0, self.message_update).start()
    #     self.statusBar().showMessage("")

    # def savefile(self):
    #     filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
    #     wbk = xlwt.Workbook()
    #     sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
    #     style = xlwt.XFStyle()
    #     font = xlwt.Font()
    #     font.bold = True
    #     style.font = font
    #     self.add2(sheet)
    #     wbk.save(filename)
    #
    # def add2(self, sheet):
    #
    #     for currentColumn in range(self.tableWidget_2.columnCount()):
    #         for currentRow in range(self.tableWidget_2.rowCount()):
    #             try:
    #                 teext = str(self.tableWidget_2.item(currentRow, currentColumn).text())
    #                 sheet.write(currentRow, currentColumn, teext)
    #             except AttributeError:
    #                 print(("error"))

    def save_patient_search(self):
        try:
            pa_id = self.lineEdit_11.text()
            pa_name = self.lineEdit_8.text()
            pa_phone=self.lineEdit_22.text()
            d_from = self.dateEdit_2.date().toPyDate()
            d_to = self.dateEdit.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(12)

                sheet1.set_column(0, 0, 27, cell_format)
                sheet1.set_column(2, 2, 14, cell_format) # fluid
                sheet1.set_column(4, 4, 60, cell_format) # note
                sheet1.set_column(1, 1, 22, cell_format) # dose
                sheet1.set_column(3, 3, 14, cell_format) # volium
                sheet1.set_column(5, 5, 14, cell_format) # date


                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 12})
                sheet1.set_row(0, None, main_cell)
                sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, cell_format)
                sheet1.set_row(3, None, main_cell)
                cell_format.set_align('center')
                main_cell.set_align('center')
                #cell_format.set_font_size(14)
                sheet1.merge_range(0, 0, 0, 5, 'Patient Search', main_cell)
                sheet1.write(1, 0, ' Patient Name')
                sheet1.write(1, 1, pa_name)
                sheet1.write(1, 2, ' ID ')
                sheet1.write(1, 3, pa_id)
                sheet1.write(2, 0, ' From ')
                sheet1.write(2, 1, str(d_from))
                sheet1.write(2, 2, ' To ')
                sheet1.write(2, 3, str(d_to))
                sheet1.write(3, 0, 'Drug')
                sheet1.write('B4', 'Dose')
                sheet1.write(3, 2, 'Fluid')
                sheet1.write(3, 3, 'Volume')
                sheet1.write(3, 4, 'Note')
                sheet1.write('F4','Date')
                sheet1.write('E2', 'phone NO')
                sheet1.write('E3', str(pa_phone))

                for currentColumn in range(self.tableWidget_2.columnCount()):
                    for currentRow in range(self.tableWidget_2.rowCount()):
                        try:
                            teext = str(self.tableWidget_2.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError:
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            print(m,"1304")
            pass

    def save_drug_search(self):
        try:
            d_from = self.dateEdit_4.date().toPyDate()
            d_to = self.dateEdit_3.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': True})
                main_cell = wb.add_format({'bold': True, 'bg_color': 'gray', 'font_size': 20})
                sheet1.set_column(0, 1, 30, cell_format)
                cell_format.set_align('center')
                main_cell.set_align('center')
                cell_format.set_font_size(14)
                sheet1.set_row(0, None, cell_format)
                sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, cell_format)
                sheet1.set_row(3, None, main_cell)
                sheet1.merge_range(0, 0, 0, 3, 'Drug Search', cell_format)
                sheet1.write(1, 0, ' From ')
                sheet1.write(1, 1, str(d_from))
                sheet1.write(2, 0, ' To ')
                sheet1.write(2, 1, str(d_to))
                sheet1.write(3, 0, 'Drug')
                sheet1.write(3, 1, 'Total Dose')

                for currentColumn in range(self.tableWidget_3.columnCount()):
                    for currentRow in range(self.tableWidget_3.rowCount()):
                        try:
                            teext = str(self.tableWidget_3.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError as x:
                            print(x,"1348")
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            print(m,"1353")
            pass

    def save_genral_search(self): # tablewidget_4 to excel when all table exported without slelction
        sss=self.tableWidget_4.selectionModel().selectedRows()
     #   print(len(sss))
        if len(sss)>0:
            #print("if selected")
            self.Ptt2()
            return
        try:
            d_from = self.dateEdit_6.date().toPyDate()
            d_to = self.dateEdit_5.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(11)
                #cell_format.set_bold()
                cell_format.set_align('center')

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 12})
                main_cell.set_align('center')

                my_formate = wb.add_format({'font_size':11})
                my_formate.set_align('left')


            
                #sheet1.set_column(0, 1, 25, cell_format)  # pt name
                #sheet1.set_column(2, 4, 8, cell_format)
                #sheet1.set_column(5, 5, 12, cell_format)
                #sheet1.set_column(6, 6, 15, cell_format)
                sheet1.set_column('I:I',11,cell_format) ############### Date
                sheet1.set_column('A:A',5,cell_format) ################# numbering
                sheet1.set_column('D:D',18,my_formate) # drugs
                sheet1.set_column('C:C',13,cell_format)  # pt id
                sheet1.set_column('G:G',6,cell_format)  # volume field
                sheet1.set_column('E:E',9,cell_format)  # Dose
                sheet1.set_column('H:H',50,my_formate) #  note 
                sheet1.set_column('F:F',10,my_formate) #  fluid
                sheet1.set_column('B:B',28,cell_format) # pt name
                #sheet1.set_column(1,7,30,cell_format)  # note field


                #sheet1.set_row(0, None, cell_format)
               # sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 1, 0, 7, 'General Search', cell_format)
                sheet1.write(1, 1, ' From ')
                sheet1.write(1, 3, str(d_from))
                sheet1.write(1, 4, ' To ')
                sheet1.write(1,7, str(d_to))
                sheet1.write(2, 1, 'Patient Name')  ###############  i increases all cols +1      thi
                sheet1.write(2, 2, 'ID')
                sheet1.write(2, 3, 'Drug')
                sheet1.write(2, 4, 'Dose')
                sheet1.write(2, 5, 'Fluid')
                sheet1.write(2, 6, 'Vol')
                sheet1.write(2, 7, 'Note')
                sheet1.write(2, 8, 'Date')
                num =1
                exists = []  ############################################################################################  1   steps to prevent repeating names in excel
                for currentRow in range(self.tableWidget_4.rowCount()):
                    for currentColumn in range(self.tableWidget_4.columnCount()):
                        try:
                            teext = str(self.tableWidget_4.item(currentRow, currentColumn).text())
                            #print(teext)
                            if currentColumn==0:
                                if not teext:teext = str(self.tableWidget_4.item(currentRow, currentColumn).data(1))

                            if currentColumn==0:  ######################################################   2
                                   ########################################################################  3
                                if teext not in exists:
                                    exists.append(teext)
                                    sheet1.write(currentRow + 3, currentColumn+1, str(teext))
                                    if currentColumn == 0 :
                                        sheet1.write(currentRow + 3,0,str(num))                               
                                        num=num+1
                                
                                

                            else:                    ########################################################################5
                                sheet1.write(currentRow + 3, currentColumn+1, str(teext))  ####################################6
                                    
                        except AttributeError as x:
                            pass
                            print(x,"1433")
                wb.close()
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            print(m,"1437")
            pass

    def save_all_drug_dose(self): # dose
        try:
            d_from = self.dateEdit_8.date().toPyDate()
            d_to = self.dateEdit_7.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()
                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(12)
                #cell_format.set_bold()
                cell_format.set_align('left')
                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 12})
                main_cell.set_align('center')

                my_formate = wb.add_format({'bold': False})
                my_formate.set_align('center')

                sheet1.set_column(0, 0, 27, cell_format)
                sheet1.set_column(1, 1, 13, cell_format)
                sheet1.set_column('C:C',12 , cell_format)
                #sheet1.set_row(0, None, cell_format)
                #sheet1.set_row(1, None, cell_format)
                #sheet1.set_row(2, None, cell_format)
                sheet1.set_row(3, None, main_cell)
                sheet1.merge_range(0, 0, 0, 2, 'All Drug Dose Search', main_cell)
                sheet1.write(1, 0, ' From ',my_formate)
                sheet1.write(1, 1, str(d_from))
                sheet1.write(2, 0, ' To ',my_formate)
                sheet1.write(2, 1, str(d_to))
                sheet1.write(3, 0, 'Drug Name')
                sheet1.write(3, 1, 'Total Dose')
                sheet1.write(3, 2, 'No')
                for currentColumn in range(self.tableWidget_5.columnCount()):
                    for currentRow in range(self.tableWidget_5.rowCount()):
                        try:
                            teext = str(self.tableWidget_5.item(currentRow, currentColumn).text())
                            sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError:
                            pass
                wb.close()
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            print(m,"1484")
            pass

    ##########################################################################################################
    #############################
    '''Genral Search '''

    ############################
    def genral_search(self):
        global loaded
        loaded=False
        try:           
            date_from = self.dateEdit_6.date().toPyDate()
            date_to = self.dateEdit_5.date().toPyDate()
            # self.cur.execute('''SELECT pname.name FROM prescription_detail as pre
            #                     LEFT JOIN prescription_no as pid ON  pid.id = pre.prescription_no
            #                     LEFT JOIN patient as pname ON pid.patient_id = pname.id
            #                     ORDER BY pre.id DESC LIMIT 1''')
            # last_prescription = self.cur.fetchone()
            main_category=self.comboBox_7.currentIndex()
           # print(main_category)
            if (main_category==1):
                main_category=1#chemo =0 ok? yes
            else:
                main_category=2

            self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose ,p.fluid , p.volume , p.note , p.date,p.is_checked , p.prescription_no FROM prescription_detail as p 
                                JOIN drugs as d ON p.drug = d.id
                                LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                WHERE p.date BETWEEN %s AND  %s and d.main_category<%s
                                ORDER BY p.date desc, p.id desc,pid.id desc
                                ''', (date_from, date_to,main_category))#BY p.date desc, p.id desc    
                 
            full_search = self.cur.fetchall()

            #self.tableWidget_4.resizeRowsToContents()
                        
            self.tableWidget_4.clearSelection()
            
            while self.tableWidget_4.rowCount() > 0:
                self.tableWidget_4.removeRow(0)
                self.tableWidget_4.clearSelection()
            noduplicates = []  ############################################### 3   
            colors=["#ccffff","#F1D4F1"]##ccffff
            colornum=0
            for row_number, items in enumerate(full_search):
                
                self.tableWidget_4.insertRow(row_number)
                for column_number, item in enumerate(items):

                    if column_number == 4:
                        self.cur.execute('''SELECT drug_name From drugs WHERE id = %s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_4.setItem(row_number, column_number, cell)
                    elif column_number == 8:
                        if item == 0:
                            chkBoxItem = QTableWidgetItem()
                            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(Qt.Unchecked)
                            chkBoxItem.setData(LastStateRole,0)
                            self.tableWidget_4.setItem(row_number, column_number, chkBoxItem)


                        else:
                            chkBoxItem = QTableWidgetItem()
                            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(Qt.Checked)
                            chkBoxItem.setData(LastStateRole,1)
                            self.tableWidget_4.setItem(row_number, column_number, chkBoxItem)
                            self.check_color_green(row_number)

                    elif column_number == 0:         #####################################  4
                        
                        
                        cell = QTableWidgetItem()  ########################### 7
                        cell.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                        
                        if item and item not in noduplicates:  ###################################5
                            noduplicates.append(item)  ##################################  6
                   #         self.tableWidget_4.setForeground(QColor('white'))  ############10
                            cell.setText(str(item))
                            colornum=not colornum
                            cell.setBackground(QColor(colors[colornum]))
                            
                        else:
                            cell.setBackground(QColor(colors[colornum]))
                            cell.setData(1,item)
                            
                        #self.tableWidget_4.resizeRowsToContents() 
                        self.tableWidget_4.setItem(row_number, column_number, cell)  ######  9
                                                        
                    else:

                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_4.setItem(row_number, column_number, cell)
            loaded=True
        except Exception as e:
            print("error",e)
            pass
#########################################################################################################################################################
########################################################################################################################################################

    #def fixpatients(self):
      #  print("fixpatients")
        #p.prescription_no ,pname.id FROM prescription_detail
        #self.cur.execute(''' SELECT id FROM patient ORDER BY id ;''')
        #p=self.cur.fetchall()
        #self.cur.execute('''DELETE from patient_number;''')
        #count =0
        #for x in p:
         #   count=count+1
        #    self.cur.execute (''' INSERT INTO patient_number (id,patient_id) values (%s,%s) ''',(str(count),x[0],) )
       
    def checked(self):
        global loaded
        global ids
        loaded=False
        numbering=0
        try:
            date_from = self.dateEdit_17.date().toPyDate()
            date_to = self.dateEdit_13.date().toPyDate()

            main_category=self.comboBox_8.currentIndex()
            if (main_category==1):
                main_category=1#chemo =0 ok? yes
            else:
                main_category=2

            self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose ,p.fluid , p.volume , p.note , 
                                p.date,p.is_checked , p.prescription_no ,pname.id,p.id_checked FROM prescription_detail as p 
                                JOIN drugs as d ON p.drug = d.id
                                LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                WHERE p.date BETWEEN %s AND  %s and d.main_category<%s and p.is_checked>0
                                ORDER BY p.id_checked asc
                                ''', (date_from, date_to,main_category))#BY p.date desc, p.id desc    
                 
            full_search = self.cur.fetchall()  #  asc

            self.tableWidget_9.clearSelection()
            while self.tableWidget_9.rowCount() > 0:
                self.tableWidget_9.removeRow(0)
                self.tableWidget_9.clearSelection()
            noduplicates = []  ############################################### 3   
            colors=["#ccffff","#F1D4F1"]##ccffff
            colornum=0
            for row_number, items in enumerate(full_search):
                
                self.tableWidget_9.insertRow(row_number)
                for column_number, item in enumerate(items):
                    column_number=column_number+1
#0 name | 1 id / 2 drug_name / 3 dose / 4 fluid /  5 volume /  6 note / 7 date / 8 is checked / 9 presctiption_no
#1 name | 2 id / 3 drug_name / 4 dose / 5 fluid /  6 volume /  7 note / 9 is checked 
#0 No   /1 name/ 2 id / 3 drug / 4 dose / 5 fluid / 6 volume / 7 note                     
                    if column_number==8 or column_number>=10:continue#/ 8 date / 10 presctiption_no
                    
                    if column_number == 5:
                        self.cur.execute('''SELECT drug_name From drugs WHERE id = %s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_9.setItem(row_number, column_number, cell)

                    elif column_number == 1:         #####################################  4                        
                        cell = QTableWidgetItem()  ########################### 7
                        cell.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                        cell1 = QTableWidgetItem()  ########################### 7
                        cell1.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                        if item and item not in noduplicates:  ###################################5
                            noduplicates.append(item)  ##################################  6
                   #         self.tableWidget_4.setForeground(QColor('white'))  ############10
                            cell.setText(str(item))
                            colornum=not colornum
                            cell.setBackground(QColor(colors[colornum]))
                            
                            numbering=numbering+1

                            #self.cur.execute('''select id from patient_number where patient_id=%s''',(str(items[-1]),))
                            #patient=self.cur.fetchall()
                            cell1.setText(str(numbering))
                            
                            cell1.setBackground(QColor(colors[colornum]))
                            #print("ok")
                        else:
                            #print("item-++-->",item)
                            cell.setBackground(QColor(colors[colornum]))
                            cell1 = QTableWidgetItem()  ########################### 7
                            cell1.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                            cell1.setBackground(QColor(colors[colornum]))
                            #print("ok")
                            cell.setData(1,item)
                            
                            
                        self.tableWidget_9.setItem(row_number, column_number, cell)  ######  9
                        self.tableWidget_9.setItem(row_number, 0, cell1)  ######  9
                                                        
                    else:
                        if column_number==2:
                            ids[str(item)]=str(numbering)
                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_9.setItem(row_number, column_number, cell)
            loaded=True
           # print(ids)
        except Exception as e:
            print("error 1974",e)
            pass
        
    def print_row(self): # to print selected row only with its informations 
        row = self.tableWidget_9.currentRow()
        for column in range(self.tableWidget_9.columnCount()):
            _item=self.tableWidget_9.item(row,column)
            if _item and column !=5 and column !=6:
                item=self.tableWidget_9.item(row,column).text()
                print(f'row:{row},column:{column},item={item}')
                
        try:
            d_from = self.dateEdit_17.date().toPyDate() ############ is it ok?  but the excel sheet differ which function is for excel? 
            d_to = self.dateEdit_13.date().toPyDate()
            path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(14)
                cell_format.set_align('center')

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 14})
                main_cell.set_align('center')

                my_formate = wb.add_format({'font_size':14})
                my_formate.set_align('left')

                sheet1.set_column('A:A',7,cell_format) ################# numbering
                sheet1.set_column('B:B',35,cell_format) # pt name
                sheet1.set_column('C:C',12,my_formate)  # pt id

                sheet1.write(0, 0, 'Name')
                sheet1.write(1, 0, ' ID ')
                sheet1.write(2, 0, ' Drug ')
               # sheet1.write(1,7, str(d_to))
                sheet1.write(3, 0, 'Dose')  ###############  i increases all cols +1      thi
                sheet1.write(4, 0, 'Note')
                sheet1.write(5, 0, 'No')
                exists = []  ############################################################################################  1   steps to prevent repeating names in excel
                sss=self.tableWidget_9.selectionModel().selectedRows()
                rowExcel=0
                for z in sss:
                    currentRow=z.row()     # i think it clear selection
                    rowExcel=rowExcel+1
                    for currentColumn in range(self.tableWidget_9.columnCount()):
                        try:
                            teext = str(self.tableWidget_9.item(currentRow, currentColumn).text())                         
                            if currentColumn == 0:
                                if teext== None:teext = str(self.tableWidget_9.item(currentRow, currentColumn).data(1)) 
                            if currentColumn == 1 or currentColumn == 2 or currentColumn==0:
                                if teext and teext.strip()!="" and teext not in exists:
                                    exists.append(teext)
                                    sheet1.write(rowExcel +1,currentColumn,str(teext))

                            else:
                                sheet1.write(rowExcel+3,currentColumn,str(teext))

                        except AttributeError as xx:
                            print(xx,"2150")
                            pass
                wb.close()
                
                self.statusBar().showMessage('Row Printed Successfully',5000)#change it to allow selection of rows no/ 
        except Exception as m:
            print(m,"2156")
            pass
                
                
        #  printedRow = self.tableWidget_9.currentRow()
      #  printedColumn = self.tableWidget_9.currentColumn()
      #  data= self.tableWidget_9.item(printedRow,printedColumn)
      #  print(f'data={data}')
      #  if data:
      #      data=data.text()
      #      print(f'data={data}')

       
       
       
  ############################################################################################################################     
     #  xxx= self.tableWidget_9.selectionModel().selectedRows()
      # if len(xxx)>0:
      #     self.selected_row_to_excel()
           
    #def selected_row_to_excel(self):
    #    try:
    #        d_from = self.dateEdit_17.date().toPyDate()   ####################### is it ok?  but the excel sheet differ which function is for excel? 
    #        d_to = self.dateEdit_13.date().toPyDate()
    #        path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
    #        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', path, ".xlsx(*.xlsx)")
    #        if filename:
    #            wb = Workbook(filename)
    #            sheet1 = wb.add_worksheet()

    #            cell_format = wb.add_format({'bold': False})
    #            cell_format.set_font_size(14)
    #            cell_format.set_align('center')

    #            main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 14})
    #            main_cell.set_align('center')

    #            my_formate = wb.add_format({'font_size':14})
    #            my_formate.set_align('left')

    #            sheet1.set_column('A:A',7,cell_format) ################# numbering
    #            sheet1.set_column('B:B',35,cell_format) # pt name
    #            sheet1.set_column('C:C',12,my_formate)  # pt id

     #           sheet1.write(0, 0, 'Name')
     #           sheet1.write(1, 0, ' ID ')
     #           sheet1.write(2, 0, ' Drug ')
               # sheet1.write(1,7, str(d_to))
     #           sheet1.write(3, 0, 'Dose')  ###############  i increases all cols +1      thi
    #            sheet1.write(4, 0, 'Note')
    #            sheet1.write(5, 0, 'No')
    #            exists = []  ############################################################################################  1   steps to prevent repeating names in excel
    #            sss=self.tableWidget_9.selectionModel().selectedRows()
    #            rowExcel=-1
     #           for z in sss:
     #               currentRow=z.row()     # i think it clear selection
    #                rowExcel=rowExcel+1
    #                for currentColumn in range(self.tableWidget_9.columnCount()):
    #                    try:
    #                        teext = str(self.tableWidget_9.item(currentRow, currentColumn).text())                         
     #                       if currentColumn == 0:
    #                            if teext== None:teext = str(self.tableWidget_9.item(currentRow, currentColumn).data(1)) 
    #                        if currentColumn == 1 or currentColumn == 2 or currentColumn==0:
    #                            if teext and teext.strip()!="" and teext not in exists:
    #                                exists.append(teext)
    #                                sheet1.write(rowExcel +1,currentColumn,str(teext))

    #                        else:
     #                           sheet1.write(rowExcel+3,currentColumn,str(teext))

    #                    except AttributeError as xx:
     #                       print(xx,"2150")
       #                     pass
      #          wb.close()
                
     #           self.statusBar().showMessage('Row Printed Successfully',5000)#change it to allow selection of rows no/ 
    #    except Exception as m:
    #        print(m,"2156")
    #        pass

        

    #########################################  checked to excel
    def checked_to_excel(self): # all table without selection
        sss=self.tableWidget_9.selectionModel().selectedRows()
        if len(sss)>0:
            self.checked_to_excel2()
            return
        try:
            d_from = self.dateEdit_17.date().toPyDate()
            d_to = self.dateEdit_13.date().toPyDate()
            def_path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', def_path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(14)
                cell_format.set_align('center')

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 14})
                main_cell.set_align('center')

                my_formate = wb.add_format({'font_size':14})
                my_formate.set_align('left')

                my_formate2 = wb.add_format({'font_size':12})
                my_formate2.set_align('left')

                my_formate3 = wb.add_format({'font_size':12})
                my_formate3.set_align('center')

                
                sheet1.set_column('A:A',7,cell_format) ################# numbering
                sheet1.set_column('B:B',35,cell_format) # pt name
                sheet1.set_column('C:C',12,my_formate3)  # pt id
                sheet1.set_column('D:D',23,my_formate) # drugs
                sheet1.set_column('E:E',11,cell_format)  # Dose
                sheet1.set_column('F:F',10,my_formate2) #  fluid
                sheet1.set_column('G:G',7,my_formate3)  # volume field
                sheet1.set_column('H:H',60,my_formate2) #  note 

                #sheet1.set_row(0, None, cell_format)
               # sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 1, 0, 7, 'Checked Patients Search', main_cell)
                sheet1.write(2, 0, 'No')
                sheet1.write(1, 1, ' From ')
                sheet1.write(1, 3, str(d_from))
                sheet1.write(1, 4, ' To ')
                sheet1.write(1,7, str(d_to))
                sheet1.write(2, 1, 'Patient Name')  ###############  i increases all cols +1      thi
                sheet1.write(2, 2, 'ID')
                sheet1.write(2, 3, 'Drug')
                sheet1.write(2, 4, 'Dose')
                sheet1.write(2, 5, 'Fluid')
                sheet1.write(2, 6, 'Vol')
                sheet1.write(2, 7, 'Note')
               # num =1
                exists = []  ############################################################################################  1   steps to prevent repeating names in excel
                for currentRow in range(self.tableWidget_9.rowCount()):
                    for currentColumn in range(self.tableWidget_9.columnCount()):
                        try:
                            teext = str(self.tableWidget_9.item(currentRow, currentColumn).text())
                            if currentColumn==0:
                                if teext== None:teext = str(self.tableWidget_9.item(currentRow, currentColumn).data(1))
                               # if not teext:teext = str(self.tableWidget_9.item(currentRow, currentColumn).data(1))

                            if currentColumn==1 or currentColumn==2 or currentColumn==0:
                                if teext not in exists:  ######################################################   2
                               # if teext not in exists:
                                    exists.append(teext)
                                    sheet1.write(currentRow + 3, currentColumn, str(teext))
                           #         if currentColumn == 0 :
                           #             sheet1.write(currentRow + 3,0,str(num))                               
                           #             num=num+1
                            else:                    ########################################################################5
                                sheet1.write(currentRow + 3, currentColumn, str(teext))  ####################################6
                                    
                        except AttributeError as x:
                            pass
                            print(x,"1433")
                wb.close()
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            print(m,"1437")
            pass

    #########################################

    def checked_to_excel2(self): # selected rowa to excel in checked tablewidget_9

        try:
            d_from = self.dateEdit_17.date().toPyDate()   ####################### is it ok?  but the excel sheet differ which function is for excel? 
            d_to = self.dateEdit_13.date().toPyDate()
            path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(14)
                cell_format.set_align('center')

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 14})
                main_cell.set_align('center')

                my_formate = wb.add_format({'font_size':14})
                my_formate.set_align('left')

                my_formate2 = wb.add_format({'font_size':12})
                my_formate2.set_align('left')

                my_formate3 = wb.add_format({'font_size':12})
                my_formate3.set_align('center')

                
                sheet1.set_column('A:A',7,cell_format) ################# numbering
                sheet1.set_column('B:B',35,cell_format) # pt name
                sheet1.set_column('C:C',12,my_formate3)  # pt id
                sheet1.set_column('D:D',23,my_formate) # drugs
                sheet1.set_column('E:E',11,cell_format)  # Dose
                sheet1.set_column('F:F',10,my_formate2) #  fluid
                sheet1.set_column('G:G',7,my_formate3)  # volume field
                sheet1.set_column('H:H',60,my_formate2) #  note 

                #sheet1.set_row(0, None, cell_format)
               # sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 1, 0, 7, 'Checked Patients Search ', main_cell)
                sheet1.write(2, 0, 'No')
                sheet1.write(1, 1, ' From ')
                sheet1.write(1, 3, str(d_from))
                sheet1.write(1, 4, ' To ')
                sheet1.write(1,7, str(d_to))
                sheet1.write(2, 1, 'Patient Name')  ###############  i increases all cols +1      thi
                sheet1.write(2, 2, 'ID')
                sheet1.write(2, 3, 'Drug')
                sheet1.write(2, 4, 'Dose')
                sheet1.write(2, 5, 'Fluid')
                sheet1.write(2, 6, 'Vol')
                sheet1.write(2, 7, 'Note')

                
               # numb =1
                exists = []  ############################################################################################  1   steps to prevent repeating names in excel
                sss=self.tableWidget_9.selectionModel().selectedRows()
                rowExcel=-1
                for z in sss:
                    currentRow=z.row()     # i think it clear selection
                    rowExcel=rowExcel+1
                    for currentColumn in range(self.tableWidget_9.columnCount()):
                        try:
                            teext = str(self.tableWidget_9.item(currentRow, currentColumn).text())                         
                            if currentColumn == 0:
                                if teext== None:teext = str(self.tableWidget_9.item(currentRow, currentColumn).data(1)) 
                                #if not teext:teext = str(self.tableWidget_9.item(currentRow,currentColumn).data(1))
                            if currentColumn == 1 or currentColumn == 2 or currentColumn==0:
                                if teext and teext.strip()!="" and teext not in exists:
                                    exists.append(teext)
                                    sheet1.write(rowExcel +3,currentColumn,str(teext))
                                   # if currentColumn == 0:
                                   #     sheet1.write(rowExcel+3,0,str(numb))
                                   #     numb=numb+1

                            else:
                                sheet1.write(rowExcel+3,currentColumn,str(teext))

                   #         sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError as xx:
                            print(xx,"2150")
                            pass
                wb.close()
                
                self.statusBar().showMessage('Report Created Successfully',5000)#change it to allow selection of rows no/ 
        except Exception as m:
            print(m,"2156")
            pass


########################################################################################################################################################
#######################################################################################################################################################
    
   # def filter(self):
    @pyqtSlot()
    def filter(self, txt, color=False,keep_color=False):  # tableWidget_4 search by name of pateint
        self.txt = txt
        self.color = color
        self.keep_color=keep_color
        self.match_found = False

        def show_color_Row(row_number: int, showRow: bool = True, colorRow: bool = False) -> None:
            for j in range(self.tableWidget_4.columnCount()):
                if colorRow == True and self.keep_color==False:
                    self.tableWidget_4.item(
                        row_number, j).setBackground(QColor(0, 255, 0))
                else:
                    if self.keep_color==False and colorRow==True:
                        self.tableWidget_4.item(
                            row_number, j).setBackground(QColor(255, 255, 255))

                if showRow == False:
                    self.tableWidget_4.hideRow(i)
                else:
                    self.tableWidget_4.showRow(i)

        for i in range(self.tableWidget_4.rowCount()):
            if self.txt != "":
                if self.tableWidget_4.item(i, 0).text().lower().startswith(self.txt.lower()):
                    self.match_found = True

                elif self.match_found == True and self.tableWidget_4.item(i, 0).text() == "":
                    self.match_found = True
                else:
                    self.match_found = False

                if self.match_found == True:
                    show_color_Row(i, colorRow=self.color)

                elif self.match_found == False and self.color == False:
                    show_color_Row(i, showRow=False)
                else:
                    show_color_Row(i)
            else:
                show_color_Row(i)


            """
            def filter(self) #  with query
            global loaded  #  tableWidget_4 search by name of pateint  with aquery
            loaded=False
            try:
                date_from = self.dateEdit_6.date().toPyDate()
                date_to = self.dateEdit_5.date().toPyDate()

                called = self.lineEdit_19.text()
                called=called+"%"            

                main_category=self.comboBox_7.currentIndex()
                if (main_category==1):
                    main_category=1#chemo =0 
                else:
                    main_category=2

                self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose ,p.fluid , p.volume , p.note , p.date,p.is_checked , p.prescription_no FROM prescription_detail as p 
                                    JOIN drugs as d ON p.drug = d.id
                                    LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                    LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                    WHERE p.date BETWEEN %s AND  %s and d.main_category<%s and pname.name LIKE %s
                                    ORDER BY p.date desc, p.id desc,pid.id desc
                                    ''', (date_from, date_to,main_category,called))#BY p.date desc, p.id desc     ##  WHERE p.date BETWEEN %s AND  %s and d.main_category<%s
                    
                full_search = self.cur.fetchall()
            # print(len(full_search))

                #self.tableWidget_4.clearSelection()
            # self.lineEdit_19.clearSelection()
            
                while self.tableWidget_4.rowCount() > 0:
                    self.tableWidget_4.removeRow(0)
                    self.tableWidget_4.clearSelection()
                noduplicates = []  ############################################### 3   
                colors=["#ccffff","#F1D4F1"]##ccffff
                colornum=0
                for row_number, items in enumerate(full_search):
                    
                    self.tableWidget_4.insertRow(row_number)
                    for column_number, item in enumerate(items):
                    #   if column_number==0:  ######################################### 1 no duplication in general search in program
                    #      print(item)   ############################################# 2

                        if column_number == 4:
                            self.cur.execute('''SELECT drug_name From drugs WHERE id = %s''', (item,))
                            drug_name = self.cur.fetchone()
                            cell = QTableWidgetItem(str(drug_name[0]))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            cell.setBackground(QColor(colors[colornum]))
                            self.tableWidget_4.setItem(row_number, column_number, cell)
                        elif column_number == 8:
                            if item == 0:
                                chkBoxItem = QTableWidgetItem()
                                chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                                chkBoxItem.setCheckState(Qt.Unchecked)
                                chkBoxItem.setData(LastStateRole,0)
                                self.tableWidget_4.setItem(row_number, column_number, chkBoxItem)


                            else:
                                chkBoxItem = QTableWidgetItem()
                                chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                                chkBoxItem.setCheckState(Qt.Checked)
                                chkBoxItem.setData(LastStateRole,1)
                                self.tableWidget_4.setItem(row_number, column_number, chkBoxItem)
                                self.check_color_green(row_number)

                        elif column_number == 0:         #####################################  4
                            
                            
                            cell = QTableWidgetItem()  ########################### 7
                            cell.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                            
                            if item and item not in noduplicates:  ###################################5
                                noduplicates.append(item)  ##################################  6
                    #         self.tableWidget_4.setForeground(QColor('white'))  ############10
                                cell.setText(str(item))
                                colornum=not colornum
                                cell.setBackground(QColor(colors[colornum]))
                            else:
                                cell.setBackground(QColor(colors[colornum]))
                                cell.setData(1,item)
                                
                                
                            self.tableWidget_4.setItem(row_number, column_number, cell)  ######  9
                                                            
                        else:

                            cell = QTableWidgetItem(str(item))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            cell.setBackground(QColor(colors[colornum]))
                            self.tableWidget_4.setItem(row_number, column_number, cell)
                loaded=True
            except Exception as e:
                print("error",e)
                pass
            """     
#####################################################################################################################################################################
    def check_color_green(self, item):
        self.tableWidget_4.item(item, 0).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 1).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 2).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 3).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 4).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 5).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 6).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 7).setBackground(QColor("#00FF7F"))
        self.tableWidget_4.item(item, 8).setBackground(QColor("#00FF7F"))


    def check_color_green1(self, item):
        self.tableWidget_8.item(item, 0).setBackground(QColor("#00FF7F"))
        self.tableWidget_8.item(item, 1).setBackground(QColor("#00FF7F"))
        self.tableWidget_8.item(item, 2).setBackground(QColor("#00FF7F"))
        self.tableWidget_8.item(item, 3).setBackground(QColor("#00FF7F"))
        self.tableWidget_8.item(item, 4).setBackground(QColor("#00FF7F"))
        self.tableWidget_8.item(item, 5).setBackground(QColor("#00FF7F"))
        self.tableWidget_8.item(item, 6).setBackground(QColor("#00FF7F"))
       # self.tableWidget_4.item(item, 7).setBackground(QColor("green"))
       # self.tableWidget_4.item(item, 8).setBackground(QColor("green"))


    def ww(self):

        #print("ww")
        rows = sorted(set(index.row() for index in self.tableWidget_4.selectedIndexes()))
        for row in rows:
            self.roww=row
####################################################################
    #def ww1(self):

        #rows = sorted(set(index.row() for index in self.tableWidget_8.selectedIndexes()))
        #for row in rows:
           # self.roww=row


    def update_check_status1(self, row, column): # make row checked if checked
        if column<5:
            return
        global loaded
       # print("entering...")
        item = self.tableWidget_8.item(row, column)
        lastState = item.data(LastStateRole)
        currentState = item.checkState()         
        if currentState != lastState:
            if True:#currentState == Qt.Checked:
                code = self.tableWidget_8.item(row, 1).text()
                if self.tableWidget_8.item(row, 0).text().strip():
                    name = self.tableWidget_8.item(row, 0).text()
                else:
                    name = self.tableWidget_8.item(row, 0).data(1)
                   
                self.cur.execute('''SELECT id FROM patient WHERE number=%s AND name = %s ''', (code, name))
                pa_id = self.cur.fetchone()
                self.cur.execute('''SELECT id FROM prescription_no  WHERE patient_id=%s  ORDER BY id DESC LIMIT 1  ''', (pa_id[0],))
                pre_id = self.cur.fetchone()
                self.cur.execute('''UPDATE prescription_detail SET is_checked =%s WHERE prescription_no=%s ''',         (str(currentState), pre_id[0],))
                self.db.commit()
                if loaded:
                    loaded=False
                   # self.premedication_fun()


    def update_check_status(self, row, column):
        if column<8:
            return
        global loaded

        item = self.tableWidget_4.item(row, column)
        lastState = item.data(LastStateRole)
        currentState = item.checkState()
        if currentState != lastState:
            if True:#currentState == Qt.Checked:
                code = self.tableWidget_4.item(row, 1).text()
                if self.tableWidget_4.item(row, 0).text().strip():
                    name = self.tableWidget_4.item(row, 0).text()
                else:
                    name=self.tableWidget_4.item(row, 0).data(1)
                
                self.cur.execute('''SELECT id FROM patient WHERE number=%s AND name = %s ''', (code, name))
                pa_id = self.cur.fetchone()
                self.cur.execute('''SELECT id FROM prescription_no  WHERE patient_id=%s  ORDER BY id DESC LIMIT 1  ''',
                                 (pa_id[0],))
                pre_id = self.cur.fetchone()
                if currentState>0:
                    #p.prescription_no ,pname.id FROM prescription_detail
                    count =0
                    self.cur.execute('''select max(id_checked) from prescription_detail;''')
                    count = self.cur.fetchone()[0]
                    if count:
                        count=count+1
                    else:count=1
                    self.cur.execute('''UPDATE prescription_detail SET is_checked =%s WHERE prescription_no=%s ''',
                                 (str(currentState), pre_id[0],))
                    self.cur.execute('''UPDATE prescription_detail SET id_checked =%s WHERE prescription_no=%s and id_checked IS null''',
                                 (str(count), pre_id[0],))
                else:
                    self.cur.execute('''UPDATE prescription_detail SET is_checked =%s WHERE prescription_no=%s ''',
                                 (str(currentState), pre_id[0],))
                    self.cur.execute('''UPDATE prescription_detail SET id_checked =null WHERE prescription_no=%s ''',
                                 (pre_id[0],))
                self.db.commit()
                if loaded:
                    loaded=False
                    #self.genral_search()
                    



    ##########################################################################################################
    #############################
    # '''Genral Dose  Search '''
    ############################
    def genral_drug_dose(self):
        main_category = -1
        user_choise = self.comboBox_3.currentIndex()
        if user_choise == 0:
            main_category = 0
        elif user_choise == 1:
            main_category = 1
        else:
            main_category = 2
        date_from = self.dateEdit_8.date().toPyDate()
        date_to = self.dateEdit_7.date().toPyDate()
        self.cur.execute(''' SELECT d.drug_name , SUM(p.dose) FROM prescription_detail as p 
                            LEFT JOIN drugs AS d ON p.drug = d.id 
                            WHERE d.main_category =%s AND p.date BETWEEN %s AND  %s 
                            GROUP BY d.id
                            ORDER BY d.drug_name 

                            ''', (main_category, date_from, date_to))  #   ORDER BY p.date, d.drug_name
        all_drugs = self.cur.fetchall()
        self.cur.execute(''' SELECT d.drug_name , SUM(p.volume) FROM prescription_detail as p 
                            LEFT JOIN drugs AS d ON p.fluid = d.id 
                            WHERE d.main_category =%s AND p.date BETWEEN %s AND  %s 
                            GROUP BY d.id
                            ORDER BY d.drug_name 
                            ''', (main_category, date_from, date_to))  #  ORDER BY p.date, d.drug_name
        all_fluid = self.cur.fetchall()

        while self.tableWidget_5.rowCount() > 0:
            self.tableWidget_5.removeRow(0)
            self.tableWidget_5.clearSelection()

        colors=["#ccffff","#F1D4F1"] ####### 1 to color th table in program
        colornum=0  ###   2 

        for row_number, items in enumerate(all_fluid):
            self.tableWidget_5.insertRow(row_number)
            for column_number, item in enumerate(items):
                cell = QTableWidgetItem(str(item))
                cell.setTextAlignment(Qt.AlignHCenter)
                cell.setBackground(QColor(colors[colornum]))
                self.tableWidget_5.setItem(row_number, column_number, cell)
        for row_number, items in enumerate(all_drugs):
            self.tableWidget_5.insertRow(row_number)
            for column_number, item in enumerate(items):
                if column_number == 1:
                    data = str(item)
                    if data.split(".")[-1] == "0":
                        #print("here")
                        cell = QTableWidgetItem(str(data.split(".")[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setText(str(item))   #### 7
                        colornum!= colornum   #####
                        
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_5.setItem(row_number, column_number, cell)
                    else:
                        new = round(item, 2)
                        cell = QTableWidgetItem(str(new))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        
                        cell.setBackground(QColor(colors[colornum])) ######  4
                        self.tableWidget_5.setItem(row_number, column_number, cell)
                        if cell.setText(str(item)):   #### 7
                            colornum!= colornum  ##   6
                            cell.setBackground(QColor(colors[colornum]))  ######
                        else:
                            cell.setBackground(QColor(colors[colornum])) ### 8
                            cell.setData(1,item)  ############   3
                else:
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    cell.setBackground(QColor(colors[colornum]))  ######  5
                    self.tableWidget_5.setItem(row_number, column_number, cell)

    def show_daily_statics(self):
        date = datetime.date.today()
        self.cur.execute('''SELECT distinct COUNT(p.id) FROM patient as p WHERE add_date=%s ''', (date,))
        total_new = self.cur.fetchone()
        self.lcdNumber_3.display(int(total_new[0]))


    def show_daily_statics_costum(self):
        date_from = self.dateEdit_9.date().toPyDate()
        date_to = self.dateEdit_10.date().toPyDate()
        self.cur.execute('''SELECT COUNT(distinct patient_id) FROM prescription_no WHERE date BETWEEN %s AND %s''',
                         (date_from, date_to))
        total_old = self.cur.fetchone()
        self.lcdNumber_4.display(int(total_old[0]))


    def number_of_prescription(self):
        date_from = self.dateEdit_14.date().toPyDate()
        date_to = self.dateEdit_15.date().toPyDate()
        self.cur.execute('''SELECT COUNT(distinct p.id) FROM prescription_no as p WHERE date BETWEEN %s AND %s''',(date_from, date_to))
        number = self.cur.fetchone()
        self.lcdNumber_5.display(int(number[0]))



    ##########################################################################################################
    #############################
    '''Set_TOday_date '''

    ############################
    def set_today_date(self):
        date = datetime.date.today()
        self.dateEdit_2.setDate(date)
        self.dateEdit.setDate(date)
        self.dateEdit_3.setDate(date)
        self.dateEdit_4.setDate(date)
        self.dateEdit_5.setDate(date)
        self.dateEdit_6.setDate(date)
        self.dateEdit_7.setDate(date)
        self.dateEdit_8.setDate(date)
        self.dateEdit_9.setDate(date)
        self.dateEdit_10.setDate(date)
        self.dateEdit_11.setDate(date)
        self.dateEdit_12.setDate(date)
        self.dateEdit_13.setDate(date)
        self.dateEdit_17.setDate(date)
        self.dateEdit_14.setDate(date)
        self.dateEdit_15.setDate(date)
        self.dateEdit_16.setDate(date)
        self.dateEdit_18.setDate(date)




    def clear_database_data(self):
        message = QMessageBox.warning(self, "Clear DATABASE ",
                                      "ARE YOU SURE YOU WILL CLEAR ALL DATA WILL BE LOSS !                  ",
                                      QMessageBox.Yes, QMessageBox.No)
        if message == QMessageBox.Yes:
            message = QMessageBox.warning(self, "Clear DATABASE ",
                                          "Last Step Press No To Clear DataBase !                  ",
                                          QMessageBox.Yes, QMessageBox.No)
            if message == QMessageBox.No:
                self.cur.execute('''DELETE FROM prescription_detail WHERE id != 0''')
                self.cur.execute('''DELETE FROM prescription_no WHERE id != 0''')
                self.cur.execute('''DELETE FROM drugs WHERE id != 0''')
                self.cur.execute('''DELETE FROM patient WHERE id != 0''')
                self.db.commit()
                names_list.clear()
                drugs_list.clear()
                id_list.clear()
                check_add_drugs.clear()
                self.clear_data()
                self.close()
                message = QMessageBox.warning(self, "Clear DATABASE ",
                                              "Database Is Clear !                  ",
                                              QMessageBox.Ok)

    #def closeEvent(self, event):

     #   quit_msg = "Are you sure you want to exit the program?"
     #   reply = QMessageBox.question(self, 'Message',
     #                                quit_msg, QMessageBox.Yes, QMessageBox.No)

     #   if reply == QMessageBox.Yes:
       #     self.close()
     #       event.accept()

      #  else:
    #        event.ignore()
    ###################################################################################### ################# my tab for premedications
     
    def Premedication_to_excel(self): # premeidcation all to excel
        sss=self.tableWidget_8.selectionModel().selectedRows()
       # print(len(sss))
        if len(sss)>0:
            self.Ptt()
            return
        try:

            date_from = self.dateEdit_11.date().toPyDate()   ####################### go to excel function
            date_to = self.dateEdit_12.date().toPyDate()
            path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(11)
                cell_format.set_align('center')

                my_format = wb.add_format({'bold': False})
                my_format.set_font_size(11)
                my_format.set_align('center')


                sheet1.set_column('A:A', 6, cell_format)
                sheet1.set_column('B:B', 28, cell_format) # patient name
                sheet1.set_column('C:C', 14, cell_format) # pt id
                sheet1.set_column('D:D', 19, my_format)  # drugs
                sheet1.set_column('E:E', 9, cell_format) # dose
                sheet1.set_column('F:F', 50, my_format) # notes
                sheet1.set_column('G:G',13,cell_format) # Date

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 12})
                main_cell.set_align('center')
                #sheet1.set_row(0, None, cell_format)
                #sheet1.set_row(1, None, cell_format)
                #sheet1.set_row(2, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 0, 0, 5, 'Premedication and chemotherapy', main_cell)

                sheet1.write(1, 1, ' From')
                sheet1.write(1, 3, str (date_from))
                #sheet1.write(1, 3, ' Patient ID ')
                sheet1.write(1, 4, 'To')
                sheet1.write(1, 5, str (date_to))
                sheet1.write(2, 1, 'Patient Name')
                sheet1.write(2, 2, ' Patient ID ')
                sheet1.write(2, 3, 'Drug')
                sheet1.write(2, 4, 'Dose')
                sheet1.write(2, 5, 'Notes')
                sheet1.write(2, 6, 'Date')

                numb = 1
                exist = []
                #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                #sss=self.tableWidget_8.selectionModel().selectedRows()
               # for i in sss:
                #    print(i.row())

                for currentRow in range(self.tableWidget_8.rowCount()):
                    for currentColumn in range(self.tableWidget_8.columnCount()):
                        try:
                            teext = str(self.tableWidget_8.item(currentRow, currentColumn).text())
                            
                            if currentColumn == 0: 
                                #print(teext)
                                #print("=====")
                                if not teext:teext = str(self.tableWidget_8.item(currentRow,currentColumn).data(1))
                                #print(teext)
                                #print("=====")
                            if currentColumn == 0:
                                if teext and teext.strip()!="" and teext not in exist:
                                    exist.append(teext)
                                    sheet1.write(currentRow +3,currentColumn+1,str(teext))
                                    if currentColumn == 0:
                                        sheet1.write(currentRow+3,0,str(numb))
                                        numb=numb+1

                            else:
                                sheet1.write(currentRow+3,currentColumn+1,str(teext))

                   #         sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError as xx:
                            print(xx,"1984")
                            pass
                wb.close()
                
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            pass
            print(m,"1905")
    def Ptt(self): # premedication row selected to excel
        
        try:
            
            date_from = self.dateEdit_11.date().toPyDate()   ####################### 
            date_to = self.dateEdit_12.date().toPyDate()
            path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(11)
                cell_format.set_align('center')

                my_format = wb.add_format({'bold': False})
                my_format.set_font_size(11)
                my_format.set_align('left')


                sheet1.set_column('A:A', 6, cell_format)
                sheet1.set_column('B:B', 28, cell_format) # patient name
                sheet1.set_column('C:C', 14, cell_format) # pt id
                sheet1.set_column('D:D', 19, my_format)  # drugs
                sheet1.set_column('E:E', 9, cell_format) # dose
                sheet1.set_column('F:F', 50, my_format) # notes
                sheet1.set_column('G:G',13,cell_format) # Date

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 12})
                main_cell.set_align('center')
                #sheet1.set_row(0, None, cell_format)
                #sheet1.set_row(1, None, cell_format)
                #sheet1.set_row(2, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 0, 0, 5, 'Premedication And Chemotherapy', main_cell)

                sheet1.write(1, 1, ' From')
                sheet1.write(1, 3, str (date_from))
                #sheet1.write(1, 3, ' Patient ID ')
                sheet1.write(1, 4, 'To')
                sheet1.write(1, 5, str (date_to))
                sheet1.write(2, 1, 'Patient Name')
                sheet1.write(2, 2, ' ID')
                sheet1.write(2, 3, 'Drug')
                sheet1.write(2, 4, 'Dose')
                sheet1.write(2, 5, 'Notes')
                sheet1.write(2, 6, 'Date')

                numb = 1
                exist = []
                sss=self.tableWidget_8.selectionModel().selectedRows()
                rowExcel=-1
                for z in sss:
                    currentRow=z.row()
                    rowExcel=rowExcel+1
                    for currentColumn in range(self.tableWidget_8.columnCount()):
                        try:
                            teext = str(self.tableWidget_8.item(currentRow, currentColumn).text())                         
                            if currentColumn == 0: 
                                if not teext:teext = str(self.tableWidget_8.item(currentRow,currentColumn).data(1))
                            if currentColumn == 0:
                                if teext and teext.strip()!="" and teext not in exist:
                                    exist.append(teext)
                                    sheet1.write(rowExcel +3,currentColumn+1,str(teext))
                                    if currentColumn == 0:
                                        sheet1.write(rowExcel+3,0,str(numb))
                                        numb=numb+1

                            else:
                                sheet1.write(rowExcel+3,currentColumn+1,str(teext))

                   #         sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError as xx:
                            print(xx,"1980")
                            pass
                wb.close()   #   left it when u have time 
                
                self.statusBar().showMessage('Report Created Successfully',5000)
        except Exception as m:
            print(m,"1986")
            pass
#############################################################################################################  
    def Ptt2(self): # tablewidget_4 work when selection rows only 
        
        try:
            
            date_from = self.dateEdit_6.date().toPyDate()   ####################### is it ok?  but the excel sheet differ which function is for excel? 
            date_to = self.dateEdit_5.date().toPyDate()
            path = "c:\\users\\{0}\\desktop".format(getpass.getuser())
            filename, _ = QFileDialog.getSaveFileName(self, 'Save File', path, ".xlsx(*.xlsx)")
            if filename:
                wb = Workbook(filename)
                sheet1 = wb.add_worksheet()

                cell_format = wb.add_format({'bold': False})
                cell_format.set_font_size(11)
                cell_format.set_align('center')

                my_formate = wb.add_format({'bold': False})
                my_formate.set_font_size(11)
                my_formate.set_align('left')

                main_cell = wb.add_format({'bold': True, 'bg_color': 'yellow', 'font_size': 12})
                main_cell.set_align('center')
                sheet1.set_column('I:I',12,cell_format) ############### Date
                sheet1.set_column('A:A',5,cell_format) ################# numbering
                sheet1.set_column('D:D',18,my_formate) # drugs
                sheet1.set_column('C:C',10,cell_format)  # pt id
                sheet1.set_column('G:G',4,cell_format)  # volume field
                sheet1.set_column('E:E',10,my_formate)  # Dose
                sheet1.set_column('H:H',50,my_formate) #  note 
                sheet1.set_column('F:F',12,my_formate) #  fluid
                sheet1.set_column('B:B',26,cell_format) # pt name
                #sheet1.set_column(1,7,30,cell_format)  # note field


                #sheet1.set_row(0, None, cell_format)
               # sheet1.set_row(1, None, cell_format)
                sheet1.set_row(2, None, main_cell)
                sheet1.merge_range(0, 1, 0, 7, 'General Search', cell_format)
                sheet1.write(1, 1, ' From ')
                sheet1.write(1, 2, str(date_from))
                sheet1.write(1, 4, ' To ')
                sheet1.write(1,5, str(date_to))
                sheet1.write(2, 1, 'Patient Name')  ###############  i increases all cols +1      thi
                sheet1.write(2, 2, 'ID')
                sheet1.write(2, 3, 'Drug')
                sheet1.write(2, 4, 'Dose')
                sheet1.write(2, 5, 'Fluid')
                sheet1.write(2, 6, 'Vol')
                sheet1.write(2, 7, 'Note')
                sheet1.write(2, 8, 'Date')
                numb =1
                exists = []  ############################################################################################  1   steps to prevent repeating names in excel
                sss=self.tableWidget_4.selectionModel().selectedRows()
                rowExcel=-1
                for z in sss:
                    currentRow=z.row()     # i think it clear selection
                    rowExcel=rowExcel+1
                    for currentColumn in range(self.tableWidget_4.columnCount()):
                        try:
                            teext = str(self.tableWidget_4.item(currentRow, currentColumn).text())                         
                            if currentColumn == 0: 
                                if not teext:teext = str(self.tableWidget_4.item(currentRow,currentColumn).data(1))
                            if currentColumn == 0:
                                if teext and teext.strip()!="" and teext not in exists:
                                    exists.append(teext)
                                    sheet1.write(rowExcel +3,currentColumn+1,str(teext))
                                    if currentColumn == 0:
                                        sheet1.write(rowExcel+3,0,str(numb))
                                        numb=numb+1

                            else:
                                sheet1.write(rowExcel+3,currentColumn+1,str(teext))

                   #         sheet1.write(currentRow + 4, currentColumn, str(teext))
                        except AttributeError as xx:
                            print(xx,"2150")
                            pass
                wb.close()
                
                self.statusBar().showMessage('Report Created Successfully',5000)#change it to allow selection of rows no/ 
        except Exception as m:
            print(m,"2156")
            pass
#####################################################################################################################

    def premedication_fun(self):# premedication Tab F12
        global loaded
        loaded=False
        try:
            #main_category = -1
            main_category = self.comboBox_6.currentIndex()
    #0 chemo    1   prem..  2 all   no  2 is fluid but i not need it i need 0 and 1 to show and all which number in combobox? i will delet fluid and put all ok so 2 is all ok
            if main_category==0:
                main_category2=1
            elif main_category==1:
                main_category2=2
            else:#2 for all
                main_category=0
                main_category2=2


            date_from = self.dateEdit_11.date().toPyDate()
            date_to = self.dateEdit_12.date().toPyDate()
    #
            self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose , p.note , p.date,p.is_checked FROM prescription_detail as p 
                                    JOIN drugs as d ON p.drug = d.id
                                    LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                    LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                    WHERE p.date BETWEEN %s AND  %s and d.main_category >= %s and d.main_category < %s
                                    ORDER BY p.date desc, p.id desc 
                                    ''', (date_from, date_to,main_category,main_category2))
            #main_category2==0:


            full_search = self.cur.fetchall()
            self.tableWidget_8.clearSelection()
            while self.tableWidget_8.rowCount() > 0:
                self.tableWidget_8.removeRow(0)
                self.tableWidget_8.clearSelection()
            noduplicates=[]
            colors=["#ccffff","#F1D4F1"]##ccffff
            colornum=0
            for row_number, items in enumerate(full_search):
                self.tableWidget_8.insertRow(row_number)
                #print(items)
                for column_number, item in enumerate(items):
                            ######################################################################################  add checked to premedication tab
                    if column_number == 6:  
                        if item == 0:
                            chkBoxItem = QTableWidgetItem()
                            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(Qt.Unchecked)
                            chkBoxItem.setData(LastStateRole,0)
                            self.tableWidget_8.setItem(row_number, column_number, chkBoxItem)

                        else:
                            chkBoxItem = QTableWidgetItem()
                            chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                            chkBoxItem.setCheckState(Qt.Checked)
                            chkBoxItem.setData(LastStateRole,1)
                            self.tableWidget_8.setItem(row_number, column_number, chkBoxItem)
                            self.check_color_green1(row_number)

                    if column_number==0:
                        if not item in noduplicates:
                            noduplicates.append(item)
                            cell = QTableWidgetItem(str(item))
                            cell.setTextAlignment(Qt.AlignHCenter)
                            colornum=not colornum
                            
                            cell.setBackground(QColor(colors[colornum]))
                            self.tableWidget_8.setItem(row_number, column_number, cell)

                        else:
                            cell = QTableWidgetItem(" ")
                            cell.setText(" ")
                            cell.setTextAlignment(Qt.AlignHCenter)
                            #cell.setBackground(QColor("blue"))
                            #cell.setData(2,item)
                            cell.setData(1,item)
                            cell.setBackground(QColor(colors[colornum]))
                            self.tableWidget_8.setItem(row_number, column_number, cell)

                    elif column_number!=6:
                        #print(column_number)
                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_8.setItem(row_number, column_number, cell)
            loaded=True
        except Exception as e:
            print(e)
            pass


#################################################################################################################
##################################################################################################################
###############################################################################################################
  #  def filter3(self):
   #     global loaded
    #    loaded=False
     #   numbering=0
      #  try:
       #     date_from = self.dateEdit_17.date().toPyDate()
        #    date_to = self.dateEdit_13.date().toPyDate()
#
 #           called = self.lineEdit_21.text()
  #          called=called+"%"
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
   #         hide=self.lineEdit_22.text()  # hide others
    #        hide.self.lineEdit_22 = QLineEdit()
     #       hide.self.lineEdit_22.setPlaceholderText("search Name - Hide the rest")
      ##      #self.layout.addWidget(self.leditHide)
            
        #    coloor=self.lineEdit_23.text()
         #   coloor.self.lineEdit_23 = QLineEdit()
          #  coloor.self.lineEdit_23.setPlaceholderText("search Name - Color result green")
           # #self.layout.addWidget(self.leditColor)

            #self.lineEdit_22.textChanged.connect(
             #   lambda: self.result(self.lineEdit_22.text()))
           # self.lineEdit_23.textChanged.connect(
           #     lambda: self.result(self.lineEdit_23.text(), color=True))
           # self.setLayout(self.layout)
            # Show window
            #self.show()
    
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
       #     main_category=self.comboBox_8.currentIndex()
        #    if (main_category==1):
        #        main_category=1#chemo =0 ok? yes
         #   else:
          #      main_category=2

          #  self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose ,p.fluid , p.volume , p.note ,
           #                      p.date,p.is_checked , p.prescription_no,pname.id,p.id_checked FROM prescription_detail as p 
           #                     JOIN drugs as d ON p.drug = d.id
            #                    LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
             #                   LEFT JOIN patient as pname ON pid.patient_id = pname.id 
              #                  WHERE p.date BETWEEN %s AND  %s and d.main_category<%s and p.is_checked>0 and pname.name LIKE %s
               #                 ORDER BY p.id_checked asc
                #                ''', (date_from, date_to,main_category,called))#BY p.date desc, p.id desc    
                 
   #         full_search = self.cur.fetchall()   #   p.id_checked asc   #  p.date desc, p.id desc,pid.id desc

    #        self.tableWidget_9.clearSelection()
     #       while self.tableWidget_9.rowCount() > 0:
      #          self.tableWidget_9.removeRow(0)
       #         self.tableWidget_9.clearSelection() #  1 no duplication in general search in program
        #    noduplicates = []  ############################################### 3   
         #   colors=["#ccffff","#F1D4F1"]##ccffff
          #  colornum=0
           # for row_number, items in enumerate(full_search):
            #    self.tableWidget_9.insertRow(row_number)
             #   for column_number, item in enumerate(items):
              #      column_number=column_number+1

               #     if column_number==8 or column_number==10:continue#/ 8 date / 10 presctiption_no
                #    if column_number == 5:
                 #       self.cur.execute('''SELECT drug_name From drugs WHERE id = %s''', (item,))
                  #      drug_name = self.cur.fetchone()
                   #     cell = QTableWidgetItem(str(drug_name[0]))
                    #    cell.setTextAlignment(Qt.AlignHCenter)
                     #   cell.setBackground(QColor(colors[colornum]))
                      #  self.tableWidget_9.setItem(row_number, column_number, cell)

#                    elif column_number == 1:         #####################################  4
 #                       cell = QTableWidgetItem()  ########################### 7
  #                      cell.setTextAlignment(Qt.AlignHCenter)  ###################### 8
   #                     celll=QTableWidgetItem()
    #                    celll.setTextAlignment(Qt.AlignHCenter)
                        
     #                   if item and item not in noduplicates:  ###################################5
      #                      noduplicates.append(item)  ##################################  6
       ##            #         self.tableWidget_4.setForeground(QColor('white'))  ############10
         #                   cell.setText(str(item))
          #                  colornum=not colornum
           #                 cell.setBackground(QColor(colors[colornum]))
            #                numbering=numbering+1
             #               celll.setText(str(numbering))
              #              celll.setBackground(QColor(colors[colornum]))

               #         else:
                #            cell.setBackground(QColor(colors[colornum]))
#
 #                           cell1 = QTableWidgetItem()  ########################### 7
  #                          cell1.setTextAlignment(Qt.AlignHCenter)  ###################### 8
   #                         cell1.setBackground(QColor(colors[colornum]))
    #                        cell.setData(1,item)
                            
     #                   self.tableWidget_9.setItem(row_number, column_number, cell)  ######  9
      #                  self.tableWidget_9.setItem(row_number, 0, celll)

       #             else:
        #                cell = QTableWidgetItem(str(item))
         #               cell.setTextAlignment(Qt.AlignHCenter)
          #              cell.setBackground(QColor(colors[colornum]))
           #             self.tableWidget_9.setItem(row_number, column_number, cell)
            #loaded=True
        #except Exception as e:
         #   print("error 1974",e)
          #  pass
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  #  @pyqtSlot()
   # def on_click(self):
    #    print("\n")
     #   for currentQTableWidgetItem in self.tableWidget_9.selectedItems():
      #      print(currentQTableWidgetItem.row(),
       #           currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  ###  @pyqtSlot()
    ###def filter3(self, txt, color=False):
     ###   self.txt = txt

      ###  if self.txt != "":
      ###      for i in range(self.tableWidget_9.rowCount()):
         ###       if self.tableWidget_9.item(i, 1).text().lower().startswith(self.txt.lower()):
            ###        if color == True:
               ###         for j in range(self.tableWidget_9.columnCount()):  ###  for coloring 1
                  ###          self.tableWidget_9.item(i,j).setBackground(QColor(0,255,0)) ### for coloring  2
                       # self.tableWidget_9.item(
                      #      i, 0).setBackground(QColor(0, 255, 0))
                      #  self.tableWidget_9.item(
                       #     i, 1).setBackground(QColor(0, 255, 0))
               ###     else:
                  ###      self.tableWidget_9.showRow(i)

   ###             else:
      ###              if color == True:
         ###               for j in range(self.tableWidget_9.columnCount()): #  coloring 3
            ###                self.tableWidget_9.item(i,j).setBackground(QColor(255,255,255))  #  coloring 4

                        #self.tableWidget_9.item(i, 0).setBackground(
                         #   QColor(255, 255, 255))
                        #self.tableWidget_9.item(i, 1).setBackground(
                         #   QColor(255, 255, 255))
               ###     else:
                  ###      self.tableWidget_9.hideRow(i)
  ###      else:
     ###       for i in range(self.tableWidget_9.rowCount()):
        ###        for j in range(self.tableWidget_9.columnCount()): #  coloring 5
           ###         self.tableWidget_9.item(i, j).setBackground(QColor(255, 255, 255)) #   coloring 6
              ###  self.tableWidget_9.showRow(i)

                #self.tableWidget_9.item(i, 0).setBackground(
                #    QColor(255, 255, 255))
               # self.tableWidget_9.item(i, 1).setBackground(
              #      QColor(255, 255, 255))
             #  self.tableWidget_9.showRow(i)
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    @pyqtSlot()
    def filter3(self, txt, color=False,keep_color=False):  # checked tab  filter by name of patient
        self.txt = txt
        self.color = color
        self.keep_color=keep_color
        self.match_found = False

        def show_color_Row(row_number: int, showRow: bool = True, colorRow: bool = False) -> None:
            for j in range(self.tableWidget_9.columnCount()):
                if colorRow == True and self.keep_color==False:
                    self.tableWidget_9.item(
                        row_number, j).setBackground(QColor(0, 255, 0))
                else:
                    if self.keep_color==False and colorRow==True:
                        self.tableWidget_9.item(
                            row_number, j).setBackground(QColor(255, 255, 255))

                if showRow == False:
                    self.tableWidget_9.hideRow(i)
                else:
                    self.tableWidget_9.showRow(i)

        for i in range(self.tableWidget_9.rowCount()):
            if self.txt != "":
                if self.tableWidget_9.item(i, 1).text().lower().startswith(self.txt.lower()):
                    self.match_found = True

                elif self.match_found == True and self.tableWidget_9.item(i, 0).text() == "":
                    self.match_found = True
                else:
                    self.match_found = False

                if self.match_found == True:
                    show_color_Row(i, colorRow=self.color)

                elif self.match_found == False and self.color == False:
                    show_color_Row(i, showRow=False)
                else:
                    show_color_Row(i)
            else:
                show_color_Row(i)

# FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF 4    
    
    def filter4(self):

        global loaded
        loaded=False
        whatToSearch=self.lineEdit_23.text()+"%"
        sql1='''select patient_id from prescription_no 
                    where id in(SELECT prescription_no FROM hospital.prescription_detail 
                    where drug in (SELECT id FROM hospital.drugs where drugs.drug_name like 'a%'));'''

        numbering=0
        try:
            date_from = self.dateEdit_17.date().toPyDate()
            date_to = self.dateEdit_13.date().toPyDate()

            main_category=self.comboBox_8.currentIndex()
            if (main_category==1):
                main_category=1#chemo =0 ok? yes
            else:
                main_category=2

            self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose ,p.fluid , p.volume , p.note , 
                                p.date,p.is_checked , p.prescription_no ,pname.id,p.id_checked FROM prescription_detail as p 
                                JOIN drugs as d ON p.drug = d.id
                                LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                WHERE p.date BETWEEN %s AND  %s and d.main_category<%s and p.is_checked>0 and pname.id in 
                                (select patient_id from prescription_no where id in
                                (SELECT prescription_no FROM hospital.prescription_detail where drug in 
                                (SELECT id FROM hospital.drugs where drug_name like %s)))
                                ORDER BY p.id_checked asc
                                ''', (date_from, date_to,main_category,whatToSearch,))#BY p.date desc, p.id desc    
               
            full_search = self.cur.fetchall()  #  asc
            list_search=[]
            index={}
            for x in full_search:
                if x[2].startswith(self.lineEdit_23.text()):
                    index[x[1]]=1
            for x in full_search:
                if x[1] in index:
                    list_search.append(x)
            full_search=list_search
            self.tableWidget_9.clearSelection()
            while self.tableWidget_9.rowCount() > 0:
                self.tableWidget_9.removeRow(0)
                self.tableWidget_9.clearSelection()
            
           # for x in full_search:
            #    print(x)
            noduplicates = []  ############################################### 3   
            colors=["#ccffff","#F1D4F1"]##ccffff
            colornum=0
            for row_number, items in enumerate(full_search):               
                self.tableWidget_9.insertRow(row_number)
                for column_number, item in enumerate(items):
                    column_number=column_number+1
                  
                    if column_number==8 or column_number>=10:continue#/ 8 date / 10 presctiption_no

                    if column_number == 5:
                        self.cur.execute('''SELECT drug_name From drugs WHERE id = %s''', (item,))
                        drug_name = self.cur.fetchone()
                        cell = QTableWidgetItem(str(drug_name[0]))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_9.setItem(row_number, column_number, cell)

                    elif column_number == 1:         #####################################  4                        
                        cell = QTableWidgetItem()  ########################### 7
                        cell.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                        cell1 = QTableWidgetItem()  ########################### 7
                        cell1.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                        if item and item not in noduplicates:  ###################################5
                            noduplicates.append(item)  ##################################  6
                   #         self.tableWidget_4.setForeground(QColor('white'))  ############10
                            cell.setText(str(item))
                            colornum=not colornum
                            cell.setBackground(QColor(colors[colornum]))
                            
                            numbering=numbering+1
                            #self.cur.execute('''select id from patient_number where patient_id=%s''',(str(items[-1]),))
                            #patient=self.cur.fetchall()
                            cell1.setText(" ")#str(numbering))
                            cell1.setBackground(QColor(colors[colornum]))
                            #print("ok")
                        else:
                            #print("item-++-->",item)self.tableWidget_9.item(i, 3).text()                           
                            cell.setBackground(QColor(colors[colornum]))
                            cell1 = QTableWidgetItem()  ########################### 7
                            cell1.setTextAlignment(Qt.AlignHCenter)  ###################### 8
                            cell1.setBackground(QColor(colors[colornum]))
                            #print("ok")
                            cell.setData(1,item)
                            
                            
                        self.tableWidget_9.setItem(row_number, column_number, cell)  ######  9
                        self.tableWidget_9.setItem(row_number, 0, cell1)  ######  9
                                                        
                    else:
                        if column_number==3 and self.tableWidget_9.item(row_number,0).text()==" ":
                            self.tableWidget_9.item(row_number,0).setText(ids[self.tableWidget_9.item(row_number,2).text()])
                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_9.setItem(row_number, column_number, cell)
            loaded=True
        except Exception as e:
            print("error 1974",e)
            pass
###############################################################################33   end


   # @pyqtSlot()
   # def filter4(self, txt='', tableName="tableWidget_9",filter_col=3,fill_text=True): # filter search by name of drug
   #     self.match_found=False
   #     self.populate=False

   #     def sort_rows():
     #       for i in range(getattr(self, tableName).rowCount()):
     #           if txt == "":
     #               self.match_found=False
      #              getattr(self, tableName).showRow(i)
      #              if fill_text:  # == true 
      #                  clean_up()

         #       elif getattr(self, tableName).item(i, filter_col).text().lower().startswith(txt.lower()):
         #           self.match_found=True
         #           getattr(self, tableName).showRow(i)

         #       elif self.match_found and getattr(self, tableName).item(i, filter_col).text() == "":
         #           self.match_found=True
         #           getattr(self, tableName).showRow(i)
         #       else:
         #           self.match_found=False
           #         getattr(self, tableName).hideRow(i)

     #   def populate():
      #      self.populate=True
       #     for i in range(getattr(self,tableName).rowCount()):
       #         if getattr(self,tableName).item(i,0).text()=='':
        #            getattr(self,tableName).setItem(i,1,QTableWidgetItem(getattr(self,tableName).item(i-1,1).text()))
        #            getattr(self,tableName).item(i,1).setBackground(getattr(self,tableName).item(i,0).background())
        #            getattr(self,tableName).item(i,1).setTextAlignment(Qt.AlignCenter)

       # def clean_up():
        #    getattr(self,tableName).selectAll()
       #     for i in getattr(self,tableName).selectedIndexes():
        #        _ = getattr(self,tableName).item(i.row(),1).text()
        #        for j in range (i.row()+1, int(len(getattr(self,tableName).selectedIndexes())/getattr(self,tableName).columnCount())):
        #            if getattr(self,tableName).item(j,1).text()== _ and getattr(self,tableName).item(j,1).text() != '':
         #               getattr(self,tableName).setItem(j,1,QTableWidgetItem(''))
           #             getattr(self,tableName).item(j,1).setBackground(getattr(self,tableName).item(j,0).background())
          #          continue
         #   getattr(self,tableName).clearSelection()
         #   self.populate=False
       # if fill_text and self.populate==False:
       #     populate()
       # sort_rows()

####$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ FFFFFFFFF4
    @pyqtSlot()
    def filter2(self, txt, color=False,keep_color=False):  # checked tab  filter by name of drug
        self.txt = txt
        self.color = color
        self.keep_color=keep_color
        self.match_found = False

        def show_color_Row(row_number: int, showRow: bool = True, colorRow: bool = False) -> None:
            for j in range(self.tableWidget_8.columnCount()):
                if colorRow == True and self.keep_color==False:
                    self.tableWidget_8.item(
                        row_number, j).setBackground(QColor(0, 255, 0))
                else:
                    if self.keep_color==False and colorRow==True:
                        self.tableWidget_8.item(
                            row_number, j).setBackground(QColor(255, 255, 255))

                if showRow == False:
                    self.tableWidget_8.hideRow(i)
                else:
                    self.tableWidget_8.showRow(i)

        for i in range(self.tableWidget_8.rowCount()):
            if self.txt != "":
                if self.tableWidget_8.item(i, 0).text().lower().startswith(self.txt.lower()):
                    self.match_found = True

                elif self.match_found == True and self.tableWidget_8.item(i, 0).text() == "":
                    self.match_found = True
                else:
                    self.match_found = False

                if self.match_found == True:
                    show_color_Row(i, colorRow=self.color)

                elif self.match_found == False and self.color == False:
                    show_color_Row(i, showRow=False)
                else:
                    show_color_Row(i)
            else:
                show_color_Row(i)

   
    """
    def filter2(self): # premedication tab  with query
        global loaded
        loaded=False

        #main_category = -1
        main_category = self.comboBox_6.currentIndex()
        if main_category==0:
            main_category2=1
        elif main_category==1:
            main_category2=2
        else:#2 for all
            main_category=0
            main_category2=2
        date_from = self.dateEdit_11.date().toPyDate()
        date_to = self.dateEdit_12.date().toPyDate()

        called = self.lineEdit_20.text()
        called = called+'%'

#
        self.cur.execute('''SELECT  pname.name ,pname.number, d.drug_name , p.dose , p.note , p.date,p.is_checked FROM prescription_detail as p 
                                JOIN drugs as d ON p.drug = d.id
                                LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                WHERE p.date BETWEEN %s AND  %s and d.main_category>=%s and d.main_category<%s and pname.name LIKE %s
                                ORDER BY p.date desc, p.id desc 
                                ''', (date_from, date_to,main_category,main_category2,called))
        full_search = self.cur.fetchall()
        self.tableWidget_8.clearSelection()
        while self.tableWidget_8.rowCount() > 0:
            self.tableWidget_8.removeRow(0)
            self.tableWidget_8.clearSelection()
        noduplicates=[]
        colors=["#ccffff","#F1D4F1"]##ccffff
        colornum=0
        for row_number, items in enumerate(full_search):
            self.tableWidget_8.insertRow(row_number)
            #print(items)
            for column_number, item in enumerate(items):
                        ######################################################################################  add checked to premedication tab
                if column_number == 6:  
                    if item == 0:
                        chkBoxItem = QTableWidgetItem()
                        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(Qt.Unchecked)
                        chkBoxItem.setData(LastStateRole,0)
                        self.tableWidget_8.setItem(row_number, column_number, chkBoxItem)

                    else:
                        chkBoxItem = QTableWidgetItem()
                        chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                        chkBoxItem.setCheckState(Qt.Checked)
                        chkBoxItem.setData(LastStateRole,1)
                        self.tableWidget_8.setItem(row_number, column_number, chkBoxItem)
                        self.check_color_green1(row_number)

                if column_number==0:
                    if not item in noduplicates:
                        noduplicates.append(item)
                        cell = QTableWidgetItem(str(item))
                        cell.setTextAlignment(Qt.AlignHCenter)
                        colornum=not colornum
                        
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_8.setItem(row_number, column_number, cell)

                    else:
                        cell = QTableWidgetItem(" ")
                        cell.setText(" ")
                        cell.setTextAlignment(Qt.AlignHCenter)
                        #cell.setBackground(QColor("blue"))
                        #cell.setData(2,item)
                        cell.setData(1,item)
                        cell.setBackground(QColor(colors[colornum]))
                        self.tableWidget_8.setItem(row_number, column_number, cell)

                elif column_number!=6:
                    #print(column_number)
                    cell = QTableWidgetItem(str(item))
                    cell.setTextAlignment(Qt.AlignHCenter)
                    cell.setBackground(QColor(colors[colornum]))
                    self.tableWidget_8.setItem(row_number, column_number, cell)
        loaded=True
        """
        #self.cur.execute(''' SELECT d.drug_name , SUM(p.dose) FROM prescription_detail as p 
         #                   LEFT JOIN drugs AS d ON p.drug = d.id 
        #                    WHERE d.main_category =%s AND p.date BETWEEN %s AND  %s 
        #                    GROUP BY d.id
         #                   ORDER BY p.date, d.drug_name 
#
        #                    ''', (main_category, date_from, date_to))
        #all_drugs = self.cur.fetchall()#dose
        #self.cur.execute(''' SELECT d.drug_name , SUM(p.volume) FROM prescription_detail as p 
        #                    LEFT JOIN drugs AS d ON p.fluid = d.id 
        #                    WHERE d.main_category =%s AND p.date BETWEEN %s AND  %s 
        #                    GROUP BY d.id
       #                     ORDER BY p.date, d.drug_name 
        #                    ''', (main_category, date_from, date_to))
       # all_fluid = self.cur.fetchall()#volume
#SQL1:  PATIENT_NAME,PATIENT_ID FROM...WHERE DRUG=COMBOBOX CATEGORY
        #while self.tableWidget_8.rowCount() > 0:
        #    self.tableWidget_8.removeRow(0)
        #    self.tableWidget_8.clearSelection()
       # for row_number, items in enumerate(all_fluid):
        #    self.tableWidget_8.insertRow(row_number)
        #    for column_number, item in enumerate(items):
       #         cell = QTableWidgetItem(str(item))
       #         cell.setTextAlignment(Qt.AlignHCenter)
       #         cell.setBackground(QColor("blue"))
       #         self.tableWidget_8.setItem(row_number, column_number+2, cell)
       # for row_number, items in enumerate(all_drugs):
       #     self.tableWidget_8.insertRow(row_number)
        #    for column_number, item in enumerate(items):
         #       if column_number == 1:
         ##           data = str(item)
        #            if data.split(".")[-1] == "0":
                        #print("here")
         #               cell = QTableWidgetItem(str(data.split(".")[0]))
         #               cell.setTextAlignment(Qt.AlignHCenter)
         #               cell.setBackground(QColor("red"))
         #               self.tableWidget_8.setItem(row_number, column_number+2, cell)
         #           else:
         #               new = round(item, 2)
         #               cell = QTableWidgetItem(str(new))
         #               cell.setTextAlignment(Qt.AlignHCenter)
         #               cell.setBackground(QColor("yellow"))
         #               self.tableWidget_8.setItem(row_number, column_number+2, cell)
         #       else:
         #           cell = QTableWidgetItem(str(item))
         #           cell.setTextAlignment(Qt.AlignHCenter)
         #           cell.setBackground(QColor("magenta"))
        #            self.tableWidget_8.setItem(row_number, column_number+2, cell)

    


    ###########################################################################################################################################  premedicatins 

#class login(QMainWindow,FORM_CLASS2):
 #   def __init__(self, parent=None):
  #      super(login, self).__init__(parent)
   #     QMainWindow.__init__(self)
    #    self.setupUi(self)
     #   self.pushButton200.clicked.connect(self.enter)

    #def enter(self):
     #   username = self.lineEdit200.text()
      #  password = self.lineEdit300.text()
        
       # try:
        #    connection = pymysql.connect(host='localhost',db='hospital',user=username,password=password, use_unicode=True,charset="utf8")
         #   cur = connection.cursor()
          #  #self.messagebox('good','connected')
           # self.main=Main()
            #self.main.setWindowTitle('Oncology Pharmacy')
            #self.main.setWindowIcon(QIcon('v.png'))
            #self.main.setFixedSize(1100, 700)
            #self.main.setWindowIcon(QIcon('v.png'))
            #self.main.show()
            #self.close()
        #except Exception as e:
         #   print(e)
          #  self.warning('Wrong','wrong pass or name')
           # self.lineEdit200.setText('')
            #self.lineEdit300.setText('') 

    #def messagebox(self,title,message):
     #   mess = QtWidgets.QMessageBox()
      #  mess.setWindowTitle(title)
       # mess.setText(message)
        #mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        #mess.exec_()

    #def warning(self,title,message):
     #   mess = QtWidgets.QMessageBox()
      #  mess.setWindowTitle(title)
       # mess.setText(message)
        #mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        #mess.exec_()

    def createTable(self):

        global loaded
        global ids
        patients=200;parts=6
        loaded=False
        numbering=0
        color=[QColor("#FFFF7F"),QColor("#00FF7F"),QColor("#000000")]
        try:
            date_from = self.dateEdit_16.date().toPyDate()
            date_to = self.dateEdit_18.date().toPyDate()

            main_category=self.comboBox_9.currentIndex()#0 all 1 chemo 2 supportive=>db chemo=0,supportive=1,all=[0,1]
            if (main_category==0):#all  0=<x<2  =>0,1
                main_category=2
                main_categoryUP=0
            elif (main_category==1):#chemo   0=<x<1 => 0
                main_category=1
                main_categoryUP=0
            elif (main_category==2):#supportive   1=<x<2 =>1
                main_category=2
                main_categoryUP=1
                
            self.cur.execute('''SELECT  pname.name ,pname.number,  
                                p.date,p.is_checked , p.prescription_no ,pname.id,p.id_checked,d.main_category FROM prescription_detail as p 
                                JOIN drugs as d ON p.drug = d.id
                                LEFT JOIN prescription_no as pid ON  pid.id = p.prescription_no 
                                LEFT JOIN patient as pname ON pid.patient_id = pname.id 
                                WHERE p.date BETWEEN %s AND  %s and d.main_category<%s and d.main_category>=%s and p.is_checked>0
                                ORDER BY p.id_checked asc
                                ''', (date_from, date_to,main_category,main_categoryUP))#BY p.date desc, p.id desc    
                 
            full_search = self.cur.fetchall()  #  asc
            colorList=[]
            colorCheck=[]
            tempList=[]
            tempListId=[]
            for x in full_search:
               # print("category=",x[7],x[1])
                if x[0] not in tempList:
                    tempList.append(x[0])
                    tempListId.append(x[1])
                    colorList.append(int(x[7]))
                    colorCheck.append(-1)
                else:
                    index=tempList.index(x[0])
                    if colorList[index]==int(x[7]):
                        pass
                    else:
                        colorCheck[index]=0

            patients=len(tempList)
        except Exception as e:
            print("error 1974",e)
            full_search=[]
            tempList=[]
            patients=len(full_search)
        self.tableWidget_10.clearSelection()
        while self.tableWidget_10.rowCount() > 0:
            self.tableWidget_10.removeRow(0)
            self.tableWidget_10.clearSelection()
        if patients>0:
            while True:
                numberInRow=int(patients/parts)
                if patients%parts!=0:
                    numberInRow=int(numberInRow)+1
                if numberInRow<20 and parts>1:
                    parts=parts-1
                else:
                    break
            self.tableWidget_10.setRowCount(numberInRow)
            self.tableWidget_10.setColumnCount(3*parts)
            strs = ["No", "Name", "id"]*parts
            self.tableWidget_10.setHorizontalHeaderLabels(strs)
            no=1
            #self.tableWidget_10.setShowGrid(False)
            
            for i in range(1,parts+1):
                #print(i)
                for j in range(numberInRow):
                    self.tableWidget_10.setItem(j,i*3-3, QTableWidgetItem(str(no)))
                    self.tableWidget_10.setItem(j,i*3-2, QTableWidgetItem(tempList[no-1]))
                    self.tableWidget_10.setItem(j,i*3-1, QTableWidgetItem(tempListId[no-1]))
                    # self.tableWidget_10.setItem(j,i*4-1, QTableWidgetItem(str("")))
                    if colorCheck[no-1]==-1:
                        color1=colorList[no-1]
                    else:
                        color1=0
                   # print(j,i*4-1)
                    self.tableWidget_10.item(j,i*3-3).setBackground(color[color1])
                    self.tableWidget_10.item(j,i*3-2).setBackground(color[color1])
                    self.tableWidget_10.item(j,i*3-1).setBackground(color[color1])
                    self.tableWidget_10.item(j,i*3-2).setData(1,color[color1])
                    if no>=patients:break
                    no=no+1

    @pyqtSlot()
    def filter5(self, txt, color=False,keep_color=False):  # screen tab  filter by name of patient
        self.txt = txt
        self.color = color
        self.keep_color=keep_color
        self.match_found = False

        def show_color_Row(row_number: int, column_number,color) -> None:
                    for j in range(-1,2):#-1,0,1
                        
                        if self.tableWidget_10.item(row_number, column_number+j):
                            self.tableWidget_10.item(row_number, column_number+j).setBackground(color)

#QColor(0, 255, 0) ,QColor(255, 255, 255)
        for i in range(self.tableWidget_10.rowCount()):
            for j in range (1,self.tableWidget_10.columnCount(),3):
            
                if self.txt != "" and self.tableWidget_10.item(i,j):
                    if self.tableWidget_10.item(i, j).text().lower().startswith(self.txt.lower()):
                        self.match_found = True
                        show_color_Row(i, j,QColor(255,87, 51))  
                    else:
                        aa=self.tableWidget_10.item(i, j).data(1)
                        if aa:
                            show_color_Row(i, j,aa)
                        else:
                            show_color_Row(i, j,QColor(51, 255, 252))
#######################################################  0, 255, 0    ,  255, 255, 255
'''App Exicution'''

def main():
    app = QApplication(sys.argv)
    CheckBox_Style = CheckBoxStyle(app.style())   ###############   to centralize checkbox 
    app.setStyle(CheckBox_Style)                  ###############   to centralize checkbox    

    #mn = QtWidgets.QMainWindow()
    #mn = login()
    #ui.setupUi(mn)
   # mn.show()
    window = Main()
    #window.show()
    window.setWindowTitle('Oncology Pharmacy')
   # window.setupUi()
    window.setWindowIcon(QIcon('v.png'))
  #  window.setFixedSize(1340, 920)  # 1192 , 725
    window.show()
    #return
    #window = Main()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
