# UCSF Philter Lite
![Python Package](https://github.com/TimOrme/philter-ucsf/workflows/Python%20package/badge.svg)
[![PyPI version](https://badge.fury.io/py/philter-lite.svg)](https://pypi.org/project/philter-lite/)

`philter_lite` is a fork of the wonderful work done here: https://github.com/BCHSI/philter-ucsf

The fork aims to tailor the functionality to more of a production-level setup.  This includes:

* Stateless functions 
* Stronger type-checking, hints, and data contracts
* Improved unit test coverage (hopefully)

It does this at the expense of breaking the model evaluation functionality provided in the original library.  If you
are developing a new set of filters, it is recommended that you evaluate them using them in the original UCSF Philter.
You can then 

There are some minor memory improvements here, and no known performance improvements; the main goal is to improve 
stability and extensibility of the code, but there shouldn't be the expectation that it will run faster.

## Citations

If you use this software for any publication, please cite: Norgeot, B., Muenzen, K., Peterson, T.A. et al. 
Protected Health Information filter (Philter): accurately and securely de-identifying free-text clinical notes. 
npj Digit. Med. 3, 57 (2020). https://doi.org/10.1038/s41746-020-0258-y

# Installing Philter

To install Philter from PyPi, run the following command:

```bash
pip3 install philter-lite
```

The main philter CLI can be executed by running:

```bash
philter_lite
```

# Running Philter: A Step-by-Step Guide

Philter is a command-line based clinical text de-identification software that removes protected health information 
(PHI) from any plain text file. Although the software has built-in evaluation capabilities and can compare Philter 
PHI-reduced notes with a corresponding set of ground truth annotations, annotations are not required to run Philter. 
The following steps may be used to 1) run Philter in the command line without ground truth annotations, or 2) generate 
Philter-compatible annotations and run Philter in evaluation mode using ground truth annotations. Although any set of 
notes and corresponding annotations may be used with Philter, the examples provided here will correspond to the I2B2 
dataset, which Philter uses in its default configuration. 

Before running Philter either with or without evaluation, make sure to familiarize yourself with the various options 
that may be used for any given Philter run:

### Flags:

```
usage: philter [-h] [-i INPUT] [-a ANNO] [-o OUTPUT] [-f FILTERS] [-x XML]
               [-c COORDS] [--eval_output EVAL_OUTPUT] [-v VERBOSE]
               [-e RUN_EVAL] [-t FREQ_TABLE] [-n INITIALS]
               [--outputformat OUTPUTFORMAT] [--ucsfformat UCSFFORMAT]
               [--prod PROD] [--cachepos CACHEPOS]

Philter -- PHI filter for clinical notes

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the directory or the file that contains the
                        PHI note, the default is ./data/i2b2_notes/
  -a ANNO, --anno ANNO  Path to the directory or the file that contains the
                        PHI annotation, the default is ./data/i2b2_anno/
  -o OUTPUT, --output OUTPUT
                        Path to the directory to save the PHI-reduced notes
                        in, the default is ./data/i2b2_results/
  -f FILTERS, --filters FILTERS
                        Path to our config file, the default is
                        ./configs/integration_1.json
  -x XML, --xml XML     Path to the json file that contains all xml data
  -c COORDS, --coords COORDS
                        Path to the json file that contains the coordinate map
                        data
  --eval_output EVAL_OUTPUT
                        Path to the directory that the detailed eval files
                        will be outputted to
  -v VERBOSE, --verbose VERBOSE
                        When verbose is true, will emit messages about script
                        progress
  -e RUN_EVAL, --run_eval RUN_EVAL
                        When run_eval is true, will run our eval script and
                        emit summarized results to terminal
  -t FREQ_TABLE, --freq_table FREQ_TABLE
                        When freqtable is true, will output a unigram/bigram
                        frequency table of all note words and their PHI/non-
                        PHI counts
  -n INITIALS, --initials INITIALS
                        When initials is true, will include initials PHI in
                        recall/precision calculations
  --outputformat OUTPUTFORMAT
                        Define format of annotation, allowed values are
                        "asterisk", "i2b2". Default is "asterisk"
  --ucsfformat UCSFFORMAT
                        When ucsfformat is true, will adjust eval script for
                        slightly different xml format
  --prod PROD           When prod is true, this will run the script with
                        output in i2b2 xml format without running the eval
                        script
  --cachepos CACHEPOS   Path to a directoy to store/load the pos data for all
                        notes. If no path is specified then memory caching
                        will be used.
```
