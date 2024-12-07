#ifndef IMM_CODON_STATE_H
#define IMM_CODON_STATE_H

#include "imm_compiler.h"
#include "imm_state.h"

struct imm_codon_lprob;

struct imm_codon_state
{
  struct imm_state super;
  struct imm_codon_lprob const *codonp;
};

void imm_codon_state_init(struct imm_codon_state *, int id,
                                  struct imm_codon_lprob const *);

#endif
