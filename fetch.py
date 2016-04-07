import csv
import urllib2
import json
import re
import os

file_name = 'data.csv'

try:
    os.remove(file_name)
except:
    pass

file_path = open(file_name, 'wb')
writer = csv.writer(file_path, quoting=csv.QUOTE_NONE)
writer.writerow(["im_name", "im_url", "im_product_id", "im_price", "im_condition"])

start = 0
number_of_products = 0

while (number_of_products < 400000):
    url = 'http://ace.tokopedia.com/search/v1/product/?image_size=700&image_square=false&start=%d&rows=100&sc=78,79&ob=8' % (number_of_products)
    print url
    try:
        response = urllib2.urlopen(url)
        data = json.load(response)

        if data['status']['message'] != "OK":
            print url
            print data['status']

        for product in data['data']:
            product_id = product['id']
            product_name = re.sub('\W', '_', product['name'])
            product_image_uri = product['image_uri']
            product_price = product['price']
            product_condition = product['condition']
            writer.writerow([product_name, product_image_uri, product_id, product_price, product_condition])
            number_of_products += 1

        print "total %d products downloaded" % number_of_products

    except urllib2.HTTPError, error:
        print "error downloading products from url %s" % url
        pass

print "download complete. %d products downloaded." % number_of_products