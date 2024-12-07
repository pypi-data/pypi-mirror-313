import pytest
import pandas as pd

from biorat.ontology import owl_to_dataframe

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_owl_to_dataframe():
    result_df = owl_to_dataframe("https://github.com/obophenotype/cell-ontology/releases/download/v2024-09-26/cl.owl")
    assert result_df is not None
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) > 0
