from didyoureadme.libdidyoureadme import *
class Update:
    """DB update system
    Cuando vaya a crear una nueva modificación pondre otro if con menor que current date para uqe se ejecute solo una vez al final, tendra que 
    poner al final self.me.set_database_version_date(current date)
    
    To check if this class works fine, you must use a subversion_date 
        Subversion_date      dbversion
        1702                None
    
    El sistema update sql ya tiene globals y  mete la versión de la base de datos del desarrollador, no obstante,
    
    AFTER EXECUTING I MUST RUN SQL UPDATE SCRIPT TO UPDATE FUTURE INSTALLATIONS
    
    OJO EN LOS REEMPLAZOS MASIVOS PORQUE UN ACTIVE DE PRODUCTS LUEGO PASA A LLAMARSE AUTOUPDATE PERO DEBERA MANTENERSSE EN SU MOMENTO TEMPORAL
    """
    def __init__(self, mem):
        self.mem=mem
        
        self.dbversion=self.get_database_version_date()     
        self.lastcodeupdate=201605191906    
        
    def need_update(self):
        """Returns if update must be done"""
        if self.dbversion>self.lastcodeupdate:
            print ("WARNING. DBVEERSION > LAST CODE UPDATE, PLEASE UPDATE LASTCODEUPDATE IN CLASS")
        if self.dbversion==self.lastcodeupdate:
            return False
        return True

    def run(self): 
        if self.dbversion==None:
            cur=self.mem.con.cursor()
            cur.execute("CREATE TABLE globals (id_globals integer NOT NULL,  global text,  value text);")
            cur.execute("ALTER TABLE documents add COLUMN datetime_end timestamp with time zone default now() + interval '3 months' not null;")
            cur.execute("ALTER TABLE documents add COLUMN file oid;")
            cur.close()
            self.mem.con.commit()
            self.set_database_version_date(201501260851)
        if self.dbversion<201501261046: #Documentos a base de datos
            self.mem.log("Migrating old didyoureadme files")
            cur=self.mem.con.cursor()
            cur2=self.mem.con.cursor()
            self.mem.log("THIS MUST BE DONE IN THE DATABASE SERVER")
            cur.execute("select * from documents;")
            for row in cur:
                if os.path.exists(dirDocs+row['hash'])==False:
                    self.mem.log("No existe y no se puede cargar la base de datos" + row['hash'])
                    continue
                if row['file']==None:
                    os.system("cp {} /tmp".format(dirDocs+row['hash']))
                    cur2.execute("update documents set file=lo_import(%s) where id=%s", ("/tmp/"+row['hash'], row['id']))
                    self.mem.log("Insertando en database para oid vacio "+  row['hash'])
                    os.system("rm /tmp/{}".format(row['hash']))
            cur2.close()
            cur.close()
            self.mem.con.commit()
            self.set_database_version_date(201501261046)
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
            self.set_database_version_date(201501261228)
        if self.dbversion<201501261900: #Removes closed and update expiration to 3 months
            cur=self.mem.con.cursor()
            cur.execute("insert into globals (id_globals,global,value) values (%s,%s,%s);", (6,"Admin mode", None ))
            self.mem.con.commit()
            cur.close()
            self.set_database_version_date(201501261900)   
        if self.dbversion<201501281348: #Removes closed and update expiration to 3 months
            cur=self.mem.con.cursor()
            cur.execute("""CREATE OR REPLACE FUNCTION lo_readall(oid) RETURNS bytea
AS $_$

SELECT loread(q3.fd, q3.filesize + q3.must_exec) FROM
	(SELECT q2.fd, q2.filesize, lo_lseek(q2.fd, 0, 0) AS must_exec FROM
		(SELECT q1.fd, lo_lseek(q1.fd, 0, 2) AS filesize FROM
			(SELECT lo_open($1, 262144) AS fd)
		AS q1)
	AS q2)
AS q3

$_$ LANGUAGE sql STRICT;""")
            cur.execute("ALTER TABLE documents add COLUMN fileb bytea;")
            cur.close()
            self.mem.con.commit()
            self.set_database_version_date(201501281348)           
        if self.dbversion<201501281350: #Removes closed and update expiration to 3 months
            cur=self.mem.con.cursor()
            cur2=self.mem.con.cursor()
            cur.execute("Select * from documents;")
            for row in cur:
                cur2.execute("update documents set fileb=lo_readall(%s) where id=%s", (row['file'], row['id']))
                print (".", )
            cur.close()
            cur2.close()
            self.mem.con.commit()
            self.set_database_version_date(201501281350)   
        if self.dbversion<201501281524: #Removes closed and update expiration to 3 months
            cur=self.mem.con.cursor()
            cur.execute("alter table documents drop column file;")      #SHOURLD RUN vacuumlo -U postgres didyoreadme in a console
            cur.close()
            self.mem.con.commit()
            self.set_database_version_date(201501281524)   
        if self.dbversion<201605191906:
            cur=self.mem.con.cursor()
            cur.execute("create role didyoureadme_admin")
            cur.execute("grant all privileges on all tables in schema public to didyoureadme_admin;")      #SHOURLD RUN vacuumlo -U postgres didyoreadme in a console
            cur.execute("grant all privileges on all sequences in schema public to didyoureadme_admin;")
            cur.execute("delete from globals where id_globals=6")
            cur.execute("ALTER TABLE globals DROP COLUMN id_globals")
            cur.execute("ALTER TABLE globals ADD CONSTRAINT globals_pk PRIMARY KEY (global)")
            cur.close()
            self.mem.con.commit()
            self.set_database_version_date(201605191906)   
            

        """AFTER EXECUTING I MUST RUN SQL UPDATE SCRIPT TO UPDATE FUTURE INSTALLATIONS
    
    OJO EN LOS REEMPLAZOS MASIVOS PORQUE UN ACTIVE DE PRODUCTS LUEGO PASA A LLAMARSE AUTOUPDATE PERO DEBERA MANTENERSSE EN SU MOMENTO TEMPORAL"""  
        self.mem.log("Database already updated")
        
    def syncing_files(self):
        """THis function download all files from database to .didyoureadme/docs/  when needed"""
        self.mem.log("Syncing files in .didyoureadme/docs")
        cur=self.mem.con.cursor()
        cur.execute("select id, datetime, title, comment, filename, hash, expiration  from documents;")
        for row in cur:                
            d=Document(self.mem)
            d.id=row['id']
            d.expiration=row['expiration']
            d.hash=row['hash']
            if d.isExpired():
                if os.path.exists(dirDocs+d.hash)==True:
                    d.unlink()
                    self.mem.log("Removing expired document: {}".format(dirDocs+d.hash))
            else:#Not expired
                if os.path.exists(dirDocs+d.hash)==False:
                    d.bytea_to_file(dirDocs+d.hash)
                    self.mem.log("Adding document: {}".format(dirDocs+d.hash))
        cur.close()
        
   
    def get_database_version_date(self):
        """REturns None or an Int"""
        
        cur=self.mem.con.cursor()
        #Compruba si existe globals
        cur.execute("SELECT EXISTS ( SELECT 1 FROM   pg_catalog.pg_class c   JOIN   pg_catalog.pg_namespace n ON n.oid = c.relnamespace  WHERE  n.nspname = 'public'  AND    c.relname = 'globals');")
        resultado=cur.fetchone()[0]
        if resultado==False:
            cur.close()
            return None           
        
        #Comprueba el valor 
        cur.execute("select value from globals where global='version_date'")
        if cur.rowcount==0:
            cur.close()
            return None
        resultado=cur.fetchone()['value']
        cur.close()
        self.dbversion=int(resultado)
        return self.dbversion
        
    def set_database_version_date(self, valor):
        """Tiene el commit"""
        self.mem.log("Updating database from {} to {}".format(self.dbversion, valor))
        cur=self.mem.con.cursor()
        if self.dbversion==None:
            cur.execute("insert into globals (global,value) values (%s,%s);", ("version_date", valor ))
        else:
            cur.execute("update globals set value=%s where global=%s;", (valor,"version_date" ))
        cur.close()        
        self.dbversion=valor
        self.mem.con.commit()
