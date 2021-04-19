import PDMPlan

plan  = PDMPlan.PDMPlan()
while True:
  print("\nInput new task:")
  sName = input(" Name of task: ")
  if sName == "":
    break
  duration = int(input(" Duration: "))
  lPre   = input(" Predecessors: ").split(",")
  if lPre[0] == "":
    lPre = list()
  plan.add(sName, duration, lPre)
plan.calc()
print("-----PRINTING RESULT-----")
for e in plan.lProc:
    print("")
    print("Name: %s" % plan.lProc[e].sName)
    print("ESD: %s" %  plan.lProc[e].esd)
    print("EFD: %s" %  plan.lProc[e].efd)
    print("LSD: %s" %  plan.lProc[e].lsd)
    print("LFD: %s" %  plan.lProc[e].lfd)
    print("SLACK: %s" %   plan.lProc[e].slack)
    print("FB: %s" %   plan.lProc[e].fb)