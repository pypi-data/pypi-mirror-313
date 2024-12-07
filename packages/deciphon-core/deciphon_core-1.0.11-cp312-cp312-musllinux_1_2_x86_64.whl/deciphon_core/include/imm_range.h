#ifndef IMM_RANGE_H
#define IMM_RANGE_H

#include <stdbool.h>
#include <stdio.h>

// Right-open interval: [start, stop)
struct imm_range
{
  int start;
  int stop;
};

struct imm_range imm_range(int start, int stop);
void imm_range_set(struct imm_range *, int start, int stop);
int imm_range_size(struct imm_range);
bool imm_range_empty(struct imm_range);
void imm_range_swap(struct imm_range *, struct imm_range *);
struct imm_range imm_range_intersect(struct imm_range, struct imm_range);
void imm_range_subtract(struct imm_range, struct imm_range, struct imm_range *,
                        struct imm_range *);
void imm_range_dump(struct imm_range, FILE *restrict);

#endif
