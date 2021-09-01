# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt6 UI code generator 6.1.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from threading import Timer
import datetime
api_key = '612e5f66a5b1200007c6a166'
api_secret = 'b56ac500-e935-4545-8184-5bcddb8980f2'

import pandas as pd
import time
from kucoin.client import Client


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(471, 600)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(30, 20, 81, 31))
        self.pushButton.setObjectName("pushButton")

        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(160, 20, 91, 31))
        self.lcdNumber.setObjectName("lcdNumber")


        self.list_widget = QtWidgets.QListWidget(Form)
        self.list_widget.setGeometry(QtCore.QRect(30, 80, 321, 491))

        self.list_widget.setStyleSheet('background-color:yellow')


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.startButton)

        self.timer = Timer(1,self.timerExpire)
        self.timer.start()
        self.currentTime = 0
        self.client = Client(api_key, api_secret,api_secret)

        self.ticker = self.client.get_ticker()
        self.df = pd.DataFrame(self.ticker['ticker'])


        self.usdtTable = self.df.loc[self.df['symbol'].str.contains("-USDT")]
        self.newUsdtTable0 = self.usdtTable[['symbol','buy']]



    def timerExpire(self):
        self.lcdNumber.display(str(datetime.timedelta(seconds=self.currentTime)))
        self.currentTime = self.currentTime + 1
        self.timer = Timer(1,self.timerExpire)
        self.timer.start()
        if self.currentTime%2 == 0:
            self.ticker = self.client.get_ticker()
            self.df = pd.DataFrame(self.ticker['ticker'])        
        
            self.usdtTable = self.df.loc[self.df['symbol'].str.contains("-USDT")]
            self.newUsdtTable1 = self.usdtTable[['symbol','buy']]
        
            
            for index, row in self.newUsdtTable1.iterrows():
                row["buy"] = round((100*(float(row["buy"]) - float(self.newUsdtTable0.loc[index,'buy']))/ float(self.newUsdtTable0.loc[index,'buy'])),2)
            
            
            sorted_df = self.newUsdtTable1.sort_values(by=['buy'], ascending=False)
            result = sorted_df.head(20)
            self.list_widget.clear()
            for ind in result.index:
                self.list_widget.insertItem(100,str(result["symbol"][ind])+ ": "+str(result["buy"][ind]))

    def startButton(self):  
        self.list_widget.clear()  
        self.currentTime = 0 
        self.ticker = self.client.get_ticker()
        self.df = pd.DataFrame(self.ticker['ticker'])
        self.usdtTable = self.df.loc[self.df['symbol'].str.contains("-USDT")]
        self.newUsdtTable0 = self.usdtTable[['symbol','buy']]



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Restart"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())




  


