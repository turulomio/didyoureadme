import os,  datetime,  configparser,  hashlib,   psycopg2,  psycopg2.extras,  pytz,  smtplib,  urllib.parse, threading,  time,  shutil
from PyQt4.QtGui import *
from PyQt4.QtCore import *

version="0.1"
version_date=datetime.date(2015,1,26)

dirTmp=os.path.expanduser("/tmp/didyoureadme/")
dirDocs=os.path.expanduser("~/.didyoureadme/docs/")
dirReaded=os.path.expanduser("~/.didyoureadme/readed/")

class Backup:
    def __init__(self):
        pass
    def save(self):
        pass

class SetGroups:
    def __init__(self, mem):
        self.arr=[]
        self.mem=mem
        
    def quit_user_from_all_groups(self, user):
        """Se quita un usuario de todos los grupos tanto l´ogicamente como f´isicamente"""
        
        todelete=None#Se usa para no borrar en iteracion
        for g in self.arr:
            for u in g.members:
                if u==user:
                    todelete=u
            if todelete!=None:
                g.members.remove(user)
                g.save(self.mem)# Para no grabar en bd salvoi que encuente se pone aqu´i
                    
   
    def load(self):
        cur=self.mem.con.cursor()
        cur.execute("select * from groups order by name")
        for row in cur:
            members=set()
            if row['id']==1:#Caso de todos
                for u in self.mem.users.arr:
                    if u.active==True:#Only active
                        members.add(u)
            else:
                for id_user in row['members']:
                    u=self.mem.users.user(id_user)
                    if u.active==True:
                        members.add(u)
            self.arr.append( Group(row['name'], members, row['id']))        
        cur.close()
    
    def group(self, id):
        for p in self.arr:
            if p.id==id:
                return p
        return None

        
    def qlistview(self, list, selected):
        """selected lista de group a seleccionar"""
        self.sort()
        model=QStandardItemModel (len(self.arr), 1); # 3 rows, 1 col
        for i,  g in enumerate(self.arr):
            item = QStandardItem(g.name)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled);
            if g in selected:
                item.setData(Qt.Checked, Qt.CheckStateRole)
            else:
                item.setData(Qt.Unchecked, Qt.CheckStateRole); #para el role check
            item.setData(g.id, Qt.UserRole) # Para el role usuario
            model.setItem(i, 0, item);
        list.setModel(model)
        
    def sort(self):
        self.arr=sorted(self.arr, key=lambda g: g.name)
        
class Group:
    def __init__(self,  name, members,  id=None):
        """members es un array a objetos User"""
        self.id=id
        self.members=members
        self.name=name
        
    def delete(self, mem):
        #Borra de la base de datos
        cur=mem.con.cursor()
        cur.execute("delete from groups where id=%s", (self.id, ))
        #Borra el grupo de self.mem.groups
        mem.con.commit()
        cur.close()
        mem.groups.arr.remove(self)
        
    def save(self, mem):
        def members2pg():
            if len(self.members)==0:
                return "'{}'"
            resultado=""
            for m in self.members:
                resultado=resultado + str(m.id)+", "
            return "ARRAY["+resultado[:-2]+"]"
            
        cur=mem.con.cursor()
        if self.id==None:
            #Crea registro en base de datos
            cur.execute("insert into groups (name,members) values(%s, "+members2pg() +") returning id", (self.name, ))
            self.id=cur.fetchone()[0]
            #Añade a self.mem.groups
            mem.groups.arr.append(self)

        else:
            #Modifica registro en base de datos
            cur.execute("update groups set name=%s, members="+members2pg()+" where id=%s",(self.name, self.id ))
        mem.con.commit()
        cur.close()
            
            
        
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
        initparams son los parametros de iniciaci´on de la clase"""
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        for a in self.arr:
            result.append(a)
        return result
        
    def union(self,  set,  *initparams):
        """Returns a new set, with the union comparing id
        initparams son los parametros de iniciaci´on de la clse"""        
        resultado=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca SetProduct(self.mem), luego ser´a self.mem
        for p in self.arr:
            resultado.append(p)
        for p in set.arr:
            if resultado.find(p.id, False)==None:
                resultado.append(p)
        return resultado
        
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
        """Selected is the id"""
        self.order_by_name()
        for l in self.arr:
            combo.addItem(self.mem.countries.find(l.id).qicon(), l.name, l.id)
        if selected!=None:
                combo.setCurrentIndex(combo.findData(selected.id))

    def cambiar(self, id):  
        """language es un string"""
        self.mem.qtranslator.load("/usr/lib/xulpymoney/didyoureadme_" + id + ".qm")
        qApp.installTranslator(self.mem.qtranslator);
#        def cargarQTranslator(cfgfile):  
#    """language es un string"""
#    so=os.environ['didyoureadmeso']
#    if so=="src.linux":
#        cfgfile.qtranslator.load("/usr/share/didyoureadme/didyoureadme_" + cfgfile.language + ".qm")
#    elif so=="src.windows":
#        cfgfile.qtranslator.load("../share/didyoureadme/didyoureadme_" + cfgfile.language + ".qm")
#    elif so=="bin.windows" or so=="bin.linux":
#        cfgfile.qtranslator.load("didyoureadme_" + cfgfile.language + ".qm")
#    qApp.installTranslator(cfgfile.qtranslator);
        
class SetUsers:
    def __init__(self, mem):
        self.arr=[]
        self.mem=mem
    

    def user(self, id):
        for u in self.arr:
            if u.id==id:
                return u
        print ("User not found")
        return None
    def user_from_hash(self, hash):
        for u in self.arr:
            if u.hash==hash:
                return u
        print ("User not found")
        return None
        
    def load(self):
        cur=self.mem.con.cursor()
        cur.execute("select * from users")
        for row in cur:
            self.arr.append(User(row['datetime'],  row['post'], row['name'], row['mail'], row['active'], row['hash'],  row['id']))
        cur.close()
            

    
    def qlistview(self, list, inactivos, selected):
        """inactivos si muestra inactivos
        selected lista de user a seleccionar"""
        self.sort()
        model=QStandardItemModel (len(self.arr), 1); # 3 rows, 1 col
        for i,  u in enumerate(self.arr):
            if inactivos==False and u.active==False:
                continue
            item = QStandardItem(u.name)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled);
            if u in selected:
                item.setData(Qt.Checked, Qt.CheckStateRole)
            else:
                item.setData(Qt.Unchecked, Qt.CheckStateRole); #para el role check
            item.setData(u.id, Qt.UserRole) # Para el role usuario
            model.setItem(i, 0, item);
        list.setModel(model)
        
    def sort(self):
        self.arr=sorted(self.arr, key=lambda u: u.name)

class User:
    def __init__(self, dt, post, name, mail, active=True, hash="hash no calculado",  id=None):
        self.id=id
        self.datetime=dt#incorporation date
        self.name=name
        self.mail=mail
        self.hash=hash
        self.post=post
        self.sent=0
        self.read=0
        self.active=active

    def __repr__(self):
        return "{0} ({1})".format(self.name, self.id)
                
                
    def isDeletable(self, mem):
        for g in mem.groups.arr:
            if self  in g.members and g.id!=1:
                return False
        
        cur=mem.con.cursor()
        cur.execute("select count(*) from userdocuments where id_users=%s", (self.id, ))
        if cur.fetchone()[0]>0:
            return False
        return True
        
    def delete(self, mem):
        #Borra de la base de datos
        cur=mem.con.cursor()
        cur.execute("delete from users where id=%s", (self.id, ))
        #Borra el grupo de self.mem.users
        mem.con.commit()
        cur.close()
        mem.users.arr.remove(self)
        mem.groups.group(1).members.remove(self)#Añade el usuario al grupo uno. el de todos
        
    def getHash(self):
        if self.id==None:
            return None
        return hashlib.sha256(("u."+str(self.id)+str(self.datetime)).encode('utf-8')).hexdigest()
    
    def save(self, mem):
        cur=mem.con.cursor()        
        if self.id==None:
            cur.execute("insert into users (datetime,post,name,mail, hash, active) values(%s,%s,%s,%s,%s, %s) returning id ", (self.datetime, self.post, self.name, self.mail, self.hash, self.active))
            self.id=cur.fetchone()[0]
            self.hash=self.getHash()
            self.sent=0
            self.read=0
            cur.execute("update users set hash=%s where id=%s", (self.hash, self.id))
            mem.users.arr.append(self)
            mem.groups.group(1).members.append(self)#Añade el usuario al grupo uno. el de todos
        else:
            cur.execute("update users set datetime=%s, post=%s, name=%s, mail=%s, active=%s where id=%s", (self.datetime, self.post, self.name, self.mail,  self.active, self.id))
        mem.con.commit()
        cur.close()

    def updateSent(self, cur):
        cur.execute("select count(*) from userdocuments where id_users=%s", (self.id, ))
        self.sent= cur.fetchone()[0]


    def updateRead(self, cur):
        cur.execute("select count(*) from userdocuments where id_users=%s and read is not null", (self.id, ))
        self.read=cur.fetchone()[0]


class TUpdateData(threading.Thread):
    def __init__(self, mem):
        threading.Thread.__init__(self)
        self.mem=mem
        self.errorupdating=0
    
    def run(self):    
        con=self.mem.connect()
        cur=con.cursor()
        #Actualiza userdocuments
        for file in os.listdir(dirReaded):
            try:
                (userhash, documenthash)=file.split("l")
                ud=UserDocument(self.mem.users.user_from_hash(userhash), self.mem.documents.document_from_hash(documenthash), self.mem)
                ud.readed( self.mem.cfgfile.localzone)
                con.commit()
            except:
                self.errorupdating=self.errorupdating+1
                f=open(self.mem.pathlogupdate, "a")
                f.write(QApplication.translate("didyoureadme","{0} Error updating data with hash: {1}\n").format(now(self.mem.cfgfile.localzone), file))
                f.close()
            finally:
                os.remove(dirReaded+file)
            
        #Actualiza users
        for u in self.mem.users.arr:
            u.updateSent(cur)
            u.updateRead(cur)
            
        #Consulta
        for i, d in enumerate(self.mem.documents.arr):
            if d.isExpired()==False:
                d.updateNums(cur)            
        cur.close()  
        self.mem.disconnect(con)

class TSend(threading.Thread):
    def __init__(self, mem):
        threading.Thread.__init__(self)
        self.mem=mem
        self.errorsending=0

    
    def run(self):    
        con=self.mem.connect()#NO SE PORQUE NO ACTUALIZABA SI USABA CONEXI´ON DE PARAMETRO
        cur=con.cursor()
        cur2=con.cursor()
        #5 minutos delay
        cur.execute("select id_documents, id_users from userdocuments, documents where userdocuments.id_documents=documents.id and sent is null and now() > datetime + interval '1 minute';")
        for row in cur:
            doc=self.mem.documents.document(row['id_documents'])
            u=self.mem.users.user(row['id_users'])
            mail=Mail(doc, u, self.mem)
            mail.send()
            
            if mail.sent==True:
                print ("Send message of document {0} to {1}".format(mail.document.id, mail.user.mail))
                d=UserDocument(mail.user, mail.document, self.mem)
                if d.sent==None:
                    d.sent=datetime.datetime.now(pytz.timezone(self.mem.cfgfile.localzone))
                d.save()
                con.commit()
            else:
                self.errorsending=self.errorsending+1  
                try: #Unicode en mail
                    f=open(self.mem.pathlogmail, "a")
                    f.write(QApplication.translate("didyoureadme","{0} Error sending message {1} to {2}\n").format(now(self.mem.cfgfile.localzone), mail.document.id, mail.user.mail))
                    f.close()          
                except:
                    print ("TSend error al escribir log")
            mail.document.updateNums(cur2)
            time.sleep(5)                  
        cur.close()
        cur2.close()
        self.mem.disconnect(con)
        
            
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
        self.title=document.title
        self.sent=None


    def message(self):
        def weekday(noww):
            """Se hace esta funci´on para que no haya problemas con la localizaci´on de %a"""
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
            """Se hace esta funci´on para que no haya problemas con la localizaci´on de %b"""
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
            
        url="http://{0}:{1}/get/{2}l{3}/{4}".format(self.mem.cfgfile.webserver,  self.mem.cfgfile.webserverport, self.user.hash, self.document.hash, urllib.parse.quote(os.path.basename(self.document.filename.lower())))

        comment=""
        if self.document.comment!="":
            comment=self.document.comment+"\n\n___________________________________________________________\n\n"
        noww=now(self.mem.cfgfile.localzone)
        s= ("From: "+self.mem.cfgfile.smtpfrom+"\n"+
        "To: "+self.user.mail+"\n"+
        "MIME-Version: 1.0\n"+
        "Subject: "+ self.document.title+"\n"+
        "Date: " + weekday(noww)+", " + str(noww.strftime("%d"))+" "+ month(noww)+" "+ str(noww.strftime("%Y %X %z")) +"\n"+
        "Content-Type: text/plain; charset=UTF-8\n" +
        "\n"+
        comment +
        QApplication.translate("DidYouReadMe","This is an automatic and personal mail from DidYouReadMe.")+"\n\n"+
        QApplication.translate("DidYouReadMe", "Don't answer and don't resend this mail.")+"\n\n"+
        QApplication.translate("DidYouReadMe", "When you click the next link, you will get the document associated to this mail and it will be registered as read:")+"\n\n"+
        url +"\n\n"+
        self.mem.cfgfile.smtpsupport)
        return s.encode('UTF-8')
    
    def send(self):      
        if self.mem.cfgfile.smtpTLS=="True":
            server = smtplib.SMTP(self.mem.cfgfile.smtpserver)
            try:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.mem.cfgfile.smtpuser,self.mem.cfgfile.smtppwd)
                server.sendmail(self.mem.cfgfile.smtpfrom, self.user.mail, self.message())
                self.sent=True        
            except:
                self.sent=False
            finally:     
                server.quit()
        else:  #ERA EL ANTIVIRUS
            server = smtplib.SMTP(self.mem.cfgfile.smtpserver, 25)
            try:
                server.login(self.mem.cfgfile.smtpuser,self.mem.cfgfile.smtppwd)
                server.helo()
                server.sendmail(self.mem.cfgfile.smtpfrom, self.user.mail, self.message())
                self.sent=True        
            except:
                self.sent=False
            finally:     
                server.quit()
        return self.sent



class SetCountries(SetCommons):
    def __init__(self, mem):
        SetCommons.__init__(self)
        self.mem=mem   
        
    def load_all(self):
        self.append(Country().init__create("es",QApplication.translate("Core","Spain")))
        self.append(Country().init__create("be",QApplication.translate("Core","Belgium")))
        self.append(Country().init__create("cn",QApplication.translate("Core","China")))
        self.append(Country().init__create("de",QApplication.translate("Core","Germany")))
        self.append(Country().init__create("en",QApplication.translate("Core","United Kingdom")))
        self.append(Country().init__create("eu",QApplication.translate("Core","Europe")))
        self.append(Country().init__create("fi",QApplication.translate("Core","Finland")))
        self.append(Country().init__create("fr",QApplication.translate("Core","France")))
        self.append(Country().init__create("ie",QApplication.translate("Core","Ireland")))
        self.append(Country().init__create("it",QApplication.translate("Core","Italy")))
        self.append(Country().init__create("jp",QApplication.translate("Core","Japan")))
        self.append(Country().init__create("nl",QApplication.translate("Core","Netherlands")))
        self.append(Country().init__create("pt",QApplication.translate("Core","Portugal")))
        self.append(Country().init__create("us",QApplication.translate("Core","United States of America")))
        self.append(Country().init__create("ro",QApplication.translate("Core","Romanian")))
        self.append(Country().init__create("ru",QApplication.translate("Core","Rusia")))
        self.order_by_name()

    def qcombobox(self, combo,  country=None):
        """Función que carga en un combo pasado como parámetro y con un SetAccounts pasado como parametro
        Se ordena por nombre y se se pasa el tercer parametro que es un objeto Account lo selecciona""" 
        for cu in self.arr:
            combo.addItem(cu.qicon(), cu.name, cu.id)

        if country!=None:
                combo.setCurrentIndex(combo.findData(country.id))

    def qcombobox_translation(self, combo,  country=None):
        """Función que carga en un combo pasado como parámetro con los pa´ises que tienen traducci´on""" 
        for cu in [self.find("es"),self.find("fr"),self.find("ro"),self.find("ru"),self.find("en") ]:
            combo.addItem(cu.qicon(), cu.name, cu.id)

        if country!=None:
                combo.setCurrentIndex(combo.findData(country.id))

class SetDocuments:
    def __init__(self, mem):
        self.arr=[]
        self.mem=mem #solo se usa para conexion, los datos se guardan en arr
                
    def load(self, sql):
        """Carga seg´un el sql pasado debe ser un select * from documents ...."""
        cur=self.mem.con.cursor()
        cur.execute(sql)
        for row in cur:
            d=Document(self.mem, row['datetime'], row['title'], row['filename'], row['comment'],  row['expiration'],  row['hash'], row['id']  )
            self.arr.append(d)        
        for d in self.arr:
            d.updateNums(cur)
        cur.close()
        
    def sort(self):
        """Ordena por datetime"""
        self.arr=sorted(self.arr, key=lambda d: d.datetime)        
            
    def document(self, id):
        for d in self.arr:
            if d.id==id:
                return d
        return None
        print ("Document not found")
        
    def document_from_hash(self, hash):
        for d in self.arr:
            if d.hash==hash:
                return d
        print ("Document not found from hash")
        return None


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
            

class Document:
    def __init__(self, mem,  dt, title, filename, comment, expiration,  hash='Not calculated',  id=None):
        self.mem=mem
        self.id=id
        self.datetime=dt
        self.title=title
        self.filename=filename
        self.comment=comment
        self.hash=hash
        self.numreads=0
        self.numsents=0
        self.numplanned=0
        self.expiration=expiration
        
    def __repr__(self):
        return "{0} ({1})".format(self.title, self.id)
        
    def isExpired(self):
        if self.expiration>now(self.mem.cfgfile.localzone):
            return False
        return True
        
    def getHash(self):
        """Se mete el datetime porque sino se podr´ia adivinar el ocmunicado"""
        return hashlib.sha256(("d."+str(self.id)+str(self.datetime)).encode('utf-8')).hexdigest()


    def delete(self, mem):
        #Borra el registro de base de datosv
        cur=mem.con.cursor()
        cur.execute("delete from documents where id=%s", (self.id, ))        
        cur.close()
        
        #Borra el fichero de readed
        os.unlink(dirDocs+self.hash)
        
        #Elimina el documento de self.mem.documents.
        mem.documents.arr.remove(self)
        
        
        
#        def delete(self):
#                cur=self.mem.con.cursor()
#                sqllo0="select lo_unlink("+str(self.foto)+");"
#                cur.execute(sqllo0)
#                sqldel="delete from films where id_films=" + str(self.id) + ";"
#                cur.execute(sqldel)
#                cur.close()
#
#        def extract_foto(self):
#                """Extracts and assign self.pathfoto"""
#                self.pathfoto='/tmp/pdffilms/{0}.jpg'.format(self.foto)
#                cur=self.mem.con.cursor()
#                sql="select lo_export({0}, '{1}');".format(self.foto,self.pathfoto)
#                cur.execute(sql)
#                cur.close()
#
#        def save(self):
#                if self.id==None:
#                        if self.year==None:
#                                name=self.name
#                        else:
#                                name="{}. {}".format(self.name,self.year)
#                        cur.execute("insert into films (savedate, name, foto, id_dvd) values (%s, %s, lo_import(%s), %s) returning id_films;",(self.savedate,name,self.pathfoto, self.id_dvd))
#                        self.id=cur.fetchone()[0]
#                        return True

        
        
    def save(self, mem):
        """No se puede modificar, solo insertar de nuevo
        Modificar es cambiar closed
        Si hubiera necesidad de modificar ser´ia borrar y crear"""
        cur=mem.con.cursor()        
        if self.id==None:
            cur.execute("insert into documents (datetime, title, comment, filename, hash, expiration) values (%s, %s, %s, %s, %s, %s) returning id", (self.datetime, self.title, self.comment, self.filename, self.hash,  self.expiration))
            self.id=cur.fetchone()[0]
            self.hash=self.getHash()
            shutil.copyfile(self.filename, "/tmp/"+self.hash)#Copia a /tmp (permisos postgres)
            cur.execute("update documents set hash=%s,file=lo_import(%s) where id=%s", (self.hash, "/tmp/"+self.hash,  self.id))
            os.system("mv {} {}".format("/tmp/" +self.hash, dirDocs+self.hash))
        else:
            cur.execute("update documents set expiration=%s where id=%s", (self.expiration, self.id ))
        mem.con.commit()
        cur.close()
        

    def updateNums(self, cur):
        cur.execute("select count(*) from userdocuments where id_documents=%s and sent is not null;", (self.id, ))
        self.numsents=cur.fetchone()[0]
        cur.execute("select count(*) from userdocuments where id_documents=%s and numreads>0;", (self.id, ))
        self.numreads=cur.fetchone()[0]
        cur.execute("select count(*) from userdocuments where id_documents=%s;", (self.id, ))
        self.numplanned=cur.fetchone()[0]
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
        
class ConfigFile:
    def __init__(self, file):
        self.error=False#Variable que es True cuando se produce un error
        self.file=file
        self.language="en"
        self.localzone="Europe/Madrid"
        self.database="didyoureadme"
        self.port="5432"
        self.user="Usuario"
        self.server="127.0.0.1"
        self.pwd="None"
        self.lastupdate=datetime.date.today().toordinal()
        self.smtpfrom="didyoureadme@donotanswer.com"
        self.smtpserver="127.0.0.1"
        self.smtpuser="UsuarioSMTP"
        self.smtpsupport="Please contact system administrator if you have any problem"
        self.smtppwd="pass"       
        self.smtpport="25"
        self.smtpTLS="False"
        self.webserver="127.0.0.1"
        self.webserverport="8000"
        self.webinterface="127.0.0.1"
        self.autoupdate="True"
        
        self.config=configparser.ConfigParser()
        self.load()
        
    def load(self):
        try:
            self.config.read(self.file)
            self.language=self.config.get("frmSettings", "language")
            self.localzone=self.config.get("frmSettings", "localzone")
            self.lastupdate=self.config.getint("frmMain", "lastupdate")
            self.database=self.config.get("frmAccess", "database")
            self.port=self.config.get("frmAccess", "port")
            self.user=self.config.get("frmAccess", "user")
            self.server=self.config.get("frmAccess", "server")        
            self.smtpfrom=self.config.get("smtp", "from")
            self.smtpserver=self.config.get("smtp", "smtpserver")
            self.smtpport=self.config.get("smtp", "smtpport")
            self.smtpuser=self.config.get("smtp", "smtpuser")
            self.smtppwd=self.config.get("smtp", "smtppwd")
            self.smtpsupport=self.config.get("smtp", "support")
            self.smtpTLS=self.config.get("smtp", "tls")
            self.webserver=self.config.get("webserver", "ip")
            self.webserverport=self.config.get("webserver", "port")
            self.webinterface=self.config.get("webserver", "interface")
            self.autoupdate=self.config.get("frmSettings", "autoupdate")
        except:
            self.error=True
        
    def save(self):
        if self.config.has_section("frmMain")==False:
            self.config.add_section("frmMain")
        if self.config.has_section("frmSettings")==False:
            self.config.add_section("frmSettings")
        if self.config.has_section("frmAccess")==False:
            self.config.add_section("frmAccess")
        if self.config.has_section("smtp")==False:
            self.config.add_section("smtp")
        if self.config.has_section("webserver")==False:
            self.config.add_section("webserver")
        self.config.set("frmAccess",  'database', self.database)
        self.config.set("frmAccess",  'port', self.port)
        self.config.set("frmAccess",  'user', self.user)
        self.config.set("frmAccess",  'server', self.server)
        self.config.set("frmSettings",  'language', self.language)
        self.config.set("frmSettings",  'localzone', self.localzone)
        self.config.set("frmSettings",  'autoupdate', self.autoupdate)
        self.config.set("frmMain",  'lastupdate', str(self.lastupdate))
        self.config.set("smtp", "from", self.smtpfrom)
        self.config.set("smtp", "smtpserver", self.smtpserver)
        self.config.set("smtp", "smtpport", self.smtpport)
        self.config.set("smtp", "smtpuser", self.smtpuser)
        self.config.set("smtp", "smtppwd", self.smtppwd)
        self.config.set("smtp", "tls", self.smtpTLS)
        self.config.set("smtp", "support", self.smtpsupport)
        self.config.set("webserver", "ip", self.webserver)
        self.config.set("webserver", "port", self.webserverport)
        self.config.set("webserver", "interface", self.webinterface)
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)
            
class Mem:
    def __init__(self):     
        self.con=None
        self.adminmode=False
        self.cfgfile=ConfigFile(os.path.expanduser("~/.didyoureadme/")+ "didyoureadme.cfg")
        self.cfgfile.save()
        self.pathlogmail=os.path.expanduser("~/.didyoureadme/mail.log")
        self.pathlogupdate=os.path.expanduser("~/.didyoureadme/updatedata.log")
        self.qtranslator=None
        self.countries=SetCountries(self)
        self.countries.load_all()
        self.languages=SetLanguages(self)
        self.languages.load_all()
        
    def __del__(self):
        if self.con:#Needed when reject frmAccess
            self.disconnect(self.con)
                
    def qicon_admin(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/admin.png"), QIcon.Normal, QIcon.Off)
        return icon

    def setQTranslator(self, qtranslator):
        self.qtranslator=qtranslator
            
    def set_admin_mode(self, pasw):
        cur=self.con.cursor()
        cur.execute("update globals set value=md5(%s) where id_globals=6;", (pasw, ))
        cur.close()
        
    def check_admin_mode(self, pasw):
        """Returns: 
                - None: No admin password yet
                - True: parameter pasw is ok
                - False: parameter pasw is wrong"""
        cur=self.con.cursor()
        cur.execute("select value from globals where id_globals=6")
        val=cur.fetchone()[0]
        if val==None or val=="":
            resultado=None
        else:
            cur.execute("select value=md5(%s) from globals where id_globals=6;", (pasw, ))
            resultado=cur.fetchone()[0]
        cur.close()
        print (resultado,  "check_admin_mode")
        return resultado
        
    def cargar_datos(self):       
        self.users=SetUsers(self)     
        self.users.load() 
        self.groups=SetGroups(self)
        self.groups.load()
        self.documents=SetDocuments(self) #Son documentos activos
        self.documents.load("select * from documents where expiration>now() order by datetime")

    def connect(self):
        strmq="dbname='%s' port='%s' user='%s' host='%s' password='%s'" % (self.cfgfile.database,  self.cfgfile.port, self.cfgfile.user, self.cfgfile.server,  self.cfgfile.pwd)
        try:
            mq=psycopg2.extras.DictConnection(strmq)
            return mq
        except psycopg2.Error:
            m=QMessageBox()
            m.setText(QApplication.translate("DidYouReadMe","Connection error. Try again"))
            m.exec_()
            sys.exit()

    def disconnect(self,  mq):
        mq.close()



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
