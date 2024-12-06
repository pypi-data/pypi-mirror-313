#ifndef LIO_H
#define LIO_H

#include "lite_pack.h"

#define LIO_BUFFER_SIZE 0x40000
#define LIO_HEADER_SIZE 9

struct lio_writer
{
  int fd;
  unsigned char buffer[LIO_BUFFER_SIZE];
  size_t backlog;
  size_t allocated;
};

struct lio_reader
{
  int fd;
  unsigned char buffer[LIO_BUFFER_SIZE];
  unsigned char invalid_buffer[1];
  size_t head;
  size_t tail;
  int _feof;
};

void           lio_wsetup(struct lio_writer *, int fd);
unsigned char *lio_alloc(struct lio_writer *);
int            lio_write(struct lio_writer *, size_t size);
int            lio_writeb(struct lio_writer *, size_t size, void const *data);
int            lio_flush(struct lio_writer *);
int            lio_wfile(struct lio_writer const *);
int            lio_wtell(struct lio_writer const *, long *offset);
int            lio_wseek(struct lio_writer *, long offset);
int            lio_wrewind(struct lio_writer *);

void           lio_rsetup(struct lio_reader *, int fd);
unsigned char *lio_read(struct lio_reader *);
int            lio_readb(struct lio_reader *, size_t size, unsigned char *data);
int            lio_free(struct lio_reader *, size_t size);
int            lio_eof(struct lio_reader const *);
int            lio_rfile(struct lio_reader const *);
int            lio_rtell(struct lio_reader const *, long *offset);
int            lio_rseek(struct lio_reader *, long offset);
int            lio_rrewind(struct lio_reader *);

#define lio_setup(x, fd)    _Generic((x), struct lio_writer *: lio_wsetup , struct lio_reader *: lio_rsetup) (x, fd)
#define lio_file(x)         _Generic((x), struct lio_writer *: lio_wfile  , struct lio_reader *: lio_rfile)  (x)
#define lio_tell(x, offset) _Generic((x), struct lio_writer *: lio_wtell  , struct lio_reader *: lio_rtell)  (x, offset)
#define lio_seek(x, offset) _Generic((x), struct lio_writer *: lio_wseek  , struct lio_reader *: lio_rseek)  (x, offset)
#define lio_rewind(x)       _Generic((x), struct lio_writer *: lio_wrewind, struct lio_reader *: lio_rrewind)(x)

#endif
