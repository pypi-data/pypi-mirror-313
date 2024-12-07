#ifndef IMM_ABC_H
#define IMM_ABC_H

#include "imm_str.h"
#include "imm_sym.h"

#define IMM_ABC_MAX_SIZE 31
#define IMM_ABC_TYPEID_SIZE 10

enum imm_abc_typeid
{
  IMM_NULL_ABC = 0,
  IMM_ABC = 1,
  IMM_AMINO = 2,
  IMM_NUCLT = 3,
  IMM_DNA = 4,
  IMM_RNA = 5,
};

/**
 * Alphabet.
 *
 * It represents a finite set of symbols and a special any-symbol
 * symbol. It should be used as an immutable object.
 */
struct imm_abc
{
  int typeid;
  int size;
  char symbols[IMM_ABC_MAX_SIZE + 1];
  struct imm_sym sym;
  int any_symbol_id;
};

struct lio_writer;
struct lio_reader;

// clang-format off
int         imm_abc_init(struct imm_abc *, struct imm_str symbols,
                                 char any_symbol_id);
char        imm_abc_any_symbol(struct imm_abc const *);
bool        imm_abc_has_symbol_id(struct imm_abc const *, int id);
bool        imm_abc_has_symbol(struct imm_abc const *, char symbol);
int         imm_abc_size(struct imm_abc const *);
int         imm_abc_symbol_idx(struct imm_abc const *, char symbol);
int         imm_abc_any_symbol_id(struct imm_abc const *);
int         imm_abc_any_symbol_idx(struct imm_abc const *);
int         imm_abc_symbol_type(struct imm_abc const *, char symbol);
char const *imm_abc_symbols(struct imm_abc const *);
int         imm_abc_union_size(struct imm_abc const *, struct imm_str seq);
bool        imm_abc_typeid_valid(int typeid);
char const *imm_abc_typeid_name(int typeid);
int         imm_abc_pack(struct imm_abc const *, struct lio_writer *);
int         imm_abc_unpack(struct imm_abc *, struct lio_reader *);
// clang-format on

int imm__abc_symbol_idx(struct imm_abc const *, int id);
int imm__abc_symbol_type(struct imm_abc const *, int id);
int imm__abc_init(struct imm_abc *, int len, char const *symbols,
                  char any_symbol, int);

#endif
