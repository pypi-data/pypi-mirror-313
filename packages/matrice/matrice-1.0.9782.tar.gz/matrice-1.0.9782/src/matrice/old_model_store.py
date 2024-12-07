from matrice.utils import handle_response
import os
import json
from datetime import datetime, timedelta

def list_public_model_families(session, project_type="classification", page_size=10, page_num=0):
    """
    Fetch public model families for a given project.

    Parameters
    ----------
    project_type : str, optional
        The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").
    page_size : int, optional
        The number of model families to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_public_model_families(session,"classification")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Public model families: {resp}")
    """
    path = f"/v1/model_store/list_public_model_families?projectType={project_type}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched all public model families",
        "An error occured while fetching the public model families",
    )

def list_private_model_families(session, project_id=None, project_name=None, page_size=10, page_num=0): 
    """
    Fetch private model families for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_name : str
        The name of the project.
    page_size : int, optional
        The number of model families to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_private_model_families(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Private model families: {resp}")
    """
    assert project_id is not None or project_name is not None

    path = f"/v1/model_store/list_private_model_families?projectId={project_id}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched all private model families",
        "An error occured while fetching the private model families",
    )

def list_public_model_archs(session, project_type="classification", page_size=10, page_num=0): 
    """
    Fetch public model architectures for a given project.

    Parameters
    ----------
    project_type : str, optional
        The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").
    page_size : int, optional
        The number of model architectures to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_public_model_archs(session,"classification")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Public model architectures: {resp}")
    """
    path = f"/v1/model_store/list_public_model_archs?projectType={project_type}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched all public model architectures",
        "An error occured while fetching the public model architectures",
    )

def list_private_model_archs(session, project_id=None, project_name=None, page_size=10, page_num=0): 
    """
    Fetch private model architectures for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_name : str
        The name of the project.
    page_size : int, optional
        The number of model architectures to fetch per page (default is 10).
    page_num : int, optional
        The page number to fetch (default is 0).

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = list_private_model_archs(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Private model architectures: {resp}")
    """
    assert project_id is not None or project_name is not None

    path = f"/v1/model_store/list_private_model_archs?projectId={project_id}&pageSize={page_size}&pageNum={page_num}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched all private model architectures",
        "An error occured while fetching the private model architectures",
    )

def _get_all_models(session, project_id=None, project_name=None, project_type="classification"): 
    """
    Fetch all models for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_type : str, optional
        The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = get_all_models(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"All models: {resp}")
    """
    path = f"/v1/model_store/get_all_models?projectId={project_id}&projectType={project_type}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched all model infos",
        "An error occured while fetching the model family",
    )

def _get_all_model_families(session , project_id, project_name=None, project_type="classification"): 
    """
    Fetch all model families for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_type : str, optional
        The type of the project (default is "classification").

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = get_all_model_families(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"All model families: {resp}")
    """
    path = f"/v1/model_store/get_all_model_families?projectId={project_id}&projectType={project_type}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched all model family",
        "An error occured while fetching the model family",
    )

def byom_status_summary(session, project_id, project_name): 
    """
    Fetch the BYOM (Bring Your Own Model) status summary for a given project.

    Parameters
    ----------
    project_id : str
        The ID of the project.
    project_name : str
        The name of the project.

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = byom_status_summary(session,"66912342583678074789d")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"BYOM status summary: {resp}")
    """
    path = f"/v1/model_store/byom_status_summary?projectId={project_id}"
    resp = session.rpc.get(path=path)

    return handle_response(
        resp,
        "Successfully fetched the BYOM status summary",
        "An error occured while fetching the BYOM status summary",
    )

# Check if the model family already exists publicly or within the project
def check_family_exists_by_name(session, family_name): 
    """
    Check if a model family exists by its name.

    Parameters
    ----------
    session : Session
        The session object containing authentication information.
    family_name : str
        The name of the model family to check.

    Returns
    -------
    bool
        True if the model family exists, False otherwise.
        
    Example
    -------
    >>> session = Session(account="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
    >>> family_name = "ResNet"
    >>> exists = check_family_exists_by_name(session, family_name)
    >>> if exists:
    >>>     print(f"The model family '{family_name}' exists.")
    >>> else:
    >>>     print(f"The model family '{family_name}' does not exist.")
    """
    path = f"/v1/model_store/check_family_exists_by_name?familyName={family_name}"
    resp = session.rpc.get(path=path)

    data, error, message = handle_response(
        resp,
        "Successfully checked model family existence",
        "An error occurred while checking model family existence",
    )

    if error:
        return False

    return data.get("exists", False)


def fetch_supported_runtimes_metrics(session, project_id, model_inputs, model_outputs):
    """
    Fetch supported runtimes and metrics for a given project.

    Parameters
    ----------
    model_inputs : list
        List of model inputs.
    model_outputs : list
        List of model outputs.

    Returns
    -------
    tuple
        A tuple containing the response data, error (if any), and message.

    Example
    -------
    >>> resp, error, message = fetch_supported_runtimes_metrics(session,["image"], ["classification"])
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Supported runtimes and metrics: {resp}")
    """
    path = f"/v1/model_store/fetch_supported_runtimes_metrics?projectId={project_id}"
    payload = {
        "modelInputs": model_inputs,
        "modelOutputs": model_outputs,
    }
    headers = {"Content-Type": "application/json"}
    resp = session.rpc.post(path=path, headers=headers, payload=payload)

    data, error, message = handle_response(
        resp,
        "Successfully fetched supported runtimes and metrics",
        "An error occurred while fetching supported runtimes and metrics",
    )

    if error:
        return data, error, message

    runtimes = data

    return runtimes, error, message

def get_automl_config(session , project_id , experiment_id , model_count , recommended_runtime , performance_tradeoff , tuning_type="auto"):
    
    """
    Generate AutoML configurations for model training based on specified parameters.

    This static method fetches recommended model configurations from the backend and
    processes them into a format suitable for model training. It calculates the 
    number of model variants based on hyperparameter combinations.

    Parameters
    ----------
    session : Session
        Active session object for making API calls
    project_id : str
        Identifier for the project
    experiment_id : str
        Identifier for the experiment
    model_count : int
        Number of models to request configurations for
    recommended_runtime : bool
        Flag to indicate whether to only include models within recommended runtime
    performance_tradeoff : float
        Value indicating the trade-off between performance and resource usage
    tuning_type : str, optional
        Type of hyperparameter tuning strategy (default: "auto")

    Returns
    -------
    tuple
        A tuple containing three elements:
        - model_archs (list): List of ModelArch instances for recommended models
        - configs (list): List of configuration dictionaries for each model
          Each config contains:
            - is_autoML (bool): Set to True for AutoML
            - tuning_type (str): Type of tuning strategy
            - model_checkpoint (str): Checkpoint configuration
            - checkpoint_type (str): Type of checkpoint
            - action_config (dict): Raw configuration parameters
            - model_config (dict): Processed configuration values
        - model_counts (list): List of integers representing the number of
          model variants for each model based on hyperparameter combinations

    Example
    -------
    >>> session = Session()
    >>> model_archs, configs, counts = get_automl_config(
    ...     session=session,
    ...     project_id="project123",
    ...     experiment_id="exp456",
    ...     model_count=5,
    ...     recommended_runtime=True,
    ...     performance_tradeoff=0.7
    ... )
    >>> for arch, config, count in zip(model_archs, configs, counts):
    ...     print(f"Model: {arch.model_key}, Variants: {count}")
    ...     print(f"Config: {config}")

    Notes
    -----
    The number of model variants (model_counts) is calculated by multiplying the
    number of unique values for batch size, epochs, and learning rate for each model.
    This represents the total number of training configurations that will be generated
    for each model architecture.
    """
    
    payload = {
        "_idExperiment": experiment_id,
        "_idProject": project_id,
        "recommendedOnly": recommended_runtime,
        "modelCount": model_count,
        "performanceTradeoff": performance_tradeoff,
        "searchType": tuning_type,
    }
    
    path = f"/v1/model_store/get_recommended_models/v2?projectId={project_id}"
    headers = {"Content-Type": "application/json"}
    resp = session.rpc.post(
        path=path, headers=headers, payload=payload
    )
    model_archs = []
    configs = []
    model_counts = []
    
    
    for model_data in resp.get("data", []):
        model_key = model_data.get("modelKey")
        model_family_name = model_data.get("modelFamilyName")
        action_config_list = model_data.get("actionConfig", [])
        
        print(model_key)
        print(model_family_name)
        
        # Extract the action_config and model_config from the response
        action_config = {item["keyName"]: item for item in action_config_list}
        model_config = {item["keyName"]: item["selectedValues"] for item in action_config_list}

        # Calculate the total model count for this model
        batch_size_count = len(model_config.get("batch", [1]))
        epochs_count = len(model_config.get("epochs", [1]))
        learning_rate_count = len(model_config.get("learning_rate", [1]))
        model_specific_count = batch_size_count * epochs_count * learning_rate_count
        print(model_specific_count)
        model_counts.append(model_specific_count)

        # Construct the new model configuration structure
        config = {
            'is_autoML': True,
            'tuning_type': tuning_type,
            'model_checkpoint': "auto",
            'checkpoint_type': 'predefined',
            'action_config': action_config,
            'model_config': model_config
        }
        
        model_arch = ModelArch(session=session, model_family_name=model_family_name, model_key=model_key)
        model_archs[model_key] = model_arch
        model_archs.append(model_arch)
        configs.append(config)

    return model_archs, configs , model_counts
    
class ModelArch:
    
    """
    A class to interact with model architectures through the model architecture API.

    This class handles fetching and storing model architecture information, including
    configuration parameters, export formats, and other model metadata.

    Parameters
    ----------
    session : Session
        Active session object for making API calls
    model_family_name : str
        Name of the model family this architecture belongs to
    model_key : str
        Unique identifier key for the model architecture

    Attributes
    ----------
    account_number : str
        Account number from the session
    project_id : str
        Project identifier from the session
    model_family_name : str
        Name of the model family
    model_key : str
        Model's unique identifier key
    last_refresh_time : datetime
        Timestamp of last data refresh
    rpc : RPCClient
        RPC client object from session for API calls
    model_info_id : str or None
        Model information unique identifier
    model_name : str or None
        Human readable name of the model
    model_family_id : str or None
        Unique identifier of the model family
    params_millions : float or None
        Number of parameters in millions
    export_formats : list or None
        List of supported export formats
    model_config : dict or None
        Default configuration parameters for model training

    Notes
    -----
    Upon initialization, the class automatically fetches:
    - Model information using _get_model_info()
    - Training configuration using get_model_train_config()
    - Export formats using get_export_formats()

    If model_key is not provided, these fetches are skipped and the class 
    initializes with minimal information.

    Example
    -------
    >>> session = Session()
    >>> model = ModelArch(
    ...     session=session,
    ...     model_family_name="resnet",
    ...     model_key="resnet50"
    ... )
    >>> print(f"Model: {model.model_name}")
    >>> print(f"Parameters: {model.params_millions}M")
    >>> print(f"Export formats: {model.export_formats}")

    Raises
    ------
    AssertionError
        If model_key or model_family_name is None
    """
    def __init__(self, session, model_family_name, model_key):
        self.session = session
        self.account_number = session.account_number
        assert model_key is not None, "Model key must be provided"
        assert model_family_name is not None, "Model family name must be provided"
        self.model_family_name=model_family_name
        self.project_id = session.project_id
        self.last_refresh_time = datetime.now()
        self.rpc = session.rpc
        self.model_key = model_key
        self.model_info_id = None
        
        if model_key is not None: 
            model_info, error , message= self._get_model_info()
            model_train_config , error , message = self.get_model_train_config()
            export_formats ,error , message = self.get_export_formats()
        else:
            print("Class initialized without model info")
                
        self.model_info_id = model_info["_id"]
        self.model_name = model_info["modelName"]
        self.model_key = model_info["modelKey"]
        self.model_family_id = model_info["_idModelFamily"]
        self.params_millions = model_info["paramsMillions"]
        self.export_formats = export_formats
        self.model_config = {
                    param["keyName"]: [param["defaultValue"]]
                    for param in model_train_config["actionConfig"]
                }
        
    
    
    def refresh(self):
        """
        Refresh the instance by reinstantiating it with the previous values.
        """
        # Check if two minutes have passed since the last refresh
        if datetime.now() - self.last_refresh_time < timedelta(minutes=2):
            raise Exception("Refresh can only be called after two minutes since the last refresh.")

        # Capture the necessary state for reinitialization
        init_params = {
            'session': self.session,
            'model_family_name': self.model_family_name,
            'model_key': self.model_key
        }

        # Reinitialize the instance
        self.__init__(**init_params)

        # Update the last refresh time
        self.last_refresh_time = datetime.now()
    
        
    # Fetch model info
    def _get_model_info(self):
        """
        Fetch model information by its ID.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info to fetch.
        model_name : str
            The name of the model.
            
        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> session = Session(account="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_arch = ModelArch(session, model_family_name="resnet", model_key="resnet50")
        >>> resp, error, message = model_arch._get_model_info()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model info: {resp}")
        """
        
        if self.model_info_id is not None:
            path = f"/v1/model_store/model_info/{self.model_info_id}"
        else:
            path = f"/v1/model_store/model_info_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
        
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched the model info",
            "An error occured while fetching the model info",
        )    
        
    def get_export_formats(self):
        """
        Fetch export formats for a given model.

        If `model_info_id` is provided, it fetches the export formats using the ID.
        Otherwise, it fetches the export formats using the model key and family name.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> session = Session(account="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_arch = ModelArch(session, model_family_name="resnet", model_key="resnet50")
        >>> resp, error, message = model_arch.get_export_formats()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Export formats: {resp}")
        """
        if self.model_info_id is not None:
            path = f"/v1/model_store/get_export_formats?modelInfoId={self.model_info_id}"
        else:
            path = f"/v1/model_store/model_export_formats_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
       
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched all model family",
            "An error occured while fetching the model family",
        )
        
            
    def get_train_config(self, experiment_id , tuning_type="default", model_checkpoint="auto"):
        
        """
        Fetch the training configuration for a given model.

        This function retrieves the training configuration for a specified model and experiment.
        It constructs the payload with the provided parameters and sends a POST request to fetch
        the model parameters. The response is then processed to extract the action configuration
        and model configuration, which are used to construct the final training configuration.

        Parameters
        ----------
        experiment_id : str
            The ID of the experiment for which the training configuration is to be fetched.
        tuning_type : str, optional
            The type of parameter search to be used for tuning (default is "default").
        model_checkpoint : str, optional
            The model checkpoint to be used (default is "auto").

        Returns
        -------
        tuple
            A tuple containing the ModelArch instance and the training configuration dictionary.

        Example
        -------
        >>> session = Session(account="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_arch = ModelArch(session, model_family_name="resnet", model_key="resnet50")
        >>> experiment_id = "your_experiment_id"
        >>> model_arch_instance, train_config = model_arch.get_train_config(experiment_id)
        >>> print("ModelArch Instance:", model_arch_instance)
        >>> print("Training Configuration:", train_config)
        """
        
        payload = {
            "modelCheckpoint": [model_checkpoint],
            "paramsSearchType": tuning_type,
            "_idExperiment": experiment_id,
            "_idModelInfo": self.model_info_id,
        }
        
        path = f"/v1/model_store/get_model_params/v2?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(
            path=path, headers=headers, payload=payload
        )
        
        # Extract the action_config and model_config from the response
        action_config = {item["keyName"]: item for item in resp["data"]}
        model_config = {item["keyName"]: item["selectedValues"] for item in resp["data"]}
        
        # Construct the new model configuration structure
        config = {
            'is_autoML': False,  
            'tuning_type': tuning_type,
            'model_checkpoint': model_checkpoint,
            'checkpoint_type': 'predefined',  
            'action_config': action_config,
            'model_config': model_config
        }
        
        
        return ModelArch(session=self.session , model_family_name=self.model_family_name,model_key=self.model_key) , config
       
    
      
    def _get_default_train_config(self):
        """
        Generates the default payload for training a model based on its configuration.

        This method retrieves model information and training configuration using the model's `model_info_id`.
        It constructs a payload that can be used for initiating model training with default parameters.

        Parameters
        ----------
        model_info_id : str
            The unique identifier of the model for which the training payload is to be generated.

        Returns
        -------
        list
            A list containing a dictionary with default training payload settings.

        Example
        -------
        >>> model_info_id = "model123"
        >>> default_payload = model_arch.get_default_model_training_payload()
        >>> print(default_payload)
        [
            {
                'model_key': 'resnet50',
                'is_autoML': False,
                'tuning_type': 'manual',
                'model_checkpoint': 'auto',
                'checkpoint_type': 'predefined',
                'params_millions': 25.6,
                'model_name': 'ResNet-50',
                'id_model_info': 'model123',
                'action_config': {},
                'model_config': {
                    'learning_rate': [0.001],
                    'batch_size': [32],
                    ...
                }
            }
        ]
        
        Detailed Description
        --------------------
        - The function first fetches model information (`model_info`) and training configuration (`model_train_config`)
          using helper functions `get_model_info` and `get_model_train_config`.
        - It then constructs a payload that contains details such as the model's key, name, tuning type, 
          and configuration parameters (e.g., learning rate, batch size) for training.
        - The parameters for model training are set to their default values, which are fetched from the 
          model's configuration.
        """
        
        model_info = self._get_model_info(model_info_id=self.model_info_id)
        model_train_config = self.get_model_train_config(model_info_id=self.model_info_id)

        model_training_payload = [
            {
                "model_key": model_info["modelKey"],
                "is_autoML": False,
                "tuning_type": "manual",
                "model_checkpoint": "auto",
                "checkpoint_type": "predefined",
                "params_millions": model_info["paramsMillions"],
                "model_name": model_info["modelName"],
                "id_model_info": self.model_info_id,
                "action_config": {},
                "model_config": {
                    param["keyName"]: [param["defaultValue"]]
                    for param in model_train_config["actionConfig"]
                },
            }
        ]

        return model_training_payload
    
    def get_default_export_config(self, export_format):
        """
        Retrieves the default configuration for exporting a model in a specified format.

        This method fetches the export configuration for the given `model_info_id` and export format, 
        returning a dictionary of default export settings.

        Parameters
        ----------
        model_info_id : str
            The unique identifier of the model whose export configuration is to be retrieved.
        export_format : str
            The format in which the model is to be exported (e.g., 'ONNX', 'TF SavedModel').

        Returns
        -------
        dict
            A dictionary containing default export configuration settings, where keys are parameter names and values are default values.

        Example
        -------
        >>> export_format = "ONNX"
        >>> default_export_config = model_arch.get_default_model_export_config(export_format)
        >>> print(default_export_config)
        {
            optimize: True,
            int8: False,
            ...
        }

        """
        model_export_config , err , msg= self.get_export_action_configs(
            export_format
        )
        
        default_model_export_config = {
            param["keyName"]: param["defaultValue"]
            for param in model_export_config["actionConfig"]
        }
        return default_model_export_config

    # To fetch model action config
    def get_model_action_configs(self):
        """
        Fetch model action configuration by its ID.

        Parameters
        ----------
        model_action_config_id : str
            The ID of the model action config to fetch.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_arch.get_model_action_config()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model action config: {resp}")
        """
        if self.model_info_id is not None:
            path = f"/v1/model_store/model_action_config/{self.model_info_id}"
        else:
            path = f"/v1/model_store/model_action_config_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
            
        #path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched the model action config",
            "An error occured while fetching the model action config",
        )
        
        
    def get_export_action_configs(self,export_format):
        """
        Fetch action configuration for model export.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info.
        export_format : str
            The export format.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_arch.get_action_config_for_model_export("ONNX")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Action config for model export: {resp}")
        """
        path = f"/v1/model_store/get_action_config_for_model_export?modelInfoId={self.model_info_id}&exportFormat={export_format}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched all model family",
            "An error occured while fetching the model family",
        )
    
    def get_model_train_config(self):
        """
        Fetch model training configuration by its ID.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_arch.get_model_train_config()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model train config: {resp}")
        """
        if self.model_info_id is not None:
            path = f"/v1/model_store/get_train_config/{self.model_info_id}"
        else:
            path = f"/v1/model_store/model_train_config_from_model_key_and_family/{self.model_key}/{self.model_family_name}"
        
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched model train config",
            "An error occured while fetching model train config",
        )    
           
class ModelFamily: 

    """
    Class to interact with the model family API to get model configuration info and model-related info.

    This class handles fetching and storing model family information, including model inputs, outputs,
    supported runtimes, metrics, and other metadata.

    Parameters
    ----------
    session : Session
        The session object containing authentication information.
    model_family_id : str, optional
        The ID of the model family to fetch.
    model_family_name : str, optional
        The name of the model family to fetch.

    Attributes
    ----------
    session : Session
        The session object containing authentication information.
    account_number : str
        The account number from the session.
    project_id : str
        The project identifier from the session.
    rpc : RPCClient
        The RPC client object from the session for API calls.
    model_family_id : str
        The ID of the model family.
    model_family_name : str
        The name of the model family.
    family_data : dict
        The data of the model family fetched from the API.
    model_inputs : list
        List of model inputs.
    model_outputs : list
        List of model outputs.
    model_keys : dict
        Dictionary mapping model keys to model names.
    description : str
        Description of the model family.
    training_framework : str
        Training framework used for the model family.
    supported_runtimes : list
        List of supported runtimes.
    benchmark_datasets : list
        List of benchmark datasets.
    supported_metrics : list
        List of supported metrics.
    input_format : str
        Input format for the model family.

    Methods
    -------
    __get_model_family()
        Fetch a model family by its ID or name.
    get_model_archs(model_name=None, model_key=None)
        Fetch model information by model family or by name and key.

    Example
    -------
    >>> session = Session(account_number="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
    >>> model_family = ModelFamily(session, model_family_name="resnet")
    >>> print(f"Model Family: {model_family.model_family_name}")
    >>> print(f"Model Inputs: {model_family.model_inputs}")
    >>> print(f"Model Outputs: {model_family.model_outputs}")
    >>> print(f"Supported Runtimes: {model_family.supported_runtimes}")
    >>> print(f"Supported Metrics: {model_family.supported_metrics}")

    Raises
    ------
    AssertionError
        If neither model_family_id nor model_family_name is provided.
    """

    def __init__(self, session , model_family_id=None, model_family_name = None):
        self.session = session
        self.account_number = session.account_number
        self.project_id = session.project_id
        self.rpc = session.rpc
        assert model_family_id is not None or model_family_name is not None , "Either model_family_id or model_family_name must be provided"
        self.model_family_id = model_family_id
        self.model_family_name = model_family_name

        resp , error, message = self.__get_model_family()
        if error:
            print(f"Error: {error}")
            return
        
        
        
        family_data = resp
        self.family_data = family_data
        self.model_family_id = family_data["_id"]
        self.model_family_name = family_data["modelFamily"]
        self.model_inputs = family_data["modelInputs"]
        self.model_outputs = family_data["modelOutputs"]
        self.model_keys = {model["modelKey"]: model["modelName"] for model in family_data["models"]}
        self.description = family_data["description"]
        self.training_framework = family_data["trainingFramework"]
        self.supported_runtimes = family_data["supportedRuntimes"]
        self.benchmark_datasets = family_data["benchmarkDatasets"]
        self.supported_metrics = family_data["supportedMetrics"]
        self.input_format = family_data["dataProcessing"]["inputFormat"]
        
        
    # To fetch a model family
    def __get_model_family(self):
        """
        Fetch a model family by its ID or name.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> session = Session(account_number="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_family = ModelFamily(session, model_family_name="resnet")
        >>> resp, error, message = model_family.__get_model_family()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model family: {resp}")
        """
        if self.model_family_id is not None:
            path = f"/v1/model_store/model_family/{self.model_family_id}"
        else:
            path = f"/v1/model_store/model_family/{self.model_family_name}"
            
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched the model family",
            "An error occured while fetching the model family",
        )

    def get_model_archs(self, model_name=None, model_key=None):
        """
        Fetch a model family by its ID or name.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> session = Session(account_number="your_account_number", access_key="your_access_key", secret_key="your_secret_key")
        >>> model_family = ModelFamily(session, model_family_name="resnet")
        >>> resp, error, message = model_family.__get_model_family()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model family: {resp}")
        """
        if model_name and model_key:
            path = f"/v1/model_store/get_model_info_by_name_and_key?modelName={model_name}&modelKey={model_key}"
        elif self.model_family_id:
            path = f"/v1/model_store/get_models_by_modelfamily?modelFamilyId={self.model_family_id}"
        else:
            path = f"/v1/model_store/get_models_by_modelfamily?modelFamilyName={self.model_family_name}"

        resp = self.rpc.get(path=path)

        data, error, message = handle_response(
            resp,
            "Successfully fetched model info",
            "An error occurred while fetching model info",
        )

        if error:
            return data, error, message
        
        if isinstance(data, list):  # Handle when data is a list of dictionaries
            data_list = data
        elif isinstance(data, dict):  # Handle when data is a single dictionary
            data_list = [data]  # Convert it to a list with one dictionary
        else:
            error = "Data is not in the expected format. Expected a list or dictionary."
            return None, error, message

        # Now proceed with processing as a list
        if model_name and model_key:
            model_info_list = [{"model_key": item["modelKey"], "model_arch_instance": ModelArch(self.session, self.model_family_name, item["modelKey"])} for item in data_list]
            return model_info_list, error, message
        else:
            model_archs = {item["modelKey"]: ModelArch(self.session, self.model_family_name, item["modelKey"]) for item in data_list}
            return model_archs, error, message


    


class BYOM:

    """
    A class to interact with the BYOM (Bring Your Own Model) API for managing model families, model information,
    and model action configurations.

    Attributes:
    -----------
    session : Session
        A session object containing account information and RPC (Remote Procedure Call) details.
    account_number : str
        The account number associated with the session.
    rpc : RPC
        The RPC object used to make API calls.

    Methods:
    --------

    delete_model_family(model_family_id)
        Deletes a model family using its ID.

    delete_model_info(model_info_id)
        Deletes model information using its ID.

    delete_model_action_config(model_action_config_id)
        Deletes a model action configuration using its ID.

    add_model_family(...)
        Adds a new model family.

    add_model_info(...)
        Adds new model information.

    add_model_action_config(...)
        Adds a new model action configuration.

    update_model_family(...)
        Updates a model family.

    update_model_info(...)
        Updates model information.

    update_model_action_config(...)
        Updates a model action configuration.

    add_model_family_action_config(...)
        Adds an action configuration to a model family.
    """

    def __init__(self, session , family_name=None , family_id=None , family_config=None):
        """
        Initializes the BYOM class with a session object.

        Parameters:
        -----------
        session : Session
            A session object containing account information and RPC details.
        """
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc
        self.project_id = session.project_id
        self.family_name = family_name
        self.family_id = family_id
        self.family_config = None

        assert family_name is not None or family_id is not None
        
        if family_config is not None:
            self.family_config = self.__load_config(family_config)

        # Check existence by family_id
        if self.family_id is not None:
            self.model_family = ModelFamily(self.session, family_id=self.family_id)

        # Check existence by family_name
        elif self.family_name is not None:
            if not check_family_exists_by_name(self.family_name):
                if self.family_config:
                    self._add_model_family(self.family_config)
                    print("added the new model family:", self.family_id)

            self.model_family = ModelFamily(self.session, family_name=self.family_name)

        else:
            raise ValueError("Either family_name, family_id, or family_config must be provided.")

    def __load_config(self, config):
        if isinstance(config, str) and os.path.isfile(config):
            with open(config, 'r') as file:
                return json.load(file)
        elif isinstance(config, dict):
            return config
        else:
            raise ValueError("Invalid family_config. Must be a dictionary or a valid file path.")
    

    # To delete a model family
    def delete_model_family(self):
        """
        Deletes a model family using its ID.

        Parameters:
        -----------
        model_family_id : str
            The ID of the model family to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        if self.family_id is not None:
            path = f"/v1/model_store/model_family/{self.family_id}"
        else:
            path = f"/v1/model_store/model_family/{self.family_name}"
        
        resp = self.rpc.delete(path=path)

        return handle_response(
            resp,
            "Successfully deleted the model family",
            "An error occured while deleting the model family",
        )

    # To delete model info
    def delete_model_info(self, model_info_id , model_key):
        """
        Deletes model information using its ID.

        Parameters:
        -----------
        model_info_id : str
            The ID of the model information to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        if model_info_id is not None:
            path = f"/v1/model_store/model_info/{model_info_id}"
        else:
            path = f"/v1/model_store/model_info/{model_key}"
        
        resp = self.rpc.delete(path=path)

        return handle_response(
            resp,
            "Successfully deleted the model family",
            "An error occured while deleting the model family",
        )

    # To delete model action config
    def delete_action_config(self, model_action_config_id, export_format=None):
        """
        Deletes a model action configuration using its ID.

        Parameters:
        -----------
        model_action_config_id : str
            The ID of the model action configuration to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        resp = self.rpc.delete(path=path)

        return handle_response(
            resp,
            "Successfully deleted the model action config",
            "An error occured while deleting the model action config",
        )


    def _add_model_family(self, config):
        """
        Adds a new model family to the model store.

        This function sends a POST request to add a new model family with the provided parameters.

        Parameters:
        -----------
        config : str or dict
            The path to the local JSON file containing the model config or the model config dictionary.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        ValueError
            If the config is neither a valid file path nor a dictionary.
        """

        # Load the config from a file if a file path is provided
        if isinstance(config, str) and os.path.isfile(config):
            with open(config, 'r') as file:
                config = json.load(file)
        elif not isinstance(config, dict):
            raise ValueError("Invalid config. Must be a dictionary or a valid file path.")
        
        project_id = self.project_id    

        # Extract necessary parameters from the config
        model_family = config.get("model_family")
        model_inputs = config.get("model_inputs")
        model_outputs = config.get("model_outputs")
        models = config.get("models")
        description = config.get("description")
        training_framework = config.get("training_framework")
        supported_runtimes = config.get("supported_runtimes")
        benchmark_datasets = config.get("benchmark_datasets")
        supported_metrics = config.get("supported_metrics")
        input_format = config.get("input_format")
        data_loader_class_definition = config.get("data_loader_class_definition")
        data_loader_call_signature = config.get("data_loader_call_signature")
        references = config.get("references")
        is_private = config.get("is_private")

        # Create the payload
        model_store_payload = {
            "modelFamily": model_family,
            "modelInputs": model_inputs,
            "modelOutputs": model_outputs,
            "models": models,
            "description": description,
            "trainingFramework": training_framework,
            "supportedRuntimes": supported_runtimes,
            "benchmarkDatasets": benchmark_datasets,
            "supportedMetrics": supported_metrics,
            "dataProcessing": {
            "inputFormat": input_format,
            "dataLoaderClassDefinition": data_loader_class_definition,
            "dataLoaderCallSignature": data_loader_call_signature,
            },
            "references": references,
            "isPrivate": is_private,
            "projectId": project_id,
        }

        # Send the POST request
        path = "/v1/model_store/add_model_family"
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(path=path, headers=headers, payload=model_store_payload)

        return handle_response(
            resp,
            "New model family created",
            "An error occurred while creating model family",
        )

    def add_or_update_model_info(self, config):
        """
        Adds or updates information for a specific model in the model store.

        This function sends a POST request to add or a PUT request to update information about a model with the provided parameters.

        Parameters:
        -----------
        config : str or dict
            The path to the local JSON file containing the model config or the model config dictionary.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        ValueError
            If the config is neither a valid file path nor a dictionary.
        """

        # Load the config and id
        config = self.load_config(config)
        model_family_id = self.model_family["id"]
        
        # Extract necessary parameters from the config
        model_key = config.get("modelKey")
        model_name = config.get("modelName")
        params_millions = config.get("paramsMillions")
        recommended_runtime = config.get("recommendedRuntimes")
        benchmark_results = config.get("benchmarkResults")
        runtime_results = config.get("runtimeResults")

        # Create the payload
        model_store_payload = {
            "modelKey": model_key,
            "modelName": model_name,
            "_idModelFamily": model_family_id,
            "paramsMillions": params_millions,
            "recommendedRuntimes": recommended_runtime,
            "benchmarkResults": benchmark_results,
            "runtimeResults": runtime_results,
        }

        # Determine if the model exists
        if self.model_family.model_infos['model_key']:
            # Update model info
            model_info_id = next(model['_id'] for model in _get_all_models() if model['modelKey'] == model_key)
            path = f"/v1/model_store/model_info/{model_info_id}"
            success_message = "Model info updated successfully"
            error_message = "An error occurred while updating model info"
            resp = self.session.put(path=path, headers={"Content-Type": "application/json"}, payload=model_store_payload)
        else:
            # Add model info
            path = "/v1/model_store/add_model_info"
            success_message = "New model info created successfully"
            error_message = "An error occurred while creating model info"
            resp = self.session.post(path=path, headers={"Content-Type": "application/json"}, payload=model_store_payload)

        return handle_response(resp, success_message, error_message)

    # To add a new entry into model action config
    def add_action_config(
        self,
        action_type,
        action_config,
        model_checkpoint,
        export_format,
        ):
            """
            Adds a new action configuration for a specific model in the model store.

            This function sends a POST request to add a new action configuration for a model with the provided parameters.

            Parameters:
            -----------
            action_type : str
                The type of action (e.g., 'train_model', 'export_model').
            action_config : dict
                Configuration details for the action.
            model_checkpoint : str
                Path or identifier for the model checkpoint.
            export_format : str
                Format for exporting the model.

            Returns:
            --------
            tuple
                A tuple containing three elements:
                - API response (dict): The raw response from the API.
                - error_message (str or None): Error message if an error occurred, None otherwise.
                - status_message (str): A status message indicating success or failure.

            Raises:
            -------
            May raise exceptions related to network issues or API errors.

            Notes:
            ------
            This function uses the self.rpc.post method to send the request and
            handle_response to process the response.
            """
            path = "/v1/model_store/add_model_action_config"
            model_store_payload = {
                "_idModelFamily": self.family_id,
                "actionType": action_type,
                "actionConfig": action_config,
                "modelCheckpoint": model_checkpoint,
                "exportFormat": export_format,
            }
            headers = {"Content-Type": "application/json"}
            resp = self.rpc.post(path=path, headers=headers, payload=model_store_payload)

            return handle_response(
                resp,
                "New model action config created",
                "An error occured while creating model action config",
            )


    def update_model_family(self, config):
        """
        Updates an existing model family in the model store.

        This function sends a PUT request to update a model family with the provided parameters.

        Parameters:
        -----------
        model_family_id : str
            The unique identifier of the model family to update.
        config : str or dict
            The path to the local JSON file containing the model config or the model config dictionary.

        Returns:
        --------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises:
        -------
        ValueError
            If the config is neither a valid file path nor a dictionary.
        """

        # Load the config
        config = self.__load_config(config)
        model_family_id = self.model_family["id"]
        project_id = self.project_id

        # Extract necessary parameters from the config
        model_family = self.model_family
        model_inputs = config.get("model_inputs")
        model_outputs = config.get("model_outputs")
        model_keys = config.get("model_keys")
        description = config.get("description")
        training_framework = config.get("training_framework")
        supported_runtimes = config.get("supported_runtimes")
        benchmark_datasets = config.get("benchmark_datasets")
        supported_metrics = config.get("supported_metrics")
        pruning_support = config.get("pruning_support")
        code_repository = config.get("code_repository")
        training_docker_container = config.get("training_docker_container")
        input_format = config.get("input_format")
        data_loader_class_definition = config.get("data_loader_class_definition")
        data_loader_call_signature = config.get("data_loader_call_signature")
        references = config.get("references")
        is_private = config.get("is_private")

        # Create the payload
        model_store_payload = {
            "modelFamily": model_family,
            "modelInputs": model_inputs,
            "modelOutputs": model_outputs,
            "modelKeys": model_keys,
            "description": description,
            "trainingFramework": training_framework,
            "supportedRuntimes": supported_runtimes,
            "benchmarkDatasets": benchmark_datasets,
            "supportedMetrics": supported_metrics,
            "pruningSupport": pruning_support,
            "codeRepository": code_repository,
            "trainingDockerContainer": training_docker_container,
            "dataProcessing": {
                "inputFormat": input_format,
                "dataLoaderClassDefinition": data_loader_class_definition,
                "dataLoaderCallSignature": data_loader_call_signature,
            },
            "references": references,
            "isPrivate": is_private,
            "projectId": project_id,
        }

        # Send the PUT request
        path = f"/v1/model_store/model_family/{model_family_id}"
        headers = {"Content-Type": "application/json"}
        resp = self.session.put(path=path, headers=headers, payload=model_store_payload)

        return handle_response(
            resp,
            "Model family successfully updated",
            "An error occurred while updating model family",
        )

    

    # To update model action config
    def update_action_config(
        self,
        model_action_config_id,
        model_info_id,
        action_type,
        action_config,
        export_format,
        model_checkpoint,
    ):
        """
        Updates the action configuration for a specific model in the model store.

        This function sends a PUT request to update model action configuration with the provided parameters.

        Parameters
        ----------
        model_action_config_id : str
            The unique identifier of the model action config to update.
        model_info_id : str
            The identifier of the model info this action config belongs to.
        action_type : str
            The updated type of action (e.g., 'train_model', 'export_model').
        action_config : dict
            Updated configuration details for the action.
        export_format : str
            Updated format for exporting the model.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises
        ------
        May raise exceptions related to network issues or API errors.

        Notes
        -----
        This function uses the self.rpc.put method to send the request and
        handle_response to process the response.

        Example
        -------
        >>> resp, error, message = model_store.update_action_config(
        >>>     model_action_config_id="12345",
        >>>     model_info_id="67890",
        >>>     action_type="train_model",
        >>>     action_config={"param1": "value1", "param2": "value2"},
        >>>     export_format="ONNX"
        >>> )
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Action config updated: {resp}")
        """
        path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        model_store_payload = {
            "_idModelInfo": model_info_id,
            "actionType": action_type,
            "model_checkpoint": model_checkpoint,
            "actionConfig": action_config,
            "export_format": export_format,
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.put(path=path, headers=headers, payload=model_store_payload)

        return handle_response(
            resp,
            "Model action config successfully updated",
            "An error occurred while updating the model action config",
        )

    def validate_model_info(self):
        """
        Validate the model information for a given project.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.validate_model_info()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Validation result: {resp}")
        """
        path = f"/v1/model_store/validate_model_info/{self.project_id}/{self.family_id}"
        resp = self.rpc.post(path=path)

        return handle_response(
            resp,
            "Successfully validated model info",
            "An error occurred while validating the model information",
        )

    def validate_train_config(self):
        """
        Validate the training configuration for a given project.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.validate_train_config()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Validation result: {resp}")
        """
        path = f"/v1/model_store/validate_train_config/{self.project_id}/{self.family_id}"
        resp = self.rpc.post(path=path)

        return handle_response(
            resp,
            "Successfully validated training configuration",
            "An error occurred while validating the training configuration",
        )

    def validate_export_config(self):
        """
        Validate the export configuration for a given project.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.validate_export_config()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Validation result: {resp}")
        """
        path = f"/v1/model_store/validate_export_config/{self.project_id}/{self.family_id}"
        resp = self.rpc.post(path=path)

        return handle_response(
            resp,
            "Successfully validated export configuration",
            "An error occurred while validating the export configuration",
        )

    def validate_local_test_logs(self, file_path):
        """
        Validate the local test logs for a given project.

        Parameters
        ----------
        file_path : str
            The path to the test log file.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.validate_test_logs("path/to/log/file")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Validation result: {resp}")
        """
        path = f"/v1/model_store/validate_test_logs/{self.project_id}/{self.family_id}"
        files = {'jsonfile': open(file_path, 'rb')}
        resp = self.rpc.post(path=path, files=files)

        return handle_response(
            resp,
            "Successfully validated test logs",
            "An error occurred while validating the test logs",
        )

    def validate_all(self):
        """
        Validate all configurations and logs for the model family.

        Returns
        -------
        dict
            A dictionary containing the results of all validations.

        Example
        -------
        >>> results = model_store.validate_all()
        >>> for key, (resp, error, message) in results.items():
        >>>     if error:
        >>>         print(f"{key} validation failed: {error}")
        >>>     else:
        >>>         print(f"{key} validation succeeded: {message}")
        """
        results = {}

        results['model_info'] = self.validate_model_info()

        results['train_config'] = self.validate_train_config()

        results['export_config'] = self.validate_export_config()

        # Validate local test logs
        # Assuming you have a predefined path for test logs
        test_log_path = "path/to/test/log/file"
        results['test_logs'] = self.validate_local_test_logs(test_log_path)

        return results

    def _get_code_upload_path(self):
        """
        Get the user upload path for a given project.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_user_upload_path()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"User upload path: {resp}")
        """
        
        path = f"/v1/model_store/get_user_upload_path/{self.project_id}/{self.family_id}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully retrieved user upload path",
            "An error occurred while retrieving the user upload path",
        )

    
    def get_validation_logs(self):
        """
        Get the validation logs for a given model family.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_validation_logs()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Validation logs: {resp}")
        """
        path = f"/v1/model_store/get_validation_logs/validation/all?{self.model_family}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully retrieved validation logs",
            "An error occurred while retrieving the validation logs",
        )

    def add_codebase(self, code_path, project_type, matrice_version, training_framework, framework_version, license_content):
        """
        Add model family code for a given project.

        Parameters
        ----------
        cloud_path : str
            The cloud path where the model family code is stored.
        project_type : str
            The type of the project (e.g., "classification", "detection", "instance_segmentation").
        python_sdk_version : str
            The version of the Python SDK.
        pytorch_version : str
            The version of PyTorch.
        license_info : str
            The license information for the model family code.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.add_model_family_code(
        >>>     "cloud/path/to/code", "classification", "1.0.0", "1.7.1", "MIT"
        >>> )
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model family code added: {resp}")
        """
        path = f"/v1/model_store/get_validation_logs/validation/all?{self.model_family}"
        model_store_payload = {
            "cloudPath": cloud_path,
            "accountNumber": self.account_number,
            "_idModelFamily": self.model_family,
            "projectType": project_type,
            "sdk_version": python_sdk_version,
            "pytorch_version": pytorch_version,
            "license": license_info,
        }
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(path=path, json=model_store_payload, headers=headers)

        return handle_response(
            resp,
            "Successfully added model family code",
            "An error occurred while adding the model family code",
        )
    
    def get_codebase_details(self):
        """
        Fetch user code base details for the specified model family.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_user_code_base_details()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"User code details: {resp}")
        """
        path = f"/v1/model_store/get_user_code_details/{self.model_family}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched user code details",
            "An error occurred while fetching user code details"
        )
    
    
    def download_codebase(self, local_path):
        """
        Fetch the download path for the user code base of a model family.


        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_user_code_base_download_path()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model code path: {resp}")
        """
        path = f"/v1/model_store/get_user_code_download_path/{self.model_family}"
        resp = self.rpc.get(path=path)

        return handle_response(
            resp,
            "Successfully fetched model family code path",
            "An error occurred while fetching model family code path"
        )
    
    
    def get_test_case_logs(self):
        pass

    def get_byom_status(self):
        self.model_family.refresh()
        return self.model_family.status
    