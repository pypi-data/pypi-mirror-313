this is my in house library for interacting with Zimra's FDMS system 
# Fiscal Device Gateway API Client

This repository provides a Python client for interacting with the Fiscal Device Gateway API provided by ZIMRA. The client can be used to manage various operations related to fiscal devices, such as registering a device, fetching configurations, issuing certificates, and handling fiscal day operations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Class Methods](#class-methods)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this client, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/lordskyzw/zimra.git
cd zimra
pip install -r requirements.txt
```

## Usage

You can use the `Device` class to interact with the Fiscal Device Gateway API. Below is an example of how to initialize the class and perform some operations.

### Example

```python
from zimra import Device

# Initialize the device in test mode
device = Device(test_mode=True)

# Get the configuration of the device
config_status = device.getConfig()
print(config_status)

# Open a fiscal day
fiscal_day_status = device.openDay(fiscalDayNo=102)
print(fiscal_day_status)
```

## Class Methods

### `__init__(self, test_mode=False, *args)`

Initializes the Device class. 

- `test_mode`: Boolean to specify whether to use the test environment or production environment.

### `register(self)`

Registers the device.

### `verifyTaxpayerInformation(self)`

Verifies the taxpayer information associated with the device.

### `getConfig(self)`

Fetches the device configuration and updates the device attributes.

### `issueCertificate(self)`

Issues a certificate for the device.

### `getStatus(self)`

Gets the current status of the device.

### `openDay(self, fiscalDayNo, fiscalDayOpened=None)`

Opens a fiscal day.

### `submitReceipt(self, receiptData)`

Submits a receipt to the fiscal device gateway.

### `closeDay(self)`

Closes the fiscal day.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
