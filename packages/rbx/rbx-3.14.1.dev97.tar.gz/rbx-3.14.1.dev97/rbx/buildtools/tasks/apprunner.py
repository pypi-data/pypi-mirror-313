import subprocess
from pathlib import Path
from textwrap import dedent

import click
from jinja2 import Environment

from .. import REGION, REGISTRY


@click.command()
@click.argument("app")
@click.option("-s", "--source", default=".")
@click.option("-v", "--version", default="latest")
def submit(app, source, version):
    """Submit a local Docker build and push the image to AWS ECR."""
    tag = f"{REGISTRY}/{app}:{version}"

    # Login to the Amazon Container Registry
    subprocess.run(
        "aws ecr get-login-password | docker login"
        f" --username AWS --password-stdin {REGISTRY}",
        shell=True,
    )

    # Build image
    subprocess.run(f"docker build -t {tag} {source}", shell=True)

    # Push image
    subprocess.run(f"docker push {tag}", shell=True)


@click.command()
@click.argument("app")
@click.option("--env", multiple=True)
@click.option("--secret", multiple=True)
@click.option("--name")
@click.option("--port", type=int, default=8000)
@click.option("-s", "--source", default=".")
@click.option("-v", "--version", default="latest")
def deploy(ctx, app, env, secret, name, port, source, version):
    """Deploy an image to App Runner."""
    config_file = Path("apprunner.yaml")
    source_file = Path(source) / "apprunner.yaml"

    if not source_file.exists():
        raise click.Abort("Cannot find source apprunner.yaml file")

    if source_file != config_file and config_file.exists():
        raise click.Abort(
            "Conflicting apprunner.yaml files (found file both at root and source)"
        )

    delete_on_exit = source_file != config_file

    with source_file.open() as fp:
        config = fp.read()

    with config_file.open("w") as fp:
        fp.write(config)

    if delete_on_exit:
        config_file.unlink()

    environments = dict([tuple(kv.split("=")) for kv in env])
    secrets = dict([tuple(kv.split("=")) for kv in secret])

    template = Environment(lstrip_blocks=True).from_string(
        dedent(
            """\
            {
              "ImageRepository": {
                "ImageIdentifier": "{{tag}}",
                "ImageRepositoryType": "ECR",
                "ImageConfiguration": {
                  "Port": "{{port}}",
                  "RuntimeEnvironmentVariables": {
                    {%- for key, value in environments.items() %}
                    "{{key}}": "{{value}}"{% if loop.last %}{% else %},{% endif %}
                    {%- endfor %}
                  },
                  "RuntimeEnvironmentSecrets": {
                    {%- for key, value in secrets.items() %}
                    "{{key}}": "{{value}}"{% if loop.last %}{% else %},{% endif %}
                    {%- endfor %}
                  }
                }
              },
              "AutoDeploymentsEnabled": false,
              "AuthenticationConfiguration": {
                "AccessRoleArn": "arn:aws:iam::474071279654:role/Service"
              }
            }
            """
        )
    )

    configuration = template.render(
        environments=environments,
        port=port,
        secrets=secrets,
        tag=f"{REGISTRY}/{app}:{version}",
    )

    name = name or app

    # Does the service already exist?
    query = f"ServiceSummaryList[?ServiceName == '{name}'].ServiceArn | [0]"
    command = subprocess.run(
        f'aws apprunner list-services --query "{query}"',
        shell=True,
        capture_output=True,
    )
    arn = command.stdout.strip().strip('"')

    if arn == "null":
        # Create service
        subprocess.run(
            "aws apprunner create-service"
            f" --region {REGION}"
            f" --service-name {name}"
            f" --source-configuration '{configuration}'"
            " --instance-configuration 'InstanceRoleArn=arn:aws:iam::474071279654:role/Service'"
            " --no-cli-pager",
            shell=True,
        )
    else:
        # Update service
        subprocess.run(
            "aws apprunner update-service"
            f" --region {REGION}"
            f" --service-arn {arn}"
            f" --source-configuration '{configuration}'"
            " --no-cli-pager",
            shell=True,
        )
