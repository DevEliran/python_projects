import sqlite3
import datetime
import socket


class Urls(object):

    def __init__(self):
        self.con=sqlite3.connect('urls.db')
        self.cur=self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY ,
                                                                url TEXT NOT NULL,
                                                                prevS INT NOT NULL,
                                                                curS INT NOT NULL,
                                                                time_stamp TEXT)
                                                                """)
        self.con.commit()
#prevS stands for previous status , curS stands for current status .
# 1 represents connection , 0 represents disconnection.

    def first_conn_check(self,url):
        try:
            print(f"Evaluating connection to {url}.... ")
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPV4 , TCP
            s.settimeout(2)
            s.connect((url,80))
            s.close()
            print(f'{url} is up\n')
            return 1
            sleep(1)
        except Exception:
            print(f'{url} is down\n')
            return 0
            sleep(1)
            sys.exit(0)

    def insert_url(self,url):
        time_stamp=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        init_conn=self.first_conn_check(url)
        self.cur.execute("INSERT INTO urls VALUES (NULL,?,?,?,?)",(url,0,init_conn,time_stamp))
        self.con.commit()


    def view_table(self):
        self.cur.execute("SELECT id,url,prevS,curS,time_stamp FROM urls")
        table=self.cur.fetchall()
        return table

    def view_urls(self):
        self.cur.execute("SELECT url FROM urls")
        urls=self.cur.fetchall()
        return urls


    def delete(self,url):
        self.cur.execute("DELETE FROM urls WHERE url=?",(url,))
        self.con.commit()

    def status_changed(self,url):
        self.cur.execute("SELECT prevS,curS FROM urls WHERE url=?",(url,))
        status=self.cur.fetchall()
        print(status)
        if status[0][0]==status[0][1]:
            return False
        return True

    def count_rows(self):
        self.cur.execute("SELECT COUNT(*) FROM urls")
        count=self.cur.fetchall()
        #print(count)
        return count

    def update_status(self,url):
        self.cur.execute("SELECT prevS FROM urls WHERE url=?",(url,))
        prev=self.cur.fetchall()[0][0]
        self.cur.execute("SELECT curS FROM urls WHERE url=?",(url,))
        cur=self.cur.fetchall()[0][0]

        self.cur.execute("UPDATE urls SET prevS=? WHERE url=?",(cur,url))
        self.con.commit()
