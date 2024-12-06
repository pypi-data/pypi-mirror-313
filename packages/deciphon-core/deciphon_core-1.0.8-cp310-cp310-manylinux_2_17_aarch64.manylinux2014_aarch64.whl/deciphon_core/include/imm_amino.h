#ifndef IMM_AMINO_H
#define IMM_AMINO_H

#include "imm_abc.h"
#include "imm_compiler.h"

#define IMM_AMINO_ANY_SYMBOL 'X'
#define IMM_AMINO_SYMBOLS "ACDEFGHIKLMNPQRSTVWY"
#define IMM_AMINO_SIZE 20

struct imm_amino
{
  struct imm_abc super;
};

extern struct imm_amino const imm_amino_iupac;

int imm_amino_init(struct imm_amino *amino, char const *symbols,
                           char any_symbol);

#endif
