#ifndef IMM_EX2_H
#define IMM_EX2_H

#include "imm_codon_marg.h"
#include "imm_dna.h"
#include "imm_frame_state.h"
#include "imm_hmm.h"
#include "imm_lprob.h"
#include "imm_mute_state.h"
#include "imm_state.h"

#define IMM_EX2_SIZE 1000

struct imm_ex2
{
  struct imm_dna const *dna;
  struct imm_code code;
  struct imm_hmm *hmm;
  int core_size;
  struct imm_mute_state start;
  struct imm_frame_state b;
  struct imm_frame_state j;
  struct imm_frame_state m[IMM_EX2_SIZE];
  struct imm_frame_state i[IMM_EX2_SIZE];
  struct imm_mute_state d[IMM_EX2_SIZE];
  struct imm_frame_state e;
  struct imm_mute_state end;
  struct imm_nuclt_lprob nucltp;
  struct imm_codon_marg m_marg;
  struct imm_codon_marg i_marg;
  struct imm_codon_marg b_marg;
  struct imm_codon_marg e_marg;
  struct imm_codon_marg j_marg;
  struct
  {
    struct imm_hmm *hmm;
    struct imm_mute_state nstart;
    struct imm_frame_state n;
    struct imm_mute_state nend;
    struct imm_codon_marg n_marg;
  } null;
};

void imm_ex2_init(int core_size, struct imm_span span);
void imm_ex2_cleanup(void);

extern struct imm_ex2 imm_ex2;
extern char const imm_ex2_seq[];

#endif
