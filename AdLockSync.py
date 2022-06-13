#!/usr/bin/env python3

import ldap
import re
from ldap.controls.libldap import SimplePagedResultsControl
from settings import settings

def SearchADLocked(conn):
  data = conn.search_ext(base=settings['ADdomain'], scope=ldap.SCOPE_SUBTREE,
            filterstr=search_flt, attrlist=searchreq_attrlist,
            serverctrls=[req_ctrl])
  return data

conn = ldap.initialize('ldap://' + settings['ADserver'])
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s(settings['ADuser'], settings['ADpassword'])
search_flt = 'userAccountControl=514' # userAccountControl: 512 = unlocked, 512+2 = locked
searchreq_attrlist=['mail']
page_size = 1300
req_ctrl = SimplePagedResultsControl(criticality=True, size=page_size, cookie='')

f = open(settings['ZimbraDumpFile'], "w")

locked_accounts = []

msgid = SearchADLocked(conn)
pages = 0
while True:
    pages += 1
    rtype, rdata, rmsgid, serverctrls = conn.result3(msgid)
    for user in rdata:
        if len(user[1]) > 0:
          mail = user[1]['mail'][0].decode('utf-8')
          #regex check to make sure email field is correct and not just one word without domain name
          regex = re.search(settings['regexMemberCheck'], mail)
          if regex is None:
            print('Mail field contains werid stuff, pls fix\n', user, '\n' ,mail)
          else:
            locked_accounts.append(mail)
        else:
          print('User dont have email field or incomplete AD data, pls fix \n', user)

    pctrls = [c for c in serverctrls if c.controlType == SimplePagedResultsControl.controlType]
    if pctrls:
        if pctrls[0].cookie:
            req_ctrl.cookie = pctrls[0].cookie
            msgid = conn.search_ext(base=settings['ADdomain'], scope=ldap.SCOPE_SUBTREE, filterstr=search_flt, attrlist=searchreq_attrlist, serverctrls=[req_ctrl])
        else:
            break
    else:
        break


for i in locked_accounts:
  f.write("ma {} zimbraAccountStatus closed\n".format(i))
# zimbraAccountStatus must be one of: active,maintenance,locked,closed,lockout,pending)

f.close()