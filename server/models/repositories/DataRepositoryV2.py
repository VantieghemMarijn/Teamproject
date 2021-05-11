from .Database import Database

# ---- Repository to query the client database

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    #########  Treinen  #########
    @staticmethod
    def read_active_clients():
        sql=f"SELECT * FROM activeclients"
        data=Database.get_rows(sql)
        return data

    @staticmethod
    def read_clients():
        sql=f"SELECT * FROM clientlist"
        data=Database.get_rows(sql)
        return data

    @staticmethod
    def read_client(name):#password control
        sql="SELECT clientnick from clientlist WHERE clientname = %s"
        params=[name]
        data=Database.get_one_row(sql,params)
        return data 
    @staticmethod
    def remove_active_client(name):
        sql="DELETE from activeclients WHERE clientname =%s"
        params=[name]
        return Database.execute_sql(sql, params)
    @staticmethod
    def add_active_client(clientname):
        sql="INSERT INTO activeclients(clientname) VALUES(%s)"
        params=[clientname]
        data = Database.execute_sql(sql,params)
        return data
    @staticmethod
    def create_client(clientname,nick,email):
        sql="INSERT INTO clientlist(clientname,clientnick,clientemail) VALUES(%s,%s,%s)"
        params=[clientname,nick,email]
        data = Database.execute_sql(sql,params)
        return data

    @staticmethod
    def read_querys_per_client(name):
        sql="SELECT * from querylog WHERE username = %s"
        params=[name]
        data=Database.get_rows(sql,params)
        return data 

    @staticmethod
    def get_querys():
        sql=f"select queryname, count(queryname) from querylog group by queryname"
        data=Database.get_rows(sql)
        return data
    
    @staticmethod
    def add_query(username,query, queryparam):
        sql="insert into querylog(username,queryname,queryparam) values(%s,%s,%s)"
        params=[username,query, queryparam]
        data = Database.execute_sql(sql,params)
        return data
