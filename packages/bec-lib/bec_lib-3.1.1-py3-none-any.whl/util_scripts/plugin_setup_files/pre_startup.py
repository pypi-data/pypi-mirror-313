"""
Pre-startup script for BEC client. This script is executed before the BEC client
is started. It can be used to add additional command line arguments. 
"""

from bec_lib.service_config import ServiceConfig


def extend_command_line_args(parser):
    """
    Extend the command line arguments of the BEC client.
    """

    # parser.add_argument("--session", help="Session name", type=str, default="cSAXS")

    return parser


# def get_config() -> ServiceConfig:
#     """
#     Create and return the service configuration.
#     """
#     return ServiceConfig(redis={"host": "localhost", "port": 6379})
