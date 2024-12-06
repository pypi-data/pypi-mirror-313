#ifndef IMM_MATRIX_H
#define IMM_MATRIX_H

#include "imm_cell.h"
#include "imm_compiler.h"
#include "imm_matrixf.h"
#include "imm_state.h"
#include <stdio.h>

#define IMM_MATRIX_NROWS (IMM_STATE_MAX_SEQSIZE)

struct imm_state_table;

struct imm_matrix
{
  struct imm_matrixf score;
  struct imm_state_table const *state_table;
  int16_t *state_col;
};

int imm_matrix_init(struct imm_matrix *, struct imm_state_table const *);
int imm_matrix_reset(struct imm_matrix *, struct imm_state_table const *);
void imm_matrix_prepare(struct imm_matrix *);
void imm_matrix_cleanup(struct imm_matrix *);
void imm_matrix_dump(struct imm_matrix const *, FILE *restrict);

IMM_PURE float imm_matrix_get_score(struct imm_matrix const *x,
                                    struct imm_cell y)
{
  int row = y.row % IMM_MATRIX_NROWS;
  int col = x->state_col[y.state_idx] + y.emission_size;
  return imm_matrixf_get(&x->score, row, col);
}

IMM_INLINE void imm_matrix_set_score(struct imm_matrix *x, struct imm_cell y,
                                     float score)
{
  int row = y.row % IMM_MATRIX_NROWS;
  int col = x->state_col[y.state_idx] + y.emission_size;
  imm_matrixf_set(&x->score, row, col, score);
}

#endif
