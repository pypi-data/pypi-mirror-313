from dataclasses import dataclass
from collections.abc import Callable

import polars as pl

from spells.enums import View, ColName, ColType


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    col_type: ColType
    expr: pl.Expr | None = None
    exprMap: Callable[[str], pl.Expr] | None = None
    views: list[View] | None = None
    dependencies: list[str] | None = None
    version: str | None = (
        None  # only needed for user-defined functions with python functions in expr
    )


@dataclass(frozen=True)
class ColumnDefinition:
    name: str
    col_type: ColType
    expr: pl.Expr | tuple[pl.Expr, ...]
    views: set[View]
    dependencies: tuple[str, ...]
    signature: str


default_columns = [
    ColName.COLOR,
    ColName.RARITY,
    ColName.NUM_SEEN,
    ColName.ALSA,
    ColName.NUM_TAKEN,
    ColName.ATA,
    ColName.NUM_GP,
    ColName.PCT_GP,
    ColName.GP_WR,
    ColName.NUM_OH,
    ColName.OH_WR,
    ColName.NUM_GIH,
    ColName.GIH_WR,
]

_column_specs = [
    ColumnSpec(
        name=ColName.NAME,
        col_type=ColType.GROUP_BY,
        # handled by internals, derived from both 'pick' and "name mapped" columns
    ),
    ColumnSpec(
        name=ColName.EXPANSION,
        col_type=ColType.GROUP_BY,
        views=[View.GAME, View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.EVENT_TYPE,
        col_type=ColType.GROUP_BY,
        views=[View.GAME, View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.DRAFT_ID,
        views=[View.GAME, View.DRAFT],
        col_type=ColType.FILTER_ONLY,
    ),
    ColumnSpec(
        name=ColName.DRAFT_TIME,
        col_type=ColType.FILTER_ONLY,
        views=[View.GAME, View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.DRAFT_DATE,
        col_type=ColType.GROUP_BY,
        expr=pl.col("draft_time").str.to_datetime("%Y-%m-%d %H:%M:%S").dt.date(),
        dependencies=[ColName.DRAFT_TIME],
    ),
    ColumnSpec(
        name=ColName.DRAFT_DAY_OF_WEEK,
        col_type=ColType.GROUP_BY,
        expr=pl.col("draft_time").str.to_datetime("%Y-%m-%d %H:%M:%S").dt.weekday(),
        dependencies=[ColName.DRAFT_TIME],
    ),
    ColumnSpec(
        name=ColName.DRAFT_HOUR,
        col_type=ColType.GROUP_BY,
        expr=pl.col("draft_time").str.to_datetime("%Y-%m-%d %H:%M:%S").dt.hour(),
        dependencies=[ColName.DRAFT_TIME],
    ),
    ColumnSpec(
        name=ColName.DRAFT_WEEK,
        col_type=ColType.GROUP_BY,
        expr=pl.col("draft_time").str.to_datetime("%Y-%m-%d %H:%M:%S").dt.week(),
        dependencies=[ColName.DRAFT_TIME],
    ),
    ColumnSpec(
        name=ColName.RANK,
        col_type=ColType.GROUP_BY,
        views=[View.GAME, View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.USER_N_GAMES_BUCKET,
        col_type=ColType.GROUP_BY,
        views=[View.DRAFT, View.GAME],
    ),
    ColumnSpec(
        name=ColName.USER_GAME_WIN_RATE_BUCKET,
        col_type=ColType.GROUP_BY,
        views=[View.DRAFT, View.GAME],
    ),
    ColumnSpec(
        name=ColName.PLAYER_COHORT,
        col_type=ColType.GROUP_BY,
        expr=pl.when(pl.col("user_n_games_bucket") < 100)
        .then(pl.lit("Other"))
        .otherwise(
            pl.when(pl.col("user_game_win_rate_bucket") > 0.57)
            .then(pl.lit("Top"))
            .otherwise(
                pl.when(pl.col("user_game_win_rate_bucket") < 0.49)
                .then(pl.lit("Bottom"))
                .otherwise(pl.lit("Middle"))
            )
        ),
        dependencies=[ColName.USER_N_GAMES_BUCKET, ColName.USER_GAME_WIN_RATE_BUCKET],
    ),
    ColumnSpec(
        name=ColName.EVENT_MATCH_WINS,
        col_type=ColType.GROUP_BY,
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.EVENT_MATCH_WINS_SUM,
        col_type=ColType.PICK_SUM,
        views=[View.DRAFT],
        expr=pl.col(ColName.EVENT_MATCH_WINS),
        dependencies=[ColName.EVENT_MATCH_WINS],
    ),
    ColumnSpec(
        name=ColName.EVENT_MATCH_LOSSES,
        col_type=ColType.GROUP_BY,
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.EVENT_MATCH_LOSSES_SUM,
        col_type=ColType.PICK_SUM,
        expr=pl.col(ColName.EVENT_MATCH_LOSSES),
        dependencies=[ColName.EVENT_MATCH_LOSSES],
    ),
    ColumnSpec(
        name=ColName.EVENT_MATCHES,
        col_type=ColType.GROUP_BY,
        expr=pl.col("event_match_wins") + pl.col("event_match_losses"),
        dependencies=[ColName.EVENT_MATCH_WINS, ColName.EVENT_MATCH_LOSSES],
    ),
    ColumnSpec(
        name=ColName.EVENT_MATCHES_SUM,
        col_type=ColType.PICK_SUM,
        expr=pl.col(ColName.EVENT_MATCHES),
        dependencies=[ColName.EVENT_MATCHES],
    ),
    ColumnSpec(
        name=ColName.IS_TROPHY,
        col_type=ColType.GROUP_BY,
        expr=pl.when(pl.col("event_type") == "Traditional")
        .then(pl.col("event_match_wins") == 3)
        .otherwise(pl.col("event_match_wins") == 7),
        dependencies=[ColName.EVENT_TYPE, ColName.EVENT_MATCH_WINS],
    ),
    ColumnSpec(
        name=ColName.IS_TROPHY_SUM,
        col_type=ColType.PICK_SUM,
        expr=pl.col(ColName.IS_TROPHY),
        dependencies=[ColName.IS_TROPHY],
    ),
    ColumnSpec(
        name=ColName.PACK_NUMBER,
        col_type=ColType.FILTER_ONLY,  # use pack_num
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.PACK_NUM,
        col_type=ColType.GROUP_BY,
        expr=pl.col("pack_number") + 1,
        dependencies=[ColName.PACK_NUMBER],
    ),
    ColumnSpec(
        name=ColName.PICK_NUMBER,
        col_type=ColType.FILTER_ONLY,  # use pick_num
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.PICK_NUM,
        col_type=ColType.GROUP_BY,
        expr=pl.col("pick_number") + 1,
        dependencies=[ColName.PICK_NUMBER],
    ),
    ColumnSpec(
        name=ColName.TAKEN_AT,
        col_type=ColType.PICK_SUM,
        expr=pl.col(ColName.PICK_NUM),
        dependencies=[ColName.PICK_NUM],
    ),
    ColumnSpec(
        name=ColName.NUM_TAKEN,
        col_type=ColType.PICK_SUM,
        expr=pl.when(pl.col(ColName.PICK).is_not_null())
        .then(1)
        .otherwise(0),  # a literal returns one row under select alone
        dependencies=[ColName.PICK],
    ),
    ColumnSpec(
        name=ColName.PICK,
        col_type=ColType.FILTER_ONLY,  # aggregated as "name"
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.PICK_MAINDECK_RATE,
        col_type=ColType.PICK_SUM,
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.PICK_SIDEBOARD_IN_RATE,
        col_type=ColType.PICK_SUM,
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.PACK_CARD,
        col_type=ColType.NAME_SUM,
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.LAST_SEEN,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"pack_card_{name}")
        * pl.min_horizontal("pick_num", 8),
        dependencies=[ColName.PACK_CARD, ColName.PICK_NUM],
    ),
    ColumnSpec(
        name=ColName.NUM_SEEN,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"pack_card_{name}") * (pl.col("pick_num") <= 8),
        dependencies=[ColName.PACK_CARD, ColName.PICK_NUM],
    ),
    ColumnSpec(
        name=ColName.POOL,
        col_type=ColType.NAME_SUM,
        views=[View.DRAFT],
    ),
    ColumnSpec(
        name=ColName.GAME_TIME,
        col_type=ColType.FILTER_ONLY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.GAME_DATE,
        col_type=ColType.GROUP_BY,
        expr=pl.col("game_time").str.to_datetime("%Y-%m-%d %H-%M-%S").dt.date(),
        dependencies=[ColName.GAME_TIME],
    ),
    ColumnSpec(
        name=ColName.GAME_DAY_OF_WEEK,
        col_type=ColType.GROUP_BY,
        expr=pl.col("game_time").str.to_datetime("%Y-%m-%d %H-%M-%S").dt.weekday(),
        dependencies=[ColName.GAME_TIME],
    ),
    ColumnSpec(
        name=ColName.GAME_HOUR,
        col_type=ColType.GROUP_BY,
        expr=pl.col("game_time").str.to_datetime("%Y-%m-%d %H-%M-%S").dt.hour(),
        dependencies=[ColName.GAME_TIME],
    ),
    ColumnSpec(
        name=ColName.GAME_WEEK,
        col_type=ColType.GROUP_BY,
        expr=pl.col("game_time").str.to_datetime("%Y-%m-%d %H-%M-%S").dt.week(),
        dependencies=[ColName.GAME_TIME],
    ),
    ColumnSpec(
        name=ColName.BUILD_INDEX,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.MATCH_NUMBER,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.GAME_NUMBER,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_GAMES,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.GAME_NUMBER).is_not_null(),
        dependencies=[ColName.GAME_NUMBER],
    ),
    ColumnSpec(
        name=ColName.NUM_MATCHES,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.GAME_NUMBER) == 1,
        dependencies=[ColName.GAME_NUMBER],
    ),
    ColumnSpec(
        name=ColName.NUM_EVENTS,
        col_type=ColType.GAME_SUM,
        expr=(pl.col(ColName.GAME_NUMBER) == 1) & (pl.col(ColName.MATCH_NUMBER) == 1),
        dependencies=[ColName.GAME_NUMBER, ColName.MATCH_NUMBER],
    ),
    ColumnSpec(
        name=ColName.OPP_RANK,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.MAIN_COLORS,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_COLORS,
        col_type=ColType.GROUP_BY,
        expr=pl.col(ColName.MAIN_COLORS).str.len_chars(),
        dependencies=[ColName.MAIN_COLORS],
    ),
    ColumnSpec(
        name=ColName.SPLASH_COLORS,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.HAS_SPLASH,
        col_type=ColType.GROUP_BY,
        expr=pl.col(ColName.SPLASH_COLORS).str.len_chars() > 0,
        dependencies=[ColName.SPLASH_COLORS],
    ),
    ColumnSpec(
        name=ColName.ON_PLAY,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_ON_PLAY,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.ON_PLAY),
        dependencies=[ColName.ON_PLAY],
    ),
    ColumnSpec(
        name=ColName.NUM_MULLIGANS,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_MULLIGANS_SUM,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.NUM_MULLIGANS),
        dependencies=[ColName.NUM_MULLIGANS],
    ),
    ColumnSpec(
        name=ColName.OPP_NUM_MULLIGANS,
        col_type=ColType.GAME_SUM,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.OPP_NUM_MULLIGANS_SUM,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.OPP_NUM_MULLIGANS),
        dependencies=[ColName.OPP_NUM_MULLIGANS],
    ),
    ColumnSpec(
        name=ColName.OPP_COLORS,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_TURNS,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_TURNS_SUM,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.NUM_TURNS),
        dependencies=[ColName.NUM_TURNS],
    ),
    ColumnSpec(
        name=ColName.WON,
        col_type=ColType.GROUP_BY,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.NUM_WON,
        col_type=ColType.GAME_SUM,
        expr=pl.col(ColName.WON),
        dependencies=[ColName.WON],
    ),
    ColumnSpec(
        name=ColName.OPENING_HAND,
        col_type=ColType.NAME_SUM,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.WON_OPENING_HAND,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"opening_hand_{name}") * pl.col(ColName.WON),
        dependencies=[ColName.OPENING_HAND, ColName.WON],
    ),
    ColumnSpec(
        name=ColName.DRAWN,
        col_type=ColType.NAME_SUM,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.WON_DRAWN,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"drawn_{name}") * pl.col(ColName.WON),
        dependencies=[ColName.DRAWN, ColName.WON],
    ),
    ColumnSpec(
        name=ColName.TUTORED,
        col_type=ColType.NAME_SUM,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.WON_TUTORED,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"tutored_{name}") * pl.col(ColName.WON),
        dependencies=[ColName.TUTORED, ColName.WON],
    ),
    ColumnSpec(
        name=ColName.DECK,
        col_type=ColType.NAME_SUM,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.WON_DECK,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"deck_{name}") * pl.col(ColName.WON),
        dependencies=[ColName.DECK, ColName.WON],
    ),
    ColumnSpec(
        name=ColName.SIDEBOARD,
        col_type=ColType.NAME_SUM,
        views=[View.GAME],
    ),
    ColumnSpec(
        name=ColName.WON_SIDEBOARD,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(f"sideboard_{name}") * pl.col(ColName.WON),
        dependencies=[ColName.SIDEBOARD, ColName.WON],
    ),
    ColumnSpec(
        name=ColName.NUM_GNS,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.max_horizontal(
            0,
            pl.col(f"deck_{name}")
            - pl.col(f"drawn_{name}")
            - pl.col(f"tutored_{name}")
            - pl.col(f"opening_hand_{name}"),
        ),
        dependencies=[
            ColName.DECK,
            ColName.DRAWN,
            ColName.TUTORED,
            ColName.OPENING_HAND,
        ],
    ),
    ColumnSpec(
        name=ColName.WON_NUM_GNS,
        col_type=ColType.NAME_SUM,
        exprMap=lambda name: pl.col(ColName.WON) * pl.col(f"num_gns_{name}"),
        dependencies=[ColName.NUM_GNS, ColName.WON],
    ),
    ColumnSpec(
        name=ColName.SET_CODE,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.COLOR,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.RARITY,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.COLOR_IDENTITY,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.CARD_TYPE,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.SUBTYPE,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.MANA_VALUE,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.DECK_MANA_VALUE,
        col_type=ColType.CARD_SUM,
        expr=pl.col(ColName.MANA_VALUE) * pl.col(ColName.DECK),
        dependencies=[ColName.MANA_VALUE, ColName.DECK],
    ),
    ColumnSpec(
        name=ColName.DECK_LANDS,
        col_type=ColType.CARD_SUM,
        expr=pl.when(pl.col(ColName.CARD_TYPE).str.contains("Land"))
        .then(pl.col(ColName.DECK))
        .otherwise(0),
        dependencies=[ColName.CARD_TYPE, ColName.DECK],
    ),
    ColumnSpec(
        name=ColName.DECK_SPELLS,
        col_type=ColType.CARD_SUM,
        expr=pl.col(ColName.DECK) - pl.col(ColName.DECK_SPELLS),
        dependencies=[ColName.DECK, ColName.DECK_SPELLS],
    ),
    ColumnSpec(
        name=ColName.MANA_COST,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.POWER,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.TOUGHNESS,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.IS_BONUS_SHEET,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.IS_DFC,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.ORACLE_TEXT,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.CARD_JSON,
        col_type=ColType.CARD_ATTR,
    ),
    ColumnSpec(
        name=ColName.PICKED_MATCH_WR,
        col_type=ColType.AGG,
        expr=pl.col(ColName.EVENT_MATCH_WINS_SUM) / pl.col(ColName.EVENT_MATCHES),
        dependencies=[ColName.EVENT_MATCH_WINS_SUM, ColName.EVENT_MATCHES],
    ),
    ColumnSpec(
        name=ColName.TROPHY_RATE,
        col_type=ColType.AGG,
        expr=pl.col(ColName.IS_TROPHY_SUM) / pl.col(ColName.NUM_TAKEN),
        dependencies=[ColName.IS_TROPHY_SUM, ColName.NUM_TAKEN],
    ),
    ColumnSpec(
        name=ColName.GAME_WR,
        col_type=ColType.AGG,
        expr=pl.col(ColName.NUM_WON) / pl.col(ColName.NUM_GAMES),
        dependencies=[ColName.NUM_WON, ColName.NUM_GAMES],
    ),
    ColumnSpec(
        name=ColName.ALSA,
        col_type=ColType.AGG,
        expr=pl.col(ColName.LAST_SEEN) / pl.col(ColName.NUM_SEEN),
        dependencies=[ColName.LAST_SEEN, ColName.NUM_SEEN],
    ),
    ColumnSpec(
        name=ColName.ATA,
        col_type=ColType.AGG,
        expr=pl.col(ColName.TAKEN_AT) / pl.col(ColName.NUM_TAKEN),
        dependencies=[ColName.TAKEN_AT, ColName.NUM_TAKEN],
    ),
    ColumnSpec(
        name=ColName.NUM_GP,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK),
        dependencies=[ColName.DECK],
    ),
    ColumnSpec(
        name=ColName.PCT_GP,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK) / (pl.col(ColName.DECK) + pl.col(ColName.SIDEBOARD)),
        dependencies=[ColName.DECK, ColName.SIDEBOARD],
    ),
    ColumnSpec(
        name=ColName.GP_WR,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_DECK) / pl.col(ColName.DECK),
        dependencies=[ColName.WON_DECK, ColName.DECK],
    ),
    ColumnSpec(
        name=ColName.NUM_OH,
        col_type=ColType.AGG,
        expr=pl.col(ColName.OPENING_HAND),
        dependencies=[ColName.OPENING_HAND],
    ),
    ColumnSpec(
        name=ColName.OH_WR,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_OPENING_HAND) / pl.col(ColName.OPENING_HAND),
        dependencies=[ColName.WON_OPENING_HAND, ColName.OPENING_HAND],
    ),
    ColumnSpec(
        name=ColName.NUM_GIH,
        col_type=ColType.AGG,
        expr=pl.col(ColName.OPENING_HAND) + pl.col(ColName.DRAWN),
        dependencies=[ColName.OPENING_HAND, ColName.DRAWN],
    ),
    ColumnSpec(
        name=ColName.NUM_GIH_WON,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_OPENING_HAND) + pl.col(ColName.WON_DRAWN),
        dependencies=[ColName.WON_OPENING_HAND, ColName.WON_DRAWN],
    ),
    ColumnSpec(
        name=ColName.GIH_WR,
        col_type=ColType.AGG,
        expr=pl.col(ColName.NUM_GIH_WON) / pl.col(ColName.NUM_GIH),
        dependencies=[ColName.NUM_GIH_WON, ColName.NUM_GIH],
    ),
    ColumnSpec(
        name=ColName.GNS_WR,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_NUM_GNS) / pl.col(ColName.NUM_GNS),
        dependencies=[ColName.WON_NUM_GNS, ColName.NUM_GNS],
    ),
    ColumnSpec(
        name=ColName.IWD,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GIH_WR) - pl.col(ColName.GNS_WR),
        dependencies=[ColName.GIH_WR, ColName.GNS_WR],
    ),
    ColumnSpec(
        name=ColName.NUM_IN_POOL,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK) + pl.col(ColName.SIDEBOARD),
        dependencies=[ColName.DECK, ColName.SIDEBOARD],
    ),
    ColumnSpec(
        name=ColName.IN_POOL_WR,
        col_type=ColType.AGG,
        expr=(pl.col(ColName.WON_DECK) + pl.col(ColName.WON_SIDEBOARD))
        / pl.col(ColName.NUM_IN_POOL),
        dependencies=[ColName.WON_DECK, ColName.WON_SIDEBOARD, ColName.NUM_IN_POOL],
    ),
    ColumnSpec(
        name=ColName.DECK_TOTAL,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK).sum(),
        dependencies=[ColName.DECK],
    ),
    ColumnSpec(
        name=ColName.WON_DECK_TOTAL,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_DECK).sum(),
        dependencies=[ColName.WON_DECK],
    ),
    ColumnSpec(
        name=ColName.GP_WR_MEAN,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_DECK_TOTAL) / pl.col(ColName.DECK_TOTAL),
        dependencies=[ColName.WON_DECK_TOTAL, ColName.DECK_TOTAL],
    ),
    ColumnSpec(
        name=ColName.GP_WR_EXCESS,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GP_WR) - pl.col(ColName.GP_WR_MEAN),
        dependencies=[ColName.GP_WR, ColName.GP_WR_MEAN],
    ),
    ColumnSpec(
        name=ColName.GP_WR_VAR,
        col_type=ColType.AGG,
        expr=(pl.col(ColName.GP_WR_EXCESS).pow(2) * pl.col(ColName.NUM_GP)).sum()
        / pl.col(ColName.DECK_TOTAL),
        dependencies=[ColName.GP_WR_EXCESS, ColName.NUM_GP, ColName.DECK_TOTAL],
    ),
    ColumnSpec(
        name=ColName.GP_WR_STDEV,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GP_WR_VAR).sqrt(),
        dependencies=[ColName.GP_WR_VAR],
    ),
    ColumnSpec(
        name=ColName.GP_WR_Z,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GP_WR_EXCESS) / pl.col(ColName.GP_WR_STDEV),
        dependencies=[ColName.GP_WR_EXCESS, ColName.GP_WR_STDEV],
    ),
    ColumnSpec(
        name=ColName.GIH_TOTAL,
        col_type=ColType.AGG,
        expr=pl.col(ColName.NUM_GIH).sum(),
        dependencies=[ColName.NUM_GIH],
    ),
    ColumnSpec(
        name=ColName.WON_GIH_TOTAL,
        col_type=ColType.AGG,
        expr=pl.col(ColName.NUM_GIH_WON).sum(),
        dependencies=[ColName.NUM_GIH_WON],
    ),
    ColumnSpec(
        name=ColName.GIH_WR_MEAN,
        col_type=ColType.AGG,
        expr=pl.col(ColName.WON_GIH_TOTAL) / pl.col(ColName.GIH_TOTAL),
        dependencies=[ColName.WON_GIH_TOTAL, ColName.GIH_TOTAL],
    ),
    ColumnSpec(
        name=ColName.GIH_WR_EXCESS,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GIH_WR) - pl.col(ColName.GIH_WR_MEAN),
        dependencies=[ColName.GIH_WR, ColName.GIH_WR_MEAN],
    ),
    ColumnSpec(
        name=ColName.GIH_WR_VAR,
        col_type=ColType.AGG,
        expr=(pl.col(ColName.GIH_WR_EXCESS).pow(2) * pl.col(ColName.NUM_GIH)).sum()
        / pl.col(ColName.GIH_TOTAL),
        dependencies=[ColName.GIH_WR_EXCESS, ColName.NUM_GIH, ColName.GIH_TOTAL],
    ),
    ColumnSpec(
        name=ColName.GIH_WR_STDEV,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GIH_WR_VAR).sqrt(),
        dependencies=[ColName.GIH_WR_VAR],
    ),
    ColumnSpec(
        name=ColName.GIH_WR_Z,
        col_type=ColType.AGG,
        expr=pl.col(ColName.GIH_WR_EXCESS) / pl.col(ColName.GIH_WR_STDEV),
        dependencies=[ColName.GIH_WR_EXCESS, ColName.GIH_WR_STDEV],
    ),
    ColumnSpec(
        name=ColName.DECK_MANA_VALUE_AVG,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK_MANA_VALUE) / pl.col(ColName.DECK),
        dependencies=[ColName.DECK_MANA_VALUE, ColName.DECK],
    ),
    ColumnSpec(
        name=ColName.DECK_LANDS_AVG,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK_LANDS) / pl.col(ColName.NUM_GAMES),
        dependencies=[ColName.DECK_LANDS, ColName.NUM_GAMES],
    ),
    ColumnSpec(
        name=ColName.DECK_SPELLS_AVG,
        col_type=ColType.AGG,
        expr=pl.col(ColName.DECK_SPELLS) / pl.col(ColName.NUM_GAMES),
        dependencies=[ColName.DECK_SPELLS, ColName.NUM_GAMES],
    ),
]

col_spec_map = {col.name: col for col in _column_specs}

for item in ColName:
    assert item in col_spec_map, f"column {item} enumerated but not specified"
