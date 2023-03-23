from widgets import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class Model:
    def __init__(self):
        self.name = None
        self.email = None
        self.contents = None
    def save(self):
        content = self.name+";"+self.email+"\n"
        with open('./data.csv','a') as file:
            file.write(content)
    def readFromFile(self):
        try:
            open('./data.csv','x')
        except:
            with open('./data.csv','r') as file:
                self.contents = file.readlines()
        return self.contents

class Controller:
    def __init__(self, /, model, view):
        self.model = model
        self.view = view
        self.labels = []
    def save(self, name, email):
        self.model.name = name
        self.model.email = email

        self.model.save()
    def read(self):
        return self.model.readFromFile()
    def clearLabels(self):
        for i in self.labels:
            i[0].setParent(None)
            i[1].setParent(None)
        self.labels = []
    def setLabels(self, labels):
        self.labels = labels
        


class View(Ui_MainWindow):
    def __init__(self):
        super().setupUi

    def setVariables(self):
        self.controller = None
        self.pushButton.clicked.connect(lambda: self.saveHandler())

    def setController(self, controller: Controller):
        self.controller = controller
        self.contents = self.controller.read()
        self.updateData()
    
    def saveHandler(self):
        if (self.controller is not None):
            name = self.lineEdit.text()
            email = self.lineEdit_2.text()
            if (len(name)>0 and len(email)>0):
                if (";" in name or ";" in email): return
                self.controller.save(name, email)
                self.updateData()
                self.lineEdit.setText("")
                self.lineEdit_2.setText("")
    
    def updateData(self):
        if self.controller is None: return
        labels = []
        self.controller.clearLabels()
        con = self.controller.read()
        for l, i in enumerate(con):
            name = i.split(";")[0]
            email = i.split(";")[1].replace("\n","")
            labels.append(self.addLabel(name, email, l+1))
        self.controller.setLabels(labels)
    
    def addLabel(self, name, email, length):
        labelName = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        labelEmail = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        labelName.setText(name)
        labelEmail.setText(email)
        self.formLayout_3.setWidget(length, QtWidgets.QFormLayout.LabelRole, labelName)
        self.formLayout_3.setWidget(length, QtWidgets.QFormLayout.FieldRole, labelEmail)
        return labelName, labelEmail



class App:
    def __init__(self, mainWindow):
        view = View()
        view.setupUi(mainWindow)
        view.setVariables()
        model = Model()
        controller = Controller(model=model, view=view)
        view.setController(controller)
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = App(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())