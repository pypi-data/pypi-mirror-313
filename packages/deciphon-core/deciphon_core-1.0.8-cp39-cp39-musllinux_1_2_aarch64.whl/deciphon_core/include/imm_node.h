#ifndef IMM_NODE_H
#define IMM_NODE_H

#include "imm_compiler.h"
#include "imm_lprob.h"
#include "imm_state.h"
#include "imm_static_assert.h"
#include <stdint.h>
#include <stdio.h>

struct imm_node
{
  float score;
  int16_t state_source;
  int8_t emission_size;
};

struct imm_state_table;

// TODO: I would like this to be 4 bytes instead
imm_static_assert(sizeof(struct imm_node) == 8, "");

void imm_node_dump(struct imm_node const *, uint16_t *ids,
                           imm_state_name *, FILE *restrict);

IMM_INLINE void imm_node_invalidate(struct imm_node *x)
{
  x->score = IMM_LPROB_NAN;
  x->state_source = IMM_STATE_NULL_IDX;
  x->emission_size = IMM_STATE_NULL_SEQSIZE;
}

#endif
