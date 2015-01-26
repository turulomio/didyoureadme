from libdidyoureadme import *
class Update:
    """DB update system
    Cuando vaya a crear una nueva modificaci´on pondre otro if con menor que current date para uqe se ejecute solo una vez al final, tendra que 
    poner al final self.me.set_database_version(current date)
    
    To check if this class works fine, you must use a subversion 
        Subversion      DBVersion
        1702                None
    
    El sistema update sql ya tiene globals y  mete la versi´on de la base de datos del desarrollador, no obstante,
    
    AFTER EXECUTING I MUST RUN SQL UPDATE SCRIPT TO UPDATE FUTURE INSTALLATIONS
    
    OJO EN LOS REEMPLAZOS MASIVOS PORQUE UN ACTIVE DE PRODUCTS LUEGO PASA A LLAMARSE AUTOUPDATE PERO DEBERA MANTENERSSE EN SU MOMENTO TEMPORAL
    """
    def __init__(self, mem):
        self.mem=mem
        
        self.dbversion=self.get_database_version()     
        if self.dbversion==None:
            cur=self.mem.con.cursor()
            cur.execute("CREATE TABLE globals (id_globals integer NOT NULL,  global text,  value text);")
            cur.execute("ALTER TABLE documents add COLUMN datetime_end timestamp with time zone default now() + interval '3 months' not null;")
            cur.execute("ALTER TABLE documents add COLUMN file oid;")
            cur.close()
            self.mem.con.commit()
            self.set_database_version(201501260851)
        if self.dbversion<201501261046: #Documentos a base de datos
        
            print ("**** Migrating old didyoureadme files")
            cur=self.mem.con.cursor()
            cur2=self.mem.con.cursor()
            cur.execute("select * from documents;")
            for row in cur:
                if os.path.exists(dirDocs+row['hash'])==False:
                    print ("No existe y no se puede cargar a base de datos",  row['hash'])
                    continue
                if row['file']==None:
                    os.system("cp {} /tmp".format(dirDocs+row['hash']))
                    cur2.execute("update documents set file=lo_import(%s) where id=%s", ("/tmp/"+row['hash'], row['id']))
                    print ("Insertando en database para oid vacio ",  row['hash'])
                    os.system("rm /tmp/{}".format(row['hash']))
            cur2.close()
            cur.close()
            self.mem.con.commit()
            self.set_database_version(201501261046)
        if self.dbversion<201501261228: #Removes closed and update expiration to 3 months
            cur=self.mem.con.cursor()
            cur.execute("alter table documents rename datetime_end to expiration;")
            cur.execute("alter table documents drop column closed;")      
            cur2=self.mem.con.cursor()
            cur.execute("select * from documents;")
            for row in cur:
                cur2.execute("update documents set expiration=datetime + interval '3 months' where id=%s", (row['id'], ))
            cur2.close()
            cur.close()
            self.mem.con.commit()
            self.set_database_version(201501261228)
        if self.dbversion<201501261900: #Removes closed and update expiration to 3 months
            cur=self.mem.con.cursor()
            cur.execute("insert into globals (id_globals,global,value) values (%s,%s,%s);", (6,"Admin mode", None ))
            self.mem.con.commit()
            self.set_database_version(201501261900)   
            

        """AFTER EXECUTING I MUST RUN SQL UPDATE SCRIPT TO UPDATE FUTURE INSTALLATIONS
    
    OJO EN LOS REEMPLAZOS MASIVOS PORQUE UN ACTIVE DE PRODUCTS LUEGO PASA A LLAMARSE AUTOUPDATE PERO DEBERA MANTENERSSE EN SU MOMENTO TEMPORAL"""  
        self.load_files()
        print ("**** Database already updated")
   
   
    def load_files(self):
        """THis function download all files from database to .didyoureadme/docs/  when needed"""
        print ("**** Regenerating files in .didyoureadme/docs")
        cur=self.mem.con.cursor()
        cur2=self.mem.con.cursor()
        cur.execute("select * from documents;")
        for row in cur:
            if os.path.exists(dirDocs+row['hash'])==False:
                cur2.execute("select lo_export(%s, %s);", (row['file'],"/tmp/"+row['hash']))
                os.system("mv /tmp/{} {}".format(row['hash'], dirDocs))
                print ("Copying a .didyoureadme/docs",  row['hash'])
        cur2.close()
        cur.close()
        
   
   
    def get_database_version(self):
        """REturns None or an Int"""
        
        cur=self.mem.con.cursor()
        #Compruba si existe globals
        cur.execute("SELECT EXISTS ( SELECT 1 FROM   pg_catalog.pg_class c   JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace  WHERE  n.nspname = 'public'  AND    c.relname = 'globals');")
        resultado=cur.fetchone()[0]
        if resultado==False:
            cur.close()
            return None           
        
        #Comprueba el valor 
        cur.execute("select value from globals where id_globals=1;")
        if cur.rowcount==0:
            cur.close()
            return None
        resultado=cur.fetchone()['value']
        cur.close()
        self.dbversion=int(resultado)
        return self.dbversion
        
    def set_database_version(self, valor):
        """Tiene el commit"""
        print ("**** Updating database from {} to {}".format(self.dbversion, valor))
        cur=self.mem.con.cursor()
        if self.dbversion==None:
            cur.execute("insert into globals (id_globals,global,value) values (%s,%s,%s);", (1,"Version", valor ))
        else:
            cur.execute("update globals set global=%s, value=%s where id_globals=1;", ("Version", valor ))
        cur.close()        
        self.dbversion=valor
        self.mem.con.commit()
