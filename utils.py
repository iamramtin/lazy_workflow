import os
import re
import sys
import subprocess
import tempfile
import logging

# Configure logging
logging.basicConfig(format="%(levelname)s - %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

class Utils:
    def __init__(self, verbose=False):
        self._set_logging_level(verbose)

    def _set_logging_level(self, verbose):
        """
        Set logging level.
        """
        level = logging.DEBUG if verbose else logging.INFO
        logger.setLevel(level)

    def get_git_branch(self):
        """
        Get the current Git branch name.
        """
        try:
            result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True)
            branch_name = result.stdout.strip()
            logger.debug(f"Current Git branch: {branch_name}")
            return branch_name
        except subprocess.CalledProcessError as e:
            logger.error(f"Error getting Git branch: {e}")
            return None

    def get_ticket_id(self, branch_name):
        """
        Extract Jira ticket number from the Git branch name.
        """
        match = re.search(r'([A-Z]+-\d+)', branch_name)
        ticket_id = match.group(0) if match else None
        logger.debug(f"Extracted Jira ticket: {ticket_id}")
        
        return ticket_id

    def get_file_changes(self, change_type='staged'):
        """
        Get the list of changes from the Git repository.
        """
        change_types = {
            'staged': '--staged',
            'cached': '--cached',
            'all': 'HEAD'
        }

        if change_type not in change_types:
            raise ValueError("Invalid change type. Choose from 'staged', 'cached', or 'all'.")

        try:
            result = subprocess.run(["git", "diff", change_types[change_type]], capture_output=True, text=True)
            changes = result.stdout.strip()

            if not changes:
                logger.info(f"No {change_type} changes found.")
                sys.exit(0)
            logger.debug(f"Retrieved {change_type} changes.")
            return changes
        except subprocess.CalledProcessError as e:
            logger.error(f"Error getting Git changes: {e}")
            return None

    def edit_commit(self, content):
        """
        Open the Git commit editor with the generated content for editing.
        """
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            editor = os.environ.get('EDITOR', 'vi')
            logger.debug(f"Opening editor {editor} for commit message editing.")
            subprocess.run([editor, temp_file.name])

        # After editor is closed, read the edited content from the temporary file
        with open(temp_file.name, 'r') as edited_file:
            edited_content = edited_file.read()
        logger.debug("Commit message edited.")
        return edited_content

    def make_commit(self, content):
        """
        Make a commit with the provided commit message.
        """
        try:
            with subprocess.Popen(['git', 'commit', '-F', '-'], stdin=subprocess.PIPE) as proc:
                proc.communicate(input=content.encode())
            logger.info("Commit made successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error making commit: {e}")

    def prompt_user(self, gen_model, content, git_changes, ticket_id):
        """
        Prompt the user to accept the generated commit message, generate a new one, edit the message, or cancel.
        """
        print("\nGenerated commit message:")
        print(content)
        print("\nOptions:")
        print("1. Accept this message and commit.")
        print("2. Generate a new commit message.")
        print("3. Edit the generated commit message.")
        print("4. Cancel the commit.")

        choice = input("\nEnter your choice (1/2/3/4): ")

        if choice == '1':
            self.make_commit(content)
        elif choice == '2':
            new_content = gen_model.generate_commit_message(git_changes, ticket_id)
            self.prompt_user(gen_model, new_content, git_changes, ticket_id)
        elif choice == '3':
            edited_content = self.edit_commit(content)
            self.prompt_user(gen_model, edited_content, git_changes, ticket_id)
        elif choice == '4':
            sys.exit("\nCommit canceled.")
        else:
            print("\nInvalid choice. Please choose 1, 2, 3, or 4.")
            self.prompt_user(gen_model, content, git_changes, ticket_id)
