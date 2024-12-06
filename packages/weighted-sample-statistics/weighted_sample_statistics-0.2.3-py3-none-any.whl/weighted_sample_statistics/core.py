"""
Definition of weighted_sample_statistics class to calculate weighted weighted_sample_statistics
"""

import logging
import re
from typing import Union, Iterable, Optional
from unittest.mock import inplace

import numpy as np
from pandas import DataFrame

DataFrameType = Union[DataFrame, None]

logger = logging.getLogger(__name__)


def make_negation_name(column_name: str, suffix: str = "_x") -> str:
    """Make a new column name for complementary values.

    Returns
    -------
    negation_name : str
    """
    negation_name = re.sub(r"_\d\.\d$", "", column_name) + suffix
    if re.search(r"_\d\.\d$", column_name):
        negation_name += re.search(r"_\d\.\d$", column_name).group()
    return negation_name


class WeightedSampleStatistics:
    """
    Calculate weighted_sample_statistics for summations

    Parameters
    ----------
    group_keys: iterable
        The variables to use to group
    records_df_selection: DataFrame
        All the microdata including non-response
    weights_df: DataFrame
        The weights per unit
    all_records_df: DataFrame
        All the microdata including non-response
    column_list: iterable
        list of columns to calculate weighted_sample_statistics
    scaling_factor_key: str
        Name of the weight variable
    var_type: str
        Type of the data
    add_inverse: bool
        Add the negated value as well for booleans
    report_numbers: bool
        Do not calculate the average, but the sum

    Attributes
    ----------
    records_sum: grouped
        The summation of the weighted values
    number_samples_sqrt: grouped
        The square root of the sample size n
    standard_error: grouped
        The standard error of the mean estimate: std / n_sqrt
    """

    def __init__(
        self,
        group_keys: Iterable,
        records_df_selection: DataFrame,
        weights_df: DataFrame,
        column_list: Optional[Iterable] = None,
        var_type: Optional[str] = None,
        scaling_factor_key: Optional[str] = None,
        units_scaling_factor_key: Optional[str] = None,
        all_records_df: Optional[DataFrame] = None,
        var_weight_key: Optional[str] = None,
        variance_df_selection: Optional[DataFrame] = None,
        records_df_unfilled: Optional[DataFrame] = None,
        add_inverse: bool = False,
        report_numbers: bool = False,
        negation_suffix: Optional[str] = None,
        start: bool = False,
    ) -> None:
        """
        Initialize the WeightedSampleStatistics object.

        This object is used to calculate weighted sample statistics for a given
        DataFrame.
        The object can be initialized with a set of records, weights, and a list of columns to
        calculate statistics for.
        The object can also be initialized with a set of all records, including non-response, and a
        variable weight.
        The object can also be initialized with a set of variance selection data and a set of
        unfilled records.

        Parameters
        ----------
        group_keys : Iterable
            The variables to use for grouping.
        records_df_selection : DataFrame
            The DataFrame containing the selected records.
        weights_df : DataFrame
            The DataFrame containing the weights per unit.
        column_list : Iterable, optional
            List of columns to calculate statistics for.
            Default is None.
        var_type : str, optional
            The type of the data.
            Default is None.
        scaling_factor_key : str, optional
            The key for the scaling factor.
            Default is None.
        units_scaling_factor_key : str, optional
            The key for the unit scaling factor.
            Default is None.
        all_records_df : DataFrame, optional
            DataFrame containing all records, including non-response.
            Default is None.
        var_weight_key : str, optional
            The key for the variable weight.
            Default is None.
        variance_df_selection : DataFrame, optional
            DataFrame containing variance selection data.
            Default is None.
        records_df_unfilled : DataFrame, optional
            DataFrame containing unfilled records.
            Default is None.
        add_inverse : bool, optional
            Whether to add the negated value for booleans.
            Default is False.
        report_numbers : bool, optional
            Whether to report numbers instead of calculating the average.
            Default is False.
        negation_suffix : str, optional
            Suffix to use for negated values.
            Default is "_x".
        start : bool, optional
            Whether to start calculations immediately.
            Default is False.
        """
        # Initialize instance variables
        self.group_keys = group_keys
        self.records_df_selection = records_df_selection
        self.weights_df = weights_df
        self.column_list = column_list or []
        self.var_type = var_type
        self.scaling_factor_key = scaling_factor_key
        self.units_scaling_factor_key = units_scaling_factor_key
        self.all_records_df = all_records_df
        self.var_weight_key = var_weight_key
        self.variance_df_selection = variance_df_selection
        self.records_df_unfilled = records_df_unfilled
        self.add_inverse = add_inverse
        self.report_numbers = report_numbers
        self.negation_suffix = negation_suffix or "_x"
        self.group_keys = group_keys
        self.records_df_selection = records_df_selection
        self.weights_df = weights_df
        self.column_list = column_list or []
        self.var_type = var_type
        self.scaling_factor_key = scaling_factor_key
        self.units_scaling_factor_key = units_scaling_factor_key
        self.all_records_df = all_records_df
        self.var_weight_key = var_weight_key
        self.variance_df_selection = variance_df_selection
        self.records_df_unfilled = records_df_unfilled
        self.add_inverse = add_inverse
        self.report_numbers = report_numbers
        self.negation_suffix = negation_suffix or "_x"

        self.weights_sel_sum_df = None
        self.scale_variabele_sel_grp = None
        self.scale_variabele_pop_grp = None
        self.var_weight_sel_grp = None
        self.var_weight_pop_grp = None
        self.unit_weights_pop_grp = None
        self.unit_weights_sel_grp = None
        self.weights_sel_grp = None
        self.weights_grp = None
        self.all_records_grp = None
        self.variance_sel_grp = None
        self.records_valid_grp = None
        self.records_sel_grp = None
        self.unit_weights_pop_grp = None
        self.unit_weights_sel_grp = None
        self.weights_sel_grp = None
        self.weights_grp = None
        self.all_records_grp = None
        self.variance_sel_grp = None
        self.records_valid_grp = None
        self.records_sel_grp = None
        self.weights = None
        self.records_df_valid = None
        self.var_weight_sel_df = None
        self.scale_variabele_sel_df = None
        self.var_weight_pop_df = None
        self.scale_variabele_pop_df = None
        self.unit_weights_sel_df = None
        self.unit_weights_pop_df = None
        self.weights_sel_df = None
        self.response_fraction = None

        self.weights = None
        self.records_df_valid = None
        self.var_weight_sel_df = None
        self.scale_variabele_sel_df = None
        self.var_weight_pop_df = None
        self.scale_variabele_pop_df = None
        self.unit_weights_sel_df = None
        self.unit_weights_pop_df = None
        self.weights_sel_df = None
        self.standard_error = None
        self.number_samples_sqrt = None
        self.n_sample = None
        self.records_std_df = None
        self.records_std_agg = None
        self.records_var_agg = None
        self.records_var_df = None
        self.proportion_pop_grp = None
        self.proportion_pop_mean_agg = None
        self.proportion_sel_grp = None
        self.proportion_sel_mean_agg = None
        self.proportion_weighted_pop_df = None
        self.number_ratio = None
        self.records_norm_sel_df = None
        self.proportion_weighted_sel_df = None
        self.proportion_pop_df = None
        self.records_norm_pop_df = None
        self.proportion_sel_df = None
        self.records_sum = None
        self.response_count = None
        self.records_weighted_conditional_mean_agg = None
        self.records_weighted_mean_agg = None
        self.sample_count_initial = None
        self.records_weighted_sel_mean_df = None
        self.records_weighted_pop_mean_df = None
        self.records_weighted_pop_grp = None
        self.records_weighted_pop_df = None
        self.records_weighted_sel_df = None
        self.weights_pop_normalized_df = None
        self.unit_weights_pop_sum_agg = None
        self.var_weights_pop_sum_agg = None
        self.var_weights_pop_sum_df = None
        self.weights_sel_normalized_df = None
        self.records_weighted_sel_grp = None
        self.var_weights_sel_sum_df = None
        self.unit_weights_pop_sum_df = None
        self.unit_weights_sel_sum_agg = None
        self.unit_weights_sel_sum_df = None
        self.var_weights_sel_sum_agg = None
        self.weights_pop_sum_agg = None
        self.weights_sel_sum_agg = None
        self.weights_pop_sum_df = None

        # If start is True, begin calculations immediately
        if start:
            self.calculate()

    def calculate(self) -> None:
        """
        Perform all calculations required for weighted sample statistics.

        This method orchestrates the sequence of calculations necessary to
        determine weighted means, proportions, and standard errors.
        It also calculates the response fraction if all records are provided.

        Returns
        -------
        None
        """
        # Set the mask for valid data entries
        self.set_mask_valid_df()

        # Scale the variables based on the provided scaling factors
        self.scale_variables()

        # Group the variables as per the specified grouping keys
        self.group_variables()

        # Calculate the weighted means for the records
        self.calculate_weighted_means()

        # If all records are available, calculate the response fraction
        if self.all_records_df is not None:
            self.calculate_response_fraction()

        # Calculate the proportions for the selected and population data
        self.calculate_proportions()

        # Calculate the standard errors for the estimates
        self.calculate_standard_errors()

    def scale_variables(self):
        """Scale the variables with the scaling factor.

        This function scales the variables by the scaling factor.
        """
        logger.debug(f"Scaling variables with {self.scaling_factor_key}")

        # The weights are the scaling factors
        self.weights = self.weights_df.loc[:, self.scaling_factor_key]

        # The unit weights are the scaling factors for the population
        self.unit_weights_pop_df = self.weights_df.loc[:, self.units_scaling_factor_key]

        # The fixed variables are the scaling variables
        fixed = set(list([self.var_weight_key, self.scaling_factor_key]))

        # Check if the variable to process (stored in the column list) is a scaling variable
        if set(self.column_list).intersection(fixed):
            # In case the variable to process (stored in the column list) is a scaling variable,
            # we do not scale it, so set the weights to 1
            self.weights.values[:] = 1.0

        # The weights for the selection are the same as the weights
        self.weights_sel_df = self.weights.reindex(
            self.records_df_selection.index
        ).astype(float)

        # The unit weights for the selection are the same as the unit weights
        self.unit_weights_sel_df = self.unit_weights_pop_df.reindex(
            self.records_df_selection.index
        ).astype(float)

        # The scale variable for the population is the variable to be scaled
        self.scale_variabele_pop_df = self.weights_df[self.var_weight_key].astype(float)

        # The scale variable for the selection is the same as the scale variable for the population
        self.scale_variabele_sel_df = self.scale_variabele_pop_df.reindex(
            self.records_df_selection.index
        ).astype(float)

        # Now we have the numerator, we also need to scale the denominator.
        # The variable to be scaled for the population is the scaling factor times the variable
        self.var_weight_pop_df = (
            self.weights_df[self.scaling_factor_key] * self.scale_variabele_pop_df
        )
        self.var_weight_pop_df = self.var_weight_pop_df.astype(float)

        # The variable to be scaled for the selection is the same as the variable to be scaled
        # for the population
        self.var_weight_sel_df = self.var_weight_pop_df.reindex(
            self.records_df_selection.index
        )
        self.var_weight_sel_df = self.var_weight_sel_df.astype(float)

    def set_mask_valid_df(self):
        """Set mask valid df

        This function sets the mask for the valid records for the
        selected variables.
        This mask is used to select the valid records from the dataframe of the population.

        Returns
        -------
        None
        """
        logger.debug("Setting mask for valid records")

        if self.records_df_unfilled is not None:
            logger.debug("Set mask for valid records to True if not NaN")
            self.records_df_valid = ~self.records_df_unfilled.isna()
            try:
                logger.debug("Select only columns in self.column_list")
                self.records_df_valid = self.records_df_valid[self.column_list]
            except KeyError:
                logger.debug("No valid columns found in records_df_unfilled")
                col = re.sub(r"_\d\.\d", "", self.column_list[0])
                try:
                    logger.debug("Select only column in self.column_list")
                    self.records_df_valid = self.records_df_valid[col]
                except KeyError:
                    logger.debug("No valid columns found in records_df_unfilled")
                    self.records_df_valid = None

    def group_variables(self):
        """Group the variables according to the group keys.

        This function groups the variables and the weights according to the
        specified group keys.
        The grouped variables are stored as attributes of the class for later use.

        Returns
        -------
        None
        """
        logger.debug(f"Grouping variables with {self.group_keys}")
        # Group the records according to the group keys
        self.records_sel_grp = self.records_df_selection.groupby(self.group_keys)

        # Group the variance (if it is present)
        if self.variance_df_selection is not None:
            self.variance_sel_grp = self.variance_df_selection.groupby(self.group_keys)

        # Group the valid records
        if self.records_df_valid is not None:
            self.records_valid_grp = self.records_df_valid.groupby(self.group_keys)

        # Group the all records (if it is present)
        if self.all_records_df is not None:
            # Add the variable weight to the all records if it is not present
            if self.var_weight_key not in self.all_records_df.columns:
                self.all_records_df[self.var_weight_key] = 1
            # Group the all records
            self.all_records_grp = self.all_records_df[self.var_weight_key].groupby(
                self.group_keys
            )

        # Group the weights
        self.weights_grp = self.weights.groupby(self.group_keys)
        self.weights_sel_grp = self.weights_sel_df.groupby(self.group_keys)

        # Group the unit weights
        self.unit_weights_sel_grp = self.unit_weights_sel_df.groupby(self.group_keys)
        self.unit_weights_pop_grp = self.unit_weights_pop_df.groupby(self.group_keys)

        # Group the variable weights
        self.var_weight_pop_grp = self.var_weight_pop_df.groupby(self.group_keys)
        self.var_weight_sel_grp = self.var_weight_sel_df.groupby(self.group_keys)

        # Group the scaled variables
        self.scale_variabele_pop_grp = self.scale_variabele_pop_df.groupby(
            self.group_keys
        )
        self.scale_variabele_sel_grp = self.scale_variabele_sel_df.groupby(
            self.group_keys
        )

    def calculate_weighted_means(self):
        """Calculate summed weighted statistics for the selected columns.

        This method calculates the weighted sums and means for the selected
        columns in the dataset.
        It normalizes weights, applies them to the records, and handles special cases such as
        empty selections and negation of values.

        Returns
        -------
        None
        """
        logger.debug(
            f"Start calculation summed weighted_sample_statistics for {self.column_list}"
        )

        if "omzet_enq" in self.column_list:
            logger.debug("Stop hier")
            return

        # Calculate the sum of weights for selection and population
        self.weights_sel_sum_df = self.weights_sel_grp.transform("sum")
        self.weights_pop_sum_df = self.weights_grp.transform("sum")
        self.weights_sel_sum_agg = self.weights_sel_grp.sum()
        self.weights_pop_sum_agg = self.weights_grp.sum()

        # Calculate the sum of unit weights for selection and population
        self.unit_weights_sel_sum_df = self.unit_weights_sel_grp.transform("sum")
        self.unit_weights_pop_sum_df = self.unit_weights_pop_grp.transform("sum")

        # Calculate the sum of variable weights for selection and population
        self.var_weights_sel_sum_df = self.var_weight_sel_grp.transform("sum")
        self.var_weights_pop_sum_df = self.var_weight_pop_grp.transform("sum")
        self.var_weights_sel_sum_agg = self.var_weight_sel_grp.sum()
        self.var_weights_pop_sum_agg = self.var_weight_pop_grp.sum()

        # Aggregate sum of unit weights for selection and population
        self.unit_weights_sel_sum_agg = self.unit_weights_sel_grp.sum()
        self.unit_weights_pop_sum_agg = self.unit_weights_pop_grp.sum()

        # Normalize weights with selection sums
        logger.debug(f"Normalizing weights with sums in selection")
        self.weights_sel_normalized_df = self.weights.div(
            self.weights_sel_sum_df, axis="index"
        )
        self.weights_sel_normalized_df = self.weights_sel_normalized_df.reindex(
            self.weights_sel_sum_df.index
        )

        # Normalize weights with population sums
        logger.debug(f"Normalizing weights with sums in population")
        self.weights_pop_normalized_df = self.weights.div(
            self.weights_pop_sum_df, axis="index"
        )
        self.weights_pop_normalized_df = self.weights_pop_normalized_df.reindex(
            self.weights_pop_normalized_df.index
        )

        # Apply normalized weights to records
        logger.debug(f"Applying weights to records")
        self.records_weighted_sel_df = self.records_df_selection.mul(
            self.weights_sel_normalized_df, axis="index"
        )
        self.records_weighted_pop_df = self.records_df_selection.mul(
            self.weights_pop_normalized_df, axis="index"
        )

        # Group weighted records by selection and population
        self.records_weighted_sel_grp = self.records_weighted_sel_df.groupby(
            self.group_keys
        )
        self.records_weighted_pop_grp = self.records_weighted_pop_df.groupby(
            self.group_keys
        )

        # Transform to get summed weighted means
        self.records_weighted_sel_mean_df = self.records_weighted_sel_grp.transform(
            "sum"
        )
        self.records_weighted_pop_mean_df = self.records_weighted_pop_grp.transform(
            "sum"
        )

        # Aggregate weighted means
        logger.debug(f"Calculating weighted means")
        self.records_weighted_mean_agg = self.records_weighted_pop_grp.sum()
        self.records_weighted_conditional_mean_agg = self.records_weighted_sel_grp.sum()

        # Calculate the sum of conditional weighted means
        logger.debug(f"Calculating conditional weighted means")
        self.records_sum = self.records_weighted_conditional_mean_agg.mul(
            self.weights_sel_sum_agg, axis="index"
        )

        # Handle NaN values by filling them with 0
        logger.debug(f"Fill NaN's with 0")
        self.records_sum = self.records_sum.astype(float).fillna(0)

        # Add negated values if required
        if self.add_inverse:
            for col_name in self.records_sum:
                new_col = make_negation_name(col_name, self.negation_suffix)
                logger.debug(f"Creating new negated column {new_col}")
                filter_sum = self.var_weights_sel_sum_agg.reindex(
                    self.records_sum.index
                ).fillna(0)
                self.records_sum[new_col] = filter_sum - self.records_sum[col_name]

        # Count the response for each group
        self.response_count = self.weights_grp.count()

        # Convert to percentage if variable type is boolean or dictionary
        if self.var_type in ("bool", "dict"):
            self.records_weighted_mean_agg *= 100
            self.records_weighted_conditional_mean_agg *= 100

    def calculate_response_fraction(self):
        """Calculate response fraction"""
        logger.debug("Calculating the response fractions")
        self.sample_count_initial = self.all_records_grp.count()
        if self.records_valid_grp is not None:
            valid_vals = self.records_valid_grp.sum()
        else:
            valid_vals = self.response_count
        response_series = 100 * valid_vals.div(self.sample_count_initial, axis="index")

        # turn the response series into a dataframe with the same number of columns and column
        # names as the mean
        for col_name in self.column_list:
            try:
                response_df: DataFrameType = response_series.to_frame(name=col_name)
            except AttributeError:
                logger.debug("Failed to transfer to frame. It is a frame already")
                response_df = response_series
            if self.response_fraction is None:
                self.response_fraction = response_df
            else:
                self.response_fraction = self.response_fraction.join(response_df)

    def calculate_proportions(self):
        """Calculate proportions"""
        logger.debug("Calculating the proportions")

        # normaliseer de records variable met de schaalfactor
        self.records_norm_pop_df = self.records_df_selection.div(
            self.scale_variabele_pop_df, axis="index"
        )
        self.records_norm_pop_df.clip(lower=0, upper=1, inplace=True)
        self.records_norm_sel_df = self.records_norm_pop_df.reindex(
            self.records_df_selection.index
        )

        sum_unit_weight = self.unit_weights_sel_sum_df
        sum_weight = self.var_weights_sel_sum_df
        try:
            self.number_ratio = sum_unit_weight.div(sum_weight, axis="index")
        except AttributeError as err:
            logger.warning(f"{err}")
            return

        self.proportion_sel_df = 100 * self.records_norm_sel_df
        self.proportion_pop_df = 100 * self.records_norm_pop_df

        self.proportion_weighted_sel_df = self.proportion_sel_df.mul(
            self.weights_sel_normalized_df, axis="index"
        )

        self.proportion_weighted_pop_df = self.proportion_pop_df.mul(
            self.weights_pop_normalized_df, axis="index"
        )

        self.proportion_sel_grp = self.proportion_weighted_sel_df.groupby(
            self.group_keys
        )
        self.proportion_pop_grp = self.proportion_weighted_pop_df.groupby(
            self.group_keys
        )

        # You can show that this proportion (calculated from the average of the fractions between
        # 0 and 100 %) is mathematically different from the sum of the elements divided by the sum of the
        # total.
        # To keep the output consistent, we simply print the last one.
        # But we still use the fraction to calculate the standard error
        self.proportion_sel_mean_agg = 100 * self.records_sum.div(
            self.var_weights_sel_sum_agg, axis="index"
        )
        self.proportion_pop_mean_agg = 100 * self.records_sum.div(
            self.var_weights_pop_sum_agg, axis="index"
        )

    def calculate_standard_errors(self):
        """Calculate standard errors"""
        logger.debug("Calculating the standard errors")

        if self.variance_df_selection is None:
            # for the first round (on the smallest strata, calculate the standard deviation based
            # on the microdata sum_i (w_i * (x_i - x_mean)**2)
            # where w_i are the normalized weight for which by definition: sum_i w_i = 1
            try:
                mean_proportion = self.proportion_pop_grp.transform("sum")
            except AttributeError as err:
                logger.warning(err)
                return

            proportion_minus_mean = self.proportion_pop_df - mean_proportion
            proportion_squared = np.square(proportion_minus_mean)
            proportion_squared_sel = proportion_squared.reindex(
                self.records_df_selection.index
            )
            records_var = proportion_squared_sel.mul(
                self.weights_pop_normalized_df, axis="index"
            )
        elif self.weights_sel_normalized_df is not None:
            # for the compound breakdowns, us the variances from the first round and multiply
            # with w_i**2
            number_of_nans = self.weights_sel_normalized_df.isna().sum()
            if number_of_nans > 0:
                logger.info(f"Weights contain {number_of_nans} nans. Filling with 0")
                self.weights_sel_normalized_df = self.weights_sel_normalized_df.fillna(0)

            weights_sel_normalized_df_squared = np.square(
                self.weights_sel_normalized_df
            )
            records_square = self.variance_df_selection.astype(float)
            try:
                records_var = records_square.mul(
                    weights_sel_normalized_df_squared, axis="index"
                )
            except TypeError as err:
                logger.warning(err)
                return
        else:
            logger.info("We have variances but no weights. Use weight factor 1")
            records_var = self.variance_df_selection.astype(float)

        records_var_grp = records_var.groupby(self.group_keys)
        self.records_var_df = records_var_grp.transform("sum")
        self.records_var_agg = records_var_grp.sum()
        self.records_std_df = self.records_var_df.pow(0.5)
        self.records_std_agg = self.records_var_agg.pow(0.5)

        if self.variance_df_selection is None:
            # for the first round when we calculated the standard dev with the sum (x_i - xm)**2
            # you have to divide  by sqrt(n)  and multiply with the fpc
            self.n_sample = self.records_sel_grp.count()
            self.number_samples_sqrt = np.sqrt(self.n_sample)

            ratio = self.n_sample.div(self.weights_sel_sum_agg, axis="index")
            ratio[ratio > 1] = 1
            fpc = np.sqrt(1 - ratio)
            try:
                self.standard_error = self.records_std_agg.div(
                    self.number_samples_sqrt, axis="index"
                )
            except ZeroDivisionError as err:
                logger.warning(f"{err}")
                return
            self.standard_error = self.standard_error.mul(fpc, axis="index")
        else:
            # We got the standard error from the compound standard deviations.
            # No need to divide by sqrt(n), as we used the w_i**2 terms already
            self.standard_error = self.records_std_agg
