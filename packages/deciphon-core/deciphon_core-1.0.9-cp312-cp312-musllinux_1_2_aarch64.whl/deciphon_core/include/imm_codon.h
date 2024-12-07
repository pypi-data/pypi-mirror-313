#ifndef IMM_CODON_H
#define IMM_CODON_H

#include "imm_compiler.h"
#include "imm_nuclt.h"

struct imm_codon
{
  struct imm_nuclt const *nuclt;
  union
  {
    struct __attribute__((__packed__))
    {
      int a;
      int b;
      int c;
    };
    int idx[3];
  };
};

struct imm_codon imm_codon(struct imm_nuclt const *, int id_a, int id_b,
                                   int id_c);
void imm_codon_set(struct imm_codon *, int id_a, int id_b, int id_c);
char imm_codon_asym(struct imm_codon const *);
char imm_codon_bsym(struct imm_codon const *);
char imm_codon_csym(struct imm_codon const *);
struct imm_codon imm_codon_any(struct imm_nuclt const *);
struct imm_codon imm_codon_from_symbols(struct imm_nuclt const *,
                                                char a, char b, char c);

#define IMM_CODON(n, x) imm_codon_from_symbols(n, x[0], x[1], x[2])

#endif
