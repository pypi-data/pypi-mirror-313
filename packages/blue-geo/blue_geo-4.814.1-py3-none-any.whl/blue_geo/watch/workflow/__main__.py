import os
import argparse

from blueness import module
from blueness.argparse.generic import sys_exit
from blue_objects import file

from blue_geo import NAME
from blue_geo.watch.workflow.generation import generate_workflow
from blue_geo.logger import logger

NAME = module.name(__file__, NAME)

list_of_tasks = "generate"


parser = argparse.ArgumentParser(NAME)
parser.add_argument(
    "task",
    type=str,
    help=list_of_tasks,
)
parser.add_argument(
    "--algo_options",
    type=str,
)
parser.add_argument(
    "--job_name",
    type=str,
)
parser.add_argument(
    "--map_options",
    type=str,
)
parser.add_argument(
    "--offset",
    type=int,
    default=0,
)
parser.add_argument(
    "--reduce_options",
    type=str,
)
parser.add_argument(
    "--datacube_id",
    type=str,
)
parser.add_argument(
    "--object_name",
    type=str,
)
parser.add_argument(
    "--query_object_name",
    type=str,
)
parser.add_argument(
    "--suffix",
    type=str,
)
parser.add_argument(
    "--content_threshold",
    type=float,
    default=0.5,
    help="0..1",
)
args = parser.parse_args()

success = args.task in list_of_tasks
if args.task == "generate":
    success = generate_workflow(
        algo_options=args.algo_options,
        query_object_name=args.query_object_name,
        job_name=args.job_name,
        object_name=args.object_name,
        map_options=args.map_options,
        reduce_options=args.reduce_options,
    )
else:
    success = None

sys_exit(logger, NAME, args.task, success)
