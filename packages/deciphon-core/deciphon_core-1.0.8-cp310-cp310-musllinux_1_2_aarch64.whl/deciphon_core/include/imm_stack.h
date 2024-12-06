#ifndef IMM_STACK_H
#define IMM_STACK_H

#include "imm_list.h"

void imm_stack_put(struct imm_list *neu, struct imm_list *stack);
void imm_stack_pop(struct imm_list *stack);

#endif
