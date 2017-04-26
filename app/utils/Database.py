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

    def execute_sql(self, sql, arguments):
        self.cur.execute(sql, arguments)

    def get_results(self):
        return self.cur.fetchall()

    def set_is_in_database(self, set_name):
        self.execute_sql("SELECT name FROM inventory_set WHERE name = %s", (set_name,))
        res = self.get_results()
        return res.__len__() > 0

    def insert_set(self, *args):
        set_name = args[0]
        if not self.set_is_in_database(set_name):
            sql = 'INSERT INTO inventory_set (name, code, release_date, cards_in_set) VALUES (%s, %s, %s, %s)'
            self.execute_sql(sql, args)
            self.update_database()

    def update_database(self):
        self.conn.commit()

    def insert_card(self, *args):
        card_name = args[0]
        set_code = args[1]
        language = args[2]
        foil = args[3]
        collector_number = args[16]
        set_id = self.get_set_id(set_code)
        if not self.does_card_exist(card_name, set_id, language, foil, collector_number):
            sql = 'INSERT INTO inventory_card (name, set_id, card_language, foil, super_types, types, sub_types, ' \
                  'mana_cost, cmc, color, rarity, artist, rules_text, flavor_text, power, toughness, ' \
                  'collector_number, multiverse_id, image, stock, price, color_identity) VALUES (%s, %s, %s, %s, %s, ' \
                  '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            lst = list(args)
            lst[1] = set_id
            args = tuple(lst)
            self.execute_sql(sql, args)
            self.update_database()

    def get_set_id(self, set_code):
        sql = 'SELECT id FROM inventory_set WHERE code = %s'
        self.execute_sql(sql, (set_code,))
        return self.get_results()[0][0]

    def does_card_exist(self, *args):
        sql = 'SELECT name from inventory_card WHERE name = %s AND set_id = %s AND card_language = %s AND foil = %s ' \
              'AND collector_number = %s'
        self.execute_sql(sql, args)
        result = self.get_results()
        return result.__len__() > 0
