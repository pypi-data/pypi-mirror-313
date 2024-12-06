# Tranqu
[![CI](https://github.com/oqtopus-team/tranqu/actions/workflows/ci.yaml/badge.svg)](https://github.com/oqtopus-team/tranqu/actions/workflows/ci.yaml)
[![pypi version](https://img.shields.io/pypi/v/tranqu.svg)](https://pypi.org/project/tranqu/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Tranqu is a one-stop framework for transpilers across multiple quantum programming libraries and formats for quantum circuits..

## Overview

**Tranqu** is is a one-stop framework for transpilers across multiple quantum programming libraries and formats for quantum circuits.

Quantum circuit transpilation is NP-complete, and heuristic algorithms are typically used.
While many transpiler libraries exist, the optimal transpiler and its options often depend on the quantum circuit and device information.
Therefore, the ability to leverage various vendors' transpilers is highly desirable.
By using Tranqu, you can run various vendors' transpilers without being bothered by the conversion of quantum circuits or device information.

The name "Tranqu" is derived from "tranquility", reflecting the desire to enable the smooth and stress-free use of transpilers.

## Features

- **Program Converter**: Converts quantum circuits into another library's format.
- **Device Converter**: Converts device information into another library's format.
- **Target Transpilation**:  Converts both quantum circuits and device information, then runs the target transpiler. Transpiler options can be easily specified by users familiar with that transpiler.
- **Transpilation Statistics**: Outputs statistical data before and after transpilation.
- **Using Custom Transpilers and Converters**: Uses user-created Transpilers, Program Converters, and Device Converters in Tranqu.

## Documentation

- [Documentation Home](https://tranqu.readthedocs.io/)

## CITATION

You can use the DOI to cite OQTOPUS Cloud in your research.

[![DOI](https://zenodo.org/badge/898082553.svg)](https://zenodo.org/badge/latestdoi/898082553)

Citation information is also available in the [CITATION](https://github.com/oqtopus-team/tranqu/blob/main/CITATION.cff) file.

## Contact

You can contact us by creating an issue in this repository,
or you can contact us by email:

- [oqtopus-team[at]googlegroups.com](mailto:oqtopus-team[at]googlegroups.com)

## LICENSE

Tranqu is released under the [Apache License 2.0](https://github.com/oqtopus-team/tranqu/blob/main/LICENSE).
