# Digital Commerce

A common package for digital commerce.

## Installation

Install using pip...

```shell
pip install git+https://github.com/ODCNC/digital-commerce.git
```

Add configurations to `.env` file

```shell
CAFE24_MALL_ID="<mall_id>"
CAFE24_CLIENT_ID="<public_key>"
CAFE24_CLIENT_SECRET="<private_key>"
CAFE24_VERSION="2021-03-01"
MONGO_URI="mongodb+src://<user_id>:<password>@<host>"
```

---

# Contribution

Install command-line tools and update requirements

```shell
pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt
```

### Test via pytest

```shell
pip install -r requirements-dev.txt
pytest --cov-report term-missing --cov=odcnc tests
```
