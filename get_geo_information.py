import numpy
import pandas
from matplotlib import pyplot
from library import PlotSettings
from library import misc
import ipinfo

access_token = '9bc342925a6a7b'
handler = ipinfo.getHandler(access_token)

within = pandas.read_csv('demographic_data/within.csv')
between = pandas.read_csv('demographic_data/between.csv')
simple = pandas.read_csv('demographic_data/simple.csv')
simple_amazon = pandas.read_csv('demographic_data/simple_amazon.csv')
jurgen = pandas.read_csv('demographic_data/jurgen.csv')
student = pandas.read_csv('demographic_data/student.csv')

data_sets = [within, between, simple, simple_amazon, jurgen, student]
names = ['within', 'between', 'simple', 'simple_amazon', 'jurgen', 'student']

record = open('demographic_data/locations.csv', 'w')
record.write('Order,Set,Dataset,IP,Country,Region,City,Latitude,Longitude\n')

counter = 0
for set in range(6):
    current_set = data_sets[set]
    current_set_name = names[set]
    ip_addresses = list(current_set.IPAddress.values)
    for ip_address in ip_addresses:
        details = handler.getDetails(ip_address)
        details = details.all

        country = details['country_name']
        region = details['region']
        city = details['city']
        latitude = details['latitude']
        longitude = details['longitude']

        city = city.replace(',','')
        region = region.replace(',', '')
        country = country.replace(',', '')

        line = misc.lst2str([counter,set,current_set_name, ip_address, country, region, city, latitude, longitude])
        print(line)
        record.write(line + '\n')
        #if counter > 5: break
        counter = counter + 1
record.close()



