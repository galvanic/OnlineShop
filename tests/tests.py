
import sqlite3
from models import DB_DIR, createTables
from helper import calculateMoneyOwed


def test_money_owed():

	# Dump data

	group_id = createTables()
	print("Group %d created" % group_id)


	# Dumping data for table 'person'

	conn = sqlite3.connect('%s/person.db' % DB_DIR)
	c = conn.cursor()
	c.execute("INSERT INTO person (name, group_id) VALUES ('Alice', ?)", (group_id, ))
	print("Alice's id is %d" % c.lastrowid)
	c.execute("INSERT INTO person (name, group_id) VALUES ('Bob', ?)", (group_id, ))
	print("Bob's id is %d" % c.lastrowid)
	c.execute("INSERT INTO person (name, group_id) VALUES ('Charlie', ?)", (group_id, ))
	print("Charlie's id is %d" % c.lastrowid)
	conn.commit()
	c.close()


	# Table structure for table 'shop'

	conn = sqlite3.connect('%s/shop.db' % DB_DIR)
	c = conn.cursor()
	c.execute("INSERT INTO shop (delivery_date, group_id) VALUES (140329, ?)", (group_id, ))
	shop_id = c.lastrowid
	conn.commit()
	c.close()


	# Table structure for table 'item'

	conn = sqlite3.connect('%s/item.db' % DB_DIR)
	c = conn.cursor()
	c.execute("INSERT INTO item (name, price) VALUES ('Bananas', '200')")
	print("Bananas' id is %d" % c.lastrowid)
	c.execute("INSERT INTO item (name, price) VALUES ('Chocolate', '300')")
	print("Chocolate's id is %d" % c.lastrowid)
	c.execute("INSERT INTO item (name, price) VALUES ('Toilet Rolls', '600')")
	print("Toilet Rolls's id is %d" % c.lastrowid)
	conn.commit()
	c.close()


	# Table structure for table 'item_to_shop'

	conn = sqlite3.connect('%s/item_to_shop.db' % DB_DIR)
	c = conn.cursor()
	c.execute("INSERT INTO item_to_shop (item_id, shop_id) VALUES (1, ?)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop (item_id, shop_id) VALUES (2, ?)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop (item_id, shop_id) VALUES (3, ?)", (shop_id, ))
	conn.commit()
	c.close()


	# Table structure for table 'item_to_shop_to_person'

	conn = sqlite3.connect('%s/item_to_shop_to_person.db' % DB_DIR)
	c = conn.cursor()
	c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (1, ?, 1)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (1, ?, 2)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (2, ?, 1)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (3, ?, 1)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (3, ?, 2)", (shop_id, ))
	c.execute("INSERT INTO item_to_shop_to_person (item_id, shop_id, person_id) VALUES (3, ?, 3)", (shop_id, ))
	conn.commit()
	c.close()

	# Alice and Bob share the Bananas. The Chocolate belongs to Alice. Everyone contributes to the toilet paper.
	# Alice paid £6.00 (£2.00/2 + £3.00 + £6.00/3)
	# Bob paid £3.00 (£2.00/2 + £6.00/3)
	# Charlie paid £2.00 (£6.00/3)

	flatmates = calculateMoneyOwed(shop_id)
	print(flatmates)

	if flatmates["Alice"] == 600:
		print("Alice passed")
	else:
		print("Alice NOT passed")

	if flatmates["Bob"] == 300:
		print("Bob passed")
	else:
		print("Bob NOT passed")

	if flatmates["Charlie"] == 200:
		print("Charlie passed")
	else:
		print("Charlie NOT passed")

	return


def main():

	test_money_owed()

	return


if __name__ == '__main__':
	main()

