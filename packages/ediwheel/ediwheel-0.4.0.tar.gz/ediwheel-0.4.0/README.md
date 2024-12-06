# Python EDIWHEEL - A Python package for data exchange in the tyre industry
#### DISCLAIMER: This is not an official EDIWHEEL package. It is a third-party implementation of the EDIWHEEL standard, and is in no way affiliated with any company or organization. Use at your own risk, no warranty is provided.


## Summary
This package is a Python implementation of the EDIWHEEL standard for data exchange in the tyre industry. It is based on the [EDIWHEEL standard](https://www.ediwheel.net/).

This standard uses XML requests to make stock inquiries and to place orders. The responses are also in XML format.

## Installation
The package can be installed using pip:
```
pip install ediwheel
```

## Usage
To use this package, you will need to obtain API authentication credentials from a given supplier.

A config is instantiated as such:
```python
from ediwheel import EdiConnectorConfig, EdiConnector

config = EdiConnectorConfig(
    host="https:/some_api_url.com",
    username="username",
    password="password",
    id="customer_id",
    timeout_s=10,
)

connector = EdiConnector(config)
connector.enquiry("EAN_CODE", "MANUFACTURER_CODE")

```

There is also a method available for batch queries, which performs better for large updates of stock.
Usually, the request will time out for large batches, therefore one must split large lists into smaller batches.
```python
results = connector.batch_enquiry(list_of_EANs, list_of_manufacturer_codes)

for ean, stock, delivery_date in results:
    print(ean, stock, delivery_date)
```


