import pandas as pd
from footium_api import GqlConnection


def get_formations(gql: GqlConnection) -> pd.DataFrame:
    query = """
query Formations {
    formations {
        id
        name
        slots {
            id
            formationId
            slotIndex
            pitchPosition
        }
    }
}
    """
    response = gql.send_query(query)
    formations = response.formations
    return formations


def convert_formations_to_pd(formations_input) -> pd.DataFrame:
    outfield_positions = [
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
        ]
    all_positions = outfield_positions + ["GK"]

    formations = pd.DataFrame(columns=["Formation"] + all_positions)
    for formation in formations_input:
        row = {pos: 0 for pos in all_positions}
        row["Formation"] = formation.name
        for position in formation.slots:
            row[position["position"]] += 1
        assert (
            sum(value for key, value in row.items() if key in all_positions) == 11
        ), "Total positions do not sum up to 11"
        new_row_df = pd.DataFrame([row])
        formations = pd.concat([formations, new_row_df], ignore_index=True)
    formations.set_index("Formation", inplace=True)
    return formations


def get_formations_as_pd(gql: GqlConnection):
    formations_input = get_formations(gql)
    formations = convert_formations_to_pd(formations_input)
    return formations
