#ifndef IMM_TRANS_H
#define IMM_TRANS_H

#include "imm_htable.h"
#include "imm_list.h"
#include "imm_pair.h"
#include <stdint.h>

#define IMM_TRANS_NULL_IDX INT16_MAX
#define IMM_TRANS_MAX_SIZE 18

struct imm_trans
{
  struct imm_pair pair;
  float lprob;
  struct imm_list outgoing;
  struct imm_list incoming;
  struct cco_hnode hnode;
};

void imm_trans_init(struct imm_trans *, int src, int dst, float lprob);

#endif
