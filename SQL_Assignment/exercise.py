from os import confstr_names
import sqlite3

conn = sqlite3.connect('sale.sqlite')
c = conn.cursor()

#How many tomatoes were sold during Jan 1st, 2016?

c.execute('''
SELECT date, SUM(units_sold) AS 'Tomatoes sold'
FROM Sales
WHERE sales.date = '2016-01-01' AND sales.product_id = (
    SELECT products.id
    FROM products
    WHERE products.name = 'Tomato'
    )
''')
tomatoes_1stjan = c.fetchall()
print('How many tomatoes were sold during Jan 1st, 2016?\n' + str(tomatoes_1stjan[0][0]))



#Display the total paid amount for each product, display the product name.

c.execute('''
SELECT products.name AS 'Name', SUM(sales.paid_amount) AS  'Total paid amount for each product'
FROM Sales, Products
WHERE sales.product_id = products.id
GROUP BY product_id
''')
totals = c.fetchall()
print('\nTotal paid amount for each product and the product name:')
print(totals)



#How many customers buy more than two different products on every visit (i.e. day)?

c.execute('''
SELECT DISTINCT COUNT(product_id) count, customer_id, date
    FROM Sales
    GROUP BY date, customer_id
Having count > 2
''')
more_2 = c.fetchall()
print('\nThe amount of customers that buy more than two different products on every visit(day):')
print(more_2)



# Assuming a customer does not return the same day to buy the same product twice.
# How would you identify if the table contains duplicates?

c.execute('''
SELECT COUNT(1) ct
FROM sales
GROUP BY customer_id, product_id, date
HAVING ct > 1
''')
dupl = c.fetchall()
print('\nAmount of duplicates:')
print(dupl)



# Display the 2nd most paid product every day.
c.execute('''
SELECT product_id, MAX (paid_amount), date
FROM sales a
WHERE product_id NOT IN (SELECT Max (paid_amount)
                          FROM sales b
Where a.product_id = b.product_id
And a.date = b.date
Group by date)

''')
2ndpaid = c.fetchall()
print('\nAmount of duplicates:')
print(2ndpaid)
