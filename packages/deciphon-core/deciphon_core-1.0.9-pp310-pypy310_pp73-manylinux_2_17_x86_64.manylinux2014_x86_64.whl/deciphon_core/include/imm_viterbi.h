#ifndef IMM_VITERBI_H
#define IMM_VITERBI_H

#include "imm_compiler.h"
#include "imm_dp_safety.h"
#include "imm_tardy_state.h"
#include <stdbool.h>

struct imm_dp;
struct imm_task;

struct imm_viterbi
{
  struct imm_dp const *dp;
  struct imm_task *task;
  struct imm_ctrans const *curr_trans;
  struct imm_dp_safety safety;
  int seqsize;
  bool has_tardy_state;
  struct tardy_state tardy_state;
};

void imm_viterbi_init(struct imm_viterbi *, struct imm_dp const *,
                              struct imm_task *);
void imm_viterbi_run(struct imm_viterbi *);

#endif
