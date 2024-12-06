"""Module for Session class handling project sessions."""
import os
from datetime import datetime, timedelta

from matrice.projects import Projects
from matrice.rpc import RPC
from matrice.utils import handle_response


class Session:
    """Class to manage sessions.

    Initialize a new session instance.

    Parameters
    ----------
    account_number : str
        The account number associated with the session.
    project_id : str, optional
        The ID of the project for this session.                          
    Example
    -------
    >>> session = Session(account_number="9625383462734064921642156")
    """

    def __init__(self, account_number, access_key, secret_key, project_id=None, project_name=None):
        # assert project_id, "project_id is empty"
        self.rpc = RPC(access_key, secret_key, project_id=project_id)
        self.account_number = account_number
        self.access_key = access_key
        self.secret_key = secret_key
        self.last_refresh_time = datetime.now()
        if project_id:
            self.project_id = project_id
        if project_name:
            self.project_name = project_name
        
    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        # Check if two minutes have passed since the last refresh
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")
        
        # Capture the current state
        init_params = {
            'account_number': self.account_number,
            'access_key': self.access_key,
            'secret_key': self.secret_key,
            'project_id': getattr(self, 'project_id', None),
            'project_name': getattr(self, 'project_name', None)
        }

        # Reinitialize the instance
        self.__init__(**init_params)

        # Update the last refresh time
        self.last_refresh_time = datetime.now()



    def update(self, project_id):
        """
        Update the session with new project details.

        Parameters
        ----------
        project_id : str, optional
            The new ID of the project.


        Example
        -------
        >>> session.update(project_id="660b96fc019dd5321fd4f8c7")
        """
        self.project_id = project_id
        self.rpc = RPC(access_key=self.access_key , secret_key = self.secret_key, project_id=project_id)

    def close(self):
        """
        Close the current session by resetting the RPC and project details.

        Example
        -------
        >>> session.close()
        """
        self.rpc = None
        self.project_id = None

    def _create_project(self, project_name, input_type, output_type):
        """
        Create a new project with specified parameters.

        Parameters
        ----------
        project_name : str
            The name of the project to be created.
        input_type : str
            The type of input for the project (e.g., 'image').
        output_type : str
            The type of output for the project (e.g., 'classification').

        Returns
        -------
        tuple
            A tuple containing the response data, error message (if any).

        Example
        -------
        >>> response, error = session._create_project("New Project", "image", "classification")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Project created with ID: {response['_id']}")
        """
        enabled_platforms = {
            "android": False,
            "ios": False,
            "tpu": False,
            "intelCPU": False,
            "gcloudGPU": False,
        }
        path = "/v1/project"
        headers = {"Content-Type": "application/json"}
        body = {
            "name": project_name,
            "inputType": input_type,
            "outputType": output_type,
            "enabledPlatforms": enabled_platforms,
            "accountType": "",
            "accountNumber": self.account_number,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)
        if resp.get("success"):
            resp_data = resp.get("data")
            return resp_data, None
        else:
            error = resp.get("message")
            return None, error

    def create_classification_project(self, project_name):
        """
        Create a classification project.

        Parameters
        ----------
        project_name : str
            The name of the classification project to be created.

        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.

        Example
        -------
        >>> project = session.create_classification_project("Image Classification Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        resp, error = self._create_project(
            project_name=project_name, input_type="image", output_type="classification"
        )

        if error is not None:
            print(f"Could not create project: \n {error}")
        else:
            P = Projects(session=self, project_name=resp["name"])
            return P

    def create_detection_project(self, project_name):
        """
        Create a detection project.

        Parameters
        ----------
        project_name : str
            The name of the detection project to be created.

        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.

        Example
        -------
        >>> project = session.create_detection_project("Object Detection Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        resp, error = self._create_project(
            project_name=project_name, input_type="image", output_type="detection"
        )
        if error is not None:
            print(f"Could not create project: \n {error}")
        else:
            P = Projects(session=self, project_name=resp["name"])
            return P

    def create_segmentation_project(self, project_name):
        """
        Create a segmentation project.

        Parameters
        ----------
        project_name : str
            The name of the segmentation project to be created.

        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.

        Example
        -------
        >>> project = session.create_segmentation_project("Instance Segmentation Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        resp, error = self._create_project(
            project_name=project_name,
            input_type="image",
            output_type="instance_segmentation",
        )
        if error is not None:
            print(f"Could not create project: \n {error}")
        else:
            P = Projects(session=self, project_name=resp["name"])
            return P

   

    def list_projects(self, project_type="", page_size=10, page_number=0):
        """
        List projects based on the specified type.

        Parameters
        ----------
        project_type : str, optional
            The type of projects to list (e.g., 'classification', 'detection'). If empty, all projects are listed.

        Returns
        -------
        tuple
            A tuple containing the dictionary of projects and a message indicating the result of the fetch operation.

        Example
        -------
        >>> projects, message = session.list_projects("classification")
        >>> print(message)
        Projects fetched successfully
        >>> for project_name, project_instance in projects.items():
        >>>     print(project_name, project_instance)
        """
        path = "/v1/project/v2"
        if project_type != "":
            path += f"?items[0][field]=outputType&items[0][operator]=is&items[0][value]={project_type}&pageSize={page_size}&pageNumber={page_number}"
        else:
            path += f"?pageSize={page_size}&pageNumber={page_number}"

        resp = self.rpc.get(path=path)
        if resp.get("success"):
            projects_data = resp.get("data", {}).get("items", [])
            projects = {project["name"]: Projects(session=self, project_name=project["name"]) for project in projects_data}
            return projects, "Projects fetched successfully"
        else:
            message = resp.get("message")
            return {}, f"Failed to fetch projects: \n {message}"

    def get_project_type_summary(self):
        """
        Get the count of different types of projects.

        Returns
        -------
        tuple
            A tuple containing:
            - A dictionary with project types as keys and their counts as values if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> project_summary, error = session.get_project_type_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Project type summary: {project_summary}")
        """
        path = "/v1/project/get_projects_count_by_type"
        resp = self.rpc.get(path=path)
        print(resp)
        data, error, message = handle_response(
            resp,
            "Successfully fetched project type summary",
            "An error occurred while fetching project type summary",
        )

        if error:
            return {}, error
        
        # Extract the project type summary from the response data
        project_type_summary = data

        # Return the project type summary as a dictionary
        return project_type_summary, None   


    def create_session(account_number, access_key, secret_key):
        """
        Create and initialize a new session with specified credentials.

        Parameters
        ----------
        account_number : str
            The account number to associate with the new session.
        access_key : str
            The access key for authentication.
        secret_key : str
            The secret key for authentication.

        Returns
        -------
        Session
            An instance of the Session class initialized with the given credentials.

        Example
        -------
        >>> session = create_session("9625383462734064921642156", "HREDGFXB6KI0TWH6UZEYR", "UY8LP0GQRKLSFPZAW1AUF")
        >>> print(session)
        <Session object at 0x...>
        """
        S = Session(account_number=account_number, access_key=access_key, secret_key=secret_key)
        return S
