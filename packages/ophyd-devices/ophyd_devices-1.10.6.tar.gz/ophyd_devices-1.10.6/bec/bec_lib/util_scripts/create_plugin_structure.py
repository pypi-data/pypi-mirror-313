"""
Helper script to create a new plugin structure
"""

import os
import sys

import yaml

# current directory:
current_dir = os.path.dirname(os.path.realpath(__file__))


class PluginStructure:
    """
    Example usage. Run this script with the target directory as an argument
    It will then automatically create the plugin structure in the target directory

    >>> python create_plugin_structure.py /path/to/my_plugin
    """

    def __init__(self, target_dir):
        """This class can be used to produce the folder structure
        of BEC. This includes copying templates for the structures
        """
        self.target_dir = target_dir
        _, self.plugin_name = os.path.split(target_dir)
        self.create_dir("")

    def create_dir(self, dir_name):
        os.makedirs(os.path.join(self.target_dir, dir_name), exist_ok=True)

    def create_init_file(self, dir_name):
        init_file = os.path.join(self.target_dir, dir_name, "__init__.py")
        with open(init_file, "w", encoding="utf-8") as f:
            f.write("")

    def copy_plugin_setup_files(self):
        # copy setup files
        self.copy_toml_file()
        git_hooks = os.path.join(current_dir, "plugin_setup_files", "git_hooks/*")
        self.create_dir(".git_hooks")
        os.system(f"cp -R {git_hooks} {self.target_dir}/.git_hooks/")
        gitignore = os.path.join(current_dir, "plugin_setup_files", "gitignore")
        os.system(f"cp {gitignore} {self.target_dir}/.gitignore")

        # copy license
        repo_license = os.path.join(current_dir, "plugin_setup_files", "plugin_repo_cliense.md")
        os.system(f"cp {repo_license} {self.target_dir}/LICENSE")

    def copy_toml_file(self):
        """Copy the toml file and change the template name in the file"""
        # copy toml file
        toml_file = os.path.join(current_dir, "plugin_setup_files", "pyproject.toml")
        with open(toml_file, "r", encoding="utf-8") as f:
            toml_template_str = f.read()
        # change template name in toml file
        toml_template_str = toml_template_str.replace("{template_name}", self.plugin_name)

        toml_file = os.path.join(self.target_dir, "pyproject.toml")
        # write toml file
        with open(toml_file, "w", encoding="utf-8") as f:
            f.write(toml_template_str)

    def add_plugins(self):
        self.create_dir(self.plugin_name)
        self.create_init_file(self.plugin_name)

    def add_scans(self):
        self.create_dir(f"{self.plugin_name}/scans")
        self.create_init_file(f"{self.plugin_name}/scans")

        # copy scan_plugin_template.py
        scan_plugin_template_file = os.path.join(
            current_dir, "plugin_setup_files", "scan_plugin_template.py"
        )
        os.system(f"cp {scan_plugin_template_file} {self.target_dir}/{self.plugin_name}/scans")

    def add_client(self):
        self.create_dir(f"{self.plugin_name}/bec_ipython_client")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client")

        # high level interface
        self.create_dir(f"{self.plugin_name}/bec_ipython_client/high_level_interface")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client/high_level_interface")

        # plugins
        self.create_dir(f"{self.plugin_name}/bec_ipython_client/plugins")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client/plugins")

        # startup
        self.create_dir(f"{self.plugin_name}/bec_ipython_client/startup")
        self.create_init_file(f"{self.plugin_name}/bec_ipython_client/startup")

        ## copy pre_startup.py
        pre_startup_file = os.path.join(current_dir, "plugin_setup_files", "pre_startup.py")
        os.system(
            f"cp {pre_startup_file} {self.target_dir}/{self.plugin_name}/bec_ipython_client/startup"
        )
        ## copy post_startup.py
        post_startup_file = os.path.join(current_dir, "plugin_setup_files", "post_startup.py")
        os.system(
            f"cp {post_startup_file} {self.target_dir}/{self.plugin_name}/bec_ipython_client/startup"
        )

    def add_devices(self):
        self.create_dir(f"{self.plugin_name}/devices")
        self.create_init_file(f"{self.plugin_name}/devices")
        # device template?

    def add_device_configs(self):
        self.create_dir(f"{self.plugin_name}/device_configs")
        self.create_init_file(f"{self.plugin_name}/device_configs")

    def add_services(self):
        self.create_dir(f"{self.plugin_name}/services")
        self.create_init_file(f"{self.plugin_name}/services")

    def add_bec_widgets(self):
        self.create_dir(f"{self.plugin_name}/bec_widgets")
        self.create_init_file(f"{self.plugin_name}/bec_widgets")

        self.create_dir(f"{self.plugin_name}/bec_widgets/configs")
        self.create_dir(f"{self.plugin_name}/bec_widgets/widgets")
        self.create_init_file(f"{self.plugin_name}/bec_widgets/widgets")

    def add_file_writer(self):
        self.create_dir(f"{self.plugin_name}/file_writer")
        self.create_init_file(f"{self.plugin_name}/file_writer")

    def add_deployments(self):
        self.create_dir(f"{self.plugin_name}/deployments")
        self.create_init_file(f"{self.plugin_name}/deployments")
        self.create_dir(f"{self.plugin_name}/deployments/device_server")
        self.create_init_file(f"{self.plugin_name}/deployments/device_server")

        ds_startup = os.path.join(current_dir, "plugin_setup_files", "setup_device_server.py")
        os.system(
            f"cp {ds_startup} {self.target_dir}/{self.plugin_name}/deployments/device_server/startup.py"
        )

    def add_gitlab_ci(self):
        out = {
            "include": [
                {
                    "project": "bec/awi_utils",
                    "file": "/templates/plugin-repo-template.yml",
                    "inputs": {"name": self.plugin_name, "target": self.plugin_name},
                }
            ]
        }
        with open(os.path.join(self.target_dir, ".gitlab-ci.yml"), "w", encoding="utf-8") as f:
            yaml.dump(out, f)

    def add_tests(self):
        self.create_dir("tests/tests_bec_ipython_client")
        self.copy_tests_readme("tests/tests_bec_ipython_client")
        self.create_dir("tests/tests_dap_services")
        self.copy_tests_readme("tests/tests_dap_services")
        self.create_dir("tests/tests_bec_widgets")
        self.copy_tests_readme("tests/tests_bec_widgets")
        self.create_dir("tests/tests_devices")
        self.copy_tests_readme("tests/tests_devices")
        self.create_dir("tests/tests_scans")
        self.copy_tests_readme("tests/tests_scans")
        self.create_dir("tests/tests_file_writer")
        self.copy_tests_readme("tests/tests_file_writer")

    def copy_tests_readme(self, file_path: str):
        readme_file = os.path.join(current_dir, "plugin_setup_files", "README_template_tests.md")
        os.system(f"cp {readme_file} {self.target_dir}/{file_path}/README.md")

    def add_bin(self):
        self.create_dir("bin")


if __name__ == "__main__":
    struc = PluginStructure(sys.argv[1])
    struc.add_plugins()
    struc.copy_plugin_setup_files()
    struc.add_scans()
    struc.add_client()
    struc.add_devices()
    struc.add_device_configs()
    struc.add_services()
    struc.add_bec_widgets()
    struc.add_file_writer()
    struc.add_tests()
    struc.add_bin()
    struc.add_deployments()
    struc.add_gitlab_ci()

    print(f"Plugin structure created in {sys.argv[1]}")
