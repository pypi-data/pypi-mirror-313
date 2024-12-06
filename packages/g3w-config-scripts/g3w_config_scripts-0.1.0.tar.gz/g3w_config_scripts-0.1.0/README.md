## G3W Configuration Scripts

This repository contains the scripts to quickly configure a G3W-SUITE instance.


### Installation

Install the module via pip:

```bash
pip install g3w_config_scripts
```

### Usage

```bash
g3w_dev_setup configure.properties
```

Where the configuration file is a properties file with the following structure:

```properties
SUITE_REPO_TAG: v3.8.0
SUITE_DOCKER_IMAGE: g3wsuite/g3w-suite:v3.8.x
MY_NEW_BRANCH: v3.8.0_myniceproject
SUITE_SHARED_VOLUME: /myniceproject/
DEBUG: True
FRONTEND: False

# optional plugin setup. Comment out completely to skip
PLUGIN_APP_NAME=myplugin
PLUGIN_REPO=https://github.com/myname/myplugin.git

WEBGIS_PUBLIC_HOSTNAME: v38.g3wsuite.it
G3WSUITE_POSTGRES_PASS: myPgPasswd
PG_SERVICE_CONF: [service@111.111.11.111]|host=111.111.11.111user=myuser|password=mypwd|dbname=mydb|port=5432
```
