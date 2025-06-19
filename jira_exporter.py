#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any

from jira import JIRA
from jira.exceptions import JIRAError

class JiraTicketExporter:
    def __init__(self, server: str, username: str = None, api_token: str = None):
        """
        Initialize JIRA client with authentication.
        
        Args:
            server: JIRA server URL
            username: JIRA username
            api_token: JIRA API token
        """
        self.auth = (username, api_token) if username and api_token else None
        try:
            self.jira = JIRA(server=server, basic_auth=self.auth)
        except JIRAError as e:
            print(f"Failed to connect to JIRA: {e}")
            sys.exit(1)

    def get_all_tickets(self, project_key: str) -> List[Dict[str, Any]]:
        """
        Retrieve all tickets for a given project with their details.
        
        Args:
            project_key: The JIRA project key (e.g., 'PROJ')
            
        Returns:
            List of dictionaries containing ticket details
        """
        try:
            # JQL query to get all issues in the project
            issues = self.jira.search_issues(
                f'project = {project_key}',
                maxResults=False,  # Get all results
                expand='changelog'  # Include change history
            )
            
            tickets = []
            for issue in issues:
                ticket = {
                    'key': issue.key,
                    'title': issue.fields.summary,
                    'description': issue.fields.description or '',
                    'status': issue.fields.status.name,
                    'created': issue.fields.created,
                    'updated': issue.fields.updated,
                    'assignee': str(issue.fields.assignee) if issue.fields.assignee else None,
                    'reporter': str(issue.fields.reporter) if issue.fields.reporter else None,
                    'priority': str(issue.fields.priority) if hasattr(issue.fields, 'priority') and issue.fields.priority else None,
                    'comments': self._get_comments(issue),
                    'history': self._get_history(issue)
                }
                tickets.append(ticket)
            
            return tickets
            
        except JIRAError as e:
            print(f"Error fetching tickets: {e}")
            return []

    def _get_comments(self, issue) -> List[Dict[str, str]]:
        """Extract comments from an issue."""
        comments = []
        for comment in issue.fields.comment.comments:
            comments.append({
                'author': str(comment.author),
                'body': comment.body,
                'created': comment.created,
                'updated': comment.updated
            })
        return comments

    def _get_history(self, issue) -> List[Dict[str, Any]]:
        """Extract change history from an issue."""
        history = []
        for history_item in issue.changelog.histories:
            changes = []
            for item in history_item.items:
                changes.append({
                    'field': item.field,
                    'from': item.fromString,
                    'to': item.toString
                })
            
            history.append({
                'author': str(history_item.author),
                'created': history_item.created,
                'changes': changes
            })
        return history

    def export_to_json(self, project_key: str, output_file: str = None) -> None:
        """
        Export all tickets to a JSON file.
        
        Args:
            project_key: The JIRA project key
            output_file: Optional output file path (defaults to project_key + timestamp)
        """
        tickets = self.get_all_tickets(project_key)
        
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"{project_key}_tickets_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=2, ensure_ascii=False)
            print(f"Successfully exported {len(tickets)} tickets to {output_file}")
        except IOError as e:
            print(f"Error writing to file: {e}")
            sys.exit(1)

def main():
    """Main entry point with example usage."""
    # Get configuration from environment variables or use defaults
    JIRA_SERVER = os.getenv('JIRA_SERVER', "https://your-jira-instance.atlassian.net")
    JIRA_USERNAME = os.getenv('JIRA_USERNAME', "your-email@domain.com")
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN', "your-api-token")
    PROJECT_KEY = os.getenv('JIRA_PROJECT_KEY', "PROJ")
    
    if JIRA_SERVER == "https://your-jira-instance.atlassian.net":
        print("Warning: Using default JIRA_SERVER. Please set the JIRA_SERVER environment variable.")
    if JIRA_USERNAME == "your-email@domain.com":
        print("Warning: Using default JIRA_USERNAME. Please set the JIRA_USERNAME environment variable.")
    if JIRA_API_TOKEN == "your-api-token":
        print("Warning: Using default JIRA_API_TOKEN. Please set the JIRA_API_TOKEN environment variable.")
    if PROJECT_KEY == "PROJ":
        print("Warning: Using default JIRA_PROJECT_KEY. Please set the JIRA_PROJECT_KEY environment variable.")
    
    exporter = JiraTicketExporter(
        server=JIRA_SERVER,
        username=JIRA_USERNAME,
        api_token=JIRA_API_TOKEN
    )
    
    exporter.export_to_json(PROJECT_KEY)

if __name__ == "__main__":
    main()

