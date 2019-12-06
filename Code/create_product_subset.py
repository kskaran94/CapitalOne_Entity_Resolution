import csv
import os
from random import sample

path = '../Data/Amazon-GoogleProducts/'
AMAZON_DATASET = os.path.join(path, "Amazon.csv")
GOOGLE_DATASET = os.path.join(path, "GoogleProducts.csv")
MATCHED_DATASET = os.path.join(path, "Amzon_GoogleProducts_perfectMapping.csv")

MATCH_COUNT = 20
NON_MATCH_COUNT = 10

amazon_products = {}
google_products = {}

matched_products = set()

with open(AMAZON_DATASET, encoding="latin") as f:
	amazon_file = csv.reader(f)
	next(amazon_file) #skip header
	for row in amazon_file:
		amazon_products[row[0]] = row[1:]

with open(GOOGLE_DATASET, encoding="latin") as f:
	google_file = csv.reader(f)
	next(google_file) #skip header
	for row in google_file:
		google_products[row[0]] = row[1:]

with open(MATCHED_DATASET, encoding="latin") as f:
	match_file = csv.reader(f)
	next(match_file)#skip header
	for row in match_file:
		matched_products.add((row[0], row[1]))

print("Initial length:", len(amazon_products), len(google_products))

amazon_ids = set(amazon_products.keys())
google_ids = set(google_products.keys())

matched_id_to_keep = []
all_matches = []
#create the matching ground truth for the subset
for am_id, g_id in matched_products:
	all_matches.append((am_id, g_id))


print("Total of matching: ", len(all_matches))

matched_id_to_keep = sample(all_matches, MATCH_COUNT)
print("Subset of matching: ", len(matched_id_to_keep))

amazon_id_used, google_id_used = set(), set()

#create new csv
with open('matched_products_subset.csv', mode='w') as matched_file:
    matched_writer = csv.writer(matched_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    matched_writer.writerow(["Amazon_ID", "Google_ID"])
    for am_id, g_id in matched_id_to_keep:
    	matched_writer.writerow([am_id, g_id])
    	amazon_id_used.add(am_id)
    	google_id_used.add(g_id)


with open('products_subset.csv', mode='w') as product_file:
	product_writer = csv.writer(product_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	#add header for csv file
	product_writer.writerow(["ID", "title", "description", "manufacturer", "price"])
	
	amazon_id_to_keep = sample(amazon_ids - amazon_id_used, NON_MATCH_COUNT)
	google_id_to_keep = sample(google_ids - google_id_used, NON_MATCH_COUNT)

	print("IDs to keep: ", len(amazon_id_to_keep), len(google_id_to_keep))

	for am_id in amazon_id_to_keep:
		row = [am_id] + amazon_products[am_id]
		product_writer.writerow(row)

	for g_id in google_id_to_keep:
		row = [g_id] + google_products[g_id]
		product_writer.writerow(row)

    



