#!/usr/bin/env python3
import urllib.request, json 
import sys
import ssl

SERVER_ADDRESS='127.0.0.1'
SERVER_PORT=443

#avoid the exception "ssl.CertificateError: hostname 'X.Y.W.Z' doesn't match 'HOSTNAME'"
ssl.match_hostname = lambda cert, hostname: True

with urllib.request.urlopen("https://" + SERVER_ADDRESS + ":" + str(SERVER_PORT) + "/admin/api.php?summaryRaw&getQuerySources&topClientsBlocked") as url:
  data = json.loads(url.read().decode())
  #print(data)
  sys.stdout.write("0 PiHole_DnsQueries_Daily TotalQueries="+str(data['dns_queries_today'])+"|BlockedQueries="+str(data['ads_blocked_today'])+"|ForwardedQueries="+str(data['queries_forwarded'])+"|CachedQueries="+str(data['queries_cached'])+" "+str(data['dns_queries_today'])+" DNS queries today (blocked "+str('{:.2f}'.format(data['ads_percentage_today']))+"%)")
  sys.stdout.write("\n")
  try: #compatibility with previous piHole versions
    sys.stdout.write("0 PiHole_DnsQueries_TypeReply reply_IP="+str(data['reply_IP'])+"|reply_CNAME="+str(data['reply_CNAME'])+"|reply_NXDOMAIN="+str(data['reply_NXDOMAIN'])+"|reply_NODATA="+str(data['reply_NODATA'])+" DNS replies for typology: IP="+str(data['reply_IP'])+", CNAME="+str(data['reply_CNAME'])+", NXDOMAIN="+str(data['reply_NXDOMAIN'])+", NODATA="+str(data['reply_NODATA']) )
    sys.stdout.write("\n")
  except:
    pass
  sys.exit(0)
