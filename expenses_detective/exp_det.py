import sqlite3
import datetime
import time
import sys


class Database:

    def __init__(self):
        self.con=sqlite3.connect('exp_det_db.db')
        self.cur=self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY ,
                                                                    category TEXT NOT NULL,
                                                                    description TEXT,
                                                                    cost INT NOT NULL,
                                                                    entry_time_stamp TEXT,
                                                                    year TEXT,
                                                                    month TEXT,
                                                                    day TEXT)
                                                                    """)
        self.con.commit()

    def search_by_category (self,cat=""):
            self.cur.execute("SELECT id,category,description,cost,entry_time_stamp FROM expenses WHERE category=? ",(cat,))
            rows=self.cur.fetchall()
            return rows


    def search_by_year (self,year=""):
            self.cur.execute("SELECT id,category,description,cost,entry_time_stamp FROM expenses WHERE year=? ",(year,))
            rows=self.cur.fetchall()
            return rows

    def search_specific_month (self,year="",month=""):
            self.cur.execute("SELECT id,category,description,cost,entry_time_stamp FROM expenses WHERE month=? AND year=? ",(month,year))
            rows=self.cur.fetchall()
            return rows

    def search_specific_day (self,year="",month="",day=""):
            self.cur.execute("SELECT id,category,description,cost,entry_time_stamp FROM expenses WHERE day=? AND month=? AND year=? ",(day,month,year))
            rows=self.cur.fetchall()
            return rows

    def insert (self,cat,des,cost):
        date=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        self.cur.execute("INSERT INTO expenses VALUES (NULL,?,?,?,?,?,?,?)",(cat,des,cost,date,date[:4],date[5:7],date[8:10]))
        self.con.commit()

    def view(self):
        self.cur.execute("SELECT id,category,description,cost,entry_time_stamp FROM expenses")
        rows=self.cur.fetchall()
        return rows

    def delete (self,id):
        self.cur.execute("DELETE FROM expenses WHERE id=?",(id,))
        self.con.commit()

    def update_cost_des(self,id,des,cost):
        self.cur.execute("UPDATE expenses SET cost=?, description=?  WHERE id=?",(cost,des , id ))
        self.con.commit()

class Database_acc:


    def __init__(self):
        self.con=sqlite3.connect('acc_db.db')
        self.cur=self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY ,
                                                                    bank TEXT NOT NULL,
                                                                    account TEXT,
                                                                    amount INT NOT NULL,
                                                                    iid TEXT NOT NULL)

                                                                   """)
        self.con.commit()

    def get_id(self,bank,account,amount):
        self.cur.execute("SELECT id FROM accounts WHERE bank=? AND account=? AND amount=?",(bank,account,amount))
        rows=self.cur.fetchall()
        return rows

    def get_bank_by_iid(self,iid):
        self.cur.execute("SELECT bank FROM accounts WHERE iid=?",(iid,))
        rows=self.cur.fetchall()
        return rows

    def update_iid(self,id,iid):
        self.cur.execute("UPDATE SET iid=? WHERE id=?",(iid,id))
        self.con.commit()

    def insert (self,bank,account,amount):
        self.cur.execute("INSERT INTO accounts VALUES (NULL,?,?,?,?)",(bank,account,amount,1))
        self.con.commit()

    def update_cash(self,iid,amount):
        self.cur.execute("UPDATE accounts SET amount=? WHERE iid=?",(amount,iid))
        self.con.commit()

    def update_bank(self,id,bank):
        self.cur.execute("UPDATE accounts SET bank=? WHERE id=?",(bank,id ))
        self.con.commit()

    def update_amount(self,id,amount):
        self.cur.execute("UPDATE accounts SET amount=? WHERE id=?",(amount,id ))
        self.con.commit()

    def delete_acc(self,iid):
        self.cur.execute("DELETE FROM accounts WHERE iid=?",(iid,))
        self.con.commit()

    def view_acc(self):
        self.cur.execute("SELECT id,bank,account,amount FROM accounts")
        rows=self.cur.fetchall()
        return rows

    def get_net_worth(self):
        self.cur.execute("SELECT SUM(amount) FROM accounts")
        net_worth=self.cur.fetchall()
        return net_worth[0][0]

    def get_number_of_rows(self):
        self.cur.execute("SELECT COUNT(id) FROM accounts")
        total=self.cur.fetchall()
        return total[0][0]

    def get_cheq_amount(self):
        self.cur.execute("SELECT SUM(amount) FROM accounts GROUP BY id HAVING account=?",("Chequing",))
        cheq_amount=self.cur.fetchall()
        sum1=0
        for i in range(len(cheq_amount)):
            sum1+=int(cheq_amount[i][0])
        return sum1

    def get_savings_amount(self):
        self.cur.execute("SELECT SUM(amount) FROM accounts GROUP BY id HAVING account=?",("Savings",))
        savings_amount=self.cur.fetchall()
        sum2=0
        for i in range(len(savings_amount)):
            sum2+=int(savings_amount[i][0])
        return sum2

    def get_credit_amount(self):
        self.cur.execute("SELECT SUM(amount) FROM accounts GROUP BY id HAVING account=?",("Credit card",))
        credit_amount=self.cur.fetchall()
        sum3=0
        for i in range(len(credit_amount)):
            sum3+=int(credit_amount[i][0])
        return sum3

    def get_cash_amount(self):
        self.cur.execute("SELECT SUM(amount) FROM accounts GROUP BY id HAVING account=?",("Cash",))
        cash_amount=self.cur.fetchall()
        sum4=0
        for i in range(len(cash_amount)):
            sum4+=int(cash_amount[i][0])
        return sum4

    def get_account_by_iid(self,iid):
        self.cur.execute("SELECT account FROM accounts WHERE iid=?",(iid,))
        rows=self.cur.fetchall()
        return rows

    def transfer(self,accFrom,accTo,bankFrom,bankTo,amount,radio_var):
        try:
            self.cur.execute("SELECT amount FROM accounts WHERE account=? AND bank=?",(accFrom.capitalize(),bankFrom))
            amount_from=self.cur.fetchall()
            print(amount_from)
            self.cur.execute("SELECT amount FROM accounts WHERE account=? AND bank=?",(accTo.capitalize(),bankTo))
            amount_to=self.cur.fetchall()
            print(amount_to)
            self.cur.execute("UPDATE accounts SET amount=? WHERE account=? AND bank=?",(int(amount_to[0][0])+int(amount),accTo.capitalize(),bankTo))
            if int(amount_from[0][0])-int(amount)<0 and radio_var==2:
                return "Negative amount isn't allowed"
            else:
                self.cur.execute("UPDATE accounts SET amount=? WHERE account=? AND bank=?",(int(amount_from[0][0])-int(amount),accFrom.capitalize(),bankFrom))
            self.con.commit()
            return "Transfer Completed"

        except IndexError:
            if(sys.exc_info()[-1].tb_lineno)==172:
                return "{} account dosen't have bank {}".format(accTo,bankTo)
            if(sys.exc_info()[-1].tb_lineno)==173:
                return "{} account dosen't have bank {}".format(accFrom,bankFrom)
