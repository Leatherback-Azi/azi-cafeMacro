from config import config
import pickle


class userDataBase:
    isDataExist = False
    data = {
        'ID': '',
        'PW': '',
    }
    ID = data['ID']
    PW = data['PW']

    def __init__(self):
        self.readFile()

    def __repr__(self):
        return str(self.ID)

    def readFile(self):
        try:
            with open(config.DB_FILE, 'rb') as f:
                self.data = pickle.load(f)
                if self.data['ID']:         # 저장된 ID가 있을 시
                    self.ID = self.data['ID']
                    self.PW = self.data['PW']
                    self.isDataExist = True
                else:
                    self.isDataExist = False
                    self.saveFile('', '')
        except FileNotFoundError:
            self.isDataExist = False
            self.saveFile('', '')

    def saveFile(self, ID, PW):
        self.ID = str(ID)
        self.PW = str(PW)
        data = {
            'ID': str(ID),
            'PW': str(PW),
        }
        with open(config.DB_FILE, 'wb') as f:
            pickle.dump(data, f)
            if self.ID == '':
                self.isDataExist = False
            else:
                self.isDataExist = True

    def deleteFileData(self):
        data = {
            'ID': '',
            'PW': '',
        }
        with open(config.DB_FILE, 'wb') as f:
            pickle.dump(data, f)
            self.isDataExist = False
