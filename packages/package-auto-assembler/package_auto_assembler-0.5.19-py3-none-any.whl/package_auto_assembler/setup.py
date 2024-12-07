from setuptools import setup

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

long_description = """# Package auto assembler

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

"""

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description += fh.read()

setup(
    name="package_auto_assembler",
    packages=["package_auto_assembler"],
    install_requires=['uvicorn', 'mkdocs>=1.6.0', 'wheel>=0.44.0', 'packaging', 'attrs>=22.2.0', 'requests', 'fastapi', 'pyyaml', 'setuptools==75.1.0', 'jupyter>=1.1.1', 'streamlit>=1.39.0', 'click==8.1.7', 'numpy==1.26.0', 'pip_audit==2.7.3', 'stdlib-list', 'nbformat', 'pandas', 'nbconvert==7.16.4', 'mkdocs-material==9.5.30', 'twine>=5.1.1'],
    classifiers=['Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'Programming Language :: Python :: 3.12', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering', 'Development Status :: 5 - Production/Stable'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kyrylo Mordan",
    author_email="parachute.repo@gmail.com",
    description="A tool to automate package creation within ci based on just .py and optionally .ipynb file.",
    keywords=['python', 'packaging', 'aa-paa-tool'],
    url="https://kiril-mordan.github.io/reusables/package_auto_assembler/",
    version="0.5.19",
    entry_points = {'console_scripts': ['paa = package_auto_assembler.cli:cli']},

    license = "mit",
    include_package_data = True,
    package_data = {'package_auto_assembler': ['mkdocs/**/*', 'artifacts/tools/**/*', 'artifacts/ppr_workflows/**/*', 'artifacts/package_licenses.json', 'artifacts/package_mapping.json', '.paa.tracking/version_logs.csv', '.paa.tracking/release_notes.md', '.paa.tracking/lsts_package_versions.yml', '.paa.tracking/notebook.ipynb', '.paa.tracking/package_mapping.json', '.paa.tracking/package_licenses.json', '.paa.tracking/.drawio', 'tests/**/*', '.paa.tracking/.paa.config', '.paa.tracking/python_modules/package_auto_assembler.py', '.paa.tracking/python_modules/components/paa_deps/mkdocs_handler.py', '.paa.tracking/python_modules/components/paa_deps/local_dependencies_handler.py', '.paa.tracking/python_modules/components/paa_deps/import_mapping_handler.py', '.paa.tracking/python_modules/components/paa_deps/ppr_handler.py', '.paa.tracking/python_modules/components/paa_deps/streamlit_handler.py', '.paa.tracking/python_modules/components/paa_deps/cli_handler.py', '.paa.tracking/python_modules/components/paa_deps/artifacts_handler.py', '.paa.tracking/python_modules/components/paa_deps/metadata_handler.py', '.paa.tracking/python_modules/components/paa_deps/long_doc_handler.py', '.paa.tracking/python_modules/components/paa_deps/fastapi_handler.py', '.paa.tracking/python_modules/components/paa_deps/setup_dir_handler.py', '.paa.tracking/python_modules/components/paa_deps/release_notes_handler.py', '.paa.tracking/python_modules/components/paa_deps/drawio_handler.py', '.paa.tracking/python_modules/components/paa_deps/version_handler.py', '.paa.tracking/python_modules/components/paa_deps/requirements_handler.py', '.paa.tracking/python_modules/components/paa_deps/tests_handler.py', '.paa.tracking/python_modules/components/paa_deps/dependencies_analyzer.py', '.paa.tracking/.paa.version']} ,
    )
