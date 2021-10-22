#!/usr/bin/env python3

import ldap
from settings import settings

# AD search user
def SearchADLocked(conn):
  data = conn.search_s(settings['ADdomain'], ldap.SCOPE_SUBTREE, 'userAccountControl=514' , ['mail'])
  # userAccountControl: 512 = unlocked, 512+2 = locked
  out = []
  for i in data:
    if i[1]:
      out.append(i[1]['mail'][0].decode('utf-8'))
  return out

conn = ldap.initialize('ldap://' + settings['ADserver'])
conn.protocol_version = 3
conn.set_option(ldap.OPT_REFERRALS, 0)
conn.simple_bind_s(settings['ADuser'], settings['ADpassword'])

f = open(settings['ZimbraDumpFile'], "w")

locked_accounts = SearchADLocked(conn)

for i in locked_accounts:
  f.write("ma {} zimbraAccountStatus closed\n".format(i))
#zimbraAccountStatus must be one of: active,maintenance,locked,closed,lockout,pending)

f.close()