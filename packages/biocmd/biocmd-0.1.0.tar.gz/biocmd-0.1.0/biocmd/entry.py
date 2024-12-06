import click

from . import local_config
from . import bio_data
from . import pipeline
from . import bio_script
from . import bio_env
from . import bio_task
from . import server_config

@click.group()
def cli():
    """A simple biolab command client, See https://github.com/BioHubX/biocmd  for more detail information"""
    pass

@cli.group()
def workflow():
    """ Define the dependencies between processes

    For example: biocmd workflow create --name 'Strain Analysis pipeline' --code StrainAnalysis --step assembly --prestep qcstat --prestep datafilter

    The above example means that creating a new pipeline requires specifying the name of the pipeline, the unique code of the pipeline, the name of the current algorithm of the pipeline, and the name of the pre-algorithm ["qcstat","datafilter"] that the algorithm depends on
    """
    pass

@cli.group()
def script():
    """ Configure the algorithm used in the analysis flow

    For example: biocmd script create --workflow StrainAnalysis --step qcstat --script biohubx/qcstat:v0.1.0

    The above example means that creating an analysis algorithm requires specifying the name of a workflow, the name of the algorithm, and the algorithm implementation of the docker image corresponding to the algorithm
    """
    pass

@cli.group()
def env():
    """  Configure the Input,Output and Environment parameters of the algorithm

    For example: biocmd env create --workflow StrainAnalysis --step qcstat --type Input --key file1 --feature _R1.fq.gz

    For the above examples, that means that for the qcstat analysis algorithm in the StrainAnalysis workflow,a dependency on an input parameter is required, with the parameter name being file1, and the feature of the value of this parameter being that it contains _R1.fq.gz.
    """
    pass

@cli.group()
def file():
    """ Data file management,such as data registration

    For example: biocmd file create --basedir /workspace/20241205

    The above example means that the "/workspace/20241205" folder is used as the starting point to scan the address of the original sequencing file, which should meet certain format requirements, such as: /{baseDir}/{sampleNo}/{uniqueNo}/{sampleNo.R1.fq.gz},the final file structure looks like this:
        sample1 => /workspace/20241205/sample1/unique1/sample1_R1.fq.gz
        sample1 => /workspace/20241205/sample1/unique1/sample1_R2.fq.gz

        sample2 => /workspace/20241205/sample2/unique2/sample2_R1.fq.gz
        sample2 => /workspace/20241205/sample2/unique2/sample2_R2.fq.gz

        and more ...

    sampleNo can same as uniqueNo
    """
    pass

@cli.group()
def task():
    """ Task management, such as starting a task and viewing a task

    For example: biocmd task create --workflow StrainAnalysis --step qcstat --uniqueno sample1

    The above example means that an StrainAnalysis_qcstat analysis task has been created for the sample1 (unique sample number)
    """
    pass

@cli.group()
def server():
    """ Configure the remote server environment, only support: server,parallel,outputDir

    For example: biocmd server --key parallel --value 30

    The biolab server specifies that the maximum concurrency capacity of the remote docker machine is 30 when doing automated scheduling (compute nodes can only allow a maximum of 30 tasks to be performed simultaneously).
    """
    pass

@cli.group()
def local():
    """ Configure the remote server address, port, and token

    For example: biocmd local set --server http://localhost --port 8080 --token xxxxxxxx

    The above example means that the client is connected to the biolab server deployed at localhost, the service exposed port is 8080, and the token is a string automatically generated when the biolab service is started
    """
    pass


@local.command()
@click.option('--server', required=True, default='http://localhost', help='server http address, eg: http://biolab.com')
@click.option('--port', required=True, default='8080', help='server port, eg 8080')
@click.option('--token', required=True, default='', help='Token of the biolab server')
def set(server,port,token):
    """
        --server,--port, --port optional be provided
    """
    local_config.set_config(server, port, token)


@workflow.command()
@click.option('--name', required=True, help='Pipeline name')
@click.option('--code', required=True, help='Pipeline code')
@click.option('--step', required=True, help='Step name in the pipeline code')
@click.option('--prestep', multiple=True, required=False, help='The pre-step of the current step in the pipeline')
def create(name,code,step, prestep):
    """
        --name, --code, --step, --prestep must be provided
    """
    for pre in prestep:
        if not pre.strip():
            print("Prestep value contains empty string")
            return
    pipeline.create_workflow(name, code, step, prestep)


@workflow.command()
@click.option('--workflow', required=False, help='Pipeline code')
def list(workflow):
    """
        --workflow must be provided
    """
    pipeline.list_workflow(workflow)


@script.command()
@click.option('--workflow', required=True, help='Pipeline code')
@click.option('--step', required=True, help='Step name in the pipeline code')
@click.option('--script', required=True, help='Docker image name (include version)')
def create(workflow,step, script):
    """
        --workflow, --step, --script must be provided
    """
    bio_script.create_script(workflow,step, "Docker", script)

@script.command()
@click.option('--workflow', required=False, help='-')
def list(workflow):
    """
        --workflow must be provided
    """
    bio_script.list_script(workflow)


@env.command()
@click.option('--workflow', required=True, help='Unique pipeline code')
@click.option('--step', required=True, help='Step name in a pipeline')
@click.option('--type', required=True,  help='Only the one of [Input,Output,Mount]')
@click.option('--key', required=True, help='Feature unique key')
@click.option('--feature', required=True, help='qcstat:v1.0.0')
def create(workflow,step,type, key, feature):
    """
        --workflow,--step, --type, --key, --feature must be provided
    """
    bio_env.create_env(workflow,step, type, key, feature)

@env.command()
@click.option('--workflow', required=True, help='Unique workflow code')
@click.option('--step', required=True, help='Step name in a pipeline')
def list(workflow, step):
    """
        --workflow,--step must be provided
    """
    bio_env.list_env(workflow, step)

@file.command()
@click.option('--basedir', required=True, help="Base dir of some sample's rawdata")
def create(basedir):
    """
        --basedir must be provided
    """
    bio_data.create_file(basedir)


@file.command()
@click.option('--uniqueno', multiple=True, required=False, help='Unique name of a sample')
def list(uniqueno):
    """
       --uniqueno optional be provided
    """
    bio_data.list_file(uniqueno)

@task.command()
@click.option('--workflow', required=True, help='Unique pipeline code')
@click.option('--step', required=True, help='Step name in a pipeline')
@click.option('--uniqueno', required=True, help='Unique name of a sample')
def create(workflow,step,uniqueno):
    """
        --workflow,--step, --uniqueno must be provided
    """
    bio_task.create_task(workflow,step, uniqueno)

# @task.command()
# @click.option('--workflow', required=True, help='Unique pipeline code')
# def list(workflow):
#     """
#         --workflow  must be provided
#     """
#     bio_task.list_task(workflow)

@server.command()
@click.option('--key', required=True, help='Only one of [server,parallel,outputDir]')
@click.option('--value', required=True, help='The value of the key')
def create(key,value):
    """
        --key,--value must be provided
    """
    server_config.create_config("Docker", key, value)


@server.command()
def list():
    """
        list all of the server config
    """
    server_config.list_config()

if __name__ == '__main__':
    cli()
