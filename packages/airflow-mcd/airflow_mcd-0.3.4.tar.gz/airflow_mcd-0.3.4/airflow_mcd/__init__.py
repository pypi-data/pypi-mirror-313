def get_provider_info():
    return {
        "name": "Monte Carlo",
        "description": "`Monte Carlo <https://www.montecarlodata.com/>`__\n",
        "connection-types": [
            {
                "hook-class-name": "airflow_mcd.hooks.SessionHook",
                "connection-type": "mcd",
            },
            {
                "hook-class-name": "airflow_mcd.hooks.GatewaySessionHook",
                "connection-type": "mcd_gateway",
            },
        ],
        "hook-class-names": [
            "airflow_mcd.hooks.SessionHook",
            "airflow_mcd.hooks.GatewaySessionHook",
        ],
        "package-name": "airflow-mcd",
    }
