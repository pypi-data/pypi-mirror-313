#ifndef IMM_EMIS_H
#define IMM_EMIS_H

#include "imm_compiler.h"
#include "imm_state.h"
#include <stdint.h>
#include <stdio.h>

struct imm_emis
{
  float *score;    /**< Sequence emission score of a state. */
  int32_t *offset; /**< Maps state to score array offset. */
};

struct imm_cartes;
struct imm_code;
struct imm_state;
struct imm_state_table;

void imm_emis_init(struct imm_emis *);
void imm_emis_cleanup(struct imm_emis *);
int imm_emis_reset(struct imm_emis *, struct imm_code const *,
                   struct imm_state **states, int nstates);
int imm_emis_score_size(struct imm_emis const *, int nstates);
int imm_emis_offset_size(int nstates);

IMM_PURE float imm_emis_score(struct imm_emis const *x, int state, int seq_code)
{
  return x->score[x->offset[state] + seq_code];
}

IMM_INLINE float const *imm_emis_table(struct imm_emis const *x, int state,
                                       int *size)
{
  *size = x->offset[state + 1] - x->offset[state];
  return &x->score[x->offset[state]];
}

void imm_emis_dump(struct imm_emis const *,
                           struct imm_state_table const *, FILE *restrict);

#endif
