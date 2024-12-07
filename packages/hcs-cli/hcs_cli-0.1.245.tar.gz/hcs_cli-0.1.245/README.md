# horizon-cloud-service-cli

[![License](https://img.shields.io/badge/License-Apache%202.0-blue)](https://github.com/vmware-labs/compliance-dashboard-for-kubernetes/blob/main/LICENSE)

- [horizon-cloud-service-cli](#horizon-cloud-service-cli)
  - [Overview](#overview)
  - [Try it out](#try-it-out)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
      - [Mac \& Linux](#mac--linux)
      - [Windows](#windows)
      - [Use the CLI](#use-the-cli)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)


## Overview
Command line toolbox for [VMware Horizon Cloud Service (HCS) Next-Gen](https://www.vmware.com/products/horizon-cloud.html). It provides human-friendly operations based on HCS REST API.

## Try it out


### Prerequisites
* Python 3.9+
* Pip3

Refer to [Setup Prerequisites](doc/dev-setup.md#setup-prerequisites) for more details.

### Installation

#### Mac & Linux

Install the tool
```
brew install python3
pip3 install hcs-cli
```

#### Windows
Install the tool.
```
pip install hcs-cli
```
If you have python installed with option "Add python to path", it should be fine. Otherwise, you need to add python and it's Script directory to path.

#### Use the CLI
Use with default public HCS service. 
```
hcs login
```
Run a command, for example, list templates:
```
hcs admin template list
```

## Documentation
* [HCS CLI - User Guide](doc/hcs-cli-user-guide.md)
* [HCS CLI - Cheatsheet](doc/hcs-cli-cheatsheet.md)
* [HCS CLI - Dev Guide](doc/hcs-cli-dev-guide.md)
* [HCS Plan - template engine for HCS](doc/hcs-plan.md)
* [Context Programming](https://github.com/nanw1103/context-programming)

  
## Contributing

The horizon-cloud-service-cli project team welcomes contributions from the community. Before you start working with horizon-cloud-service-cli, please read and sign our Contributor License Agreement [CLA](https://cla.vmware.com/cla/1/preview). If you wish to contribute code and you have not signed our CLA, our bot will prompt you to do so when you open a Pull Request. For any questions about the CLA process, please refer to our [FAQ]([https://cla.vmware.com/faq](https://cla.vmware.com/faq)).

## License

Apache 2.0


