import socket
import sys
from time import sleep
from url_db import Urls
import argparse
import winsound

urls_db=Urls()

#urls=['www.facebook.com','www.google.com','www.twitter.com','www.instagram.com','www.github.com']

def check(url):

    ndex=url.find('w.')
    short_url=url[ndex+2:].capitalize()
    while True:
        try:
            print(f"Evaluating connection to {url}.... ")
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # IPV4 , TCP
            s.settimeout(2)
            s.connect((url,80))
            s.close()
            print(f'{short_url} is up\n')
            return 1
            sleep(1)
        except Exception:
            print(f'{short_url} is down\n')
            return 0
            sleep(1)
            sys.exit(0)


def parse():
    parser=argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-e","--execute",help="Executes the script",action="store_true" )
    group.add_argument("-v","--view_url",help="View all the urls store in the database",action="store_true")
    group.add_argument("-a","--add_url",help="Add a url formatted as  : www.url.domain",action="store")
    parser.add_argument("-i","--interval",help="Choose the interval of the program execution",action="store")
    group.add_argument("-d","--delete",help="Delete a url from the database ; specify the url formatted as : www.url.domain",action="store")

    args=parser.parse_args()

    command=args.execute

    if args.execute:
        get_urls=urls_db.view_urls()
        while True:
            for i in range(int(urls_db.count_rows()[0][0])):
                current_status=check(get_urls[i][0])
                if current_status==1:
                    urls_db.cur.execute("UPDATE urls SET curS=? WHERE url=?",(1,get_urls[i][0]))
                    urls_db.con.commit()
                    if urls_db.status_changed(get_urls[i][0]):
                        notify()
                elif current_status==0:
                    urls_db.cur.execute("UPDATE urls SET curS=? WHERE url=?",(0,get_urls[i][0]))
                    urls_db.con.commit()
                    if urls_db.status_changed(get_urls[i][0]):
                        notify()
                urls_db.update_status(get_urls[i][0])            
            sleep(int(args.interval))

    elif args.view_url:
        get_urls=urls_db.view_urls()
        #print(get_urls)

    elif args.add_url:
        urls_db.insert_url(args.add_url)

    elif args.delete:
        urls_db.delete(args.delete)

def notify():
    duration=1000 #milliseconds
    freq=440 #hz
    winsound.Beep(duration,freq)

if __name__=='__main__':
    parse()


#for url in urls:
    #urls_db.insert_url(url)

#urlview=urls_db.view_table()
#get_urls=urls_db.view_urls()
#print(get_urls)
#for i in range (5):
#    check(get_urls[i][0])
#for url in urlview
