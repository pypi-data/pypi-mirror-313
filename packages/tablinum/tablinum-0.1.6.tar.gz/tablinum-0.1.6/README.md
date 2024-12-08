# Tablinum

Tablinum is a Python library to make, manipulate, and neatly print tabular output to the console.

[![PyPI - Version](https://img.shields.io/pypi/v/tablinum.svg)](https://pypi.org/project/tablinum)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tablinum.svg)](https://pypi.org/project/tablinum)

-----

**Table of Contents**

- [Introduction](#introduction)
- [Usage modes and installation](#usage-modes-and-installation)
- [Special rows](#special-rows)
- [Verbs in the DSL](#verbs-in-the-dsl)
- [What counts as a number?](#what-counts-as-a-number?)
- [Methods available for a Table object](#methods-available-for-a-table-object)
- [License](#license)


## Introduction

Tablinum is an exportable module that will line up tabular material automatically,
and so save you hours of time faffing about with format and alignment.  As a script
it provides a filter with a simple DSL (domain-specific language) that can be used
to make and manipulate tables in editors that support external filters (such as
Vim).

If your work involves editing lots of plain text you will get familiar with a
plain text editor such as Vim or Emacs or similar. You will get familiar with
the facilities for arranging code and paragraphs of plain text.  Eventually you
will need to create a table of data or other information, something like this

    event  eruption  waiting
    A         3.600       79
    B         1.800       54
    C         3.333       74
    D         2.283       62
    E         4.533       85

You may find that your editor has some useful facilities for working in "block"
mode that help to manage the table, but you might also find that the facilities
are just a little bit limited.   For example, you might want to know the totals
of each column, but you really didn't want to load the data into a spreadsheet
or a statistics system like R; you just want the simple totals.   That's what
Tablinum for.  If you set it up in Vim (see below) as a user command, then
you can just say `:Table add` to get this:

    event  eruption  waiting
    A         3.600       79
    B         1.800       54
    C         3.333       74
    D         2.283       62
    E         4.533       85
    Total    15.549      354

Tablinum also lets you transpose your table, `:Table xp`, to get this...

    event         A      B      C      D      E
    eruption  3.600  1.800  3.333  2.283  4.533
    waiting      79     54     74     62     85

You can also sort by any column in the table, rearrange the columns, delete
columns, or add new columns computed from the others.  It can't do everything
you can do in a spreadsheet but it can do most of the simple things, and you
can use it right in the middle of your favourite editor.

Many of my Python scripts create tables of data that I need to share in plain
text (on Slack for example), and I often found myself loading the output into
Vim just so I could tidy it up with Tablinum.  So I have re-written my original
Perl `tabulate` script as a Python package that can be imported, and used to
tidy up a list of lists of data for printing directly as part of a script.

## Usage modes and installation

You can use Tablinum from the command line, from your editor, or as a Python module.
In each case, you use the same mini-language of verbs to act on your table.  This
mini-language is described in the next main section.

### Usage from the command line

The package provides a command line filter "entry point" called `tablinum_filter`.
This lets you get use Tablinum from the command line as a regular script.

If you are always working inside a Python virtual environment, you can install the library
and the script with:

```console
pip install tablinum
```

After successful installation you should be able to do `tablinum_filter --h` from within your
virtual environment, to get this:

    usage: tablinum_filter [-h] [--file FILE] [agenda [agenda ...]]

    positional arguments:
      agenda       [delimiter.maxsplit] [verb [option]]...

    optional arguments:
      -h, --help   show this help message and exit
      --file FILE  Source file name, defaults to STDIN

The script can be used with the DSL `gen` to generate data or to read from STDIN
or from an optional file path.

If you want the script part available globally, then you might prefer to install it using
[pipx](https://pipx.pypa.io/stable/installation/).  Once you have `pipx` available on your
system you should be able to do.

```console
pipx install tablinum
```

Then `tablinum_filter` should be available from any command line.

If you don't like typing such a long name, then you could try something
like `alias tbl=tablinum_filter`.

### Usage from within Vim

The Tablinum filter was originally written for use from Vim.  Originally all you
had to do was store the whole script locally and set up a command that pointed to it.
But now that it has grown into a proper Python package with an entry-point script, you
need to install it in your system and get it working on the command line before you
can use it in Vim.  It is theoretically possible to get Vim to work within an activated
Python virtual environment, but it is probably easier to use `pipx` as shown above.

So, once you have installed successfully and you can run `tablinum_filter` from the console
then you can use the same filter from within Vim, by adding a line to your `.vimrc`
file like this:

```vimscript
:command! -nargs=* -range=% Table <line1>,<line2>!tablinum_filter <q-args>
```

You can of course use some word other than `Table` as the command name. Perhaps
`Tbl` ?  Take your pick, you can choose anything, except that Vim insists on
the name starting with an uppercase letter.

With a definition like this, when you type `:Table` in normal mode in Vim, it
will pass the current buffer to the script and replace the contents with the
output.  If you are in Visual Line mode then the current buffer will just be
the marked lines.  If you are in Normal mode then the current buffer will be
the whole file.

    :Table [delimiter.maxsplit] [verb [option]]...

### Writing the agenda line

Whether you are calling Tablinum from Vim or the command line, the
parsing of your input is the same.

Use blanks to separate the arguments you type: the delimiter argument and any
verbs must be single blank-separated words.  Any word that looks like a verb
will be treated as a verb, even if you meant it to be an option.  See below for
details.  Options can in some cases contain blanks.

The delimiter is used to split up each input line into cells.  It can be any
single non-alphabetic character or a whole number between 0 and 9.  You can't use
blanks (even inside quotes) because of the simple way that I split up the
command line, and so I use whole numbers to mean `split on at least that many
consecutive blanks` so if you use 1 as an argument the line will be split on
every blank space, and so on. The default argument is 2.  This means the line
will be split at every occurrence of two or more blanks.  This is generally
what you want.  Consider this example.

    Item          Amount
    First label       23
    Second thing      45
    Third one         55
    Total            123

In most circumstances you can just leave the delimiter out and let it default
to two or more spaces.  Incidentally, any tab characters in your input are
silently converted to double spaces before parsing.

You can also limit the number of cell splits done by adding a second number to
a numeric delimiter.  So "1.3" will use one or more spaces as the delimiter,
but will only make 4 columns. This is often handy when parsing log files etc.

If you want to parse a regular CSV file, use "," as the delimiter.

After the optional delimiter you should specify a sequence of verbs.  If the
verb needs an option then that goes right after the verb.  Verbs and options
are separated by blanks.  The parsing is very simple.  If it looks like a verb
it's treated as one.  If it doesn't, it's assumed to be an option.  Anything
coming after an option, but not recognized as a verb, causes an error.  A
message will be written back in the file.  You will probably want to use the
`undo` function after reading it.

### Usage as a Python library

Tablinum can also be used from your own Python projects.  Assuming that you
are working in a virtual environment, then after you have activated it you can
just do
```console
pip install tablinum
```
to make the library available.  You might also add it to your `requirements.txt` file.

Once installed you can use the pacakge to parse and format lists of lists or lists
of strings.  Something like this

```python
import tablinum
data = [('Item', 'Amount'), ('First label', 23), ('Second thing', 45), ('Third one', 55)]
tt = tablinum.Table()
tt.parse_lol(data)
tt.do("rule add")
print(tt)
```

which should produce

```console
Item          Amount
First label       23
Second thing      45
Third one         55
--------------------
Total            123
```

`parse_lol` is expecting a list of lists (or list of iterables) as shown.  But
you can also use `tt.parse_lines(object_with_lines)` to read a file or a list of strings.

```python
tt.parse_lines(lines_thing, splitter=re.compile('\\s\\s+'), splits=0)
```

As shown, `parse_lines` takes two optional arguments:  a regex for splitting
and a maximum number of splits to make, where 0 means "as many as there are".
The defaults are as shown above -- split on two or more consecutive spaces, and
make as many splits as needed.

You can also add lines one at a time using the Table.append() method.  So the example
above could be done as
```python
import tablinum
data = [('Item', 'Amount'), ('First label', 23), ('Second thing', 45), ('Third one', 55)]
tt = tablinum.Table()
for row in data:
    tt.append(row)
tt.do("rule add")
print(tt)
```
The appended `row` is treated as an iterable. If you append a single string it will be
split up into letters following normal Python semantics.

The `do` method processes a list of verbs and options as described above.

The tabulate module overloads the `__str__` method, so that printing your Table object
will show it neatly tabulated.  If you want the individual lines, use the `tabulate()` method
to get a generator of neat lines.

See [below](#methods-available-for-a-table-object) for all the public methods provided by a `Table` object.

## Special rows

Any blank lines in your table are saved as special lines and reinserted at the
appropriate place on output. So if you have a long table you can use blanks to
separate blocks of data.  Similarly any lines consisting entirely of `-`
characters are treated as horizontal rules and reinserted (appropriately sized)
on output.  Any lines starting with `#` are treated as comment lines, and again
reinserted in the right places on output.

## Verbs in the DSL

If you do `help`, then tabulate will print "Try one of these:" followed by a list of
all the defined verbs.  Like this:

    Try one of these: add arr ditto dp dup filter gen group help label
    levels make noblanks nospace pivot pop push roll rule sf shuffle sort
    tap uniq unwrap unzip wrap xp zip

DSL = [Domain Specific Language](https://en.wikipedia.org/wiki/Domain-specific_language)

The following thematic tables summarize the ones you are likely to use most.
Then they are all described in more detail below, in alphabetical order.

**Re-arrange the columns**

- [xp](#xp---transpose-the-table) - transpose the table
- [arr](#arr---rearrange-the-columns) - rearrange the columns and/or calculate new columns
- [pivot](#pivot---expand-or-condense-data-tables) - expand or condense data tables
- [wrap](#wrap-and-unwrap---reshape-table-in-blocks) and unwrap - reshape table in blocks
- [zip](#zip-and-unzip---reshape-a-table-by-rows) and unzip - reshape a table by rows
- [roll](#roll---roll-the-values-in-one-or-more-columns) - roll the values in one or more columns

**Re-arrange or filter the rows**

- [sort](#sort---sort-on-column) - sort on column
- [group](#group---insert-special-blank-rows-between-different-values-in-given-column) - insert special blank rows between different values in given col
- [uniq](#uniq---filter-out-duplicated-rows) - filter out duplicated rows
- [filter](#filter---select-rows) - select rows
- [shuffle](#shuffle---rearrange-the-rows-with-a-Fisher-Yates-shuffle) - rearrange the rows with a Fisher-Yates shuffle.
- [ditto](#ditto---copy-down-from-cell-above) - copy down from cell above
- [gen](#gen---generate-new-rows) - generate new rows
- [pop](#pop---remove-a-row) - remove a row, by default the last
- [push](#push---restore-a-row) - put back the last row popped
- [clear](#clear---clear-all-rows) - remove all the rows

**Decorate or adjust the whole table**

- [add](#add---insert-the-sum-at-the-bottom-of-each-column) - insert the sum at the bottom of each column
- [dp](#dp---round-numbers-to-n-decimal-places) - round numbers to n decimal places
- [sf](#sf---round-numbers-to-given-significant-figures) - round numbers to n significant figures
- [label](#label---add-alphabetic-labels-to-all-the-columns) - add alphabetic labels to all the columns
- [make](#make---set-the-output-format) - set the output format
- [nospace](#nospace---remove-spaces-from-cell-values) - remove spaces from cell values
- [rule](#rule---add-a-rule) - add a rule
- [tap](#tap---apply-a-function-to-each-numerical-value) - apply a function to each numerical value

You can string together as many verbs (plus optional arguments) as you like.

### add - insert the sum at the bottom of each column

    add [sum|mean|median|q95|...]*

`add` adds the total to the foot of a column.  The default option is `sum`, but
it also can be any one or more methods from the Python3 `statistics` library:
`mean`, `median`, `mode`, `stdev`, `variance`, and so on, plus `q95` for the
95%-ile.  So given this:

    First   100
    Second  200
    Third   300

then `add` produces:

    First   100
    Second  200
    Third   300
    Total   600

If you would like to mark the total line with a rule above it, then do `rule add`
which will produce:

    First   100
    Second  200
    Third   300
    -----------
    Total   600

If you want to change the function, or if you have changed a value and you want
to update the total, then you need to get rid of the total line first.  There
is a slick way to do this.  Given a table like the one immediately above with a
total row, try `pop add mean`:

    First   100
    Second  200
    Third   300
    -----------
    Mean    200

The `pop` removes the last row before adding the new function.  You can use the
same trick if you change one or more of the values and want to update the
total.  Note that if you have already added the rule there is no need to add it
again.

If you want to see (say) both `min` and `max` then try `rule add min max`:

    First   100
    Second  200
    Third   300
    -----------
    Min     100
    Max     300

Note that non-numeric cells in a column are ignored, but if there are no numeric entries
at all in a column, then the value of the total is the name of the function.

### arr - rearrange the columns

    arr [arrange-expression]

#### Simple permutations

At it simplest `arr` lets you rearrange, duplicate, or delete columns.  So if you have a
four column table then:

- `arr dabc` puts the fourth column first
- `arr aabcd` duplicates the first column
- `arr cd` deletes the first two columns
- `arr abc` keeps only the first three columns

and so on.  Astute readers may spot a problem here.  The sequence `arr add`
meaning _delete cols b and c and duplicate col d_ won't work because `add` is a
valid verb.  In this case (as similar ones) just put a pair of empty braces on
the end, like so `arr add{}`.

There are shortcuts to save you typing lots of column letters:

- `arr ~a` will keep *all* the columns and then add a copy of the first one on the end.
- `arr -b` will remove column `b` but keep all the others
- `arr a..e` will keep only columns a, b, c, d, and e
- `arr abyz` will keep the first two and the last two columns (for tables with up to 22 columns)

If you are working in an editor, and  you want to do more complicated things
with lots of columns, you might find it easier to transpose the table first
with `xp` and then use the regular line editing facilities rearrange the rows,
before transposing them back to columns.

If you have trouble keeping track of which column is now (say) column `h`, then
you might like to use the `label` verb to add alphabetic labels to the top each
column before you start.

Besides letters to identify column values you can use `?` to insert a random number.

Note that you should use lower case letters only to refer to each column value.
If you use an upper case letter, `A`, `B`, etc, it will be replaced by the
cumulative sum of the corresponding column, in other words the sum of the
values in the column from the top of the table to the current row. So given

    First   1
    Second  2
    Third   3

`arr abB` gives you,

    First   1  1
    Second  2  3
    Third   3  6

Finally note that while tabulate supports tables with as many columns as
you like, the `arr` verb will only let you manipulate the first 26 because
there are only 26 characters in `string.ascii_lowercase`.  If you need to
manipulate more columns, you should transpose your table with `xp` and
work on the rows.

#### Rearrangement with calculated columns

The `arr` verb also lets you insert arbitrary calculated columns by putting an
expression in curly braces or parentheses:

- `arr ab(a+b)` adds a new column that contains the sum of the values in the first two

- `arr a(a**2)(sqrt(a))` adds two new cols with square and square root of the value in col 1.

- `arr ~{sqrt(a)}` keeps all existing cols and adds a new col with the square root of the value in col 1.

and so on.  Each single letter `a`, `b`, etc is changed into the corresponding
cell value and then the resulting expression is evaluated.  An expression can also be
a constant.  So `arr ~(1)` will add a column of 1s to the table.

As shown above, you can use a subset of the normal built-in or `math` functions
such as `log` and `sqrt`, but the access to Python is not entirely general, as
it is only intended for simple manipulation of a few values, and therefore the
library tries quite hard to prevent you accidentally loading the `sys` module
and deleting the contents of your file system.

Only the following names of functions are allowed in a calculation.

- maths functions: `abs cos cosd divmod exp floor hypot log log10 pow round sin sind sqrt tan tand`
- integer functions: `gcd lcm comb perm`  (inputs are truncated to integer values) 
- number conversion: `bool chr hex int oct ord str`
- maths constants: `pi tau`
- string functions: `caps lower upper reversed len` - see below
- date functions: `base date dow epoch hms hr mins secs` - see below
- list functions: `all any max min sorted sum`

The list functions are enhanced so you can call them with a tuple or a list of
arguments.  If a function returns more than one value (like `divmod`) the
values will be inserted in separate columns. The others are the regular BIF or
`math` functions except for the trig functions for angles in degrees.
In some cases the inputs are truncated to integer values, where the
standard function expects integers.

The expression should be a valid Python expression, but there are a couple of
useful additions:  borrowing from Metapost, you can write `2a` instead of
`2*a`, and `3++4` instead of `hypot(3,4)`.  You can also write `a mod b`
instead of `a%b`, and `a<>b` instead of `a!=b`; these two make it easier to use
the filter with Vim or any other editor that gives `%` and `!` a special
meaning on the command line. You can also use "?" in a formula to get a uniform
random number between 0 and 1.

If you want the current row number or the total number of rows use the
pre-defined variables `row_number` and `rows` in your formula. So with the
simple table from above, `arr ~(f'{row_number}/{rows}')` should produce this:

    First   1  1  1/3
    Second  2  3  2/3
    Third   3  6  3/3

You can also use simple `format` and `f''` strings. And string slices or indexes.  So

    arr (a[:2])

would give you the first two characters of the strings in column a.  This only works
with values that are strings of course, but this

    arr (str(a)[:2])

should work with numbers as well.

Curly braces are only treated as parentheses at the top level (and this only for compatibility
with the old Perl version of tabulate), so you can put them in normal Python expressions like

    arr ab('{} {}'.format(c, d))

or

    arr ab(f"{c} {d}")

which show how to concatenate two columns into one.  You can also include
spaces in your formula as the argument to `arr` continues to the next verb or
the end of the command line.  Beware that because tablinum restricts the functions
available in a formula, some fancy f-strings might not work.  Also beware that
tablinum treats all numbers as decimal.Decimal objects, and that therefore the Python
`d` suffix does not work.   So if you have this table:

Year  Month  Day  Saint
2023      1    2  Basil the Great
2023      7   15  Swithun
2023     11   18  Elizabeth of Hungary

and you want to make a proper date column with zero filled months and days, you
might try this: `arr (f'{a}-{b:02d}-{c:02d}')d`  but that will cause an error.
The solution is to leave out the suffixes and rely on the defaults.

So this: `arr (f'{a}-{b:02}-{c:02}')d` works correctly.

Year-Month-Day  Saint
2023-01-02      Basil the Great
2023-07-15      Swithun
2023-11-18      Elizabeth of Hungary

There are also three functions for changing the case of a string column, so given:

    Crosby   crines   hobbies  sola
    Juno     aril     horn     culicid
    Krishna  parched  debouch  moutan
    Lille    gowd     medius   tanrec

the DSL `arr (lower(a))(upper(b))(caps(c)+caps(d))` gives you:

    crosby   CRINES   HobbiesSola
    juno     ARIL     HornCulicid
    krishna  PARCHED  DebouchMoutan
    lille    GOWD     MediusTanrec

and `arr (reversed(a))bc(len(c))` would give you:

    ybsorc   CRINES   HobbiesSola    11
    onuj     ARIL     HornCulicid    11
    anhsirk  PARCHED  DebouchMoutan  13
    ellil    GOWD     MediusTanrec   12

There are also some simple date routines included.

- `base` returns an integer representing the number of days since 1 Jan in the
  year 1 (assuming the Gregorian calendar extended backwards).  The argument
  should be blank for today, or some recognisable form of a date.  So you can
  parse most common date strings.  The default is None, so that you should have
  `base() == datetime.date.today().toordinal()`

- `date` does the opposite: given a number that represents the number of days
  since the year dot, it returns the date in `yyyy-mm-dd` form.  However see below
  for special cases of small and large values.

- `dow` which takes a date and returns the day of the week, as a three letter
  string.

So given a table with a column of dates, like this

    2011-01-17
    2011-02-23
    2011-03-19
    2011-07-05

The command `arr a{dow(a)}` creates this

    2011-01-17  Mon
    2011-02-23  Wed
    2011-03-19  Sat
    2011-07-05  Tue

Alternatively `arr a{base()-base(a)}` will produce the days from each date to today.

    2011-01-17  4720
    2011-02-23  4683
    2011-03-19  4659
    2011-07-05  4551

And `arr a{date(base(a)+140)}` will add 20 weeks to each date

    2011-01-17  2011-06-06
    2011-02-23  2011-07-13
    2011-03-19  2011-08-06

As a convenience `date()` supports some special ranges of values.

- If the abs value of the number is less than 1000, then it's assumed that you
  mean a delta on today.  So `date(70)` will produce the date in 10 weeks time,
  and `date(-91)` will give you the date three months ago, and so on.

- `date(0)` or just `date()` produces today's date.

- If the number is larger than `datetime.date.max.toordinal`, then the number
  will be interpreted as epoch seconds, and if it is very large, epoch milliseconds.

Note: `base()` will actually recognize dates in several different (mainly ISO
or British) forms as well as `yyyy-mm-dd`, as follows:

    Example                   strftime format used
    ----------------------------------------------
    2020-12-25                %Y-%m-%d
    20201225                  %Y%m%d
    2020-W52-5                %G-W%V-%u
    Fri Dec 25 12:34:56 2020  %c
    12/25/20                  %x
    25 December 2020          %d %B %Y
    25 Dec 2020               %d %b %Y
    25 Dec 20                 %d %b %y
    25 December 20            %d %B %y
    25/12/2020                %d/%m/%Y
    25/12/20                  %d/%m/%y
    15-dec-2020               %d-%b-%Y
    Friday                    %A

This table shows the strftime formats used.  This is not as clever as using
`dateutil.parser` but it does mean that the package only uses the standard Python3
libraries.  Note that for the last one, you would get the date of next Friday,
so `date(base('Monday'))` will give you the date of next Monday in ISO format.

If you want to convert a date in column `a` from any of these formats to
standard ISO format then do `date(base(a))`.

If you want something other than ISO date format, then `date()` takes an optional
second argument that can be any strftime code.  So given the table from above

    2011-01-17
    2011-02-23
    2011-03-19
    2011-07-05

then `arr a{date(a, "%G-W%V-%u")}` will produce this:

    2011-01-17  2011-W03-1
    2011-02-23  2011-W08-3
    2011-03-19  2011-W11-6
    2011-07-05  2011-W27-2

There are also a few useful functions to convert HH:MM:SS to fractional hours,
minutes or seconds.  `hms()` takes fractional hours and produces `hh:mm:ss`,
while `hr`, `mins`, and `secs` go the other way.

Plus `epoch()` that will convert a full date-time timestamp to epoch seconds.


### clear - remove all rows

   clear

This verb removes all the rows.  This is useful before you create more data with `gen`.
For example `clear gen 16 shuffle wrap 4` gives you a new randomized 4x4 grid of numbers.

### ditto - copy down from cell above

    ditto [marker]

This verb helps you create a regular table from headings and lists.  It is only really useful from within an editor.
Given input like this (note the double spaces after the - marker).

    First group
    -  one thing
    -  another thing
    Second group
    -  something else
    -  more of it

then `ditto -` will produce:

    First group
    First group   one thing
    First group   another thing
    Second group
    Second group  something else
    Second group  more of it

The default marker is the " character, hence the name of the verb.

### dp - round numbers to n decimal places

    dp [nnnnn...]

As delivered, tabulate calculates with 12 decimal places, so you might need to round your answers a bit.
This is what `dp` does.  The required argument is a string of digits indicating how many decimal places
between 0 and 9 you want for each column.  There's no default, it just does nothing with no argument, but
if your string is too short the last digit is repeated as necessary.  So to round everything to a whole number
do `dp 0`.  To round the first col to 0, the second to 3 and the rest to 4 do `dp 034`, and so on.
Cells that contain values that are not numbers are not changed, so given this table

    Category         Type A         Type B
    --------------------------------------
    First     6.94119005507  6.92853781816
    Second    6.96413561242  6.97728134163

applying `dp 4` should produce

    Category  Type A  Type B
    ------------------------
    First     6.9412  6.9285
    Second    6.9641  6.9773


### filter - select rows

    filter [expression]

This verb selects rows where "expression" is True.  In long tables it is
sometimes useful to pick out only some of the rows.  You can do this with
`filter`.   Say you have a table of rainfall data like this:

    Monday      Week  Mon  Tue   Wed  Thu  Fri   Sat   Sun  Total
    2019-12-30     1  0.0  0.2   0.0  0.0  1.2   0.0   0.0    1.4
    2020-01-06     2  0.5  0.0   0.0  6.4  0.0   0.1   1.7    8.7
    2020-01-13     3  5.3  1.7   9.1  3.0  1.7   0.0   0.0   20.8
    2020-01-20     4  0.0  0.0   0.0  0.0  0.0   0.1   2.3    2.4
    2020-01-27     5  8.4  2.1   0.0  0.5  1.0   0.0   7.1   19.1
    2020-02-03     6  0.1  0.0   0.0  0.0  0.0   1.5  10.6   12.2
    2020-02-10     7  5.5  0.0   0.5  6.6  0.0   4.9  15.6   33.1
    2020-02-17     8  0.2  3.3   1.0  3.8  0.0   0.5   1.0    9.8
    2020-02-24     9  6.1  0.5   0.1  8.6  5.9   7.1   0.2   28.5
    2020-03-02    10  0.0  0.0   4.3  0.0  3.0  12.4   0.0   19.7
    2020-03-09    11  0.0  4.3   6.3  1.3  1.0   1.0   0.0   13.9
    2020-03-16    12  3.6  1.3   0.0  0.0  0.0   0.5   0.0    5.4
    2020-03-23    13  0.0  0.0   0.0  0.0  0.0   0.0   0.0    0.0
    2020-03-30    14  0.1  0.1  10.9  0.0  0.0   0.0   0.0   11.1

and you want only to keep the rows where the Total value is greater than 10, then you
can try `filter j>10` to get

    Monday      Week  Mon  Tue   Wed  Thu  Fri   Sat   Sun  Total
    2020-01-13     3  5.3  1.7   9.1  3.0  1.7   0.0   0.0   20.8
    2020-01-27     5  8.4  2.1   0.0  0.5  1.0   0.0   7.1   19.1
    2020-02-03     6  0.1  0.0   0.0  0.0  0.0   1.5  10.6   12.2
    2020-02-10     7  5.5  0.0   0.5  6.6  0.0   4.9  15.6   33.1
    2020-02-24     9  6.1  0.5   0.1  8.6  5.9   7.1   0.2   28.5
    2020-03-02    10  0.0  0.0   4.3  0.0  3.0  12.4   0.0   19.7
    2020-03-09    11  0.0  4.3   6.3  1.3  1.0   1.0   0.0   13.9
    2020-03-30    14  0.1  0.1  10.9  0.0  0.0   0.0   0.0   11.1

Notice that the header row was included.  If the expression causes an error (in
this case because you can't compare a string to a number) then the row will
always be included.  But if you had done `filter i=0` you would get

    2019-12-30   1  0.0  0.2   0.0  0.0  1.2   0.0  0.0   1.4
    2020-01-13   3  5.3  1.7   9.1  3.0  1.7   0.0  0.0  20.8
    2020-03-02  10  0.0  0.0   4.3  0.0  3.0  12.4  0.0  19.7
    2020-03-09  11  0.0  4.3   6.3  1.3  1.0   1.0  0.0  13.9
    2020-03-16  12  3.6  1.3   0.0  0.0  0.0   0.5  0.0   5.4
    2020-03-23  13  0.0  0.0   0.0  0.0  0.0   0.0  0.0   0.0
    2020-03-30  14  0.1  0.1  10.9  0.0  0.0   0.0  0.0  11.1

because "Sun" is not equal to 0.  In cases like this you could do
`pop 0 filter i=0 push 0` to keep the header, or as a short cut you can do
`filter @i=0` which does the same:

    Monday      Week  Mon  Tue   Wed  Thu  Fri   Sat  Sun  Total
    2019-12-30     1  0.0  0.2   0.0  0.0  1.2   0.0  0.0    1.4
    2020-01-13     3  5.3  1.7   9.1  3.0  1.7   0.0  0.0   20.8
    2020-03-02    10  0.0  0.0   4.3  0.0  3.0  12.4  0.0   19.7
    2020-03-09    11  0.0  4.3   6.3  1.3  1.0   1.0  0.0   13.9
    2020-03-16    12  3.6  1.3   0.0  0.0  0.0   0.5  0.0    5.4
    2020-03-23    13  0.0  0.0   0.0  0.0  0.0   0.0  0.0    0.0
    2020-03-30    14  0.1  0.1  10.9  0.0  0.0   0.0  0.0   11.1

The expressions should be valid bits of Python, with the exceptions noted
below.  You  can use the same subset of built-in and maths functions as the
normal row arrangements with `arr`, and single letters refer to the value of
the cells in the way described for `arr` above.

Again like `arr` you can use the variables `rows` and `row_number` in the
expression: `rows` is the count of rows in your table, and `row_number` starts
at 1 and is incremented by 1 on successive rows.  You could use this to pick
out every other row: `filter row_number % 2`.

NB. If you are calling tabulate from the Vim command line, you need to escape
the `%` character, like so: `row_number \% 2`.  But you can also write
`row_number mod 2`. Similarly to avoid having to escape `!=` you can write `<>`
instead.  And if you write `a=b` it will be interpreted as `a==b` since
assignment makes no sense here.  Finally any undefined variable will be
interpreted as a string; this saves you typing the " marks.

The default action is to do nothing.


### gen - generate new rows

- `gen a..b` -- where `a` and `b` are integers will generate a table with a single
  column of integers running from `a` to `b`.   For example `gen 1..10`

- `gen a:b` -- is exactly the same, so you can write `gen 1:10` if you prefer.  In fact
  you can use any non-numeric string, for example `gen 1 -> 4` or just `gen 1 4`.

The numbers `a` and `b` can be negative.  If `a` is greater than `b`, the values are
reversed, so the new rows always run in ascending sequence.

- `gen n`  -- where `n` is a single integer without a range is interpreted as
  `gen 1:n`.  So `gen 10` is interpreted as `gen 1:10`.

If the table already has some data, then the single column will be appended as new rows at the bottom
of the existing column `a`.

To get more general new rows try `gen` with a pattern like `AB2`, which will produce:

    A  A
    A  B
    B  A
    B  B

or `gen PQR2`

    P  P
    P  Q
    P  R
    Q  P
    Q  Q
    Q  R
    R  P
    R  Q
    R  R

The argument should be a string of letters followed by a single digit.  The
digit controls the number of columns created, and all the required combinations
of letters in the string will be used to generate rows. Thus the number of new
rows generated will be the length of the letter-part raised to the power of the
single digit.  Hence `AB2` produces `2**2 = 4` rows, and `PQR2` produces `3**2 = 9`.
If you omit the digit, it will default to 1.

If you want to generate more complicated lists, you can combine `gen` with one or more
`arr` stages.  For example  `gen 1:4 arr (2a-1)` produces a list of odd numbers

    1
    3
    5
    7

Or how about a list of the dates of the next five Mondays?

    1  2024-04-22
    2  2024-04-29
    3  2024-05-06
    4  2024-05-13
    5  2024-05-20

For the above, try `gen 5 arr a(date(base('Monday')+7a))`

Or perhaps your next Lottery numbers?  Try `gen 6 arr (int(?*48+1)) sort wrap 6`

    3  11  19  21  30  46


### group - insert special blank rows between different values in given column

    group [col]

A bit like `group by` in SQL, `group` will add blank rows between different values
in the given column.  This works best if the table is sorted on the same column.
Given this:

    A  A  871  819
    A  B  934  319
    B  A  363  470
    B  B  121  219

Then `group a` would produce

    A  A  871  819
    A  B  934  319

    B  A  363  470
    B  B  121  219


### label - add alphabetic labels to all the columns

    label [name name ...]

`label` adds labels at the top of each column.  You can supply zero or more
names that you would like to use as single words separated by blanks.  The only
restriction is that you can't use any of the DSL verbs.  If you supply too many
the excess are just ignored, if you don't supply enough, then the labels
default to single letters of the alphabet.  This means that if you don't supply
any names, the columns will be labeled `a`, `b`, `c`, etc which might help you
work out which is which when rearranging.

If you want to replace the existing labels try

    pop 0 label [name name...]


### make - set the output format

    make [plain|pipe|tex|latex|csv|tsv]

`make` sets the output format.

- `plain` is the default, where each cell is separate by two or more spaces, and there is no EOL mark
- `pipe` will attempt to make a markdown table
- `tex` will use `&` to separate the cells and put `\cr` at the end
- `latex` is the same except the EOL is `\\`

Note that these last two only affect the rows, tabulate won't magically generate the TeX or LaTeX table preamble.

The `make csv` option should produce something that you can easily import into Excel
or similar spreadsheets.  The output is produced with the standard Python CSV writer,
so double quotes will be added around cell values where needed.

The `make tsv` option can be used when you want to import into Word -- you can
use Table... Convert Text to Table...  using tabs as the column separator.



### nospace - remove spaces from cell values

    nospace [filler]

This is useful for the `read.table` function in R, that by default treats all blanks including
single ones as delimiters.  Given this table

    Exposure category     Name            Value
    -------------------------------------------
    Asbestos exposure     Lung cancer         6
    Asbestos exposure     No lung cancer     51
    No asbestos exposure  Lung cancer        52
    No asbestos exposure  No lung cancer    941

the verb `nospace` will produce:

    ExposureCategory    Name          Value
    ---------------------------------------
    AsbestosExposure    LungCancer        6
    AsbestosExposure    NoLungCancer     51
    NoAsbestosExposure  LungCancer       52
    NoAsbestosExposure  NoLungCancer    941

Since that's a little hard to read unless you are a camel, you can also specify
an optional filler character, so `nospace .` would have produced this:

    Exposure.category     Name            Value
    -------------------------------------------
    Asbestos.exposure     Lung.cancer         6
    Asbestos.exposure     No.lung.cancer     51
    No.asbestos.exposure  Lung.cancer        52
    No.asbestos.exposure  No.lung.cancer    941

so that all spaces are replaced by periods.  Now you can read that into R
without an error.


### pivot - expand or condense data tables

    pivot [long|wide]

This is used to take a square table and make it a long one.  It's best explained with an example.

Consider the following table.

    Exposure category     Lung cancer  No lung cancer
    -------------------------------------------------
    Asbestos exposure               6              51
    No asbestos exposure           52             941

Nice and compact, but the values are in a 2x2 matrix rather than a useful column.  Sometimes you want
them to look like this, where each column is a variable and each row is an observation.

    Exposure category     Name            Value
    -------------------------------------------
    Asbestos exposure     Lung cancer         6
    Asbestos exposure     No lung cancer     51
    No asbestos exposure  Lung cancer        52
    No asbestos exposure  No lung cancer    941

And that's what `pivot long` does.  Here's another example.

    Region  Quarter  Sales
    ----------------------
    East    Q1        1200
    East    Q2        1100
    East    Q3        1500
    East    Q4        2200
    West    Q1        2200
    West    Q2        2500
    West    Q3        1990
    West    Q4        2600

With this input, `pivot wide` gives you this

    Region    Q1    Q2    Q3    Q4
    ------------------------------
    East    1200  1100  1500  2200
    West    2200  2500  1990  2600

Notice that parts of the headings may get lost in transposition.
Notice also that you *need* a heading of some sort, otherwise `pivot wide` will
mangle the first row of your data.  So you might like to use `label` before `pivot`.

The `pivot wide` function assumes that the right hand column contains numeric values
and the second-from-the-right column contains the names you want as new column headings.
Any non-numeric value in the values column is treated as 0.  If you have duplicate names
in the names column then the corresponding values will be added together.

The `pivot` function also allows for repeated rows.  So given this

    Region  Quarter  Sales
    ----------------------
    East    Q1        1200
    East    Q2        1100
    East    Q3        1500
    East    Q4        2200
    West    Q1        2200
    West    Q2        2500
    West    Q3        1990
    West    Q4         600
    West    Q4        1215
    East    Q4         640
    West    Q4         624

`pivot wide` would add up all the values to consolidate the data:

    Region    Q1    Q2    Q3    Q4
    ------------------------------
    East    1200  1100  1500  2840
    West    2200  2500  1990  2439

while `pivot count` would tell you how many of each type you had:

    Region  Q1  Q2  Q3  Q4
    ----------------------
    East     1   1   1   2
    West     1   1   1   3

and `pivot mean` would produce:

    Region    Q1    Q2    Q3    Q4
    ------------------------------
    East    1200  1100  1500  1420
    West    2200  2500  1990   813

You could also do `pivot wide pivot long` to eliminate the duplicates but leave the data
in long form.

    Region  Name  Value
    -------------------
    East    Q1     1200
    East    Q2     1100
    East    Q3     1500
    East    Q4     2840
    West    Q1     2200
    West    Q2     2500
    West    Q3     1990
    West    Q4     2439

Notice that this replaces the headers with Name and Value.  If you wanted to preserve the old headers
you could do `pop 0 label pivot wide pivot long push 1 pop 0`

    Region  Quarter  Sales
    ----------------------
    East    Q1        1200
    East    Q2        1100
    East    Q3        1500
    East    Q4        2840
    West    Q1        2200
    West    Q2        2500
    West    Q3        1990
    West    Q4        2439

### pop - remove a row

    pop [i]

This verb provides an equivalent of the normal Python3 list method `pop` for
the table.  By default `pop` removes the last row, but you can use it to remove
any row with the appropriate integer argument.  For the purposes of `pop` the
rows are zero indexed, so `pop 0` will remove the top row, and the usual
convention of negative indexes applies, so `pop -1` will remove the last.
Indexes that are too large are just ignored.

Obviously if you are using tabulate from an editor you could just delete the
row directly instead of use this command, but it is handy in certain idioms.
For example, to update a total row that you have created with `add` you can use
`pop add` so that the old total is removed and then replaced with a new one.

### push - restore a row

    push [i]

Any rows removed with `pop` are temporarily stored in each table object, and you
can put them back with `push`.  You can use this to move a row about, or to temporarily
exclude a row from some other operation.  So if you would like to keep your total row
at the bottom when you sort the table in reverse, you could do (say):

    pop sort A push

This removes the last row temporarily, sorts the table on column a in reverse, then
puts the last row back again.   Or again, if your header row does not automagically stay
at the top when you sort the table you can do

    pop 0 sort push 0

### roll - roll the values in one or more columns

    roll [col-list]

Roll like the stack on an HP RPN calculator.  So with a random table like this

     9   6  2   1
     8  14  3  15
     7  10  5  12
    16  11  4  13

the DSL `roll d` will produce the following

     9   6  2  13
     8  14  3   1
     7  10  5  15
    16  11  4  12

Upper case letters roll up, so `roll DD` will now produce

     9   6  2  15
     8  14  3  12
     7  10  5  13
    16  11  4   1

As with `sort` you can string column letters together.

One use of this is to calculate the differences between a series of timestamps,
so for example with a list of epoch milliseconds like this, how long was the
gap between each one?

    10099  1534951868290
    10070  1534951868808
    10091  1534951869177
    10085  1534951870335
    10085  1534951873005

You can find that with `arr abb roll c arr ab(b-c)` to get:

    10099  1534951868290  -4715
    10070  1534951868808    518
    10091  1534951869177    369
    10085  1534951870335   1158
    10085  1534951873005   2670

The negative number at the top shows you the difference between
the last and the first. (And hence the new column sums to zero).


### rule - add a rule

    rule [n]

Adds a rule after line `n` where the top line is line 1.  If `n` is larger than
the number of rows in the table, the rule will be added after the last line,
however it will not get shown when the table is tabulated unless you have added
more data by then.  To add a line just before the last line (to show a total or
a footer) use `rule -1`

### shuffle - rearrange the rows with a Fisher-Yates shuffle

    shuffle [colspec]

Shuffle the rows in the table.  This is implemented using `random.shuffle`.
Here's a one liner to generate a random 4x4 arrangement of the numbers 1 to 16:
(start with a blank file)

    gen 16 shuffle wrap 4

produces (for example):

     5   7   4   9
    13   2   3   8
    15   1   6  16
    12  11  10  14

You can also give a colspec, as for sort.  So `shuffle b` will randomize only the second column.
If you want to leave the top row alone, do `pop 0 shuffle push 0` or just `shuffle @`.

### sf - round numbers to given significant figures

    sf [sf-list]

This verb works like `dp` but instead of fixing the decimal places, it sets the number of
significant figures for each column to the corresponding figure in `sf-list`.  As with `dp` the
list of figures is extend as needed. So `sf 3` will adjust all columns to three sigfig, while
`sf 445` will adjust the first two columns to 4 figures, and the remaining columns to 5.
For example, given this:

    Name     a     b     c     d
    a      142    86    77    70
    b     1464   806   871   701
    c     5474  3352  3185  2964
    d     1281   860   790   722

the action `sf 04444` will produce

    Name      a      b      c      d
    a     142.0  86.00  77.00  70.00
    b      1464  806.0  871.0  701.0
    c      5474   3352   3185   2964
    d      1281  860.0  790.0  722.0

while `sf 02` produces

    Name     a     b     c     d
    a      140    86    77    70
    b     1500   810   870   700
    c     5500  3400  3200  3000
    d     1300   860   790   720

The most number of figures you can have is 9 in each column.  This is because if you do
`sf 10` it is interpreted as 1 for column one, and zero for all the others.

### sort - sort on column

    sort [a|b|c|...]

`sort` sorts the table on the given column.  `a` is the first, `b` the second, etc.
If you use upper case letters, `A`, `B`, etc the sort direction is reversed.
An index beyond the last column is automatically adjusted so `sort z` sorts on the last column
assuming you have fewer than 26 columns).

You can sort on a sequence of columns by just giving a longer string.
So `sort abc` is the same as `sort c sort b sort a` (but slightly quicker).

The default is to sort by all columns from right to left, but with some
built-in smarts: things that look like dates are treated as dates; "book
titles" ignore leading articles; and labels with numeric suffixes are sorted
properly. So given this table:

    20 Feb 2014  Social Darwinism               p5912
    27 Feb 2020  The Evolution of Horses        p233
    11 Feb 2016  Rumi's Poetry                  p7019
    24 Nov 2016  Baltic Crusades                p5060
    30 Sep 2021  The Tenant of Wildfell Hall    p780
    21 Sep 2017  Kant's Categorical Imperative  p265
    24 Sep 2020  Cave Art                       p904
    29 Oct 2015  The Empire of Mali             p423
    03 May 2018  The Almoravid Empire           p3972
    04 Feb 2016  Chromatography                 p11

`sort a` produces this

    20 Feb 2014  Social Darwinism               p5912
    29 Oct 2015  The Empire of Mali             p423
    04 Feb 2016  Chromatography                 p11
    11 Feb 2016  Rumi's Poetry                  p7019
    24 Nov 2016  Baltic Crusades                p5060
    21 Sep 2017  Kant's Categorical Imperative  p265
    03 May 2018  The Almoravid Empire           p3972
    27 Feb 2020  The Evolution of Horses        p233
    24 Sep 2020  Cave Art                       p904
    30 Sep 2021  The Tenant of Wildfell Hall    p780

`sort b` produces this

    03 May 2018  The Almoravid Empire           p3972
    24 Nov 2016  Baltic Crusades                p5060
    24 Sep 2020  Cave Art                       p904
    04 Feb 2016  Chromatography                 p11
    29 Oct 2015  The Empire of Mali             p423
    27 Feb 2020  The Evolution of Horses        p233
    21 Sep 2017  Kant's Categorical Imperative  p265
    11 Feb 2016  Rumi's Poetry                  p7019
    20 Feb 2014  Social Darwinism               p5912
    30 Sep 2021  The Tenant of Wildfell Hall    p780

and `sort c` produces this

    04 Feb 2016  Chromatography                 p11
    27 Feb 2020  The Evolution of Horses        p233
    21 Sep 2017  Kant's Categorical Imperative  p265
    29 Oct 2015  The Empire of Mali             p423
    30 Sep 2021  The Tenant of Wildfell Hall    p780
    24 Sep 2020  Cave Art                       p904
    03 May 2018  The Almoravid Empire           p3972
    24 Nov 2016  Baltic Crusades                p5060
    20 Feb 2014  Social Darwinism               p5912
    11 Feb 2016  Rumi's Poetry                  p7019

The smarts also recognize IP addresses, MAC addresses, and SI unit suffixes.
If the smarts get your sorting wrong, then you can turn them off by adding "="
to the front of the sort column specifier.  So you can do `sort =b` on the
table above to get this:

    24 Nov 2016  Baltic Crusades                p5060
    24 Sep 2020  Cave Art                       p904
    04 Feb 2016  Chromatography                 p11
    21 Sep 2017  Kant's Categorical Imperative  p265
    11 Feb 2016  Rumi's Poetry                  p7019
    20 Feb 2014  Social Darwinism               p5912
    03 May 2018  The Almoravid Empire           p3972
    29 Oct 2015  The Empire of Mali             p423
    27 Feb 2020  The Evolution of Horses        p233
    30 Sep 2021  The Tenant of Wildfell Hall    p780

You can also sort on simple functions; essentially any function that you can use with `arr`.
So given a table like this:

    tamarix     33  18
    tamasha     89  13
    tambac      57  72
    tambourine  48  46

if you can do `sort len(a)` to get

    tambac      57  72
    tamarix     33  18
    tamasha     89  13
    tambourine  48  46

or `sort reversed(a)` to get

    tamasha     89  13
    tambac      57  72
    tambourine  48  46
    tamarix     33  18

or  `sort (b-c)` to get:

    tambac      57  72
    tambourine  48  46
    tamarix     33  18
    tamasha     89  13

If you have a header row in your table, then usually `sort` will automagically leave it in place.
But if this does not work you can do `pop 0 sort abc push 0` or (as a convenience) `sort @abc`.


### tap - apply a function to each numerical value

    tap [x-expression]

This is useful for adjusting all the numeric values in your table at once,
perhaps for making byte values into megabytes etc.  Given values with headings like this

    Category  Type A  Type B
    ------------------------
    First         34      21
    Second        58      72

`tap +1000` will produce

    Category  Type A  Type B
    ------------------------
    First       1034    1021
    Second      1058    1072

and then `tap log(x)` produces

    Category         Type A         Type B
    --------------------------------------
    First     6.94119005507  6.92853781816
    Second    6.96413561242  6.97728134163

The default, if you omit the expression is to do nothing. If your expression
starts with an operator like + shown above, but does not include `x` in it,
then `x` will be assumed at the start.  If your expression is not valid Python
or includes undefined names, the cells will be unchanged.

Besides `x`, there are seven other variables available for your calculation:

- `rows`, `row_number`, `row_total`
- `cols`, `col_number`, `col_total`
- `total`

You can use these to normalize the values in the table, or calculate "expected" values
for a chi-squared test.  So for example, starting with the first table above, `tap /total`
will give you

    Category          Type A          Type B
    ----------------------------------------
    First     0.183783783784  0.113513513514
    Second    0.313513513514  0.389189189189

which adds to 1, while `tap /row_total` will make all the rows add to 1, and `tap /col_total`
will make all the columns add to 1.

You can calculate the "expected" values, such as you might use in a chi-squared test, with
`tap col_total*row_total/total dp 1`

    Category  Type A  Type B
    ------------------------
    First       27.4    27.6
    Second      64.6    65.4

Or perhaps the differences from the expected values, with
`tap x-col_total*row_total/total dp 1`

    Category  Type A  Type B
    ------------------------
    First        6.6    -6.6
    Second      -6.6     6.6

(which probably *should* sum to zero).

### uniq - filter out duplicated rows

    uniq [a|b|c|...]

`uniq` removes duplicate rows from the table.  With no argument the first
column is used as the key.  But if you provide a list of columns the key will
consist of the values in those columns.  So `uniq af` will remove all rows with
duplicate values in column `a` and `f`, so that you are left with just the rows
where the values in these columns are distinct.


### wrap and unwrap - reshape table in blocks

    wrap [n]
    unwrap [n]

Here is another way to reshape a table.  Given

    East  Q1  1200
    East  Q2  1100
    East  Q3  1500
    East  Q4  2200
    West  Q1  2200
    West  Q2  2500
    West  Q3  1990
    West  Q4  2600

as input, `wrap` gives you

    East  Q1  1200  West  Q1  2200
    East  Q2  1100  West  Q2  2500
    East  Q3  1500  West  Q3  1990
    East  Q4  2200  West  Q4  2600

while `wrap 3` gives

    East  Q1  1200  East  Q4  2200  West  Q3  1990
    East  Q2  1100  West  Q1  2200  West  Q4  2600
    East  Q3  1500  West  Q2  2500

The option for `wrap` should be a positive number greater than 1; it defaults to 2,
which means split the rows into two blocks and put them beside each other.

`unwrap` does the opposite - it splits the columns into blocks and puts them
after each other as rows.  The option for `unwrap` should also be a positive number
greater than 1, and it also defaults to 2, which means split the columns into two blocks
and put the right hand block under the left hand block.

In both cases numbers less than 2 are ignored.



### xp - transpose the table

`xp` just transposes the entire table. It takes no options.

    First   100
    Second  200
    Third   300

becomes

    First  Second  Third
    100    200     300

It's often useful in combination with verbs that operate on columns like `sort`
or `add`.  So the sequence `xp add xp` will give you row totals, for example,
while `xp add xp add` will add totals in both dimensions.

Running `xp` resets all the special rows (blanks, rules, comments), so the
apparent no-op sequence `xp xp` is sometimes useful to clear all the specials.



### zip and unzip - reshape a table by rows

    zip [n]
    unzip [n]

Re-shape a table row by row.  Given

    Q1  East  1200
    Q1  West  2200
    Q2  East  1100
    Q2  West  2500
    Q3  East  1500
    Q3  West  1990
    Q4  East  2200
    Q4  West  2600

as input, `zip` gives you

    Q1  East  1200  Q1  West  2200
    Q2  East  1100  Q2  West  2500
    Q3  East  1500  Q3  West  1990
    Q4  East  2200  Q4  West  2600

`unzip` does the opposite.  The option is the number of rows to combine.  The default is 2, so that
you zip every other row, and unzip the table in half (as it were).

## What counts as a number?

Tablinum reads and writes everything as strings, but it has a fairly broad
definition of which of them count as numbers.

- Any string like '4' or '-2.17' that is a valid input to the `decimal.Decimal`
  constructor, including strings like '1E-3'

- Any string with '_' or ',' as separators like '1,234' or '0.456_789'

- Any string that looks like a number but ends with '%' is treated as a
  percentage, so '45%' is interpreted as 0.45

- Binary, octal, and hex strings with leading '0b', '0o' or '0x' are converted
  to decimal integers

- The strings 'True' and 'False' count as 1 and 0

Here is a sampler, given this

    First example   True  42  3.1415  1,234  0.123_245   32%  0b1111  0xdead       4E3
    Another one    False  39  2.7185  4,537  0.892_244   67%    0o63  0xBEEF     21E-3

then `rule add` will produce

    First example   True  42  3.1415  1,234  0.123_245   32%  0b1111  0xdead       4E3
    Another one    False  39  2.7185  4,537  0.892_244   67%    0o63  0xBEEF     21E-3
    ----------------------------------------------------------------------------------
    Total              1  81  5.8600   5771   1.015489  0.99      66  105884  4000.021

Notice that the results are always given as decimals, but you can use `tap` or `arr` to
set a common format.  You can reset them all to "normal" decimals with `tap +0`:

    First example  1  42  3.1415  1234  0.123245  0.32  15   57005      4000
    Another one    0  39  2.7185  4537  0.892244  0.67  51   48879     0.021
    ------------------------------------------------------------------------
    Total          1  81  5.8600  5771  1.015489  0.99  66  105884  4000.021

while `tap f'{x:,}'` gives you:

    First example  1  42  3.1415  1,234  0.123245  0.32  15   57,005      4,000
    Another one    0  39  2.7185  4,537  0.892244  0.67  51   48,879      0.021
    ---------------------------------------------------------------------------
    Total          1  81  5.8600  5,771  1.015489  0.99  66  105,884  4,000.021


## Methods available for a Table object

The `Table` class defined by `tabulate` provides the following instance methods.
To use them you need to instantiate a table, then call the methods on that
instance.
```python
    t = tablinum.Table()
    t.parse_lol(data_rows)
    t.do("add")
    print(t)
```
An instance of a `Table` is essentially an augmented list of lists, so
it implements most of the normal Python list interface, except that you
can't assign to it directly.  Instead you should use one of the two
data parsing methods to insert data, or `append`, or `insert`.

### Parsing methods

- `parse_lol(list_of_iterables, append=False, filler='')`

    Parse a list of iterables into your table instance.  By default this will
    replace any existing values in the instance but if you add `append=True` the
    new values will be appended (or rather the old values will not be cleared first).

    Note that you can use lists or tuples or strings as the "rows" in the list of iterables.
    The "rows" can vary in length, and short ones will be expanded using the optional
    filler string, so that they are all the same length. The default filler is an empty string
    so quite often you will not notice this expansion.

    After this expansion each row in the list of iterables is passed to the `append` method.

- `parse_lines(lines_thing, splitter=re.compile(r'\s\s+'), splits=0, append=False)`

    Parse a list of plain text lines into your table instance.  Each line will be split up
    using the compiled regular expression passed as the `splitter` argument.  The default pattern is
    two or more blanks.  The `splits` argument controls how many splits you want.  The append
    argument behaves the same as for `parse_lol`.  If it is false (default) then any data
    in the table instance will be cleared first.

    This method will recognise rules (any line consisting of only "---" chars), blanks,
    and comments (lines with leading '#').

### List like methods

You can use some of the regular list syntax with a Table instance.  So after

    t = tablinum.Table()
    t.parse_lol(list_of_iterables)

you can get the number of rows with `len(t)`, and you can get the first row with `t[0]`
and the last with `t[-1]`, and so on.  A non-integer index, or an index that is too big
will raise the normal list exceptions.  A row will be returned as a list of strings.
(Even the strings that look like numbers will be returned as strings).  You can also
return slices, so `t[::2]` gives you every other row, while `t[:]` gives you a raw copy
of all the data.

- `append(row, filler='')`

    Add a new row to the bottom of the table.  The row should be an iterable as above.

- `insert(i, row, filler='')`

    Insert a new row after line `i`.   Note that both `append` and `insert` maintain
    the other properties of the table instance.

- `pop(n=None)`

    Remove row `n` (or the last one if `n` is `None`).  The row will be returned as a
    list of strings.

- `clear()`

    Remove all the rows of data from your table instance.

### Manipulation and printing

- `column(i)`

    Get a column from the table.  The data is returned as a list of 2-tuples.
    Each tuple is either:

    - True, followed by a numeric value as a Decimal object
    - False, followed by a string that does not look like a number

    So (for example) you could get the total of the numbers in column 2 of your
    table like this

        sum(x[1] for x in t.column(2) if x[0])

- `transpose()`

    Swap rows and columns. This is the equivalent of the `xp` DSL verb.
    So if `t` is a Table object then this:

        t.transpose()

    has the same effect as this:

        t.do('xp')

    You could use this to add a new column:

        t.transpose()
        t.append(iterable)
        t.transpose()

- `do(agenda)`

    Apply a sequence of DSL verbs and options to the contents of the table.
    The verbs are described above.  Separate each verb and option by one or more blanks.

- `add_blank(n=None)`

    Add a special blank line after row `n`, or at the end if `n` is None

- `add_rule(n=None)`

    Add a special rule line after row `n` or at the end if `n` is None

- `add_comment(contents)`

    Add a special comment line after row `n` or at the end if `n` is None

- `tabulate()`

    Return a generator object, that will yield a tabulated string for each row in the table.
    You can print your table neatly like this:
    ```python
        for r in t.tabulate():
            print(r)
    ```
    This allows you to print rows selectively or perhaps highlight some of them in some
    way.  If you just want to print the whole thing, you could do

        print("\n".join(t.tabulate()))

    except that you don't need to do that because the Table objects implement the magic printing
    interface, so that all you have to do is

        print(t)

    and `t.tabulate()` will be called automatically.  The `tabulate` method will use the current settings
    for separators, so if you have done `t.do('make csv')` you will get lines of values with commas.

## License

Tablinum is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
