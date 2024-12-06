from inspect import stack
from logging import Logger, getLogger
import requests
from pandas import DataFrame
from pydash import pick, mapcat
from requests import Response
from requests.auth import HTTPBasicAuth
import json
import pandas as pd

class JiraIssuesGetter:
    _obj_logger: Logger = getLogger(__name__)
    _str_username: str
    _str_password: str
    _str_url: str

    __FIELDS__: list[dict] = [
        { "json.field": "id", "df.field": "id"},
        { "json.field": "key", "df.field": "key"},
        { "json.field": "fields.summary", "df.field": "summary"},
        { "json.field": "fields.resolution.name", "df.field": "resolution"},
        { "json.field": "fields.status.name", "df.field": "status"},
        { "json.field": "fields.issuetype.name", "df.field": "type"},
        { "json.field": "fields.parent.id", "df.field": "parent"},
        { "json.field": "fields.created", "df.field": "created"},
        { "json.field": "fields.updated", "df.field": "updated"},
        { "json.field": "fields.priority.name", "df.field": "priority"},
        { "json.field": "fields.assignee.displayName", "df.field": "assignee"},
        { "json.field": "fields.creator.displayName", "df.field": "creator"},
        { "json.field": "fields.customfield_10039", "df.field": "points"}
    ]

    def __init__(
            self,
            str_username: str,
            str_password: str,
            str_url: str
    ):
        self._str_username = str_username
        self._str_password = str_password
        self._str_url = str_url

    def get_issues(
            self,
            int_start: int = 0,
            int_max: int = 50
    ) -> DataFrame:

        self._obj_logger.debug("abc"
            f"Function '{stack()[0].filename} - {stack()[0].function}' is called with parameters:\n"
            f"- int_start: '{int_start}'\n"
            f"- int_max: '{int_max}'."
        )

        _dict_the_query: dict = {
            'jql': 'project = GENO',
            'startAt': int_start,
            'maxResults': int_max
            # 'nextPageToken': '<string>',
            # 'maxResults': '{maxResults}',
            #'fields': 'summary,key',
            # 'expand': 'versionedRepresentations',
            # 'reconcileIssues': '{versionedRepresentations}'
        }

        _obj_the_response: Response = requests.request(
            "GET",
            self._str_url ,
            headers= {
                "Accept": "application/json"
            },
            params=_dict_the_query,
            auth=HTTPBasicAuth(self._str_username, self._str_password)
        )

        if _obj_the_response.status_code != 200:
            raise Exception(f"REST requested returned '{_obj_the_response.status_code}'.")

        _dict_the_issues: dict = json.loads(_obj_the_response.text)

        _lst_the_issues = mapcat(_dict_the_issues["issues"], lambda x: pick(
            x,
            *[field["json.field"] for field in self.__FIELDS__]
        ))

        _df_the_return: DataFrame = pd.json_normalize(_lst_the_issues).rename(columns={
            field["json.field"]: field["df.field"] for field in self.__FIELDS__
        })

        # We recursively call the function...
        _int_the_max_result: int = _dict_the_issues["maxResults"]
        _int_the_start_at: int = _dict_the_issues["startAt"]
        _int_the_total: int = _dict_the_issues["total"]
        if _int_the_total > (_int_the_start_at + _int_the_max_result):
            _df_the_return = pd.concat(
                [_df_the_return, self.get_issues(_int_the_start_at+_int_the_max_result, _int_the_max_result)]
            )

        # We ensure we have all the expected columns
        _lst_missing_columns: list[str] = [
            i_col["df.field"]
            for i_col in self.__FIELDS__
            if i_col["df.field"] not in _df_the_return.columns
        ]
        if len(_lst_missing_columns):
            self._obj_logger.warning(f"Following columns were not provided by Jira. They will be added and "
                                  f"defaulted for the sake of returning same structure... Maybe check in Jira "
                                  f"if these fields are still to be expected:\n- {'\n- '.join(_lst_missing_columns)}")
            for i_col in _lst_missing_columns:
                _df_the_return[i_col] = None

        self._obj_logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning "
                               f"a DataFrame containing '{len(_df_the_return.index)}' lines.")

        return _df_the_return.reset_index(drop=True)