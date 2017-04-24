import psycopg2
import yaml


class Database:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            creds = yaml.load(f)
            dbname = creds['database_name']
            host = creds['host']
            port = creds['port']
            user = creds['database_user']
            password = creds['password']
            connection_string = "dbname='" + dbname + "' user='" + user + "' host='" + host + "' port='" + str(port) \
                                + "' password='" + password + "'"
            self.conn = psycopg2.connect(connection_string)
            self.cur = self.conn.cursor()

    def execute_sql(self, sql, *args):
        self.cur.execute(sql, args)

    def get_results(self):
        return self.cur.fetchall()

    def insert_set(self, *args):
        set_name = args[0]
        self.execute_sql("SELECT name FROM inventory_set WHERE name = %s", set_name)
        res = self.get_results()
        if res.__len__() == 0:
            sql = 'INSERT INTO inventory_set (name, code, release_date, cards_in_set) VALUES (%s, %s, %s, %s)'
            # self.execute_sql(sql, args)
            self.cur.execute(sql, args)
            self.update_database()

    def update_database(self):
        self.conn.commit()

