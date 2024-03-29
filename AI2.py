import spacy
import sqlite3
import time
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
print(datetime.now())
sentence = "give me the name of all category"
cred = credentials.Certificate(r"C:\Users\aa738\AppData\Local\Programs\Python\Python311\minor 3rd sem\minor-3rd-sem-firebase-adminsdk-ickcq-28636289b5.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://minor-3rd-sem-default-rtdb.firebaseio.com/'})
data_ref = db.reference('/')
print(data_ref.get())
nlp = spacy.load("en_core_web_sm")
nlp1 = spacy.load("en_core_web_md")
final={"table":None,"feild":None,"record":None}
doc = nlp(sentence)
database_file_path = r'C:\Users\aa738\AppData\Local\Programs\Python\Python311\minor 3rd sem\aayush.db'
connection = sqlite3.connect(database_file_path)
cursor = connection.cursor()
d={}

try:
    all_children = data_ref.get()
    for key, value in all_children.items():
        d[key]=value.get('description')
except Exception as e:
    print("error")

def list_string(a):
    s=""
    for i in a:
        s=s+i+" "
    return s

def new_statment(s):
    noun_chunks = [token.text for token in doc if token.pos_=="NOUN"]
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    prep = [token.text for token in doc if token.pos_ == "ADP"]
    ques = ["what", "which", "when", "who", "whom", "how", "where"]
    pro = [token.text for token in doc if token.pos_ == "PRON"]
    aux = ["is", "are", "was", "were", "will", "shall", "the", "be", "by", "did", "do", "does", "and", "a", "an", "the","in"]
    a = noun_chunks + verbs + prep + ques + pro + aux
    unique = [i for i in sentence.split() if i not in a]
    elements=[]
    for i in s.split():
        if i in noun_chunks:
            elements.append(i)
        elif i in unique:
            elements.append(i)
        else:
            continue
    return elements

def similar(d):
    s={}
    for key in d:
        for j in new_statment(sentence):      
            doc1 = nlp1(j)
            doc2 = nlp1(d[key])
            similarity = doc1.similarity(doc2)
            if similarity>0:
                try:
                    if s[key]<similarity:
                        s[key]=similarity
                    else:
                        pass
                except:
                    s[key]=similarity
            else:
                final["record"]=j
    sorted_items = sorted(s.items(), key=lambda x: x[1])
    sorted_dict = dict(sorted_items)
    return sorted_dict

def similar1(d):
    s={}
    lis=new_statment(sentence)
    stri=list_string(lis)
    for key in d:    
        doc1 = nlp1(stri)
        doc2 = nlp1(d[key])
        similarity = doc1.similarity(doc2)
        s[key]=similarity
    sorted_items = sorted(s.items(), key=lambda x: x[1])
    sorted_dict = dict(sorted_items)
    return sorted_dict


def search(final):
    if final["record"]==None:
        table_name=final["table"]
        attribute_name=final["feild"]
        query = f"SELECT {attribute_name} FROM {table_name}"
        cursor.execute(query)
        records = cursor.fetchall()
        return {"all":records}
    else:
        table_name=final["table"]
        attribute_name=final["feild"]
        record=final["record"]
        query =f"SELECT * FROM {table_name}"
        cursor.execute(query)
        records = cursor.fetchall()
        for i in records:
            if record.upper() in i:
                return {"single":i}
def word_db_check(element):
        table_name=final["table"]
        for i in element:
            record=i
            query =f"SELECT * FROM {table_name}"
            cursor.execute(query)
            records = cursor.fetchall()
            for i in records:
                if record.upper() in i:
                    return {"single":i}



similar(d)
element=new_statment(sentence)
r="/"
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
table_names = cursor.fetchall()
t0=similar(d).popitem()
#print(similar(d))
t=t0[0]
final["table"]=t
r=r+t
print(t)
d1={}
data_ref1 = db.reference(r)
print(datetime.now())
try:
    all_children = data_ref1.get()
    for key, value in all_children.items():
        try:
            d1[key]=value['description']
        except:
            continue
    print(similar1(d1))
    simp=similar1(d1).popitem()
    final["feild"]=simp[0]
except Exception as e:
    pass
print(similar(d))
print(final)
print(search(final))
