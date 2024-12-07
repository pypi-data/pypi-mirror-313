#ifndef IMM_TRANS_TABLE_H
#define IMM_TRANS_TABLE_H

#include "imm_assume.h"
#include "imm_compiler.h"
#include "imm_ctrans.h"
#include "imm_state.h"
#include "imm_trans.h"
#include <stdio.h>

struct imm_trans_table
{
  int ntrans;
  struct imm_ctrans *trans;
  int16_t *offset; /**< `trans[offset[dst]]` is the first transition and
                        `trans[offset[dst+1]-1]` is the last transition. */
};

struct imm_dp_cfg;
struct imm_state_table;

void imm_trans_table_init(struct imm_trans_table *);
int imm_trans_table_reset(struct imm_trans_table *, struct imm_dp_cfg const *);

int imm_trans_table_idx(struct imm_trans_table const *, int src, int dst);

void imm_trans_table_change(struct imm_trans_table *, int trans, float score);

void imm_trans_table_cleanup(struct imm_trans_table *);

int imm_trans_table_transsize(int ntrans);
int imm_trans_table_offsize(int nstates);

IMM_PURE int imm_trans_table_ntrans(struct imm_trans_table const *x, int dst)
{
  imm_assume(x->offset[dst + 1] >= x->offset[dst]);
  return (int)(x->offset[dst + 1] - x->offset[dst]);
}

IMM_PURE int imm_trans_table_source_state(struct imm_trans_table const *x,
                                          int dst, int trans)
{
  return x->trans[x->offset[dst] + trans].src;
}

IMM_PURE float imm_trans_table_score(struct imm_trans_table const *x, int dst,
                                     int trans)
{
  return x->trans[x->offset[dst] + trans].score;
}

IMM_PURE int16_t imm_trans_table_trans_start(struct imm_trans_table const *x,
                                             int state)
{
  return x->offset[state];
}

IMM_PURE struct imm_ctrans const *
imm_trans_table_ctrans_start(struct imm_trans_table const *x)
{
  return x->trans;
}

void imm_trans_table_dump(struct imm_trans_table const *,
                                  struct imm_state_table const *st,
                                  FILE *restrict);

#endif
