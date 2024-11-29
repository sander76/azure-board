# import requests
# from base64 import b64encode

# def create_work_item(organization, project, personal_access_token, title, description, work_item_type="Task"):
#     """
#     Creates a work item in Azure Boards

#     Parameters:
#     organization (str): Azure DevOps organization name
#     project (str): Project name
#     personal_access_token (str): Azure DevOps PAT
#     title (str): Title of the work item
#     description (str): Description of the work item
#     work_item_type (str): Type of work item (Task, Bug, User Story, etc.)

#     Returns:
#     dict: Response from the API containing the created work item details
#     """

#     # API URL
#     url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/${work_item_type}?api-version=6.0"

#     # Create authorization header
#     auth = b64encode(f":{personal_access_token}".encode()).decode()

#     # Headers
#     headers = {
#         'Content-Type': 'application/json-patch+json',
#         'Authorization': f'Basic {auth}'
#     }

#     # Request body
#     body = [
#         {
#             "op": "add",
#             "path": "/fields/System.Title",
#             "value": title
#         },
#         {
#             "op": "add",
#             "path": "/fields/System.Description",
#             "value": description
#         }
#     ]

#     try:
#         # Make the POST request
#         response = requests.post(url, json=body, headers=headers)
#         response.raise_for_status()  # Raise an exception for bad status codes

#         return response.json()

#     except requests.exceptions.RequestException as e:
#         print(f"Error creating work item: {e}")
#         return None

# # Example usage:
# if __name__ == "__main__":
#     # Replace these values with your own
#     organization = "your-organization"
#     project = "your-project"
#     personal_access_token = "your-pat"

#     title = "Sample Work Item"
#     description = "This is a test work item created using Python"

#     result = create_work_item(
#         organization=organization,
#         project=project,
#         personal_access_token=personal_access_token,
#         title=title,
#         description=description,
#         work_item_type="Task"  # Can be "Task", "Bug", "User Story", etc.
#     )

#     if result:
#         print(f"Work item created successfully. ID: {result['id']}")
#     else:
#         print("Failed to create work item")
# ```

# To use this function, you'll need to:

# 1. Install the requests library if you haven't already:
# ```bash
# pip install requests
# ```

# 2. Get your Azure DevOps Personal Access Token (PAT):
#    - Go to Azure DevOps
#    - Click on your profile picture
#    - Select "Personal access tokens"
#    - Create a new token with "Work Items (read, write)" permissions

# 3. Replace the placeholder values in the example usage:
#    - `organization`: Your Azure DevOps organization name
#    - `project`: Your project name
#    - `personal_access_token`: Your PAT
#    - `title`: The title for your work item
#    - `description`: The description for your work item
#    - `work_item_type`: The type of work item you want to create

# Additional features you can add to the function:

# 1. Add more fields to the work item:
# ```python
# # Add to the body list
# {
#     "op": "add",
#     "path": "/fields/System.AssignedTo",
#     "value": "user@example.com"
# },
# {
#     "op": "add",
#     "path": "/fields/System.State",
#     "value": "New"
# },
# {
#     "op": "add",
#     "path": "/fields/System.Priority",
#     "value": 2
# }
# ```

# 2. Add error handling for specific status codes:
# ```python
# if response.status_code == 401:
#     print("Authentication failed. Check your PAT.")
# elif response.status_code == 403:
#     print("You don't have permission to create work items.")
# ```

# 3. Add support for attachments:
# ```python
# def add_attachment(organization, project, personal_access_token, work_item_id, file_path):
#     # First, upload the file
#     upload_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/attachments?fileName={os.path.basename(file_path)}&api-version=6.0"
#     # Then, link it to the work item
#     # Implementation details omitted for brevity
# ```

