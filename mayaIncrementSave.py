import maya.cmds as cmds
import datetime
import os

class mayaIncrementSave(object):
    def __init__(self):
        self.window = 'incrementSave'
        self.title = "Increment and Save"
        self.size = (205, 350)

    def buildUI(self):
        # Check to see if the window is already open
        if cmds.window(self.window, exists=True) == True:
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size, menuBar=True)

        # Creates a form layout to window
        self.mainForm = cmds.formLayout(numberOfDivisions=100)

        # Creates Stage of Production Radio Buttons
        cmds.frameLayout(label="Stage of Production")
        self.objType = cmds.radioCollection("stageSelection")
        modellingSelect = cmds.radioButton(label='Modelling')
        texturingSelect = cmds.radioButton(label='Texturing')
        riggingSelect = cmds.radioButton(label='Rigging')
        animationSelect = cmds.radioButton(label='Animation')
        lightingSelect = cmds.radioButton(label='Lighting')
        fxSelect = cmds.radioButton(label='FX')
        renderingSelect = cmds.radioButton(label='Rendering')
        randdSelect = cmds.radioButton(label='Research and Development')
        noneSelect = cmds.radioButton(label='None', select=True)

        # Adds Set Location Button
        self.btnFolderSet = cmds.button(label='Save Location', height=30, width=200, command=self.setFolderBtn)

        # Adds folder location textfield
        self.txtFieldFolderLocation = cmds.textField()

        cmds.frameLayout(label="Filename")

        self.txtFileName = cmds.textField(text = self.getFileName())

        # Adds Increment and Save Button
        self.btnSave = cmds.button(label='Increment and Save', height=30, width=200, command=self.saveBtn)

        # Renders the final UI
        cmds.showWindow()

    def setFolderBtn(self, *args):
        cmds.fileBrowserDialog(mode=4, fileCommand=self.linkFolder, actionName='Set Folder', operationMode='Reference')

    def linkFolder(self, fileName, fileType):
        cmds.textField(self.txtFieldFolderLocation, edit=True, text=fileName)

    def getFileName(self):
        # Gets current scene file name and takes the file extension off
        fullfilename = os.path.splitext(cmds.file(query=True, sceneName=True, shn=True))[0]
        if fullfilename == "" or None:
            return "scene name"
        else:
            return fullfilename.split(".")[0]

    def saveBtn(self, *args):
        # Gets Radio Button Selection
        radio = cmds.radioCollection("stageSelection", query=True, select=True)
        stage = cmds.radioButton(radio, query=True, label=True)
        if stage == "Research and Development":
            stage = "r&d"
        elif stage == "None":
            stage = ""
        stage = stage.lower()

        # Gets current time into the format of (DD.MM.YY)(HH.MM.SS)
        basePath = cmds.textField(self.txtFieldFolderLocation, query=True, text=True)
        currentDateTime = datetime.datetime.now().strftime("(%d.%m.%Y)(%H.%M.%S)")
        extension = os.path.splitext(cmds.file(query=True, sceneName=True, shn=True))[1]
        filename = os.path.splitext(cmds.file(query=True, sceneName=True, shn=True))[0].split(".")[0]
        prefix = filename.split(".")[0]

        try:
            increment = filename.split(".")[1]
        except IndexError:
            increment = "001"
        else:
            increment = str(int(increment) + 1).rjust(len(increment), '0')

        """if extension == ".ma":
            savetype = "mayaAscii"
        elif extension == ".mb":
            savetype = "mayaBinary"
        else:
            raise TypeError("Unknown fine extension. I can only save as Maya Ascii or Maya Binary")"""
        if stage == "":
            print(basePath + "/" + filename + " " + currentDateTime + "." + increment+extension)
            cmds.file(rename=basePath + "/" + filename + " " + currentDateTime + "." + increment+extension)
        else:
            print(basePath+"/"+filename+" "+currentDateTime+" "+stage+"."+increment+extension)
            cmds.file(rename=basePath+"/"+filename+" "+currentDateTime+" "+stage+"."+increment+extension)

incrementSave = mayaIncrementSave()
incrementSave.buildUI()