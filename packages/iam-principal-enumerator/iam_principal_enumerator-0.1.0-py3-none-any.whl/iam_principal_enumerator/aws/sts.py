"""
STS utility functions.

This module provides utility functions for working with AWS STS, including
retrieving the current AWS account ID.
"""

import sys

from loguru import logger
from mypy_boto3_sts import STSClient
from botocore.exceptions import BotoCoreError, ClientError

logger.remove()
logger.add(sys.stderr, level="INFO")


def get_current_account_id(client: STSClient) -> str:
    """
    Get the current AWS account ID.

    :param client: Boto3 STS client
    :return: AWS account ID as a string
    """
    try:
        account_id = client.get_caller_identity()["Account"]
        logger.info(f"Current account ID: {account_id}")
        return account_id
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Error getting account ID: {e}")
        raise
