# zero-totp-db-model

<div align="center">
 <img src="https://github.com/SeaweedbrainCY/zero-totp-db-model/actions/workflows/publish.yml/badge.svg"> <img src="https://img.shields.io/github/v/tag/SeaweedbrainCY/zero-totp-db-model"/> <img src="https://img.shields.io/pypi/v/zero-totp-db-model"> <img src="https://img.shields.io/github/license/seaweedbraincy/zero-totp-db-model"/>
</div>
<br>

This is the repository of the shared database Model for all Zero-TOTP projects. The package is available on [PyPi](https://pypi.org/project/zero-totp-db-model/).

## About Zero-TOTP
Zero-TOTP is a secure Zero-TOTP authenticator based on Zero-Knowledge Encryption, 100% open source and giving user control over encryption, storage and availability.

To learn more, visit the main [repository](https://github.com/SeaweedbrainCY/zero-totp).

## Installation 
```bash
pip install zero-totp-db-model
```
> [!WARNING]
>  **DISCLAIMER :** Outside of the Zero-TOTP project, this package is not intended to be used. It is a shared model for all Zero-TOTP projects.
## Usage
First in your main app, initialize the model after the database has been initialized : 
```python
from zerp_totp_db_model.model_init import init_db
import SQLAlchemy

db = SQLAlchemy()
init_db(db) # mandatory to use model
```

Then you can import the model in your app and use it as you wish : 
```python
from zero_totp_db_model.model import User
```

## Contributing
If you already are a Zero-TOTP contributor, please feel free to contribute to this project.

If your are not yet, please start first contributing to the main Zero-TOTP project.

## Licence 
This project is under the MIT License.