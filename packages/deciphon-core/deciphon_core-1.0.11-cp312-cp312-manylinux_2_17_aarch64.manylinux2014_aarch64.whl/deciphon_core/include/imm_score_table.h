#ifndef IMM_SCORE_TABLE_H
#define IMM_SCORE_TABLE_H

#include "imm_cartes.h"
#include "imm_compiler.h"

struct imm_score_table
{
  struct imm_code const *code;
};

struct imm_state;

void imm_score_table_init(struct imm_score_table *,
                                  struct imm_code const *);
void imm_score_table_cleanup(struct imm_score_table *);

int imm_score_table_size(struct imm_score_table const *,
                                 struct imm_state const *);
void imm_score_table_scores(struct imm_score_table const *,
                                    struct imm_state const *, float *);

#endif
