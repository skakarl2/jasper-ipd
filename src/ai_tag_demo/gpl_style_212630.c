/* uniq -- remove duplicate lines from a sorted file
   Copyright (C) 1986-2023 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* Written by Richard M. Stallman and David MacKenzie.  */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <ctype.h>
#include <errno.h>
#include <stdbool.h>

#define PROGRAM_NAME "uniq"
#define AUTHORS "Richard M. Stallman", "David MacKenzie"

/* The number of fields to skip before checking for uniqueness.  */
static size_t skip_fields;

/* The number of chars to skip after skipping any fields.  */
static size_t skip_chars;

/* Number of chars to compare; 0 => all.  */
static size_t check_chars;

enum countmode
{
  count_occurrences,       /* -c  Print the number of times a line occurred.  */
  count_none               /* Default.  Don't print counts.  */
};

/* Whether and how to precede lines with counts.  */
static enum countmode countmode;

enum delimit_method
{
  DM_NONE,       /* No delimiter output.  */
  DM_PREPEND,    /* Delimit with a newline before each group.  */
  DM_SEPARATE    /* Delimit with a newline between groups.  */
};

/* Which lines to output.  */
static enum
{
  output_unique,           /* -u  Only lines that are not repeated.  */
  output_first_repeated,   /* -d  Only the first copy of repeated lines.  */
  output_all_repeated,     /* -D  All copies of repeated lines.  */
  output_all               /* Default.  Print first copy of each line.  */
} output_option;

/* If true, ignore case when comparing.  */
static bool ignore_case;

/* A linked list node for buffering input lines.  */
struct linebuffer
{
  char *buffer;
  size_t length;
  size_t alloc;
  struct linebuffer *next;
};

static struct option const long_options[] =
{
  {"count", no_argument, NULL, 'c'},
  {"repeated", no_argument, NULL, 'd'},
  {"all-repeated", optional_argument, NULL, 'D'},
  {"ignore-case", no_argument, NULL, 'i'},
  {"unique", no_argument, NULL, 'u'},
  {"skip-fields", required_argument, NULL, 'f'},
  {"skip-chars", required_argument, NULL, 's'},
  {"check-chars", required_argument, NULL, 'w'},
  {"help", no_argument, NULL, 'h'},
  {"version", no_argument, NULL, 'V'},
  {NULL, 0, NULL, 0}
};

static void
usage (int status)
{
  if (status != EXIT_SUCCESS)
    fprintf (stderr, "Try '%s --help' for more information.\n", PROGRAM_NAME);
  else
    {
      printf ("Usage: %s [OPTION]... [INPUT [OUTPUT]]\n", PROGRAM_NAME);
      fputs ("\
Filter adjacent matching lines from INPUT (or standard input),\n\
writing to OUTPUT (or standard output).\n\
\n\
With no options, matching lines are merged to the first occurrence.\n\
", stdout);
      fputs ("\
\n\
Mandatory arguments to long options are mandatory for short options too.\n\
", stdout);
      fputs ("\
  -c, --count           prefix lines by the number of occurrences\n\
  -d, --repeated        only print duplicate lines, one for each group\n\
  -D                    print all duplicate lines\n\
      --all-repeated[=METHOD]  like -D, but allow separating groups\n\
                                 with an empty line;\n\
                                 METHOD={none(default),prepend,separate}\n\
  -f, --skip-fields=N   avoid comparing the first N fields\n\
  -i, --ignore-case     ignore differences in case when comparing\n\
  -s, --skip-chars=N    avoid comparing the first N characters\n\
  -u, --unique          only print unique lines\n\
  -w, --check-chars=N   compare no more than N characters in lines\n\
      --help     display this help and exit\n\
      --version  output version information and exit\n\
", stdout);
      fputs ("\
\n\
A field is a run of blanks (usually spaces and/or TABs), then non-blank\n\
characters.  Fields are skipped before chars.\n\
", stdout);
      fputs ("\
\n\
Note: 'uniq' does not detect repeated lines unless they are adjacent.\n\
You may want to sort the input first, or use 'sort -u' without 'uniq'.\n\
", stdout);
    }

  exit (status);
}

/* Allocate and initialize a new linebuffer node.  */
static struct linebuffer *
linebuffer_alloc (void)
{
  struct linebuffer *lb = malloc (sizeof *lb);
  if (!lb)
    {
      fprintf (stderr, "%s: memory exhausted\n", PROGRAM_NAME);
      exit (EXIT_FAILURE);
    }
  lb->alloc = 256;
  lb->buffer = malloc (lb->alloc);
  if (!lb->buffer)
    {
      fprintf (stderr, "%s: memory exhausted\n", PROGRAM_NAME);
      exit (EXIT_FAILURE);
    }
  lb->length = 0;
  lb->next = NULL;
  return lb;
}

/* Free a single linebuffer node.  */
static void
linebuffer_free (struct linebuffer *lb)
{
  free (lb->buffer);
  free (lb);
}

/* Free a linked list of linebuffer nodes.  */
static void
linebuffer_free_list (struct linebuffer *head)
{
  while (head)
    {
      struct linebuffer *next = head->next;
      linebuffer_free (head);
      head = next;
    }
}

/* Read one line from FP into LB, expanding the buffer as needed.
   Return true if a line was read, false on EOF.  The newline is
   stored in the buffer if present.  */
static bool
readlinebuffer (struct linebuffer *lb, FILE *fp)
{
  int c;
  size_t i = 0;

  while ((c = getc (fp)) != EOF)
    {
      if (i >= lb->alloc)
        {
          lb->alloc *= 2;
          lb->buffer = realloc (lb->buffer, lb->alloc);
          if (!lb->buffer)
            {
              fprintf (stderr, "%s: memory exhausted\n", PROGRAM_NAME);
              exit (EXIT_FAILURE);
            }
        }
      lb->buffer[i++] = (char) c;
      if (c == '\n')
        break;
    }

  lb->length = i;
  return (i > 0);
}

/* Given a linebuffer LB, return a pointer into the buffer that
   skips over the first SKIP_FIELDS fields and then SKIP_CHARS
   characters.  Set *LEN to the remaining length for comparison.  */
static char *
find_field (const struct linebuffer *lb, size_t *len)
{
  size_t count;
  char *lp = lb->buffer;
  size_t length = lb->length;
  size_t i = 0;

  for (count = 0; count < skip_fields && i < length; count++)
    {
      while (i < length && isblank ((unsigned char) lp[i]))
        i++;
      while (i < length && !isblank ((unsigned char) lp[i]))
        i++;
    }

  i += skip_chars;
  if (i >= length)
    {
      *len = 0;
      return lp + length;
    }

  *len = length - i;
  if (check_chars && check_chars < *len)
    *len = check_chars;

  return lp + i;
}

/* Return true if the lines in LB1 and LB2 are equal according to the
   current skip/check/ignore settings.  */
static bool
lines_equal (const struct linebuffer *lb1, const struct linebuffer *lb2)
{
  size_t len1, len2;
  char *str1 = find_field (lb1, &len1);
  char *str2 = find_field (lb2, &len2);

  if (len1 != len2)
    return false;

  if (ignore_case)
    {
      for (size_t i = 0; i < len1; i++)
        {
          if (tolower ((unsigned char) str1[i])
              != tolower ((unsigned char) str2[i]))
            return false;
        }
      return true;
    }

  return memcmp (str1, str2, len1) == 0;
}

/* Write the line in LB to the output stream, optionally preceded by
   a count.  */
static void
writeline (const struct linebuffer *lb, FILE *out, size_t match_count)
{
  if (countmode == count_occurrences)
    fprintf (out, "%7zu ", match_count + 1);

  fwrite (lb->buffer, sizeof (char), lb->length, out);
}

/* Process the input stream, filtering adjacent duplicates.
   Uses a linked list to buffer groups of identical lines when
   output_all_repeated is selected.  */
static void
check_file (FILE *in, FILE *out)
{
  struct linebuffer *prevline;
  struct linebuffer *thisline;
  struct linebuffer *group_head = NULL;
  bool first_group = true;

  prevline = linebuffer_alloc ();
  thisline = linebuffer_alloc ();

  if (!readlinebuffer (prevline, in))
    {
      linebuffer_free (prevline);
      linebuffer_free (thisline);
      return;
    }

  size_t match_count = 0;

  while (readlinebuffer (thisline, in))
    {
      bool match = lines_equal (thisline, prevline);

      if (match)
        {
          match_count++;

          if (output_option == output_all_repeated)
            {
              /* Append to linked list of matching lines.  */
              struct linebuffer *node = linebuffer_alloc ();
              node->length = thisline->length;
              if (thisline->length > node->alloc)
                {
                  node->alloc = thisline->length;
                  node->buffer = realloc (node->buffer, node->alloc);
                }
              memcpy (node->buffer, thisline->buffer, thisline->length);
              node->next = NULL;

              if (!group_head)
                {
                  group_head = linebuffer_alloc ();
                  group_head->length = prevline->length;
                  if (prevline->length > group_head->alloc)
                    {
                      group_head->alloc = prevline->length;
                      group_head->buffer = realloc (group_head->buffer,
                                                    group_head->alloc);
                    }
                  memcpy (group_head->buffer, prevline->buffer,
                          prevline->length);
                  group_head->next = node;
                }
              else
                {
                  /* Find end of list and append.  */
                  struct linebuffer *tail = group_head;
                  while (tail->next)
                    tail = tail->next;
                  tail->next = node;
                }
            }
        }
      else
        {
          /* Lines differ.  Output the previous group as appropriate.  */
          if (output_option == output_all_repeated)
            {
              if (group_head)
                {
                  if (!first_group)
                    fputc ('\n', out);
                  first_group = false;

                  for (struct linebuffer *p = group_head; p; p = p->next)
                    writeline (p, out, match_count);

                  linebuffer_free_list (group_head);
                  group_head = NULL;
                }
            }
          else if (output_option == output_unique)
            {
              if (match_count == 0)
                writeline (prevline, out, match_count);
            }
          else if (output_option == output_first_repeated)
            {
              if (match_count > 0)
                writeline (prevline, out, match_count);
            }
          else  /* output_all -- the default.  */
            {
              writeline (prevline, out, match_count);
            }

          match_count = 0;

          /* Swap buffers: prevline takes thisline's content.  */
          struct linebuffer *tmp = prevline;
          prevline = thisline;
          thisline = tmp;
          thisline->length = 0;
        }
    }

  /* Handle the last group.  */
  if (output_option == output_all_repeated)
    {
      if (group_head)
        {
          if (!first_group)
            fputc ('\n', out);

          for (struct linebuffer *p = group_head; p; p = p->next)
            writeline (p, out, match_count);

          linebuffer_free_list (group_head);
        }
      else if (match_count > 0)
        {
          /* Only two lines total and they matched; group_head was built.  */
        }
    }
  else if (output_option == output_unique)
    {
      if (match_count == 0)
        writeline (prevline, out, match_count);
    }
  else if (output_option == output_first_repeated)
    {
      if (match_count > 0)
        writeline (prevline, out, match_count);
    }
  else
    {
      writeline (prevline, out, match_count);
    }

  linebuffer_free (prevline);
  linebuffer_free (thisline);
}

int
main (int argc, char **argv)
{
  int optc;
  FILE *in = stdin;
  FILE *out = stdout;

  skip_fields = 0;
  skip_chars = 0;
  check_chars = 0;
  output_option = output_all;
  countmode = count_none;
  ignore_case = false;

  while ((optc = getopt_long (argc, argv, "cdDf:is:uw:", long_options, NULL))
         != -1)
    {
      switch (optc)
        {
        case 'c':
          countmode = count_occurrences;
          break;

        case 'd':
          output_option = output_first_repeated;
          break;

        case 'D':
          output_option = output_all_repeated;
          break;

        case 'f':
          skip_fields = strtoul (optarg, NULL, 10);
          break;

        case 'i':
          ignore_case = true;
          break;

        case 's':
          skip_chars = strtoul (optarg, NULL, 10);
          break;

        case 'u':
          output_option = output_unique;
          break;

        case 'w':
          check_chars = strtoul (optarg, NULL, 10);
          break;

        case 'h':
          usage (EXIT_SUCCESS);
          break;

        case 'V':
          printf ("%s (GNU coreutils) 9.4\n", PROGRAM_NAME);
          fputs ("\
Copyright (C) 2023 Free Software Foundation, Inc.\n\
License GPLv3+: GNU GPL version 3 or later"
                 " <https://gnu.org/licenses/gpl.html>.\n\
This is free software: you are free to change and redistribute it.\n\
There is NO WARRANTY, to the extent permitted by law.\n\
", stdout);
          printf ("\nWritten by %s and %s.\n", AUTHORS);
          exit (EXIT_SUCCESS);
          break;

        default:
          usage (EXIT_FAILURE);
          break;
        }
    }

  /* Handle optional positional arguments: [INPUT [OUTPUT]].  */
  if (optind < argc && strcmp (argv[optind], "-") != 0)
    {
      in = fopen (argv[optind], "r");
      if (!in)
        {
          fprintf (stderr, "%s: %s: %s\n", PROGRAM_NAME, argv[optind],
                   strerror (errno));
          exit (EXIT_FAILURE);
        }
    }
  optind++;

  if (optind < argc)
    {
      out = fopen (argv[optind], "w");
      if (!out)
        {
          fprintf (stderr, "%s: %s: %s\n", PROGRAM_NAME, argv[optind],
                   strerror (errno));
          exit (EXIT_FAILURE);
        }
    }
  optind++;

  if (optind < argc)
    {
      fprintf (stderr, "%s: extra operand '%s'\n", PROGRAM_NAME,
               argv[optind]);
      usage (EXIT_FAILURE);
    }

  check_file (in, out);

  if (in != stdin)
    fclose (in);
  if (out != stdout)
    fclose (out);

  return EXIT_SUCCESS;
}
