#ifndef IMM_FRAME_STATE_H
#define IMM_FRAME_STATE_H

#include "imm_codon_marg.h"
#include "imm_compiler.h"
#include "imm_frame_epsilon.h"
#include "imm_nuclt_lprob.h"
#include "imm_span.h"
#include "imm_state.h"

struct imm_codon;
struct imm_codon_marg;
struct imm_nuclt_lprob;

struct imm_frame_state
{
  struct imm_state super;
  struct imm_nuclt_lprob const *nucltp;
  struct imm_codon_marg const *codonm;
  float epsilon;
  struct imm_frame_epsilon eps;
};

void imm_frame_state_init(struct imm_frame_state *, int id,
                                  struct imm_nuclt_lprob const *,
                                  struct imm_codon_marg const *, float epsilon,
                                  struct imm_span);

float imm_frame_state_lposterior(struct imm_frame_state const *,
                                         struct imm_codon const *,
                                         struct imm_seq const *);

float imm_frame_state_decode(struct imm_frame_state const *,
                                     struct imm_seq const *,
                                     struct imm_codon *);

void imm_frame_state_dump(struct imm_frame_state const *,
                                  FILE *restrict);

#endif
