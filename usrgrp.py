import pwd, grp

def getusrgrpnames():
  """
  Get all the username and groupnames
  """
  names = []
  for p in pwd.getpwall():
    names.append(p[0])

  for g in grp.getgrall():
    names.append(g[0])

  return names
