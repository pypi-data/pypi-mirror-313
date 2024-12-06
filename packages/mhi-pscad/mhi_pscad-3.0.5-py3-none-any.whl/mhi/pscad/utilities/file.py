# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Power Systems Computer Aided Design (PSCAD)
# ------------------------------------------------------------------------------
#  PSCAD is a powerful graphical user interface that integrates seamlessly
#  with EMTDC, a general purpose time domain program for simulating power
#  system transients and controls in power quality studies, power electronics
#  design, distributed generation, and transmission planning.
#
#  This Python script is a utility class that can be used by end users
#
#
#     PSCAD Support Team <support@pscad.com>
#     Manitoba HVDC Research Centre Inc.
#     Winnipeg, Manitoba. CANADA
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
File Utilities
"""

# Import dependancies
import os.path
import re
import shutil
import sys
from typing import Dict, List, Union

_ENCODING='cp1252'

#---------------------------------------------------------------------
# everything_except
#
# Create a filter to be used to exclude file types.
#---------------------------------------------------------------------
def everything_except(*exts):
    """
    Create an lambda function appropriate for use as the ``ignore=``
    filter of ``shutil.copytree()``.

    Given a list of file extensions, the returned lambda will filter
    out all files with those extensions from a list of files provided
    to the lambda function.

    >>> from mhi.pscad.utilities.file import everything_except
    >>> filter = everything_except(".in", ".out")
    >>> filter(None, ["file.obj", "file.exe", "file.in", "file.out"])
    ["file.obj", "file.exe"]

    """

    return lambda _, files: [f for f in files if not any(f.endswith(ext)
                                                         for ext in exts)]

#---------------------------------------------------------------------
# File class
#---------------------------------------------------------------------
class File:
    """
    Useful File utilities
    """

    #---------------------------------------------------------------------
    # compare_files
    #---------------------------------------------------------------------
    @staticmethod
    def compare_files(file1, file2):
        """
        Compares two text files.  Return ``True`` if the contents match.
        """

        with open(file1, encoding=_ENCODING) as fp1, \
             open(file2, encoding=_ENCODING) as fp2:
            # ZIP (like a mechanical zipper, not file compression) the
            # iterators so that a line is returned from each.
            # Call these lines x and y, and test if they are equal.
            # Repeat for ALL lines in the file, AND-ing the results together.
            # Short circuit AND-logic applies; all() will stop at first False.
            files_match = all(x == y for x, y in zip(fp1, fp2))

            # Now check if the file lengths are the same.
            files_match = files_match and next(fp1, None) is None and \
                          next(fp2, None) is None

        return files_match

    #---------------------------------------------------------------------
    # move_files
    #
    # Create a filter to be used to exclude file types.
    #---------------------------------------------------------------------
    @staticmethod
    def move_files(src_dir, dest_dir, *exts):
        """
        Copies files from the source directory to a destination directory.

        The destination directory must not exist; it will be created.
        Only files which match the given extension(s) are copied.
        """

        shutil.copytree(src_dir, dest_dir, ignore=everything_except(*exts))

    #---------------------------------------------------------------------
    # copy_files
    #
    # Copy files from source directory to destination directory.
    #---------------------------------------------------------------------
    @staticmethod
    def copy_files(src_dir, dst_dir, *exts, recursive=False):
        """
        Copies files from the source directory to a destination directory.

        Only files matching the given extensions are copied.  If no
        extensions are given, all files are copied.

        If recursive is True, subdirectories are copied.
        """

        if os.path.exists(dst_dir):
            if not os.path.isdir(dst_dir):
                raise ValueError("Destination is not a directory")
        else:
            os.makedirs(dst_dir)

        for filename in os.listdir(src_dir):
            src = os.path.join(src_dir, filename)
            dst = os.path.join(dst_dir, filename)
            if os.path.isfile(src):
                if not exts or os.path.splitext(filename)[1] in exts:
                    shutil.copy(src, dst)
            elif recursive and os.path.isdir(src):
                File.copy_files(src, dst, *exts, recursive=recursive)

    #---------------------------------------------------------------------
    # copy_file
    #
    # Copy a file to destination directory.
    #---------------------------------------------------------------------
    @staticmethod
    def copy_file(file, dest_dir):
        """
        Copies a file to the destination directory
        """

        shutil.copyfile(file, dest_dir)

    #---------------------------------------------------------------------
    # convert_out_to_csv
    #
    # Converts PSCAD output file to csv.
    #---------------------------------------------------------------------
    @staticmethod
    def convert_out_to_csv(directory, out_file, csv_file):
        """Converts PSCAD output file into a csv file"""

        with open(directory+'\\'+out_file, 'r', encoding=_ENCODING) as out, \
             open(directory+'\\'+csv_file, 'w', encoding=_ENCODING) as csv:
            csv.writelines(",".join(line.split())+"\n" for line in out)

#---------------------------------------------------------------------
# OutFile class
#---------------------------------------------------------------------

class OutFile:
    """
    PSCAD Output files utility class
    """

    #---------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------

    def __init__(self, basename):
        """
        Construct an instance which can manipulate a set of PSCAD output
        files (``<basename>.inf``, & ``<basename>_##.out``)
        """

        self._basename = basename       # Save basename of output files
        self._files = None

        # Column 0 is always "TIME"
        self._column = {'TIME': 0, ('', 'TIME'): 0}
        self._column_names = ['TIME']
        self._names = []

        self._read_inf()                # Read in the *.inf file


    def _read_inf(self):
        """
        Read in the *.inf file, and record the PGB descriptions, groups,
        and channel numbers
        """

        # Look for 'PGB(##) ... Desc="<desc>" Group="<group>" ...' lines
        inf_re = re.compile(r'^PGB\((\d+)\).+Desc="([^"]+)"\s+Group="([^"]+)"')

        descriptions = set()
        max_column = 0


        # Open the *.inf file ...
        with open(self._basename + ".inf", encoding=_ENCODING) as inf:
            # For each line in the file ...
            for line in inf:
                # Test it against the above pattern
                match = inf_re.match(line)
                if match:
                    # If found, extract the column, description and group
                    col = int(match.group(1))
                    desc = match.group(2)
                    grp = match.group(3)

                    # Keep track of maximum column (PGB)
                    max_column = max(max_column, col)

                    # Store the column number under the 'desc' key.
                    self._column[desc] = col
                    if grp:
                        # ... and under the 'group:desc' key.
                        self._column[grp+":"+desc] = col

                    # Store the column under ("grp", "desc") key as well.
                    self._column[(grp, desc)] = col

                    if desc in descriptions:
                        desc = grp + ":" + desc
                    else:
                        descriptions.add(desc)

                    # Store the column description, by column number
                    # (Note: we assume sequential PGB ordering)
                    self._column_names.append(desc)


    #---------------------------------------------------------------------
    # open/close
    #---------------------------------------------------------------------

    def open(self):
        """
        Open all of the internal data files
        """

        if self._files is not None:
            raise IOError("Already open")

        # 1 output file for every 10 channels => #files = ceil(#channels/10)
        # (But don't include the TIME channel in the channel count)
        num_files = (len(self._column_names) + 8) // 10

        # Open up all output files
        filename_fmt = self._basename + "_{:02d}.out"
        filenames = [filename_fmt.format(i+1) for i in range(num_files)]
        self._files = [open(filename, encoding=_ENCODING) # pylint: disable=consider-using-with
                       for filename in filenames]

        return self

    def close(self):
        """
        Close all of the internal data files
        """

        if self._files is None:
            raise IOError("Already closed")

        for file in self._files:
            try:
                file.close()
            except IOError:
                print(f"Failed to close file {file}", file=sys.stderr)

        self._files = None

    #---------------------------------------------------------------------
    # Enter/Exit
    #
    # Allow OutFile to be used with the Python "with" statement, for proper
    # resource management
    #---------------------------------------------------------------------

    def __enter__(self):
        """
        Allow OutFile to be treated as a resource in a with statement

        eg)
            with OutFile("basename") as out:
                # use 'out' here

            # 'out' is automatically closed at end of 'with' statement
        """

        self.open()

        return self

    def __exit__(self, type_, value, traceback):
        """
        Close all of the _##.out files
        """

        self.close()

    #---------------------------------------------------------------------
    # read_values
    #
    # Return one row of values from each data file, joined together as one
    # list of values.  The time value will only appear once, as the first
    # value
    #---------------------------------------------------------------------

    def read_values(self):
        """
        Return next row of data, read from all ``*.out`` data files
        """

        values = None
        # For each file ...
        for file in self._files:
            # ... read one line from each ...
            line = file.readline()
            if not line:
                return None

            # ... split into individual fields
            vals = line.split()
            if values is None:
                # if first file, grab all data, including TIME (column #0)
                values = vals
            else:
                # otherwise, skip the time value, grab the rest
                values.extend(vals[1:])

        return values

    #---------------------------------------------------------------------
    # Iterator
    #
    # Allow an OutFile to be treated as an iterable resource, returning
    # one complete row of data at each iteration.
    #---------------------------------------------------------------------

    def __iter__(self):
        """
        Returns an iterable object for this OutFile.

        eg)
            for values in out_file:
                time = values[0]
                ch1 = value[1]
                ch2 = value[2]
        """

        return self

    def __next__(self):
        """
        Return next row of data
        """

        values = self.read_values()
        if values is None:
            raise StopIteration

        return values

    #---------------------------------------------------------------------
    # Columns
    #---------------------------------------------------------------------

    def columns(self) -> List[str]:
        """
        All of the columns in the datafile
        """

        return self._column_names


    #---------------------------------------------------------------------
    # Column name to number
    #---------------------------------------------------------------------

    def column(self, name) -> int:
        """
        Turn a column name into a number
        """

        if isinstance(name, int):
            return name

        return self._column[name]

    def column_name(self, column) -> str:
        """
        Turn a column number into a column name
        """

        return self._column_names[column]


    #---------------------------------------------------------------------
    # Convert OutFile to CSV
    #---------------------------------------------------------------------

    def toCSV(self, csv=None, columns=None, start=0, end=float("inf")): # pylint: disable=invalid-name
        """
        Convert OutFile into a Comma Separated Value (CSV) file

        If no csv file is specified, defaults to "<basename>.csv".
        If no column names are specified, defaults to all columns.
        If no start time is given, defaults to start of file.
        If no end time is given, defaults to end of file.
        """

        if start < 0:
            raise ValueError("Start must not be negative")
        if end <= start:
            raise ValueError("End must be greater than start")

        if csv is None:
            # Default csv filename, if none given
            csv = self._basename+".csv"

        # Determine which columns to export to CSV
        if columns is None:
            # All columns!
            columns = self._column_names
            cols = range(len(columns))
        else:
            # Convert column names into column numbers
            columns = ['TIME'] + list(columns)
            cols = [self.column(name) for name in columns]

        self._to_csv(csv, columns, cols, start, end)

    def _to_csv(self,                       # pylint: disable=too-many-arguments
                csv_filename, columns, cols, start, end):

        # Open all "<basename>_##.out" files for input as a closeable resource
        with self as data:

            # Skip header line (from all .out files)
            next(data)

            # Open CSV file for output (as closeable resource)
            with open(csv_filename, 'w', encoding=_ENCODING) as csv:
                # Write out quoted column names in first row
                csv.write('"' + '","'.join(columns)+'"\n')

                # Loop over all rows of data
                for values in data:
                    # Convert time value to a number, and check start/end
                    time = float(values[0])
                    if time >= start:
                        if time >= end:
                            break
                        # Write out all values, separated by commas
                        csv.write(','.join(values[i] for i in cols))
                        csv.write('\n')



    #---------------------------------------------------------------------
    # Fetch one or more values from a specific moment in time
    #---------------------------------------------------------------------

    def values_at(self, time: float, *columns: str,
                  as_dict=False) -> Union[List[float], Dict[str,float]]:
        """
        Fetch one or more values from a specific moment in time.

        Values from the row in the datafile closest to the given time
        are returned.  If no column names are specified, all columns are
        returned.

        Parameters:
            time (float): The desired time to retrieve the column values at
            columns (List[str]): the columns to retrieve the values for
                (optional)
            as_dict (bool): Set to true to return a column name=value dictionary
                (optional)

        Returns:
            A list or a dictionary of column values, as indicated by ``as_dict``
        """

        def to_numeric(value):
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return value

        # Determine which columns are desired
        cols: Union[range, List[int]]
        if columns:
            # Convert column names into column numbers
            cols = [self.column(name) for name in columns]
        else:
            # All columns!
            columns = self._column_names
            cols = range(len(columns))

        # Find data row pair bracketing desired time value
        with self as data:
            next(data)
            last = None
            for values in data:
                if time <= float(values[0]):
                    break
                last = values
            else:
                values = None

        if not (last or values):
            raise ValueError("No data")

        # Determine which row is closest to desired time value
        if last:
            if values:
                if abs(float(last[0]) - time) < abs(float(values[0]) - time):
                    values = last
            else:
                values = last

        vals = [to_numeric(values[col]) for col in cols]
        return dict(zip(columns, vals)) if as_dict else vals


# ------------------------------------------------------------------------------
#  End of script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
