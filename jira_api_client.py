import os
import requests
import logging
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(format="%(levelname)s - %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

class JiraClient:
    def __init__(self, domain, email=None, api_token=None, verbose=False):
        self.domain = domain
        self.email = email or os.getenv('JIRA_EMAIL')
        self.api_token = api_token or os.getenv('JIRA_API_TOKEN')
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        self._set_logging_level(verbose)
        self._configure()

    def _configure(self):
        """
        Configure the Jira client with domain, email, and API token.
        """
        if not self.email:
            logger.error("JIRA_EMAIL is not set.")
            raise ValueError("JIRA_EMAIL is not set.")
        
        if not self.api_token:
            logger.error("JIRA_API_TOKEN is not set.")
            raise ValueError("JIRA_API_TOKEN is not set.")
        self._check_domain()

    def _set_logging_level(self, verbose):
        """
        Set logging level.
        """
        level = logging.DEBUG if verbose else logging.INFO
        logger.setLevel(level)

    def _check_domain(self):
        """
        Check if the JIRA domain is reachable.
        """
        try:
            response = requests.get(self.domain, headers=self.headers)
            if response.status_code != 200:
                logger.error(f"Failed to reach JIRA domain: {self.domain}")
                response.raise_for_status()
            logger.debug("JIRA domain is reachable.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error reaching JIRA domain: {e}")
            raise

    def get_issue(self, ticket_id):
        """
        Get issue details from JIRA.
        """
        url = f"{self.domain}/rest/api/2/issue/{ticket_id}"
        try:
            response = requests.get(url, headers=self.headers, auth=self.auth)
            response.raise_for_status()
            logger.debug(f"Fetched issue details for ticket {ticket_id}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch issue details for {ticket_id}: {e}")
            raise


    def update_issue_description(self, ticket_id, description):
        """
        Update the issue description in JIRA.
        """
        self._check_ticket_exists(ticket_id)
        url = f"{self.domain}/rest/api/2/issue/{ticket_id}"
        payload = {
            "fields": {
                "description": description
            }
        }

        try:
            response = requests.put(url, headers=self.headers, auth=self.auth, json=payload)
            response.raise_for_status()
            logger.info(f"Updated description for ticket {ticket_id}: \n{description}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to update description for {ticket_id}: {e}")
            raise

    def get_current_description(self, ticket_id):
        """
        Get the current description of the issue from JIRA.
        """
        issue_details = self.get_issue(ticket_id)
        description = issue_details["fields"]["description"]
        logger.debug(f"Retrieved current description for ticket {ticket_id}.")
        
        return description

    def _check_ticket_exists(self, ticket_id):
        """
        Check if the ticket exists.
        """
        try:
            self.get_issue(ticket_id)
            logger.debug(f"Ticket {ticket_id} exists.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ticket {ticket_id} does not exist: {e}")
            raise
