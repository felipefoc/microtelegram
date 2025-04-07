BASE_URL = "http://host.docker.internal:8100"
BASE_EXPENSE = "/expense"

ADD_EXPENSE_ENDPOINT = f"{BASE_URL}/{BASE_EXPENSE}/add"
DELETE_EXPENSE_ENDPOINT = f"{BASE_URL}/{BASE_EXPENSE}/delete/{id}"
BALANCE_ENDPOINT = f"{BASE_URL}/list"
BALANCE_RAW_ENDPOINT = f"{BASE_URL}/list_raw"
FREE_SQL_BUILDER = f"{BASE_URL}/freedbconsulting"
CHECK_INPUT_PROMPT = f"{BASE_URL}/checkinput/"