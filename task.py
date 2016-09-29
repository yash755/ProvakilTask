import requests
import json
import pdb
from bs4 import BeautifulSoup

# pdb.set_trace()


def emptyrequest(case_type,case_no,case_year):  #To get important parameters.
      url = 'http://www.greentribunal.gov.in/search_all_case.aspx'
      payload = {}
      headers = {}

      response = requests.post(url, data=payload, headers=headers)
      cookies=response.cookies
      html = BeautifulSoup(response.content, 'html.parser')

      payload_elements = html.find_all("input")
      payload_elements.extend(html.find_all("select"))
      for element in payload_elements:
            payload[element.get('name')] = element.get('value')

      # for x in payload:
      #       print x
      payload["ctl00$content2$ddl_case"] = case_type
      payload["ctl00$content2$txt_no"] = case_no
      payload["ctl00$content2$ddl_year"] = case_year

      
      case_list(payload,cookies)


def case_list(payload,cookies):
      url = 'http://www.greentribunal.gov.in/search_all_case.aspx'
      response = requests.post(url, data=payload, cookies=cookies)
      html = BeautifulSoup(response.content, 'html.parser')
      payload_elements = []
      payload_elements = html.find_all("input")


      for element in payload_elements:
             payload[element.get('name')] = element.get('value')


      payload.pop("ctl00$content2$Button1",None)
      payload.pop("ctl00$content2$BtnSearch",None)
      payload.pop("ctl00$content2$btn_submit",None)
  

      #payload['__EVENTTARGET'] = "ctl00$content2$grv_all$ctl02$lnkbtnshowall"
      payload['__EVENTARGUMENT'] = ""
      payload['__LASTFOCUS'] = ""

      # payload_elements.extend(html.find_all("select"))

      # print html.find_all("select")
      # payload = {}
      # for element in payload_elements:
      #       payload[element.get('name')] = element.get('value')

      rows = html.find(id="ctl00_content2_grv_all").find_all('tr')
      for row in rows:
            cols = row.find_all('td')

            # if cols[0] != Null and cols[0].text.strip() == "No Data Found":
            #       print "No Data"
            #       break


            #############No valid for all tables change the tables
            

            if len(cols) >0:
                  links = cols[-1].find_all('a')
                  if len(links) >0 :
                        link = links[0].get('href')
                        trg = link.split('(')
                        event_trg =  trg[1].split(',')
                        payload['__EVENTTARGET'] = event_trg[0].replace("'","")
                        #case_details(payload,cookies)




      
      



def case_details(payload,cookies):
      url = 'http://www.greentribunal.gov.in/search_all_case.aspx'
      response = requests.post(url, data=payload, cookies=cookies)
      html = BeautifulSoup(response.content, 'html.parser')
      print html

      


if __name__ == '__main__':
      # case_type = raw_input("Enter Case Type ??")
      # case_no = raw_input("Enter Case No. ??")
      # case_year = raw_input("Enter Case Year ??")
      # emptyrequest(case_type,case_no,case_year)
      emptyrequest("3","496/2015","2015")

