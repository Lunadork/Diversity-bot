import server

#checks if user exists in database and returns false if they do (not new), true if they don't (is new)
def check_if_new(username):
    with server.con:
        with server.con.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s;",[username] )
            rows = cursor.fetchall()
            
            if rows:
                return False
            else:
                return True

#checks if user has a task and returns the task if they do, false if they don't.
def check_if_has_task(username):
    with server.con:
        with server.con.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s;",[username])
            rows = cursor.fetchall()
            print(rows)
            if rows[0][5] == True:
                return rows[0][6]
            else:
                return False

def check_primary_concern(username):
        with server.con:
            with server.con.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s;",[username])
                rows = cursor.fetchall()
                if rows[0][3] != "None":
                    return rows[0][3]
                else:
                    return False

def get_preferred_name(username):
        with server.con:
            with server.con.cursor() as cursor:
                cursor.execute("SELECT preferred_name FROM users WHERE username = %s;",[username])

                rows = cursor.fetchall()
                return rows[0][0]
                
def set_task_done(username):
        with server.con:
            with server.con.cursor() as cursor:
                cursor.execute("UPDATE users SET has_task = false WHERE username = %s",[username])
                cursor.execute("UPDATE users SET task = %s WHERE username = %s",["Done",username])

def stop_task(username):  
        with server.con:
            with server.con.cursor() as cursor:
                cursor.execute("UPDATE users SET has_task = false WHERE username = %s",[username])
                cursor.execute("UPDATE users SET task = %s WHERE username = %s",["Stopped",username])

def set_cbt_task(username):
    with server.con:
        with server.con.cursor() as cursor:
            cursor.execute("UPDATE users SET has_task = true WHERE username = %s",[username])
            cursor.execute("UPDATE users SET task = %s WHERE username = %s",["CBT Excecises",username])

