import os
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
class ApiService:
    def _api_call(self,method,url,**kwargs):
        response = requests.request(method,url, **kwargs)
        print(response)
        return response
    def _basic_auth(self,email,token):
        auth = HTTPBasicAuth(email,token)
        print(auth)
        return auth


class JiraApiService(ApiService):

    """

    JIRA api service for creating and updating jira ticket

    """
    load_dotenv()
    def __init__(self):
        self.JIRA_HOST = "https://vivekvishalnitjsr.atlassian.net"
        #self.JIRA_URL = "https://vivekvishalnitjsr.atlassian.net/rest/api/3/issue"
        self.JIRA_API_ENDPOINT = "/rest/api/3/issue"
        #self.JIRA_URL_COMMENT = "https://vivekvishalnitjsr.atlassian.net/rest/api/3/issue/MCP-2/comment"
        self.EMAIL = "vivekvishalnitjsr@gmail.com"
        self.API_TOKEN = os.getenv("JIRA_API_TOKEN")
        self.PROJECT_KEY = "MCP"
        self.HEADERS = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def create_jira_ticket( self, summary: str, description: str ):
        """Create Jira

        Args:
            summary : Summary
            description: Description
        Return:
            id : Jira ID
            key : Jira Key related to project
            browse : link

            example : {'id': '10110', 'key': 'MCP-45', 'browse': 'https://vivekvishalnitjsr.atlassian.net//browse/MCP-45'}
        """
        payload = json.dumps({
            "fields": {
                "project":
                    {
                        "key": "MCP"
                    },
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "name": "Incident"
                             }
                      }
        })
        auth = self._basic_auth(self.EMAIL,self.API_TOKEN)
        url = self.JIRA_HOST + self.JIRA_API_ENDPOINT
        response = self._api_call("POST",url, headers=self.HEADERS, data=payload,auth=auth)


        if response.status_code == 201:
            response = (response.json())
            response.pop("self")
            response["browse"] = self.JIRA_HOST + "/browse/" + response["key"]

            return response
        else:
            return response.json()
    def add_jira_comment( self, key: str, comment: str ):
        """Create Jira

        Args:
            key : Jira Key where comment will be add
            comment: Comment to be updated in the jira key
        Return:
            message : "Comment Added"
            browse : link

            example : {'message': 'Comment Added', 'browse': 'https://vivekvishalnitjsr.atlassian.net/browse/MCP-58'}
        """
        payload = json.dumps({
            "body": {
                "content": [
                    {
                        "content": [
                            {
                                "text": comment,
                                "type": "text"
                            }
                        ],
                        "type": "paragraph"
                    }
                ],
                "type": "doc",
                "version": 1
            }

        })
        auth = self._basic_auth(self.EMAIL,self.API_TOKEN)
        url = self.JIRA_HOST + self.JIRA_API_ENDPOINT + "/" + key + "/comment"
        response = self._api_call("POST",url, headers=self.HEADERS, data=payload,auth=auth)

        if response.status_code == 201:
            response = (response.json())
            return ({
                "message" : "Comment Added",
                "browse": self.JIRA_HOST + "/browse/" + key
            })
        else:
            return ({
                "message" : "Failed adding comments"
            })


js = JiraApiService()
k=js.add_jira_comment("MCP-58","Connection Error")
print(k)