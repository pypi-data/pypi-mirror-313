"""Module containing all the client functionality for the Deepchecks LLM Client."""
import io
import logging
import os
import time
import typing as t
from datetime import datetime

import pandas as pd
from deepchecks_llm_client.api import API
from deepchecks_llm_client.data_types import (
    AnnotationType,
    ApplicationType,
    ApplicationVersionSchema,
    CustomPropertyType,
    EnvType,
    Interaction,
    InteractionCompleteEvents,
    LogInteractionType,
    PropertyColumnType,
    Step,
    StepType,
)
from deepchecks_llm_client.exceptions import DeepchecksLLMClientError
from deepchecks_llm_client.utils import HandleExceptions, HandleGeneratorExceptions, check_topic, get_timestamp, safe_list_eval

logging.basicConfig()
logger = logging.getLogger(__name__)
init_logger = logging.Logger(__name__ + ".init")

DEFAULT_ENV_TYPE = EnvType.PROD
DEFAULT_DC_HOST = "https://app.llm.deepchecks.com"

class DeepchecksLLMClient:
    """DeepchecksLLMClient is the class through which you can interact with the Deepchecks LLM API."""

    def __init__(self,
                 host: str = None,
                 api_token: str = None,
                 log_level: int = logging.WARNING,
                 silent_mode: bool = False):
        """Init Deepchecks LLM Client. Connect to the server and perform a simple handshake with the API.

        Parameters
        ==========
        host : str
            The URL of the Deepchecks server to communicate with. By default,
            it's set to the Deepchecks LLM host (https://app.llm.deepchecks.com),
            but you can override it by providing a custom URL.
            If not provided, the value is read from the environment variable DEEPCHECKS_LLM_HOST.
        api_token : str
            Deepchecks API Token (can be generated from the UI).
            If not provided, the value is read from the environment variable DEEPCHECKS_LLM_API_TOKEN.
        silent_mode: bool, default=False
            If True, the SDK will print logs upon encountering errors rather than raising them
        log_level: int, default=logging.WARNING
            Set SDK loggers logging level

        Returns
        =======
        None
        """
        self._api: API = None
        self._host = host or os.environ.get("DEEPCHECKS_LLM_HOST", None) \
                     or os.environ.get("AWS_PARTNER_APP_URL", DEFAULT_DC_HOST) # AWS Hadron env var
        self._api_token = api_token or os.environ.get("DEEPCHECKS_LLM_API_TOKEN")

        logger.setLevel(log_level)
        self._log_level = log_level
        self.silent_mode = silent_mode

        self._init_api()

    @HandleExceptions(init_logger)
    def _init_api(self):
        if self._api is None:
            if self._host is not None and self._api_token is not None:
                self._api = API.instantiate(host=self._host, token=self._api_token)
            else:
                raise DeepchecksLLMClientError("host/token parameters must be provided")

    @property
    def api(self) -> API:
        """Get the API object for the client."""
        if self._api:
            return self._api
        raise DeepchecksLLMClientError("deepchecks llm client was not initialized correctly, please re-create it")

    @HandleExceptions(logger)
    def create_application(
            self,
            app_name: str,
            app_type: ApplicationType,
            versions: t.Optional[t.List[ApplicationVersionSchema]] = None,
            description: t.Optional[str] = None,
    ):
        """Create a new application.

        Parameters
        ----------
        app_name
            Application name
        app_type
            The type of application to create
        versions
            List of versions to create for the application
        description
            Description of the application

        Returns
        -------
            The response from the API
        """
        self.api.create_application(app_name=app_name, app_type=app_type, versions=versions, description=description)
        return self.api.get_application(app_name=app_name)

    @HandleExceptions(logger)
    def create_app_version(
            self,
            app_name: str,
            version_name: str,
            description: t.Optional[str] = None,
            additional_fields: t.Optional[t.Dict[str, t.Any]] = None,
    ):
        """Create a new application.

        Parameters
        ----------
        app_name
            Application name
        version_name
            Version name
        description
            Description of the version
        additional_fields
            Additional fields to add to the version
        Returns
        -------
            The response from the API
        """
        app_id = self._get_application_id(app_name)
        return self.api.create_application_version(
            application_id=app_id,
            version_name=version_name,
            description=description,
            custom=[{key: value} for key, value in additional_fields.items()] if additional_fields else []
        )

    @HandleExceptions(logger)
    def get_applications(self):
        """Get all applications as Application objects.

        Returns
        -------
        List[Application]
            List of applications
        """
        return self.api.get_applications()

    @HandleExceptions(logger)
    def get_versions(self, app_name: t.Optional[str] = None):
        """Get all versions of an application as Version objects.

        Parameters
        ----------
        app_name
            Name of the application to get versions for

        Returns
        -------
        List[ApplicationVersion]
            List of versions
        """
        return self.api.get_versions(app_name=app_name)

    @HandleExceptions(logger)
    def annotate(self, app_name: str, version_name: str, user_interaction_id: str,
                 annotation: AnnotationType = None, reason: t.Optional[str] = None):
        """Annotate a specific interaction by its user_interaction_id.

        Parameters
        ----------
        app_name
            Application name
        version_name
            Name of the version to which this interaction belongs
        user_interaction_id
            The user_interaction_id of the interaction to annotate
        annotation
            Could be one of AnnotationType.GOOD, AnnotationType.BAD, AnnotationType.UNKNOWN
            or None to remove annotation
        reason
            String that explains the reason for the annotation

        Returns
        -------
            None
        """
        version_id = self._get_version_id(version_name=version_name, app_name=app_name)
        self.api.annotate(user_interaction_id, version_id, annotation, reason=reason)

    # pylint: disable=redefined-builtin
    @HandleExceptions(logger)
    def log_interaction(
            self,
            app_name: str,
            version_name: str,
            env_type: t.Union[EnvType, str],
            input: t.Union[str, None] = None,
            output: t.Union[str, None] = None,
            full_prompt: str = None,
            information_retrieval: t.Union[t.List[str], str] = None,
            history: t.Union[t.List[str], str] = None,
            annotation: t.Union[AnnotationType, str] = None,
            annotation_reason: str = None,
            user_interaction_id: str = None,
            started_at: t.Union[datetime, float, None] = None,
            finished_at: t.Union[datetime, float, None] = None,
            steps: t.List[Step] = None,
            custom_props: t.Dict[str, t.Any] = None,
            vuln_type: t.Optional[str] = None,
            vuln_trigger_str: t.Optional[str] = None,
            topic: t.Optional[str] = None,
            is_completed: bool = True,
    ) -> str:
        """Log a single interaction.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of the version to which this interaction will be added
        env_type : EnvType or str
            Type of environment. Allowed values: 'eval', 'prod', 'pentest'
        input : str or None
            Input data
        output : str or None
            Output data
        full_prompt : str or None
            Full prompt data
        information_retrieval : str or list of str
            Information retrieval.
        history : str
            History
        annotation : AnnotationType or str
            Annotation type of the interaction. Allowed values: 'good', 'bad', 'unknown'
        user_interaction_id : str
            Unique identifier of the interaction
        started_at : datetime or float
            Timestamp the interaction started at. Datetime format is deprecated, use timestamp instead
        finished_at : datetime or float
            Timestamp the interaction finished at. Datetime format is deprecated, use timestamp instead
        steps : list of Step
            List of steps taken during the interaction
        custom_props : dict
            Additional custom properties
        annotation_reason : str, optional
            Reason for the annotation
        vuln_type : str, optional
            Type of vulnerability (Only used in case of EnvType.PENTEST and must be sent there).
        vuln_trigger_str : str, optional
            Vulnerability trigger string (Only used in case of EnvType.PENTEST and is optional there).
        topic: t.Optional[str], optional
            The custom topic of the interaction
        is_completed: bool
            Completed interactions will be shown in the system,
            and cannot be further modified except for annotations,
            topics and custom properties.

        Returns
        -------
        str
            The uuid of the interaction

        """
        if isinstance(started_at, datetime) or isinstance(finished_at, datetime):
            logger.warning(
                "Deprecation Warning: Usage of datetime for started_at/finished_at is deprecated, use timestamp instead."
            )
            if isinstance(started_at, datetime):
                started_at = started_at.timestamp()

            if isinstance(finished_at, datetime):
                finished_at = finished_at.timestamp()

        check_topic(topic)
        self._validate_steps(steps)

        # pylint: disable=redefined-builtin
        result = self.api.log_interaction(
            app_name=app_name,
            version_name=version_name,
            env_type=env_type,
            input=input,
            output=output,
            full_prompt=full_prompt,
            information_retrieval=safe_list_eval(information_retrieval) if information_retrieval is not None else None,
            history=safe_list_eval(history) if history is not None else None,
            annotation=annotation,
            annotation_reason=annotation_reason,
            user_interaction_id=user_interaction_id,
            started_at=started_at,
            finished_at=finished_at,
            steps=steps,
            custom_props=custom_props,
            vuln_type=vuln_type,
            vuln_trigger_str=vuln_trigger_str,
            topic=topic,
            is_completed=is_completed,
        )
        return result.json()[0]

    @HandleExceptions(logger)
    def log_batch_interactions(
            self,
            app_name: str,
            version_name: str,
            env_type: t.Union[EnvType, str],
            interactions: t.List[LogInteractionType],
    ) -> t.List[str]:
        """Log multiple interactions at once.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of the version to which this interaction will be added
        env_type : EnvType or str
            Type of environment. Could be one of EnvType or 'prod', 'eval', 'pentest'
        interactions : list of LogInteractionType
            The list of interaction data to log.

        Returns
        -------
        list of str
            List of the uuids of the interactions

        """
        for interaction in interactions:
            check_topic(interaction.topic)
            interaction.information_retrieval = (
                safe_list_eval(interaction.information_retrieval) if interaction.information_retrieval else None
            )
            self._validate_steps(interaction.steps)

        result = self.api.log_batch(
            app_name=app_name,
            version_name=version_name,
            env_type=env_type,
            interactions=interactions,
        )
        return result.json()

    @HandleExceptions(logger)
    def update_interaction(
        self,
        app_name: str,
        version_name: str,
        user_interaction_id: str,
        annotation: t.Optional[t.Union[AnnotationType, str]] = None,
        annotation_reason: t.Optional[str] = None,
        custom_props: t.Union[t.Dict[str, t.Any], None] = None,
        steps: t.Union[t.List[Step]] = None,
        information_retrieval: t.Union[t.List[str], str] = None,
        input: t.Union[str, None] = None,
        output: t.Union[str, None] = None,
        is_completed: t.Union[bool, None] = None,
        finished_at: t.Union[datetime, float] = None,
    ):
        """Update a specific interaction by its user_interaction_id.

        Parameters
        ----------
        app_name : str
            Application name
        version_name
            Name of the version to which this interaction belongs
        user_interaction_id
            Unique id of the interaction to update
        annotation : AnnotationType or str
            Could be one of AnnotationType or 'good', 'bad', 'unknown'
        annotation_reason: str
            String that explains the reason for the annotation
        custom_props: dict
            Dictionary of custom properties for interaction
        steps: list of Step
            List of steps taken during the interaction.
            New steps will be added to existing ones for previously incomplete interactions.
            Cannot be changed for completed interactions
        information_retrieval : str or list of str
            Information retrieval. New data will be added to existing ones for previously incomplete interactions.
            Cannot be changed for completed interactions
        input: str or None
            Input data. Old value will be overridden by the new value.
            Note that once interactions are marked as completed, this value cannot be changed.
        output: str or None
            Output data. Old value will be overridden by the new value.
            It cannot be modified for completed interactions.
        is_completed: bool or None.
            Completed interactions will be shown in the system,
            and cannot be further modified except for annotations,
            topics and custom properties.
            Interaction completeness status will be not changed if None is sent
        finished_at : datetime or float
            Timestamp the interaction finished at. Datetime format is deprecated, use timestamp instead
        Returns
        -------
            None
        """
        # pylint: disable=redefined-builtin
        version_id = self._get_version_id(app_name=app_name, version_name=version_name)
        if isinstance(finished_at, datetime):
            finished_at = finished_at.timestamp()

        self.api.update_interaction(
            user_interaction_id=user_interaction_id,
            app_version_id=version_id,
            annotation=annotation,
            annotation_reason=annotation_reason,
            custom_props=custom_props,
            steps=steps,
            information_retrieval=safe_list_eval(information_retrieval) if information_retrieval is not None else None,
            input=input,
            output=output,
            is_completed=is_completed,
            finished_at=finished_at,
        )

    @HandleExceptions(logger)
    def delete_interactions(self, app_name: str, version_name: str, user_interaction_ids: t.List[str]):
        """Delete specific interactions by their user_interaction_ids.

        Parameters
        ----------
        app_name : str
            Application name
        version_name: str
            Name of application version
        user_interaction_ids: List[str]
            List of interaction user ids to delete

        Returns
        -------
            None
        """
        version_id = self._get_version_id(app_name=app_name, version_name=version_name)
        self.api.delete_interactions(
            user_interaction_ids=user_interaction_ids, app_version_id=version_id,
        )

    @HandleExceptions(logger)
    def update_application_config(self, app_name: str, file):
        """Update the auto-annotation YAML configuration file for the current application.

        Parameters
        ----------
        app_name : str
            Application name
        file : str
            The path to the configuration file to update

        Returns
        -------
            None
        """
        app_id = self._get_application_id(app_name)
        self.api.update_application_config(application_id=app_id, file=file)

    @HandleExceptions(logger)
    def get_application_config(self, app_name: str, file_save_path: t.Union[str, None] = None) -> str:
        """Write the auto-annotation YAML configuration file to the specified path.

        Parameters
        ----------
        app_name : str
            Application name
        file_save_path : str | None, optional
            The path to save the configuration file to. If None, the file will not be saved.

        Returns
        -------
        str
            The auto-annotation YAML configuration file as a string.
        """
        app_id = self._get_application_id(app_name)
        return self.api.get_application_config(application_id=app_id, file_save_path=file_save_path)

    @HandleGeneratorExceptions(init_logger)
    def data_iterator(self,
                      app_name: str,
                      version_name: str,
                      env_type: t.Union[EnvType, str],
                      start_time: t.Union[datetime, int, None] = None,
                      end_time: t.Union[datetime, int, None] = None,
                      user_interaction_ids: t.Union[t.List[str], None] = None,
                      include_incomplete: bool = False,
                      ) -> t.Iterable[Interaction]:
        """
        Fetch all interactions from the specified environment type (PROD/EVAL) as an iterable.

        Supports pagination, so this API is suitable for iterating over large amounts of data.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of application version
        env_type : EnvType | str
            The environment type from which to fetch interactions. This can be either "PROD" or "EVAL".
        start_time : datetime | int | None, optional
            The start time from which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched from the beginning.
        end_time : datetime | int | None, optional
            The end time until which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched up to the most recent.
        user_interaction_ids: list | None, optional
            user interactions ids to include into the list of interactions.annotation_reason
        include_incomplete : bool
            Return only interactions with completed status or not.
            Only completed are returned by default.

        Returns
        -------
        Iterable[Interaction]
            An iterable collection of interactions.

        """
        version_id = self._get_version_id(app_name=app_name, version_name=version_name)

        offset = 0
        limit = 20

        while True:
            interactions = \
                self.api.get_interactions(version_id,
                                          env_type=env_type,
                                          start_time_epoch=get_timestamp(start_time),
                                          end_time_epoch=get_timestamp(end_time),
                                          user_interaction_ids=user_interaction_ids,
                                          limit=limit, offset=offset,
                                          include_incomplete=include_incomplete)
            for interaction in interactions:
                yield self._build_interaction_object(interaction)

            # If the size of the data is less than the limit, we"ve reached the end
            if len(interactions) < limit:
                break

            offset += limit

    @HandleExceptions(init_logger)
    def get_data(
            self,
            app_name: str,
            version_name: str,
            env_type: t.Union[EnvType, str],
            return_topics: bool = True, return_annotation_data: bool = True,
            return_input_props: bool = True, return_output_props: bool = True,
            return_custom_props: bool = True, return_llm_props: bool = True,
            start_time: t.Union[datetime, int, None] = None,
            end_time: t.Union[datetime, int, None] = None,
            return_similarities: bool = False,
            user_interaction_ids: t.Union[t.List[str], None] = None,
            include_incomplete: bool = False,
            return_steps: bool = True,
    ) -> t.Union[pd.DataFrame, None]:
        """
        Fetch all the interactions from the specified environment (PROD/EVAL) as a pandas DataFrame.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of application version
        env_type : EnvType | str
            The environment type from which to fetch interactions. This can be either "PROD" or "EVAL".
        return_annotation_data : bool, optional
            Whether to include annotation info in the data.
        return_topics : bool, optional
            Whether to include the topic in the data.
        return_input_props : bool, optional
            Whether to include input properties in the data.
        return_output_props : bool, optional
            Whether to include the output properties in the data.
        return_custom_props : bool, optional
            Whether to include custom properties in the data.
        return_llm_props : bool, optional
            Whether to include LLM properties in the data.
        return_similarities : bool, optional
            Whether to include similarities in the data.
        start_time : datetime | int | None, optional
            The start time from which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched from the beginning.
        end_time : datetime | int | None, optional
            The end time until which to fetch interactions. This can be a datetime object or an integer.
            If not provided, interactions will be fetched up to the most recent.
        user_interaction_ids: list | None, optional
            user interactions ids to include in the data.
        include_incomplete : bool
            Return only interactions with completed status or not.
            Only completed are returned by default.
        return_steps : bool, optional
            Whether to include steps in the data.
        Returns
        -------
        pd.DataFrame | None
            A pandas DataFrame containing the interactions, or None in case of a problem retrieving the data.
        """
        eval_set_version_id = self._get_version_id(app_name=app_name, version_name=version_name)
        csv_as_text = self.api.get_interactions_csv(
            eval_set_version_id,
            env_type=env_type,
            start_time_epoch=get_timestamp(start_time),
            end_time_epoch=get_timestamp(end_time),
            return_topics=return_topics,
            return_annotation_data=return_annotation_data,
            return_output_props=return_output_props,
            return_custom_props=return_custom_props,
            return_input_props=return_input_props,
            return_llm_props=return_llm_props,
            return_similarities=return_similarities,
            user_interaction_ids=user_interaction_ids,
            include_incomplete=include_incomplete,
            return_steps=return_steps,
        )
        if not csv_as_text:
            return pd.DataFrame()
        return pd.read_csv(io.StringIO(csv_as_text))

    @HandleExceptions(init_logger)
    def get_interaction_by_user_interaction_id(self, app_name: str, version_name: str, user_interaction_id: str) -> Interaction:
        """Get a specific interaction by its user_interaction_id.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of application version
        user_interaction_id : str
            Unique id of the interaction to get

        Returns
        -------
        Interaction
            The interaction object, including the input, output, properties and other fields
        """
        version_id = self._get_version_id(app_name=app_name, version_name=version_name)
        interaction = self.api.get_interaction_by_user_interaction_id(version_id, user_interaction_id)
        return self._build_interaction_object(interaction)

    def _get_application_id(self, app_name: str):
        app = self.api.get_application(app_name)
        if not app:
            raise DeepchecksLLMClientError(f"Application: \"{app_name}\", does not exist")
        return app["id"]

    def _get_version_id(self, app_name: str, version_name: str, create_if_not_exist: bool = False):

        app = self.api.get_application(app_name)
        if not app:
            raise DeepchecksLLMClientError(f"Application: \"{app_name}\", does not exist")
        eval_set_version = next((ver for ver in app["versions"] if ver["name"] == version_name), None)
        if not eval_set_version:
            if not create_if_not_exist:
                raise DeepchecksLLMClientError(
                    f"Could not find version \"{version_name}\", in application \"{app_name}\"",
                )
            else:
                return self.api.create_application_version(
                    application_id=app["id"], version_name=version_name,
                )["id"]

        return eval_set_version["id"]

    def get_pentest_prompts(self, app_name: str, probes: t.Optional[t.List[str]] = None) -> pd.DataFrame:
        """Get pentest prompts for the application.

        Parameters
        ----------
        app_name : str
            Application name
        probes: list of str
            List of probes to get pentest prompts for. If None, all probes will be returned.

        Returns
        -------
        pd.DataFrame
            A pandas DataFrame containing the pentest prompts
        """
        app_id = self._get_application_id(app_name)
        csv_content = self.api.get_pentest_prompts(app_id=app_id, probes=probes)
        df = pd.read_csv(io.StringIO(csv_content))
        return df

    def get_custom_properties(self, app_name: str) -> t.List[CustomPropertyType]:
        """Get the custom properties defined for the current application.

        Parameters
        ----------
        app_name : str
            Application name

        Returns
        -------
        list[CustomPropertyType]
            A list of custom properties defined for the application
        """
        app_id = self._get_application_id(app_name)
        custom_props = self.api.get_custom_properties_definitions(application_id=app_id)
        return [
            CustomPropertyType(
                display_name=prop["display_name"],
                type=prop["type"],
                description=prop["description"]
            ) for prop in custom_props
        ]

    def create_custom_property(self, app_name: str, name: str, prop_type: PropertyColumnType, description: t.Optional[str] = None
                               ) -> None:
        """Define a custom property for the current application.

        Parameters
        ----------
        app_name : str
            Application name
        name : str
            Name of the custom property
        prop_type : PropertyColumnType
            Type of the custom property
        description : str, optional
            Description of the custom property

        Returns
        -------
        None
        """
        app_id = self._get_application_id(app_name)
        self.api.create_custom_property_definition(
            application_id=app_id, name=name, prop_type=prop_type, description=description,
        )

    def update_custom_property(
            self,
            app_name: str,
            old_property_name: str,
            new_property_name: t.Optional[str] = None,
            description: t.Optional[str] = None,
    ) -> None:
        """Update a custom property for the current application.

        Parameters
        ----------
        app_name : str
            Application name
        old_property_name : str
            Name of the custom property to update
        new_property_name : str, optional
            New name for the custom property
        description : str, optional
            Description of the custom property (if none provided, the description will not be updated)

        Returns
        -------
        None
        """
        app_id = self._get_application_id(app_name)
        self.api.update_custom_property_definition(
            application_id=app_id,
            old_name=old_property_name,
            new_name=new_property_name if new_property_name else old_property_name,
            description=description,
        )

    def delete_custom_property(self, app_name: str, property_name: str):
        """Delete a custom property for the current application.

        Parameters
        ----------
        app_name : str
            Application name
        property_name : str
            Name of the custom property to delete

        Returns
        -------
        None
        """
        app_id = self._get_application_id(app_name)
        self.api.delete_custom_property_definition(application_id=app_id, name=property_name)

    @HandleExceptions(init_logger)
    def get_interactions_complete_status(
            self,
            app_name: str,
            version_name: str,
            user_interaction_ids: t.List[str],
            events_to_check: t.Optional[t.List[InteractionCompleteEvents]] = None,
    ):
        """Get the completion status of interactions for specified events and user interaction IDs.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of application version
        events_to_check : Optional[List[InteractionCompleteEvents]]
            A list of events whose completion status needs to be checked. By default, only annotation_completed is
            checked
        user_interaction_ids : List[str]
            A list of user interaction IDs to check for completion status.

        Returns
        -------
        Dict[InteractionCompleteEvents, bool]
            A dictionary where keys are events from `events_to_check`
            and values are objects that indicating whether interactions for each event are completed and number of
            completed interactions {"annotation_completed": {"all_completed": True, "number_of_completed": 10}}
        """
        if not events_to_check:
            events_to_check = [InteractionCompleteEvents.ANNOTATION_COMPLETED]

        version_id = self._get_version_id(app_name=app_name, version_name=version_name)
        return self.api.get_interactions_complete_status(
            app_version_id=version_id,
            events_to_check=events_to_check,
            user_interaction_ids=user_interaction_ids,
        )

    @HandleExceptions(init_logger)
    def get_data_if_calculations_completed(
            self,
            app_name: str,
            version_name: str,
            env_type: EnvType,
            user_interaction_ids: t.List[str],
            events_to_check: t.Optional[t.List[InteractionCompleteEvents]] = None,
            max_retries: int = 60,
            retry_interval_in_seconds: int = 20,
            return_topics: bool = True, return_annotation_data: bool = True,
            return_input_props: bool = True, return_output_props: bool = True,
            return_custom_props: bool = True, return_llm_props: bool = True,
            return_similarities: bool = False,
    ) -> t.Optional[pd.DataFrame]:
        """Check if calculations for specified events are completed by calling `get_interactions_complete_status`.

        If all user_interaction_ids completed then we will fetch the data for those ids,
        if not - will sleep and retry again. Consider increasing max_retries or retry_interval_in_seconds if running
        the method returns None.

        Parameters
        ----------
        app_name : str
            Application name
        version_name : str
            Name of application version
        env_type : EnvType
            Environment type
        events_to_check : Optional[List[InteractionCompleteEvents]]
            A list of events whose completion status needs to be checked. By default, only annotation_completed
            is checked
        user_interaction_ids : List[str]
            A list of user interaction IDs to retrieve data for.
        max_retries : Optional[int]
            Maximum number of retries if calculations are not completed. Defaults to 60.
        retry_interval_in_seconds : Optional[float]
            Interval between retries in seconds. Defaults to 20.
        return_annotation_data : bool, optional
            Whether to include annotation info in the data.
        return_topics : bool, optional
            Whether to include the topic in the data.
        return_annotation_data : bool, optional
            Whether to include annotation info in the data.
        return_input_props : bool, optional
            Whether to include input properties in the data.
        return_output_props : bool, optional
            Whether to include the output properties in the data.
        return_custom_props : bool, optional
            Whether to include custom properties in the data.
        return_llm_props : bool, optional
            Whether to include LLM properties in the data.
        return_similarities : bool, optional
            Whether to include similarities in the data.

        Returns
        -------
        Optional[pd.DataFrame]
            A DataFrame containing the retrieved data if calculations are completed, otherwise None.
        """
        if not events_to_check:
            events_to_check = [InteractionCompleteEvents.ANNOTATION_COMPLETED]
        retry_count = 0
        while retry_count < max_retries:
            complete_statuses = self.get_interactions_complete_status(
                app_name=app_name,
                version_name=version_name,
                events_to_check=events_to_check,
                user_interaction_ids=user_interaction_ids,
            )
            if all(status["all_completed"] for status in complete_statuses.values()):
                return self.get_data(
                    app_name=app_name,
                    version_name=version_name,
                    env_type=env_type,
                    return_topics=return_topics,
                    return_annotation_data=return_annotation_data,
                    return_input_props=return_input_props,
                    return_output_props=return_output_props,
                    return_custom_props=return_custom_props,
                    return_llm_props=return_llm_props,
                    return_similarities=return_similarities,
                    user_interaction_ids=user_interaction_ids,
                )
            else:
                for event, status in complete_statuses.items():
                    logger.debug(f"{event} = {status['number_of_completed']}")
                retry_count += 1
                time.sleep(retry_interval_in_seconds)
        return None

    @staticmethod
    def _build_interaction_object(interaction: dict) -> Interaction:
        return Interaction(
            user_interaction_id=interaction["user_interaction_id"],
            input=interaction["input"]["data"] if interaction.get("input") else None,
            information_retrieval=[i["data"] for i in interaction["information_retrieval"]] if
            interaction.get("information_retrieval") else None,
            history=[i["data"] for i in interaction["history"]] if interaction.get("history") else None,
            full_prompt=interaction["prompt"]["data"] if interaction.get("prompt") else None,
            output=interaction["output"]["data"] if interaction.get("output") else None,
            created_at=interaction["created_at"],
            interaction_datetime=interaction["interaction_datetime"],
            topic=interaction["topic"],
            output_properties=interaction.get("output_properties", {}) or {},
            input_properties=interaction.get("input_properties", {}) or {},
            custom_properties=interaction.get("custom_properties", {}) or {},
            llm_properties=interaction.get("llm_properties", {}) or {},
            llm_properties_reasons=interaction.get("llm_properties_reasons", {}) or {},
            is_completed=interaction["is_completed"],
        )

    @staticmethod
    def _validate_steps(steps: t.Union[t.List[Step], None]):
        if steps:
            for step in steps:
                if step.type == StepType.INFORMATION_RETRIEVAL:
                    logger.warning("Information retrieval step is deprecated, use information_retrieval field instead")
