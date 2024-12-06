#ifndef IMM_RNA_H
#define IMM_RNA_H

#include "imm_compiler.h"
#include "imm_nuclt.h"

#define IMM_RNA_ANY_SYMBOL 'X'
#define IMM_RNA_SYMBOLS "ACGU"
#define IMM_RNA_SIZE 4

struct imm_rna
{
  struct imm_nuclt super;
};

extern struct imm_rna const imm_rna_iupac;

int imm_rna_init(struct imm_rna *rna, char const symbols[],
                         char any_symbol);

#endif
