import argparse
import os

from graphstorm.config import SUPPORTED_TASKS
from graphstorm.sagemaker.sagemaker_infer import run_infer

def parse_train_args():
    """  Add arguments for model training
    """
    parser = argparse.ArgumentParser(description='gs sagemaker train pipeline')

    parser.add_argument("--task-type", type=str,
        help=f"task type, builtin task type includes: {SUPPORTED_TASKS}")

    # disrributed training
    parser.add_argument("--graph-name", type=str, help="Graph name")
    parser.add_argument("--graph-data-s3", type=str,
        help="S3 location of input training graph")
    parser.add_argument("--infer-yaml-s3", type=str,
        help="S3 location of inference yaml file. "
             "Do not store it with partitioned graph")
    parser.add_argument("--output-emb-s3", type=str,
        help="S3 location to store GraphStorm generated node embeddings.",
        default=None)
    parser.add_argument("--output-prediction-s3", type=str,
        help="S3 location to store prediction results. " \
             "(Only works with node classification/regression " \
             "and edge classification/regression tasks)",
        default=None)
    parser.add_argument("--model-artifact-s3", type=str,
        help="S3 bucket to load the saved model artifacts")
    parser.add_argument("--custom-script", type=str, default=None,
        help="Custom training script provided by a customer to run customer training logic. \
            Please provide the path of the script within the docker image")

    # following arguments are required to launch a distributed GraphStorm training task
    parser.add_argument('--data-path', type=str, default=os.environ['SM_CHANNEL_TRAIN'])
    parser.add_argument('--num-gpus', type=str, default=os.environ['SM_NUM_GPUS'])
    parser.add_argument('--sm-dist-env', type=str, default=os.environ['SM_TRAINING_ENV'])
    parser.add_argument('--master-addr', type=str, default=os.environ['MASTER_ADDR'])
    parser.add_argument('--region', type=str, default=os.environ['AWS_REGION'])

    # Add your args if any

    return parser

if __name__ =='__main__':
    parser = parse_train_args()
    args, unknownargs = parser.parse_known_args()

    run_infer(args, unknownargs)
