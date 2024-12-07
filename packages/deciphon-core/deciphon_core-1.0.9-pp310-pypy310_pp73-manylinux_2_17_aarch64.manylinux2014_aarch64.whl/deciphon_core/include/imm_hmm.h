#ifndef IMM_HMM_H
#define IMM_HMM_H

#include "imm_code.h"
#include "imm_compiler.h"
#include "imm_pair.h"
#include "imm_rc.h"
#include "imm_state.h"
#include "imm_trans.h"
#include <stdio.h>

struct imm_dp;
struct imm_hmm;
struct imm_path;
struct imm_seq;
struct imm_state;
struct imm_mute_state;

struct imm_hmm
{
  struct imm_code const *code;
  int start_state_id;
  int end_state_id;

  struct
  {
    int size;
    CCO_HASH_DECLARE(tbl, IMM_TRANS_MAX_SIZE - 1);
  } states;

  struct
  {
    int size;
    CCO_HASH_DECLARE(tbl, IMM_TRANS_MAX_SIZE - 1);
    struct imm_trans data[(1 << IMM_TRANS_MAX_SIZE)];
    struct imm_trans *avail;
  } transitions;
};

struct imm_hmm *imm_hmm_new(struct imm_code const *);
void imm_hmm_del(struct imm_hmm const *);

void imm_hmm_dump(struct imm_hmm const *, imm_state_name *,
                          FILE *restrict);
int imm_hmm_add_state(struct imm_hmm *, struct imm_state *);
int imm_hmm_del_state(struct imm_hmm *, struct imm_state *);
int imm_hmm_init_dp(struct imm_hmm const *, struct imm_dp *);
void imm_hmm_reset(struct imm_hmm *);

int imm_hmm_reset_dp(struct imm_hmm const *, struct imm_dp *);

float imm_hmm_trans(struct imm_hmm const *, struct imm_state const *src,
                            struct imm_state const *dst);

float imm_hmm_loglik(struct imm_hmm const *, struct imm_seq const *,
                             struct imm_path const *);

int imm_hmm_normalize_trans(struct imm_hmm const *);

int imm_hmm_normalize_state_trans(struct imm_state *src);

int imm_hmm_set_start(struct imm_hmm *, struct imm_mute_state const *);
int imm_hmm_set_end(struct imm_hmm *, struct imm_mute_state const *);

int imm_hmm_set_trans(struct imm_hmm *, struct imm_state *src,
                              struct imm_state *dst, float lprob);

#endif
