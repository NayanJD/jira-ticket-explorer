# JIRA Ticket Exporter

A Python script to export all tickets from a JIRA project into a JSON file. The export includes ticket titles, descriptions, comments, and complete change history.

## Features

- Exports all tickets from a specified JIRA project
- Includes comprehensive ticket information:
  - Title and description
  - Status and priority
  - Creation and update timestamps
  - Assignee and reporter
  - All comments with author and timestamps
  - Complete change history
- Outputs to a formatted JSON file
- Handles authentication via API token
- Includes error handling and proper encoding

## Prerequisites

- Python 3.6 or higher
- JIRA API token (see [Getting a JIRA API Token](#getting-a-jira-api-token))

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Getting a JIRA API Token

1. Go to your Atlassian Account Settings:
   - Visit https://id.atlassian.com/manage-profile/security
   - Log in if necessary

2. Create an API token:
   - Scroll to the "Security" section
   - Find "API tokens" or "Create and manage API tokens"
   - Click "Create API token"
   - Enter a meaningful label (e.g., "JIRA Ticket Exporter")
   - Click "Create"
   - Copy the token immediately (it's shown only once!)

## Configuration

Modify the following variables in `jira_exporter.py`:

```python
JIRA_SERVER = "https://your-jira-instance.atlassian.net"
JIRA_USERNAME = "your-email@domain.com"
JIRA_API_TOKEN = "your-api-token"
PROJECT_KEY = "PROJ"  # Your JIRA project key
```

Alternatively, you can use environment variables:
```bash
export JIRA_SERVER="https://your-jira-instance.atlassian.net"
export JIRA_USERNAME="your-email@domain.com"
export JIRA_API_TOKEN="your-api-token"
export JIRA_PROJECT_KEY="PROJ"
```

## Usage

Run the script:
```bash
python jira_exporter.py
```

The script will create a JSON file named `{PROJECT_KEY}_tickets_{timestamp}.json` containing all tickets with their details.

## Output Format

The exported JSON file will have the following structure:

```json
[
  {
    "key": "PROJ-123",
    "title": "Ticket title",
    "description": "Ticket description",
    "status": "In Progress",
    "created": "2023-06-19T10:00:00.000+0000",
    "updated": "2023-06-19T11:00:00.000+0000",
    "assignee": "John Doe",
    "reporter": "Jane Smith",
    "priority": "High",
    "comments": [
      {
        "author": "John Doe",
        "body": "Comment text",
        "created": "2023-06-19T10:30:00.000+0000",
        "updated": "2023-06-19T10:30:00.000+0000"
      }
    ],
    "history": [
      {
        "author": "Jane Smith",
        "created": "2023-06-19T11:00:00.000+0000",
        "changes": [
          {
            "field": "status",
            "from": "To Do",
            "to": "In Progress"
          }
        ]
      }
    ]
  }
]
```

## Error Handling

The script includes comprehensive error handling:
- Exits with an error if it can't connect to JIRA
- Skips any tickets that cause errors during fetching
- Exits with an error if it can't write to the output file
- Uses proper encoding for international characters

## Security Best Practices

- Never commit your API token to version control
- Store sensitive information in environment variables
- Regularly rotate your API tokens
- Revoke unused tokens from your Atlassian Account Settings

## Contributing

Feel free to submit issues and enhancement requests!

