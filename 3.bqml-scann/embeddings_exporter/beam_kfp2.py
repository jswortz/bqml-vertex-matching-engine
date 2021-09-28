#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import absolute_import

import argparse
import logging
import re
import os

from past.builtins import unicode

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--bq_dataset_name', 
                        dest='bq_dataset_name', 
                        help='BigQuery dataset name.', 
                        required=True)
    parser.add_argument('--embeddings_table_name', 
                        dest='embeddings_table_name', 
                        help='BigQuery table name where the embeddings are strored', 
                        required=True)
    parser.add_argument('--output_dir',
                        dest='output_dir',
                        help='GCS location where the embedding CSV files will be stored.',
                        required=True)
    parser.add_argument('--project_id',
                        dest='project_id',
                        help='GCS project id.',
                        required=True)

    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_args.extend([
    #     # CHANGE 2/5: (OPTIONAL) Change this to DataflowRunner to
    #     # run your pipeline on the Google Cloud Dataflow Service.
        '--runner=DataflowRunner',
    #     # CHANGE 3/5: Your project ID is required in order to run your pipeline on
    #     # the Google Cloud Dataflow Service.
         f'--project={known_args.project_id}',
    #     # CHANGE 4/5: Your Google Cloud Storage path is required for staging local
    #     # files.
    #     '--staging_location=gs://YOUR_BUCKET_NAME/AND_STAGING_DIRECTORY',
    #     # CHANGE 5/5: Your Google Cloud Storage path is required for temporary
    #     # files.
    #     '--temp_location=gs://YOUR_BUCKET_NAME/AND_TEMP_DIRECTORY',
        '--job_name=embedding-export-matching-engine',
    ])
    print(known_args)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    with beam.Pipeline(options=pipeline_options) as p:
        def get_query(dataset_name, table_name):
            query = f'''
            SELECT 
                item_Id,
                embedding
            FROM 
                `{dataset_name}.{table_name}`;
            '''
            return query

        def to_csv(entry):
            item_Id = entry['item_Id']
            embedding = entry['embedding']
            csv_string = f'{item_Id},'
            csv_string += ','.join([str(value) for value in embedding])
            return csv_string

        query = get_query(known_args.bq_dataset_name, known_args.embeddings_table_name)
        output_prefix = os.path.join(known_args.output_dir, 'embeddings')
            
        _ = (
            p
            | 'ReadFromBigQuery' >> beam.io.ReadFromBigQuery(
                project=known_args.project_id, query=query, use_standard_sql=True, flatten_results=False)
            | 'ConvertToCsv' >> beam.Map(to_csv)
            | 'WriteToCloudStorage' >> beam.io.WriteToText(
                file_path_prefix = output_prefix,
                file_name_suffix = ".csv")
            )
        
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()