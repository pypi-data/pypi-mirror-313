import datetime as dt
import os
import unittest
from rumorz.client import RumorzClient, RumorzAPIException
from rumorz.enums import AssetClass, EntityType, EntityMetrics, Lookback, EntityMetricTransform

rumorz = RumorzClient(api_key=os.environ['RUMORZ_API_KEY'],
                      api_url=os.environ.get('RUMORZ_API_URL', 'http://localhost:8000'))


class TestRumorz(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        entities = rumorz.graph.search_entities(**{
            "name": "Bitcoin",
            "asset_class": AssetClass.CRYPTO,
            "entity_type": EntityType.FINANCIAL_ASSET,
            "symbol_search": "BTC",
            "limit": 1
        })
        assert len(entities) == 1, "Bitcoin entity search returned an unexpected number of results"
        cls.bitcoin_entity_id = entities[0]['id']

    def test_time_series(self):
        timeseries = rumorz.graph.get_metrics(**{
            "operation": EntityMetricTransform.LAST,
            "ids": [self.bitcoin_entity_id],
            "metrics":  [EntityMetrics.SENTIMENT, EntityMetrics.MENTIONS],
            "lookback": Lookback.ONE_DAY,
            "page": 1,
            "limit": 100
        })
        self.assertTrue(len(timeseries) > 0)

    def test_entity_summary(self):
        entity_update = rumorz.agent.summarize(**{
            "id": self.bitcoin_entity_id,
            "timestamp": dt.datetime.utcnow().isoformat(),
            "scores_filter": "sentiment > 0.75"
        })
        self.assertTrue(len(entity_update) > 0)

    def test_get_ranking(self):
        screener = rumorz.graph.get_ranking(**{
            "lookback": Lookback.ONE_DAY,
            "page": 1,
            "limit": 10,
            "sort_by": EntityMetrics.SENTIMENT,
            "entity_type": "financial_asset",
            "scores_filter": 'mentions > 10',
            "ascending": False
        })
        self.assertTrue(len(screener) > 0)

    def test_limit_validation(self):
        try:
            rumorz.graph.get_ranking(**{
                "lookback": "1D",
                "page": 1,
                "limit": 1000,
                "sort_by": "mentions",
                "entity_type": "financial_asset",
            })
        except Exception as e:
            self.assertTrue("limit" in str(e).lower())

    def test_get_feed(self):
        posts = rumorz.graph.get_feed(**{
            "ids": [self.bitcoin_entity_id],
            "lookback": "3D",
            "scores_filter": "sentiment > 0.75",
            "page": 1,
            "limit": 10
        })
        self.assertTrue(len(posts) > 0)

    def test_get_price_stats(self):
        summary = rumorz.graph.get_price_stats(**{
            "id": self.bitcoin_entity_id,
        })
        print(summary)
        self.assertTrue(len(summary) > 0)



# <start_ignore>
    def test_agent_state(self):
        try:
            rumorz.agent.get_state(id='xxxx')
        except Exception as e:
            self.assertTrue(isinstance(e, RumorzAPIException))

    def test_agent_logs(self):
        logs = rumorz.agent.get_logs(id='36a5e6ba-160d-45bf-b28a-bea369e0136f',
                                     lookback="1D",
                                     limit=10)
        self.assertIsNotNone(logs)
# <end_ignore>