#ifndef IMM_LIKELY_H
#define IMM_LIKELY_H

#ifdef __GNUC__
#define imm_likely(x) __builtin_expect(!!(x), 1)
#define imm_unlikely(x) __builtin_expect(!!(x), 0)
#else
#define imm_likely(x) (x)
#define imm_unlikely(x) (x)
#endif

#endif
