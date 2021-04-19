class Task:
  def __init__(self, sName, duration, lPre):
    self.sName       = sName
    self.duration    = duration
    self.lPre        = lPre
    self.lPost       = list()
    self.esd         = 0         # Early Start Date
    self.efd         = 0         # Early Finish Date
    self.lsd         = 0         # Late Start Date
    self.lfd         = 0         # Late Finish Date
    self.slack       = 0         # Slack
    self.fb          = 0         # Free buffer
    self._bIsTainted = False     # Needed for loop-detection

class LoopDetected(BaseException):
    def __init__(self, message):
      self.message = message
    
class PDMPlan:
  def __init__(self):
    self.lProc = dict()

  # Description:
  #   Calculates all dates / buffers for the current PDM.
  #   This includes the following:
  #     esd:   Early start date
  #     efd:   Early finish date
  #     lsd:   Late start date
  #     lfd:   Late finish date
  #     slack: Time the Task can be delayed, without delaying the successor
  #     fb:    Time the task can be delayed, without delaying the early start date(s)
  #            of the successors
  # Returns True on success or False on error
  def calc(self):
    # Determine ESD and EFD of all nodes
    for sEntry in self.lProc:
      try:
        self._descForEarly(sEntry)
      except LoopDetected:
        return False
    # Determine LSD and LFD of all nodes
    # plus FB and SLACK
    for sEntry in self.lProc:
      self._ascForLatest(sEntry)
    return True

  # Description:
  #   Adds new task to PDM
  def add(self, sName, duration, lPre):
    self.lProc[sName] = Task(sName, duration, lPre)

  def _descForEarly(self, sKey):
    curNode = self.lProc[sKey]
    # Loop detection
    if curNode._bIsTainted:
      raise LoopDetected("Detected loop in PDM")
    curNode._bIsTainted = True
    # Early out, when node has already been calculated.
    if curNode.efd != 0:
      curNode._bIsTainted = False
      return
    # Handle beginning of network plan
    if len(curNode.lPre) == 0:
      curNode.efd = curNode.duration
    # Calculate maximum of EFD of all predecessors
    else:
      maxEFD = 0
      for sEntry in curNode.lPre:
        self.lProc[sEntry].lPost.append(sKey)
        # Descend to determine EFD of node below
        self._descForEarly(sEntry)
        if self.lProc[sEntry].efd > maxEFD:
          maxEFD = self.lProc[sEntry].efd
        curNode.esd = maxEFD
        curNode.efd = curNode.esd + curNode.duration
    curNode._bIsTainted = False

  def _ascForLatest(self, sKey):
    curNode = self.lProc[sKey]
    # Early out, when node has already been calculated
    if curNode.lfd != 0:
      return
    # Handle end node of PDM
    if len(curNode.lPost) == 0:
      curNode.lsd = curNode.esd
      curNode.lfd = curNode.efd
    # Calculate minimum of LSD of all successors
    else:
      minLSD = 0
      for sEntry in curNode.lPost:
        # Ascend to determine LSD of node above
        self._ascForLatest(sEntry)
        if self.lProc[sEntry].lsd < minLSD or minLSD == 0:
          minLSD = self.lProc[sEntry].lsd
      curNode.lfd   = max(minLSD, curNode.efd)
      curNode.lsd   = curNode.lfd - curNode.duration
      curNode.slack = curNode.lfd - curNode.efd
      # Determine FB
      minESD = 0
      for sEntry in curNode.lPost:
        if self.lProc[sEntry].esd < minESD or minESD == 0:
          minESD = self.lProc[sEntry].esd
      curNode.fb = minESD - curNode.efd