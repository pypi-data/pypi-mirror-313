import argparse


def parse_arguments():
    """
    Parses command-line arguments for the TTXT_V2 Framework.

    Returns:
        argparse.Namespace: Parsed command-line arguments with the following attributes:
            --c, --config (str): Path to client config file. This argument is not required we have set
            default file to: connector_config.json
    """
    parser = argparse.ArgumentParser(description="TTXT_V2 Framework argument parser")
    parser.add_argument(
        "--c", "--config", required=False, help="Path to TTXT_V2 framework config file"
    )
    return parser.parse_args()
