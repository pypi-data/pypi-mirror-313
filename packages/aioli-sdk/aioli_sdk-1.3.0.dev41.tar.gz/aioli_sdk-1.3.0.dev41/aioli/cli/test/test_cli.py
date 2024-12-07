# © Copyright 2024 Hewlett Packard Enterprise Development LP
import csv
import json
import os
import subprocess
import uuid

import yaml


class TestCli:
    testdir = os.path.dirname(os.path.realpath(__file__))

    def test_version(self, setup_login: None) -> None:
        version_file = self.testdir + "/../../../../VERSION"
        expected = None
        with open(version_file, "r") as file:
            expected = file.read().rstrip()
            expected = "aioli " + expected
        assert 0 == os.system("aioli --version")
        actual = os.popen("aioli --version").read().strip()
        assert actual == expected

    def test_version_bad(self, setup_login: None) -> None:
        bad_version = "aioli 0.0.1-bad"
        assert 0 == os.system("aioli --version")
        actual = os.popen("aioli --version").read().strip()
        assert actual != bad_version

    def test_project_list(self, setup_login: None) -> None:
        # Validating table headers, expect to see the default project
        expected = (
            " Name    | Description         | Owner\n"
            "---------+---------------------+---------\n"
            " default | The default project | admin\n"
        )
        actual = subprocess.check_output(["aioli", "project", "list"]).decode("utf-8")
        assert actual == expected

    def test_project_create(self, setup_login: None) -> None:
        # Create a project and test for expected values
        assert (
            os.system(
                "aioli project create proj-2 " "--description 'the test project' " "--owner admin"
            )
            == 0
        )
        expected = "proj-2  | the test project    | admin"
        actual = subprocess.check_output(["aioli", "project", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_project_list_csv(self, setup_login: None) -> None:
        csv_output = subprocess.check_output(["aioli", "project", "list", "--csv"]).decode("utf-8")
        temp_file: str = "/tmp/test-cli-p.csv"
        with open(temp_file, "w") as file:
            file.write(csv_output)
        with open(temp_file, newline="") as file:
            reader = csv.DictReader(file)
            row1 = reader.__next__()
            assert row1["Name"] == "default", "Expected default"
            assert row1["Description"] == "The default project", "Expected The default project"
            assert row1["Owner"] == "admin", "Expected admin"
            row2 = reader.__next__()
            assert row2["Name"] == "proj-2", "Expected proj-2"
            assert row2["Description"] == "the test project", "Expected the test project"
            assert row2["Owner"] == "admin", "Expected admin"

    # fmt: off
    def test_project_list_json_yaml(self, setup_login: None) -> None:
        expected = (
            '[\n'       # noqa: Q000
            '  {\n'     # noqa: Q000
            '    "description": "the test project",\n'
            '    "name": "proj-2",\n'
            '    "owner": "admin"\n'
            '  },\n'    # noqa: Q000
            '  {\n'     # noqa: Q000
            '    "description": "The default project",\n'
            '    "name": "default",\n'
            '    "owner": "admin"\n'
            '  }\n'     # noqa: Q000
            ']\n'       # noqa: Q000
        )
        actual = subprocess.check_output(
            ["aioli", "project", "list", "--json"]).decode("utf-8")
        assert actual == expected

        expected_obj = json.loads(expected)
        actual_obj = yaml.safe_load(
            subprocess.check_output(["aioli", "project", "list", "--yaml"]).decode("utf-8"))

        assert actual_obj == expected_obj

    # fmt: on

    def test_project_update(self, setup_login: None) -> None:
        # Update project and test for expected values
        assert (
            os.system(
                "aioli project update proj-2 --name proj-3 "
                "--description 'the updated test project' "
                "--owner admin"
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "project", "list"]).decode("utf-8")
        expected = "proj-3  | the updated test project | admin"
        assert (actual.find(expected)) > 0

    def test_project_delete(self, setup_login: None) -> None:
        # Delete project and test for expected values
        assert os.system("aioli project delete proj-3") == 0
        actual = subprocess.check_output(["aioli", "project", "list"]).decode("utf-8")
        expected = "proj-3"
        assert (actual.find(expected)) < 0  # Expect to be not found

    def test_project_show(self, setup_login: None) -> None:
        # Show project and test for expected values
        expected = "description: The default project\nname: default\nowner: admin"
        result = subprocess.check_output(["aioli", "project", "show", "default"]).decode("utf-8")
        result_list = result.split("\n")
        filtered_result = ""

        # Filter out modifiedAt and id fields as they vary for each test run
        for line in result_list:
            if "modifiedAt" in line:
                continue
            if "id" in line:
                continue
            filtered_result = filtered_result + "\n" + line

        actual = filtered_result.strip()
        assert actual == expected

    def test_registry_list(self, setup_login: None) -> None:
        # Validating table headers, there are no entries yet
        assert os.system("aioli registry list") == 0
        expected = (
            " Name   | Type   | Access Key   | Bucket   | Secret Key   | Endpoint URL"
            "\n--------+--------+--------------+----------+--------------+----------------\n"
        )
        actual = subprocess.check_output(["aioli", "registry", "list"]).decode("utf-8")
        assert actual == expected

    def test_registry_create_and_update_insecure(self, setup_login: None) -> None:
        # Create a registry with insecure-https and test for expected values
        assert (
            os.system(
                "aioli registry create --type s3 --access-key minioadmin "
                "--secret-key minioadmin --bucket demo-bento-registry "
                "--endpoint-url http://10.30.89.14:30008 --insecure-https bento-registry-insecure"
            )
            == 0
        )

        # Newly created registry entry without id/modified as dict
        expected = yaml.safe_load(
            "accessKey: minioadmin\nbucket: demo-bento-registry\nendpointUrl: "
            "http://10.30.89.14:30008\ninsecureHttps: true\n"
            "name: bento-registry-insecure\nsecretKey: '**********'\ntype: s3\n\n"
        )
        actualstr = subprocess.check_output(
            ["aioli", "registry", "show", "bento-registry-insecure"]
        ).decode("utf-8")
        actual = yaml.safe_load(actualstr)
        del actual["id"]
        del actual["modifiedAt"]
        assert actual == expected

        # Update to secure
        if False:
            # This is blocked until CI is at python 3.9 -- then update
            # registry.py to use action=argparse.BoolOptionalAction
            assert (
                os.system("aioli registry update --no-insecure-https bento-registry-insecure") == 0
            )
            expected["insecureHttps"] = False
            actual = subprocess.check_output(
                ["aioli", "registry", "show", "bento-registry-insecure"]
            ).decode("utf-8")
            actual = yaml.safe_load(actual)
            del actual["id"]
            del actual["modifiedAt"]
            assert actual == expected

        # Cleanup test registry
        assert os.system("aioli registry delete bento-registry-insecure") == 0

    def test_registry_create(self, setup_login: None) -> None:
        # Create a registry entry and test for success
        assert (
            os.system(
                "aioli registry create --type s3 --access-key minioadmin "
                "--secret-key minioadmin --bucket demo-bento-registry "
                "--endpoint-url http://10.30.89.14:30008/ bento-registry"
            )
            == 0
        )

        # The following test is expected to fail since we already created the
        # registry and we are trying to recreate the same.
        expected = (
            "Failed to create a registry: model registry named 'bento-registry' exists already."
        )
        try:
            subprocess.check_output(
                [
                    "aioli",
                    "registry",
                    "create",
                    "--type",
                    "s3",
                    "--access-key",
                    "minioadmin",
                    "--secret-key",
                    "minioadmin",
                    "--bucket",
                    "demo-bento-registry",
                    "--endpoint-url",
                    "http://10.30.89.14:30008/",
                    "bento-registry",
                ],
                stderr=subprocess.STDOUT,
            ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            actual = (e.output).decode("utf-8")
            assert (actual.find(expected)) >= 0

        # Check enforcement of --type values
        proc = subprocess.run(
            [
                "aioli",
                "registry",
                "create",
                "--type",
                "bob",
                "--access-key",
                "minioadmin",
                "--secret-key",
                "minioadmin",
                "--bucket",
                "demo-bento-registry",
                "--endpoint-url",
                "http://10.30.89.14:30008/",
                "bento-registry-wrong-type",
            ],
            capture_output=True,
        )
        assert proc.returncode == 1
        expected = (
            "Failed to create a registry: registry type must be one of the values "
            + "(s3, http, openllm, ngc, pfs, huggingface), provided 'bob'"
        )
        assert proc.stderr.decode("utf-8").find(expected) == 0

        # List the newly created registry entry and test for expected values
        expected = (
            "bento-registry | s3     | minioadmin   | demo-bento-registry | "
            "**********   | http://10.30.89.14:30008/"
        )
        actual = subprocess.check_output(["aioli", "registry", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_registry_model_list(self, setup_login: None) -> None:
        # List the models for the registry and test for expected values
        expected = (
            "Failed to lists the available models in a registry (for certain registry types): "
            "a registry of type s3 is unable to provide a list of supported models. "
            "Supported registries: (openllm, ngc, huggingface, pfs)"
        )
        outcome = subprocess.run(
            ["aioli", "registry", "models", "bento-registry"], capture_output=True
        )

        assert outcome.returncode == 1
        assert outcome.stderr.decode("utf-8").find(expected) == 0

    def test_registry_list_csv(self, setup_login: None) -> None:
        csv_output = subprocess.check_output(["aioli", "registry", "list", "--csv"]).decode("utf-8")
        temp_file: str = "/tmp/test-cli-r.csv"
        with open(temp_file, "w") as file:
            file.write(csv_output)
        with open(temp_file, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                assert row["Name"] == "bento-registry", "Expected bento-registry"
                assert row["Type"] == "s3", "Expected s3"
                assert row["Access Key"] == "minioadmin", "Expected minioadmin"
                assert row["Bucket"] == "demo-bento-registry", "Expected demo-bento-registry"
                assert row["Secret Key"] == "**********", "Expected **********"
                assert (
                    row["Endpoint URL"] == "http://10.30.89.14:30008/"
                ), "Expected http://10.30.89.14:30008/"

    # fmt: off
    def test_registry_list_json_yaml(self, setup_login: None) -> None:
        expected = (
            '[\n'    # noqa: Q000
            '  {\n'  # noqa: Q000
            '    "accessKey": "minioadmin",\n'
            '    "bucket": "demo-bento-registry",\n'
            '    "endpointUrl": "http://10.30.89.14:30008/",\n'
            '    "insecureHttps": false,\n'
            '    "name": "bento-registry",\n'
            '    "secretKey": "**********",\n'
            '    "type": "s3"\n'
            '  }\n'  # noqa: Q000
            ']\n'    # noqa: Q000
        )
        actual = subprocess.check_output(["aioli", "registry", "list", "--json"]).decode("utf-8")
        assert actual == expected

        expected_obj = json.loads(expected)
        actual_obj = yaml.safe_load(
            subprocess.check_output(["aioli", "registry", "list", "--yaml"]).decode("utf-8"))

        assert actual_obj == expected_obj

    # fmt: on

    def test_registry_update(self, setup_login: None) -> None:
        # Update registry and test for expected values
        subprocess.check_output(
            [
                "aioli",
                "registry",
                "update",
                "--type",
                "s3",
                "--access-key",
                "minioadmin",
                "--secret-key",
                "minioadmin",
                "--bucket",
                "demo-bento-registry",
                "--endpoint-url",
                "http://10.30.89.14:30008/",
                "--name",
                "bento-registry1",
                "bento-registry",
            ],
            stderr=subprocess.STDOUT,
        ).decode("utf-8")
        expected = (
            "bento-registry1 | s3     | minioadmin   | demo-bento-registry | "
            "**********   | http://10.30.89.14:30008/"
        )
        actual = subprocess.check_output(["aioli", "registry", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

        # Check enforcement of --type values
        proc = subprocess.run(
            [
                "aioli",
                "registry",
                "update",
                "--type",
                "bob",
                "bento-registry1",
            ],
            capture_output=True,
        )
        assert proc.returncode == 1
        expected = (
            "Failed to modify a registry: registry type must be one of the values "
            + "(s3, http, openllm, ngc, pfs, huggingface), provided 'bob'"
        )
        assert proc.stderr.decode("utf-8").find(expected) == 0

    def test_model_list(self, setup_login: None) -> None:
        # Test header row of model table, there are no entries at this point.
        assert os.system("aioli model list") == 0
        expected = (
            " Name   | Description   | Version   | URI   | Image   | Registry"
            "\n--------+---------------+-----------+-------+---------+------------\n"
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        assert actual == expected

        # Test that --name and --all are mutually exclusive parameters
        assert os.system("aioli model list --all --name doesnt-matter") == 512

        # Create version 1 of a model
        command = [
            "aioli",
            "model",
            "create",
            "my-model",
            "--image",
            "fictional.registry.example/imagename",
            "--description",
            "the model description",
            "--requests-cpu",
            "1.0",
            "--requests-memory",
            "1Gi",
            "--requests-gpu",
            "1.0",
            "--limits-cpu",
            "2.5",
            "--limits-memory",
            "1Gi",
            "--limits-gpu",
            "1.0",
        ]

        # Run the command and capture stdout and stderr
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Print the stdout and stderr
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Check the exit status
        assert result.returncode == 0, f"Command failed with exit code {result.returncode}"

        # Create version 2
        assert os.system("aioli model update my-model " "--limits-cpu 5.0 ") == 0

        # Check that aioli model list shows only the latest version of all models
        # by default
        not_expected = (
            "my-model | the model description |         1 |       |"
            " fictional.registry.example/imagename"
        )
        expected = (
            "my-model | the model description |         2 |       |"
            " fictional.registry.example/imagename"
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        assert actual.find(not_expected) < 0 and actual.find(expected) > 0

        # Check that aioli model list with the --all flag shows all versions of
        # all models
        expected = (
            "my-model | the model description |         2 |       |"
            " fictional.registry.example/imagename |\n my-model |"
            " the model description |         1 |       |"
            " fictional.registry.example/imagename"
        )

        actual = subprocess.check_output(["aioli", "models", "list", "--all"]).decode("utf-8")
        assert actual.find(expected) > 0

        # Create a different model
        assert (
            os.system(
                "aioli model create other-model "
                "--image fictional.registry.example/imagename "
                '--description "the model description" '
                "--requests-cpu 1.0 "
                "--requests-memory 1Gi "
                "--requests-gpu 1.0 "
                "--limits-cpu 2.5 "
                "--limits-memory 1Gi "
                "--limits-gpu 1.0 "
            )
            == 0
        )

        not_expected = (
            "other-model | the model description |         1 |       |"
            " fictional.registry.example/imagename"
        )
        actual = subprocess.check_output(["aioli", "models", "list", "--name", "my-model"]).decode(
            "utf-8"
        )
        # Same expected as previous
        assert actual.find(not_expected) < 0 and actual.find(expected) > 0

    # This test uses and cleans up models created in test_model_list
    def test_model_show(self, setup_login: None) -> None:
        # Check that aioli model show displays the latest version by default
        # when multiple versions of the model exist
        actual = subprocess.check_output(["aioli", "model", "show", "my-model"]).decode("utf-8")
        assert actual.find("version: 2") > 0 and actual.find("version: 1") < 0

        # Cleanup
        assert (
            os.system(
                "aioli model delete my-model.v1 && "
                "aioli model delete my-model.v2 && "
                "aioli model delete other-model"
            )
            == 0
        )

    def test_model_create(self, setup_login: None) -> None:
        # Create an entry for model table and test for expected values
        assert (
            os.system(
                "aioli model create iris-tf-keras --registry bento-registry1 "
                "--url s3://demo-bento-registry/iris-tf-keras "
                "--image fictional.registry.example/imagename "
                '--description "the model description" '
                "-e name1 --env name2=value2 "
                "-a arg1 --arg arg2 '-a -optarg' "
                "--requests-cpu 1.0 "
                "--requests-memory 1Gi "
                "--requests-gpu 1.0 "
                "--limits-cpu 2.5 "
                "--limits-memory 1Gi "
                "--limits-gpu 1.0 "
                "--gpu-type T4 "
                "--format openllm"
            )
            == 0
        )
        expected = (
            "iris-tf-keras | the model description |         1 | "
            "s3://demo-bento-registry/iris-tf-keras | "
            "fictional.registry.example/imagename | bento-registry1"
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_model_list_csv(self, setup_login: None) -> None:
        csv_output = subprocess.check_output(["aioli", "model", "list", "--csv"]).decode("utf-8")
        temp_file: str = "/tmp/test-cli-m.csv"
        with open(temp_file, "w") as file:
            file.write(csv_output)

        matching_row_found = False
        with open(temp_file, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                    row["Name"] == "iris-tf-keras"
                    and row["Description"] == "the model description"
                    and row["Version"] == "1"
                    and row["URI"] == "s3://demo-bento-registry/iris-tf-keras"
                    and row["Image"] == "fictional.registry.example/imagename"
                    and row["Registry"] == "bento-registry1"
                ):
                    matching_row_found = True
                    break

        assert matching_row_found, "No row with the expected properties was found"

    # Exercise various means of specifying the model version, using the show command as a vehicle.
    def test_model_versions(self, setup_login: None) -> None:
        yaml_output = subprocess.check_output(["aioli", "model", "show", "iris-tf-keras"]).decode(
            "utf-8"
        )
        temp_file: str = "/tmp/test-cli-m.yaml"

        # Demonstrate that we have valid yaml
        with open(temp_file, "w") as file:
            file.write(yaml_output)
        with open(temp_file, newline="") as file:
            from ruamel.yaml import YAML

            yaml = YAML(typ="safe")
            model = yaml.load(file)

        assert model["version"] == 1, "Validity check -- version == 1"

        yaml_output2 = subprocess.check_output(
            ["aioli", "model", "show", "iris-tf-keras.v1"]
        ).decode("utf-8")
        assert yaml_output == yaml_output2, "Expect the same output using .v1"

        yaml_output2 = subprocess.check_output(
            ["aioli", "model", "show", "iris-tf-keras.V1"]
        ).decode("utf-8")
        assert yaml_output == yaml_output2, "Expect the same output using .V1"

    # fmt: off
    def test_model_list_json_yaml(self, setup_login: None) -> None:
        expected = (
            '[\n'    # noqa: Q000
            '  {\n'  # noqa: Q000
            '    "arguments": [\n'
            '      "arg1",\n'
            '      "arg2",\n'
            '      "-optarg"\n'
            '    ],\n'  # noqa: Q000
            '    "cachingEnabled": false,\n'
            '    "description": "the model description",\n'
            '    "environment": {\n'
            '      "name1": "",\n'
            '      "name2": "value2"\n'
            '    },\n'  # noqa: Q000
            '    "image": "fictional.registry.example/imagename",\n'
            '    "modelFormat": "openllm",\n'
            '    "name": "iris-tf-keras",\n'
            '    "registry": "bento-registry1",\n'
            '    "resources": {\n'
            '      "gpuType": "T4",\n'
            '      "limits": {\n'
            '        "cpu": "2.5",\n'
            '        "gpu": "1.0",\n'
            '        "memory": "1Gi"\n'
            '      },\n'  # noqa: Q000
            '      "requests": {\n'
            '        "cpu": "1.0",\n'
            '        "gpu": "1.0",\n'
            '        "memory": "1Gi"\n'
            '      }\n'  # noqa: Q000
            '    },\n'   # noqa: Q000
            '    "url": "s3://demo-bento-registry/iris-tf-keras",\n'
            '    "version": 1\n'
            '  }\n'  # noqa: Q000
            ']\n'    # noqa: Q000
        )
        actual = subprocess.check_output(["aioli", "model", "list", "--json"]).decode("utf-8")
        assert actual.find(expected) >= 0

        expected_obj = json.loads(expected)
        actual_obj = yaml.safe_load(
            subprocess.check_output(["aioli", "model", "list", "--yaml"]).decode("utf-8"))

        assert actual_obj == expected_obj
    # fmt: on

    def test_model_create_no_image(self, setup_login: None) -> None:
        # The image is optional; verify...
        assert (
            os.system(
                "aioli model create openllm --registry bento-registry1 "
                "--format openllm "
                "--url s3://demo-bento-registry/iris-tf-keras "
                '--description "the model description"'
            )
            == 0
        )
        expected = (
            "openllm       | the model description |         1 | "
            "s3://demo-bento-registry/iris-tf-keras |"
            "                                      | bento-registry1"
        )
        actual = subprocess.check_output(["aioli", "model", "list"]).decode("utf-8")

        assert (actual.find(expected)) > 0
        assert os.system("aioli model delete openllm.v1") == 0

    def test_model_update_bad_model_name(self, setup_login: None) -> None:
        # Attempt to update model specifying the version incorrectly. Here we specify
        # a suffix of ".1", and not ".v1" which would specify the name & version.
        # assert (os.system("aioli model update iris-tf-keras.1") == 0)
        try:
            subprocess.check_output(
                ["aioli", "model", "update", "iris-tf-keras.1"], stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            assert e.returncode == 1
            expected = "Failed to modify a packaged model: model 'iris-tf-keras.1' does not exist."
            actual: str = e.output.decode("utf-8")
            assert actual.find(expected) == 0

    def test_model_update(self, setup_login: None) -> None:
        # Update existing model entry and test for expected values
        assert (
            os.system(
                "aioli model update iris-tf-keras --name iris-tf-keras1 "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris-tf-keras_updated "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "model", "list", "--all"]).decode("utf-8")
        expected = (
            "iris-tf-keras1 | the updated model description |         1 "
            "| s3://demo-bento-registry/iris-tf-keras_updated | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

        # Create a second version of the model
        assert (
            os.system(
                "aioli model update iris-tf-keras --name iris-tf-keras "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris-tf-keras_updated_v2 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "model", "list", "--all"]).decode("utf-8")
        expected = (
            "iris-tf-keras  | the updated model description |         2 "
            "| s3://demo-bento-registry/iris-tf-keras_updated_v2 | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

        # Try to create a third version of the model which fails without version
        assert (
            os.system(
                "aioli model update iris-tf-keras --name iris-tf-keras "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris-tf-keras_updated_v2 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 256
        )

        # Create a third version of the model using the second version
        assert (
            os.system(
                "aioli model update iris-tf-keras.v2 --name iris-tf-keras "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris-tf-keras_updated_v3 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )

        actual = subprocess.check_output(["aioli", "model", "list", "--all"]).decode("utf-8")

        expected = (
            "iris-tf-keras  | the updated model description |         3 "
            "| s3://demo-bento-registry/iris-tf-keras_updated_v3 | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

        # Create a fourth with a new name of the model using the second version
        # (specifying the version with the optional v{n} format)
        assert (
            os.system(
                "aioli model update iris-tf-keras.v2 --name iris-tf-keras-v4 "
                "--registry bento-registry1 "
                "--url s3://demo-bento-registry/iris-tf-keras_updated_v3 "
                "--image fictional.registry.example/updated_imagename "
                '--description "the updated model description"'
            )
            == 0
        )

        actual = subprocess.check_output(["aioli", "model", "list", "--all"]).decode("utf-8")

        expected = (
            "iris-tf-keras-v4 | the updated model description |         1 "
            "| s3://demo-bento-registry/iris-tf-keras_updated_v3 | "
            "fictional.registry.example/updated_imagename | bento-registry1"
        )
        assert (actual.find(expected)) > 0

    def test_deployment_create(self, setup_login: None) -> None:
        # Create a deployment and test for expected values
        assert (
            os.system(
                "aioli deployment create --model iris-tf-keras "
                "--namespace aioli "
                "--authentication-required false "
                "iris-tf-keras-deployment"
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "deployment", "list"]).decode("utf-8")
        expected = (
            "iris-tf-keras-deployment | iris-tf-keras |         3 | aioli       "
            "| Deploying | False           | Deploying |           0"
        )

        assert actual.find(expected) > 0

    def test_deployment_list_csv(self, setup_login: None) -> None:
        csv_output = subprocess.check_output(["aioli", "deployment", "list", "--csv"]).decode(
            "utf-8"
        )
        temp_file: str = "/tmp/test-cli-d.csv"
        with open(temp_file, "w") as file:
            file.write(csv_output)
        with open(temp_file, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                assert (
                    row["Name"] == "iris-tf-keras-deployment"
                ), "Expected iris-tf-keras-deployment"
                assert row["Model"] == "iris-tf-keras", "Expected iris-tf-keras"
                assert row["Namespace"] == "aioli", "Expected aioli"
                assert row["Status"] == "Deploying", "Expected Deploying"
                assert row["Auth Required"] == "False", "Expected False"
                assert row["State"] == "Deploying", "Expected Deploying"
                assert row["Traffic %"] == "0", "Expected 0"

    def test_deployment_update(self, setup_login: None) -> None:
        # Update the deployment and test for expected values.
        assert (
            os.system(
                "aioli deployment update "
                "--authentication-required true "
                "--model iris-tf-keras "
                "iris-tf-keras-deployment"
            )
            == 0
        )
        actual = subprocess.check_output(["aioli", "deployment", "list"]).decode("utf-8")

        expected = (
            "iris-tf-keras-deployment | iris-tf-keras |         3 | aioli       "
            "| Deploying | True            | Deploying |           0"
        )
        assert actual.find(expected) > 0

        # Disallow --pause and --resume at the same time
        proc = subprocess.run(
            [
                "aioli",
                "deployment",
                "update",
                "iris-tf-keras-deployment",
                "--pause",
                "--resume",
            ],
            capture_output=True,
        )
        assert proc.returncode == 1
        expected = "--pause and --resume cannot be specified at the same time"
        assert proc.stderr.decode("utf-8").find(expected) == 0

        # List the models and it's version for the deployment
        actual = subprocess.check_output(
            ["aioli", "model", "list-deployments", "iris-tf-keras"]
        ).decode("utf-8")
        expected = "| iris-tf-keras |         3 |       100"
        assert actual.find(expected) > 0

    # fmt: off
    def test_deployment_list_json_yaml(self, setup_login: None) -> None:
        expected = (
            '[\n'    # noqa: Q000
            '  {\n'  # noqa: Q000
            '    "arguments": [],\n'
            '    "autoScaling": {\n'
            '      "maxReplicas": 1,\n'
            '      "metric": "concurrency",\n'
            '      "minReplicas": 0,\n'
            '      "target": 1\n'
            '    },\n'  # noqa: Q000
            '    "canaryTrafficPercent": 100,\n'
            '    "environment": {},\n'
            '    "goalStatus": "Ready",\n'
            '    "model": "iris-tf-keras",\n'
            '    "name": "iris-tf-keras-deployment",\n'
            '    "namespace": "aioli",\n'
            '    "nodeSelectors": {},\n'
            '    "priorityClassName": "",\n'
            '    "secondaryState": {\n'
            '      "endpoint": "",\n'
            '      "modelId": "",\n'
            '      "nativeAppName": "",\n'
            '      "status": "None",\n'
            '      "trafficPercentage": 0\n'
            '    },\n'  # noqa: Q000
            '    "security": {\n'
            '      "authenticationRequired": true\n'
            '    },\n'  # noqa: Q000
            '    "state": {\n'
            '      "endpoint": "",\n'
            '      "modelId": "",\n'
            '      "nativeAppName": "",\n'
            '      "status": "Deploying",\n'
            '      "trafficPercentage": 0\n'
            '    },\n'  # noqa: Q000
            '    "status": "Deploying",\n'
            '    "version": "3"\n'
            '  }\n'  # noqa: Q000
            ']\n'    # noqa: Q000
        )
        actual = subprocess.check_output(
            ["aioli", "deployment", "list", "--json"]).decode("utf-8")
        assert actual == expected

        expected_obj = json.loads(expected)
        actual_obj = yaml.safe_load(subprocess.check_output(
            ["aioli", "deployment", "list", "--yaml"]).decode("utf-8"))
        assert actual_obj == expected_obj
    # fmt: on

    def test_deployment_create_with_all_options(self, setup_login: None) -> None:
        # Create a second deployment with all supported options
        # and test for expected values
        assert (
            os.system(
                "aioli deployment create --model iris-tf-keras "
                "--namespace aioli "
                "--authentication-required false "
                "--autoscaling-min-replicas 1 "
                "--autoscaling-max-replicas 10 "
                "--autoscaling-target 1 "
                "--autoscaling-metric concurrency "
                "--canary-traffic-percent 20 "
                "-a='--debug' "
                "-e MODS=SOME "
                "--node-selector kubernetes.io/arch=amd64 "
                "--priority-class-name '' "
                "iris-tf-keras-deployment-2"
            )
            == 0
        )

    def test_deployment_show(self, setup_login: None) -> None:
        # Test deployment table header, there are no entries at this point.
        assert os.system("aioli deployment show iris-tf-keras-deployment-2") == 0
        expected = None
        data_file = self.testdir + "/aioli_deployment_show.txt"
        with open(data_file, "r") as file:
            expected = file.read()
        result = subprocess.check_output(
            ["aioli", "deployment", "show", "iris-tf-keras-deployment-2"]
        ).decode("utf-8")
        result_list = result.split("\n")
        filtered_result = ""

        # Filter out modifiedAt and id fields as they vary for each test run
        for line in result_list:
            if "modifiedAt" in line:
                continue
            if "id" in line:
                continue
            filtered_result = filtered_result + "\n" + line

        actual = filtered_result.strip()
        assert actual == expected

    def test_deployment_update_args_environment(self, setup_login: None) -> None:
        # Update the deployments arguments and environment and check that changes
        # were made.
        assert (
            os.system(
                "aioli deployment update "
                "-a='--updated' "
                "-e MODS=UPDATED "
                "--env OTHER=VALUE "
                "iris-tf-keras-deployment-2"
            )
            == 0
        )

        result = subprocess.check_output(
            ["aioli", "deployment", "show", "iris-tf-keras-deployment-2"]
        ).decode("utf-8")
        result_list = result.split("\n")
        args_found = False
        other_found = False
        node_selector_found = False
        for line in result_list:
            if "- --updated" in line:
                args_found = True
            if "MODS: UPDATED" in line:
                mods_found = True
            if "OTHER: VALUE" in line:
                other_found = True
            if "kubernetes.io/arch: amd64" in line:
                node_selector_found = True

        assert args_found
        assert mods_found
        assert other_found
        assert node_selector_found

    def test_deployment_update_node_selectors(self, setup_login: None) -> None:
        # Update the deployments nodeSelectors check that changes
        # were made. Also verify arguments and environment are preserved.
        assert (
            os.system(
                "aioli deployment update "
                "--node-selector x/y=a-b "
                "--node-selector x/z=a-c "
                "iris-tf-keras-deployment-2"
            )
            == 0
        )

        result = subprocess.check_output(
            ["aioli", "deployment", "show", "iris-tf-keras-deployment-2"]
        ).decode("utf-8")
        result_list = result.split("\n")
        args_found = False
        other_found = False
        prev_node_selector_not_found = True
        node_selector_1_found = False
        node_selector_2_found = False
        for line in result_list:
            if "- --updated" in line:
                args_found = True
            if "MODS: UPDATED" in line:
                mods_found = True
            if "OTHER: VALUE" in line:
                other_found = True
            if "kubernetes.io/arch: amd64" in line:
                prev_node_selector_not_found = False
            if "x/y: a-b" in line:
                node_selector_1_found = True
            if "x/z: a-c" in line:
                node_selector_2_found = True
        assert args_found
        assert mods_found
        assert other_found
        assert node_selector_1_found
        assert node_selector_2_found
        assert prev_node_selector_not_found

    def test_deployment_clear_env_args_node_selectors(self, setup_login: None) -> None:
        # Update the deployments and clear env/args/node_selectors
        assert (
            os.system(
                "aioli deployment update "
                "iris-tf-keras-deployment-2 "
                "--env "
                "--arg "
                "--node-selector"
            )
            == 0
        )

        result = subprocess.check_output(
            ["aioli", "deployment", "show", "iris-tf-keras-deployment-2"]
        ).decode("utf-8")
        result_list = result.split("\n")
        args_not_found = True
        mods_not_found = True
        other_not_found = True
        node_selector_1_not_found = True
        node_selector_2_not_found = True
        for line in result_list:
            if "- --updated" in line:
                args_not_found = False
            if "MODS: UPDATED" in line:
                mods_not_found = False
            if "OTHER: VALUE" in line:
                other_not_found = False
            if "x/y: a-b" in line:
                node_selector_1_not_found = False
            if "x/z: a-c" in line:
                node_selector_2_not_found = False
        assert args_not_found
        assert mods_not_found
        assert other_not_found
        assert node_selector_1_not_found
        assert node_selector_2_not_found

    def test_deployment_delete(self, setup_login: None) -> None:
        assert os.system("aioli deployment delete iris-tf-keras-deployment") == 0
        assert os.system("aioli deployment delete iris-tf-keras-deployment-2") == 0

    def test_model_delete(self, setup_login: None) -> None:
        assert os.system("aioli model delete iris-tf-keras1") == 0

        # Test that a model with multiple versions cannot be deleted by only name
        assert os.system("aioli model delete iris-tf-keras") != 0

        assert os.system("aioli model delete iris-tf-keras.v1") == 0
        assert os.system("aioli model delete iris-tf-keras.v2") == 0
        assert os.system("aioli model delete iris-tf-keras.v3") == 0
        assert os.system("aioli model delete iris-tf-keras-v4.v1") == 0

    def test_registry_delete(self, setup_login: None) -> None:
        # Delete the registry entry
        assert os.system("aioli registry delete bento-registry1") == 0

    def test_user_list(self, setup_login: None) -> None:
        # Test the user table header fields
        assert os.system("aioli user list") == 0
        expected = "admin      | Default Administrator | True     | False    | default"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_user_list_json_yaml(self, setup_login: None) -> None:
        expected = (
            "[\n"
            "  {\n"
            '    "active": true,\n'
            '    "displayName": "Default Administrator",\n'
            '    "id": "1",\n'
            '    "remote": false,\n'
            '    "username": "admin"\n'
            "  }\n"
            "]\n"
        )

        expected = json.loads(expected)

        actual = json.loads(
            subprocess.check_output(["aioli", "user", "list", "--json"]).decode("utf-8")
        )
        for d in actual:
            del d["lastAuthAt"]
            del d["modifiedAt"]
            # defaultProject should exist, but will be a different UUID each time
            defaultProject = d["defaultProject"]
            del d["defaultProject"]
            assert uuid.UUID(defaultProject)
        assert actual == expected

        actual = yaml.safe_load(
            subprocess.check_output(["aioli", "user", "list", "--yaml"]).decode("utf-8")
        )
        for d in actual:
            del d["lastAuthAt"]
            del d["modifiedAt"]
            # defaultProject should exist, but will be a different UUID each time
            defaultProject = d["defaultProject"]
            del d["defaultProject"]
            assert uuid.UUID(defaultProject)
        assert actual == expected

    def test_user_list_csv(self, setup_login: None) -> None:
        csv_output = subprocess.check_output(["aioli", "user", "list", "--csv"]).decode("utf-8")
        temp_file: str = "/tmp/test-cli-u.csv"
        with open(temp_file, "w") as file:
            file.write(csv_output)
        with open(temp_file, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                assert row["Username"] == "admin", "Expected admin"
                assert (
                    row["Display Name"] == "Default Administrator"
                ), "Expected Default Administrator"
                assert row["Active"] == "True", "Expected True"
                assert row["Remote"] == "False", "Expected False"

    def test_user_create(self, setup_login: None) -> None:
        # create a user and test for expected values
        assert os.system("aioli user create testuser --password passwd") == 0
        expected = "testuser   |"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_user_update(self, setup_login: None) -> None:
        # update testuser and check for expected values
        assert (
            os.system(
                "aioli user update testuser --username newuser --display-name 'new display name'"
            )
            == 0
        )
        expected = "newuser    | new display name      | True"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0
        assert os.system("aioli user update newuser --username testuser --active f") == 0
        expected = "testuser   | new display name      | False"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_user_whoami(self, setup_login: None) -> None:
        assert os.system("aioli user whoami") == 0
        expected = "You are logged in as user 'admin'\n"
        actual = subprocess.check_output(["aioli", "user", "whoami"]).decode("utf-8")
        assert actual == expected

    def test_user_activate(self, setup_login: None) -> None:
        # Check activate feature
        assert os.system("aioli user activate testuser") == 0

    def test_user_deactivate(self, setup_login: None) -> None:
        # Check deactivate feature
        assert os.system("aioli user deactivate testuser") == 0

    def test_user_create_remote(self, setup_login: None) -> None:
        # create a remote user and test for expected values
        assert os.system("aioli user create --remote testuser-r") == 0
        expected = "testuser-r |                       | True     | True"
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_user_delete(self, setup_login: None) -> None:
        assert os.system("aioli user create testuser2 --password passwd") == 0
        # Delete user and test for expected values
        assert os.system("aioli user delete testuser2") == 0
        actual = subprocess.check_output(["aioli", "user", "list"]).decode("utf-8")
        expected = "testuser2"
        assert (actual.find(expected)) < 0  # Expect to be not found

    def test_template_resource_create_and_update(self, setup_login: None) -> None:
        # Create a resource template
        assert (
            os.system(
                "aioli template resource create my-template "
                '--description "My test reource template" '
                "--gpu-type nvidia "
                "--limits-cpu 10 "
                "--limits-memory 10Gi "
                "--limits-gpu 4 "
                "--requests-cpu 0 "
                "--requests-memory 10Gi "
                "--requests-gpu 4 "
            )
            == 0
        )

        expected = (
            "my-template | My test reource template               | Request: 0, Limit: 10 |"
            " Request: 10Gi, Limit: 10Gi | Request: 4, Limit: 4 | nvidia"
        )
        actual = subprocess.check_output(["aioli", "template", "resource", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

        # Make an update where gpu_type remains unchanged
        assert (
            os.system(
                "aioli template resource update my-template "
                '--description "My updated test resource template" '
                "--limits-cpu 5 "
                "--limits-memory 100Gi "
                "--limits-gpu 0 "
                "--requests-cpu 5 "
                "--requests-memory 100Gi "
                "--requests-gpu 0 "
            )
            == 0
        )

        expected = (
            "my-template | My updated test resource template      | Request: 5, Limit: 5  |"
            " Request: 100Gi, Limit: 100Gi | Request: 0, Limit: 0 | nvidia"
        )
        actual = subprocess.check_output(["aioli", "template", "resource", "list"]).decode("utf-8")
        assert (actual.find(expected)) > 0

    def test_template_autoscaling_create_and_update(self, setup_login: None) -> None:
        # Create a resource template
        assert (
            os.system(
                "aioli template autoscaling create my-template "
                '--description "My test autoscaling template" '
                "--autoscaling-min-replicas 0 "
                "--autoscaling-max-replicas 2 "
                "--autoscaling-metric rps "
                "--autoscaling-target 25 "
            )
            == 0
        )

        expected = (
            "my-template                | My test autoscaling template            "
            "                       |"
            "             0 |             2 | rps         |       25"
        )
        actual = subprocess.check_output(["aioli", "template", "autoscaling", "list"]).decode(
            "utf-8"
        )
        assert (actual.find(expected)) > 0

        # Make an update where autoscaling_metric remains unchanged
        assert (
            os.system(
                "aioli template autoscaling update my-template "
                '--description "My updated test autoscaling template" '
                "--autoscaling-min-replicas 2 "
                "--autoscaling-max-replicas 2 "
                "--autoscaling-target 50 "
            )
            == 0
        )

        expected = (
            "my-template                | My updated test autoscaling template              "
            "             |             2 |             2 | rps         |       50"
        )

        actual = subprocess.check_output(["aioli", "template", "autoscaling", "list"]).decode(
            "utf-8"
        )
        assert (actual.find(expected)) > 0

    def test_template_resource_show(self, setup_login: None) -> None:
        assert os.system("aioli template resource show my-template") == 0

        expected = yaml.safe_load(
            "description: My updated test resource template\n"
            "name: my-template\n"
            "resources:\n"
            "  gpuType: nvidia\n"
            "  limits:\n"
            "    cpu: '5'\n"
            "    gpu: '0'\n"
            "    memory: 100Gi\n"
            "  requests:\n"
            "    cpu: '5'\n"
            "    gpu: '0'\n"
            "    memory: 100Gi\n"
        )
        actual = yaml.safe_load(
            subprocess.check_output(["aioli", "template", "resource", "show", "my-template"])
        )
        del actual["modifiedAt"]
        assert actual == expected

    def test_template_autoscaling_show(self, setup_login: None) -> None:
        assert os.system("aioli template autoscaling show my-template") == 0

        expected = yaml.safe_load(
            "autoScaling:\n"
            "  maxReplicas: 2\n"
            "  metric: rps\n"
            "  minReplicas: 2\n"
            "  target: 50\n"
            "description: My updated test autoscaling template\n"
            "name: my-template\n"
        )
        actual = yaml.safe_load(
            subprocess.check_output(["aioli", "template", "autoscaling", "show", "my-template"])
        )
        del actual["modifiedAt"]
        assert actual == expected

    def test_template_resource_delete(self, setup_login: None) -> None:
        assert os.system("aioli template resource delete my-template") == 0

    def test_template_autoscaling_delete(self, setup_login: None) -> None:
        assert os.system("aioli template autoscaling delete my-template") == 0
