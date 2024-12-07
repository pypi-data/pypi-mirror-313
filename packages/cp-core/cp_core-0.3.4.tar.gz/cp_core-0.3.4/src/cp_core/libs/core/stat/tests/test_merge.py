from cp_core.libs.core.stat.merge import (
    generate_df_from_files,
    generate_row_from_data,
)


def test_merge(get_data):
    data = get_data
    values = {"judge_metric": -0.85, "type_zhiliu": False}
    res = generate_row_from_data(data, values, True)
    for val in res:
        assert len(val) == 2, val
    print(res)


def test_dataframe(FILE_PATH):
    values = {"judge_metric": -0.85, "type_zhiliu": False}

    res = generate_df_from_files((FILE_PATH,), values=values, interval_jihua=True)
    print(res)
