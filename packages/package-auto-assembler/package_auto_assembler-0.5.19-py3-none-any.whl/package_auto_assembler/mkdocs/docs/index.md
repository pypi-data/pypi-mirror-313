# Intro

[![PyPiVersion](https://img.shields.io/pypi/v/package-auto-assembler)](https://pypi.org/project/package-auto-assembler/) [![License](https://img.shields.io/github/license/Kiril-Mordan/reusables)](https://github.com/Kiril-Mordan/reusables/blob/main/LICENSE)

`package-auto-assembler` is a tool that meant to streamline creation of `single module packages`.
Its primary goal is to automate as many aspects of python package creation as possible,
thereby shortening the development cycle of reusable components and maintaining a high standard of quality for reusable code. 

With `package-auto-assembler`, you can simplify the package creation process to the point where it can be seamlessly triggered within CI/CD pipelines, requiring minimal setup and preparation for new modules.

## Key features

- [Set up new Python packaging repositories](https://kiril-mordan.github.io/reusables/package_auto_assembler/python_packaging_repo/) for Github and Azure DevOps.
- [Create new packages dynamically](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#creating-packages), reducing manual effort.
- [Check module dependencies](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#checking-dependencies) for vulnerabilities and unexpected licenses.
- [Run FastAPI and Streamlit apps](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#running-apps-from-packages) directly from packages created with this tool.
- [Extract artifacts and files](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#extracting-files-from-packages) packaged alongside code.
- [Show detailed information](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#show-modules-info) about installed packages made with the tool.
- [Automatically assemble release notes](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#other) based on commit messages.
- [Extract requirements](https://kiril-mordan.github.io/reusables/package_auto_assembler/cli_tools/#other) automatically from `.py` files without maintaining separate `requirements.txt`.


## Installation

```bash
pip install package-auto-assembler
```

