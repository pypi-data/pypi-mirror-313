import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import click

from hcs_ext_hst.base.helper import print_profile
from hcs_ext_hst.base.outpost import Outpost
from hcs_ext_hst.probe_test import ProbeTest

# configuration
MAX_THREADS = 20
MAX_CONCURRENT_NUM = 20
INTERVAL = 3
CASE_NAME = "cloudscale/test"
CASE_TYPE = "TEST_HZN_LAUNCH"

start_time = 0
end_time = 0


@click.group(invoke_without_command=True)
@click.option("--region", type=str, required=True, help="Specify target regions to test.")
@click.option("--num", type=int, required=True, help="Specify number of probes.")
def cloudscale(region: str, num: int):
    """Test cloud agent performance"""
    print_profile()
    # reduce_log()

    # prepare outpost
    outpost = Outpost(region)
    outpost.register()
    print("outpost id: ", outpost.id())

    try:
        futures = []
        with ThreadPoolExecutor(MAX_THREADS) as executor:
            for x in range(num):
                futures.append(executor.submit(run_probes, outpost.id(), x))
                if x > 0 and x % MAX_CONCURRENT_NUM == 0:
                    time.sleep(INTERVAL)

        global start_time
        global end_time
        fail = 0
        success = 0
        last_report_time = start_time
        max_cost = datetime.timedelta(microseconds=0)
        for future in as_completed(futures):
            result, cost, last_report = future.result()
            if result:
                success += 1
                if cost > max_cost:
                    max_cost = cost

                report_time = get_report_time(last_report.createdAt)
                if report_time > last_report_time:
                    last_report_time = report_time
            else:
                fail += 1

        requests_duration = end_time - start_time
        success_duration = last_report_time - start_time

        print(
            "\nProbe requests:",
            num,
            ", Duration:",
            requests_duration,
            ", Requests/Min:",
            num / (requests_duration.total_seconds() / 60),
        )
        print("Success:", success, ", Fail:", fail, ", Duration:", success_duration)
        print("Total duration: ", datetime.datetime.now() - start_time)
        print("\nSuccess probes/Min:", success / (success_duration.total_seconds() / 60), ", Test type:", CASE_TYPE)

    finally:
        outpost.delete()


def run_probes(outpost_id, i):
    global start_time
    global end_time

    if start_time == 0:
        start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()

    case = CASE_NAME + str(i)
    print("run case: ", case)

    result = True
    cost = datetime.timedelta(microseconds=0)
    last_report = None
    case = ProbeTest(case)
    try:
        cost, last_report = case.run(outpost_id, True)
        print("done case: ", i)
    except Exception as e:
        print("Test %s failed: %s", case.id, e)
        result = False
        print("fail case: ", i)

    return result, cost, last_report


def get_report_time(utcTime: str):
    report_time = datetime.datetime.fromisoformat(utcTime).replace(tzinfo=None)
    now_timestamp = time.time()
    offset = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
    report_time = report_time + offset
    return report_time
