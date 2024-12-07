#ifndef IMM_PROD_H
#define IMM_PROD_H

#include "imm_compiler.h"
#include "imm_path.h"

struct imm_seq;

struct imm_prod
{
  struct imm_seq const *seq;
  struct imm_path path;
  float loglik;
  uint64_t mseconds;
};

struct imm_prod imm_prod(void);
void imm_prod_cleanup(struct imm_prod *);
void imm_prod_reset(struct imm_prod *);

#endif
