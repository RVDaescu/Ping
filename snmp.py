import netsnmp

def snmp_get(oid = None, ver = '2', dst = None, community = 'public'):

    oid =netsnmp.Varbind('sysDescr')
  
    result = netsnmp.snmpwalk(oid = oid, Version = ver, DestHost=dst, communityy = community)

    return result
