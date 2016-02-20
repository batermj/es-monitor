import unittest
import es_query


class SelectInsideLeafResponseTest(unittest.TestCase):
    def test_no_group_by(self):
        executor = es_query.create_executor("select count(*) from quote")
        rows = executor.select_response({
            "hits": {
                "hits": [],
                "total": 20994400,
                "max_score": 0.0
            },
            "_shards": {
                "successful": 1,
                "failed": 0,
                "total": 1
            },
            "took": 26,
            "timed_out": False
        })
        self.assertEqual([{'count(*)': 20994400}], rows)

    def test_single_group_by(self):
        executor = es_query.create_executor("select exchange, count(*) from symbol group by exchange")
        rows = executor.select_response({
            "hits": {
                "hits": [],
                "total": 6714,
                "max_score": 0.0
            },
            "_shards": {
                "successful": 1,
                "failed": 0,
                "total": 1
            },
            "took": 23,
            "aggregations": {
                "exchange": {
                    "buckets": [
                        {
                            "key": "nyse",
                            "doc_count": 3240
                        },
                        {
                            "key": "nasdaq",
                            "doc_count": 3089
                        },
                        {
                            "key": "nyse mkt",
                            "doc_count": 385
                        }
                    ],
                    "sum_other_doc_count": 0,
                    "doc_count_error_upper_bound": 0
                }
            },
            "timed_out": False
        })
        self.assertEqual(
            [{'count(*)': 3240, u'exchange': 'nyse'},
             {'count(*)': 3089, u'exchange': 'nasdaq'},
             {'count(*)': 385, u'exchange': 'nyse mkt'}],
            rows)

    def test_multiple_group_by(self):
        executor = es_query.create_executor(
            "select exchange, sector, max(market_cap) from symbol group by exchange, sector")
        rows = executor.select_response({
            "hits": {
                "hits": [],
                "total": 6714,
                "max_score": 0.0
            },
            "_shards": {
                "successful": 1,
                "failed": 0,
                "total": 1
            },
            "took": 11,
            "aggregations": {
                "exchange": {
                    "buckets": [
                        {
                            "sector": {
                                "buckets": [
                                    {
                                        "max(market_cap)": {
                                            "value": 1409695805.0
                                        },
                                        "key": "n/a",
                                        "doc_count": 963
                                    }
                                ],
                                "sum_other_doc_count": 0,
                                "doc_count_error_upper_bound": 0
                            },
                            "key": "nyse",
                            "doc_count": 3240
                        },
                        {
                            "sector": {
                                "buckets": [
                                    {
                                        "max(market_cap)": {
                                            "value": 30620000000.0
                                        },
                                        "key": "Finance",
                                        "doc_count": 637
                                    },
                                    {
                                        "max(market_cap)": {
                                            "value": 126540000000.0
                                        },
                                        "key": "Health Care",
                                        "doc_count": 621
                                    }
                                ],
                                "sum_other_doc_count": 0,
                                "doc_count_error_upper_bound": 0
                            },
                            "key": "nasdaq",
                            "doc_count": 3089
                        },
                        {
                            "sector": {
                                "buckets": [
                                    {
                                        "max(market_cap)": {
                                            "value": 971774087.0
                                        },
                                        "key": "n/a",
                                        "doc_count": 123
                                    },
                                    {
                                        "max(market_cap)": {
                                            "value": 424184478.0
                                        },
                                        "key": "Basic Industries",
                                        "doc_count": 52
                                    }
                                ],
                                "sum_other_doc_count": 0,
                                "doc_count_error_upper_bound": 0
                            },
                            "key": "nyse mkt",
                            "doc_count": 385
                        }
                    ],
                    "sum_other_doc_count": 0,
                    "doc_count_error_upper_bound": 0
                }
            },
            "timed_out": False
        })
        self.assertEqual(
            [{u'sector': 'n/a', 'max(market_cap)': 1409695805.0, u'exchange': 'nyse'},
             {u'sector': 'Finance', 'max(market_cap)': 30620000000.0, u'exchange': 'nasdaq'},
             {u'sector': 'Health Care', 'max(market_cap)': 126540000000.0, u'exchange': 'nasdaq'},
             {u'sector': 'n/a', 'max(market_cap)': 971774087.0, u'exchange': 'nyse mkt'},
             {u'sector': 'Basic Industries', 'max(market_cap)': 424184478.0, u'exchange': 'nyse mkt'}],
            rows)
