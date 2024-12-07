import json
import os

import litellm
import pandas as pd
import requests

from rumorz.encoder import RumorzJSONEncoder

litellm.set_verbose = False


class RumorzAPIException(Exception):
    pass


class RumorzClient:
    def __init__(self,
                 api_key=os.environ['RUMORZ_API_KEY'],
                 api_url=os.environ.get('RUMORZ_API_URL', 'http://rumorz-api.eastus2.azurecontainer.io'),
                 api_version='v0'):
        self.api_url = api_url
        self.api_version = api_version
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
        self.graph = self.Graph(self)
        self.agent = self.Agent(self)
        response = requests.post(self.api_url + '/ping', headers=self.headers, timeout=5)
        response.raise_for_status()

    def call_function(self, function_name, params):
        url = f"{self.api_url}/{self.api_version}/{function_name}"
        json_data = json.dumps(params, cls=RumorzJSONEncoder)
        response = requests.post(url, json=json_data, headers=self.headers, timeout=30)
        try:
            response.raise_for_status()
            return response.json()['data']
        except Exception as e:
            raise RumorzAPIException(response.text)

    class Graph:

        def __init__(self, api):
            self.api = api

        def get_feed(self,
                     **kwargs):
            return self.api.call_function('graph/get_feed', params=kwargs)

        def search_entities(self,
                            **kwargs):
            """
            Search for entities in the Rumorz Graph by name and/or symbol
            """
            return self.api.call_function('graph/search_entities', params=kwargs)

        def get_ranking(self,
                        **kwargs):
            """
            Returns a ranking of every single entity in the Graph based on the given parameters.
            """
            return self.api.call_function('graph/get_ranking', params=kwargs)

        def get_metrics(self,
                        as_df=True,
                        **kwargs):
            """
            Get metrics for an entity in the Rumorz Graph
            """
            timeseries = self.api.call_function('graph/get_metrics', params=kwargs)
            if as_df:
                dfs = {}
                for node_ts in timeseries:
                    data = {ts['metric']: [v[1] for v in ts['values']] for ts in node_ts['time_series']}
                    timestamps = [v[0] for v in node_ts['time_series'][0]['values']]
                    df = pd.DataFrame(data, index=pd.to_datetime(timestamps))
                    dfs[node_ts['entity_id']] = df
                return dfs

        def get_price_stats(self,
                            **kwargs):
            """
            Get summary price stats of a financial asset entity in the Rumorz Graph
            """
            return self.api.call_function('graph/get_price_stats', params=kwargs)


    class Agent:
        def __init__(self, api):
            self.api = api

        def create_agent(self,
                         **kwargs):
            """
            Create an agent with a goal, name and personality
            """
            return self.api.call_function('agent/create_agent', params=kwargs)

        def summarize(self,
                      **kwargs):
            """
            Summarize events and news for any entity in the graph
            """
            return self.api.call_function('agent/summarize', params=kwargs)

        def get_state(self,
                      **kwargs):
            """
            Get the state of an agent. This includes current sentiment, personality, trading strategy, and more.
            """
            return self.api.call_function('agent/get_state', params=kwargs)

        def get_logs(self,
                     **kwargs):
            return self.api.call_function('agent/get_logs', params=kwargs)
