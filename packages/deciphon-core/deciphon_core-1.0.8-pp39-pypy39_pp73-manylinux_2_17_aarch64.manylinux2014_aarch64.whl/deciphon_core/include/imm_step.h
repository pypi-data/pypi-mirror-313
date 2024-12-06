#ifndef IMM_STEP_H
#define IMM_STEP_H

#include "imm_compiler.h"
#include "imm_state.h"
#include "imm_static_assert.h"
#include <stdalign.h>
#include <stdint.h>

struct imm_step
{
  uint16_t state_id;
  int8_t seqsize;
  float score;
};

imm_static_assert(sizeof(struct imm_step) == 8, "struct pair must be packed");
imm_static_assert(alignof(struct imm_step) == 4, "struct pair must align to 4");

struct imm_step imm_step(int state_id, int seqsize, float score);

#endif
