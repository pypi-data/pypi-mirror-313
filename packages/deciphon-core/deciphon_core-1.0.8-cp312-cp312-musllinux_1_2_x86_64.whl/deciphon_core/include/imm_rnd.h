#ifndef IMM_RND_H
#define IMM_RND_H

#include "imm_compiler.h"
#include <stdint.h>

struct imm_rnd
{
  uint64_t data[4];
};

struct imm_rnd imm_rnd(uint64_t seed);
double imm_rnd_dbl(struct imm_rnd *);
uint64_t imm_rnd_u64(struct imm_rnd *);

#endif
