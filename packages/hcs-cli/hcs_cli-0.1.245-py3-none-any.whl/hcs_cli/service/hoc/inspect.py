from .es import client as es


def inspect(org: str, template_id: str, vm_id: str):

    index = "prod110_na_r_westus2_a-cp102-*"
    parts = vm_id.split("-")
    query = {
        "bool": {
            "must": [],
            "filter": [
                {
                    "bool": {
                        "filter": [
                            {"multi_match": {"type": "phrase", "query": "OTP", "lenient": True}},
                            {
                                "bool": {
                                    "filter": [
                                        {"multi_match": {"type": "phrase", "query": parts[0], "lenient": True}},
                                        {
                                            "bool": {
                                                "filter": [
                                                    {
                                                        "multi_match": {
                                                            "type": "phrase",
                                                            "query": parts[1],
                                                            "lenient": True,
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "type": "phrase",
                                                            "query": "valid",
                                                            "lenient": True,
                                                        }
                                                    },
                                                ]
                                            }
                                        },
                                    ]
                                }
                            },
                        ]
                    }
                },
                {
                    "range": {
                        "@timestamp": {
                            "gte": "2024-10-30T01:00:00.000Z",
                            "lte": "2024-10-30T23:59:00.000Z",
                            "format": "strict_date_optional_time",
                        }
                    }
                },
            ],
            "should": [],
            "must_not": [],
        }
    }
    sort = [{"@timestamp": {"order": "desc", "unmapped_type": "boolean"}}]
    ret = es("us").search(index=index, query=query, sort=sort)
    # print(ret)
    print()
    print()
    if ret["hits"]["hits"]:
        print("Agent reached the cloud. (Found success redeem OTP)")
    else:
        print("Agent can not reach the cloud. (Redeem OTP not found)")
