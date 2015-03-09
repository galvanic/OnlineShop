import sqlite3

DB_DIR = "databases"


def createTables():

	# Table structure for table 'user_group'

	db = sqlite3.connect('%s/user_group.db' % DB_DIR)
	db.execute("DROP TABLE IF EXISTS 'user_group'")
	db.execute("CREATE TABLE user_group (id INTEGER PRIMARY KEY, address CHAR(100) NOT NULL)")
	# Dumping data for table 'user_group'
	c = db.cursor()
	c.execute("INSERT INTO user_group (address) VALUES ('Latymer Court')")
	group_id = c.lastrowid
	db.commit()


	# Table structure for table 'person'

	db = sqlite3.connect('%s/person.db' % DB_DIR)
	db.execute("DROP TABLE IF EXISTS 'person'")
	# db.execute("CREATE TABLE person (id INTEGER PRIMARY KEY, first_name CHAR(100) NOT NULL, surname CHAR(100) NOT NULL, email CHAR(100) NOT NULL, password CHAR(100) NOT NULL, group_id INTEGER NOT NULL)")
	db.execute("CREATE TABLE person (id INTEGER PRIMARY KEY, name CHAR(100) NOT NULL, group_id INTEGER NOT NULL)")
	db.commit()


	# Table structure for table 'shop'

	db = sqlite3.connect('%s/shop.db' % DB_DIR)
	db.execute("DROP TABLE IF EXISTS 'shop'")
	db.execute("CREATE TABLE shop (id INTEGER PRIMARY KEY, delivery_date INTEGER NOT NULL, group_id INTEGER NOT NULL)")
	db.commit()


	# Table structure for table 'item'

	db = sqlite3.connect('%s/item.db' % DB_DIR)
	db.execute("DROP TABLE IF EXISTS 'item'")
	db.execute("CREATE TABLE item (id INTEGER PRIMARY KEY, name CHAR(100) NOT NULL, price INTEGER NOT NULL)")
	db.commit()


	# Table structure for table 'item_to_shop'

	db = sqlite3.connect('%s/item_to_shop.db' % DB_DIR)
	db.execute("DROP TABLE IF EXISTS 'item_to_shop'")
	db.execute("CREATE TABLE item_to_shop (id INTEGER PRIMARY KEY, item_id INTEGER NOT NULL, shop_id INTEGER NOT NULL)")
	db.commit()


	# Table structure for table 'item_to_shop_to_person'

	db = sqlite3.connect('%s/item_to_shop_to_person.db' % DB_DIR)
	db.execute("DROP TABLE IF EXISTS 'item_to_shop_to_person'")
	db.execute("CREATE TABLE item_to_shop_to_person (id INTEGER PRIMARY KEY, item_id INTEGER NOT NULL, shop_id INTEGER NOT NULL, person_id INTEGER NOT NULL)")
	db.commit()

	return group_id


if __name__ == '__main__':
	createTables()
