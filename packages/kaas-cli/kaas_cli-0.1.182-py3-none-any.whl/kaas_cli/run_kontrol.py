from __future__ import annotations

import logging
import os
import random
import re
import shutil
import subprocess
import sys
import time
from typing import TYPE_CHECKING, Optional

import click
import docker
import requests

from .constants import CONFIG_LOG_PATH, KONTROL_JOB_DETAILS_URL
from .types import KontrolVersion  # noqa: TC003
from .types import KaasCliException
from .utils import find_kontrol_configs, get_foundry_out_dir

if TYPE_CHECKING:
    from .client import KaasClient


class RunKontrol:
    def __init__(
        self,
        kontrol_version: KontrolVersion,
        mode: str,
        extra_build_args: str = "",
        extra_prove_args: str = "",
        org_name: str = "",
        vault_name: str = "",
        branch: str = "",
        client: Optional[KaasClient] = None,
        watch: bool = False,
    ):
        self.kontrol_version = kontrol_version
        self.mode = mode
        self.extra_build_args = extra_build_args
        self.extra_prove_args = extra_prove_args
        self.org_name = org_name
        self.vault_name = vault_name
        self.branch = branch
        self.client = client
        self._configure_logging()
        self.watch = watch

    def _configure_logging(self) -> None:
        """Configure logging for the application."""
        if not CONFIG_LOG_PATH.exists():
            CONFIG_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            CONFIG_LOG_PATH.touch()
        logging.basicConfig(
            filename=CONFIG_LOG_PATH,
            filemode='a',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG,
        )

    def run(
        self,
    ) -> bool:
        """
        Run Kontrol with the given version and current source code within the current directory structure.
        KaaS will do the best it can to provide default values for kontrol.toml and foundry.toml, but it may not be possible to provide defaults for all configurations.
        Execution will start and results dumped to log/console.
        True if Kontrol ran at all PERIOD. If there are errors in the proofs these will be output but that is still a success to RUN kontrol.
        Returns:
            bool: True if Kontrol ran successfully, False otherwise
        """
        if self.mode == 'container':
            return self._run_in_container()
        elif self.mode == 'local':
            return self._run_locally()
        elif self.mode == 'remote':
            return self._run_remotely()
        else:
            click.echo(f"Invalid mode: {self.mode}")
            return False

    def _run_in_container(self) -> bool:
        if not self._is_docker_installed():
            click.echo("Docker is not installed. Please install Docker to run in a container.")
            return False
        self.kontrol_version = self._get_or_set_kontrol_version()
        if self.kontrol_version == "v0.0.0":
            click.echo("Error getting latest Kontrol release and No Version Specified. Exiting...")
            sys.exit(1)
        try:
            self._setup_docker_container()
            self._run_kontrol_in_container()
            return True
        except Exception as e:
            click.echo(f"Critical Container Error: {e}")
            sys.exit(1)

    def _get_or_set_kontrol_version(self) -> KontrolVersion:
        if self.kontrol_version == "v0.0.0":
            click.echo("No Version Specified... Using LATEST Kontrol Version")
            return self._get_latest_kontrol_release()
        return self.kontrol_version

    def _setup_docker_container(self) -> None:
        kv = self.kontrol_version.lstrip('v')
        click.echo(f"Using Kontrol Image: runtimeverificationinc/kontrol:ubuntu-jammy-{kv}")
        kontrol_toml, foundry_toml = find_kontrol_configs()
        self.output_folder = get_foundry_out_dir()
        try:
            docker_client = docker.from_env()
        except Exception as e:
            raise KaasCliException(f"Error talking to Docker client: {e}") from e
        click.echo("Pulling Kontrol Image...")
        image_tag = "ubuntu-jammy-" + kv
        try:
            docker_client.images.pull("runtimeverificationinc/kontrol", tag=image_tag)
        except Exception as e:
            raise KaasCliException(f"Error pulling Kontrol Image: {e}") from e
        container_id = random.randint(1000, 2000)
        click.echo(f"Generated container ID: {container_id}")
        try:
            self.container = docker_client.containers.run(
                f"runtimeverificationinc/kontrol:ubuntu-jammy-{kv}",
                name=f"kaas-proof-container-{container_id}",
                command="/bin/bash",
                # volumes={os.getcwd(): {'bind': '/opt/kaas', 'mode': 'rw'}},
                user="user",
                remove=True,
                detach=True,
                tty=True,
                working_dir="/opt/kaas",
            )
        except Exception as e:
            raise KaasCliException(f"Error running Kontrol Container: {e}") from e
        click.echo("Setting Permissions on Container Files...")
        self.container.exec_run("chown -R user:user /opt/kaas", stream=True, user='root')
        self._copy_files_to_container(self.container.name, '/opt/kaas', os.path.dirname(kontrol_toml))

    def _copy_files_to_container(self, container_id: str | None, container_path: str | None, host_path: str) -> None:
        if container_id is None:
            click.echo("Lost Context to Container... Exiting...")
            raise KaasCliException("Lost context to container")

        user_id = 'user'
        group_id = 'user'

        if not host_path:
            host_path = os.getcwd()

        click.echo(f"Copying files from {host_path} to {container_path}")

        # Construct the tar command to archive the current directory
        tar_command = "tar -cf - ./"

        # Construct the docker exec command to extract the archive inside the container
        docker_command = (
            f"docker exec -i {container_id} bash -cl "
            f"'tar -xf - -C {container_path} --owner={user_id} --group={group_id}'"
        )

        # Combine the commands with a pipe
        full_command = f"{tar_command} | {docker_command}"

        try:
            click.echo("Copying files to container")
            os.chdir(host_path)
            subprocess.run(full_command, shell=True, check=True)
        except Exception as e:
            raise KaasCliException(f"Error copying files to container: {e}") from e

    def _copy_files_from_container(self, container_id: str | None, container_path: str) -> None:
        if container_id is None:
            click.echo("Lost Context to Container... Exiting...")
            raise KaasCliException("Lost context to container")
        # Find the .xml file and pull it from the container to the current folder
        find_command = (
            f"docker exec -i {container_id} bash -cl 'find {container_path} -name \"kontrol_prove_report.xml\"'"
        )
        try:
            result = subprocess.run(
                find_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            kontrol_prove_report = result.stdout.decode('utf-8').strip()
            if not kontrol_prove_report:
                raise KaasCliException("kontrol_prove_report.xml not found in the container")
            copy_command = f"docker cp {container_id}:{kontrol_prove_report} ."
            subprocess.run(copy_command, shell=True, check=True)
            click.echo(f"Copied {kontrol_prove_report} from container to current folder")
        except Exception as e:
            raise KaasCliException(f"Error finding or copying kontrol_prove_report.xml from container: {e}") from e
        # Create a tarball inside the container and stream it to the host
        # user_id = os.getuid()
        # group_id = os.getgid()
        copy_out_folder_command = (
            f"docker exec -i {container_id} bash -cl 'tar -cf - -C {container_path} {self.output_folder}/' | tar -xf -"
        )
        copy_report_command = f"docker cp {container_id}:{container_path}/kontrol_prove_report.xml ."
        try:
            click.echo("Copying files from container")
            subprocess.run(copy_out_folder_command, shell=True, check=True)
            subprocess.run(copy_report_command, shell=True, check=True)
        except Exception as e:
            raise KaasCliException(f"Error copying files from container: {e}") from e

    def _parse_run_args(self, args: str) -> tuple[list[str], str]:
        # Split the args string while preserving quoted strings
        prove_args_list = []
        current_arg: list[str] = []
        in_quotes = False

        if not args:
            return [], ''

        for char in self.extra_prove_args:
            if char == '"':
                in_quotes = not in_quotes
            elif char.isspace() and not in_quotes:
                if current_arg:
                    prove_args_list.append(''.join(current_arg))
                    current_arg = []
            else:
                current_arg.append(char)

        if current_arg:
            prove_args_list.append(''.join(current_arg))

        # Separate config profiles from other options
        config_profiles = []
        other_options = []
        i = 0
        while i < len(prove_args_list):
            if prove_args_list[i] == '--config-profile' and i + 1 < len(prove_args_list):
                config_profiles.append(f'--config-profile {prove_args_list[i + 1]}')
                i += 2
            else:
                other_options.append(prove_args_list[i])
                i += 1

        # Join the other options with spaces
        options_str = ' '.join(other_options)

        return config_profiles, options_str

    def _run_kontrol_in_container(self) -> None:
        click.echo(f"Container Status: {self.container.status}")
        click.echo(f"Container Name: {self.container.name}")
        click.echo(f"Container ID: {self.container.id}")
        try:
            click.echo("Starting Kontrol Build...")
            return_code, output = self.container.exec_run(
                "kontrol build " + (f" {self.extra_build_args}" if self.extra_build_args else " "), stream=True
            )
            click.echo(f"Build Return Code: {return_code}")
            for log in output:
                click.echo(log.decode('utf-8'))
            click.echo("Starting Kontrol Prove...")
            config_profiles, options_list = self._parse_run_args(self.extra_prove_args)
            if config_profiles:
                for profile in config_profiles:
                    click.echo(f"Running kontrol prove with profile: {profile}")
                    click.echo(f'kontrol prove {profile} ' + " ".join({options_list}))
                    self._execute_kontrol_prove_container(profile + " " + options_list)
            else:
                click.echo("Running kontrol prove with profile: Default")
                self._execute_kontrol_prove_container(self.extra_prove_args)
        except KeyboardInterrupt:
            click.echo("SIGINT or CTRL-C detected. Exiting gracefully..")
            self._cleanup_container()
            sys.exit(0)
        except Exception as e:
            self._cleanup_container()
            raise KaasCliException(f"Unexpected error while running kontrol prove: {e}") from e
        self._copy_files_from_container(self.container.name, "/opt/kaas")
        self._cleanup_container()

    def _execute_kontrol_prove_container(self, args: str) -> bool:
        return_code, output = self.container.exec_run(
            "kontrol prove --xml-test-report" + (f" {args}" if args else " "),
            stream=True,
        )
        click.echo(f"Prove Return Code: {return_code}")
        for log in output:
            click.echo(log.decode('utf-8'))
        return return_code == 0

    def _cleanup_container(self) -> None:
        try:
            click.echo("Stopping Container...")
            self.container.stop()
            self.container.remove(force=True)
            click.echo("Container cleaned up successfully")
        except Exception as e:
            logging.error(f"Error stopping or removing container: {e}")

    def handle_user_interrupt(self) -> None:
        click.echo("SIGINT or CTRL-C detected. Exiting gracefully..")
        self._cleanup_container()
        sys.exit(0)

    def _run_locally(self) -> bool:
        if not self._is_kontrol_installed():
            click.echo("Kontrol is not installed. Please install Kontrol to run locally. Using kup.")
            click.echo(
                "  For installation instructions, visit: https://github.com/runtimeverification/kontrol#fast-installation"
            )
            return False

        self._check_local_kontrol_version()
        kontrol_toml, foundry_toml = find_kontrol_configs()
        click.echo(f"  Change directory to: {os.path.dirname(kontrol_toml)}")
        dirname = os.path.dirname(kontrol_toml)
        os.chdir(dirname)
        if not self._run_kontrol_build():
            return False

        if not self._run_kontrol_prove():
            return False

        return True

    def _check_local_kontrol_version(self) -> None:
        os.system("kontrol version")
        click.echo("  is installed. Checking Kontrol Version...")
        if self.kontrol_version == "v0.0.0":
            click.echo('No Version Specified... Using currently installed version')
        else:
            self._verify_specific_kontrol_version()

    def _verify_specific_kontrol_version(self) -> None:
        click.echo(f"Requested Kontrol Version: {self.kontrol_version}")
        try:
            result = subprocess.run(["kontrol", "version"], check=True, capture_output=True, text=True)
            version = self.kontrol_version.lstrip('v')
            version_pattern = re.compile(rf"Kontrol version: {re.escape(version)}\b")
            if version_pattern.search(result.stdout):
                click.echo("Exact Version Installed. Proceeding...")
            else:
                click.echo(f"Requested Version: {version}, NOT FOUND")
                click.echo(
                    "  Visit https://github.com/runtimeverification/kontrol#fast-installation for installation instructions"
                )
                sys.exit(1)
        except Exception as e:
            click.echo(f"Error checking Kontrol Version: {e}")
            sys.exit(1)

    def _run_kontrol_build(self) -> bool:
        try:
            click.echo("Starting Kontrol Build...")
            process = subprocess.Popen(
                "kontrol build " + (f" {self.extra_build_args}" if self.extra_build_args else " "),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if process.stdout is None:
                click.echo("Error running Kontrol Build...")
                return False
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    click.echo(output.strip())
            rc = process.poll()
            if rc != 0:
                click.echo("Error detected during Kontrol Build...")
                return False
            return True
        except Exception as e:
            click.echo(f"Error running Kontrol Build: {e}")
            return False

    def _run_kontrol_prove(self) -> bool:
        try:
            click.echo("Starting Kontrol Prove...")
            config_profiles, options_list = self._parse_run_args(self.extra_prove_args)
            if not config_profiles:
                return self._execute_kontrol_prove_local(self.extra_prove_args)
            else:
                click.echo(config_profiles)
                click.echo(options_list)
                for profile in config_profiles:
                    click.echo(f'Running kontrol prove with profile: {profile}')
                    click.echo(f'kontrol prove {profile} ' + " ".join({options_list}))
                    rc = self._execute_kontrol_prove_local(profile + " " + options_list)
                    if not rc:
                        return False
                return True
        except Exception as e:
            raise KaasCliException(f"Error running Kontrol Prove: {e}") from e

    def _execute_kontrol_prove_local(self, args: str) -> bool:
        process = subprocess.Popen(
            "kontrol prove --xml-test-report " + (f" {args}" if args else " "),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if process.stdout is None:
            click.echo("Error running Kontrol Prove...")
            return False
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                click.echo(output.strip())
        rc = process.poll()
        if rc != 0:
            click.echo("Error detected during Kontrol Prove...")
            return False
        return True

    def _run_remotely(
        self,
    ) -> bool:
        if self.client is not None:
            click.echo(f"  Running on {self.client._url}")
            click.echo("Visit your Compute Dashboard to check the status of your jobs.")

        repo_name, commit_hash, branch_name = self._is_git_repository()
        click.echo(f"  Repository Name: {repo_name}")
        click.echo(f"  Commit Hash: {commit_hash}")
        click.echo(f"  Branch Name: {branch_name}")

        kontrol_toml, foundry_toml = find_kontrol_configs()
        click.echo(f"  Kontrol Config File: {kontrol_toml}")
        click.echo(f"  Foundry Config File: {foundry_toml}")

        click.echo("Sending Request on Remote Proof Runner...")
        self.kontrol_version = self._get_or_set_kontrol_version()
        if self.client is None:
            click.echo("Error: KaasClient Communication Failed.")
            return False
        try:
            data = self.client.run_kontrol(
                self.org_name,
                self.vault_name,
                self.branch,
                self.extra_build_args,
                self.extra_prove_args,
                self.kontrol_version,
            )
            click.echo(
                f"  Results of remote runs can be found at {self.client.url}/app/organization/{self.org_name}/vault/{self.vault_name}"
            )
            click.echo(f"  \nYour Compute Job ID is: {data.jobId}\n")
            if self.watch:
                self._watch_job(data.jobId)
        except Exception as e:
            click.echo(f"ERROR: Running Kontrol Remote Proof Runner: \n{e}")
            return False
        return True

    def _watch_job(self, job_id: str) -> None:
        click.echo(f"Watching Job: {job_id}")
        last_status = None

        if not self.client:
            click.echo("Error: KaasClient is not provided.")
            sys.exit(1)

        try:
            while True:
                response_data = self.client.get(url=f'{self.client.url}{KONTROL_JOB_DETAILS_URL.format(job_id)}')
                # Check job status
                status = response_data.get('status')

                if status != last_status:
                    last_status = status
                    click.echo(f"Job {job_id} Status: {status}")
                if status == 'success':
                    click.echo(f"Job {job_id} completed successfully.")
                    sys.exit(0)
                elif status in ['cancelled', 'failure']:
                    click.echo(f"Job failed with status: {status}")
                    sys.exit(1)

                # Sleep for 5 seconds before checking the status again
                time.sleep(5)
        except Exception as e:
            click.echo(f"Error watching job: {e}")
            sys.exit(1)

    def _is_git_repository(self) -> tuple[str, str, str]:
        try:
            repo_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
            commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
            branch_name = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
            return repo_name, commit_hash, branch_name
        except subprocess.CalledProcessError as e:
            if "not a git repository" in str(e).lower():
                click.echo("Error: Not a git repository")
                sys.exit(1)
            else:
                click.echo(f"Error: {e}")
                raise KaasCliException(f"Unexpected error: {e}") from e
        except Exception as e:
            raise KaasCliException(f"Unexpected error: {e}") from e

    def _get_latest_kontrol_release(self) -> KontrolVersion:
        url = "https://api.github.com/repos/runtimeverification/kontrol/releases/latest"
        try:
            reponse = requests.get(url)
            if reponse.status_code == 200:
                return reponse.json()['tag_name']
            else:
                raise KaasCliException("Fetching Latest Release Failed..")
        except Exception as e:
            click.echo(f"Error: {e}")
            click.echo("  Specify a version already locally installed or check your internet connection")
            sys.exit(1)

    def _is_docker_installed(self) -> bool:
        # Check User environment for 'docker' command
        try:
            shutil.which('docker')
        except Exception as e:
            logging.error(f"Error checking for docker installation: {e}")
            return False
        return True

    def _is_kontrol_installed(self) -> bool:
        # Check User environment for 'kontrol' command
        click.echo("Checking local Kontrol installation...")
        try:
            shutil.which('kontrol')
        except Exception as e:
            click.echo(f"Error checking for kontrol: {e}")
            return False
        return True
