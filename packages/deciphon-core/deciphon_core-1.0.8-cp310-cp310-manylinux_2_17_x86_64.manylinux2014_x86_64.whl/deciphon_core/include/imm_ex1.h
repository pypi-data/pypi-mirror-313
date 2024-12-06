#ifndef IMM_EX1_H
#define IMM_EX1_H

#include "imm_abc.h"
#include "imm_code.h"
#include "imm_hmm.h"
#include "imm_lprob.h"
#include "imm_mute_state.h"
#include "imm_normal_state.h"
#include "imm_state.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define IMM_EX1_SIZE 3000
#define IMM_EX1_NUCLT_ANY_SYMBOL '*'
#define IMM_EX1_NUCLT_SYMBOLS "BMIEJ"

struct imm_ex1
{
  struct imm_abc abc;
  struct imm_code code;
  struct imm_hmm *hmm;
  int core_size;
  struct imm_mute_state start;
  struct imm_normal_state b;
  struct imm_normal_state j;
  struct imm_normal_state m[IMM_EX1_SIZE];
  struct imm_normal_state i[IMM_EX1_SIZE];
  struct imm_mute_state d[IMM_EX1_SIZE];
  struct imm_normal_state e;
  struct imm_mute_state end;
  struct
  {
    struct imm_hmm *hmm;
    struct imm_mute_state nstart;
    struct imm_normal_state n;
    struct imm_mute_state nend;
  } null;
};

void imm_ex1_init(int core_size);
void imm_ex1_cleanup(void);
void imm_ex1_remove_insertion_states(int core_size);
void imm_ex1_remove_deletion_states(int core_size);
char *imm_ex1_state_name(int id, char *name);

extern struct imm_ex1 imm_ex1;

#endif
