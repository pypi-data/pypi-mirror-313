> [!NOTE]
> This repository has been forked from https://github.com/mscribellito/jilutil, and credit is given to the original author.

# JIL Utility
AutoSys JIL command line utility

This utility provides functionality to:
* **Export to CSV** - makes jobs easier to read for non-technical people
* **Format JIL** - aids in comparison of jobs in different environments
* **Output to console** - allows quick inspection of jobs contained within

Additionally, the functionality to parse JIL files is provided as a library.

## What is JIL?
Job Information Language (JIL) is a scripting language that lets you define and modify assets such as jobs, global variables, machines, job types, external instances, and blobs.

## Basic Usage

Basic usage for working with a JIL file.

```usage: jilutil.py [-h] [-e] [-f] [-n] [-o] [-r] [-v] path```

### Positional Arguments
* path - path to JIL source file

### Optional Arguments
* -h, --help - show this help message and exit
* -e, --export - Exports jobs contained in the JIL source file in ascending order by name to a CSV file.
* -f, --format - Formats jobs contained in the JIL source file in ascending order by name.
* -o, --output - Outputs jobs contained in the JIL source file in ascending order by name to standard out.
* -a, --attributes - Attributes to list when outputting jobs (ex: job_type,box_name).
* -n, --new - Formats as new file.
* -r, --reverse - Sorts jobs in descending order by name.
* -v, --verbose - Increases output verbosity.

## Functionality

### Export
Exports jobs contained in the JIL source file in ascending order by name to a CSV file.

Export jobs contained in JIL file:
```python -m jilutil sample.jil -e```

### Format
Formats jobs contained in the JIL source file in ascending order by name.

Format JIL file in place:
```python -m jilutil sample.jil -f```

Format JIL file as new file:
```python -m jilutil sample.jil -f -n```

### Output
Outputs jobs contained in the JIL source file in ascending order by name to standard out.

Output jobs contained in JIL file:
```python -m jilutil sample.jil -o```

```
SAMPLE_BOX_JOB
SAMPLE_CMD_JOB_1
SAMPLE_CMD_JOB_2
```

Output jobs contained in JIL file with extra attributes:
```python -m jilutil sample.jil -o -a box_name,job_type,condition```

```
SAMPLE_BOX_JOB -> box_name:  ; job_type: BOX ; condition:
SAMPLE_CMD_JOB_1 -> box_name: SAMPLE_BOX_JOB ; job_type: CMD ; condition:
SAMPLE_CMD_JOB_2 -> box_name: SAMPLE_BOX_JOB ; job_type: CMD ; condition: s(SAMPLE_CMD_JOB_1)
```

## Executable
Stand alone executable (no Python required) can be compiled using pyinstaller and the build.ps1 script included. Executable will be placed in "dist" folder.
