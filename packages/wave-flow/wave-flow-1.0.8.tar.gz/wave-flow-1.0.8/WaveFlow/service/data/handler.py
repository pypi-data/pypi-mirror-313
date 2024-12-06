import pandas as pd

from WaveFlow.service.data.archive import Archive


class DataHandler:
    TYPE_DATA_ALLOWED:dict
    
    def __init__(self, fileReceived, *sepInCaseOfCSV) -> None:
        self.__sepInCaseOfCSV = sepInCaseOfCSV
        DataHandler.TYPE_DATA_ALLOWED = {'csv':self.__caseCSV,
                                      'xlsx':self.__caseXLSX,
                                      'json':self.__caseJSON}
        self.fileReceived = Archive(fileReceived)
        self.__dtypeToPD:dict={}


    def readFile(self):
        typeOf = self.fileReceived.getFileType()
        
        if typeOf in DataHandler.TYPE_DATA_ALLOWED.keys():
            self.fileReceived.setDataframe(
                DataHandler.TYPE_DATA_ALLOWED[typeOf](
                    self.fileReceived.getDesignatedFile()
                    )
                )
            
        elif typeOf not in DataHandler.TYPE_DATA_ALLOWED.keys():
            raise KeyError('Non Allowed Extension')

    
    def __caseCSV(self, file):
        return pd.read_csv(file, dtype=self.__dtypeToPD, sep=self.__sepInCaseOfCSV if self.__sepInCaseOfCSV else ";")


    def __caseXLSX(self, file):
        return pd.read_excel(file, dtype=self.__dtypeToPD)


    def __caseJSON(self, file):
        return pd.read_json(file, dtype=self.__dtypeToPD, convert_dates=False).astype(str)
    
        
    def getArchive(self) -> Archive:
        return self.fileReceived
    
    
    def setDtype(self, dtype:dict):
        "You must use again the method readFile() after use this one to confirm the dtype."
        self.__dtypeToPD = dtype
