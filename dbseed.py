import server

def seed():
    username = "Test"
    have_spoken = False
    primary_concern = "Depression"
    has_task = False
    task = "None"

    new_user = server.User(username,have_spoken,primary_concern,has_task,task)

    server.db.session.add(new_user)
    server.db.session.commit()

    username = "Test2"
    have_spoken = True
    primary_concern = "Anxiety"
    has_task = True
    task = "CBT exercises"

    new_user = server.User(username,have_spoken,primary_concern,has_task,task)

    server.db.session.add(new_user)
    server.db.session.commit()


    #### CONDITIONS ####

    name = "Depression"
    resource = "https://www.nhsinform.scot/illnesses-and-conditions/mental-health/depression"
    task = "CBT Exercises"

    new_condition = server.Condition(name,resource,task)

    server.db.session.add(new_condition)
    server.db.session.commit()


    name = "Anxiety"
    resource = "https://www.nhsinform.scot/illnesses-and-conditions/mental-health/anxiety"
    task = "CBT Exercises"

    new_condition = server.Condition(name,resource,task)

    server.db.session.add(new_condition)
    server.db.session.commit()



    name = "Social Isolation"
    resource = "https://www.nhsinform.scot/illnesses-and-conditions/mental-health/mental-health-self-help-guides/social-anxiety-self-help-guide"
    task = "CBT Exercises"

    new_condition = server.Condition(name,resource,task)

    server.db.session.add(new_condition)
    server.db.session.commit()