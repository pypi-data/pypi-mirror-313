#!python

# Run this *in* the RAFT directory, or bad things will happen (or nothing at all).

import cmd
import argparse
import google.cloud
from glob import glob
import hashlib
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import tarfile
import time
import wget
from os.path import join as pjoin
from os import getcwd

from git import Repo
import gitlab

import base64


def get_args():
    """
    Collecting user-defined arguments.
    """
    parser = argparse.ArgumentParser(prog="RAFT",
                                     description="""Reproducible
                                                    Analyses
                                                    Framework
                                                     and
                                                    Tools""")

    subparsers = parser.add_subparsers(dest='command')

    # Subparser for initial RAFT setup.
    parser_setup = subparsers.add_parser('setup',
                                         help="""RAFT setup and configuration.""")
    parser_setup.add_argument('-d', '--default',
                              help="Use default paths for setup.",
                              action='store_true',
                              default=False)

    # Subparser for initializing a project.
    parser_init_project = subparsers.add_parser('init-project',
                                                help="Initialize a RAFT project.")
    parser_init_project.add_argument('-c', '--init-config',
                                     help="Project config file (see documentation).",
                                     default=pjoin(getcwd(), '.init.cfg'))
    parser_init_project.add_argument('-p', '--project-id',
                                     help="Project identifier",
                                     required=True)
    parser_init_project.add_argument('-r', '--repo-url',
                                     help="Git repo url for remote pushing/pulling.",
                                     default='')

    # Subparser for loading reference files/dirs into a project.
    parser_load_reference = subparsers.add_parser('load-reference',
                                                  help="Loads ref files/dirs into a project.")
    parser_load_reference.add_argument('-f', '--file',
                                       help="Reference file or directory (see documentation).",
                                       required=True)
    parser_load_reference.add_argument('-s', '--sub-dir',
                                       help="Subdir for reference file or directory witin project.",
                                       default='')
    parser_load_reference.add_argument('-p', '--project-id',
                                       help="Project identifier",
                                       required=True)
    parser_load_reference.add_argument('-m', '--mode',
                                       help="Mode (copy or symlink). Default: symlink",
                                       default='symlink')

    # Subparser for loading metadata into a project.
    parser_load_metadata = subparsers.add_parser('load-metadata',
                                                 help="Loads metadata into a project.")
    parser_load_metadata.add_argument('-f', '--file',
                                      help="Metadata file. Check docs for more info.",
                                      required=True)
    parser_load_metadata.add_argument('-s', '--sub-dir',
                                      help="Subdir for metadata file within project.", default='')
    parser_load_metadata.add_argument('-p', '--project-id',
                                      help="Project identifier.",
                                      required=True)
    parser_load_metadata.add_argument('-m', '--mode',
                                      help="Mode (copy or symlink). Default: copy",
                                      default='symlink')

    # Subparser for loading component into a project.
    parser_load_module = subparsers.add_parser('load-module',
                                               help="Clones Nextflow module into project.")
    parser_load_module.add_argument('-p', '--project-id',
                                    help="Project identifier",
                                    required=True)
    parser_load_module.add_argument('-r', '--repo',
                                    help="Module repository.",
                                    default='')
    parser_load_module.add_argument('-m', '--module',
                                    help="Module to add to project.",
                                    required=True)
    # Need support for commits and tags here as well.
    parser_load_module.add_argument('-b', '--branches',
                                    help="Branches to checkout per module (see documentation). Default='main'.",
                                    default='prod')
    parser_load_module.add_argument('-n', '--no-deps',
                                    help="Do not automatically load dependencies.",
                                    default=False)
    parser_load_module.add_argument('-d', '--delay',
                                    help="Delay (in seconds) before git pulls. (Default = 15s).",
                                    default=5)
    parser_load_module.add_argument('--silent',
                                    help="No notifications",
                                    default=False)

    # Subparser for listing module steps.
    parser_list_steps = subparsers.add_parser('list-steps',
                                              help="List module's processes and workflows.")
    parser_list_steps.add_argument('-p', '--project-id',
                                   help="Project identifier",
                                   required=True)
    parser_list_steps.add_argument('-m', '--module',
                                   help="Module")
    parser_list_steps.add_argument('-s', '--step',
                                   help="Step")

    # Subparser for updating project-specific mounts.config file.
    parser_update_mounts = subparsers.add_parser('update-mounts',
                                                 help="""Updates project-specific mounts.config
                                                         file with symlinks found in a directory.""")
    parser_update_mounts.add_argument('-p', '--project-id',
                                      help="Project identifier",
                                      required=True)
    parser_update_mounts.add_argument('-d', '--dir',
                                      help="Directory containing symlinks for mounts.config.",
                                      required=True)

    # Subparser for adding a step into workflow step of a project.
    parser_add_step = subparsers.add_parser('add-step',
                                            help="""Add step (process/workflow) to project
                                                    (see documentation).""")
    parser_add_step.add_argument('-p', '--project-id',
                                 help="Project identifier",
                                 required=True)
    parser_add_step.add_argument('-m', '--module',
                                 help="Module containing step (process/workflow).",
                                 required=True)
    parser_add_step.add_argument('-s', '--step',
                                 help="Process/workflow to add.",
                                 required=True)
    parser_add_step.add_argument('-S', '--subworkflow',
                                 help="Subworkflow to add step to (default: main)",
                                 default='main')
    parser_add_step.add_argument('-a', '--alias',
                                 help="Assign an alias to step.",
                                 default='')
    parser_add_step.add_argument('--silent',
                                 help="No notifications",
                                 default=False,
                                 action='store_true')

    # Subparser for running workflow.
    parser_run_workflow = subparsers.add_parser('run-workflow',
                                                help="Run workflow.")
    parser_run_workflow.add_argument('--no-resume',
                                     help="Do not use Nextflow's -resume functionality.",
                                     default=False,
                                     action='store_true')
    parser_run_workflow.add_argument('-w', '--workflow',
                                     help="Workflow to run (default: main).",
                                     default='main')
    parser_run_workflow.add_argument('-n', '--nf-params',
                                     help="Parameter string passed to Nextflow (see documentation).")
    parser_run_workflow.add_argument('-p', '--project-id',
                                     help="Project identifier",
                                     required=True)
    parser_run_workflow.add_argument('-k', '--keep-previous-outputs',
                                     help="Do not remove previous run's outputs before running.",
                                     action='store_true')
    parser_run_workflow.add_argument('-r', '--no-reports',
                                     help="Do not create report files.",
                                     action='store_true')
    parser_run_workflow.add_argument('--show-all-processes',
                                     help="Show all running processes.",
                                     action='store_true')
    parser_run_workflow.add_argument('--cloud', '-c',
                                     help="Replace local RAFT directories with cloud buckets.",
                                     default=False)

    # Subparser for packaging project (to generate sharable rftpkg tar file)
    parser_package_project = subparsers.add_parser('package-project',
                                                   help="Package project (see documentation).")
    parser_package_project.add_argument('-p', '--project-id',
                                        help="Project identifier")
    parser_package_project.add_argument('-o', '--output',
                                        help="Output file.",
                                        default='')
    parser_package_project.add_argument('-n', '--no-git',
                                        help="Do not include Git files.",
                                        default=False,
                                        action='store_true')
    parser_package_project.add_argument('-c', '--no-checksums',
                                        help="Do not include checksums.",
                                        default=False,
                                        action='store_true')

    # Subparser for loading package (after receiving rftpkg tar file)
    parser_load_project = subparsers.add_parser('load-project',
                                                help="Load project (see documentation).")
    parser_load_project.add_argument('-p', '--project-id', help="Project identifier")
    parser_load_project.add_argument('-r', '--rftpkg', help="rftpkg file")
    parser_load_project.add_argument('--repo-url', help="Git repo url.")
    parser_load_project.add_argument('--branch', help="Git repo branch.", default='main')

    # Subparser for pushing package
    parser_push_project = subparsers.add_parser('push-project',
                                                help="Push project to repo (see documentation).")
    parser_push_project.add_argument('-p', '--project-id', help="Project identifier")
    parser_push_project.add_argument('-r', '--rftpkg', help="rftpkg file.")
    parser_push_project.add_argument('--repo', help="Repo push to.")
    parser_push_project.add_argument('-c', '--comment', help="Commit comment.")
    parser_push_project.add_argument('-b', '--branch', help="Git branch.")

    # Subparser for pulling package from repo
    parser_pull_project = subparsers.add_parser('pull-project',
                                                help="Pull project from repo (see documentation).")
    parser_pull_project.add_argument('-p', '--project-id', help="Project identifier")
    parser_pull_project.add_argument('-r', '--rftpkg', help="rftpkg file")

    parser_update_modules = subparsers.add_parser('update-modules',
                                                  help="Pull the latest commits for each module.")
    parser_update_modules.add_argument('-p', '--project-id', help="Project identifier")
    parser_update_modules.add_argument('-m', '--modules',
                                       help="List of modules to update (Default = all)",
                                       default='')
    parser_update_modules.add_argument('-d', '--delay',
                                       help="Delay (in seconds) before git pulls. (Default = 15s).",
                                       default=15)

    parser_rename_project = subparsers.add_parser('rename-project',
                                                  help="Rename a project.")
    parser_rename_project.add_argument('-p', '--project-id', help="Project identifier")
    parser_rename_project.add_argument('-n', '--new-id', help="New project identifier")

    # Subparser for cleaning work directories associated with a project.
    parser_clean_project = subparsers.add_parser('clean-project',
                                                 help="Remove failed/aborted work directories for a project.")
    parser_clean_project.add_argument('-p', '--project-id', help="Project.")
    parser_clean_project.add_argument('-k', '--keep-latest',
                                      help="Keep only directories from latest successful run.",
                                      action='store_true',
                                      default=False)
    parser_clean_project.add_argument('-n', '--no-exec',
                                      help="Provide latest/completed/cleanable work directory counts but do NOT delete.",
                                      action='store_true',
                                      default=False)

    # Subparser for copying parameters between projects or from a config file.
    parser_copy_params = subparsers.add_parser('copy-parameters',
                                               help="Copy parameters between projects or from a configuration file.")
    parser_copy_params.add_argument('-s', '--source-project',
                                    help="Source project identifier")
    parser_copy_params.add_argument('-d', '--dest-project',
                                    help="Destination project identifier")
    parser_copy_params.add_argument('-c', '--source-config',
                                    help="Source configuration file (to copy parameters from)")
    parser_copy_params.add_argument('--silent',
                                    help="No notifications",
                                    default=False)

    # Subparser for running an off-the-shelf workflow on a user-provided manifest
    parser_run_ots = subparsers.add_parser('run-ots',
                                               help="Run an off-the-shelf workflow on a user-provided manifest.")
    parser_run_ots.add_argument('-p', '--project-id',
                                    help="Project identifier",
                                    required=True)
    parser_run_ots.add_argument('-w', '--workflow',
                                    help="Off-the-shelf workflow to run",
                                    required=True)
    parser_run_ots.add_argument('-v', '--version',
                                    help="Workflow version to run",
                                    default="latest")
    parser_run_ots.add_argument('-m', '--manifest',
                                    help="RAFT Manifest",
                                    required=True)
    parser_run_ots.add_argument('-s', '--species',
                                    default='human',
                                    help="Species")
    parser_run_ots.add_argument('-up', '--user-params',
                                    nargs='+',
                                    action='append',
                                    help="User-provided parameters. Provide once per parameter.")
    parser_run_ots.add_argument('-d', '--input-data',
                                    default='fastqs',
                                    help="Input data (fastqs, processed fastqs, bams, etc.)")
    parser_run_ots.add_argument('--setup-only',
                                    help="Only set up the project, but do not run it.",
                                    action='store_true',
                                    default=False)
    parser_run_ots.add_argument('--debug',
                                    default=False,
                                    action='store_true',
                                    help="Debug mode")
    parser_run_ots.add_argument('--show-all-processes',
                                     help="Show all running processes.",
                                     action='store_true')
    parser_run_ots.add_argument('--cloud', '-c',
                                     help="Replace local RAFT directories with cloud buckets.",
                                     default=False)
    parser_run_ots.add_argument('-r', '--no-reports',
                                     help="Do not create report files.",
                                     action='store_true')

    # Subparser for running an off-the-shelf workflow on a user-provided manifest
    parser_run_demo = subparsers.add_parser('run-demo',
                                            help="Demonstrate an off-the-shelf workflow on a user-provided manifest.")
    parser_run_demo.add_argument('-p', '--project-id',
                                    help="Project identifier",
                                    default="default-demo")
    parser_run_demo.add_argument('-w', '--workflow',
                                    help="Off-the-shelf workflow to run",
                                    required=True)
    parser_run_demo.add_argument('-v', '--version',
                                    help="Workflow branch to pull",
                                    default="latest")
    parser_run_demo.add_argument('-m', '--manifest',
                                    help="RAFT Manifest",
                                    default='demo')
    parser_run_demo.add_argument('-s', '--species',
                                    default='human',
                                    help="Species")
    parser_run_demo.add_argument('-d', '--input-data',
                                    default='demo',
                                    help="Input data (fastqs, processed fastqs, bams, etc.)")
    parser_run_demo.add_argument('--setup-only',
                                    help="Only set up the project, but do not run it.",
                                    action='store_true',
                                    default=False)
    parser_run_demo.add_argument('--debug',
                                    default=False,
                                    action='store_true',
                                    help="Debug mode")
    parser_run_demo.add_argument('-up', '--user-params',
                                    nargs='+',
                                    action='append',
                                    help="User-provided parameters. Provide once per parameter.")
    parser_run_demo.add_argument('--show-all-processes',
                                    help="Show all running processes.",
                                    action='store_true')
    parser_run_demo.add_argument('--cloud', '-c',
                                     help="Replace local RAFT directories with cloud buckets.",
                                     default=False)
    parser_run_demo.add_argument('-r', '--no-reports',
                                     help="Do not create report files.",
                                     action='store_true')

    # Subparser for listing available off-the-shelf workflows
    parser_list_ots = subparsers.add_parser('available-workflows',
                                            help="List available off-the-shelf workflows.")
    parser_list_ots.add_argument('-wf', '--workflow',
                                 default='')
    parser_list_ots.add_argument('-s', '--species',
                                 default='human')
    parser_list_ots.add_argument('-i', '--input',
                                 default='')

    # Subparser for listing available modules
    parser_list_mods = subparsers.add_parser('available-modules',
                                            help="List available modules.")

    # Subparser for running an off-the-shelf workflow on a user-provided manifest
    parser_chk_mani = subparsers.add_parser('check-manifest',
                                               help="Check manifest for RAFT compatibility.")
    parser_chk_mani.add_argument('-m', '--manifest',
                                    help="Manifest file to check")

    return parser.parse_args()


def setup(args):
    """
    Part of the setup mode.

    Installs RAFT into current working directory.
    Installation consists of:

        - Moving any previously generated RAFT configuration files.

        #Paths
        - Prompting user for paths for paths shared amongst analyses (if not using -d/--default).

        #NF Repos
        - Prompting user for git urls for module-level repositories.

        #RAFT Repos
        - Prompting user for git urls for RAFT-specific repositories (storing rftpkgs).

        #Saving
        - Saving these urls in a JSON format in ${PWD}/.raft.cfg

        #Executing
        - Making the required shared paths.
        - Checking out RAFT-specific repositories to repos directory specific in cfg.

    Args:
        # This requires more information. What are the keys of this object?
        args (Namespace object): User-provided arguments.
    """
    print("Setting up RAFT...\n")
    if args.default:
        print("Using defaults due to -d/--default flag...")

    # DEFAULTS
    raft_paths = {'projects': pjoin(getcwd(), 'projects'),
                  'references': pjoin(getcwd(), 'references'),
                  'fastqs': pjoin(getcwd(), 'fastqs'),
                  'bamss': pjoin(getcwd(), 'bams'),
                  'imgs': pjoin(getcwd(), 'imgs'),
                  'metadata': pjoin(getcwd(), 'metadata'),
                  'shared': pjoin(getcwd(), 'shared')}

    init_cfg = {"references": "",
                "fastqs": "",
                "bamss": "",
                "tmp": "",
                "outputs": "",
                "workflow": "",
                "work": "",
                "metadata": "",
                "logs": "",
                "rftpkgs": "",
                ".raft": ""}

    with open(pjoin(getcwd(), '.init.cfg'), 'w', encoding='utf8') as init_cfg_fo:
        json.dump(init_cfg, init_cfg_fo)

    with open(pjoin(getcwd(), '.init.wf'), 'w', encoding='utf8') as init_wf_fo:
        init_wf_fo.write('#!/usr/bin/env nextflow\n')
        init_wf_fo.write('nextflow.enable.dsl=2\n')
        init_wf_fo.write('\n')
        init_wf_fo.write('/*Parameters*/\n')
        init_wf_fo.write("params.project_dir = ''\n")
        init_wf_fo.write('params.fq_dir = "${params.project_dir}/fastqs"\n')
        init_wf_fo.write("params.global_fq_dir = ''\n")
        init_wf_fo.write("params.global_bam_dir = ''\n")
        init_wf_fo.write("params.shared_dir = ''\n")
        init_wf_fo.write('params.metadata_dir = "${params.project_dir}/metadata"\n')
        init_wf_fo.write('params.ref_dir = "${params.project_dir}/references"\n')
        init_wf_fo.write('params.output_dir = "${params.project_dir}/outputs"\n')
        init_wf_fo.write('params.dsp_output_dir = "${params.output_dir}/dataset_prep"\n')
        init_wf_fo.write('params.analyses_dir = "${params.output_dir}/analyses"\n')
        init_wf_fo.write('params.gene_sigs_dir = "${params.output_dir}/gene_signatures"\n')
        init_wf_fo.write('params.samps_out_dir = "${params.output_dir}/samples"\n')
        init_wf_fo.write('params.qc_out_dir = "${params.output_dir}/qc"\n')
        init_wf_fo.write('params.dummy_file = ""\n')
        init_wf_fo.write('params.prnt_docs = ""\n')
        init_wf_fo.write('\n')
        init_wf_fo.write('/*Inclusions*/\n')
        init_wf_fo.write('\n')
        init_wf_fo.write('/*Workflows*/\n')
        init_wf_fo.write('\n')
        init_wf_fo.write('workflow {\n')
        init_wf_fo.write('}\n')

    with open(pjoin(getcwd(), '.nextflow.config'), 'w', encoding='utf8') as nf_cfg_fo:
        nf_cfg_fo.write("manifest.mainScript = 'main.nf'\n")
        nf_cfg_fo.write("\n")
        nf_cfg_fo.write("process {\n")
        nf_cfg_fo.write("errorStrategy = 'retry'\n")
        nf_cfg_fo.write("maxRetries = 3\n")
        nf_cfg_fo.write("}\n")


#    git_prefix = 'https://gitlab.com/landscape-of-effective-neoantigens-software/nextflow'
    git_prefix = 'https://gitlab.com/reproducible-analyses-framework-and-tools/nextflow'
    nf_repos = {'nextflow_modules': pjoin(git_prefix, 'modules')}
#    nf_subs = {'nextflow_module_subgroups': ['Tools', 'Projects', 'Datasets']}
    nf_subs = {'nextflow_module_subgroups': ['tools', 'Projects', 'Datasets']}

    raft_repos = {}

    # Ideally, users should be able to specify where .raft.cfg lives but RAFT
    # needs an "anchor" for defining other directories.
    cfg_path = pjoin(getcwd(), '.raft.cfg')

    # Make backup of previous configuration file.
    if os.path.isfile(cfg_path):
        bkup_cfg_path = cfg_path + '.orig'
        print("A configuration file already exists.")
        print(f"Copying original to {bkup_cfg_path}.")
        os.rename(cfg_path, bkup_cfg_path)

    if not args.default:
        # Setting up filesystem paths.
        raft_paths = get_user_raft_paths(raft_paths)

        # Setting up Nextflow module repositories.
        nf_repos, nf_subs = get_user_nf_repos(nf_repos, nf_subs)

    master_cfg = {'filesystem': raft_paths,
                  'nextflow_repos': nf_repos,
                  'nextflow_subgroups': nf_subs,
                  'analysis_repos': raft_repos}

    print(f"Saving configuration file to {cfg_path}...")
    dump_cfg(cfg_path, master_cfg)

    print("Executing configuration file...")
    setup_run_once(master_cfg)

    print("Setup complete.")


def get_user_raft_paths(raft_paths):
    """
    Part of setup mode.

    NOTE: The language should really be cleared up here. Users should
    understand that the keys are simply names while the values are actual
    filesystem paths.

    Prompts user for desired path for directories to be shared among analyses
    (e.g. metadata, fastqs, etc.)

    Args:
        raft_paths (dict): Dictionary containing RAFT paths (e.g. indexes,
                           fastqs, etc.) as keys and the default path as
                           values.

    Returns:
        Dictionary containing RAFT paths as keys and user-specified directories as values.
    """
    for raft_path, default in raft_paths.items():
        user_spec_path = input(f"Provide a global (among projects) directory for {raft_path} (Default: {default}): ")
        # Should be doing some sanity checking here to ensure the path can exist.
        if user_spec_path:
            if re.search('~', user_spec_path):
                user_spec_path = os.path.realpath(os.path.expanduser(user_spec_path))
            raft_paths[raft_path] = user_spec_path
    return raft_paths


def get_user_nf_repos(nf_repos, nf_subs):
    """
    Part of setup mode.

    Prompts user for desired Nextflow reposities.

    Args:
        nf_repos (dict): Dictionary containing repo names as keys and git url as values.

    Returns:
        Dictionary containing repo names as keys and user-specific git urls as values.
    """
    # Allow users to specify their own Nextflow workflows and modules repos.
    for nf_repo, default in nf_repos.items():
        user_spec_repo = input(f"\nProvide a repository for Nextflow {nf_repo}\n(Default: {default}):")
        if user_spec_repo:
            nf_repos[nf_repo] = user_spec_repo

    # This should be in its own function.
    for nf_sub, default in nf_subs.items():
        user_spec_subs = input(f"\nProvide a comma separated list for Nextflow Module subgroups \n(Default: {default}):")
        if user_spec_subs:
            nf_subs[nf_sub] = user_spec_subs

    return nf_repos, nf_subs


def dump_cfg(cfg_path, master_cfg):
    """
    Part of setup mode.

    Writes configuration file to cfg_path.

    Args:
        cfg_path (str): Path for writing output file.
        master_cfg (dict): Dictionary containing configuration information.
    """
    with open(cfg_path, 'w', encoding='utf8') as cfg_fo:
        json.dump(master_cfg, cfg_fo, indent=4)


def setup_run_once(master_cfg):
    """
    Part of setup mode.

    Makes/symlinks directories in the 'filesystem' portion of configuration
    file. Clones/initializes any RAFT repositories.

    Args:
        master_cfg (dict): Dictionary with configuration information.
    """
    for directory in master_cfg['filesystem'].values():
        if os.path.isdir(directory): # Need to ensure directory isn't already in RAFT directory.
            print(f"Symlinking {directory} to {getcwd()}...")
            try:
                os.symlink(directory, pjoin(getcwd(), os.path.basename(directory)))
            except FileExistsError:
                print(f"{directory} already exists.")
        else:
            print(f"Making {directory}...")
            os.mkdir(directory)


def init_project(args):
    """
    Part of init-project mode.

    Initializes project.

    Initializing a project includes:
      - Make a project directory within RAFT /projects directory.
      - Populate project directory using information within specificed
        init_config file.
      - Make a mounts.config file to allow Singularity to access RAFT directories.
      - Make auto.raft file (which records steps taken within RAFT).
      - Create workflow/modules/ directory and project.nf overall workflow.

    Args:
        args (Namespace object): User-provided arguments
    """
    # Make project directory
    proj_dir = mk_proj_dir(args, args.project_id)
    # Populate project directory
    bound_dirs = fill_dir(args, proj_dir, args.init_config)
    # Make mounts.config
    mk_mounts_cfg(proj_dir, bound_dirs)
    # Make auto.raft
    mk_auto_raft(args)
    # Make main.nf and nextflow.config
    mk_main_wf_and_cfg(args)
    # Make local repo for storing .rftpkg files
    mk_repo(args)


def mk_repo(args):
    """
    Initialize a local Git repo for storing rftpkg files.

    Args:
        args (namespace object): User-defined arugments
    """
    raft_cfg = load_raft_cfg()
    local_repo = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'rftpkgs')
    repo = Repo.init(local_repo)
    if args.repo_url:
        repo.create_remote('origin', args.repo_url)


def mk_main_wf_and_cfg(args):
    """
    Part of the init-project mode.

    Copies default main.nf template and creates sparse nextflow.config.

    Args:
        args (Namespace object): User-provided arguments
    """
    raft_cfg = load_raft_cfg()
    tmplt_wf_file = os.path.join(os.getcwd(), '.init.wf')
    tmplt_cfg_file = os.path.join(os.getcwd(), '.nextflow.config')
    proj_wf_path = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow')
    with open(tmplt_wf_file, encoding='utf8') as origfo:
        with open(pjoin(proj_wf_path, 'main.nf'), 'w', encoding='utf8') as outfo:
            for line in origfo.readlines():
                if line == "params.project_dir = ''\n":
                    line = f"params.project_identifier = '{args.project_id}'\nparams.project_dir = ''\n"
                outfo.write(line)

    shutil.copyfile(tmplt_cfg_file, pjoin(proj_wf_path, 'nextflow.config'))

    # Adding Singularity info and making nextflow.config.
    imgs_dir = raft_cfg['filesystem']['imgs']
    cfg_out = ["manifest.mainScript = 'main.nf'\n\n"]
    cfg_out.append('singularity {\n')
    cfg_out.append(f'  cacheDir = "{imgs_dir}"\n')
    cfg_out.append("  autoMount = 'true'\n")
    cfg_out.append('}\n')

    with open(pjoin(proj_wf_path, 'nextflow.config'), encoding='utf8') as nf_cfg_fo:
        cfg_out.extend(nf_cfg_fo.readlines()[1:])
    proc_idx = cfg_out.index("process {\n")
    mounts_cfg_path = pjoin(proj_wf_path, 'mounts.config')
    cfg_out.insert(proc_idx + 1, f"containerOptions = '-B `cat {mounts_cfg_path}` --no-home'\n")

    with open(pjoin(proj_wf_path, 'nextflow.config'), 'w', encoding='utf8') as nf_cfg_fo:
        for row in cfg_out:
            nf_cfg_fo.write(row)


def mk_auto_raft(args):
    """
    Part of the init-project mode.

    Makes auto.raft file (within Analysis /.raft directory). auto.raft keeps
    track of RAFT commands executed within a project.

    Args:
        args (Namespace object): User-provided arguments
    """
    raft_cfg = load_raft_cfg()
    auto_raft_file = pjoin(raft_cfg['filesystem']['projects'],
                           args.project_id,
                           '.raft',
                           'auto.raft')

    with open(auto_raft_file, 'w', encoding='utf8') as auto_raft_fo:
        auto_raft_fo.write(f"{' '.join(sys.argv)}\n")


def mk_proj_dir(args, proj_id):
    """
    Part of the init-project mode.

    Makes the project directory within the RAFT /projects directory.

    Args:
        name (str): Project identifier.

    Returns:
        str containing the generated project path.
    """
    proj_dir = ''
    raft_cfg = load_raft_cfg()
    global_dir = raft_cfg['filesystem']['projects']
    proj_dir = pjoin(global_dir,proj_id)

#    if not(args.cloud):
    try:
        os.mkdir(proj_dir)
    except FileExistsError:
        sys.exit("Project directory already exists. Please try another.")
#    elif args.cloud.startswith('gs://'):
#        proj_dir = convert_path_to_bucket(args, proj_dir)
#        client = google.cloud.storage.Client()
#        bucket = client.bucket(proj_dir)
#        bucket.location = 'us'
#        bucket.create()

    return proj_dir


def fill_dir(args, directory, init_cfg):
    """
    Part of the init-project mode.

    Populates a project directory with template defined in init_cfg. Returns
    a list of directories to be included in the mounts.config file for the
    project.

    Args:
        args (Namespace object):
        dir (str): Project path.
        init_cfg (str): Initialization configuration path. File should be in
                        JSON format.

    Returns:
        bind_dirs (list): List of directories to be included in mounts.config
                           file.
    """
    # Getting the directories to be bound by this function as well. This should
    # probably be done a different way.
    bind_dirs = []
    raft_cfg = load_raft_cfg()
    req_sub_dirs = {}
    with open(init_cfg, encoding='utf8') as init_cfg_fo:
        req_sub_dirs = json.load(init_cfg_fo)
    for name, sdir in req_sub_dirs.items():
        # If the desired directory has an included path, link that path to
        # within the project directory. This should include some sanity
        # checking to ensure the sub_dir directory even exists.
        if sdir:
            os.symlink(sdir, pjoin(directory, name))
        # Else if the desired directory doesn't have an included path, simply
        # make a directory by that name within the project directory.
        elif not sdir:
            os.mkdir(pjoin(directory, name))
    bind_dirs.append(pjoin(raft_cfg['filesystem']['projects'], args.project_id))
#    bind_dirs.append(raft_cfg['filesystem']['work'])
    bind_dirs.append(getcwd())

    # Bindable directories are returned so they can be used to generate
    # mounts.config which allows Singularity (and presumably Docker) to bind
    # (and access) these directories.
    return bind_dirs


def mk_mounts_cfg(directory, bind_dirs):
    """
    Part of the init-project mode.

    Creates a mounts.config file for a project. This file is provided to
    Nextflow and used to bind directories during Singularity execution. This
    will have to be modified to use Docker, but works sufficiently for
    Singularity now.

    Args:
        directory (str): Project path.
        bind_dirs (list): Directories to be included in mounts.config file.
    """
    out = []
    out = ','.join(bind_dirs)

    with open(pjoin(directory, 'workflow', 'mounts.config'), 'w', encoding='utf8') as mnt_cfg_fo:
        mnt_cfg_fo.write(f'{out}')


def update_mounts_cfg(mounts_cfg, bind_dirs):
    """
    Part of update-mounts mode.

    Updates a mount.config file for a project.

    This is primarily intended to update the mount.config file with absolute
    paths for symlinked FASTQs, but can also be used generally.

    Args:
        mount_cfg (str): Path to mounts.config file to update.
        bind_dirs (list): Directories to be included in mounts.config file.
    """
    out = []
    with open(mounts_cfg, 'r', encoding='utf8') as ifo:
        line = ifo.readline()
        line = line.strip('\n')
        paths = line.split(',')
        bind_dirs_to_add = []
        for bind_dir in bind_dirs:
            if not any([bind_dir.startswith(path) for path in paths]):
                bind_dirs_to_add.append(bind_dir)
            for path in paths:
                if path.startswith(bind_dir):
                    paths.remove(path)
        paths.extend(bind_dirs_to_add)
        paths = ','.join(paths) + '\n'
        out.append(paths)

    with open(mounts_cfg, 'w', encoding='utf8') as mnt_cfg_fo:
        for row in out:
            mnt_cfg_fo.write(row)


def update_mounts(args):
    """
    Part of the update-mounts mode.

    This functions finds the real paths of all symlinks within the specified
    directory and adds them the the project-specific mounts.config file.

    Args:
        args (Namespace object)
    """
    raft_cfg = load_raft_cfg()
    bind_dirs = []
    to_check = glob(pjoin(os.path.abspath(args.dir), "**", "*"), recursive=True)
    for fle in to_check:
        bind_dirs.append(os.path.dirname(os.path.realpath(fle)))

    bind_dirs = list(set(bind_dirs))

    if bind_dirs:
        update_mounts_cfg(pjoin(raft_cfg['filesystem']['projects'],
                                args.project_id,
                                'workflow',
                                'mounts.config'),
                          bind_dirs)


def load_metadata(args):
    """
    Part of the load-metadata mode.

    NOTE: This is effectively load_samples without the sample-level checks.
          These can probably be easily consolidated.

    Given a user-provided metadata CSV file:
        - Copy/symlink file to project's /metadata directory.
        - Update project's mounts.config file if metadata file is symlinked.

    Args:
        args (Namespace object): User-provided arguments.
    """
    load_files(args, 'metadata')


def load_reference(args):
    """
    Part of load-reference mode.

    Given a user-provided reference file:
        - Copy/symlink reference file to project's /reference directory.
        - Update project's mounts.config file if reference file is symlinked.

    Args:
        args (Namespace object): User-provided arguments.
    """
    load_files(args, 'references')


def load_files(args, out_dir):
    """
    Generic loading/symlinking function for functions like load_metadata(), load_reference(), etc.

    Args:
        args (Namespace object): User-provided arguments.
        out_dir (str): Output directory for copied/symlinked file.

    """
    raft_cfg = load_raft_cfg()

    if not(os.path.isdir(pjoin(raft_cfg['filesystem']['projects'], args.project_id))):
        sys.exit("Cannot not find Project {} directory.".format(args.project_id))

    base = out_dir # output dir is input dir

    full_base = raft_cfg['filesystem'][base]

    globbed_files =  glob(pjoin(full_base, '**', args.file), recursive=True)
    if len(globbed_files) == 0:
        sys.exit(f"Cannot find {args.file} in {full_base}/**")
        # Put list of available references here.
    if len(globbed_files) > 1:
        sys.exit(f"File name {args.file} is not specific enough. Please provide a directory prefix.")
        # Put list of conflicting files here.
    globbed_file = globbed_files[0]

    abs_out_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, out_dir)
    if args.sub_dir and not os.path.exists(pjoin(abs_out_dir, args.sub_dir)):
        os.makedirs(pjoin(abs_out_dir, args.sub_dir))

    result_file = pjoin(abs_out_dir, args.sub_dir, os.path.basename(globbed_file))

    if os.path.exists(result_file):
        sys.exit(f"{result_file} already exists within the project. Ignoring load request.")
    elif args.mode == 'symlink':
        os.symlink(os.path.realpath(globbed_file),
                   result_file)

        update_mounts_cfg(pjoin(raft_cfg['filesystem']['projects'],
                                args.project_id,
                                'workflow',
                                'mounts.config'),
                          [os.path.realpath(globbed_file)])

    elif args.mode == 'copy':
        shutil.copyfile(os.path.realpath(globbed_file),
                        result_file)


def recurs_load_modules(args):
    """
    Recurively loads Nextflow modules. This occurs in multiple iterations such
    that each time a dependencies is loaded/cloned, another iteration is initated. This
    continues until an instance in which no new dependencies are loaded/cloned. There's
    probably a more intelligent way of doing this, but this should be able to
    handle the multiple layers of dependencies we're working with.

    Args:
        args (Namespace object): User-provided arguments.

    """
    raft_cfg = load_raft_cfg()
    wf_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow')
    new_deps = 1
    while new_deps == 1:
        new_deps = 0
        mods = glob(pjoin(wf_dir, '**', "{}.nf".format(args.module)), recursive=True)
        for mod in mods:
            deps = []
            with open(mod, encoding='utf8') as mfo:
                for line in mfo:
                    if re.search('^include.*nf.*', line):
                        dep = line.split()[-1].replace("'", '').split('/')[1]
                        # Adding the negative regex to avoid capturing /tests
                        # include statements.
                        if dep not in deps and not(re.search('.nf$', dep)):
                            deps.append(dep)
        if deps:
            for dep in deps:
                curr_deps = [i.split('/')[-1] for i in glob(pjoin(wf_dir, '*'))]
                if dep not in curr_deps:
                    new_deps = 1
                    spoofed_args = args
                    spoofed_args.module = dep
                    load_module(spoofed_args)


def list_steps(args):
    """
    List the process and workflows available from a Nextflow component.
    Requires project since it assumes users may modify componenets in a
    project-specific manner.

    Args:
       args (Namespace object): User-provided arguments
    """
    indexable_lines = []
    lois = {}
    output = []
    raft_cfg = load_raft_cfg()

    glob_term = '*/'
    if args.module:
        glob_term = args.module + '/'

    globbed_mods = glob(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', glob_term))
    for mod in globbed_mods:
        with open(pjoin(mod, mod.split('/')[-2] + '.nf'), encoding='utf8') as mod_fo:
            for line_idx, line in enumerate(mod_fo.readlines()):
                line = line.strip()
                indexable_lines.append(line)
                comment = ''
                if re.search('^workflow', line):
                    if not(args.step):
                        comment = f"module: {mod.split('/')[-2]}\ntype: workflow\nstep: {line.split(' ')[1]}"
                        lois[comment] = line_idx
                    elif args.step and re.search("{} ".format(args.step), line):
                        comment = f"module: {mod.split('/')[-2]}\ntype: workflow\nstep: {line.split(' ')[1]}"
                        lois[comment] = line_idx

                elif re.search('^process', line):
                    if not(args.step):
                        comment = f"module: {mod.split('/')[-2]}\ntype: process\nstep: {line.split(' ')[1]}"
                        lois[comment] = line_idx
                    elif args.step and re.search("{} ".format(args.step), line):
                        comment = f"module: {mod.split('/')[-2]}\ntype: process\nstep: {line.split(' ')[1]}"
                        lois[comment] = line_idx

    for loi in lois:
        start_idx = lois[loi]
        stop_idx = indexable_lines[start_idx:].index("// require:")
        output.append(loi)
        output.append('\n'.join(indexable_lines[start_idx+1:start_idx+stop_idx]))

    print("{}".format('\n'.join(output)))


def get_module_branch(args):
    """
    Given the --branches parameter and a module, return the branch requested
    for that module. This function parses the user-provided string, maps
    modules to branches, finds the desired module, and emits it. Defaults to
    'main' branch.

    Args:
        args (namespace object): User-provided arguments

    Return:
        branch (str): Branch requested for module.
    """
    branch = 'main'
    if re.search(':', args.branches):
        branch_lookup = {}
        arged_branches = args.branches.split(',')
        for combination in arged_branches:
            combo_mod, combo_branch = combination.split(':')
            branch_lookup[combo_mod] = combo_branch
        if args.module in branch_lookup.keys():
            branch = branch_lookup[args.module]
    else:
        branch = args.branches
    return branch


def load_module(args):
    """
    Part of the load-module mode.

    Loads a Nextflow module into a project's workflow directory.
    Allows users to specify a specific branch to checkout.
    Automatically loads 'main' branch of module's repo unless specified by user.

    Args:
        args (Namespace object): User-provided arguments.
    """
    raft_cfg = load_raft_cfg()
    if not args.repo:
        args.repo = raft_cfg['nextflow_repos']['nextflow_modules']
    # Should probably check here and see if the specified project even exists...
    workflow_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow')

    branch = get_module_branch(args)

    if not(args.silent):
        print(f"Loading module {args.module} (branch {branch}) into project {args.project_id}")

    if not glob(pjoin(workflow_dir, args.module)):
        found = 0
        for subgroup in raft_cfg['nextflow_subgroups']["nextflow_module_subgroups"]:
            try:
                #print("{}".format(pjoin(args.repo, subgroup, args.module)))
                Repo.clone_from(pjoin(args.repo, subgroup, args.module),
                                pjoin(workflow_dir, args.module),
                                branch=branch)
                time.sleep(args.delay)
                found = 1
            except:
                pass
        if not found:
            sys.exit(f"ERROR: Could not find module {args.module} in any subgroups specified in RAFT config")
        nf_cfg = pjoin(raft_cfg['filesystem']['projects'],
                       args.project_id,
                       'workflow',
                       'nextflow.config')
        mod_cfg = pjoin(raft_cfg['filesystem']['projects'],
                        args.project_id,
                        'workflow',
                        args.module,
                        args.module + '.config')
        if os.path.isfile(mod_cfg):
            update_nf_cfg(nf_cfg, mod_cfg)
    else:
        if not(args.silent):
            print(f"Module {args.module} is already loaded into project {args.project_id}. Skipping...")
    if not(args.no_deps):
        recurs_load_modules(args)


#def run_auto(args):
#    """
#    Given a loaded project, run auto.raft steps. This is a bit dangerous since
#    malicious code could be implanted into an auto.raft file, but can be made
#    safer by ensuring all commands are called through RAFT (in other words,
#    ensure steps are valid RAFT modes before running).
#
#    There are other considerations -- sometimes metadata may already be within
#    the metadata directory, so they won't need to be loaded a second time.
#    Perhaps this should be part of load-metadata?
#    """
#    raft_cfg = load_raft_cfg()
#    auto_raft = pjoin(raft_cfg['filesystem']['projects'],


def newest(log_dir, pattern):
    #https://stackoverflow.com/a/58991637
    files = os.listdir(log_dir)
    file_list = [os.path.join(log_dir, basename) for basename in files if basename.startswith(pattern)]
    return os.path.basename(max(file_list, key=os.path.getctime))

def convert_path_to_bucket(args, path):
    """
    Replaces the local portion of the path with the specified cloud bucket.
    """
#    path = path.replace('/'.join(path.split('/')[:-3]), args.cloud)
    path = path.replace(os.getcwd(), args.cloud)
    return path

def run_workflow(args):
    """
    Part of the run-workflow mode.

    Runs a specified workflow on a user-specific set of sample(s), for all
    samples in manifest csv file(s), or both. Executes checked out branch of
    workflow unless specificed by user.

    Args:
        args (Namespace object): User-provided arguments.
    """
    raft_cfg = load_raft_cfg()
    init_dir = getcwd()
    all_samp_ids = []
    processed_samp_ids = []


    if not args.keep_previous_outputs:
        # Check for directory instead of try/except.
        try:
            shutil.rmtree(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'outputs'))
        except FileNotFoundError:
            pass

    # Getting base command
    nf_cmd = get_base_nf_cmd(args)

    # Appending work directory
    work_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'work')
    nf_cmd = add_nf_work_dir(args, work_dir, nf_cmd)

    # Appending global FASTQ directory (for internal FASTQ symlinking)
    nf_cmd = add_global_fq_dir(args, nf_cmd)

    nf_cmd = add_global_bam_dir(args, nf_cmd)

    # Appending global shared outputs directory
    nf_cmd = add_global_shared_dir(args, nf_cmd)

    # Hide subjoin processes
    if not(args.show_all_processes):
        nf_cmd = hide_subjoins(nf_cmd)

    os.chdir(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'logs'))
    print(f"Running:\n{nf_cmd}")
    nf_exit_code = subprocess.run(nf_cmd, shell=True, check=False)

    reports_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'outputs', 'reports')
    samples_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'outputs', 'samples')

    if not nf_exit_code.returncode:
        print("Workflow completed!\n")
        if not args.no_reports:
            print(f"Workflow reports are available in {reports_dir}.")
            report_patterns = ['report', 'timeline', 'dag', 'trace']
            newest_reports = [newest(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'logs'), x) for x in report_patterns]
            os.makedirs(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'outputs', 'reports'))
            for report in newest_reports:
                if os.path.exists(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'logs', report)):
                    shutil.copy(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'logs', report),
                                pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'outputs', 'reports', report))
        print(f"Sample-level outputs are available in {samples_dir}.")



def get_work_dirs(args):
    """
    Get all work dirs associated with the latest run of the project.
    """
    raft_cfg = load_raft_cfg()
    work_dirs = []
    log_dir = pjoin(raft_cfg['filesystem']['projects'],
                    args.project_id, 'logs')
    project_uuid = ''
    with open(pjoin(log_dir, '.nextflow', 'history'), encoding='utf8') as nf_hist_fo:
        for line in reversed(nf_hist_fo.read().split('\n')):
            if line:
                line = line.split('\t')
                if line[3] == 'OK':
                    project_uuid = line[5]
                    break
    os.chdir(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'logs'))
    work_dirs = [x for x in subprocess.run(f'nextflow log {project_uuid}', shell=True, check=False, capture_output=True).stdout.decode("utf-8").split('\n') if os.path.isdir(x)]
    return work_dirs


def get_size(start_path = '.'):
    """
    https://stackoverflow.com/a/1392549
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for filename in filenames:
            filename_path = os.path.join(dirpath, filename)
            # skip if it is symbolic link
            if not os.path.islink(filename_path):
                total_size += os.path.getsize(filename_path)

    return total_size


def add_global_fq_dir(args, samp_nf_cmd):
    """
    Part of run-workflow mode.

    Appends global fastq directory to Nextflow command.

    Args:
        samp_nf_cmd (str): Sample-specific Nextflow command.

    Returns:
        Str containing the modified Nextflow command with a working directory.
    """
    raft_cfg = load_raft_cfg()
    global_fq_dir = raft_cfg['filesystem']['fastqs']
    if args.cloud:
        global_fq_dir = convert_path_to_bucket(args, global_fq_dir)
    return ' '.join([samp_nf_cmd, f'--global_fq_dir {global_fq_dir}'])

def add_global_bam_dir(args, samp_nf_cmd):
    """
    Part of run-workflow mode.

    Appends global BAM directory to Nextflow command.

    Args:
        samp_nf_cmd (str): Sample-specific Nextflow command.

    Returns:
        Str containing the modified Nextflow command with a working directory.
    """
    raft_cfg = load_raft_cfg()
    global_bam_dir = raft_cfg['filesystem']['bams']
    if args.cloud:
        global_bam_dir = convert_path_to_bucket(args, global_bam_dir)
    return ' '.join([samp_nf_cmd, f'--global_bam_dir {global_bam_dir}'])

def hide_subjoins(samp_nf_cmd):
    """
    Part of run-workflow mode.

    Appends global fastq directory to Nextflow command.

    Args:
        samp_nf_cmd (str): Sample-specific Nextflow command.

    Returns:
        Str containing the modified Nextflow command with a working directory.
    """
    return ' '.join([samp_nf_cmd, '| grep -v join_run | grep -v subjoin'])


def add_global_shared_dir(args, samp_nf_cmd):
    """
    Part of run-workflow mode.

    Appends global fastq directory to Nextflow command.

    Args:
        samp_nf_cmd (str): Sample-specific Nextflow command.

    Returns:
        Str containing the modified Nextflow command with a working directory.
    """
    raft_cfg = load_raft_cfg()
    shared_dir = raft_cfg['filesystem']['shared']
    if args.cloud:
        shared_dir = convert_path_to_bucket(args, shared_dir)
    return ' '.join([samp_nf_cmd, f'--shared_dir {shared_dir}'])


def add_nf_work_dir(args, work_dir, nf_cmd):
    """
    Part of run-workflow mode.

    Appends working directory to Nextflow command.

    Args:
        work_dir (str): Work directory path to be appended.
        nf_cmd (str): Nextflow command.

    Returns:
        Str containing the modified Nextflow command with a working directory.
    """
    if args.cloud:
        work_dir = convert_path_to_bucket(args, work_dir)
    return ' '.join([nf_cmd, f'-w {work_dir}'])


def get_base_nf_cmd(args):
    """
    Part of run-workflow mode.

    Prepends the actual Nextflow execution portion to Nextflow command prior to
    execution. This currently globs for a *.nf file within the specified
    workflow directory (so workflow Nextflow files do NOT have to be named the
    same as the workflow repo).

    Args:
        args (Namespace object): User-specific arguments.
        samp_nf_cmd (str): Nextflow command.

    Returns:
        Str containing modified Nextflow command with execution portion.
    """
    raft_cfg = load_raft_cfg()

    # Processing nf-params
    cmd = []
    if args.nf_params:
        cmd = args.nf_params.split(' ')
    new_cmd = []
    # Should this be in its own additional function?
    for component in cmd:
        # Do any processing here.
        new_cmd.append(component)

    #Discovering workflow script
    workflow_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow')
    #Ensure only one nf is discoverd here! If more than one is discovered, then should multiple be run?
    discovered_nf = glob(pjoin(workflow_dir, 'main.nf'))[0]

    # Adding project directory
    proj_dir_str = ''
    proj_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id)
    if args.cloud:
        proj_dir = convert_path_to_bucket(args, proj_dir)
    proj_dir_str = f"--project_dir {proj_dir}"
    ref_dir_str = ''
    metadata_dir_str = ''
    fq_dir_str = ''
    if args.cloud:
        if not(re.search('--ref_dir', args.nf_params)):
            ref_dir_str = "--ref_dir {}".format(pjoin(args.cloud, 'references/cloud'))
        if not(re.search('--metadata_dir', args.nf_params)):
            metadata_dir_str = "--metadata_dir {}".format(pjoin(args.cloud, 'metadata'))
        if not(re.search('--fq_dir', args.nf_params)):
            fq_dir_str = "--fq_dir {}".format(pjoin(args.cloud, 'fastqs'))

    # Adding all components to make base command.
    resume = ''
    reports = ''
    if not args.no_resume:
        resume = '-resume'
    if not args.no_reports:
        reports = '-with-trace -with-report -with-dag -with-timeline'
    cmd = ' '.join(['export NXF_VER=23.10.4; nextflow -Dnxf.pool.type=sync run', discovered_nf, ' '.join(new_cmd), proj_dir_str, ref_dir_str, metadata_dir_str, fq_dir_str, resume, reports])
    return cmd


def update_nf_cfg(nf_cfg, mod_cfg):
    """
    Part of load-module mode.

    Updates the project-specific nextflow.config file with information from a
    specific module's config file (named <module>.config).

    This is currently designed to only pull in configuration parameters if they
    are not already in the nextflow.config. This is a blind spot that should be
    addressed in the future.

    Args:
        nf_cfg (str): Path to nextflow.config to be updated.
        comp_cfg (str): Path to component config file to use for updating nextflow.config.
    """
    new_nf_cfg = []
    lines_to_copy = []
    with open(mod_cfg, encoding='utf8') as mfo:
        for line in mfo:
            if line not in ["process {\n", "}\n"]:
                lines_to_copy.append(line)

    with open(nf_cfg, encoding='utf8') as nfo:
        for line in nfo:
            new_nf_cfg.append(line)
            if line == "process {\n":
                new_nf_cfg.extend(lines_to_copy)

    with open(nf_cfg, 'w', encoding='utf8') as nfo:
        for line in new_nf_cfg:
            nfo.write(line)


def rndm_str_gen(k=5):
    """
    Creates a random k-mer.
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(k))


def load_raft_cfg():
    """ Part of several modes.

    This function reads the RAFT configuration file and provides a dictionary
    with configuration information.

    Returns:
        Dictionary with configuration information.
    """
    cfg = {}
    cfg_path = pjoin(getcwd(), '.raft.cfg')
    if os.path.isfile(cfg_path):
        with open(cfg_path, encoding='utf8') as cfg_fo:
            cfg = json.load(cfg_fo)
    else:
        sys.exit("Cannot find RAFT configuration file.\nPlease run raft.py in your RAFT installation directory.")
    return cfg


def dump_to_auto_raft(args):
    """
    Part of several modes.

    Called anytime RAFT is called with non-administrative commands. This copies
    commands to auto.raft file.

    Args:
        args (Namespace object): User-specified arguments.
    """
    if args.command and args.command not in ['init-project', 'run-auto', 'package-project',
                                             'load-project', 'setup', 'push-project',
                                             'rename-project', 'run-workflow', 'run-ots',
                                             'copy-parameters', 'available-workflows',
                                             'available-modules', 'check-manifest']:
        raft_cfg = load_raft_cfg()
        auto_raft_path = pjoin(raft_cfg['filesystem']['projects'],
                               args.project_id,
                               '.raft',
                               'auto.raft')
        comment_out = ''
        if args.command in ['add-step']:
            comment_out = '#'
        with open(auto_raft_path, 'a', encoding='utf8') as auto_raft_fo:
            auto_raft_fo.write(f"{comment_out}{' '.join(sys.argv)}\n")


def snapshot_postproc(inf, outf):
    """
    Strips out repeated steps from snapshot so auto-run can run as expected.

    This may be overly aggressive, but can modify it later.
    """
    with open(outf, 'w', encoding='utf8') as ofo:
        with open(inf, encoding='utf8') as ifo:
            new_contents = []
            contents = ifo.readlines()
            for line_idx, line in enumerate(contents):
                if not re.search("run-workflow", line):
                    new_contents.append(line)
                elif line_idx == len(contents) - 1:
                    line = line.strip().replace('n=', 'n="')
                    #print(line)
                    if re.search('-profile', line):
                        spl = line.split(' ')
                        ind =  [i for i, word in enumerate(spl) if re.search('-profile', word)]
                        spl[ind[0] + 1] = "RAFT_PROFILE_PLACEHOLDER"
                        line = ' '.join(spl)
                new_contents.append(line + '"\n')
            for line in new_contents:
                ofo.write(line)


def package_project(args):
    """
    Part of package-project mode.
    """
    raft_cfg = load_raft_cfg()
    proj_dir = os.path.join(raft_cfg['filesystem']['projects'], args.project_id)
    rndm_str = rndm_str_gen()
    proj_tmp_dir = os.path.join(raft_cfg['filesystem']['projects'], args.project_id, 'tmp', rndm_str)

    os.mkdir(proj_tmp_dir)

    # Copying metadata directory. Should probably perform some size checks here.
    os.mkdir(pjoin(proj_tmp_dir, 'metadata'))
    metadata_files = glob(pjoin(proj_dir, 'metadata', '**'), recursive=True)
    for mfile in metadata_files:
        mfilel = mfile.split('/')
        msuffix = '/'.join(mfilel[mfilel.index('metadata')+1:])
        if not os.path.islink(mfile) and not os.path.isdir(mfile):
            basedir = pjoin(proj_tmp_dir, 'metadata', os.path.dirname(msuffix))
            if '/' in msuffix:
                os.makedirs(pjoin(proj_tmp_dir, 'metadata', os.path.dirname(msuffix)))
            shutil.copyfile(mfile, pjoin(proj_tmp_dir, 'metadata', msuffix))

    # Getting required checksums. Currently only doing /datasets, but should
    # probably do other directories produced by workflow as well.
    dirs = ['outputs', 'metadata', 'fastqs', 'references', 'workflow']
    if not args.no_checksums:
        print("Calculating checksums...")
        hashes = {}
        with open(pjoin(proj_tmp_dir, 'checksums'), 'w', encoding='utf8') as checksums_fo:
            hashes = {}
            for directory in dirs:
                print(f"Calculating checksums for files in {directory}...")
                files = glob(pjoin('projects', args.project_id, directory, '**'), recursive=True)
                sub_hashes = {file: md5(file) for file in files if os.path.isfile(file)}
                hashes.update(sub_hashes)
            json.dump(hashes, checksums_fo, indent=4)

    # Get Nextflow configs, etc.
    os.mkdir(pjoin(proj_tmp_dir, 'workflow'))
    wf_dirs = glob(pjoin(proj_dir, 'workflow', '*'))
    igpat = ''
    if args.no_git:
        igpat = '.*'
    for wf_dir in wf_dirs:
        if os.path.isdir(wf_dir):
            shutil.copytree(wf_dir,
                            pjoin(proj_tmp_dir, 'workflow', os.path.basename(wf_dir)),
                            ignore=shutil.ignore_patterns(igpat))
        else:
            shutil.copyfile(wf_dir,
                            pjoin(proj_tmp_dir, 'workflow', os.path.basename(wf_dir)))

    # Get auto.raft
    shutil.copyfile(pjoin(proj_dir, '.raft', 'auto.raft'),
                    pjoin(proj_dir, '.raft', 'snapshot.raft.actual'))
    snapshot_postproc(pjoin(proj_dir, '.raft', 'snapshot.raft.actual'),
                      pjoin(proj_dir, '.raft', 'snapshot.raft.postproc'))

    shutil.copyfile(pjoin(proj_dir, '.raft', 'snapshot.raft.postproc'),
                    pjoin(proj_tmp_dir, 'snapshot.raft'))
    shutil.copyfile(pjoin(proj_dir, '.raft', 'snapshot.raft.actual'),
                    pjoin(proj_tmp_dir, 'snapshot.raft.actual'))

    rftpkg = ''
    if args.output:
        rftpkg = pjoin(proj_dir, 'rftpkgs', args.output + '.rftpkg')
    else:
        rftpkg = pjoin(proj_dir, 'rftpkgs', 'default.rftpkg')
    with tarfile.open(rftpkg, 'w', encoding='utf8') as taro:
        for i in os.listdir(proj_tmp_dir):
            #print(i)
            taro.add(os.path.join(proj_tmp_dir, i), arcname = i)


def md5(fname):
#https://stackoverflow.com/a/3431838
    hash_md5 = hashlib.md5()
#    with open(fname, "rb", encoding='utf8') as f:
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def load_project(args):
    """
    Part of load-project mode.
    """
    raft_cfg = load_raft_cfg()
    # Should really be using .init.cfg from package here...
    fixt_args = {'init_config': os.path.join(os.getcwd(), '.init.cfg'),
                 'project_id': args.project_id,
                 'repo_url': ''}
    fixt_args = argparse.Namespace(**fixt_args)

    # Initialize project
    print("Initializing project...")
    init_project(fixt_args)
    # Moving mounts.config so that can be protected and reintroduced after copying over workflow.config.
    shutil.move(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'mounts.config'),
                pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.mounts.config'))

    tarball = ''
    if args.rftpkg:
        # Copy rftpkg into project
        print("Copying RAFT Package into project...")
        shutil.copyfile(args.rftpkg,
                        pjoin(raft_cfg['filesystem']['projects'],
                              args.project_id,
                              'rftpkgs',
                              os.path.basename(args.rftpkg)))
    elif args.repo_url:
        repo = Repo(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'rftpkgs'))
        repo.create_remote('origin', args.repo_url)
        repo.git.pull('origin', args.branch)

    tarball = pjoin(raft_cfg['filesystem']['projects'],
                    args.project_id,
                    'rftpkgs',
                    os.path.basename(args.rftpkg))

    # Extract and distribute tarball contents
    print("Extracting and distributing RAFT Package...")
    tar = tarfile.open(tarball, encoding='utf8')
    tar.extractall(os.path.join(raft_cfg['filesystem']['projects'], args.project_id, '.raft'))
    tar.close()

    for dir in ['metadata', 'workflow']:
        print(f"Populating project's {dir} directory...")
        shutil.rmtree(pjoin(raft_cfg['filesystem']['projects'], args.project_id, dir))
        shutil.copytree(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', dir),
                        pjoin(raft_cfg['filesystem']['projects'], args.project_id, dir))
    shutil.move(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'mounts.config'),
                pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', '.mounts.config.orig'))
    shutil.move(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.mounts.config'),
                pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'mounts.config'))

    # Create back-up of snapshot.raft and checksums

    if os.path.isfile(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'checksums')):
        shutil.copyfile(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'checksums'),
                        pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'checksums.orig'))

        replace_proj_id(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'checksums'),
                              get_orig_prod_id(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'snapshot.raft.actual')),
                              args.project_id)
    else:
        print("Checksums file not found within RFTPKG. Checksums cannot be checked.")


    shutil.copyfile(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'snapshot.raft'),
                    pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'snapshot.raft.orig'))

    orig_proj_id = get_orig_prod_id(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'snapshot.raft'))

    replace_proj_id(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'snapshot.raft'), get_orig_prod_id(pjoin(raft_cfg['filesystem']['projects'], args.project_id, '.raft', 'snapshot.raft.orig')), args.project_id)


def replace_proj_id(fle, old_proj_id, new_proj_id):
    """
    """
    raft_cfg = load_raft_cfg()
    with open(pjoin(raft_cfg['filesystem']['projects'], new_proj_id, 'tmp', 'tmp_file'), 'w', encoding='utf8') as tfo:
        with open(fle, encoding='utf8') as ffo:
            contents = ffo.readlines()
            for line in contents:
                line = line.replace(f'-p {old_proj_id}', f'-p {new_proj_id}')
                line = line.replace(f'projects/{old_proj_id}', f'projects/{new_proj_id}')
                tfo.write(line)

    shutil.move(pjoin(raft_cfg['filesystem']['projects'], new_proj_id, 'tmp', 'tmp_file'), fle)


def get_orig_prod_id(fle):
    """
    """
    with open(fle, encoding='utf8') as ffo:
        contents = ffo.readlines()
        first = contents[0].strip()
        ind = ''
        ind = first.split(' ').index('-p')
        if not ind:
            ind = first.split(' ').index('--project-id')
        return first.split(' ')[ind+1]


def get_params_from_module(module_path):
    """
    Extracta parameters from a module.

    Args:
      module_path (str): Module path.

    Returns:
      undef_params (list): Parameters not defined within module.
      defined_params (list): Parameters defined within module.
    """
    undef_params, defined_params = ([], [])
    with open(module_path, encoding='utf8') as mfo:
        for line in mfo.readlines():
            line = line.rstrip()
            if re.search("^params.*", line):
                if re.search(" = ''", line):
                    undef_params.append(line.partition(' ')[0])
                else:
                    defined_params.append(line.partition(' ')[0])

    return undef_params, defined_params


def get_section_insert_idx(contents, section, stop='\n'):
    """
    Part of add-step mode.

    Find the index of the nearest empty row for a section. Basically, find
    where the the a set of rows should be inserted within a main.nf specific
    section.
    """
    start = contents.index(section)
    insert_idx = contents[start:].index(stop)
    return start + insert_idx


def get_wf_mod_map(args):
    """
    Create a dictionary mapping workflows to modules.

    Args
        args (namespace object): User-defined arguments

    Returns:
        wf_mod_map (dict): Keys are workflow and values are module containing workflow.
    """
    raft_cfg = load_raft_cfg()
    wf_mod_map = {}
    nf_scripts = glob(pjoin(raft_cfg['filesystem']['projects'],
                            args.project_id,
                            'workflow',
                            '*/*.nf'))
    for nf_script in nf_scripts:
        workflows = extract_wfs_from_script(nf_script)
        for workflow in workflows:
            wf_mod_map[workflow] = nf_script

    return wf_mod_map


def extract_wfs_from_script(script_path):
    """
    Extract all workflows from a nextflow module.

    Args:
        script_path (str): Nextflow module path.

    Returns:
        wfs (list): Workflows contained in Nextflow module.
    """
    wfs = []
    with open(script_path, encoding='utf8') as spo:
        for line in spo:
            if re.search('^workflow', line):
                wfs.append(line.replace('workflow ', '').split('{')[0].strip())
    return wfs


def add_step(args):
    """
    Part of add-step mode.

    Args:
        args (Namespace object): User-provided arguments.
    """
    raft_cfg = load_raft_cfg()

    # Relevant files
    main_nf = pjoin(raft_cfg['filesystem']['projects'],
                    args.project_id,
                    'workflow',
                    'main.nf')
    mod_nf = pjoin(raft_cfg['filesystem']['projects'],
                   args.project_id,
                   'workflow',
                   args.module,
                   args.module + '.nf')

    # Load main.nf contents
    main_contents = []
    with open(main_nf, encoding='utf8') as mfo:
        main_contents = mfo.readlines()

    if not(args.silent):
        print("Making backup of project's main.nf...")
    shutil.copyfile(main_nf, main_nf + '.bak')

    # Step's inclusion statement for main.nf
    if args.alias:
        inclusion_str = f"include {{ {args.step} as {args.alias} }} from './{args.module}/{args.module}.nf'\n"
    else:
        inclusion_str = f"include {{ {args.step} }} from './{args.module}/{args.module}.nf'\n"

    # Need to load main.nf params here to check against when getting step-specific params.
    # Seems odd to emit the undefined and defined separately.
    main_undef_params, main_defined_params = get_params_from_module(main_nf)
    main_params = main_undef_params + main_defined_params

    # Extract step contents from step's module file in order to make string to
    # put within main.nf
    step_str = ''
    step_slice = extract_step_slice_from_nfscript(mod_nf, args.step)
    if not step_slice:
        sys.exit(f"ERROR: Step {args.step} could not be found in module {args.module}.")
    if re.search('workflow', step_slice[0]):
        step_str = get_workflow_str(step_slice)
    elif re.search('process', step_slice[0]):
        step_str = get_process_str(step_slice)
    if args.alias:
        params = step_str.partition('(')[2]
        step_str = ''.join([args.alias, '(', params]).replace(args.step, args.alias)
    pprint_step = ''
    if args.alias:
        pprint_step = ',\n  '.join([x for x in step_str.rstrip().split(', ')]).replace('(', '(\n  ').replace(args.step, args.alias)
    else:
        pprint_step = ',\n  '.join([x for x in step_str.rstrip().split(', ')]).replace('(', '(\n  ')
    if not(args.silent):
        print("Adding the following step to main.nf:")
        print(f"{pprint_step}")

    # Parameterization
    all_step_params = []
    if re.search('workflow', step_slice[0]):
        wf_mod_map = get_wf_mod_map(args)
        final_steps = []
        discoverd_steps = [args.step]
        while discoverd_steps:
            new_round_steps = []
            for step in discoverd_steps:
                step_slice = extract_step_slice_from_nfscript(wf_mod_map[step], step)
                new_round_steps.extend([i.partition('(')[0] for i in step_slice if i.partition('(')[0] in wf_mod_map.keys()])
                discoverd_steps.remove(step)
                final_steps.append(step)
            discoverd_steps.extend(new_round_steps)

        for step in final_steps:
            step_slice = extract_step_slice_from_nfscript(wf_mod_map[step], step)
            if step == args.step:
                all_step_params.extend(extract_params_from_contents(step_slice, False))
            else:
                all_step_params.extend(extract_params_from_contents(step_slice, True))
    elif re.search('process', step_slice[0]):
        all_step_params = get_process_params(step_slice)

    all_new_step_params = [x for x in all_step_params if x not in [y.partition(' ')[0] for y in main_contents]]

    # Applying changes to main.nf
    if step_str not in main_contents and inclusion_str not in main_contents:

        inc_idx = get_section_insert_idx(main_contents, "/*Inclusions*/\n")
        main_contents.insert(inc_idx, inclusion_str)

        params_idx = get_section_insert_idx(main_contents, "/*Parameters*/\n")
        params_to_add = ''
        if args.alias:
            params_to_add = "{}\n".format('\n'.join(["{} = ''".format(x) for x in list(dict.fromkeys(all_new_step_params))]).replace(args.step, args.alias))
        else:
            params_to_add = "{}\n".format('\n'.join(["{} = ''".format(x) for x in list(dict.fromkeys(all_new_step_params))]))
        main_contents.insert(params_idx, params_to_add)

        wf_idx = get_section_insert_idx(main_contents, "workflow {\n", "}\n")
        main_contents.insert(wf_idx, step_str.replace('(', '(\n  ').replace(', ', ',\n  '))


        with open(main_nf, 'w', encoding='utf8') as ofo:
            ofo.write(''.join(main_contents))
    else:
        print(f"Step {step_str.split('(')[0]} has already been added to Project {args.project_id}")
        print("Please use step aliasing (-a/--alias) if you intend to use this step multiple times.")
        sys.exit(1)


def is_workflow(step):
    """
    Part of add-step mode.

    Determine if a step is a workflow.

    Args:
        contents (list): List containing the contents of a module/component in
                         which step is defined.
        step (str): Step being queried. This string may be associated with a process or a workflow.

    Returns:
        True if step is a workflow, otherwise False.
    """
    is_workflow = False
    if re.search('workflow', step[0]):
        is_workflow = True
    return is_workflow


def find_step_module(contents, step):
    """
    Part of add-step mode.

    Find a step's module based on the contents of the module in which it's being called. This is effectively parsing 'include' statements.

    Args:
        contents (list): List containing rows from a Nextflow module/component.
        step (str): Step that requires parent component.

    Returns:
        Str containing parent component for step.
    """
    mod = []
    try:
        mod = [re.findall(f'include .*{step}.*', i) for i in contents if re.findall(f'include .*{step}.*', i)][0][0].split('/')[1]
    except FileNotFoundError:
        pass
    return mod


def find_step_actual_and_alias(contents, step):
    """
    Part of add-step mode.

    Find a step's module based on the contents of the module in which it's
    being called. This is effectively parsing 'include' statements.

    Args:
        contents (list): List containing rows from a Nextflow module/component.
        step (str): Step that requires parent component.

    Returns:
        Tuple containing parent component for step.
    """
    mod = []

    mod = [re.findall(f'include .*{step}.*', i) for i in contents if re.findall(f'include .*{step}.*', i)][0][0]
    if not re.findall(' as ', mod):
        actual = step
        alias = ''
    else:
        mod = mod.split('{')[1].split('}')[0]
        mod = mod.partition(' as ')
        actual = mod[0].strip()
        alias = mod[2].strip()
    return(actual, alias)


def extract_steps_from_contents(contents):
    """
    Part of add-step mode.

    Get list of (sub)steps (workflows/processes) being called from contents.
    NOTE: Contents in this case means a single workflow's contents.

    Args:
        contents (list): List containing the rows from a workflow's entry in a component.
    """
    wfs = [re.findall('^[\\w_]+\\(.*', i) for i in contents if re.findall('^[\\w_]+\\(.*', i)]
    flat = [i.partition('(')[0] for j in wfs for i in j]
    return flat


def extract_params_from_contents(contents, discard_requires):
    """
    Part of add-step mode.

    Get list of parameters defined for a process or workflow.

    Args:
        contents (list): process/workflow line-by-line contents.


    Returns:
        flat (list): Parameters either list in require:// block or passed as
                     parameter options within process/workflow definition.
    """
    contents_bfr = [x.strip() for x in contents]
    contents = contents_bfr
    require_params = []
    if [re.findall("// require:", i) for i in contents if re.findall("// require:", i) for i in contents]:
        start = contents.index("// require:") + 1
        end = contents.index("take:")
#        require_params = [i.replace('//   ','').split(',')[0] for i in contents[start:end] if re.search('^//   params', i)]
    params = [re.findall("(params.*?,|params.*?\\)|params.*\\?})", i) for i in contents if
              re.findall("params.*,|params.*\\)", i) and i != 'params.']
    params.append([i.replace('//   ','').split(',')[0] for i in contents[start:end] if re.search('^//   params', i)])
    flat = [i.partition('/')[0].replace(',','').replace(')', '').replace('}', '').replace("'", '').replace('"', '').replace('/', '').replace('\\', '').replace(' =~ ', '').replace(' != ', '') for
            j in params for i in j]
    # THIS IS TOO RESTRICTIVE!!! This should only be applied if it's not the initial step being called.
    if discard_requires:
        flat = [i for i in flat if i not in require_params]
    else:
        flat = flat + require_params
    return flat
#    return require_params


def extract_step_slice_from_nfscript(nfscript_path, step):
    """
    Part of add-step mode.

    Extract a step's contents (for parameter and wf_extraction) from a
    module file's conents.

    Args:
        contents (list): List containing the contents of a module file.
        step (str): User-specificied step (process/workflow).

    Returns:
        step_slice (list): step contents extracted from module.
    """
    step_slice = []
    contents = []
    if not(os.path.exists(nfscript_path)):
        sys.exit("Module not loaded within project. Exiting.")
    else:
        with open(nfscript_path, encoding='utf8') as nf_script_fo:
            contents = [i.rstrip() for i in nf_script_fo.readlines()]
    # Need the ability to error out if step doesn't exist. Should list steps
    # from module in that case.
    if f'workflow {step} {{' in contents:
        step_start = contents.index(f'workflow {step} {{')
        step_end = contents.index("}", step_start)
        step_slice = contents[step_start:step_end]
    elif f'process {step} {{' in contents:
        step_start = contents.index(f'process {step} {{')
        step_end = contents.index("}", step_start)
        step_slice = contents[step_start:step_end]
    else:
        sys.exit(f"Cannot find step {step} in module {nfscript_path}")
    return step_slice



def get_workflow_str(wf_slice):
    """
    Part of add-step mode.

    Get the string containing a workflow and its parameters for the main.nf
    workflow.

    Args:
        wf_slice (list): Contains entirety of workflow definition.

    Returns:
        wf_str (str): String representation for calling workflow within main.nf

    """
    wf_slice_bfr = [x.strip() for x in wf_slice]
    wf_slice = wf_slice_bfr
    # Can just strip contents before processing to not have to deal with a lot
    # of the newlines and space considerations.
    wf_list = []
    if '// require:' in wf_slice:
        require_idx = wf_slice.index('// require:')
        take_idx = wf_slice.index('take:')
        wf_list = [wf_slice[0].replace("workflow ", "").replace(" {",""), '(',
                   ", ".join([x.replace('//  ', '').strip() for x in wf_slice[require_idx+1:take_idx]]), ')\n']
    else:
        wf_list = [wf_slice[0].replace("workflow ", "").replace(" {", ""), '()\n']
    wf_str = "".join(wf_list)
    return wf_str


def get_process_str(proc_slice):
    """
    Part of add-step mode.

    Get the string containing a process and its parameters for the main.nf
    workflow.

    Args:
        proc_slice (list): Process slice.
    """
    stop_idx = ''
    start_idx = proc_slice.index('// require:')
    stop_idx = proc_slice[start_idx:].index('')
    params = [x.lstrip('//   ') for x in proc_slice[start_idx+1:start_idx + stop_idx] if x]
    cleaned_params = []
    for param in params:
        cleaned_params.append(param)
    proc_list = [proc_slice[0].replace('process ', '').replace(' {', ''), '(', ', '.join(cleaned_params), ')\n']
    proc_str = ''.join(proc_list)
    return proc_str

def get_process_params(proc_slice):
    """
    Part of add-step mode.

    Get the string containing a process and its parameters for the main.nf
    workflow.

    Args:
        proc_slice (list): Process slice.
    """
    stop_idx = ''
    start_idx = proc_slice.index('// require:')
    stop_idx = proc_slice[start_idx:].index('')
    params = [x.lstrip('//   ') for x in proc_slice[start_idx+1:start_idx + stop_idx] if re.search('params.', x)]
    cleaned_params = []
    for param in params:
        cleaned_params.append(param)
    return cleaned_params



def push_project(args):
    """
    Push a project's .rftpkg to a Git repository.

    This needs further testing and documentation.

    Args:
        args (namespace object): User-defined arguments
    """
    raft_cfg = load_raft_cfg()
    local_repo = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'repo')
    shutil.copyfile(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'rftpkgs', args.rftpkg + '.rftpkg'),
                    pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'repo', args.rftpkg + '.rftpkg'))
    repo = Repo(local_repo)
    repo.index.add(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'repo', args.rftpkg + '.rftpkg'))
    repo.index.commit(f"rftpkg commit {time.time()}")
    repo.git.push('origin', repo.head.ref)


def chk_proj_id_exists(project_id):
    """
    Checks that a user-specific project exists within RAFT's project directory.a

    Args:
        project_id (str): Project identifier

    Returns:
        True
    """
    raft_cfg = load_raft_cfg()
    projects_dir = raft_cfg['filesystem']['projects']
    error_message = f"Project {project_id} cannot be found in {projects_dir}"

    raft_cfg = load_raft_cfg()
    if not os.path.isdir(pjoin(raft_cfg['filesystem']['projects'], project_id)):
        sys.exit(error_message)

    return True


def update_modules(args):
    """
    Pulls the latest versions of either all modules or user-specific modules for a project.

    Args:
        args (namespace object): User-specified arguments
    """
    raft_cfg = load_raft_cfg()
    main_nf = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow')
    for module in glob(pjoin(main_nf, '*', '')):
        if os.path.basename(os.path.dirname(module)) in args.modules.split(',') or not args.modules:
            repo = Repo(module)
            ori = repo.remotes.origin
            module_dir = os.path.basename(os.path.dirname(module))
            print(f"Pulling latest for module {module_dir} (branch {repo.active_branch.name})")
            ori.pull() # Need some exception handling here.
            time.sleep(args.delay)


def rename_project(args):
    """
    Given an original project identifier and a new project identifier,
    exhaustively rename the project and associated files.

    This function is limited to the files explicitly listed in the function.

    Args:
        args (namespace object): User-provided arguments
    """
    raft_cfg = load_raft_cfg()
    proj_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id)

    renamable_contents = [pjoin('workflow', 'mounts.config'),
                          pjoin('workflow', 'nextflow.config'),
                          pjoin('.raft', 'auto.raft')]

    for renamable_contents_file in renamable_contents:
        # Creating a backup prior to modifying file. Serves as template for renaming.
        shutil.move(pjoin(proj_dir, renamable_contents_file),
                    pjoin(proj_dir, renamable_contents_file + '.rename.bak'))

        with open(pjoin(proj_dir, renamable_contents_file), 'w', encoding='utf8') as f_fo:
            with open(pjoin(proj_dir, renamable_contents_file + '.rename.bak'), encoding='utf8') as f_io:
                for line in f_io.readlines():
                    f_fo.write(line.replace(args.project_id, args.new_id))

    shutil.move(proj_dir,
                pjoin(raft_cfg['filesystem']['projects'], args.new_id))


def clean_project(args):
    """
    """
    raft_cfg = load_raft_cfg()
    log_dir = pjoin(raft_cfg['filesystem']['projects'],
                    args.project_id, 'logs')
    successful_run = ''
    project_uuid = ''
    with open(pjoin(log_dir, '.nextflow', 'history'), encoding='utf8') as nf_hist_fo:
        for line in reversed(nf_hist_fo.read().split('\n')):
            if line:
                line = line.split('\t')
                if line[3] == 'OK':
                    successful_run = line[2]
                    project_uuid = line[5]
                    break
    print(f"Project UUID is: {project_uuid}")
    print(f"Last successful run is: {successful_run}")
    os.chdir(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'logs'))
    all_work_hashes = [x for x in subprocess.run(f'nextflow log {project_uuid}', shell=True, check=False, capture_output=True).stdout.decode("utf-8").split('\n') if os.path.isdir(x)]
    successful_work_hashes = [x for x in subprocess.run(f"nextflow log -f 'workdir, status' {successful_run} | grep -E 'COMPLETED|CACHED' | cut -f 1 -d '	'", shell=True, check=False, capture_output=True).stdout.decode("utf-8").split('\n') if x in all_work_hashes]
    completed_work_hashes = [x for x in subprocess.run(f"nextflow log -f 'workdir, status' {project_uuid} | grep -E 'COMPLETED|CACHED' | cut -f 1 -d '	'", shell=True, check=False, capture_output=True).stdout.decode("utf-8").split('\n') if x in all_work_hashes]
    print(f"All run work hashes count: {len(all_work_hashes)}")
    print(f"Successful run work hashes count: {len(successful_work_hashes)}")
    print(f"Completed run work hashes count: {len(completed_work_hashes)}")
    cleanable_hashes = []
    if args.keep_latest and input("This will only keep work directories from the latest successful run!\nAre you sure? ") in ['YES', 'yes', 'Yes', 'Y', 'y']:
        cleanable_hashes = [x for x in all_work_hashes if x not in successful_work_hashes]
    else:
        cleanable_hashes = [x for x in all_work_hashes if x not in completed_work_hashes]
    print(f"Cleanable run work hashes count: {len(cleanable_hashes)}")
    if not args.no_exec:
        for cleanable_dir in cleanable_hashes:
            print(f"Removing extra files from {cleanable_dir}...")
            cleanable_files = [i for i in os.listdir(cleanable_dir) if i not in ['meta'] and not re.search('command', i)]
            for cleanable_file in cleanable_files:
                try:
                    shutil.rmtree(cleanable_file)
                except FileNotFoundError:
                    pass
    else:
        print("Skipping deletion due to -n/--no-exec.")


def touch(path):
    """
    Touches a path.
    https://stackoverflow.com/a/12654798
    """
    with open(path, 'a', encoding='utf8'):
        os.utime(path, None)


def copy_parameters(args):
    """
    Copy parameters from either a source project or previously defined configuration file.

    Currently, generates a .main.nf.copy_params file to allow users to review
    parameters prior to applying the parameters to their project.

    Args:
        args (namespace object): User-defined arguments

    """
    raft_cfg = load_raft_cfg()

    if args.source_project:
        src_proj_main = pjoin(raft_cfg['filesystem']['projects'], args.source_project, 'workflow', 'main.nf')
        orig_proj_main = pjoin(raft_cfg['filesystem']['projects'], args.dest_project, 'workflow', 'main.nf')
        new_proj_main = pjoin(raft_cfg['filesystem']['projects'], args.dest_project, 'workflow', 'main.nf.copy_params')
    elif args.source_config:
        src_proj_main = args.source_config
        orig_proj_main = pjoin(raft_cfg['filesystem']['projects'], args.dest_project, 'workflow', 'main.nf')
        new_proj_main = pjoin(raft_cfg['filesystem']['projects'], args.dest_project, 'workflow', 'main.nf.copy_params')

    source_params = {}
    if args.source_project:
        with open(src_proj_main, encoding='utf8') as f_obj:
            source_params = extract_params_from_proj_or_cfg(f_obj)
    elif args.source_config:
        with open(args.source_config, encoding='utf8') as f_obj:
            source_params = extract_params_from_proj_or_cfg(f_obj)

    with open(orig_proj_main, encoding='utf8') as dfo:
        with open(new_proj_main, 'w', encoding='utf8') as tfo:
            for line in dfo.readlines():
                parted_line = line.rstrip().partition(' = ')
                if parted_line[0] in source_params.keys() and source_params[parted_line[0]] != parted_line[2]:
                    tfo.write(f"{parted_line[0]} = {source_params[parted_line[0]]}\n")
                else:
                    tfo.write(line)
    if not(args.silent):
        print("Done copying parameters.")
        print(f"Verify parameters in {new_proj_main} and")
        print(f"copy {new_proj_main} to {orig_proj_main} to complete.")


def extract_params_from_proj_or_cfg(f_obj):
    """
    Extracts parameter strings from a file object.

    Args:
      f_obj (file object): File containing parameters for extraction.

    Returns:
      source_params (dict): Dictionary containing defined parameters from f_obj.
    """
    source_params = {}
    for line in f_obj.readlines():
        line = line.rstrip()
        if (line.startswith('params.') and
#            not line.partition(' = ')[2].startswith('params') and
            not re.search('project_identifier', line)):
            line = line.partition(' = ')
            source_params[line[0]] = line[2]
    return source_params


def list_ots_workflows(args):
    """
    """
    if args.workflow == '':
        print("Listing all workflows. Run\nraft.py available-workflows -wf/--workflow <WORKFLOW>\nfor more information about a workflow group.\n{}".format('-'*80))
    gl = gitlab.Gitlab('https://www.gitlab.com')
    group = gl.groups.get(82538869, include_subgroups=True)
    if args.workflow == '':
        for subgroup in group.subgroups.list(iterator=True):
            print(subgroup.attributes['name'])
    elif args.workflow and args.input == '':
        print("Listing all versions of {} workflow.\n{}".format(args.workflow, '-'*80))
        wf_group_id = [x.attributes['id'] for x in group.subgroups.list() if x.attributes['name'] == args.workflow][0]
        wf_group = gl.groups.get(wf_group_id, include_subgroups=True)
        print("Workflow\tSpecies\tInput")
        for wf_species_group in wf_group.subgroups.list(iterator=True):
            group = gl.groups.get(wf_species_group.attributes['id'])
            wf_species_input_projects = group.projects.list()
            for project in wf_species_input_projects:
                full_name = project.attributes['name']
                input_type = full_name.split('-')[-1]
                species = full_name.split('-')[-2]
                workflow = '-'.join(full_name.split('-')[:-2])
                print(f"{workflow}\t{species}\t{input_type}")
        print("{}\nRun\nraft.py available-workflows -wf/--workflow <WORKFLOW> -s/--species <SPECIES> -i/--input <INPUT>\nfor more information about a specific workflow.".format('-'*80))
    elif args.workflow and args.input:
        print("Details for {} {} workflow starting from {}.\n{}".format(args.species, args.workflow, args.input, '-'*80))
        wf_group_id = [x.attributes['id'] for x in group.subgroups.list() if x.attributes['name'] == args.workflow][0]
#        print("workflow group id: {}".format(wf_group_id))
        wf_group = gl.groups.get(wf_group_id, include_subgroups=True)
        wf_species_group_id = [x.attributes['id'] for x in wf_group.subgroups.list() if x.attributes['name'] == "{}-{}".format(args.workflow, args.species)][0]
#        print("workflow species group id: {}".format(wf_species_group_id))
        wf_species_group = gl.groups.get(wf_species_group_id)
        wf_species_input_project_id = [x.attributes['id'] for x in wf_species_group.projects.list() if x.attributes['name'] == "{}-{}-{}".format(args.workflow, args.species, args.input)][0]
#        print("workflow species input project id: {}".format(wf_species_input_project_id))
        project = gl.projects.get(wf_species_input_project_id)
        config = project.files.get(file_path='{}.{}.{}.config'.format(args.workflow, args.species, args.input), ref='main')
        config_contents = base64.b64decode(config.content).decode("utf-8")
        ### Should be its own function...
        uniq = 0
        index = -1
        while uniq == 0 and index > -4:
            params = {}
            params_uniqness = []
            for line in config_contents.split('\n'):
                if line and not(line.startswith('#')):
                    key = ''
                    if '$' in line.partition(' ')[0]:
                        print(index)
                        print(line)
                        key = '$'.join(line.partition(' ')[0].split('$')[index:])
                        print(key)
                    else:
                        key = line.partition(' ')[0]
                    value = line.partition('=')[-1].strip().replace("'", '').replace('"', '').replace('[', '').replace(']', '').replace('\\', '')
                    if re.search('tool', key) and not(value):
                        value = "None (tool defaults)"
                    elif not(value):
                        value = 'None'
                    if key not in ['separator']:
                        params_uniqness.append(key)
                        params[key] = value
            dup = [item for item in params_uniqness if params_uniqness.count(item) >1]
            if len(set(params_uniqness)) == len(params_uniqness):
                uniq = 1
            else:
                index = index - 1
#        print('-'*80)
        print("Default parameters:")
        print("-------------------")
        p = 'Parameter'
        p2 = '---------'
        v = 'Value'
        v2 = '-----'
        print(f"{p:<30}\t{v}")
        print(f"{p2:<30}\t{v2}")
        for k,v in params.items():
            print(f"{k:<30}\t{v}")


        json = project.files.get(file_path='{}.{}.{}.json'.format(args.workflow, args.species, args.input), ref='main')
        json_contents = base64.b64decode(json.content).decode("utf-8").split('\n')
#        print(json_contents)
        steps_start = json_contents.index('  "steps": {')
        steps_stop = steps_start + json_contents[steps_start:].index('  },')
        steps = [x.strip().replace('"', '').replace(',', '') for x in json_contents[steps_start+1:steps_stop]]
        modules_of_interest = [x.partition(': ')[2] for x in steps]
        loaded_modules = []
        all_module_code = []
        individ_steps = [f"{x.partition(': ')[2]}::{x.partition(': ')[0]}" for x in steps]
        print('-'*80)
        print("Workflow steps:")
        print("---------------")
        for i in individ_steps:
            print(f"{i}")
        print('-'*80)


        print("Alternate tools:")
        print("----------------")
        alt_tools = {}
        module_project_id_list = get_all_module_project_id_list()
        deps = 1
        while deps == 1:
            for module in modules_of_interest:
                #print("Considering module {}...".format(module))
                if module not in loaded_modules and module:
                    module_project_id = get_module_project_id(module, module_project_id_list)
                    module_code = get_module_code(module, module_project_id)
                    all_module_code.extend(module_code)
                    mod_deps = get_module_depends(module_code)
                    for mod_dep in mod_deps:
                        if mod_dep not in modules_of_interest and mod_dep not in loaded_modules:
                            modules_of_interest.append(mod_dep)
                    loaded_modules.append(module)
            #print("Loaded modules: {}".format(loaded_modules))
            #print("Modules of interest: {}".format(modules_of_interest))
            if set(loaded_modules) == set(modules_of_interest):
                deps = 0
        for param in params.keys():
            alt_tools[param] = []
            for line in all_module_code:
                if re.search("if.*\\(.*{} =~".format(param), line):
                    tool = line.partition('/')[2].partition('/')[0]
                    if re.search('\\)', tool):
                        tool = tool.partition(')')[2] #Dealing with regex stuff.
                    if tool != ',':
                        alt_tools[param].append(tool)
        p = 'Parameter'
        p2 = '---------'
        v = 'Alternate tools'
        v2 = '---------------'
        print(f"{p:<30}\t{v}")
        print(f"{p2:<30}\t{v2}")
        for k,v in alt_tools.items():
            if v:
                v2 = ','.join(set(v))
                print(f"{k:<30}\t{v2}")



def get_all_module_project_id_list():
    gl = gitlab.Gitlab('https://gitlab.com')
    module_group = gl.groups.get(16497923, include_subgroups=True)
    return module_group.projects.list(get_all=True)


def get_module_project_id(module, module_project_id_list):
    return [x.attributes['id'] for x in module_project_id_list if x.attributes['name'] == "{}".format(module)][0]

def get_module_code(module, module_project_id):
    gl = gitlab.Gitlab('https://gitlab.com')
    project = gl.projects.get(module_project_id)
    module = project.files.get(file_path='{}.nf'.format(module), ref='versaraft')
    return base64.b64decode(module.content).decode("utf-8").split('\n')

def get_module_depends(module_code):
    deps = list(set([i.split('/')[-1].replace("'", '').replace('.nf', '') for i in module_code if re.findall(f'^include ', i)]))
    return deps

def list_modules(args):
    """
    """
    cli = cmd.Cmd()
    modules = []
    gl = gitlab.Gitlab('https://www.gitlab.com', keep_base_url=True)
    group = gl.groups.get(16497923, include_subgroups=True)
    for project in group.projects.list(iterator=True):
        modules.append(project.attributes['name'])
    cli.columnize(sorted(modules), displaywidth=80)


def run_ots(args):
    """
    Run an off-the-shelf workflow on a user-provided manifest.

    Args:

    Returns:
    """
    raft_cfg = load_raft_cfg()
    ip_args = args
    if ip_args.project_id == 'default-demo':
        ip_args.project_id = "demo-{}-v{}".format(args.workflow, re.sub('^v', '', args.version))
    print("Initializing project {}...".format(args.project_id))
    ip_args.init_config = pjoin(getcwd(), '.init.cfg')
    ip_args.repo_url = ''
    init_project(ip_args)

    print("Pulling off-the-shelf workflow...")
    print("This may take some time due to module fetching.")
    go_args = args
    if re.search("^v", args.version):
        go_args.branch = "{}-{}". format(args.workflow, args.version)
    else:
        go_args.branch = "{}-v{}". format(args.workflow, args.version)
    ots_meta_path = get_ots(go_args)

    ots_meta = parse_ots_meta(ots_meta_path)

    for module in ots_meta['modules']:
        lm_args = args
        lm_args.module = module
        lm_args.repo = ''
#        lm_args.branches = args.module_branch
        if re.search("^v", args.version):
            lm_args.branches = "{}-{}". format(args.workflow, args.version)
        else:
            lm_args.branches = "{}-v{}". format(args.workflow, args.version)
        lm_args.no_deps = False
        lm_args.silent = True
        if lm_args.debug == True:
            lm_args.silent = False
        lm_args.delay = 5
        load_module(lm_args)

    if args.cloud:
        print("NOTE! RAFT is running in -c/--cloud mode!")
        print("FASTQs are assumed to be in {}/fastqs.".format(args.cloud))
        print("References are assumed to be in {}/references/cloud.".format(args.cloud))
        print("The manifest file is assumed to be in {}/metadata.".format(args.cloud))
        print("")
        print("Output files will be available in {}/projects/{}/outputs upon workflow completion.".format(args.cloud,args.project_id))
        if args.manifest == 'demo':
            args.manifest = 'lens.human.demo.manifest'
    else:   
        #Load demo manifest here.
        print("Loading manifest...")
        ots_mani_dir = pjoin(raft_cfg['filesystem']['metadata'], 'ots')
        if not(os.path.exists(ots_mani_dir)):
            os.mkdir(ots_mani_dir)

        lm_args = args
        lm_args.file = args.manifest
        lm_args.sub_dir = ''
        lm_args.mode = 'symlink'
        lm_args.silent = True
        demo_manifest = ''
        if lm_args.file == 'demo':
            demo_manifest = glob(pjoin(ots_meta_path, '*manifest'))[0]
            lm_args.file = demo_manifest
            args.manifest = demo_manifest
        load_ots_mani(args, args.manifest, ots_mani_dir)


        print("Loading references...")
        ots_ref_dir = pjoin(raft_cfg['filesystem']['references'], 'ots')
        if not(os.path.exists(ots_ref_dir)):
            os.mkdir(ots_ref_dir)
    
        for ref_url in ots_meta['references']:
            if ref_url.endswith('.sh') or ref_url.endswith('.py'):
                run_ots_script(args, ref_url, ots_ref_dir)
            else:
                load_ots_ref(args, ref_url, ots_ref_dir, ots_meta["references_postproc"])

        if 'fastqs' in ots_meta.keys():
            print("Loading fastqs...")
            ots_fq_dir = pjoin(raft_cfg['filesystem']['fastqs'], 'ots')
            if not(os.path.exists(ots_fq_dir)):
                os.mkdir(ots_fq_dir)

            for fq_url in ots_meta['fastqs']:
                load_ots_fq(args, fq_url, ots_fq_dir)

    proj_bin_path = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'bin')
    if not(os.path.exists(proj_bin_path)):
        os.mkdir(proj_bin_path)
    wget.download('https://gitlab.com/landscape-of-effective-neoantigens-software/nextflow/modules/tools/lens/-/wikis/uploads/329db9653ec2d64d9f23eb04de835325/clean_work_files.sh', proj_bin_path)
    subprocess.run('chmod +x {}'.format(pjoin(proj_bin_path, 'clean_work_files.sh')), shell=True, check=False)
    print("")


    print("Building workflow...")
    for step, module in ots_meta['steps'].items():
        as_args = args
        as_args.step = step
        as_args.module = module
        as_args.alias = ''
        as_args.silent = True
        add_step(as_args)

    print("Connecting subworkflows...")
    main_nf_path = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'main.nf')
    fnr = ots_meta['find_and_replace']
    fnr['_manifest(\n  MANIFEST'] = '_manifest(\n  Channel.fromPath("${{params.metadata_dir}}/{}")'.format(args.manifest.split('/')[-1])
    fnr['MANIFEST_PATH'] = '"${{params.metadata_dir}}/{}"'.format(args.manifest.split('/')[-1])
    # Support for get_files() call
#    fnr['get_files(\n  MANIFEST'] = 'get_files(\n  Channel.fromPath("${{params.metadata_dir}}/{}")'.format(args.manifest.split('/')[-1])
    ots_find_and_replace(fnr, main_nf_path)

    print("Populating default parameters...")
    cp_args = args
    cp_args.dest_project = args.project_id
    cp_args.source_config = glob(pjoin(ots_meta_path, '*config'))[0]
    cp_args.source_project = ''
    cp_args.silent = True
    copy_parameters(cp_args)
    shutil.copyfile(pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'main.nf.copy_params'),
                    pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'main.nf'))

    if args.user_params:
        print("Updating parameters with user-provided parameters...")
        up_args = args
        ots_update_user_params(args)


    if not(args.setup_only):
        print("Running workflow...")
        rw_args = args
        rw_args.keep_previous_outputs = False
        rw_args.nf_params = False
        rw_args.no_resume = False
        run_workflow(args)

def ots_update_user_params(args):
    """
    Args:

    Returns:
    """
    params_dict = {}
    raft_cfg = load_raft_cfg()
    main_nf = pjoin(raft_cfg['filesystem']['projects'], args.project_id, 'workflow', 'main.nf')
    main_nf_contents = []
    new_main_nf_contents = []
    with open(main_nf) as mfi:
        main_nf_contents = mfi.readlines()
    for user_param in args.user_params:
        param, bfr, value = user_param[0].partition('=')
        print("Changing parameter {} to {}".format(param, value))
        new_value = ''
        if not(re.search(':', value)):
            new_value = "'{}'".format(value)
            print("[debug]New value: {}".format(new_value))
        else:
            new_value = ['\'{}{}{}\''.format(x.partition(":")[0],"':'",x.partition(":")[2].replace("'", '')) for x in value.split(',')]
            new_value = '"{}"'.format(new_value)
            print("[debug]New value: {}".format(new_value))
        params_dict[param] = new_value
    for line in main_nf_contents:
        for user_param, user_value in params_dict.items():
            if re.search("{} = ".format(user_param), line):
                user_value = user_value
                tmp = line.partition('=')[0]
                line = "{}= {}\n".format(tmp, user_value.replace('["', '[').replace('"]', ']').replace('", "', ', '))
        new_main_nf_contents.append(line)

    with open(main_nf, 'w') as mfo:
        for line in new_main_nf_contents:
            mfo.write(line)



def get_ots(args):
    """
    Get an off-the-shelf workflow from Gitlab.

    Args:

    Returns:
    """
    raft_cfg = load_raft_cfg()
    local_ots = pjoin(raft_cfg['filesystem']['projects'], args.project_id, "{}-{}-{}".format(args.workflow, args.species, args.input_data))
    ots_repo = 'https://gitlab.com/reproducible-analyses-framework-and-tools/nextflow/workflows'
    repo_to_pull = pjoin(ots_repo, args.workflow, "{}-{}".format(args.workflow, args.species), "{}-{}-{}".format(args.workflow, args.species, args.input_data))
    if args.debug:
        print("Cloning repo {}".format(repo_to_pull))
    Repo.clone_from(pjoin(ots_repo, args.workflow, "{}-{}".format(args.workflow, args.species), "{}-{}-{}".format(args.workflow, args.species, args.input_data)),
                    pjoin(local_ots),
                    branch=args.branch)
    return(local_ots)


def parse_ots_meta(ots_meta_path):
    """
    """
    json_path = glob(pjoin(ots_meta_path, "*json"))
    with open(json_path[0], encoding='utf8') as tmp_fo:
        return json.load(tmp_fo)

def load_ots_ref(args, ref_url, ots_ref_dir, postproc):
    """
    """
    ref = ref_url.split('/')[-1]
    lr_args = args
    lr_args.file = ref
    if ref in postproc.keys() and postproc[ref] == 'gunzip':
        new_ref = ref.replace(".gz", '')
        lr_args.file = new_ref
    if ref in postproc.keys() and postproc[ref] == 'tar -xvf':
        new_ref = ref.replace(".tar.gz", '')
        lr_args.file = new_ref
    if ref in postproc.keys() and postproc[ref] == 'bgzip':
        new_ref = ref + '.gz'
        lr_args.file = new_ref
    try:
        load_reference(args)
    except:
        print("\nCouldn't find {}. Downloading...".format(ref))
        wget.download(ref_url, pjoin(ots_ref_dir, ref))
        if ref in postproc.keys() and postproc[ref] == 'gunzip':
            subprocess.run("gunzip --quiet {}".format(pjoin(ots_ref_dir, ref)), shell=True, check=False)
        elif ref in postproc.keys() and postproc[ref] == 'tar -xvf':
            subprocess.run("mkdir {}; tar -xf {} -C {}; rm -rf {}".format(pjoin(ots_ref_dir, new_ref), pjoin(ots_ref_dir, ref), ots_ref_dir, pjoin(ots_ref_dir, ref)), shell=True, check=False)
        elif ref in postproc.keys() and postproc[ref] == 'bgzip':
            subprocess.run("bgzip {}".format(pjoin(ots_ref_dir, ref)), shell=True, check=False)
        load_reference(args)

def load_ots_fq(args, fq_url, ots_fq_dir):
    """
    """
    fq = fq_url.split('/')[-1]
    if not(os.path.isfile(pjoin(ots_fq_dir, fq))):
        print("\nCouldn't find {}. Downloading...".format(fq))
        wget.download(fq_url, pjoin(ots_fq_dir, fq))

def run_ots_script(args, ref_url, ots_ref_dir):
    """
    """
    ref = ref_url.split('/')[-1]
    print("\nRunning OTS download script {}...".format(ref))
    if not(os.path.exists(pjoin(ots_ref_dir, ref))):
        wget.download(ref_url, pjoin(ots_ref_dir, ref))
    if ref.endswith(".sh"):
        subprocess.run("bash {} {}".format(pjoin(ots_ref_dir, ref), ots_ref_dir), shell=True, check=False)
    elif ref.endswith(".py"):
        subprocess.run("python3 {}".format(pjoin(ots_ref_dir, ref)), shell=True, check=False)


def load_ots_mani(args, mani_path, ots_mani_dir):
    """
    """
    mani = mani_path.split('/')[-1]
    lm_args = args
    lm_args.file = mani
    try:
        load_metadata(args)
    except:
        print("Couldn't find {} in RAFT metadata directory. Copying...".format(mani))
        shutil.copyfile(mani_path, pjoin(ots_mani_dir, mani))
        load_metadata(args)

def ots_find_and_replace(fnr, main_nf_path):
    """
    """
    bufr = ''
    with open(main_nf_path) as tfo:
        contents = tfo.read()
        for k, v in fnr.items():
            contents = contents.replace(k, v)
        bufr = contents
    with open(main_nf_path, 'w') as ofo:
        ofo.write(bufr)

def check_manifest(args):
    """
    """
    report = []

    raft_cfg = load_raft_cfg()

    full_base = raft_cfg['filesystem']['metadata']

    hdr_idx_map = {}

    pat_samps = {}

    required_columns = ['Patient_Name', 'Dataset', 'Run_Name', 'Sequencing_Method', 'Normal', 'File_Prefix']
    nice_to_have_columns = ['Alleles']
    globbed_files =  glob(pjoin(full_base, '**', args.manifest), recursive=True)
    if len(globbed_files) == 0:
        sys.exit(f"Cannot find {args.manifest} in {full_base}/**")
        # Put list of available references here.
    if len(globbed_files) > 1:
        sys.exit(f"File name {args.file} is not specific enough. Please provide a directory prefix.")
        # Put list of conflicting files here.
    globbed_file = globbed_files[0]
    with open(globbed_file) as mfo:
       for line_idx, line in enumerate(mfo.readlines()):
           line = line.rstrip()
           if line_idx == 0:
               header = line.split('\t')
               for required_column in required_columns:
                   if required_column not in line:
                       sys.exit("Missing column {} from the header. Add and populate this column and re-run.".format(required_column))
               for nice_to_have_column in nice_to_have_columns:
                   if nice_to_have_column not in line:
                       report.append("Missing column {} from the header. This column may be needed for some workflows".format(nice_to_have_column))
               for idx, col in enumerate(header):
                   hdr_idx_map[col] = idx
           else:
#               print("Checking manifest entry #{}...".format(line_idx))
               # Check for spaces over tabs
               line_spaces = line.split(' ')
               if len(line_spaces) > 1:
                   sys.exit("Spaces detected in manifest. Please use tab separation.\nFirst observed affected line: {}".format(line))
               line = line.split('\t')
               acceptable_seq_methods = ['WES', 'wes', 'RNA-Seq', 'RNA', 'WGS', 'wgs', 'WXS', 'wxs']
               if line[hdr_idx_map['Sequencing_Method']] not in acceptable_seq_methods:
                   print("Invalid sequencing method detected in manifest.")
                   print("Please use one of the following methods: {}.".format(', '.join(acceptable_seq_methods)))
                   sys.exit("First observed affected line: {}".format(line))
               if line[hdr_idx_map['Run_Name']].partition('-')[0] in ['ad', 'ar'] and line[hdr_idx_map['Normal']] != 'FALSE':
                   print("Abnormal sample prefix assigned to normal sample.")
                   print("Please ensure abnormal prefixes ('ar' and 'ad') are used with abnormal samples.")
                   sys.exit("First observed affected line: {}".format(', '.join(acceptable_seq_methods), line))
               if line[hdr_idx_map['Run_Name']].partition('-')[0] in ['nd', 'nr'] and line[hdr_idx_map['Normal']] != 'TRUE':
                   print("Normal sample prefix assigned to abnormal sample.")
                   print("Please ensure normal prefixes ('nr' and 'nd') are used with normal samples.")
                   sys.exit("First observed affected line: {}".format(line))
               if line[hdr_idx_map['Run_Name']].partition('-')[0] not in ['ad', 'ar', 'nd', 'nr']:
                   print("Sample prefix not allowed..")
                   print("Please ensure prefixes are 'nr', 'nd', 'ad', or 'ar'.")
                   sys.exit("First observed affected line: {}".format(line))
               pat_name = line[hdr_idx_map['Patient_Name']]
               samp = line[hdr_idx_map['Run_Name']].partition('-')[0]
               if pat_name not in pat_samps.keys():
                   pat_samps[pat_name] = []
               if samp in pat_samps[pat_name]:
                   sys.exit("Patient {} has multiple samples of type '{}'.\nPlease correct this issue and re-run check-manifest.".format(pat_name, samp))
               pat_samps[pat_name].append(samp)

       observed_samp_counts = [len(x) for x in list(pat_samps.values())]
       counts_mode = max(set(observed_samp_counts), key=observed_samp_counts.count)
       non_mode_pats = [i for i,j in pat_samps.items() if len(j) != counts_mode]
#       counts_of_counts = {}
#       for i in observed_samp_counts:
#           counts_of_counts[i] = counts_of_counts.get(i, 0) + 1

       print("The following patients had a different number of samples compared to most patients")
       print("Patient\tSamples\tCount")
       for pat in non_mode_pats:
           print("{}\t{}\t{}".format(pat,','.join(pat_samps[pat]), len(pat_samps[pat])))

       print('\n'.join(report))

def main():
    """
    Main function
    """

    args = get_args()

    if 'project_id' in args and args.command not in ['init-project', 'load-project', 'copy-parameters', 'run-ots', 'available-workflows', 'available-modules', 'run-demo', 'check-manifest']:
        chk_proj_id_exists(args.project_id)


    # I'm pretty sure .setdefaults within subparsers should handle running
    # functions, but this will work for now.
    if args.command == 'setup':
        setup(args)
    elif args.command == 'init-project':
        init_project(args)
    elif args.command == 'load-metadata':
        load_metadata(args)
    elif args.command == 'load-reference':
        load_reference(args)
    elif args.command == 'load-module':
        raft_cfg = load_raft_cfg()
        nf_config_dir = pjoin(raft_cfg['filesystem']['projects'], args.project_id,'workflow', 'nextflow.config')
        print(f"NOTE: Module Nextflow configuration modifications must be performed in {nf_config_dir}")
        load_module(args)
    elif args.command == 'list-steps':
        list_steps(args)
    elif args.command == 'update-mounts':
        update_mounts(args)
    elif args.command == 'add-step':
        add_step(args)
    elif args.command == 'run-workflow':
        run_workflow(args)
#    elif args.command == 'run-auto':
#        run_auto(args)
    elif args.command == 'package-project':
        package_project(args)
    elif args.command == 'load-project':
        load_project(args)
    elif args.command == 'push-project':
        push_project(args)
    elif args.command == 'update-modules':
        update_modules(args)
    elif args.command == 'rename-project':
        rename_project(args)
    elif args.command == 'clean-project':
        clean_project(args)
    elif args.command == 'load-dataset':
        load_dataset(args)
    elif args.command == 'copy-parameters':
        copy_parameters(args)
    elif args.command == 'run-ots':
        run_ots(args)
    elif args.command == 'run-demo':
        run_ots(args)
    elif args.command == 'available-workflows':
        list_ots_workflows(args)
    elif args.command == 'available-modules':
        list_modules(args)
    elif args.command == 'check-manifest':
        check_manifest(args)

    # Only dump to auto.raft if RAFT successfully completes.
    dump_to_auto_raft(args)


if __name__ == '__main__':
    main()
