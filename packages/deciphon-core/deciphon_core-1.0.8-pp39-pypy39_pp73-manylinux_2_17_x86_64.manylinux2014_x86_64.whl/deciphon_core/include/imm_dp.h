#ifndef IMM_DP_H
#define IMM_DP_H

#include "imm_code.h"
#include "imm_compiler.h"
#include "imm_emis.h"
#include "imm_state_table.h"
#include "imm_trans.h"
#include "imm_trans_table.h"
#include <float.h>
#include <stdio.h>

struct imm_abc;
struct imm_prod;
struct imm_seq;
struct imm_task;
struct imm_dp_cfg;

struct imm_dp
{
  struct imm_code const *code;
  struct imm_emis emis;
  struct imm_trans_table trans_table;
  struct imm_state_table state_table;
};

struct lio_writer;
struct lio_reader;

void imm_dp_init(struct imm_dp *, struct imm_code const *);
int imm_dp_reset(struct imm_dp *, struct imm_dp_cfg const *);
void imm_dp_set_state_name(struct imm_dp *, imm_state_name *);

void imm_dp_cleanup(struct imm_dp *);

void imm_dp_dump(struct imm_dp const *, FILE *restrict);

void imm_dp_dump_path(struct imm_dp const *, struct imm_task const *,
                              struct imm_prod const *, struct imm_seq const *,
                              FILE *restrict);

int imm_dp_nstates(struct imm_dp const *);
int imm_dp_trans_idx(struct imm_dp *, int src_idx, int dst_idx);
int imm_dp_change_trans(struct imm_dp *, int trans_idx, float lprob);
int imm_dp_viterbi(struct imm_dp const *, struct imm_task *task,
                           struct imm_prod *prod);

int imm_dp_pack(struct imm_dp const *, struct lio_writer *);
int imm_dp_unpack(struct imm_dp *, struct lio_reader *);

float imm_dp_emis_score(struct imm_dp const *, int state_id,
                                struct imm_seq const *seq);

float const *imm_dp_emis_table(struct imm_dp const *dp, int state_id,
                                       int *size);

float imm_dp_trans_score(struct imm_dp const *, int src, int dst);

void imm_dp_write_dot(struct imm_dp const *, FILE *restrict,
                              imm_state_name *);

#endif
