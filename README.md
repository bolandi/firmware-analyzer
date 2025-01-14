## Security-Focused Firmware Analyzer

A Generic cross-platform framework to integrate firmware analysis tools with pre-defined configuration in a docker image. 

### Requirements

    * Python 3.8+
    * Docker

### Installation

The firmware images to be analyzed should be placed in the `images` folder under the repository root directory. To 
install the dependencies and see the analysis options, just execute `python3 run.py --help` or run the following script:

```commandline
git clone "https://github.com/bolandi/firmware-analyzer" analyzer && cd analyzer
python3 run.py -h
```

The results will be generated under `$PWD/target/{tool_name}`

### Existing integrated tools

    * binwalk
    * cwe-checker
    * firmwalker
    * firmadyne
    * bytesweep
    * binary-analysis-next-gen
    * cve-bin-tool

### Further reading

This framework has been used for the following study:\
[Automated Security Analysis of Firmware](https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A1704788&dswid=-2964)

