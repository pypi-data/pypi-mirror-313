#ifndef IMM_AMINO_LPROB_H
#define IMM_AMINO_LPROB_H

#include "imm_amino.h"
#include "imm_compiler.h"

struct imm_amino_lprob
{
  struct imm_amino const *amino;
  float lprobs[IMM_AMINO_SIZE];
};

struct imm_amino_lprob imm_amino_lprob(struct imm_amino const *,
                                               float const *lprobs);
float imm_amino_lprob_get(struct imm_amino_lprob const *, char symbol);

#endif
