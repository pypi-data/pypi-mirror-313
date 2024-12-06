from typing import List
import pandas as pd
from footium_api import GqlConnection


def get_players_in_clubs(gql: GqlConnection, club_ids: List[int])->pd.DataFrame:
    filter = {
        "clubId": {"in": club_ids},
    }
    return get_players(gql, filter)


def get_players(gql: GqlConnection, filter: dict)->pd.DataFrame:
    query = """
query GetPlayers($filter: PlayerWhereInput!, $take: Int, $skip: Int) {
  players(where: $filter, take: $take, skip: $skip) {
    id
    fullName
    creationRating
    potential
    rarity
    clubId
    ownerId
    originClubId
    generationId
    isAcademy
    isReserve
    isInitial
    isTraining
    isRetired
    seed
    firstName
    lastName
    firstSeasonId
    assetId
    nationality
    heightMeters
    mintPrice
    isPartOfAcademyMerkleTree
    clubName: club{name}
    clubOwnerId: club{ownerId}
    playerAttributes: timesteppedPlayerAttributes {
      age
      leadership
      condition
      stamina
      gamesSuspended
      accumulatedYellows
      isLatest
      timestamp
      footedness
      weakFootAbility
      unlockedPotential
      usedPotential
      accumulatedMinutes
    }
    positionalRating {
      position
      relativeCompetence
      rating
    }
  }
}
"""

# note: removed playerStatsRecord for now
# playerStatsRecord{
#     appearances
#     goals
#     penaltiesScored
#     freeKicksScored
#     shotsOnTarget
#     shotsOffTarget
#     assists
#     saves
#     fouls
#     offsides
#     yellowCards
#     redCards
#     crosses
#     attemptedPasses
#     completedPasses
#     interceptedPasses
#     groundPasses
#     offsidePasses
#     shotsBlocked
#     totalShots
#     shotsFromInsideTheBox
#     normalShots
#     backHeelShots
#     divingHeaderShots
#     halfVolleyShots
#     volleyShots
#     lobShots
#     overheadKickShots
#     timeInPossessionMilliseconds
#     blocks
#     clearances
#     interceptions
#     failedInterceptions
#     fiftyFiftiesWon
#     fiftyFiftiesLost
#     duelsWon
#     duelsLost
#     attemptedDribbles
#     completedDribbles
#     carries
#     tacklesExecuted
#     tacklesReceived
#     playerTimeInfo
#     goalsConceded
#     isGlobal
#     playerId
#     shotAccuracy
#     passAccuracy
#     dribbleSuccessRate
# }

    variables = {
        "filter": filter,
    }
    response = gql.send_paging_query(query, variables)
    players = response
    players = pd.DataFrame(players).set_index("id")

    # unwrap clubName {'name': 'Martot Park'}
    players["clubName"] = players["clubName"].apply(
        lambda x: x["name"] if x is not None else None
    )
    players["clubOwnerId"] = players["clubOwnerId"].apply(
        lambda x: x["ownerId"] if x is not None else None
    )

    # unwrap playerAttributes
    # attributes_list = [attr[0] for attr in players["playerAttributes"] if attr]
    attributes_list = players["playerAttributes"]
    combined_data_with_ids = [
        {**attr, "id": player_id}
        for attr, player_id in zip(attributes_list, players.index)
    ]
    attributes_df = pd.DataFrame(combined_data_with_ids)
    attributes_df.set_index("id", inplace=True)
    # print(attributes_df.columns)
    existing_columns = set(players.columns)
    conflicting_columns = {
        col for col in attributes_df.columns if col in existing_columns
    }
    for col in conflicting_columns:
        attributes_df.rename(columns={col: "playerAttributes_" + col}, inplace=True)
    # print(attributes_df.columns)
    players = players.drop("playerAttributes", axis=1)
    players = pd.concat([players, attributes_df], axis=1)
    # print(players.columns)

    # Unwrap positionalRating
    positional_rating_list = [pos for pos in players["positionalRating"] if pos]
    positional_rating_dict_list = []
    for row in positional_rating_list:
        ratings = {f"{r['position']}": r["rating"] for r in row}
        # relativeCompetence = {f"{r['position']}rc": r["relativeCompetence"] for r in row}
        # combined_dict = {**ratings, **relativeCompetence}  # Combine both dictionaries
        # positional_rating_dict_list.append(combined_dict)
        positional_rating_dict_list.append(ratings)

    # Combine dictionaries with IDs before creating DataFrame
    combined_data_with_ids = [
        {**pos_dict, "id": player_id}
        for pos_dict, player_id in zip(positional_rating_dict_list, players.index)
    ]
    positional_rating_df = pd.DataFrame(combined_data_with_ids)
    positional_rating_df.set_index("id", inplace=True)

    # Handle conflicting column names
    existing_columns = set(players.columns)
    conflicting_columns = {
        col for col in positional_rating_df.columns if col in existing_columns
    }
    for col in conflicting_columns:
        positional_rating_df.rename(
            columns={col: "positionalRating_" + col}, inplace=True
        )
    # Drop original positionalRating column and concatenate
    players = players.drop("positionalRating", axis=1)
    players = pd.concat([players, positional_rating_df], axis=1)

    # fix types
    players["assetId"] = pd.to_numeric(players["assetId"], errors="coerce").astype(
        "Int64"
    )
    players["ownerId"] = pd.to_numeric(players["ownerId"], errors="coerce").astype(
        "Int64"
    )
    all_positions = [
        "RB",
        "LB",
        "CB",
        "RWB",
        "LWB",
        "DM",
        "RM",
        "LM",
        "CM",
        "RW",
        "LW",
        "AM",
        "RF",
        "LF",
        "CF",
        "GK",
    ]
    for column in all_positions:
        players[column] = pd.to_numeric(players[column], errors="coerce")

    # create two new columns, topRating and topPosition
    players['topRating'] = players[all_positions].max(axis=1)
    players['topPosition'] = players[all_positions].idxmax(axis=1)

    return players
