#ifndef IMM_DP_CFG_H
#define IMM_DP_CFG_H

struct imm_dp_cfg
{
  int ntrans;
  int nstates;
  struct imm_state **states;
  struct imm_state const *start_state;
  struct imm_state const *end_state;
};

#endif
