import sqlite3,time,threading
import Crawler
def task():
    while True:
        db_path = '/root/mysite/info.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('select openid,account,passwd from user where is_valid="True"')
        value = cursor.fetchall()
        for each in value:
            Crawler.invoke(each[0], each[1], each[2])
            time.sleep(10)
        with open('/root/mysite/task_log.txt','a') as f:
            f.write(str(time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time())))+':finish\r\n')
        time.sleep(2*60 * 60)
t=threading.Thread(target=task,daemon=True)
t.start()
t.join()