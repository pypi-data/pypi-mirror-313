import json
from datetime import datetime, timedelta

from footium_api import GqlConnection
from footium_api.queries import get_server_timestamp

# import execjs

# def stringify(data):
#     js_runtime = execjs.get()
#     js_code = f'JSON.stringify({data})'
#     js_code = js_code.replace('True', 'true').replace('False', 'false')
#     return js_runtime.eval(js_code)


def prepare_lineup_to_sign(gql: GqlConnection, lineup):
    current_time = get_server_timestamp(gql)
    current_time_local = datetime.utcnow()
    current_time = current_time / 1000.0
    current_time = datetime.utcfromtimestamp(current_time)
    timeout = 120000
    expiration_time = current_time + timedelta(milliseconds=timeout)
    # expiration_iso_string = expiration_time.isoformat() + 'Z'
    expiration_iso_string = expiration_time.isoformat(timespec='milliseconds') + 'Z'
    data = {
            "lineup": {
                "id": lineup.id,
                "clubId": lineup.clubId,
                "isSelected": lineup.isSelected,
                "tacticsId": lineup.tacticsId,
            },
            "tactics": {
                "id": lineup.tactics.id,
                "mentality": lineup.tactics.mentality,
                "formationId": lineup.tactics.formationId,
            },
            "playerLineups": lineup.playerLineups.to_list(),
        }
    message_to_sign = {
        "type": "LINEUP_SET",
        "data": json.dumps(data, separators=(',', ':'), ensure_ascii=False),
        # "data": stringify(data),
        "expirationTime": expiration_iso_string,
    }
    message_to_send = {
        "type": "LINEUP_SET",
        "data": data,
        "expirationTime": expiration_iso_string,
    }
    message_to_send = json.dumps(message_to_send, separators=(',', ':'), ensure_ascii=False)
    # message_to_send = stringify(message_to_send)
    # return json.dumps(message)
    return message_to_sign, message_to_send

def submit_lineup(gql: GqlConnection, message, signed_message, address):
    query = """
mutation SubmitAction($action: String!, $signature: String!, $address: String!) {
    submitAction(action: $action, signature: $signature, address: $address)
    {
        code
        error
        message
        __typename
    }
}
"""
    variables = {
        "signature": signed_message,
        "address": address,
        "action": message,
    }
    response = gql.send_mutation(query, variables, "SubmitAction")
    return response
