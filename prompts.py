COMMIT_MESSAGE_PROMPT = '''
Generate a concise Git commit message based on a set of changes.
The message should follow the format: 
Jira ticket number: (type of change): Brief description

Where: 
Jira ticket number (if it exists) is the ID of the relevant task. 
Type of change can be either 'fix' for bug fixes or 'feat' for new features. 
Brief description is a short, simple, non-repetitive, non-verbose, and directly relevant description of the changes made. It should always be in the present tense and one line long.

For example: "ABC-123: (feat): Add new feature" or "ABC-123: (fix): Patch bug".

If there is no Jira ticket, you can omit the ticket number from the commit message.
For example: "(feat): Add new feature" or "(fix): Patch bug".

Here is the Jira ticket number: {ticket_id}
Here is a list of the changes: 
{file_changes}
'''

TICKET_DESCRIPTION_PROMPT = '''
Generate a Jira ticket description, acceptance criteria, and test steps based on a set of changes.
**Summary:**
Summary of the changes made.

**Acceptance Criteria:**
Acceptance criteria for the changes made.

**Test Steps:**
Test steps to verify the changes made.

List of Changes:

The description should be a concise, clear, and direct summary of the changes made. 
The acceptance criteria should be a short list of conditions that must be met for the changes to be considered complete. They must be concise, clear, and directly related to the changes made.
The test steps should be a brief and simple outline of the steps needed to test the changes. It should be clear, concise, and directly related to the changes made.
The description and acceptance criteria should be relevant to the set of changes and written in a simple and professional tone.
Here is a list of the changes: {file_changes}
'''
