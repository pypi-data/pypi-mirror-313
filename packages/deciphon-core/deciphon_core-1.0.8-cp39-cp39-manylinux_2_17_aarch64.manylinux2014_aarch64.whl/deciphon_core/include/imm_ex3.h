#ifndef IMM_EX3_H
#define IMM_EX3_H

#include "imm_abc.h"
#include "imm_dna.h"
#include "imm_hmm.h"
#include "imm_mute_state.h"
#include "imm_normal_state.h"
#include "imm_state.h"

#define IMM_EX3_SIZE 3000
#define IMM_EX3_NUCLT_ANY_SYMBOL '*'
#define IMM_EX3_NUCLT_SYMBOLS "NMCJ"

struct imm_ex3
{
  struct imm_abc abc;
  struct imm_code code;
  struct imm_hmm *hmm;
  int core_size;
  struct imm_mute_state S;
  struct imm_normal_state N;
  struct imm_mute_state B;
  struct imm_normal_state M[IMM_EX3_SIZE];
  struct imm_mute_state E;
  struct imm_normal_state C;
  struct imm_mute_state T;
  struct imm_normal_state J;
};

extern struct imm_ex3 imm_ex3;
extern char const imm_ex3_seq1[];

void imm_ex3_init(int core_size);
void imm_ex3_cleanup(void);
char *imm_ex3_state_name(int id, char *name);

#endif
