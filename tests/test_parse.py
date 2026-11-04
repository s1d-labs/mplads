from parse import body, record_id, rows


def test_rows_string():
    assert rows({"a": '[{"Sno": 1, "WORK_RECOMMENDATION_DTL_ID": 7}, {"total": 2}]'}) == [{"Sno": 1, "WORK_RECOMMENDATION_DTL_ID": 7}]


def test_rows_empty():
    assert rows({}) == [] and rows({"a": []}) == []


def test_ids():
    assert body(11, 2, 5, "Works Sanctioned")["combo"] == "11,0,0,2,5"
    assert record_id("ls17", 11, "Works Sanctioned", {"Sno": 3, "WORK_RECOMMENDATION_DTL_ID": 9}) == "ls17-11-works-9-3"
