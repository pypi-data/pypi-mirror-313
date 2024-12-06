#ifndef IMM_PATH_H
#define IMM_PATH_H

#include "imm_compiler.h"
#include "imm_state.h"
#include "imm_step.h"
#include <stdio.h>

struct imm_path
{
  int capacity;
  int nsteps;
  int dir;
  int start;
  struct imm_step *steps;
};

struct imm_path imm_path(void);
int imm_path_add(struct imm_path *, struct imm_step);
struct imm_step *imm_path_step(struct imm_path const *, int);
void imm_path_add_unsafe(struct imm_path *, struct imm_step);
void imm_path_cleanup(struct imm_path *);
void imm_path_reset(struct imm_path *);
int imm_path_nsteps(struct imm_path const *);
void imm_path_reverse(struct imm_path *);
float imm_path_score(struct imm_path const *);
void imm_path_cut(struct imm_path *, int step, int size);
void imm_path_dump(struct imm_path const *, imm_state_name *,
                           struct imm_seq const *, FILE *restrict);

#endif
