from concurrent.futures import Executor
import logging
import mysql.connector

logging.basicConfig(level=logging.INFO)



class DB():
    def __init__(self) -> None:
        
        db_user = 'root'
        db_password = 'root'
        db_host = 'localhost'
        db_name = 'mydb'


        self.db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
        )

        self.cursor = self.db.cursor()
    def setUser(self, id, client_fio, client_phone, client_email):
        self.cursor.execute('INSERT INTO client (idclient,client_fio, client_phone, client_email) VALUES (%s,%s, %s, %s)', (id, client_fio, client_phone, client_email) )
        
        self.db.commit()
    def getEvents(self):
        self.cursor.execute("SELECT * FROM event")
        data = self.cursor.fetchall()
        return data
    def getProv_Serv(self):
        self.cursor.execute("SELECT * FROM `prov_serv`")
        data = self.cursor.fetchall()
        return data
    def setServ_Order(self, idprov_serv,idclient):
        self.cursor.execute('INSERT INTO `serv_order` (idprov_serv, idorder) VALUES (%s,(SELECT idorder FROM `order` WHERE idclient = %s));', (idprov_serv,idclient) )
        
        self.db.commit()
    def getPlace(self,number_people:str = 1):
        self.cursor.execute("SELECT * FROM `place` WHERE persons >= %s",(number_people,))
        data = self.cursor.fetchall()
        return data
    def setOrder(self, idclient, idevent,idplace,number_people,date,idorganizer):
        #INSERT INTO `order` (idclient, idevent,idplace,number_people,date,idorganizer) VALUES ("1194404057","1","1",3,'2011-11-23',"2");
        self.cursor.execute('INSERT INTO `order` (idclient, idevent,idplace ,number_people,date,idorganizer) VALUES (%s,%s,%s,%s,%s,%s);', (idclient, idevent,idplace,number_people,date,idorganizer,) )
        
        self.db.commit()
    def IsUserExist(self,userid):
        self.cursor.execute('SELECT * FROM `client` WHERE idclient = %s;', (userid,) )
        if self.cursor.fetchall():
            return True
        else:
            return False
    def getALL(self,clientid):
        self.cursor.execute('SELECT client_fio,client_phone,client_email,`order`.idorder,`event`.event_name,`place`.place_name,`place`.address,`order`.number_people,`order`.date,`prov_serv`.serv_name \
                                FROM `client`  \
                                INNER JOIN `order` ON  `client`.idclient=`order`.idclient \
                                INNER JOIN `place` ON `order`.idplace = `place`.idplace \
                                INNER JOIN `serv_order` ON `order`.idorder = `serv_order`.idorder \
                                INNER JOIN `prov_serv` ON `serv_order`.idprov_serv = `prov_serv`.idprov_serv \
                                INNER JOIN `event` ON `order`.idevent = `event`.idevent \
                                WHERE `client`.idclient = %s',
                             (clientid,) )
        data = self.cursor.fetchall()
        return data
       
