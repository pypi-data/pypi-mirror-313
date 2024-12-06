#ifndef IMM_ABC_LPROB_H
#define IMM_ABC_LPROB_H

#include "imm_lprob.h"

struct imm_abc;

struct imm_abc_lprob
{
  struct imm_abc const *abc;
  float const *lprobs;
};

struct imm_abc_lprob imm_abc_lprob(struct imm_abc const *,
                                           float const *lprobs);
float imm_abc_lprob_get(struct imm_abc_lprob const *, char symbol);

#endif
