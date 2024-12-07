#ifndef IMM_NORMAL_STATE_H
#define IMM_NORMAL_STATE_H

#include "imm_compiler.h"
#include "imm_state.h"

struct imm_abc;

struct imm_normal_state
{
  struct imm_state super;
  float const *lprobs;
};

void imm_normal_state_init(struct imm_normal_state *, int id,
                                   struct imm_abc const *, float const *lprobs);

#endif
