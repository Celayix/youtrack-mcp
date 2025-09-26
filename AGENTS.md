# Agent Instructions

- if the user's prompt mentions something with 'SXM-*' it means they are refering to a YouTrack issue ticket, thats the issue id.

- if the prompt only mention the issue id, it means you have to work on the issue, in that case, use the issue id from the prompt and the 'TOKEN' from the environment variable to run the '/youtrackapi.py' program, it will return issue title, desciption and any attachments, use those as your prompt and work on the the bug/feature. 