#ifndef IMM_MUTE_STATE_H
#define IMM_MUTE_STATE_H

#include "imm_compiler.h"
#include "imm_state.h"

struct imm_abc;

struct imm_mute_state
{
  struct imm_state super;
};

void imm_mute_state_init(struct imm_mute_state *, int id,
                                 struct imm_abc const *);

#endif
