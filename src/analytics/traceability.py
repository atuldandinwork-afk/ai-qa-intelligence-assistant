from src.analytics.execution_lookup import get_execution_by_test_case
from src.analytics.defects import get_defect_by_id

def trace_test_case(test_case_id: str):
    exec_result = get_execution_by_test_case(test_case_id)

    if exec_result is None:
        return None

    linked_defects = exec_result.get("linked_defects", [])

    defects = []
    for defect_id in linked_defects:
        d = get_defect_by_id(defect_id)
        if d:
            defects.append(d)

    return {
        "test_case_id": test_case_id,
        "execution": exec_result,
        "defects": defects,
    }
