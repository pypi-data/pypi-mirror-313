#ifndef IMM_FRAME_COND_H
#define IMM_FRAME_COND_H

#include "imm_compiler.h"
#include "imm_frame_epsilon.h"
#include "imm_frame_state.h"

struct imm_codon;
struct imm_nuclt_lprob;
struct imm_seq;

struct imm_frame_cond
{
  struct imm_frame_epsilon epsilon;
  struct imm_nuclt_lprob const *nucltp;
  struct imm_codon_marg const *codonm;
};

struct imm_frame_cond imm_frame_cond(struct imm_frame_state const *);
float imm_frame_cond_decode(struct imm_frame_cond const *,
                                    struct imm_seq const *, struct imm_codon *);
float imm_frame_cond_loglik(struct imm_frame_cond const *,
                                    struct imm_codon const *,
                                    struct imm_seq const *);
float imm_frame_cond_lprob(struct imm_frame_cond const *,
                                   struct imm_codon const *,
                                   struct imm_seq const *);

#endif
