from __future__ import annotations

import datetime
import uuid

from type_aliases import ConnDB


def test_read(conn_db_readonly: ConnDB) -> None:
    conn, _ = conn_db_readonly
    prepared_statement = conn.prepare("MATCH (a:person) WHERE a.isStudent = $1 AND a.isWorker = $k RETURN COUNT(*)")
    assert prepared_statement.is_success()
    assert prepared_statement.get_error_message() == ""

    result = conn.execute(prepared_statement, {"1": False, "k": False})
    assert result.has_next()
    assert result.get_next() == [1]
    assert not result.has_next()

    result = conn.execute(prepared_statement, {"1": True, "k": False})
    assert result.has_next()
    assert result.get_next() == [3]
    assert not result.has_next()

    result = conn.execute(prepared_statement, {"1": False, "k": True})
    assert result.has_next()
    assert result.get_next() == [4]
    assert not result.has_next()

    result = conn.execute(prepared_statement, {"1": True, "k": True})
    assert result.has_next()
    assert result.get_next() == [0]
    assert not result.has_next()


def test_null_value(conn_db_readonly: ConnDB) -> None:
    conn, _ = conn_db_readonly
    prepared_statement = conn.prepare("RETURN [4, $1, 2, $3, 4]")
    assert prepared_statement.is_success()
    assert prepared_statement.get_error_message() == ""

    result = conn.execute(prepared_statement, {"1": None, "3": 5})
    assert result.has_next()
    assert result.get_next() == [[4, None, 2, 5, 4]]
    assert not result.has_next()


def test_write(conn_db_readwrite: ConnDB) -> None:
    conn, _ = conn_db_readwrite
    orgs = [
        {
            "ID": 1001,
            "name": "org1",
            "orgCode": 1,
            "mark": 1.0,
            "score": 1,
            "history": "history1",
            "licenseValidInterval": datetime.timedelta(days=1),
            "rating": 1.0,
        },
        {
            "ID": 1002,
            "name": "org2",
            "orgCode": 2,
            "mark": 2.0,
            "score": 2,
            "history": "history2",
            "licenseValidInterval": datetime.timedelta(days=2),
            "rating": 2.0,
        },
        {
            "ID": 1003,
            "name": "org3",
            "orgCode": 3,
            "mark": 3.0,
            "score": 3,
            "history": "history3",
            "licenseValidInterval": datetime.timedelta(days=3),
            "rating": 3.0,
        },
    ]

    prepared_statement = conn.prepare(
        "CREATE (n:organisation {ID: $ID, name: $name, orgCode: $orgCode, mark: $mark, score: $score, history: $history, licenseValidInterval: $licenseValidInterval, rating: $rating})"
    )
    assert prepared_statement.is_success()
    for org in orgs:
        org_dict = {str(k): v for k, v in org.items()}
        conn.execute(prepared_statement, org_dict)

    all_orgs_res = conn.execute("MATCH (n:organisation) RETURN n")
    while all_orgs_res.has_next():
        n = all_orgs_res.get_next()[0]
        if n["ID"] not in [o["ID"] for o in orgs]:
            continue
        for expected_org in orgs:
            if n["ID"] == expected_org["ID"]:
                assert n["ID"] == expected_org["ID"]
                assert n["name"] == expected_org["name"]
                assert n["orgCode"] == expected_org["orgCode"]
                assert n["mark"] == expected_org["mark"]
                assert n["score"] == expected_org["score"]
                assert n["history"] == expected_org["history"]
                assert n["licenseValidInterval"] == expected_org["licenseValidInterval"]
                assert n["rating"] == expected_org["rating"]
                break

    conn.execute("CREATE NODE TABLE uuid_table (id UUID, PRIMARY KEY(id));")
    conn.execute("CREATE (:uuid_table {id: $1});", {"1": uuid.uuid5(uuid.NAMESPACE_DNS, "kuzu")})
    result = conn.execute("MATCH (n:uuid_table) RETURN n.id;")
    assert result.get_next() == [uuid.uuid5(uuid.NAMESPACE_DNS, "kuzu")]


def test_error(conn_db_readonly: ConnDB) -> None:
    prepared_statement = conn_db_readonly[0].prepare("MATCH (d:dog) WHERE d.isServiceDog = $1 RETURN COUNT(*)")
    assert not prepared_statement.is_success()
    assert prepared_statement.get_error_message() == "Binder exception: Table dog does not exist."

    prepared_statement = conn_db_readonly[0].prepare("SELECT * FROM person")
    assert not prepared_statement.is_success()
    assert prepared_statement.get_error_message().startswith("Parser exception: extraneous input 'SELECT'")
