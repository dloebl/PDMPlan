# PDMPlan
Library for solving PDM (Precedence diagram method) plans (German: Netzplantechnik).

PDMs covered by this scripts contain the following attributes per task:
- Name of task
- Duration of task
- Early start date (ESD)
- Early finish date (EFD)
- Late start date (LSD)
- Late finish date (LFD)
- Slack: Time the task can be delayed, without delaying the LSD of successors
- Free buffer: Time the task can be delayed, without delaying the ESD of successors
