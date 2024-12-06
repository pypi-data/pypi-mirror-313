import json
import click
from pydantic import Field

from chaiverse.cli_utils.login_cli import developer_login, developer_logout
from chaiverse.leaderboard_cli import get_leaderboard, display_leaderboard
from chaiverse import submit
from chaiverse.cli_utils.submit_cli import print_model_info, add_submit_cli_options, add_formatter_cli_options, submit_model_from_params, submit_blend_from_params
from chaiverse.cli_utils.formatters_cli import print_formatter_info, get_formatter_map
from chaiverse.feedback import get_feedback


@click.group()
def cli():
    pass


@cli.command(help="Login with your chai developer_key. If you don't have one, contact us!")
def login():
    return developer_login()


@cli.command(help="Logout and clear developer_key from cache")
def logout():
    return developer_logout()


@cli.command(help="Print current season's leaderboard")
def leaderboard():
    return display_leaderboard()


@cli.command(help="List your submissions")
def my_submissions():
    response = submit.get_my_submissions()
    for submission_id, status in response.items():
        print(submission_id, ':', status)


@cli.command(help="Provide model's submission_id, print its information")
@click.argument('submission_id')
def model_info(submission_id):
    return print_model_info(submission_id)


@cli.command(help="Provide model's submission_id, randomly sample a feedback. It uses cached feedback by default, to refresh, pass in '--reload'. ")
@click.option('--reload', is_flag=True, help="Reload the model feedback.")
@click.argument('submission_id')
def sample_feedback(reload, submission_id):
    feedback = get_feedback(submission_id, reload=reload)
    feedback.sample()


@cli.command(help="Provide model's submission_id, deactivate it")
@click.argument('submission_id')
def deactivate(submission_id):
    return submit.deactivate_model(submission_id)


@cli.command(help="List available formatters")
def list_formatters():
    for formatter_name in get_formatter_map().keys():
        print(formatter_name)


@cli.command(help="Provide formatter_name, print its information.")
@click.argument('formatter_name')
def formatter_info(formatter_name):
    return print_formatter_info(formatter_name)


@cli.command(help="Submit model by providing submission and generation paramters.")
@add_submit_cli_options(submit.FrontEndSubmissionRequest, submit.GenerationParams)
@add_formatter_cli_options(submit.FrontEndSubmissionRequest)
def submit_model(**params):
    return submit_model_from_params(**params)


@cli.command(help="Submit model blends by providing multiple submission_ids, e.g. --submissions submission_id_1 --submissions submission_id_2")
@add_submit_cli_options(submit.FrontEndBlendSubmissionRequest)
def submit_blend(**params):
    return submit_blend_from_params(**params)
