import enum

class SolveStatus(enum.IntEnum):
  UNSTARTED = 0
  STOPPED   = 1
  FAILED    = 2
  COMPLETED = 3

class SolStatus(enum.IntEnum):
  NOTFOUND   = 0
  OPTIMAL    = 1
  FEASIBLE   = 2
  INFEASIBLE = 3
  UNBOUNDED  = 4

del enum
