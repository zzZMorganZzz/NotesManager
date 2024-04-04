import json
import enum
from datetime import datetime


class TypeEdit(enum.Enum):
    create = 0
    edit = 1
    delete = 2
    restore = 3
    none = -1
    
class log:
    def __init__(self):
        self.typeAction ="TypeEdit.none"
        self.datetime = datetime.now()
    
    def __str__(self) -> str:
        return (f'[Type = {self.typeAction}] {self.datetime}')  


class Note:
    
    def __init__(self):
        self.Index = 0
        self.Description = ''
        self.Caption = ''
        self.CollectionEdit = []
        
    def __str__(self) -> str:
        return (f'[Index = {self.Index}] {self.Caption} ({self.Description}) ')
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def PrintNotes():
    for i in range(len(Notes)):
        print(Notes[i])
    MainMethod()
    
def PrintLog():
    print ('Укажите ID заметки:')
    Id = input()
    row = None
    for i in range(len(Notes)):
        if(int(Notes[i].Index)== int(Id)):
            row =Notes[i] 
    
    if (row!=None):
        for i in range(len(row.CollectionEdit)):
            print(row.CollectionEdit[i])
    else:
        print('Запись не найдена.')
    MainMethod ()

def FoundNote(Index):
    Result = None
    for i in range(len(Notes)):
        if(Notes[i].Index ==Index):
            return Notes[i]        
    return Result

def CreateNote (Caption,Description):
    global maxIndex
    nt = Note ()
    maxIndex+=1
    nt.Index = maxIndex
    nt.Caption = Caption
    nt.Description = Description
    _log = log()
    _log.typeAction = TypeEdit.create
    _log.datetime = datetime.now()
    nt.CollectionEdit.append(_log.__str__())
    Notes.append(nt)

def DeleteItem (index):
    IsDelete = False
    for i in range(len(Notes)):
        if (int(Notes[i].Index) ==int(index)):
            print(f'Запись {Notes[i].Index} удалена')
            Notes.remove(Notes[i])
            IsDelete = True
            break
    return IsDelete

def DeleteNote ():
    print ('Укажите индекс записи для удаления:')
    index = input()
    
    if (not DeleteItem(index)):
        print('запись не найдена')
    MainMethod()

def AddNewNote():
    print ('Укажите заголовок заметки:')
    Caption = input()
    print ('Укажите текст заметки:')
    Description = input()
    CreateNote (Caption,Description)
    print ('Запись сохранена.')
    MainMethod ()
    
def EditNote():
    print ('Укажите ID заметки:')
    Id = input()
    row = None
    for i in range(len(Notes)):
        if(int(Notes[i].Index)== int(Id)):
            row =Notes[i] 
    
    if (row!=None):
        print ('Укажите заголовок заметки:')
        Caption = input()
        print ('Укажите текст заметки:')
        Description = input()
        row.Caption = Caption
        row.Description=Description
        _log = log()
        _log.typeAction = TypeEdit.edit
        _log.datetime = datetime.now()
        row.CollectionEdit.append(_log.__str__())
        print('Изменение выполнено.')
    else:
        print('Запись не найдена, изменение недоступно.')
    MainMethod ()

with open("DB.json", "r") as f:
    data = json.load(f)

Notes = []

maxIndex = 0

for record in data:
    item = Note()
    item.Caption = record['Caption']
    item.Index = record['Index']
    item.Description = record['Description']
   
    
    if maxIndex<record['Index']:
        maxIndex = record['Index']
    
    for editRow in record['CollectionEdit']:
        item.CollectionEdit.append(editRow)
    Notes.append(item)
    
    
def ShowMenu ():
    print('1. Вывести все заметки\n'
          '2. Добавить новую запись\n'
          '3. Изменить заметку\n'
          '4. Посмотреть историю изменений заметки\n'
          '5. Удалить запись\n'
          '6. Закончить работу (Сохранить)', sep = '\n'
          )
    return int(input())

def MainMethod ():
    i = ShowMenu()
    
    if i ==1:
        PrintNotes()
    elif i ==2:
        AddNewNote()
    #elif i==5:
    #    FindToNum()
    elif i==5:
        DeleteNote ()
    elif i==3:
        EditNote()
        MainMethod()
    elif i ==4:
        PrintLog()
        MainMethod()
    elif i ==6:
        var =  json.dumps(Notes, default=lambda o: o.__dict__, sortkeys=True, indent=4)
        with open('DB.json', 'w') as outfile:
            outfile.write(var)
        exit()

MainMethod()




