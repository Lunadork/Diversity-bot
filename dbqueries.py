import server
import asyncio

#checks if user exists in database and returns false if they do (not new), true if they don't (is new)
async def check_if_new(username):
    with server.con:
        with server.con.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s;",[username] )
            rows = cursor.fetchall()
            
            if rows:
                return False
            else:
                return True

#checks if user has a task and returns the task if they do, false if they don't.
async def check_if_has_task(username):
    with server.con:
        with server.con.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s;",[username])
            rows = cursor.fetchall()
            print(rows)
            if rows[0][5] == True:
                return rows[0][6]
            else:
                return False

async def check_primary_concern(username):
        with server.con:
            with server.con.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE username = %s;",[username])
                rows = cursor.fetchall()
                if rows[0][3] != "None":
                    return rows[0][3]
                else:
                    return False

async def get_preferred_name(username):
        with server.con:
            with server.con.cursor() as cursor:
                cursor.execute("SELECT preferred_name FROM users WHERE username = %s;",[username])

                rows = cursor.fetchall()
                print("rows")
                print(rows[0][0])
                print("endrow")
                return rows[0][0]
                
async def set_task_done(username):
        with server.con:
            with server.con.cursor() as cursor:
                try:
                    cursor.execute("UPDATE users SET has_task = False WHERE username = %s;",[username])
                    cursor.execute("UPDATE users SET task = %s WHERE username = %s;",["Done",username])
                except:
                    print("Failed to set user "+username+" task to done")


async def stop_task(username):  
        with server.con:
            with server.con.cursor() as cursor:
                try:
                    cursor.execute("UPDATE users SET has_task = False WHERE username = %s;",[username])
                    cursor.execute("UPDATE users SET task = %s WHERE username = %s;",["Stopped",username])
                except:
                    print("Failed to set user "+username+" task to stopped and false")

async def set_cbt_task(username):
    with server.con:
        with server.con.cursor() as cursor:
            cursor.execute("""UPDATE users SET has_task = 'True' WHERE username = 'anon2';""")
            cursor.execute("""UPDATE users SET task = %s WHERE username = %s""",['CBT Excercises',username+""])
            print("updooted " +username + "with cbt task") 




                

async def add_user(username,prefname):
    with server.con:
        with server.con.cursor() as cursor:
            
            cursor.execute("""INSERT INTO users (username, preferred_name, has_task, task) 
                                         VALUES (%s, %s, False, 'no');""",[username+"", prefname+""])

            cursor.execute("SELECT * FROM users")
            print("users:")
            rows = cursor.fetchall()
            for r in rows:
                print(r)
