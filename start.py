"""
Setup/Start utility for the Quil Evaluator Server
"""

import configparser
import sys
import argparse
from index import APP

def setup_api_key(apikey):
    """
    Write a Forest API Key to the local file system if needed
    """
    config = configparser.ConfigParser()
    config.read('.pyquil_config_template')
    config['Rigetti Forest']['key'] = apikey

    with open('.pyquil_config', 'w') as configfile:
        config.write(configfile)

    print """
    Your .pyquil_config was updated with the above API Key.
    To change your API Key, please re-run: 'python start.py --setup'
    """

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description="Start Quil Evaluator Web App")
    PARSER.add_argument(
        "-s",
        "--setup",
        action="store_true",
        help="Using this flag will setup Forest API key"
    )
    ARGS = PARSER.parse_args()
    if ARGS.setup:
        API_KEY = raw_input("\nPlease enter your Forest API Key: ")
        setup_api_key(API_KEY)
        sys.exit(1)

    # default behavior is to just run the app from index.py
    APP.run()
