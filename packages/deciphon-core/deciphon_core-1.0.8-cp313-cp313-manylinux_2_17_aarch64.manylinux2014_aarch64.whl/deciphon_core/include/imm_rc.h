#ifndef IMM_RC_H
#define IMM_RC_H

// clang-format off
enum imm_rc
{
  IMM_ENOMEM        =  1,
  IMM_EIO           =  2,
  IMM_EINVAL        =  3,
  IMM_EMANYSYMBOLS  =  4,
  IMM_ERANGE        =  5,
  IMM_EMUTECYLES    =  6,
  IMM_EDIFFABC      =  7,
  IMM_EMANYTRANS    =  8,
  IMM_ESTATEPRESENT =  9,
  IMM_ENOEND        = 10,
  IMM_ENOSTART      = 11,
  IMM_ENOTFOUND     = 12,
  IMM_ENOSEQ        = 13,
  IMM_ESHORTSEQ     = 14,
  IMM_EELAPSED      = 15,
  IMM_EDSTSTART     = 16,
  IMM_ESRCEND       = 17,
};
// clang-format on

#endif
