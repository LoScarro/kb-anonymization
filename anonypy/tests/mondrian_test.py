import anonypy
from anonypy import util
import pandas as pd

data = [
    [6, "1", "test1", "x", 20],
    [6, "1", "test1", "x", 30],
    [8, "2", "test2", "x", 50],
    [8, "2", "test3", "w", 45],
    [8, "1", "test2", "y", 35],
    [4, "2", "test3", "y", 20],
    [4, "1", "test3", "y", 20],
    [2, "1", "test3", "z", 22],
    [2, "2", "test3", "y", 32],
]

columns = ["col1", "col2", "col3", "col4", "col5"]
categorical = set(("col2", "col3", "col4"))


def test_k_anonymity():
    df = pd.DataFrame(data=data, columns=columns)
    print(df)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"
    m = anonypy.Mondrian(df, feature_columns, sensitive_column)
    partitions = m.partition(k=2)
    print(f"partitions: {partitions}")

    indexes = util.build_indexes(df)
    column_x, column_y = feature_columns[:2]
    rects = util.get_partition_rects(
        df, partitions, column_x, column_y, indexes, offsets=[0.1, 0.1]
    )

    print(f"rect: {rects[:10]}")


def test_l_diversity():
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    m = anonypy.Mondrian(df, feature_columns, sensitive_column)
    partitions = m.partition(k=2, l=2)

    print(f"partitions: {partitions}")


def test_t_closeness():
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]
    sensitive_column = "col4"

    m = anonypy.Mondrian(df, feature_columns, sensitive_column)
    partitions = m.partition(k=2, p=0.2)

    print(f"partitions: {partitions}")


def test_get_spans():
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    feature_columns = ["col1", "col2", "col3"]

    m = anonypy.Mondrian(df, feature_columns)
    spans = m.get_spans(df.index)

    assert {"col1": 6, "col2": 2, "col3": 3} == spans
