import psycopg2
import hashlib
import uuid
import datetime
import os
db_ip =  os.environ.get('DB_IP')
db_port =  os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
db_password = os.environ.get('DB_PASSWORD')
db_user = os.environ.get('DB_USER')
def connect_db(db,user,host,password,port):
    try:
        conn = psycopg2.connect(database = db, 
                        user = user, 
                        host= host,
                        password = password,
                        port = port)
    except Exception as e:
        print (e)
        return None
    return (conn)
def check_user(user , password):
    conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
    if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT name, password FROM idm.users WHERE name = %s;", (user,))
     #cursor.execute('SELECT name, password FROM idm.users;')
     rows = cursor.fetchall()
     print(hashlib.md5(password.encode()).hexdigest())
     if (len(rows)  == 0):
        print('utilisateur nexiste pas')
        return (False)
     else:
        if (hashlib.md5(password.encode()).hexdigest() == rows[0][1]):
           print ("mot de passe correct")
           return (True)
        else: 
           print("mots de passe incorrect")
           return(False)
    else:
        return None
def get_user_ui(user_name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT uuid FROM idm.users WHERE name = %s;", (user_name,))
     rows = cursor.fetchall()
     if (len(rows) == 0):
        print('utilisateur nexiste pas')
        return (False)
     else :
        return(rows[0][0])
def get_group_ui(group_name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT uuid FROM idm.group WHERE name = %s;", (group_name,))
     rows = cursor.fetchall()
     if (len(rows) == 0):
        print('le groupe nexiste pas')
        return (False)
     else :
        return(rows[0][0])
def get_org_ui(org_name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT uuid FROM idm.organistations WHERE name = %s;", (org_name,))
     rows = cursor.fetchall()
     if (len(rows) == 0):
        print('lorganisation nexiste pas')
        return (False)
     else :
        return(rows[0][0])
def get_assigned_groups(user_ui):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn :
      cursor = conn.cursor()
      cursor.execute("SELECT 'group' FROM idm.USER_Group WHERE user = %s;",(user_ui,))
      rows = cursor.fetchall()
      if (len(rows) > 0):
        print('utilisateur nexiste pas')
        return (False)
      else:
        print(rows)
def check_user_existance(name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT name FROM idm.users WHERE name = %s;", (name,))
     rows = cursor.fetchall()
     if (len(rows) > 0):
        print('utilisateur existe')
        return (False)
     else :
        return(True)
def create_org(name):
    conn = connect_db(db_name, db_name, db_ip, db_password, db_port)
    if not conn:
        print("Error: Connection to database failed.")
        return None

    if (get_org_ui(name) != False):
        print(f"Organization {name} already exists.")
        return False

    try:
        cursor = conn.cursor()
        uuid_generated = str(uuid.uuid4())
        datenow = datetime.datetime.now()

        insert_query = """
            INSERT INTO idm.organistations (
                uuid,name
            ) VALUES (%s, %s);
        """

        values = (
            uuid_generated,
            name   
        )
        try :
         cursor.execute(insert_query, values)
         conn.commit()
         print(f"Organization {name} is added")
        except Exception as e:
         print(f"Error adding organization: {e}")
        return True

    except Exception as e:
        print(f"Error inserting organization: {e}")
        return None
def create_groupe(name, org):
    conn = connect_db(db_name, db_name, db_ip, db_password, db_port)
    if not conn:
        print("Error: Connection to database failed.")
        return None

    if (get_group_ui(name) != False):
        print(f"Groupe {name} already exists.")
        return False

    try:
        cursor = conn.cursor()
        uuid_generated = str(uuid.uuid4())
        datenow = datetime.datetime.now()

        insert_query = """
            INSERT INTO idm.group (uuid, created_date, last_modified, display_name, name, org) VALUES (%s, %s, %s, %s, %s, %s);
        """

        values = (
            uuid_generated,
            datenow,
            datenow,        
            name,   
            name,   
            org,
        )
        try :
         cursor.execute(insert_query, values)
         conn.commit()
         print(f"groupe {name} is added")
        except Exception as e:
         print(f"Error adding group: {e}")
        return True

    except Exception as e:
        print(f"Error inserting user: {e}")
        return None
def delete_groupe(name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if not conn:
        print("Error: Connection to database failed.")
        return None
   cursor = conn.cursor()
   delete_query =  """DELETE FROM idm.group WHERE name = %s;"""
   values = (name,)
   try :
      cursor.execute(delete_query, values)
      conn.commit()
   except Exception as e:
        print(f"Error deleating group: {e}")
        cursor.close()
        conn.close()
        return (False)
   print(f"group {name} is deleted")
   return True
def create_user(name, password, email, org):
    conn = connect_db(db_name, db_name, db_ip, db_password, db_port)
    if not conn:
        print("Error: Connection to database failed.")
        return False

    if (check_user_existance(name)== False):
        print(f"User {name} already exists.")      
        return False
    if (name == ''):
       print("name is null")
       return False
    if (password == ''):
       print("password is null")
       return False
    try:
        cursor = conn.cursor()
        uuid_generated = str(uuid.uuid4())
        datenow = datetime.datetime.now()
        passwd = hashlib.md5(password.encode()).hexdigest()

        insert_query = """
            INSERT INTO idm.users (
                uuid, created_date, is_disabled, locked, 
                "last_Modified", email, display_name, name, org, password
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        values = (
            uuid_generated,
            datenow,
            True,
            False,
            datenow,
            email,
            name,   
            name,   
            org,
            passwd
        )
        try :
         cursor.execute(insert_query, values)
         conn.commit()
         print(f"user {name} is added")
        except Exception as e:
         print(f"Error Creating user: {e}")
         return False
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error inserting user: {e}")
        cursor.close()
        conn.close()
        return False
#check_user_existance("admin")
#create_user("admin", "admin", "admin.admin@gamil.com", "a6621849-9434-46a6-8fbb-498a56ef40d8")
def delete_user(name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if not conn:
        print("Error: Connection to database failed.")
        return None
   cursor = conn.cursor()
   delete_query =  """DELETE FROM idm.users WHERE name = %s;"""
   values = (name,)
   try :
      cursor.execute(delete_query, values)
      conn.commit()
   except Exception as e:
        print(f"Error deleating user: {e}")
        cursor.close()
        conn.close()
        return (False)
   print(f"user {name} is deleted")
   cursor.close()
   conn.close()
   return True
def get_user_org(name):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT org FROM idm.users WHERE name = %s;", (name,))
     rows = cursor.fetchall()
     if (len(rows) == 0):
        print('utilisateur nexiste pas')
        cursor.close()
        conn.close()
        return (False)
     else :
        cursor.close()
        conn.close()
        return(rows[0][0])
def get_org_name_from_ui(org_ui):
   conn = connect_db (db_name,db_name,db_ip,db_password,db_port)
   if conn:
     cursor = conn.cursor()
     cursor.execute("SELECT name FROM idm.organistations WHERE uuid = %s;", (org_ui,))
     rows = cursor.fetchall()
     if (len(rows) == 0):
        print('lorganisation nexiste pas')
        cursor.close()
        conn.close()
        return (False)
     else :
        cursor.close()
        conn.close()
        return(rows[0][0])
def get_prefix(user_name):
   org = get_user_org(user_name)
   if (org == True) :
      return False
   prefix = get_org_name_from_ui(org)
   if (prefix == False):
      return False
   else :
      return (prefix) 
