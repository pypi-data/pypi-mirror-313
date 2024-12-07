#ifndef IMM_DP_SAFETY_H
#define IMM_DP_SAFETY_H

#include "imm_range.h"

struct imm_dp_safety
{
  struct imm_range safe_future;
  struct imm_range safe;
  struct imm_range unsafe;
  struct imm_range safe_past;
};

void imm_dp_safety_init(struct imm_dp_safety *x, int size);

#endif
