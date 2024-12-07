#ifndef LITE_PACK_H
#define LITE_PACK_H

#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

size_t lip_pack_nil(unsigned char buffer[]);
size_t lip_pack_bool(unsigned char buffer[], bool data);
size_t lip_pack_i8 (unsigned char buffer[], int8_t  data);
size_t lip_pack_i16(unsigned char buffer[], int16_t data);
size_t lip_pack_i32(unsigned char buffer[], int32_t data);
size_t lip_pack_i64(unsigned char buffer[], int64_t data);
size_t lip_pack_u8 (unsigned char buffer[], uint8_t  data);
size_t lip_pack_u16(unsigned char buffer[], uint16_t data);
size_t lip_pack_u32(unsigned char buffer[], uint32_t data);
size_t lip_pack_u64(unsigned char buffer[], uint64_t data);
size_t lip_pack_f32(unsigned char buffer[], float  data);
size_t lip_pack_f64(unsigned char buffer[], double data);
size_t lip_pack_string(unsigned char buffer[], uint32_t size);
size_t lip_pack_array(unsigned char buffer[], uint32_t size);
size_t lip_pack_map(unsigned char buffer[], uint32_t size);
size_t lip_pack_ext(unsigned char buffer[], uint32_t size, uint8_t type);
size_t lip_pack_bin(unsigned char buffer[], uint32_t size);

size_t lip_unpack_nil(unsigned char buffer[]);
size_t lip_unpack_bool(unsigned char const buffer[], bool *data);
size_t lip_unpack_i8 (unsigned char const buffer[], int8_t  *data);
size_t lip_unpack_i16(unsigned char const buffer[], int16_t *data);
size_t lip_unpack_i32(unsigned char const buffer[], int32_t *data);
size_t lip_unpack_i64(unsigned char const buffer[], int64_t *data);
size_t lip_unpack_u8 (unsigned char const buffer[], uint8_t  *data);
size_t lip_unpack_u16(unsigned char const buffer[], uint16_t *data);
size_t lip_unpack_u32(unsigned char const buffer[], uint32_t *data);
size_t lip_unpack_u64(unsigned char const buffer[], uint64_t *data);
size_t lip_unpack_f32(unsigned char const buffer[], float  *data);
size_t lip_unpack_f64(unsigned char const buffer[], double *data);
size_t lip_unpack_string(unsigned char const buffer[], uint32_t *size);
size_t lip_unpack_array(unsigned char const buffer[], uint32_t *size);
size_t lip_unpack_map(unsigned char const buffer[], uint32_t *size);
size_t lip_unpack_ext(unsigned char const buffer[], uint32_t *size, uint8_t *type);
size_t lip_unpack_bin(unsigned char const buffer[], uint32_t *size);

size_t lip_size(unsigned char const buffer[]);

#ifndef LLONG_WIDTH
#define LLONG_WIDTH (__SIZEOF_LONG_LONG__ * CHAR_BIT)
#endif

#ifndef LONG_WIDTH
#define LONG_WIDTH (__SIZEOF_LONG__ * CHAR_BIT)
#endif

#ifndef INT_WIDTH
#define INT_WIDTH (__SIZEOF_INT__ * CHAR_BIT)
#endif

#ifndef SHRT_WIDTH
#define SHRT_WIDTH (__SIZEOF_SHORT__ * CHAR_BIT)
#endif

#ifndef SCHAR_WIDTH
#define SCHAR_WIDTH CHAR_BIT
#endif

#ifndef ULLONG_WIDTH
#define ULLONG_WIDTH LLONG_WIDTH
#endif

#ifndef ULONG_WIDTH
#define ULONG_WIDTH LONG_WIDTH
#endif

#ifndef UINT_WIDTH
#define UINT_WIDTH INT_WIDTH
#endif

#ifndef USHRT_WIDTH
#define USHRT_WIDTH SHRT_WIDTH
#endif

#ifndef UCHAR_WIDTH
#define UCHAR_WIDTH SCHAR_WIDTH
#endif

#if LLONG_WIDTH == 64
static inline size_t lip_pack_signed_long_long(unsigned char buffer[], signed long long data) { return lip_pack_i64(buffer, data); }
static inline size_t lip_unpack_signed_long_long(unsigned char buffer[], signed long long *data) { return lip_unpack_i64(buffer, (int64_t *)data); }
#else
#error "Unsupported signed long long width"
#endif

#if LONG_WIDTH == 64
static inline size_t lip_pack_signed_long(unsigned char buffer[], signed long data) { return lip_pack_i64(buffer, data); }
static inline size_t lip_unpack_signed_long(unsigned char buffer[], signed long *data) { return lip_unpack_i64(buffer, (int64_t *)data); }
#else
#error "Unsupported signed long width"
#endif

#if INT_WIDTH == 32
static inline size_t lip_pack_signed_int(unsigned char buffer[], signed int data) { return lip_pack_i32(buffer, data); }
static inline size_t lip_unpack_signed_int(unsigned char buffer[], signed int *data) { return lip_unpack_i32(buffer, data); }
#else
#error "Unsupported signed int width"
#endif

#if SHRT_WIDTH == 16
static inline size_t lip_pack_signed_short(unsigned char buffer[], signed short data) { return lip_pack_i16(buffer, data); }
static inline size_t lip_unpack_signed_short(unsigned char buffer[], signed short *data) { return lip_unpack_i16(buffer, data); }
#else
#error "Unsupported signed short width"
#endif

#if SCHAR_WIDTH == 8
static inline size_t lip_pack_signed_char(unsigned char buffer[], signed char data) { return lip_pack_i8(buffer, data); }
static inline size_t lip_unpack_signed_char(unsigned char buffer[], signed char *data) { return lip_unpack_i8(buffer, data); }
#else
#error "Unsupported signed char width"
#endif

#if ULLONG_WIDTH == 64
static inline size_t lip_pack_unsigned_long_long(unsigned char buffer[], unsigned long long data) { return lip_pack_u64(buffer, data); }
static inline size_t lip_unpack_unsigned_long_long(unsigned char buffer[], unsigned long long *data) { return lip_unpack_u64(buffer, (uint64_t *)data); }
#else
#error "Unsupported unsigned long long width"
#endif

#if ULONG_WIDTH == 64
static inline size_t lip_pack_unsigned_long(unsigned char buffer[], unsigned long data) { return lip_pack_u64(buffer, data); }
static inline size_t lip_unpack_unsigned_long(unsigned char buffer[], unsigned long *data) { return lip_unpack_u64(buffer, (uint64_t *)data); }
#else
#error "Unsupported unsigned long width"
#endif

#if UINT_WIDTH == 32
static inline size_t lip_pack_unsigned_int(unsigned char buffer[], unsigned int data) { return lip_pack_u32(buffer, data); }
static inline size_t lip_unpack_unsigned_int(unsigned char buffer[], unsigned int *data) { return lip_unpack_u32(buffer, data); }
#else
#error "Unsupported unsigned int width"
#endif

#if USHRT_WIDTH == 16
static inline size_t lip_pack_unsigned_short(unsigned char buffer[], unsigned short data) { return lip_pack_u16(buffer, data); }
static inline size_t lip_unpack_unsigned_short(unsigned char buffer[], unsigned short *data) { return lip_unpack_u16(buffer, data); }
#else
#error "Unsupported unsigned short width"
#endif

#if UCHAR_WIDTH == 8
static inline size_t lip_pack_unsigned_char(unsigned char buffer[], unsigned char data) { return lip_pack_u8(buffer, data); }
static inline size_t lip_unpack_unsigned_char(unsigned char buffer[], unsigned char *data) { return lip_unpack_u8(buffer, data); }
#else
#error "Unsupported unsigned char width"
#endif


#define lip_pack_int(buffer, data)                                             \
  _Generic((data),                                                             \
      int8_t: lip_pack_i8,                                                     \
      int16_t: lip_pack_i16,                                                   \
      int32_t: lip_pack_i32,                                                   \
      int64_t: lip_pack_i64,                                                   \
      uint8_t: lip_pack_u8,                                                    \
      uint16_t: lip_pack_u16,                                                  \
      uint32_t: lip_pack_u32,                                                  \
      uint64_t: lip_pack_u64,                                                  \
      default: _Generic((data),                                                \
      signed char: lip_pack_signed_char,                                       \
      signed short: lip_pack_signed_short,                                     \
      signed int: lip_pack_signed_int,                                         \
      signed long: lip_pack_signed_long,                                       \
      signed long long: lip_pack_signed_long_long,                             \
      unsigned char: lip_pack_unsigned_char,                                   \
      unsigned short: lip_pack_unsigned_short,                                 \
      unsigned int: lip_pack_unsigned_int,                                     \
      unsigned long: lip_pack_unsigned_long,                                   \
      unsigned long long: lip_pack_unsigned_long_long))(buffer, data)

#define lip_unpack_int(buffer, data)                                           \
  _Generic((data),                                                             \
      int8_t *: lip_unpack_i8,                                                 \
      int16_t *: lip_unpack_i16,                                               \
      int32_t *: lip_unpack_i32,                                               \
      int64_t *: lip_unpack_i64,                                               \
      uint8_t *: lip_unpack_u8,                                                \
      uint16_t *: lip_unpack_u16,                                              \
      uint32_t *: lip_unpack_u32,                                              \
      uint64_t *: lip_unpack_u64,                                              \
      default: _Generic((data),                                                \
      signed char *: lip_unpack_signed_char,                                   \
      signed short *: lip_unpack_signed_short,                                 \
      signed int *: lip_unpack_signed_int,                                     \
      signed long *: lip_unpack_signed_long,                                   \
      signed long long *: lip_unpack_signed_long_long,                         \
      unsigned char *: lip_unpack_unsigned_char,                               \
      unsigned short *: lip_unpack_unsigned_short,                             \
      unsigned int *: lip_unpack_unsigned_int,                                 \
      unsigned long *: lip_unpack_unsigned_long,                               \
      unsigned long long *: lip_unpack_unsigned_long_long))(buffer, data)

#define lip_pack_float(buffer, data)                                           \
  _Generic((data), float: lip_pack_f32, double: lip_pack_f64)(buffer, data)

#define lip_unpack_float(buffer, data)                                         \
  _Generic((data), float *: lip_unpack_f32, double *: lip_unpack_f64)(buffer,  \
                                                                      data)

#endif
