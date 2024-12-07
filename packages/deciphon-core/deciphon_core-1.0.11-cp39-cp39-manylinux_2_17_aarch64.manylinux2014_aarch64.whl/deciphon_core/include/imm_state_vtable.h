#ifndef IMM_STATE_VTABLE_H
#define IMM_STATE_VTABLE_H

#include "imm_state_typeid.h"

struct imm_seq;
struct imm_state;

struct imm_state_vtable
{
  float (*lprob)(struct imm_state const *state, struct imm_seq const *seq);
  enum imm_state_typeid typeid;
  void *derived;
};

#endif
