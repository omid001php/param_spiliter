# Parameter List Processor

This Python script processes parameter lists from an input file, appends a keyword to each parameter, and splits the results into multiple output files. It utilizes multiprocessing for improved performance on multi-core systems.

## Features

- Read parameters from an input file
- Append a keyword to each parameter
- Process parameters in parallel using multiple CPU cores
- Split the results into multiple output files
- Option to remove the last character from each output chunk

## Installation

1. Ensure you have Python 3.6 or later installed on your system.
2. Clone this repository:
   
```
git clone https://github.com/omid001php/param_spiliter.git
```

```
cd param_spiliter
```

4. 	**No additional** dependencies are required as the script uses only Python standard libraries.

## Usage

Run the script from the command line with the following syntax:

```python3 param_processor.py -u <input_file> -p <keyword> -s <split_size> [-c <cores>] [-e]```

### Arguments

| Argument | Short | Long | Required | Description |
|----------|-------|------|----------|-------------|
| Input file | -u | --input | Yes | Path to the input text file containing parameters |
| Keyword | -p | --keyword | Yes | Keyword to append to each parameter |
| Split size | -s | --split | Yes | Number of parameters per output file |
| CPU cores | -c | --cores | No | Number of CPU cores to use (default: 2) |
| Remove end | -e | --remove_end | No | Remove the last character from each output chunk |

## Example

1. Create an input file named `params.txt` with the following content:
```
param1
param2
param3
param4
param5
param6
```

You can using [Fallparam](https://github.com/ImAyrix/fallparams), [X8](https://github.com/Sh1Yo/x8), [Arjun](https://github.com/s0md3v/Arjun)

```
python3 main.py -u params.txt -p _keyword -s 2 -c 4 -e
```


2. This will create output files:
- `params_00.txt` containing: `param1_keywordparam2_keywor`
- `params_01.txt` containing: `param3_keywordparam4_keywor`
- `params_02.txt` containing: `param5_keywordparam6_keywor`


