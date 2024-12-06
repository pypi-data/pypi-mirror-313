#ifndef IMM_NUCLT_H
#define IMM_NUCLT_H

#include "imm_abc.h"
#include "imm_compiler.h"

#define IMM_NUCLT_ANY_SYMBOL 'X'
#define IMM_NUCLT_SYMBOLS "ACGT"
#define IMM_NUCLT_SIZE 4

struct imm_nuclt
{
  struct imm_abc super;
};

int imm_nuclt_init(struct imm_nuclt *, char const symbols[],
                           char any_symbol);
int imm_nuclt_size(struct imm_nuclt const *);

#endif
