from flask import Flask, jsonify
import spacy
import sqlite3
import firebase_admin
from firebase_admin import credentials, db
def list_string(a):
    s=""
    for i in a:
        s=s+i+" "
    return s

def new_statment(sentence):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)
    noun_chunks = [token.text for token in doc if token.pos_=="NOUN"]
    verbs = [token.text for token in doc if token.pos_ == "VERB"]
    prep = [token.text for token in doc if token.pos_ == "ADP"]
    ques = ["what", "which", "when", "who", "whom", "how", "where"]
    pro = [token.text for token in doc if token.pos_ == "PRON"]
    aux = ["is", "are", "was", "were", "will", "shall", "the", "be", "by", "did", "do", "does", "and", "a", "an", "the","in"]
    a = noun_chunks + verbs + prep + ques + pro + aux
    unique = [i for i in sentence.split() if i not in a]
    elements=[]
    for i in sentence.split():
        if i in noun_chunks:
            elements.append(i)
        elif i in unique:
            elements.append(i)
        else:
            continue
    return elements

def similar(d,sentence,final):
    nlp1 = spacy.load("en_core_web_md")
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

def similar1(d,sentence):
    nlp1 = spacy.load("en_core_web_md")
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
    database_file_path = r'C:\Users\aa738\AppData\Local\Programs\Python\Python311\minor 3rd sem\aayush.db'
    connection = sqlite3.connect(database_file_path)
    cursor = connection.cursor()
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
cred = credentials.Certificate(r"C:\Users\aa738\AppData\Local\Programs\Python\Python311\minor 3rd sem\minor-3rd-sem-firebase-adminsdk-ickcq-28636289b5.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://minor-3rd-sem-default-rtdb.firebaseio.com/'})
data_ref = db.reference('/')
final={"table":None,"feild":None,"record":None}
database_file_path = r'C:\Users\aa738\AppData\Local\Programs\Python\Python311\minor 3rd sem\aayush.db'
connection = sqlite3.connect(database_file_path,check_same_thread=False)

d={}
try:
    all_children = data_ref.get()
    for key, value in all_children.items():
        d[key]=value.get('description')
except Exception as e:
    print("error")            
app = Flask(__name__)
@app.route('/analyze_sentence/<sentence>', methods=['get'])
def analyze_sentence(sentence):
    
    try:
        cursor = connection.cursor()
        similar(d,sentence,final)
        r="/"
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        t0=similar1(d,sentence).popitem()
        #print(similar(d))
        t=t0[0]
        final["table"]=t
        r=r+t
        print(t)
        d1={}
        data_ref1 = db.reference(r)
        
        try:
            all_children = data_ref1.get()
            for key, value in all_children.items():
                try:
                    d1[key]=value['description']
                except:
                    continue
            simp=similar1(d1,sentence).popitem()
            final["feild"]=simp[0]
        except Exception as e:
            pass

        
        result={"response":search(final)}
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/greet', methods=['get'])
def greet():
    result={"responce":"hello!!"}
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)