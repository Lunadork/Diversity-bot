from server import con

def setup():
    with con:
        with con.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS users;")
            cursor.execute("DROP TABLE IF EXISTS conditions;")

            cursor.execute("""CREATE TABLE IF NOT EXISTS users( id serial PRIMARY KEY, 
                                                        username VARCHAR(200) NOT NULL UNIQUE,
                                                        preferred_name VARCHAR(200),
                                                        primary_concern VARCHAR(200),
                                                        secondary_concerns VARCHAR(1000),
                                                        has_task boolean,
                                                        task VARCHAR(1000),
                                                        flag_words VARCHAR(1000),
                                                        sought_help boolean);""")
                                        
            cursor.execute("""CREATE TABLE IF NOT EXISTS conditions ( id serial PRIMARY KEY, 
                                                        name VARCHAR(200) NOT NULL UNIQUE,
                                                        resource VARCHAR(1000),
                                                        task VARCHAR(1000));""")
            
            res = cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
            print("tables:")
            rows = cursor.fetchall()
            for r in rows:
                print(r)

            res = cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            print("dbs")
            rows = cursor.fetchall()
            for r in rows:
                print(r)

            res = cursor.execute("""INSERT INTO users (username,preferred_name,has_task,task) VALUES('Test','Test_user','False','none'),
                                                                                                    ('Zeia','Zeia-PrefName','True','CBT Excercises'),
                                                                                                    ('Test2','Test2_prefname','False','none');""")

            res = cursor.execute("""INSERT INTO conditions (name,resource,task) VALUES ('depression','https://www.nhsinform.scot/illnesses-and-conditions/mental-health/depression','CBT Exercises'),
                                                                                       ('Anxiety','https://www.nhsinform.scot/illnesses-and-conditions/mental-health/anxiety','CBT Exercises'),
                                                                                       ('Social Isolation','https://www.nhsinform.scot/illnesses-and-conditions/mental-health/mental-health-self-help-guides/social-anxiety-self-help-guide','CBT, chatroom');""")

            
            
            
            
            
def debug():
    with con:
        with con.cursor() as cursor:            
            cursor.execute("SELECT * FROM users")
            print("users:")
            rows = cursor.fetchall()
            for r in rows:
                print(r)

            # cursor.execute("SELECT * FROM conditions")
            # print("conditions:")
            # rows = cursor.fetchall()
            # for r in rows:
            #     print(r)





