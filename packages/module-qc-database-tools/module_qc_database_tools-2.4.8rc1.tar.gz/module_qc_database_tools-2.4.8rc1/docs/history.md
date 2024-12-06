# module-qc-tools history

---

All notable changes to module-qc-tools will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

**_Changed:_**

**_Added:_**

**_Fixed:_**

## [2.4.7](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.7) - 2024-11-21 ## {: #mqt-v2.4.7 }

**_Fixed:_**

- misleading error message for `KeyError` raised when trying to access with an
  incorrect chip type

## [2.4.6](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.6) - 2024-11-21 ## {: #mqt-v2.4.6 }

**_Fixed:_**

- bug in checking for authentication with mongo for uploading yarr scans

## [2.4.5](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.5) - 2024-11-21 ## {: #mqt-v2.4.5 }

**_Fixed:_**

- bug in changing `Protocol` for uploading measurements (#36)

## [2.4.4](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.4) - 2024-10-03 ## {: #mqt-v2.4.4 }

**_Changed:_**

- migrate from `currentStage` to `stage` for LDB interactions
  (1a60273d284a1cb8f3c878a4cdb1d416821b36fe,
  3a18800a5e9859c83ea6a24ee9d3256a1e79d8db,
  cc26823091aa51ce74fe2dfad886f0b9e508961f,
  343d26d1cdb693cf785eab0c3483913452265295)

**_Added:_**

- add three command-line interfaces migrated from `YARR`: `localdbtool-upload`,
  `localdbtool-retrieve`, `influxdbtool-retrieve` (!56)

**_Fixed:_**

- make `mqdbt upload-measurement` more robust to errors from LDB that are not
  JSON-formatted (b09b759f5ce49662b01f471369714cc4e84910fb,
  ba120930633f29ebc8a386266aa76d3dc4166fab)
- sort entries using the `tuple` form instead of the `dict` form
  (bb87551d5e2a3acf59102c2b98fde4cf8d495424)

## [2.4.3](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.3) - 2024-10-15 ## {: #mqt-v2.4.3 }

**_Changed:_**

- add support for fetching reference IVs of triplet modules (!55)

## [2.4.2](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.2) - 2024-10-03 ## {: #mqt-v2.4.2 }

**_Fixed:_**

- add some protection for attachment titles that may be missing or not set
  (4cabe51038e58fd7a48863b9c827bbb4c83853cf)

## [2.4.1](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.1) - 2024-10-03 ## {: #mqt-v2.4.1 }

**_Changed:_**

- improve support of triplet modules by making sure we identify it correctly
  from `itksn` (06542155f8fc136ee5341391a8654731f6ae1304)

## [2.4.0](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.4.0) - 2024-07-13 ## {: #mqt-v2.4.0 }

**_Changed:_**

- refactored some common code across the command-line interfaces

**_Added:_**

- ability to sync component stages recursively (!51)

## [2.3.0](https://gitlab.cern.ch/atlas-itk/pixel/module/module-qc-database-tools/-/tags/v2.3.0) - 2024-07-13 ## {: #mqt-v2.3.0 }

First release for this documentation. (!47)

**_Changed:_**

- connectivity generation supports a `--dp`/`--port` option for specifying the
  DP Port (!42)

**_Added:_**

- command-line interface for fetching reference IVs (!46)
- support for ITkPix v2 (!39, !43)
- `ssl` option for mongo-client connections from command line (!37)

**_Fixed:_**

- bug in obtaining chip type from config when saving to localDB (!45)
