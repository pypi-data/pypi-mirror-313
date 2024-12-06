import logging
from eo4eu_data_utils.config import ConfigBuilder, Try


logging.basicConfig()

data = {
    "host": {
        "port": 9100,
        # "https": False,
    },
    "client": {
        "max_attempts": 5,
        "name": "myself",
    },
}

config_builder = ConfigBuilder(
    yes = "Yes",
    no = "No",
    web = dict(
        port  = Try.option("host", "port"),
        https = Try.option("host", "https").default(True).to_bool(),
        sec   = Try.parent("web", "https")
                   .ifelse(Try.parent("yes"), Try.parent("no"))
    ),
    client_port = Try.option("client", "port").or_parent("web", "port"),
    client_name = Try.option("client", "name").format("client_{}"),
    also_client = Try.create(
        lambda a, b: (a, b),
        Try.option("client", "name"),
        Try.option("client", "last_name").default("unknown"),
    ),
)

try:
    config = config_builder.use_dict(data).build()
    print(config)
    print(config.web.https)
except Exception as e:
    print(str(e))
