import os
import sys
import argparse
import logging
from gen_model import GenModel
from jira_api_client import JiraClient
from prompts import COMMIT_MESSAGE_PROMPT, TICKET_DESCRIPTION_PROMPT
from utils import Utils

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
JIRA_DOMAIN = "https://your-domain.atlassian.net"
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

# Configure logging
logging.basicConfig(format="%(levelname)s - %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Generate a commit message or update the Jira ticket description.")
    parser.add_argument("action", choices=["commit", "description"], help="Action to perform: 'commit' to generate a commit message or 'description' to update the Jira ticket description.")
    parser.add_argument("--change-type", choices=["staged", "cached", "all"], default="staged", help="Type of changes to fetch from Git: 'staged' (default), 'cached', or 'all'.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose (info) logging.")

    return parser.parse_args()

if __name__ == '__main__':
    # Parse command-line arguments
    args = parse_arguments()

    # Configure Gemini client
    gen_model = GenModel(api_key=GOOGLE_API_KEY, verbose=args.verbose)

    # Configure utility functions
    utils = Utils(verbose=args.verbose)

    file_changes = utils.get_file_changes(args.change_type)
    branch_name = utils.get_git_branch()
    ticket_id = utils.get_ticket_id(branch_name)

    # Perform action based on command-line argument
    if args.action == "commit":
        # content = gen_model.generate_commit_message(file_changes, ticket_id)
        content = gen_model.generate_from_prompt(COMMIT_MESSAGE_PROMPT, ticket_id=ticket_id, file_changes=file_changes)
        utils.prompt_user(gen_model, content, file_changes, ticket_id)
    
    elif args.action == "description":
        
        if not ticket_id:
            logger.error("Cannot update Jira ticket description: no ticket found in the branch name.")
            sys.exit(1)
        
        description = gen_model.generate_from_prompt(TICKET_DESCRIPTION_PROMPT, file_changes=file_changes)

        # Configure Jira client
        jira_client = JiraClient(domain=JIRA_DOMAIN, email=JIRA_EMAIL, api_token=JIRA_API_TOKEN, verbose=args.verbose)
        jira_client.update_issue_description(ticket_id, description)
