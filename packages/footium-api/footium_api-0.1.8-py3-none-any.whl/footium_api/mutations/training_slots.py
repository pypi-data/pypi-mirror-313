import json
from datetime import datetime, timedelta

from footium_api import GqlConnection
from footium_api.queries import get_server_timestamp


def prepare_finish_training_to_sign(
        gql: GqlConnection, 
        club_id: int,
        player_id: str,
        slot_id: int
):
    current_time = get_server_timestamp(gql)
    current_time_local = datetime.utcnow()
    current_time = current_time / 1000.0
    current_time = datetime.utcfromtimestamp(current_time)
    timeout = 120000
    expiration_time = current_time + timedelta(milliseconds=timeout)
    expiration_iso_string = expiration_time.isoformat(timespec='milliseconds') + 'Z'
    data = {
            "clubId": club_id,
            "playerId": player_id,
            "slotId": slot_id,
        }
    message_to_sign = {
        "type": "FINISH_TRAINING_SESSION",
        "data": json.dumps(data, separators=(',', ':'), ensure_ascii=False),
        "expirationTime": expiration_iso_string,
    }
    message_to_send = {
        "type": "FINISH_TRAINING_SESSION",
        "data": data,
        "expirationTime": expiration_iso_string,
    }
    message_to_send = json.dumps(message_to_send, separators=(',', ':'), ensure_ascii=False)
    return message_to_sign, message_to_send

def prepare_assign_player_to_sign(
        gql: GqlConnection, 
        club_id: int,
        player_id: str,
        slot_id: int,
        position: str
):
    current_time = get_server_timestamp(gql)
    current_time_local = datetime.utcnow()
    current_time = current_time / 1000.0
    current_time = datetime.utcfromtimestamp(current_time)
    timeout = 120000
    expiration_time = current_time + timedelta(milliseconds=timeout)
    expiration_iso_string = expiration_time.isoformat(timespec='milliseconds') + 'Z'
    data = {
            "clubId": club_id,
            "playerId": player_id,
            "slotId": slot_id,
            "position": position,
        }
    message_to_sign = {
        "type": "ASSIGN_PLAYER_TO_TRAINING_SLOT",
        "data": json.dumps(data, separators=(',', ':'), ensure_ascii=False),
        "expirationTime": expiration_iso_string,
    }
    message_to_send = {
        "type": "ASSIGN_PLAYER_TO_TRAINING_SLOT",
        "data": data,
        "expirationTime": expiration_iso_string,
    }
    message_to_send = json.dumps(message_to_send, separators=(',', ':'), ensure_ascii=False)
    return message_to_sign, message_to_send

def submit_signed_message(gql: GqlConnection, message, signed_message, address):
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