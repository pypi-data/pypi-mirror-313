from typing import Dict, List
from footium_api import GqlConnection

def get_training_slots(gql: GqlConnection, club_ids: List[int])->List[Dict]:
    query = """
query TrainingLink_Query($clubIds: [Int!]) {
  trainingSlots(where: {clubId: {in: $clubIds}}, orderBy: {id: asc}) {
    id
    clubId
    baseDuration
    growthFactor
    conditionCost
    trainablePositions
    playerId
    expiryTime
    position
    isComplete
    __typename
  }
}
"""

    variables = {
        "clubIds": club_ids,
    }
    response = gql.send_query(query, variables)
    training_slots = response.trainingSlots
    return training_slots