import requests
import unicodecsv as csv
from xml.etree import ElementTree
from xml.etree.ElementTree import tostring
import time

def get_csv_col(filename):
  column_list = []
  with open(filename) as f:
    for row in f:
      column_list.append(row.split()[0])
  f.close()
  return column_list

def parse_company_row(tree, field_names, xpath):
  row = []
  for record in tree.findall(xpath):
    for field_name in field_names:
      value = record.find(field_name)
      if value is None:
        row.append('')
        continue
      row.append(value.text)
  return row

def parse_sni_row(tree, org_number):
  row = [org_number]
  snis = list(tree.iter())
  for value in snis:
    if(value.text):
      if not value.text.isspace():
        row.append(value.text)
  return row

apikey = "BIWS5c18a1a1b8a236ecee0f53e48581"
baseurl = "http://www.allabolag.se/ws/BIWS/service.php?key="+apikey+"&type=fetch&query=nummer:"

field_names = get_csv_col('field_names.csv')
org_numbers = get_csv_col('org_numbers.csv')

timestamp = str(int(time.time()))

companies_ofile = open('data/companies'+timestamp+'.csv', "wb")
snis_ofile = open('data/snis'+timestamp+'.csv', "wb")
company_writer = csv.writer(companies_ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8')
sni_writer = csv.writer(snis_ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8')

company_writer.writerow(field_names)
saldomultipel = 13

for org_number in org_numbers:
  response = requests.get(baseurl+org_number)
  tree = ElementTree.fromstring(response.content)
  company_writer.writerow(parse_company_row(tree, field_names, ".//records/record"))
  xml_file = open('data/'+org_number+'.xml','wb')
  xml_file.write(tostring(tree, 'utf-8', method="xml"))

  for snis in tree.findall(".//records/record/sni"):
    sni_writer.writerow(parse_sni_row(snis, org_number))

  saldo = float(tree.find(".//clientdata/saldo").text.replace(",", "."))
  print("Orgnr = "+org_number+". Saldo = "+ str(int(saldo)) +". "+ str(int(saldo/saldomultipel))+" hämtningar kvar.")
 
companies_ofile.close()
snis_ofile.close()


