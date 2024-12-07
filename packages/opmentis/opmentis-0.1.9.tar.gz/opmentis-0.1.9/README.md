# Opmentis

Opmentis is a Python package designed to manage user registrations within a decentralized application, allowing users to register as miners or validators. This package simplifies the process of user registration by providing a single function that can handle different user roles based on the presence of a stake.

## Features

- **User Registration**: Simplified user registration that supports different roles (miner or validator).
- **Scalable and Secure**: scalable and secure data storage.

## Installation

Install Opmentis using pip:

```bash
pip install opmentis
```

# Usage

### Registering as Miner
To register a new user as a miner:



```python
from opmentis import get_active_lab, register_user

# Fetch active lab information
active_lab = get_active_lab()
print("Active Lab Information:", active_lab)


# Register a user as a miner
wallet_address = "your_wallet_address"
labid = "your_lab_id"
role_type = "miner"
register_response = register_user(wallet_address, labid, role_type)
print("Registration Response:", register_response)

```


### Check your data
To check miners data:

```python
from opmentis import userdata, userpoint

# Example: check miners data
miner_wallet_address = "miner_wallet_address"
labid = "your_lab_id"
userdata(labid=labid, wallet_address=miner_wallet_address)

labid = "your_lab_id"
userpoint(labid, miner_wallet_address)

```
### Start new Chat
To end the current chat and update your points for the session, use the following code:

```python
from opmentis import endchat

# Example
endchat()

```

### Contributing
Contributions to Opmentis will be welcomed soon. 

### License


For more information and updates, contact the project maintainers @admin@opmentis.xyz 

