import requests
import sys

apikey = sys.argv[1]
baseurl = "http://www.allabolag.se/ws/BIWS/service.php?key="+apikey+"&type=fetch&query=nummer:"


for org_number in sys.argv[2:]:
  xml_file = open(org_number + '.xml','wb')
  response = requests.get(baseurl+org_number)
  xml_file.write(response.content)
  print("Data saved to " + xml_file.name)
  xml_file.close()
