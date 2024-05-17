# Python Project README

This Python project assists in generating commit messages or updating Jira ticket descriptions based on specified prompts using a configured Gemini model.

## Files

### `prompts.py`

This file contains prompts used for generating content.

### `gen_model.py`

`gen_model.py` is responsible for generating content based on prompts and arguments passed in.

### `jira_api_client.py`

`jira_api_client.py` provides functionality for interacting with the Jira API, notably updating a Jira description.

### `utils.py`

`utils.py` contains general functionality.

### `main.py`

`main.py` serves as the entry point to the project and contains the main functionality.

## Required Credentials and Arguments

Ensure the following credentials and arguments are configured:

- `GOOGLE_API_KEY`: Google API key for Gemini model.
- `JIRA_DOMAIN`: Jira domain URL.
- `JIRA_EMAIL`: Jira account email.
- `JIRA_API_TOKEN`: Jira API token.

These credentials can be set as environment variables.

## Usage

### Running the Project

Ensure you are in an existing Git project directory with staged changes, as the project will use these changes to generate content.

Execute `main.py` with appropriate command-line arguments to perform the desired action:

python main.py <action> [--change-type <change_type>] [--verbose]

- <action>: Choose between "commit" to generate a commit message or "description" to update the Jira ticket description.
- --change-type: (Optional) Type of changes to fetch from Git: "staged" (default), "cached", or "all".
- --verbose: (Optional) Enable verbose (info) logging.

## Example Usage

Generate a commit message:

python main.py commit --verbose

Update the Jira ticket description:

python main.py description --verbose

## Dependencies

Ensure you have the following dependencies installed:

- Python 3.x
- [Google Gemini](https://pypi.org/project/google-generativeai/) (google-generativeai)