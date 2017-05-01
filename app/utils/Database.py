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
        sql = 'INSERT INTO inventory_card (name, set_id, card_language, foil, super_types, types, sub_types, ' \
              'mana_cost, cmc, color, rarity, artist, rules_text, flavor_text, power, toughness, ' \
              'collector_number, multiverse_id, image, stock, price, color_identity, layout_type, ' \
              'ordered_card_names, is_focal_card, condition, super_types_text, types_text, sub_types_text, ' \
              'color_text) VALUES (%s,(SELECT id from inventory_set WHERE code = %s), %s, %s, %s, ' \
              '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.execute_sql(sql, args)
