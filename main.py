import mysql.connector as con
import func
import json
import time

mydb = con.connect(host='localhost',
                user='khaihoan',
                password='Kh04082002',
                database='userinfo')
cursor=mydb.cursor()
def run():
    cursor.execute("select * from userinfo")
    records = cursor.fetchall()
    for tuple in records:
        func.KEY=tuple[2]
        if tuple[3]==None:
            info=func.call('core_webservice_get_site_info')
            idlist=func.courseRetrieve(info['userid'])
            cursor.execute("update userinfo set courses='%s' where id=%d"%(json.dumps(idlist),tuple[0]))
            mydb.commit()
        else:
            idlist=json.loads(tuple[3])
        msg=''
        for courseId in idlist:
            update=func.call('core_course_get_updates_since',courseid=courseId,since=int(time.time())-600)
            if (update['instances']!=[]):
                msg=msg+idlist[courseId]+':\n'
                for module in update['instances']:
                    content=func.call('core_course_get_course_module',cmid=module['id'])
                    msg=msg+content['cm']['name']+'\n'
                msg+='\n'
        if (msg!=''):
            func.send_email(msg,tuple[1])
        else:
            print("No message!")
while (True):
    run()
    time.sleep(500)

