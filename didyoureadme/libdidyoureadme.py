import os
import datetime
import hashlib
import multiprocessing
import psycopg2
import psycopg2.extras
import pytz
import smtplib 
import urllib.parse
import io
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import http.server
import socketserver
import pkg_resources

dirTmp=os.path.expanduser("~/.didyoureadme/tmp/").replace("\\", "/")#The replace is for windows, but works in linux
dirDocs=os.path.expanduser("~/.didyoureadme/docs/").replace("\\", "/")


class Connection(QObject):
    """Futuro conection object
    COPIADA DE didyoureadme NO EDITAR"""
    def __init__(self):
        QObject.__init__(self)
        
        self.user=None
        self.password=None
        self.server=None
        self.port=None
        self.db=None
        self._con=None
        self._active=False
        self.init=None
        self.roles=None #Se carga al realizar la conexi´on
        
    def init__create(self, user, password, server, port, db):
        self.user=user
        self.password=password
        self.server=server
        self.port=port
        self.db=db
        return self


    def cursor(self):
        return self._con.cursor()

        
    
    def mogrify(self, sql, arr):
        """Mogrify text"""
        cur=self._con.cursor()
        s=cur.mogrify(sql, arr)
        cur.close()
        return  s
        
    def cursor_one_row(self, sql, arr=[]):
        """Returns only one row"""
        cur=self._con.cursor()
        cur.execute(sql, arr)
        row=cur.fetchone()
        cur.close()
        return row        
        
    def cursor_one_column(self, sql, arr=[]):
        """Returns un array with the results of the column"""
        cur=self._con.cursor()
        cur.execute(sql, arr)
        result=[]
        for row in cur:
            result.append(row[0])
        cur.close()
        return result
        
    def commit(self):
        self._con.commit()
        
    def rollback(self):
        self._con.rollback()
        
        
    def connection_string(self):
        return "dbname='{}' port='{}' user='{}' host='{}' password='{}'".format(self.db, self.port, self.user, self.server, self.password)
        
    def connect(self, connection_string=None):
        """Used in code to connect using last self.strcon"""
        if connection_string==None:
            s=self.connection_string()
        else:
            s=connection_string        
        try:
            self._con=psycopg2.extras.DictConnection(s)
        except psycopg2.Error as e:
            print (e.pgcode, e.pgerror)
            return
        self._active=True
        self.init=datetime.datetime.now()
        self.roles=self.getUserRoles()

        
    def newConnection(self):
        """Return a new connection object, with the same connection string"""
        new=Connection()
        new.connect(self.connection_string())
        return new
        
    def disconnect(self):
        self._active=False
        self._con.close()
        
    def is_active(self):
        return self._active
        
        
    def is_superuser(self):
        """Checks if the user has superuser role"""
        res=False
        cur=self.cursor()
        cur.execute("SELECT rolsuper FROM pg_roles where rolname=%s;", (self.user, ))
        if cur.rowcount==1:
            if cur.fetchone()[0]==True:
                res=True
        cur.close()
        return res

    def getUserRoles(self):
        """Returns a list with the roles of the connection user"""
        if self.user=="postgres":
            return ["didyoureadme_user", "didyoureadme_admin"]
        cur=self.cursor()
        #Saca el id del usuario actual
        cur.execute("SELECT usesysid FROM pg_user WHERE usename = current_user")
        userid=cur.fetchone()[0]
        #Saca los grupos que empiezan con didyoureadme_ en los que est´e el usuario
        return self.cursor_one_column("select groname from pg_group where %s=ANY(grolist) and groname like 'didyoureadme_%%'", (userid, ))
        
    def server_datetime(self):
        return self.cursor_one_row("SELECT NOW()")[0]

class Backup:
    def __init__(self):
        pass
    def save(self):
        pass
            
            
            
            
class MyHTTPServer(socketserver.TCPServer):
    """Clase usada para pasar el objeto mem, al servidor y a sus request"""
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, mem=None):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.mem=mem    
        self.served=0
        self.errors=0

    def finish_request(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        request=self.RequestHandlerClass(request, client_address, self, self.mem)
        
        if request.path in ["/favicon.ico",  "/expired.png", "/didyoureadme.png" ]:#Imagenes del servidor
            return 
        
        if request.request_served==True:
            #Actualiza la base de datos
            con=self.mem.con.newConnection()
            cur=con.cursor()
            try:
                ud=UserDocument(request.user, request.document, self.mem)
                ud.readed( self.mem.localzone)
                con.commit()
                self.mem.log(QApplication.translate("DidYouReadMe","User {} downloaded document {}".format(request.user.mail, request.document.id)))
            except:
                self.errors=self.errors+1
                self.mem.log(QApplication.translate("DidYouReadMe", "Error registering in database"))    
            cur.close()  
            con.disconnect()
            self.served=self.served+1
        else:
            #"""Puede ser por muchos motivos, expirados, no existe, no encontrado...""", se trata en la request
            self.errors=self.errors+1
            self.mem.log("Request has not been served correctly, so it is not registered")#Fallaba con QApplication.translate

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self,request, client_address, server, mem=None):
        self.mem=mem#Debe ir antes
        self.userhash=None
        self.documenthash=None
        self.user=None
        self.document=None
        self.request_served=False
        http.server.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        
    def Resource(self, resource):
        """Serve Qt resources"""
        stream = QFile(resource)
        stream.open(QFile.ReadOnly)
        buffer=stream.readAll()
        stream.close()
        f = io.BytesIO()
        f.write(buffer)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", str(len(buffer)))
        self.end_headers()
        return f
                
    def Expired(self, document):
        s="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>"""+ QApplication.translate("DidYouReadMe","Didyoureadme - Expired document")+"""</title>
</head>
<body>
    <h1><center>"""+ QApplication.translate("DidYouReadMe","Document '{}' of '{}' has expired".format(self.document.name, self.document.datetime)) +"""</center></h1>
<center>
    <img src="/expired.png" width="200"/><p>
    """+QApplication.translate("DidYouReadMe","Document you're trying to read has expired")+"""<p>
    """+QApplication.translate("DidYouReadMe", "Please talk with DidYouReadMe administrator")+"""<p>
</center>
</body>
</html>"""
        encoded=s.encode("UTF-8", 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f
        
        
    def ErrorPage(self, text):
        """To avoid listing"""
        s="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset={0}">
    <title>"""+ QApplication.translate("DidYouReadMe","Didyoureadme - Error page")+"""</title>
</head>
<body>
    <h1><center>"""+ text +"""</center></h1>
<center>
    <img src="/didyoureadme.png" width="120"/><p>
    """+QApplication.translate("DidYouReadMe","There has been a problem with your request")+"""<p>
    """+QApplication.translate("DidYouReadMe", "Please talk with DidYouReadMe administrator")+"""<p>
</center>
</body>
</html>"""
        encoded=s.encode("UTF-8", 'surrogateescape')
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f
        
    def send_head(self):
        """Overriden
        
        Tras muchos dolores de cabeza no consigo nada
        Funciona bien lanzando con eric
        Pero al pasar por freeze falla en esta función
        He usado log para verlo
        Se produce cuando es compilado sin consola con Win32 en la base del setup. Si se pone base="Console" funciona
        """
        if self.path=="/favicon.ico":
            return self.Resource(':/didyoureadme.ico')       
        elif self.path=="/expired.png":
            return self.Resource(':/expired.png')
        elif self.path=="/didyoureadme.png":
            return self.Resource(':/didyoureadme.png')
        
        #self.path is /get/hash1l68f2e2cd140e4c2e2fd94eb51376f3730d15108a4689de1a918a6526b0d7ee37/aldea.odt
        try:
            (userhash, documenthash)=self.path.split("/")[2].split("l")
            self.document=Document(self.mem).init__from_hash(documenthash)
            self.user=self.mem.data.users_all().user_from_hash(userhash)
            assert type(self.document) is Document,  "Asserting error"
            assert type(self.user) is User,  "Asserting error"
        except:
            self.document=None
            self.user=None
            self.mem.log(QApplication.translate("DidYouReadMe","Error parsing path"))
            return self.ErrorPage(QApplication.translate("DidYouReadMe","Error parsing path"))
            
        path = self.translate_path(self.document.hash)  

        if self.document.expiration<now(self.mem.localzone):
            self.mem.log(QApplication.translate("DidYouReadMe", "Document {} has expired".format(self.document.id)))
            return self.Expired(self.document)
            
        ctype = self.guess_type(path)

        f=None
        try:
            f = open(path, 'rb')
        except OSError:
            self.mem.log(QApplication.translate("DidYouReadMe", "File {} not found".format(path)))
            return self.ErrorPage(QApplication.translate("DidYouReadMe","File not found"))
            
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            self.request_served=True
            return f
        except:
            self.mem.log("Sending page raised an error")
            f.close()
            raise
            



class SetCommons:
    """Base clase to create Sets, it needs id and name attributes, as index. It has a list arr and a dics dic_arr to access objects of the set"""
    def __init__(self):
        self.dic_arr={}
        self.arr=[]
        self.id=None
        self.name=None
        self.selected=None#Used to select a item in the set. Usefull in tables. Its a item
    
    def arr_position(self, id):
        """Returns arr position of the id, useful to select items with unittests"""
        for i, a in enumerate(self.arr):
            if a.id==id:
                return i
        return None
            

    def append(self,  obj):
        self.arr.append(obj)
        self.dic_arr[str(obj.id)]=obj
        
    def remove(self, obj):
        self.arr.remove(obj)
        del self.dic_arr[str(obj.id)]
        
    def length(self):
        return len(self.arr)
        
    def find(self, id,  log=False):
        """Finds by id"""
        try:
            return self.dic_arr[str(id)]    
        except:
            if log:
                print ("SetCommons ({}) fails finding {}".format(self.__class__.__name__, id))
            return None

    def find_by_id(self, id,  log=False):
        """Finds by id"""
        try:
            return self.dic_arr[str(id)]    
        except:
            if log:
                print ("SetCommons ({}) fails finding {}".format(self.__class__.__name__, id))
            return None
            
    def find_by_arr(self, id,  log=False):
        """log permite localizar errores en find. Ojo hay veces que hay find fallidos buscados como en UNION
                inicio=datetime.datetime.now()
        self.mem.data.products_all().find(80230)
        print (datetime.datetime.now()-inicio)
        self.mem.agrupations.find_by_arr(80230)
        print (datetime.datetime.now()-inicio)
        Always fister find_by_dict
        0:00:00.000473
        0:00:00.000530

        """
        for a in self.arr:
            if a.id==id:
                return a
        if log:
            print ("SetCommons ({}) fails finding  by arr {}".format(self.__class__.__name__, id))
        return None
                
    def order_by_id(self):
        """Orders the Set using self.arr"""
        try:
            self.arr=sorted(self.arr, key=lambda c: c.id,  reverse=False)     
            return True
        except:
            return False
        
    def order_by_name(self):
        """Orders the Set using self.arr"""
        try:
            self.arr=sorted(self.arr, key=lambda c: c.name,  reverse=False)       
            return True
        except:
            return False

    def qcombobox(self, combo,  selected=None):
        """Load set items in a comobo using id and name
        Selected is and object
        It sorts by name the arr""" 
        self.order_by_name()
        combo.clear()
        for a in self.arr:
            combo.addItem(a.name, a.id)

        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.id))
                
    def clean(self):
        """Deletes all items"""
        self.arr=[]
        self.dic_arr={}
#        for a in self.arr:
#            self.remove(a)
                
    def clone(self,  *initparams):
        """Returns other Set object, with items referenced, ojo con las formas de las instancias
        initparams son los parametros de iniciación de la clase"""
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        for a in self.arr:
            result.append(a)
        return result
        
    def union(self,  set,  *initparams):
        """Returns a new set, with the union comparing id
        initparams son los parametros de iniciación de la clse"""        
        resultado=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca SetProduct(self.mem), luego será self.mem
        for p in self.arr:
            resultado.append(p)
        for p in set.arr:
            if resultado.find(p.id, False)==None:
                resultado.append(p)
        return resultado
        
class SetCommonsQListView(SetCommons):
    def __init__(self):
        SetCommons.__init__(self)
        
    def qlistview(self, list, selected):
        """Shows a list with the items of arr,
        selected lista de group a seleccionar"""
        self.order_by_name()
        model=QStandardItemModel (len(self.arr), 1); # 3 rows, 1 col
        for i,  g in enumerate(self.arr):
            item = QStandardItem(g.name)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled);
            if g in selected.arr:
                item.setData(Qt.Checked, Qt.CheckStateRole)
            else:
                item.setData(Qt.Unchecked, Qt.CheckStateRole); #para el role check
            item.setData(g.id, Qt.UserRole) # Para el role usuario
            model.setItem(i, 0, item);
        list.setModel(model)
        
    def qlistview_getselected(self, list, *initparams):
        """Returns a new set, with the selected in the list
        initparams son los parametros de iniciación de la clse"""        
        resultado=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca SetProduct(self.mem), luego será self.mem   
        for i in range(list.model().rowCount()):
            if list.model().index(i, 0).data(Qt.CheckStateRole)==Qt.Checked:
                id=list.model().index(i, 0).data(Qt.UserRole)
                resultado.append(self.find(id))   
        return resultado
        

class SetGroups(SetCommonsQListView):
    def __init__(self, mem):
        SetCommonsQListView.__init__(self)
        self.mem=mem
        
    def quit_user_from_all_groups(self, user):
        """Se quita un usuario de todos los grupos tanto lógicamente como físicamente"""
        
        todelete=None#Se usa para no borrar en iteracion
        for g in self.arr:
            for u in g.members.arr:
                if u.id==user.id:
                    todelete=u
            if todelete!=None:
                g.members.remove(user)
                g.save()# Para no grabar en bd salvoi que encuente se pone aquí
                todelete=None
                    
           
    def qtablewidget(self, table):
        """Section es donde guardar en el config file, coincide con el nombre del formulario en el que está la table
        Devuelve sumatorios"""
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Name" )))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Users" )))    
        table.clearContents()
        table.setRowCount(len(self.arr))
        table.applySettings()
        for i, p in enumerate(self.arr):
            table.setItem(i, 0, QTableWidgetItem(p.name))
            table.item(i, 0).setIcon(QIcon(":/group.png"))
            table.setItem(i, 1, QTableWidgetItem(p.members.string_of_names()))
        table.clearSelection() 

    def load(self, sql):
        cur=self.mem.con.cursor()
        cur.execute(sql)
        for row in cur:
            members=SetUsers(self.mem)
            if row['id']==1:#Caso de todos
                for u in self.mem.data.users_active.arr:
                    members.append(u)
            else:
                for id_user in row['members']:
                    u=self.mem.data.users_all().find(id_user)
                    if u.active==True:
                        members.append(u)
            self.append( Group(self.mem, row['name'], members, row['id']))        
        cur.close()

        
class Group:
    def __init__(self, mem,   name, members,  id=None):
        """members es un SetUsers"""
        self.members=members
        self.name=name
        self.id=id
        self.mem=mem
        
    def delete(self):
        #Borra de la base de datos
        cur=self.mem.con.cursor()
        cur.execute("delete from groups where id=%s", (self.id, ))
        cur.close()
        
    def save(self):
        def members2pg():
            if self.members.length()==0:
                return "'{}'"
            resultado=""
            for m in self.members.arr:
                resultado=resultado + str(m.id)+", "
            return "ARRAY["+resultado[:-2]+"]"
            
        cur=self.mem.con.cursor()
        if self.id==None:
            #Crea registro en base de datos
            cur.execute("insert into groups (name,members) values(%s, "+members2pg() +") returning id", (self.name, ))
            self.id=cur.fetchone()[0]
        else:
            #Modifica registro en base de datos
            cur.execute("update groups set name=%s, members="+members2pg()+" where id=%s",(self.name, self.id ))
        cur.close()
            

class SetLanguages(SetCommons):
    def __init__(self, mem):
        SetCommons.__init__(self)
        self.mem=mem
        
    def load_all(self):
        self.append(Language(self.mem, "en","English" ))
        self.append(Language(self.mem, "es","Español" ))
        self.append(Language(self.mem, "fr","Français" ))
        self.append(Language(self.mem, "ro","Rom\xe2n" ))
        self.append(Language(self.mem, "ru",'\u0420\u0443\u0441\u0441\u043a\u0438\u0439' ))

    def qcombobox(self, combo, selected=None):
        """Selected is the object"""
        self.order_by_name()
        for l in self.arr:
            combo.addItem(self.mem.countries.find_by_id(l.id).qicon(), l.name, l.id)
        if selected!=None:
                combo.setCurrentIndex(combo.findData(selected.id))

    def cambiar(self, id):    
        filename=pkg_resources.resource_filename("didyoureadme","i18n/didyoureadme_{}.qm".format(id))
        print(os.getcwd(), filename, os.path.exists(filename))
        self.mem.qtranslator.load(filename)
        qApp.installTranslator(self.mem.qtranslator)
        print("Language changed to {}".format(id))

        
class SetUsers(SetCommonsQListView):
    def __init__(self, mem):
        SetCommonsQListView.__init__(self)
        self.mem=mem
    

    def user_from_hash(self, hash):
        for u in self.arr:
            if u.hash==hash:
                return u
        self.mem.log("User {} not found".format(hash))
        return None
        
    def load(self, sql):
        cur=self.mem.con.cursor()
        cur.execute(sql)
        for row in cur:
            self.append(User(self.mem, row['datetime'],  row['post'], row['name'], row['mail'], row['active'], row['hash'],  row['id']))
        cur.close()
            
            
    def string_of_names(self):
        "String of names sorted"
        self.order_by_name()
        users=""
        for u in self.arr:
            users=users+u.name+"\n"
        return users[:-1]

           
    def qtablewidget(self, table):
        """Section es donde guardar en el config file, coincide con el nombre del formulario en el que está la table
        Devuelve sumatorios"""
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Start date" )))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Post" )))    
        table.setHorizontalHeaderItem(2, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Full name" )))    
        table.setHorizontalHeaderItem(3, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Mail" )))    
        table.setHorizontalHeaderItem(4, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Read" )))    
        table.setHorizontalHeaderItem(5, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Sent" )))    
        table.clearContents()
        table.setRowCount(len(self.arr))
        table.applySettings()
        for i, u in enumerate(self.arr):
            table.setItem(i, 0, qdatetime(u.datetime, self.mem.localzone))
            if u.post==None:
                post=""
            else:
                post=u.post
            table.setItem(i, 1, qleft(post))
            table.setItem(i, 2, qleft(u.name))
            if u.active==True:
                table.item(i, 2).setIcon(QIcon(":/user.png"))
            else:
                table.item(i, 2).setIcon(QIcon(":/alerta.png"))
            table.setItem(i, 3, qleft(u.mail))
            table.setItem(i, 4, qcenter(u.read))
            table.setItem(i, 5, qcenter(u.sent))
        table.clearSelection()    

class User:
    def __init__(self, mem,  dt, post, name, mail, active=True, hash="hash no calculado",  id=None):
        self.mem=mem
        self.id=id
        self.name=name
        self.datetime=dt#incorporation date
        self.mail=mail
        self.hash=hash
        self.post=post
        self.sent=0
        self.read=0
        self.active=active

    def __repr__(self):
        return "{0} ({1})".format(self.name, self.id)
                
                
    def isDeletable(self):
        for g in self.mem.data.groups.arr:
            if g.members.find(self.id)!=None and g.id!=1:
                return False
        
        cur=self.mem.con.cursor()
        cur.execute("select count(*) from userdocuments where id_users=%s", (self.id, ))
        num=cur.fetchone()[0]
        cur.close()
        if num>0:
            return False
        return True
        
    def delete(self):
        cur=self.mem.con.cursor()
        cur.execute("delete from users where id=%s", (self.id, ))
        cur.close()
        
    def calculateHash(self):
        if self.id==None:
            return None
        return hashlib.sha256(("u."+str(self.id)+str(self.datetime)).encode('utf-8')).hexdigest()
    
    def save(self):
        cur=self.mem.con.cursor()        
        if self.id==None:
            cur.execute("insert into users (datetime,post,name,mail, hash, active) values(%s,%s,%s,%s,%s, %s) returning id ", (self.datetime, self.post, self.name, self.mail, self.hash, self.active))
            self.id=cur.fetchone()[0]
            self.hash=self.calculateHash()
            self.sent=0
            self.read=0
            cur.execute("update users set hash=%s where id=%s", (self.hash, self.id))
        else:
            cur.execute("update users set datetime=%s, post=%s, name=%s, mail=%s, active=%s where id=%s", (self.datetime, self.post, self.name, self.mail,  self.active, self.id))
        cur.close()

    def updateSent(self):
        cur=self.mem.con.cursor()
        cur.execute("select count(*) from userdocuments where id_users=%s", (self.id, ))
        self.sent= cur.fetchone()[0]
        cur.close()


    def updateRead(self):
        cur=self.mem.con.cursor()
        cur.execute("select count(*) from userdocuments where id_users=%s and read is not null", (self.id, ))
        self.read=cur.fetchone()[0]
        cur.close()

class TWebServer(QThread):
    def __init__(self, mem):
        QThread.__init__(self)
        self.mem=mem
        
        os.chdir(dirDocs)
        self.server=MyHTTPServer((self.mem.settings.value("webserver/interface", "127.0.0.1"), int(self.mem.settings.value("webserver/port", "8000"))), MyHTTPRequestHandler, mem=self.mem)

    def run(self):
        self.server.serve_forever()
class SettingsDB:
    def __init__(self, mem):
        self.mem=mem
    
    def exists(self, name):
        """Returns true if globals is saved in database"""
        cur=self.mem.con.cursor()
        cur.execute("select value from globals where global=%s", (name, ))
        num=cur.rowcount
        cur.close()
        if num==0:
            return False
        else:
            return True
  
    def value(self, name, default):
        """Search in database if not use default"""            
        cur=self.mem.con.cursor()
        cur.execute("select value from globals where global=%s", (name, ))
        if cur.rowcount==0:
            return default
        else:
            value=cur.fetchone()[0]
            cur.close()
            return value
        
    def setValue(self, name, value):
        """Set the global value.
        It doesn't makes a commit, you must do it manually
        value can't be None
        """
        cur=self.mem.con.cursor()
        if self.exists(name)==False:
            cur.execute("insert into globals (global,value) values(%s,%s)", ( name, value))     
        else:
            cur.execute("update globals set value=%s where global=%s", ( value, name))
        cur.close()
        self.mem.con.commit()

class TSend(QThread):
    def __init__(self, mem):
        QThread.__init__(self)
        self.mem=mem
        self.errors=0
        self.sent=0
        self.stop_request=False
        self.interval=30#segundos
        
    def setInterval(self, interval):
        self.interval=interval
        
    def shutdown(self):
        self.stop_request=True

    def run(self):    
        while self.stop_request==False:
            con=self.mem.con.newConnection()#NO SE PORQUE NO ACTUALIZABA SI USABA CONEXIóN DE PARAMETRO
            cur=con.cursor()
            #5 minutos delay
            cur.execute("select id_documents, id_users from userdocuments, documents where userdocuments.id_documents=documents.id and sent is null and now() > datetime + interval '1 minute';")
            for row in cur:
                doc=self.mem.data.documents_active.find(row['id_documents'])
                u=self.mem.data.users_active.find(row['id_users'])
                mail=Mail(doc, u, self.mem)
                mail.send()
                
                if mail.sent==True:
                    self.mem.log("Document {0} was sent to {1}".format(mail.document.id, mail.user.mail))
                    d=UserDocument(mail.user, mail.document, self.mem)
                    if d.sent==None:
                        d.sent=datetime.datetime.now(pytz.timezone(self.mem.localzone))
                    d.save()
                    con.commit()
                    self.sent=self.sent+1
                else:
                    self.errors=self.errors+1  
                    self.mem.log(QApplication.translate("DidYouReadMe","Error sending message {} to {}").format(mail.document.id, mail.user.mail))  
                self.sleep(2) 
            cur.close()
            con.disconnect()
            #Interactive wait
            for i in range(self.interval):
                if self.stop_request==True:
                    break
                else:
                    self.sleep(1)

class Language:
    def __init__(self, mem, id, name):
        self.id=id
        self.name=name
    

class Mail:
    def __init__(self, document, user,  mem):
        self.mem=mem
        self.user=user
        self.document=document
        self.sender=""
        self.receiver=user.mail
        self.name=document.name
        self.sent=None


    def message(self):
        def weekday(noww):
            """Se hace esta función para que no haya problemas con la localización de %a"""
            if noww.isoweekday()==1:
                return "Mon"
            if noww.isoweekday()==2:
                return "Tue"
            if noww.isoweekday()==3:
                return "Wed"
            if noww.isoweekday()==4:
                return "Thu"
            if noww.isoweekday()==5:
                return "Fri"
            if noww.isoweekday()==6:
                return "Sat"
            if noww.isoweekday()==7:
                return "Sun"
                
        def month(noww):
            """Se hace esta función para que no haya problemas con la localización de %b"""
            if noww.month==1:
                return "Jan"
            elif noww.month==2:
                return "Feb"
            elif noww.month==3:
                return "Mar"
            elif noww.month==4:
                return "Apr"
            elif noww.month==5:
                return "May"
            elif noww.month==6:
                return "Jun"
            elif noww.month==7:
                return "Jul"
            elif noww.month==8:
                return "Aug"
            elif noww.month==9:
                return "Sep"
            elif noww.month==10:
                return "Oct"
            elif noww.month==11:
                return "Nov"
            elif noww.month==12:
                return "Dec"
            
        url="http://{0}:{1}/get/{2}l{3}/{4}".format(self.mem.settings.value("webserver/ip", "127.0.0.1"), self.mem.settings.value("webserver/port", "8000"), self.user.hash, self.document.hash, urllib.parse.quote(os.path.basename(self.document.filename.lower())))

        comment=""
        if self.document.comment!="":
            comment=self.document.comment+"\n\n___________________________________________________________\n\n"
        noww=now(self.mem.localzone)
        s= ("From: "+self.mem.settings.value("smtp/from", "didyoureadme@donotanswer.com")+"\n"+
        "To: "+self.user.mail+"\n"+
        "MIME-Version: 1.0\n"+
        "Subject: "+ self.document.name+"\n"+
        "Date: " + weekday(noww)+", " + str(noww.strftime("%d"))+" "+ month(noww)+" "+ str(noww.strftime("%Y %X %z")) +"\n"+
        "Content-Type: text/plain; charset=UTF-8\n" +
        "\n"+
        comment +
        QApplication.translate("DidYouReadMe","This is an automatic and personal mail from DidYouReadMe.")+"\n\n"+
        QApplication.translate("DidYouReadMe", "Don't answer and don't resend this mail.")+"\n\n"+
        QApplication.translate("DidYouReadMe", "When you click the next link, you will get the document associated to this mail and it will be registered as read:")+"\n\n"+
        url +"\n\n"+
        self.mem.settings.value("smtp/support", "Please, contact system administrator"))
        return s.encode('UTF-8')
    
    def send(self):      
        server=None#server creation could fail
        if self.mem.settings.value("smtp/tls", "False")=="True":
            try:
                server = smtplib.SMTP(self.mem.settings.value("smtp/smtpserver", "smtpserver"), int(self.mem.settings.value("smtp/smtpport", "25")))
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.mem.settings.value("smtp/smtpuser", "smtpuser"), self.mem.settings.value("smtp/smtppwd", "*"))
                server.sendmail(self.mem.settings.value("smtp/from", "didyoureadme@donotanswer.com"), self.user.mail, self.message())
                self.sent=True        
            except:
                self.sent=False
                self.mem.log("Mail failed from {}:{} and user {}/{}".format(self.mem.settings.value("smtp/smtpserver", "smtpserver"), self.mem.settings.value("smtp/smtpport", "25"), self.mem.settings.value("smtp/smtpuser", "smtpuser"), self.mem.settings.value("smtp/from", "didyoureadme@donotanswer.com")))
            finally:   
                if server:
                    server.quit()
        else:  #ERA EL ANTIVIRUS
            try:
                server = smtplib.SMTP(self.mem.settings.value("smtp/smtpserver", "smtpserver"), int(self.mem.settings.value("smtp/smtpport", "25")))
                server.login(self.mem.settings.value("smtp/smtpuser", "smtpuser"),self.mem.settings.value("smtp/smtppwd", "*"))
                server.helo()
                server.sendmail(self.mem.settings.value("smtp/from", "didyoureadme@donotanswer.com"), self.user.mail, self.message())
                self.sent=True        
            except:
                self.sent=False                
                self.mem.log("Mail failed from {}:{} and user {}/{}".format(self.mem.settings.value("smtp/smtpserver", "smtpserver"), self.mem.settings.value("smtp/smtpport", "25"), self.mem.settings.value("smtp/smtpuser", "smtpuser"), self.mem.settings.value("smtp/from", "didyoureadme@donotanswer.com")))
            finally:     
                if server:
                    server.quit()
        return self.sent



class SetCountries(SetCommons):
    def __init__(self, mem):
        SetCommons.__init__(self)
        self.mem=mem   
        
    def load_all(self):
        self.append(Country().init__create("es",QApplication.translate("DidYouReadMe","Spain")))
        self.append(Country().init__create("be",QApplication.translate("DidYouReadMe","Belgium")))
        self.append(Country().init__create("cn",QApplication.translate("DidYouReadMe","China")))
        self.append(Country().init__create("de",QApplication.translate("DidYouReadMe","Germany")))
        self.append(Country().init__create("en",QApplication.translate("DidYouReadMe","United Kingdom")))
        self.append(Country().init__create("eu",QApplication.translate("DidYouReadMe","Europe")))
        self.append(Country().init__create("fi",QApplication.translate("DidYouReadMe","Finland")))
        self.append(Country().init__create("fr",QApplication.translate("DidYouReadMe","France")))
        self.append(Country().init__create("ie",QApplication.translate("DidYouReadMe","Ireland")))
        self.append(Country().init__create("it",QApplication.translate("DidYouReadMe","Italy")))
        self.append(Country().init__create("jp",QApplication.translate("DidYouReadMe","Japan")))
        self.append(Country().init__create("nl",QApplication.translate("DidYouReadMe","Netherlands")))
        self.append(Country().init__create("pt",QApplication.translate("DidYouReadMe","Portugal")))
        self.append(Country().init__create("us",QApplication.translate("DidYouReadMe","United States of America")))
        self.append(Country().init__create("ro",QApplication.translate("DidYouReadMe","Romanian")))
        self.append(Country().init__create("ru",QApplication.translate("DidYouReadMe","Rusia")))
        self.order_by_name()

    def qcombobox(self, combo,  country=None):
        """Función que carga en un combo pasado como parámetro y con un SetAccounts pasado como parametro
        Se ordena por nombre y se se pasa el tercer parametro que es un objeto Account lo selecciona""" 
        for cu in self.arr:
            combo.addItem(cu.qicon(), cu.name, cu.id)

        if country!=None:
                combo.setCurrentIndex(combo.findData(country.id))

    def qcombobox_translation(self, combo,  country=None):
        """Función que carga en un combo pasado como parámetro con los países que tienen traducción""" 
        for cu in [self.find("es"),self.find("fr"),self.find("ro"),self.find("ru"),self.find("en") ]:
            combo.addItem(cu.qicon(), cu.name, cu.id)

        if country!=None:
                combo.setCurrentIndex(combo.findData(country.id))

class SetDocuments(SetCommons):
    def __init__(self, mem):
        SetCommons.__init__(self)
        self.mem=mem #solo se usa para conexion, los datos se guardan en arr
                
    def load(self, sql):
        """Carga según el sql pasado debe ser un select * from documents ...."""
        cur=self.mem.con.cursor()
        cur.execute(sql)
        for row in cur:
            d=Document(self.mem).init__create( row['datetime'], row['title'], row['filename'], row['comment'],  row['expiration'],  row['hash'], row['id']  )
            self.append(d)        
        for d in self.arr:
            d.updateNums()
        cur.close()

    def qtablewidget(self, table):
        """Section es donde guardar en el config file, coincide con el nombre del formulario en el que está la table
        Devuelve sumatorios"""
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Datetime" )))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Planned" )))    
        table.setHorizontalHeaderItem(2, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Sent" )))    
        table.setHorizontalHeaderItem(3, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Read" )))    
        table.setHorizontalHeaderItem(4, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Expiration" )))    
        table.setHorizontalHeaderItem(5, QTableWidgetItem(QApplication.translate("DidYouReadMe", "Title" )))    
        table.clearContents()
        table.setRowCount(len(self.arr))
        table.applySettings()
        for i, d in enumerate(self.arr):
            table.setItem(i, 0, qdatetime(d.datetime, self.mem.localzone))
            table.setItem(i, 1, qcenter(d.numplanned))
            table.setItem(i, 2, qcenter(d.numsents))
            table.setItem(i, 3, qcenter(d.numreads))
            table.setItem(i, 4, qdatetime(d.expiration, self.mem.localzone))
            if d.isExpired():
                table.item(i, 4).setIcon(QIcon(":/expired.png"))
            table.setItem(i, 5, qleft(d.name))
            table.item(i, 5).setIcon(QIcon(":/document.png"))
            
            if d.numreads==d.numplanned and d.numplanned>0:
                for column in range( 1, 4):
                    table.item(i, column).setBackground(QColor(198, 205, 255))

        table.setCurrentCell(len(self.arr)-1, 0)       
        table.clearSelection()    


    def order_by_datetime(self):
        """Ordena por datetime"""
        self.arr=sorted(self.arr, key=lambda d: d.datetime)        

#    def document_from_hash(self, hash):
#        for d in self.arr:
#            if d.hash==hash:
#                return d
#        print ("Document not found from hash")
#        return None


class Country:
    def __init__(self):
        self.id=None
        self.name=None
        
    def init__create(self, id, name):
        self.id=id
        self.name=name
        return self
            
    def qicon(self):
        icon=QIcon()
        icon.addPixmap(self.qpixmap(), QIcon.Normal, QIcon.Off)    
        return icon 
        
    def qpixmap(self):
        if self.id=="be":
            return QPixmap(":/belgium.gif")
        elif self.id=="cn":
            return QPixmap(":/china.gif")
        elif self.id=="fr":
            return QPixmap(":/france.png")
        elif self.id=="ie":
            return QPixmap(":/ireland.gif")
        elif self.id=="it":
            return QPixmap(":/italy.gif")
        elif self.id=="es":
            return QPixmap(":/spain.png")
        elif self.id=="eu":
            return QPixmap(":/eu.gif")
        elif self.id=="de":
            return QPixmap(":/germany.gif")
        elif self.id=="fi":
            return QPixmap(":/fi.jpg")
        elif self.id=="nl":
            return QPixmap(":/nethland.gif")
        elif self.id=="en":
            return QPixmap(":/uk.png")
        elif self.id=="jp":
            return QPixmap(":/japan.gif")
        elif self.id=="pt":
            return QPixmap(":/portugal.gif")
        elif self.id=="us":
            return QPixmap(":/usa.gif")
        elif self.id=="ro":
            return QPixmap(":/rumania.png")
        elif self.id=="ru":
            return QPixmap(":/rusia.png")
        else:
            return QPixmap(":/star.gif")
            
        
class DBData:
    def __init__(self, mem):
        self.mem=mem


    def load(self):
        inicio=datetime.datetime.now()
        self.users_active=SetUsers(self.mem)
        self.users_active.load("select * from users where active=true order by name")
        self.users_inactive=SetUsers(self.mem)
        self.users_inactive.load("select * from users where active=false order by name")    
        self.groups=SetGroups(self.mem)
        self.groups.load( "select * from groups order by name")
        self.documents_active=SetDocuments(self.mem)
        self.documents_active.load("select  id, datetime, title, comment, filename, hash, expiration  from documents where expiration>now() order by datetime")
        self.documents_inactive=SetDocuments(self.mem)#Carga solo los de un mes y un año.
        self.mem.log(QApplication.translate("DidYouReadMe","Loading data from database took {}".format(datetime.datetime.now()-inicio)))

    def users_all(self):
        return self.users_active.union(self.users_inactive, self.mem)
            
    def users_set(self, active):
        """Function to point to list if is active or not"""
        if active==True:
            return self.users_active
        else:
            return self.users_inactive    
    def documents_set(self, active):
        """Function to point to list if is active or not"""
        if active==True:
            return self.documents_active
        else:
            return self.documents_inactive    
    


class Document:
    def __init__(self, mem):
        self.mem=mem
        
    def init__create(self,  dt, name, filename, comment, expiration,   hash='Not calculated',  id=None):
        self.id=id
        self.datetime=dt
        self.name=name
        self.filename=filename
        self.comment=comment
        self.hash=hash
        self.numreads=0
        self.numsents=0
        self.numplanned=0
        self.expiration=expiration
        return self
        
    def init__from_hash(self, hash):
        cur=self.mem.con.cursor()
        cur.execute("select  id, datetime, title, comment, filename, hash, expiration  from documents where hash=%s", (hash, ))
        if cur.rowcount==1:
            row=cur.fetchone()
            self.init__create(row['datetime'], row['title'], row['filename'], row['comment'],  row['expiration'],  row['hash'], row['id']  )
            cur.close()
            return self
        elif cur.rowcount>1:
            self.mem.log("There are several documents with the same hash")
            cur.close()
            return None
        else:
            cur.close()
            qDegug("I couldn't create document from hash {}".format(hash ))
            return None
        
    def __repr__(self):
        return "{0} ({1})".format(self.name, self.id)
        
    def hasPendingMails(self):
        """Returns a boolean, if the document has pending mails searching in database"""
        cur=self.mem.con.cursor()
        cur.execute("select count(*) from userdocuments  where id_documents=%s and sent is null", (self.id, ))
        number=cur.fetchone()[0]
        cur.close()
        if number==0:
            return False
        else:
            return True
        
    def isExpired(self):
        if self.expiration>now(self.mem.localzone):
            return False
        return True
        
    def calculateHash(self):
        """Se mete el datetime porque sino se podría adivinar el ocmunicado"""
        return hashlib.sha256(("d."+str(self.id)+str(self.datetime)).encode('utf-8')).hexdigest()


    def delete(self):
        """Database delete and fisical delete"""
        cur=self.mem.con.cursor()
        cur.execute("delete from documents where id=%s", (self.id, ))        
        cur.close()
        self.unlink()
        
    def send_again(self):
        """Send document to all userdocuments even if allready have been send"""
        cur=self.mem.con.cursor()
        cur.execute("select id_users from userdocuments where id_documents=%s", (self.id, ))
        for row in cur:
            u=self.mem.data.users_active.find(row['id_users'])
            mail=Mail(self, u, self.mem)
            mail.send()            
            if mail.sent==True:
                self.mem.log("Document {0} was sent again to {1}".format(mail.document.id, mail.user.mail))
                d=UserDocument(mail.user, mail.document, self.mem)
                if d.sent==None:
                    d.sent=datetime.datetime.now(pytz.timezone(self.mem.localzone))
                    d.save()
                    self.mem.con.commit()
            else:
                self.mem.log(QApplication.translate("DidYouReadMe","Error sending again message {} to {}").format(mail.document.id, mail.user.mail))  
        cur.close()
        
    def unlink(self):
        """Physical deletion of the document"""
        try:
            os.unlink(dirDocs+self.hash)
        except:
            print ("Error deleting {}. Document {}".format(dirDocs+self.hash,  self.id))
        
        
    def save(self):
        """No se puede modificar, solo insertar de nuevo
        Modificar es cambiar expiration
        It creates or unlinks file in dirDocs según proceda
        Si hubiera necesidad de modificar sería borrar y crear"""
        cur=self.mem.con.cursor()        
        if self.id==None:
            cur.execute("insert into documents (datetime, title, comment, filename, hash, expiration) values (%s, %s, %s, %s, %s, %s) returning id", (self.datetime, self.name, self.comment, self.filename, self.hash,  self.expiration))
            self.id=cur.fetchone()[0]
            self.hash=self.calculateHash()
            cur.execute("update documents set hash=%s where id=%s", (self.hash,  self.id))
            self.file_to_bytea(self.filename)
            self.bytea_to_file(dirDocs+self.hash)
        else:
            cur.execute("update documents set expiration=%s where id=%s", (self.expiration, self.id ))
            if self.isExpired()==False:
                self.bytea_to_file(dirDocs+self.hash)
            else:
                self.unlink()
        cur.close()
        
    def bytea_to_file(self, filename):
#        print("bytea_to_file", filename)
        cur=self.mem.con.cursor()
        cur.execute("SELECT fileb FROM documents where id=%s and fileb is not null;", (self.id, ))#Si es null peta el open, mejor que devuelva fals3ee3 que pasar a variable
        if cur.rowcount==1:
            open(filename, "wb").write(cur.fetchone()[0])
            cur.close()
            return True
        cur.close()
        return False
        
    def file_to_bytea(self, filename):
#        print("file_to_bytea", filename)
        bytea=open(filename,  "rb").read()        
        cur=self.mem.con.cursor()
        cur.execute("update documents set fileb=%s where id=%s", (bytea, self.id))
        cur.close()

    def updateNums(self):
        cur=self.mem.con.cursor()
        cur.execute("select count(*) from userdocuments where id_documents=%s and sent is not null;", (self.id, ))
        self.numsents=cur.fetchone()[0]
        cur.execute("select count(*) from userdocuments where id_documents=%s and numreads>0;", (self.id, ))
        self.numreads=cur.fetchone()[0]
        cur.execute("select count(*) from userdocuments where id_documents=%s;", (self.id, ))
        self.numplanned=cur.fetchone()[0]
        cur.close()
        
class UserDocument:
    def __init__(self, user, document, mem):
        self.user=user
        self.document=document
        self.mem=mem
        cur=mem.con.cursor()
        cur.execute("select * from userdocuments where id_users=%s and id_documents=%s", (self.user.id, self.document.id))
        if cur.rowcount==0:
            self.sent=None
            self.read=None
            self.numreads=0
            self.new=True #Variable que controla si el registro es nuevo o esta en la base de datos
        else:
            row=cur.fetchone()
            self.sent=row['sent']
            self.read=row['read']
            self.numreads=row['numreads']
            self.new=False
        cur.close()
        
    def save(self):
        cur=self.mem.con.cursor()
        if self.new==True:
            cur.execute("insert into userdocuments(id_users,id_documents,sent,read,numreads) values (%s,%s,%s,%s,%s)", 
                                (self.user.id, self.document.id, self.sent, self.read, self.numreads))
        else:
            cur.execute("update userdocuments set sent=%s,read=%s,numreads=%s where id_users=%s and id_documents=%s", 
                                (self.sent, self.read, self.numreads, self.user.id, self.document.id))
        self.mem.con.commit()
        cur.close()
            
        
    def readed(self, localzone):
        """Actualiza datos y salva"""
        
        if self.read==None:
            self.read=datetime.datetime.now(pytz.timezone(localzone))
        self.numreads=self.numreads+1
        self.save()

class Mem:
    def __init__(self):     
        self.con=None
        self.settings=QSettings()
        self.qtranslator=None
        self.countries=SetCountries(self)
        self.countries.load_all()
        self.languages=SetLanguages(self)
        self.languages.load_all()
        self.data=DBData(self)
        self.language=self.languages.find_by_id(self.settings.value("mem/language", "en"))
        self.localzone=self.settings.value("mem/localzone", "Europe/Madrid")
        self.lock_log=multiprocessing.Lock()
        
    def __del__(self):
        if self.con:#Needed when reject frmAccess
            self.con.disconnect()
            
    def log(self, message):
        s="{} {}\n".format(str(datetime.datetime.now()),  message)
        print(s[:-1])
        with self.lock_log:
            f=open(dirDocs+"log.txt", "a")
            f.write(s)
            f.close()
                
    def qicon_admin(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/admin.png"), QIcon.Normal, QIcon.Off)
        return icon

    def setQTranslator(self, qtranslator):
        self.qtranslator=qtranslator

    def hasDidyoureadmeRole(self):
        if "didyoureadme_admin" in self.con.roles or "didyoureadme_user" in self.con.roles:
            return True
        return False
    def isAdminMode(self):
        if "didyoureadme_admin" in self.con.roles:
            return True
        return False

def qmessagebox(text):
    """Common message box"""
    m=QMessageBox()
    m.setWindowIcon(QIcon(":/didyoureadme.png"))
    m.setIcon(QMessageBox.Information)
    m.setText(text)
    m.exec_()     

def qdatetime(dt, localzone):
    """dt es un datetime con timezone
    dt, tiene timezone, 
    Convierte un datetime a string, teniendo en cuenta los microsehgundos, para ello se convierte a datetime local
    SE PUEDE OPTIMIZAR
    No hace falta cambiar antes a dt con local.config, ya que lo hace la función
    """
    if dt==None:
        resultado="None"
    else:
        dt=dt_changes_tz(dt,  localzone)#sE CONVIERTE A LOCAL DE dt_changes_tz 2012-07-11 08:52:31.311368-04:00 2012-07-11 14:52:31.311368+02:00
        resultado=str(dt.date())+" "+str(dt.hour).zfill(2)+":"+str(dt.minute).zfill(2)+":"+str(dt.second).zfill(2)
    a=QTableWidgetItem(resultado)
    if dt==None:
        a.setTextColor(QColor(0, 0, 255))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a
    
    
def qcenter(text):
    a=QTableWidgetItem(str(text))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a    
def qleft(text):
    a=QTableWidgetItem(str(text))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
    return a
    
def dt(date, hour, zonename):
    """Función que devuleve un datetime con zone info.
    Zone is an object."""
    z=pytz.timezone(zonename)
    a=datetime.datetime(date.year,  date.month,  date.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)
    a=z.localize(a)
    return a

def dt_changes_tz(dt,  tztarjet):
    """Cambia el zoneinfo del dt a tztarjet. El dt del parametre tiene un zoneinfo"""
    if dt==None:
        return None
    tzt=pytz.timezone(tztarjet)
    tarjet=tzt.normalize(dt.astimezone(tzt))
    return tarjet


def makedirs(dir):
    try:
        os.makedirs(dir)
    except:
        pass

def now(localzone):
    return datetime.datetime.now(pytz.timezone(localzone))

def c2b(state):
    """QCheckstate to python bool"""
    if state==Qt.Checked:
        return True
    else:
        return False
        


def b2c(booleano):
    """QCheckstate to python bool"""
    if booleano==True:
        return Qt.Checked
    else:
        return Qt.Unchecked     
        
        

