from unittest import TestCase

from freezegun import freeze_time
from pandas import DataFrame
from pandas.testing import assert_frame_equal
from typeguard import TypeCheckError

from tommytomato_utils.hashing_client.exceptions import (
    DuplicateHashValuesError, MissingHashColumnsError
)
from tommytomato_utils.hashing_client.hashing_client import HashingClient


class TestHashGenerator(TestCase):

    def test_hashing_string(self):
        input_string = 'hello'
        expected_output = '9342d47a-1bab-5709-9869-c840b2eac501'
        output = HashingClient.get_hash_uuid_from_string(input_string)
        self.assertEqual(output, expected_output)

    def test_dataframe_hash_with_just_columns_needed(self):
        df = DataFrame({
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4'],
        })
        hash_columns = ['col1', 'col2']

        expected_output = df.copy()
        expected_output['box_id'] = [
            '1f3ac418-9828-51c9-9404-f88123f7fa65', 'f9171cd3-e34d-50c2-993d-803a16ace55f'
        ]

        output = HashingClient.add_dataframe_column_hash_given_column_names(
            df, hash_columns, 'box_id'
        )
        assert_frame_equal(output, expected_output)

    def test_dataframe_hash_with_additional_column(self):
        """Same as previous test, but adding a new column that has no impact on output."""
        df = DataFrame(
            {
                'col1': ['value1', 'value2'],
                'col2': ['value3', 'value4'],
                'col3': ['value5', 'value6'],
            }
        )
        hash_columns = ['col1', 'col2']

        expected_output = df.copy()
        expected_output['box_id'] = [
            '1f3ac418-9828-51c9-9404-f88123f7fa65', 'f9171cd3-e34d-50c2-993d-803a16ace55f'
        ]

        output = HashingClient.add_dataframe_column_hash_given_column_names(
            df, hash_columns, 'box_id'
        )
        assert_frame_equal(output, expected_output)

    def test_missing_columns_error(self):
        df = DataFrame({
            'col1': ['value1', 'value2'],
        })
        hash_columns = ['col1', 'col2']  # Col 2 not in dataframe!

        with self.assertRaises(MissingHashColumnsError):
            HashingClient.add_dataframe_column_hash_given_column_names(df, hash_columns, 'box_id')

    def test_wrong_input_type(self):
        df = None
        with self.assertRaises(TypeCheckError):
            HashingClient.add_dataframe_column_hash_given_column_names(df, ['col1'], 'box_id')

    def test_no_duplicates_allowed_raises_error(self):
        df = DataFrame({
            'col1': ['value1', 'value1'],
            'col2': ['value3', 'value3'],
        })
        hash_columns = ['col1', 'col2']

        with self.assertRaises(DuplicateHashValuesError):
            HashingClient.add_dataframe_column_hash_given_column_names(
                df, hash_columns, 'box_id', allow_duplicates=False
            )

    def test_no_duplicates_allowed_passes(self):
        df = DataFrame({
            'col1': ['value1', 'value2'],
            'col2': ['value3', 'value4'],
        })
        hash_columns = ['col1', 'col2']

        expected_output = df.copy()
        expected_output['box_id'] = [
            '1f3ac418-9828-51c9-9404-f88123f7fa65', 'f9171cd3-e34d-50c2-993d-803a16ace55f'
        ]

        output = HashingClient.add_dataframe_column_hash_given_column_names(
            df, hash_columns, 'box_id', allow_duplicates=False
        )
        assert_frame_equal(output, expected_output)


class TestHashGeneratorTimeDependent(TestCase):
    """You can create time dependent hashes."""

    @freeze_time("2010-07-11 20:26:33")  # Iniesta scores
    def test_hashing_with_utc_is_consistent_in_every_row(self):
        """
        If each row is hashed at different times, it could be that each row ends up with a
        different hash, even if input is the same.
        """
        # arrange
        input_df = DataFrame({'data': [1, 1, 1, 1]})  # same data 4 times
        expected_output = input_df.copy()
        expected_output['utc_hash'] = 'e6a2ca49-5733-5f4f-9866-f4aadc2ec1f5'

        # act
        output = HashingClient.add_dataframe_column_hash_given_column_names(
            input_df,
            ['data'],
            'utc_hash',
            allow_duplicates=True,
            append_current_time=True,
        )

        # assert
        assert_frame_equal(output, expected_output)

    def test_hash_changes_if_timestamp_changes(self):
        """Make sure that hash changes, given same input, and different times."""
        # arrange
        input_df = DataFrame({'data': [1, 1, 1, 1]})  # same data 4 times
        expected_output_1 = input_df.copy()
        expected_output_2 = input_df.copy()
        expected_output_1['utc_hash'] = 'e6a2ca49-5733-5f4f-9866-f4aadc2ec1f5'  # hash Iniesta
        expected_output_2['utc_hash'] = '33cf0646-5176-501a-bbb9-43c4ea559081'  # hash Van Persie

        # act, same DF, different times
        with freeze_time("2010-07-11 20:26:33"):  # Time when Iniesta scored in 2010
            output_1 = HashingClient.add_dataframe_column_hash_given_column_names(
                input_df.copy(),
                ['data'],
                'utc_hash',
                allow_duplicates=True,
                append_current_time=True,
            )
        with freeze_time("2014-06-13 19:42:00"):  # Time when Van Persie scored in 2014
            output_2 = HashingClient.add_dataframe_column_hash_given_column_names(
                input_df.copy(),
                ['data'],
                'utc_hash',
                allow_duplicates=True,
                append_current_time=True,
            )

        # assert
        assert_frame_equal(expected_output_1, output_1)
        assert_frame_equal(expected_output_2, output_2)
