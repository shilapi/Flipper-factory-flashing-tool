# Flipper Factory Flashing Tool

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/shilapi/Flipper-factory-flashing-tool)](LICENSE)
[![Issues](https://img.shields.io/github/issues/shilapi/Flipper-factory-flashing-tool)](https://github.com/shilapi/Flipper-factory-flashing-tool/issues)
[![Stars](https://img.shields.io/github/stars/shilapi/Flipper-factory-flashing-tool?style=social)](https://github.com/shilapi/Flipper-factory-flashing-tool/stargazers)

A lightweight script designed for flashing the **Flipper Zero**. Also supports writing keys into the **CKS area** (secure enclave). 

## Features

- Flash firmware onto Flipper Zero effortlessly.

- Securely write keys into the CKS area.

- Simple configuration via `config.yaml`.

## Prerequisites

Make sure the following requirements are met before running the script:

1. **STM32 Cube Programmer CLI** is installed and added to your PATH.

   - Verify installation with:

     ```bash
     STM32_Programmer_CLI --version
     ```

2. Python dependencies are installed (see the instructions below).

## Usage

1. Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Edit the config.yaml file to suit your needs.

3. Run the script:

    ```bash
    python main.py
    ```
