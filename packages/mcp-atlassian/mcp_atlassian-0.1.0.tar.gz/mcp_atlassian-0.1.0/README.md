# mcp-atlassian

MCP server to interact with Atlassian products (currently supporting Confluence).

## Features

### Tools

- search_confluence: Search Confluence content using natural language
- get_page_content: Get content of a specific Confluence page
- get_page_comments: Get comments for a specific page

### Example prompts

- "Search for all documentation related to authentication and summarize the key points"
- "Get the content of the onboarding guide and create a checklist from it"
- "Find all comments on the project requirements page and highlight any concerns raised"

## Setup

### Requirements

Create a `.env` file with:
```
CONFLUENCE_CLOUD_URL=your_confluence_url
CONFLUENCE_CLOUD_USER=your_username
CONFLUENCE_CLOUD_TOKEN=your_api_token
```

To get an API token:
1. Log in to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click Create API token
3. Enter a memorable Label for your token and click Create
4. Click Copy to clipboard to save your token securely

### Claude Desktop Configuration

Location:
- MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Configuration:
```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uv",
      "args": [
        "--directory",
        "<dir_to>/mcp-atlassian",
        "run",
        "mcp-atlassian"
      ],
      "env": {
        "CONFLUENCE_CLOUD_URL": "your_confluence_url",
        "CONFLUENCE_CLOUD_USER": "your_username",
        "CONFLUENCE_CLOUD_TOKEN": "your_api_token"
      }
    }
  }
}
```

## Development

### Building

```bash
# Install dependencies
uv sync

# Build package
uv build

# Publish to PyPI
uv publish
```

### Debugging

Use MCP Inspector:
```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/mcp-atlassian run mcp-atlassian
```

View logs:
```bash
tail -n 20 -f ~/Library/Logs/Claude/mcp-server-mcp-atlassian.log
```

## Todo

- [ ] Jira integration
