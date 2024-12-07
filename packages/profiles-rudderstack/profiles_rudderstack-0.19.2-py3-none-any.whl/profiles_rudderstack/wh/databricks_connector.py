#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Databricks Connector."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from logging import Logger
from profiles_rudderstack.wh.connector_base import ConnectorBase, register_connector


@register_connector
class DatabricksConnector(ConnectorBase):
    REF_QUOTES = "`"

    @staticmethod
    def standardize_ref_name(ref_name: str) -> str:
        return ref_name.lower()

    @staticmethod
    def get_warehouse_config(config: dict):
        return {
            "user": config.get("user"),
            "host": config.get("host"),
            "port": config.get("port"),
            "http_endpoint": config.get("http_endpoint"),
            "access_token": config.get("access_token"),
            "catalog": config.get("catalog"),
            "schema": config.get("schema"),
        }

    def __init__(self, config: dict, **kwargs) -> None:
        self.logger = Logger("DatabricksConnector")
        super().__init__(config, **kwargs)

        creds = self.creds
        connection_string = f"databricks://token:{creds['access_token']}@{creds['host']}?http_path={creds['http_endpoint']}&catalog={creds['catalog']}&schema={creds['schema']}"
        self.engine = create_engine(connection_string)
        self.connection = Session(self.engine)

    def write_to_table(self, df, table_name, schema, if_exists):
        # not the best method to achieve this (performance wise)
        df.to_sql(name=table_name, con=self.engine,
                  schema=schema, index=False, if_exists=if_exists)
