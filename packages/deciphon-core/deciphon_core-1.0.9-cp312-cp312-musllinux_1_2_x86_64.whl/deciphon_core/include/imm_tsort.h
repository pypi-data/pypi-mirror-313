#ifndef IMM_TSORT_H
#define IMM_TSORT_H

#include "imm_rc.h"

struct imm_state;

int imm_tsort(int nstates, struct imm_state **states, int start_idx);

#endif
