# Flask API for the Chemical Transformation Database

The API currently requires a config.json file, which has the format below.

```
{
    "ssh host address": "ssh_host_address",
    "ssh username": "ssh_username",
    "ssh password": "ssh_password",
    "sql username": "sql_username",
    "sql password": "sql_password",
    "remote bind address": "mysql_epa_url",
    "database" : "sbox_zchiodini_transdb_prototype"
}
```

This will be replaced with a login system in the future.

This API is functional. However, separating this API into two APIs, one for DSSTox and another for the Chemical Transformation Database is underway in the branches. The two distinct APIs will replace this single API.