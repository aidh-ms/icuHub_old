# icuHUb
Streamlit version of the icu visualizer

## Pre-requisites

This app expects a local installation of the queried databases. The databases themselves are not included in this repository. So far the following datbases are supported:

- [MIMIC-IV](https://mimic.mit.edu/)
- more to follow...

For mimic, the app expects you to have the mimic_derived schema installed. The mimic_derived schema contains pre-computed tables that are used by the app to speed up the queries. You can find the mimic_derived schema [here](https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts). An instruction on how to build these schemas are also provided in the mimic documentation.
