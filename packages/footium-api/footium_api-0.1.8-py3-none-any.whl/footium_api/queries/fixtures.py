from typing import List, Optional
import pandas as pd

from footium_api.gql_connection import GqlConnection


def get_next_fixtures(
    gql: GqlConnection, club_ids: List[int], max_games: Optional[int] = None
):
    query = """
query NextFixtures($clubIds: [Int!]!, $take: Int, $skip: Int) {
    nextFixtures: fixtures(
    where: {
        AND: [
        { clubFixtures: { some: { clubId: { in: $clubIds } } } },
        { state: { in: ["BEFORE_KICKOFF", "LIVE"] } }
        ]
    },
    take: $take, skip: $skip,
    orderBy: { realWorldTimestamp: asc }
    ) {
    realWorldTimestamp
    clubFixtures {
        isHome
        club {
        id
        name
        }
    }
    tournament {
        name
        id
        clubTournaments {
        clubId
        position
        }
    }
    }
}
    """

    variables = {
        "clubIds": club_ids,
    }

    # response = gql.execute(gql.gql(query), variable_values=variables)
    # response = gql.send_query(query, variables)
    # fixtures = response['nextFixtures']
    max_games = max_games or len(club_ids) * 2
    fixtures = gql.send_paging_query(query, variables, take=max_games)

    # Process the response into a DataFrame
    fixtures_data = []
    for fixture in fixtures:
        for clubFixture in fixture["clubFixtures"]:
            if clubFixture["club"]["id"] in club_ids:
                fixtures_data.append(
                    {
                        # "realWorldTimestamp": fixture['realWorldTimestamp'],
                        "realWorldTimestamp": pd.to_datetime(
                            fixture["realWorldTimestamp"], unit="ms", utc=True
                        ),
                        "clubId": clubFixture["club"]["id"],
                        "clubName": clubFixture["club"]["name"],
                        "isHome": clubFixture["isHome"],
                        "tournamentName": fixture["tournament"]["name"],
                        "tournamentId": fixture["tournament"]["id"],
                        "position": next(
                            (
                                ct["position"]
                                for ct in fixture["tournament"]["clubTournaments"]
                                if ct["clubId"] == clubFixture["club"]["id"]
                            ),
                            None,
                        ),
                    }
                )

    fixtures_df = pd.DataFrame(fixtures_data)
    return fixtures_df
