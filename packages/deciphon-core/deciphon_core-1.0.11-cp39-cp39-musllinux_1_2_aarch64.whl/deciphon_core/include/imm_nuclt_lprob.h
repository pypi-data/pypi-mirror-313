#ifndef IMM_NUCLT_LPROB_H
#define IMM_NUCLT_LPROB_H

#include "imm_compiler.h"
#include "imm_nuclt.h"
#include <stdio.h>

struct imm_nuclt_lprob
{
  struct imm_nuclt const *nuclt;
  float lprobs[IMM_NUCLT_SIZE];
};

struct lio_writer;
struct lio_reader;

struct imm_nuclt_lprob imm_nuclt_lprob(struct imm_nuclt const *,
                                               float const *lprobs);
float imm_nuclt_lprob_get(struct imm_nuclt_lprob const *, char symbol);
int imm_nuclt_lprob_pack(struct imm_nuclt_lprob const *,
                                 struct lio_writer *);
int imm_nuclt_lprob_unpack(struct imm_nuclt_lprob *, struct lio_reader *);
void imm_nuclt_lprob_dump(struct imm_nuclt_lprob const *,
                                  FILE *restrict);

float imm__nuclt_lprob_get(struct imm_nuclt_lprob const *, int idx);

#endif
