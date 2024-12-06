# Copyright (c) 2024, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import json
import shutil

from nemo_curator.utils.distributed_utils import get_client, read_data
from nemo_curator.utils.file_utils import (
    expand_outdir_and_mkdir,
    get_all_files_paths_under,
    separate_by_metadata,
)
from nemo_curator.utils.script_utils import ArgumentHelper


def main(args):
    client = get_client(**ArgumentHelper.parse_client_args(args))

    files = get_all_files_paths_under(args.input_data_dir)
    input_data = read_data(
        files, file_type=args.input_file_type, backend="pandas", add_filename=True
    )

    output_dir = expand_outdir_and_mkdir(args.output_data_dir)

    metadata_field = args.input_metadata_field
    print(f"Beginning metadata separation for {metadata_field}")
    metadata_distribution = separate_by_metadata(
        input_data,
        output_dir,
        metadata_field,
        remove_metadata=args.remove_metadata_field,
        output_type=args.output_file_type,
    ).compute()
    print(f"Finished metadata separation for {metadata_field}")

    with open(args.output_metadata_distribution, "w") as fp:
        json.dump(metadata_distribution, fp)

    if args.remove_input_dir:
        print(f"Removing all files in {args.input_data_dir}")
        shutil.rmtree(args.input_data_dir)
        print(f"Finished removing all files in {args.input_data_dir}")


def attach_args(
    parser=argparse.ArgumentParser(
        """
    Spits a dataset into subdirectories based on metadata values
""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
):
    argumentHelper = ArgumentHelper(parser)

    argumentHelper.add_arg_input_data_dir()
    argumentHelper.add_arg_input_file_type()
    argumentHelper.add_arg_output_data_dir(
        help="The output directory to where the metadata-separated files "
        "will be written. Each file will be written to its respective "
        "metadata directory that is a sub-directory of this directory"
    )
    argumentHelper.add_arg_output_file_type()
    argumentHelper.add_distributed_args()
    parser.add_argument(
        "--input-metadata-field",
        type=str,
        default="language",
        help="The name of the field within each datapoint object of the input "
        "file that the dataset should be separated by.",
    )
    parser.add_argument(
        "--output-metadata-distribution",
        type=str,
        help="Output json file containing the frequency of documents "
        "that occur for a particular metadata.",
    )
    ArgumentHelper.attach_bool_arg(
        parser,
        "remove-input-dir",
        default=False,
        help="Specify '--remove-input-dir' to remove the original "
        "input directory. This is false by default.",
    )
    ArgumentHelper.attach_bool_arg(
        parser,
        "remove-metadata-field",
        default=False,
        help="Option of whether to remove the metadata field "
        "after filtering. Useful only in the case in which one metadata "
        "is desired to be separated from the others",
    )

    return parser


def console_script():
    main(attach_args().parse_args())
