import requests
import json
import pdb
import re
from bs4 import BeautifulSoup



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

      payload["ctl00$content2$ddl_case"] = case_type
      payload["ctl00$content2$txt_no"] = case_no
      payload["ctl00$content2$ddl_year"] = case_year
      return case_list(payload,cookies)


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
      payload['__EVENTARGUMENT'] = ""
      payload['__LASTFOCUS'] = ""
      resp = []
      rows = html.find("table", {"id" : lambda L: L and L.startswith('ctl00_content2_grv')}).find_all('tr')
      for row in rows:
            cols = row.find_all('td')

            if len(cols) >0:
                  links = cols[-1].find_all('a')

                  if cols[0] != None and cols[0].text.strip() == "No Data Found":
                        break
                  elif len(links) >0 :
                        link = links[0].get('href')
                        trg = link.split('(')
                        event_trg =  trg[1].split(',')
                        payload['__EVENTTARGET'] = event_trg[0].replace("'","")
                        resp.append(case_details(payload,cookies))
      return resp



      
      



def case_details(payload,cookies):
      url = 'http://www.greentribunal.gov.in/search_all_case.aspx'
      response = requests.post(url, data=payload, cookies=cookies)
      html = BeautifulSoup(response.content, 'html.parser')
      data = {}
      data['petitioner'] =  html.find(id="ctl00_content2_lblpartyname3").text.strip()
      data['respondent'] = html.find(id="ctl00_content2_lblpartyname1").text.strip()
      if html.find(id="ctl00_content2_lblstatus").text.strip() == "DisposedOff":
            data['is_disposed'] = True
      else:
            data['is_disposed'] = False

      return data


def inputs():
      input_list = []
      input_list.append(raw_input("Enter Case Type ??"))
      input_list.append(raw_input("Enter Case No ??"))
      input_list.append(raw_input("Enter Case Year ??"))

      return input_list

if __name__ == '__main__':
      # case_type = raw_input("Enter Case Type ??")
      # case_no = raw_input("Enter Case No. ??")
      # case_year = raw_input("Enter Case Year ??")
      # emptyrequest(case_type,case_no,case_year)

      input_list = inputs()

      print input_list
      
      lists = emptyrequest(input_list[0],input_list[1],input_list[2])


      if not lists:
             print "Sorry ! No data found"
      else:
            print json.dumps(lists)

