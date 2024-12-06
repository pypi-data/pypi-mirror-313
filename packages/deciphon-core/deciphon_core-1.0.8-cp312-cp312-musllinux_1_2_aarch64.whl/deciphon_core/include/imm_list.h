#ifndef IMM_LIST_H
#define IMM_LIST_H

#include "imm_compiler.h"
#include "imm_container.h"
#include <stdbool.h>

struct imm_list
{
  struct imm_list *next;
  struct imm_list *prev;
};

void imm_list_init(struct imm_list *list);
void imm_list_add(struct imm_list *neu, struct imm_list *head);
void imm_list_del(struct imm_list *entry);
bool imm_list_is_head(struct imm_list const *list,
                              struct imm_list const *head);
bool imm_list_empty(struct imm_list const *head);

#define imm_list_for_each(pos, head)                                           \
  for (pos = (head)->next; !imm_list_is_head(pos, (head)); pos = pos->next)

#define imm_list_for_each_safe(pos, n, head)                                   \
  for (pos = (head)->next, n = pos->next; !imm_list_is_head(pos, (head));      \
       pos = n, n = pos->next)

#define imm_list_entry(ptr, type, member) imm_container(ptr, type, member)

#define imm_list_first_entry(ptr, type, member)                                \
  imm_list_entry((ptr)->next, type, member)

#define imm_list_entry_is_head(pos, head, member) (&pos->member == (head))

#define imm_list_next_entry(pos, member)                                       \
  imm_list_entry((pos)->member.next, __typeof__(*(pos)), member)

#define imm_list_for_each_entry(pos, head, member)                             \
  for (pos = imm_list_first_entry(head, __typeof__(*pos), member);             \
       !imm_list_entry_is_head(pos, head, member);                             \
       pos = imm_list_next_entry(pos, member))

#endif
