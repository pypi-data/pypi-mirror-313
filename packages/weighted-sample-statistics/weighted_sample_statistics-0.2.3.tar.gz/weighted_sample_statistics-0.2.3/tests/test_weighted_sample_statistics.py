from weighted_sample_statistics import WeightedSampleStatistics

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"


def test_class_import():
    weighted_sample_statistics = WeightedSampleStatistics(
        group_keys=None, records_df_selection=None, weights_df=None
    )
    assert weighted_sample_statistics.group_keys is None
