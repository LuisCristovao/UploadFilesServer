# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:42:39 2018

@author: lcristovao
"""



import bottle as bt
#import pandas as pd
#import numpy as np
import os
from sys import argv
#import ML_MegaFunction as ml
import threading
#import sqlite3
import random

secret='some-secret-key'


shared_files={}

clients={}
clients_upload_threads={}
clients_delete_threads={}
class Client:
    
  
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.files={}
    
    def uploadFile(self,save_path):
        upload = bt.request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
    
        #save_path='files/Template'
        upload.save(save_path, overwrite=True) # appends upload.filename automatically
        self.files[upload.filename]=(upload.filename,'{{NotShared}}')
        
    def deleteFile(self,path):
        try:
            os.remove(path)
            self.delete_file=True
            
            self.RemoveFileFromMemory(path.split('/')[3])
        except:
           self.delete_file=False
           
    @staticmethod       
    def UniqueString(num=30):
       s="abcdfghijklmnopqrstuvxzyw1234567890ABCDEFGHIJKLMNOPQTUVXZWY"
       control=True
       ns=""
       while(control):
           
           for i in range(num):
               n=random.randint(0,len(s)-1)
               ns+=''+s[n]
           # if already exists try again    
           if ns in shared_files:
               ns=""
           else:
               control=False
       
       return ns
    
    
    def FilesToString(self):
        filenames=[]
        
        for key in self.files:
            value=self.files[key]
            filenames.append(value[0]+'        '+value[1])
            
        
        return (filenames)
    
    
    def AddShareFile(self,filename):
        global shared_files
        if filename in self.files:
            value=self.files[filename]
            if(value[1]=="{{NotShared}}"):
                uniquecode=self.UniqueString()
                new_val=(value[0],uniquecode)
                self.files[filename]=new_val
                shared_files[uniquecode]=''+self.username+'/'+filename
                return uniquecode
            else:
                return value[1]
        
        
    def RemoveSharedFile(self,filename):
        global shared_files
        if filename in self.files:
            value=self.files[filename]
            if value[1]!="{{NotShared}}":
                del shared_files[value[1]]
                new_val=(value[0],"{{NotShared}}")
                self.files[filename]=new_val
                return "Delete"    
            else:
                return "Fail"
        else:
            return 'Fail'
            
    def RemoveFileFromMemory(self,filename):
        global shared_files
        if filename in self.files:
            value=self.files[filename]
            del self.files[filename]
            unicode=value[1]
            if(unicode!=None):
                del shared_files[unicode]
                    
            return "Delete"    
            
        else:
            return 'Fail'
                

#def getUsers():
#   data = np.genfromtxt('files/Users.txt',dtype=str, delimiter=',')
#   return data
#
##for db        
#def getUsersDB():
#    conn = sqlite3.connect('users.db')
#    c = conn.cursor()
#    c.execute("SELECT username, password FROM users")
#    result = c.fetchall()
##    print(result[0][0])
#    c.close()
#    return result


def validate_user(secret):
    global clients
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            return True
    return False

#for txt file
#def check_login(username,password):
#    Users=getUsers()
#    for l in Users:
#        print(l)
#        if(username==l[0] and password==l[1]):
#            return True
#    return False


#for BD
#def check_login(username,password):
#    conn = sqlite3.connect('users.db')
#    c = conn.cursor()
#    c.execute("SELECT username, password FROM users where username='"+username+"' and password='"+password+"'")
#    result = c.fetchall()
#    if result:
#        return True
#    else:
#        return False
#    
#    
#def SignUp(username,password):
#    conn = sqlite3.connect('users.db')
##    c = conn.cursor()
#    try:
#        conn.execute("INSERT INTO users (username,password) VALUES ('"+username+"','"+password+"')")
#        conn.commit()
#    except:
#        return False
#    
#    return True
    

def SignUp(username,password):
    global clients
    #if already exists
    if username in clients:
       return False
   
    else:
        clients[username]=Client(username,password)
        return True
       
   
def check_login(username,password):
    global clients
    
    #user exists
    if username in clients:
        client_pass=clients[username].password
        #check if pass correct
        if client_pass==password:
            return True
        else:
            return False
    else:
        return False
   

#_______Main___________________________

#Users=getUsers()
#print(Users)

#########################################
    
#sql version###only use in case of db not created###################
#import CreateDB as db
#db.Start()
#db.DropTable()
#db.InsertNewuser('Luis','555')
#db.DeleteUser('Luis')    

###################################

                 
        
@bt.route('/') # or @route('/login')
def init():
    return bt.template('index')
    
@bt.get('/SignUp')
def sign_up_page():
    return bt.template('sign_up',different_pass_error="hidden",username_error="hidden")
    
@bt.post('/login')
def do_login():
    global clients
    global secret
    
    username = bt.request.forms.get('username')
    password = bt.request.forms.get('password')
    if check_login(username, password):
#        client=Client(username,password)
#        clients[username]=client
        bt.response.set_cookie(username, password, secret=secret)
        newpath = r'files/Template/'+username+'/' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        return bt.redirect('/restricted')
    else:
        return "<p>Login failed.</p>"
    
    
@bt.post('/SignUp/form',method='POST')
def signUp():
    global clients
    global secret
    
    username = bt.request.forms.get('username')
    password = bt.request.forms.get('password')
    cpassword = bt.request.forms.get('cpassword')
    if cpassword!=password:
        return bt.template('sign_up',different_pass_error="visible",username_error="hidden")
    else:
        if SignUp(username,password):
            #if it was successful de sign uo in the db
            return "<h2>Your username: "+username+" was successfully inserted in our DataBase.</h2><br><a href='/'>Return</a>"
        else:
            return bt.template('sign_up',different_pass_error="hidden",username_error="visible")    


@bt.get('/restricted')
def restricted_area():
    global secret
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            #files_dir = 'files/Template/'+c
            #user_files = os.listdir(files_dir)
            #print(clients[c].files)
            if bool(clients[c].files):
                files_unicodes=clients[c].FilesToString()
                
                return bt.template('user_files',rows=files_unicodes,User=c)
            else:
                #Dont have files yet
                return bt.template('no_files_yet',User=c)
    
    return "You are not logged in. Access denied."
    
    
    
@bt.get('/upload', method='POST')
def do_upload():
    global clients
    global secret
    global clients_upload_threads
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            #upload = bt.request.files.get('upload')
            newpath = r'files/Template/'+c+'/' 
#            if not os.path.exists(newpath):
#                os.makedirs(newpath)
            t=threading.Thread(target=clients[c].uploadFile(newpath))
            clients_upload_threads[c]=t
            t.start()
            return bt.redirect('/restricted')
        
    return "You are not logged in. Access denied."

@bt.get('/delete')
def delete():
    global secret
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            files_dir = 'files/Template/'+c
            user_files = os.listdir(files_dir)
            print(user_files)
            if user_files:
                return bt.template('delete_files',rows=user_files,User=c)
            else:
                #Dont have files yet
                return "<h1>No Files Yet to Delete</h1><br><a href='restricted'>Return</a>"
    
    return "You are not logged in. Access denied."



@bt.get('/delete/<filename>',method='GET')
def erase(filename):
    global clients
    global secret
    global clients_upload_threads
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            
            newpath = r'files/Template/'+c+'/'+filename 
#            if not os.path.exists(newpath):
#                os.makedirs(newpath)
            t=threading.Thread(target=clients[c].deleteFile(newpath))
            clients_delete_threads[c]=t
            t.start()
            if clients[c].delete_file:
                return bt.redirect('/restricted')
            else:
                return bt.redirect('/restricted')
        
    return "You are not logged in. Access denied."

@bt.get('/share/<filename>',method='GET')
def share(filename):
    global clients
    global secret
    global clients_upload_threads
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            clients[c].AddShareFile(filename)

            return bt.redirect('/restricted')
        
    return "You are not logged in. Access denied."
        
@bt.get('/stopshare/<filename>',method='GET')
def stopshare(filename):
    global clients
    global secret
    global clients_upload_threads
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            clients[c].RemoveSharedFile(filename)
            return bt.redirect('/restricted')
        
    return "You are not logged in. Access denied."    


@bt.get('/<filepath:path>')
def server_static(filepath):
    global secret
    print(filepath)
    if(filepath in shared_files):
        value=shared_files[filepath]
        user=value.split('/')[0]
        root='files/Template/'+user
        filename=value.split('/')[1] 
        return bt.static_file(filename, root=root,download=True) 
    for c in clients:
        key = bt.request.get_cookie(clients[c].username, secret=secret)
        if key:
            #valid user
            return bt.static_file(filepath, root='files/Template/'+c,download=True) 
    else:
        return "You are not logged in. Access denied."


bt.run(host='0.0.0.0', port=argv[1], server='paste')
