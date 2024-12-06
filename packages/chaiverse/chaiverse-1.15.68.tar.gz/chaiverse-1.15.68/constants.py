import os


DEFAULT_MAX_WORKERS = 1


PUBLIC_LEADERBOARD_MINIMUM_FEEDBACK_COUNT = 0


SUBMISSION_CONSTANT_FIELD_DEFAULTS = {
    'is_custom_reward': False,
    'elo_rating': float('nan'),
    'num_battles': 0,
    'num_wins': 0,
    'model_num_parameters': float('nan'),
}


LEADERBOARD_INDIVIDUAL_RANK_PARAMS = [
    dict(value_column='elo_rating', rank_column='elo_rank', ascending=False),
]


LEADERBOARD_OVERALL_RANK_PARAMS = [
    dict(
        from_rank_columns=['elo_rank',],
        overall_score_column='overall_user_score', overall_rank_column='overall_user_rank'
    ),
]


LEADERBOARD_FORMAT_CONFIGS = {}


LEADERBOARD_FORMAT_CONFIGS['meval'] = {
    "output_columns": [
        'developer_uid',
        'model_name',
        'is_custom_reward',
        "overall_meval_score",
        'elo_rating',
        'num_battles',
        'num_wins',
        'size',
        'status',
        'submission_id',
    ],
    "sort_params": {
        "by": "overall_meval_score",
        "ascending": True
    },
}


LEADERBOARD_FORMAT_CONFIGS['user'] = {
    "output_columns": [
        'developer_uid',
        'model_name',
        'elo_rating',
        'elo_rank',
        'overall_user_score',
        'num_battles',
        'num_wins',
        'is_custom_reward',
        'submission_id',
        'size',
    ],
    "sort_params": {
        "by": "overall_user_score",
        "ascending": True
    }
}
