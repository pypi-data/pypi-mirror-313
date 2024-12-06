from unittest import TestCase

import pandas

from tecton_core import conf
from tecton_core.data_processing_utils import split_spine


df = pandas.DataFrame({"join_key": ["abc", "abd", "dbc", "dbe", "ace", "xyz", "xya", "xzz"]})
join_keys = ["join_key"]


class SpineSplitTest(TestCase):
    def test_spine_split_even(self):
        conf.set("DUCKDB_SPINE_SPLIT_STRATEGY", "even")
        conf.set("DUCKDB_SPINE_SPLIT_COUNT", 3)

        split_dfs = split_spine(df, join_keys)

        assert pandas.DataFrame.equals(split_dfs[0], pandas.DataFrame({"join_key": ["abc", "abd", "ace"]}))
        assert pandas.DataFrame.equals(split_dfs[1], pandas.DataFrame({"join_key": ["dbc", "dbe", "xya"]}))
        assert pandas.DataFrame.equals(split_dfs[2], pandas.DataFrame({"join_key": ["xyz", "xzz"]}))

    def test_spine_split_minimize_distance(self):
        conf.set("DUCKDB_SPINE_SPLIT_STRATEGY", "minimize_distance")
        conf.set("DUCKDB_SPINE_SPLIT_COUNT", 3)

        split_dfs = split_spine(df, join_keys)

        assert pandas.DataFrame.equals(split_dfs[0], pandas.DataFrame({"join_key": ["abc", "abd", "ace"]}))
        assert pandas.DataFrame.equals(split_dfs[1], pandas.DataFrame({"join_key": ["dbc", "dbe"]}))
        assert pandas.DataFrame.equals(split_dfs[2], pandas.DataFrame({"join_key": ["xya", "xyz", "xzz"]}))

    def test_spine_split_agglomerative_clustering(self):
        conf.set("DUCKDB_SPINE_SPLIT_STRATEGY", "agglomerative_clustering")
        conf.set("DUCKDB_SPINE_SPLIT_COUNT", 3)

        split_dfs = split_spine(df, join_keys)
        assert pandas.DataFrame.equals(split_dfs[0], pandas.DataFrame({"join_key": ["xyz", "xya", "xzz"]}))
        assert pandas.DataFrame.equals(split_dfs[1], pandas.DataFrame({"join_key": ["abc", "abd", "ace"]}))
        assert pandas.DataFrame.equals(split_dfs[2], pandas.DataFrame({"join_key": ["dbc", "dbe"]}))
