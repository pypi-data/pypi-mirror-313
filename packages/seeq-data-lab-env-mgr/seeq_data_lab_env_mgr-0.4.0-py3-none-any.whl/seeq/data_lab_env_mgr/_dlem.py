from ._version import __version__

import asyncio
import json
import os
import re
import traceback
from datetime import timedelta, datetime, timezone
from dateutil import tz
from dateutil.parser import isoparse
from urllib.parse import urljoin, urlparse
import requests

import ipywidgets
import nbformat
import pandas as pd
from IPython.display import display, HTML

from seeq import spy
from seeq.sdk import ProjectsApi, SystemApi, ProjectInputV1, ScalarPropertyV1
try:
    from seeq.sdk import AddOnsApi
except:
    pass
from seeq.spy._datalab import is_datalab, is_ipython

from ._mixpanel import MixpanelTracker, Consumer, EventConstants, MIXPANEL_EVENT_VERSION
from ._helper import _extract_token_from_host


class DataLabEnvMgr(ipywidgets.VBox):
    _local_base_path = "/home/datalab/.local/lib/"
    _global_base_path = "/seeq/python/global-packages/lib/"
    _system_base_path = "/usr/local/.pyenv/versions/"
    _global_base = "/seeq/python/global-packages"
    _categories = ["local", "global", "system"]
    _datalab_home = "/home/datalab"
    _version = __version__
    _full_width_table_css = """<style> #full-width-table { width: 100%; } </style>"""
    _datetime_format = '%Y-%m-%d %H:%M:%S'
    _file_export_datetime_format = '%Y%h%d_%H%M%S'
    _is_python311_compatible = 'is_python311_compatible'
    _verified_label = '<span style="color: green;">This project has been verified to work with Python 3.11.</span>'
    _not_verified_label = '<span style="color: red;">This project has not been verified to work with Python 3.11.</span>'
    _verified_by_label = '<span style="color: green;">Verified by: {}</span>'
    _verified_on_label = '<span style="color: green;">Verified on: {}</span>'
    _mark_verified_button_desc = 'Mark Verified'
    _remove_verification_button_desc = 'Remove Verification'
    _info_button_style = 'info'
    _success_button_style = 'success'
    _danger_button_style = 'danger'
    _col_name_maps = {
            'name': 'Project Name',
            'project_name': 'Project Name',
            'id': 'ID',
            'url': 'URL',
            'owner_name': 'Owner Name',
            'creator_name': 'Creator Name',
            'project_type': 'Project Type',
            'updated_at': 'Last Updated',
            'scheduled_notebooks': "Scheduled Notebooks",
            'has_local_packages' : 'Local Packages (Python)',
            'python311_verified' : "Python 3.11 Verified",
            'python311_verified_by' : "Python 3.11 Verified By"
        }

    def __init__(self):

        if not (is_datalab() and is_ipython()):
            super().__init__(children=[ipywidgets.HTML(value="Data Lab Environment Manager is only available in Data Lab.")])
            return

        self._seeq_major_version = spy.utils.get_server_version_tuple(spy.session)[0]

        self._markdown_doc = ipywidgets.HTML("""
        <h1>Data Lab Environment Manager</h1>
        <p>This tool helps Data Lab users transition their Notebooks between different Python versions,
        manage projects, and handle Python packages effectively.</p>
        <p>For detailed instructions, please refer to the 
        <a href="https://support.seeq.com/kb/latest/cloud/user-guide-data-lab-environment-manager"
        target="_blank">full documentation</a>.</p>
        """)

        self._config = self._generate_config()
        self._has_global_write_access = os.access(self._global_base_path, os.W_OK)
        self._user_timezone = tz.gettz(spy.utils.get_user_timezone(spy.session))
        self._project_id = spy.utils.get_data_lab_project_id()
        self._projects_api = ProjectsApi(spy.session.client)

        project_url = spy.utils.get_data_lab_project_url(use_private_url=False)
        parsed_project_url = urlparse(project_url)
        self._hostname = f"{parsed_project_url.scheme}://{parsed_project_url.netloc}"
        mixpanel_token, mixpanel_host = _extract_token_from_host(self._hostname)
        self._mixpanel = None
        if mixpanel_token and mixpanel_host:
            consumer = Consumer(api_host=mixpanel_host)
            self._mixpanel = MixpanelTracker(mixpanel_token, consumer=consumer)

        # Projects Overview Section
        self._from_last_date_filter = ipywidgets.Dropdown(
            options=['Last 1 Month', 'Last 3 Months', 'Last 6 Months', 'Last 1 Year', 'All-time'],
            value='Last 6 Months',
            description='Last Used:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        _scheduled_notebook_status = ["All", "Active", "Stopped", "None"]
        self._scheduled_notebook_filter = ipywidgets.Dropdown(
            options=_scheduled_notebook_status,
            value=_scheduled_notebook_status[0],
            style={'description_width': 'initial'},
            description='Scheduled Notebook:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        _project_types = ["All"]
        self._project_type_filter = ipywidgets.Dropdown(
            options=_project_types,
            value=_project_types[0],
            style={'description_width': 'initial'},
            description='Project Type:',
            layout=ipywidgets.Layout(height="fit-content")
        )
        self._sort_projects_by_filter = ipywidgets.Dropdown(
            options=["Last Updated", "Project Name"],
            value="Last Updated",
            style={'description_width': 'initial'},
            description='Sort By:',
            layout=ipywidgets.Layout(height="fit-content")
        )

        self._has_local_python_packages_filter = ipywidgets.Dropdown(
            options=["All"],
            value="All",
            style={'description_width': 'initial'},
            description='Local Packages (Python):',
            layout=ipywidgets.Layout(height="fit-content")
        )

        self._python311_verified_filter = ipywidgets.Dropdown(
            options=["All", "True", "False"],
            value="False",
            style={'description_width': 'initial'},
            description='Python 3.11 Verified:',
            layout=ipywidgets.Layout(height="fit-content")
        )

        self._export_projects_button = ipywidgets.Button(
            description="",
            button_style=self._info_button_style,
            icon="file-csv",
            tooltip="Export to CSV",
            style={'description_width': 'initial'},
            layout=ipywidgets.Layout(width='40px', height='fit-content')
        )

        self._export_projects_button.on_click(self._on_export_projects_button_click)
        
        self._project_report_output = ipywidgets.Output(
            layout=ipywidgets.Layout(overflow='auto', height='93%', padding='0px'))

        self._project_report_controls = ipywidgets.HBox(
            [self._from_last_date_filter, self._scheduled_notebook_filter, self._project_type_filter,
             self._sort_projects_by_filter, self._python311_verified_filter],
            layout=ipywidgets.Layout(justify_content='space-between', height='7%', padding_left='10px',
                                     padding_right='10px'))
        self._project_report_progress_bar = ipywidgets.IntProgress(value=3, min=0, max=100,
                                                                   description='Loading Projects:',
                                                                   style={'description_width': 'initial'},
                                                                   layout=ipywidgets.Layout(width='auto'))

        self._project_report_wrap = ipywidgets.VBox([self._project_report_progress_bar],
                                                    layout=ipywidgets.Layout(overflow='auto', height='550px',
                                                                             padding='0px'))

        # Notebook Overview Section
        self._notebook_kernels_output = ipywidgets.Output(
            layout=ipywidgets.Layout(overflow='auto', height='auto', padding='0px', display="grid"))

        self._notebook_kernels_wrap = ipywidgets.VBox([self._notebook_kernels_output],
                                                      layout=ipywidgets.Layout(overflow='auto', height='550px',
                                                                               padding='0px'))

        # Packages Section
        self._packages_section_progress_bar = ipywidgets.IntProgress(value=3, min=0, max=100,
                                                                     description='Listing Packages:',
                                                                     style={'description_width': 'initial'},
                                                                     layout=ipywidgets.Layout(width='auto'))
        self._package_tabs = None

        package_scope_dropdown_options = ['local']
        if self._has_global_write_access:
            package_scope_dropdown_options.append('global')

        self._package_input = ipywidgets.Text(value='', placeholder='Enter package name', description='Install ',
                                              style={'description_width': 'initial'},
                                              layout=ipywidgets.Layout(height="fit-content"))

        self._package_version_dropdown = ipywidgets.Dropdown(options=[k for k, v in self._config.items()
                                                                      if v.get('pip_path') is not None],
                                                             description=' scope for Python ',
                                                             style={'description_width': 'initial'},
                                                             layout=ipywidgets.Layout(height="fit-content",
                                                                                      width="fit-content")
                                                             )

        self._package_scope_dropdown = ipywidgets.Dropdown(options=package_scope_dropdown_options,
                                                           value='local', description=' in ',
                                                           style={'description_width': 'initial'},
                                                           layout=ipywidgets.Layout(height="fit-content",
                                                                                    width="fit-content")
                                                           )

        self._package_install_button = ipywidgets.Button(description='Install', button_style=self._success_button_style)
        self._package_install_button.on_click(self._general_install_packages)

        self._package_install_box = ipywidgets.HBox([self._package_input,
                                                     self._package_scope_dropdown,
                                                     self._package_version_dropdown,
                                                     self._package_install_button],
                                                    layout=ipywidgets.Layout(justify_content='flex-start', height='7%'))

        self._packages_section_wrap = ipywidgets.VBox([self._packages_section_progress_bar],
                                                      layout=ipywidgets.Layout(overflow='auto', height='550px',
                                                                               padding='0px'))

        # Console Output Section
        self._console = ipywidgets.Output(layout=ipywidgets.Layout(overflow='auto', height='93%', padding='0px'))
        self._console_description = ipywidgets.Label(value="Console Output", style={'font_weight': 'bold'})
        self._clear_console_button = ipywidgets.Button(description="Clear", layout=ipywidgets.Layout(overflow='auto'))
        self._clear_console_button.on_click(self._clear_output_terminal)

        self._console_section_header = ipywidgets.HBox([self._console_description, self._clear_console_button],
                                                       layout=ipywidgets.Layout(justify_content='space-between',
                                                                                height='7%',
                                                                                padding_left='10px',
                                                                                padding_right='10px'))

        self._console_section_wrap = ipywidgets.VBox([self._console_section_header, self._console],
                                                     layout=ipywidgets.Layout(
                                                         overflow='auto', height='550px', padding='0px'))

        # Header Section
        project = self._projects_api.get_project(id=self._project_id).to_dict()
        compatibility_data = next(
            (item.get('value',False) for item in project.get('configuration', []) if item.get('name','') == self._is_python311_compatible),
            None)
        if compatibility_data:
            compatibility_info = json.loads(compatibility_data)
        else:
            compatibility_info = dict(verified=False, by=None, on=None)
        is_verified = compatibility_info.get('verified', False)

        self._verify_button = ipywidgets.Button(
            description= self._remove_verification_button_desc if is_verified else self._mark_verified_button_desc,
            button_style= self._success_button_style if is_verified else self._danger_button_style,
            layout=ipywidgets.Layout(width='fit-content')
        )
        self._verify_button.project_verified = is_verified
        self._verify_status_label = ipywidgets.HTML(value=self._verified_label if is_verified else self._not_verified_label)
        self._verify_info_label = ipywidgets.HTML(
            value=f'''
                <span style="color: red;">By Clicking <b>{self._mark_verified_button_desc}</b>, I Confirm that,</span>
                <ul style="list-style-type: disc; padding-left: 20px;">
                    <li style="color: red;">I have updated all notebooks in this project to <b>Python 3.11</b> and verified their proper functionality.</li>
                    <li style="color: red;">This project does not have any notebook that rely on <b>Python 3.8</b>.</li>
                    <li style="color: red;">No further actions are required for this project to ensure compatibility with <b>Python 3.11</b>.</li>
                </ul>
                '''
        )
        self._verify_by_label = ipywidgets.HTML(
            value=self._verified_by_label.format(compatibility_info.get('by', '-'))
        )
        parsed_time = ""
        if compatibility_info.get('on'):
            parsed_time = isoparse(compatibility_info.get('on')).astimezone(self._user_timezone).strftime(self._datetime_format)
        self._verify_on_label = ipywidgets.HTML(
            value=self._verified_on_label.format(parsed_time)
        )
        self._verify_section = ipywidgets.VBox([self._verify_status_label, self._verify_button, self._verify_info_label], 
            layout=ipywidgets.Layout(align_items='flex-start', width='35%', padding='10px'))
        if self._verify_button.project_verified:
            self._verify_section.children = [self._verify_status_label, self._verify_button, self._verify_by_label, self._verify_on_label]

        self._verify_button.on_click(self._verify_project)

        separator = ipywidgets.HTML(value="<div style='width:1px; height:100%; background-color:gray;'></div>")
        self._header_wrap = ipywidgets.HBox([self._markdown_doc], layout=ipywidgets.Layout(
            overflow='auto', border='1px solid #ccc', padding='10px', justify_content='space-between'))
        
        if self._seeq_major_version >=61:
            self._header_wrap.children = [self._markdown_doc, separator, self._verify_section]

        # Main Tab Layout
        self._tabs = ipywidgets.Tab(layout=ipywidgets.Layout(height='fit-content', ))
        self._tabs.children = [self._notebook_kernels_wrap, self._project_report_wrap, self._packages_section_wrap,
                               self._console_section_wrap]
        titles = ('Notebooks Overview', 'Projects Overview', 'Packages', 'Console Output')
        for i, title in enumerate(titles):
            self._tabs.set_title(i, title)

        version_label = ipywidgets.Label(value=f"Version: {self._version}")
        self._version_widget = ipywidgets.HBox([version_label],
                                        layout=ipywidgets.Layout(justify_content='flex-end', height="fit-content"))

        super().__init__(children=[self._header_wrap, self._tabs, self._version_widget])

        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = None

        self._update_notebook_kernels_wrap()
        if self._loop and self._loop.is_running():
            asyncio.create_task(self._update_packages_section_wrap())
            asyncio.create_task(self._update_projects_section_wrap())
        else:
            asyncio.run(self._update_packages_section_wrap())
            asyncio.run(self._update_projects_section_wrap())

    async def _update_projects_section_wrap(self):
        try:
            self._project_report_progress_bar.value += 10
            self.projects_df = pd.DataFrame(self._get_all_projects())
            self.projects_df.loc[self.projects_df["id"].isin(
                self._get_add_on_ids()), "project_type"] = "Data Lab Add-On"
            self.projects_df.loc[self.projects_df["id"].isin(
                self._get_packaged_add_on_ids()), "project_type"] = "Data Lab Packaged Add-On"
            self.projects_df['updated_at'] = self.projects_df.apply(
                lambda row: isoparse(row['updated_at'])
                .astimezone(self._user_timezone)
                .strftime(self._datetime_format), 
                axis=1
            )
            self.projects_df["url"] = self.projects_df.apply(lambda row: 
                urljoin(spy.session.public_url, f"data-lab/{row.id}"), axis=1)
            
            self.projects_df["name"] = self.projects_df.apply(lambda row: "<a href='{}' target='_blank'>{}</a>".format(
                row["url"], row["project_name"]), axis=1)
            self._project_type_filter.options = ["All"] + list(self.projects_df["project_type"].unique())
            self._has_local_python_packages_filter.options = ["All"] + ["3.7", "3.8", "3.11"]
            project_report_controls_children = [self._from_last_date_filter, self._scheduled_notebook_filter, 
                                                self._project_type_filter, self._sort_projects_by_filter]
            if 'has_local_packages' in self.projects_df.columns:
                project_report_controls_children.append(self._has_local_python_packages_filter)
            if self._seeq_major_version >=61:
                project_report_controls_children.append(self._python311_verified_filter)
            project_report_controls_children.append(self._export_projects_button)
            self._project_report_controls.children = project_report_controls_children
            self._project_report_progress_bar.value = 100
            self._project_report_wrap.children = [self._project_report_controls, self._project_report_output]
            self._track(EventConstants.EVENT_NAME_LAUNCH)
            ipywidgets.interactive(self._filter_projects_dataframe,
                                   from_last_date=self._from_last_date_filter,
                                   scheduled_notebook=self._scheduled_notebook_filter,
                                   project_type=self._project_type_filter,
                                   sort_projects_by=self._sort_projects_by_filter,
                                   python311_verified=self._python311_verified_filter,
                                   local_package=self._has_local_python_packages_filter
                                   )
        except Exception as e:
            self._project_report_wrap.children = [self._project_report_output]
            with self._project_report_output:
                self._project_report_output.clear_output()
                print(traceback.format_exc())

    def _update_notebook_kernels_wrap(self):
        try:
            self._parsed_notebooks = self._parse_notebooks(self._datalab_home)
            with self._notebook_kernels_output:
                self._notebook_kernels_output.clear_output()
                display(HTML(
                    self._full_width_table_css + self._parsed_notebooks.to_html(max_rows=None, max_cols=None,
                                                                                index=True,
                                                                                escape=False,
                                                                                table_id="full-width-table")))
        except Exception as e:
            with self._notebook_kernels_output:
                self._notebook_kernels_output.clear_output()
                print(traceback.format_exc())

    async def _update_packages_section_wrap(self):
        try:
            self._packages_section_progress_bar.value += 10
            self._packages = self._list_packages(self._config)
            self._packages_consolidated = self._consolidate(self._packages)
            selected_index = self._package_tabs.selected_index if self._package_tabs is not None else None
            self._package_tabs = self._create_package_tabs(self._packages_consolidated, self._config)
            if selected_index:
                self._package_tabs.selected_index = selected_index
            self._packages_section_progress_bar.value = 100
            self._packages_section_wrap.children = [self._package_tabs, self._package_install_box]
        except Exception as e:
            packages_output = ipywidgets.Output(layout=ipywidgets.Layout(overflow='auto', height='auto',
                                                                         padding='0px', display="grid"))

            self._packages_section_wrap.children = [packages_output]
            with packages_output:
                packages_output.clear_output()
                print(traceback.format_exc())

    def _generate_config(self):
        config = {}

        def _update_config(base_path, python, mode):
            site_packages_path = os.path.join(base_path, python, "site-packages", "")

            if os.path.isdir(site_packages_path):
                v = _parse_version(python)
                if v:
                    config.setdefault(v, {"site_package_path": {}})
                    config[v]["site_package_path"][mode] = site_packages_path

        def _update_config_for_base_path(base_path, mode):
            if os.path.isdir(base_path):
                for python_directory in os.listdir(base_path):
                    _update_config(base_path, python_directory, mode)

        def _parse_version(name):
            v = re.search(r'\d+\.\d+', name)
            return v.group(0) if v else None

        # Update config for local, global, and system Python installations
        _update_config_for_base_path(self._local_base_path, "local")
        _update_config_for_base_path(self._global_base_path, "global")

        if os.path.isdir(self._system_base_path):
            for path in os.listdir(self._system_base_path):
                system_lib_path = os.path.join(self._system_base_path, path, "lib")
                version = _parse_version(path)
                if version:
                    config.setdefault(version, {"site_package_path": {}})
                    config[version]["pip_path"] = os.path.join(self._system_base_path, path, "bin", "pip")
                    config[version]["python_path"] = os.path.join(self._system_base_path, path, "bin", "python")
                if os.path.isdir(system_lib_path):
                    for python_dir in os.listdir(system_lib_path):
                        if python_dir.startswith("python"):
                            _update_config(system_lib_path, python_dir, "system")

        return config

    def _list_packages_in_site_packages(self, site_packages_path):
        from importlib.metadata import distributions

        packages = {}
        try:
            distributions = distributions(path=[site_packages_path])
            for item in distributions:
                name = item.metadata.get('name', None)
                if name is None:
                    continue
                packages[name] = {"project_name": name, "version": item.metadata.get('version')}
        except Exception as e:
            print(f"Error listing packages in {site_packages_path}: {e}")
        return packages

    def _list_packages(self, config):
        result = {}
        for version, c in config.items():
            v_result = {}
            for mode, path in c.get("site_package_path", {}).items():
                v_result[mode] = self._list_packages_in_site_packages(path)
                self._packages_section_progress_bar.value += 10
            result[version] = v_result
        return result

    def _consolidate(self, packages):
        from collections import defaultdict
        result = defaultdict(lambda: defaultdict(dict))
        for version, item in packages.items():
            for k in self._categories:
                for package, detail in item.get(k, {}).items():
                    result[k][package][version] = detail
        return result

    def _create_table_grid(self, packages, config, mode="local"):

        def _version_key(v):
            major, minor = map(int, v.split('.'))
            return major, minor

        def get_ui_item(package, version, item, mode):
            if item:
                return item.get('version')
            pip_path = self._config.get(version, {}).get("pip_path", None)
            if not pip_path:
                return "-"
            if mode == "local":
                return self._create_install_button("Install Locally", package, pip_path, mode)
            if mode == "global":
                if self._has_global_write_access:
                    return self._create_install_button("Install Globally", package, pip_path, mode)
                else:
                    return ipywidgets.Button(description="Ask Admin to Install", disabled=True)
            return "-"

        def generate_rows():
            all_python_versions = sorted(config.keys(), key=_version_key)
            for package, v in sorted(packages.items()):
                row = [package]
                for version in all_python_versions:
                    item = v.get(version)
                    row.append(get_ui_item(package, version, item, mode))
                yield row

        headers = ["Package Name"] + [f"Python {v}" for v in sorted(config.keys(), key=_version_key)]
        table_data = list(generate_rows())

        # Create header and row widgets
        header_widgets = [ipywidgets.Label(value=header, style={'font_weight': 'bold'}) for header in headers]
        row_widgets = [ipywidgets.Label(value=str(cell)) if isinstance(cell, str) else cell for row in table_data for
                       cell in row]

        return ipywidgets.GridBox(header_widgets + row_widgets, layout=ipywidgets.Layout(
            grid_template_columns=f'40% repeat({len(headers) - 1}, auto)',
            grid_gap='2px',
            padding='5px'
        ))

    def _create_install_button(self, description, package, pip_path, mode):
        button = ipywidgets.Button(description=description)
        button.on_click(lambda btn: self._install_package(package, pip_path, mode, btn))
        return button

    def _create_package_tabs(self, packages, config):
        tab_contents = {}
        for category in self._categories:
            content = self._create_table_grid(packages[category], config,
                                              mode=category)
            tab_contents[category] = content

        # Create a Tab widget and add content
        tab = ipywidgets.Tab(layout=ipywidgets.Layout(overflow='auto', height='93%', padding='0px'))
        tab.children = [tab_contents[cat] for cat in self._categories]

        # Set tab titles
        for i, category in enumerate(self._categories):
            tab.set_title(i, f"{category} packages".capitalize())

        return tab

    def _general_install_packages(self, b):
        package_name = self._package_input.value
        mode = self._package_scope_dropdown.value
        version = self._package_version_dropdown.value
        pip_path = self._config.get(version, {}).get("pip_path")

        if package_name and mode and pip_path:
            self._package_input.value = ''
            self._install_package(package_name, pip_path, mode)

    def _install_package(self, package, pip_path, mode, button=None):
        import subprocess
        from IPython.display import clear_output
        self._tabs.selected_index = 3
        if button:
            button.disabled = True
            button.description = "Installing"
        with self._console:
            clear_output(wait=True)
            print(f"Installing latest version of {package} ...")
            try:
                env = os.environ.copy()
                install_commands = [pip_path, 'install']
                if mode == "global":
                    env['PYTHONUSERBASE'] = self._global_base
                    install_commands.append("--ignore-installed")
                subprocess.run(install_commands + [package], env=env, check=True)
                if button:
                    button.description = "Installed"
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}:")
                if e.stderr:
                    print(e.stderr.decode('utf-8'))
                if button:
                    button.description = "Install Locally"
                    button.disabled = False
        extra_props = {EventConstants.INSTALLED_PACKAGE_NAME : package}
        self._track(EventConstants.EVENT_NAME_PACKAGE_INSTALL, extra_props)
        if self._loop and self._loop.is_running():
            asyncio.create_task(self._update_packages_section_wrap())
        else:
            asyncio.run(self._update_packages_section_wrap())

    def _clear_output_terminal(self, button):
        from IPython.display import clear_output
        with self._console:
            clear_output()

    def _parse_notebooks(self, directory="."):
        data = []
        ignore_folders = {'SPy Documentation'}

        def add_to_data(path, last_modified, kernel):
            parts = path.split(os.sep)
            dir_path = os.sep.join(parts[:-1])
            file_name = parts[-1]
            data.append((dir_path, file_name, last_modified, kernel))

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ignore_folders]

            for file in files:
                if file.endswith('.ipynb'):
                    abs_path = os.path.join(root, file)
                    path = os.path.relpath(abs_path, start=directory)
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        nb = nbformat.read(f, as_version=4)
                        kernel_display_name = nb.get('metadata', {}).get('kernelspec', {}).get('display_name', '-')
                        kernel = nb.get('metadata', {}).get('kernelspec', {}).get('name', None)
                        if kernel and kernel=='python3':
                            kernel_display_name = "Python 3.8"
                    last_modified_time = datetime.fromtimestamp(os.path.getmtime(abs_path)).astimezone(self._user_timezone)
                    last_modified = last_modified_time.strftime(self._datetime_format)

                    add_to_data(path, last_modified, kernel_display_name)

        # Create a MultiIndex DataFrame
        index = pd.MultiIndex.from_tuples(data, names=['Directory', 'Notebook Name', 'Last Modified',
                                                       'Selected Kernel'])
        return pd.DataFrame(index=index).sort_values(by=['Directory', 'Notebook Name'])

    def _get_all_projects(self, ):
        prev = 0
        limit = 1000
        name_max_length = 38
        project_type_map = {"DATA_LAB": "Data Lab", "DATA_LAB_FUNCTIONS": "Data Lab Functions"}
        projects = []
        self._project_report_progress_bar.value += 10

        def get_projects(offset=None, limit=None):
            try:
                body =  {"action": "LOCAL_PYTHON_PACKAGES"}
                params = {'offset':offset, 'limit':limit}
                url = urljoin(spy.session.private_url, 'data-lab-management')
                headers = {}
                spy.session.client.add_authorization_header(headers)
                headers.update(spy.session.client.default_headers)
                resp = requests.post(url, json=body, params=params, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except:
                return self._projects_api.get_projects(offset=offset, limit=limit).to_dict()
        
        while True:
            resp = get_projects(offset=prev, limit=limit)
            prev += limit
            for project in resp.get('projects',[]):
                x = dict()
                project_name = project.get('name')
                x["project_name"] = project_name if len(project_name) <= name_max_length \
                    else project_name[:name_max_length - 3] + '...'
                x["type"] = project.get('type')
                x["id"] = project.get('id')
                owner = project.get('owner', {})
                x["owner_name"] = owner.get('name', None) if owner else None
                creator = project.get('creator', {})
                x["creator_name"] = creator.get('name', None) if creator else None
                project_type = project.get('project_type',None) or project.get('projectType')
                x["project_type"] = project_type_map.get(project_type, "Data Lab")
                x["updated_at"] = project.get('updated_at',None) or project.get('updatedAt')
                scheduled_notebook_status = 'None'
                scheduled_notebooks = project.get('scheduled_notebooks',None) or project.get('scheduledNotebooks')
                if scheduled_notebooks:
                    if any(not schedule.get('stopped') for sn in scheduled_notebooks for schedule in sn.get('schedules', [])):
                        scheduled_notebook_status = 'Active'
                    elif all(schedule.get('stopped') for sn in scheduled_notebooks for schedule in sn.get('schedules', [])):
                        scheduled_notebook_status = 'Stopped'
                x['scheduled_notebooks'] = scheduled_notebook_status

                compatibility_data = next(
                    (item.get('value',False) for item in project.get('configuration', []) if item.get('name','') == self._is_python311_compatible),
                    None)
                if compatibility_data:
                    compatibility_info = json.loads(compatibility_data)
                else:
                    compatibility_info = dict(verified=False, by=None, on=None)
                x['python311_verified'] = compatibility_info.get('verified', False)
                x['python311_verified_by'] = compatibility_info.get('by', None)

                localPackagePythonVersions = project.get('localPackagePythonVersions', None)
                if localPackagePythonVersions is not None:
                    x['has_local_packages'] = ", ".join(localPackagePythonVersions)
                projects.append(x)
            self._project_report_progress_bar.value += 10
            if resp.get('next',None) is None:
                break
        return projects

    def _get_add_on_ids(self):
        def extract_id(url):
            pattern = r'/([0-9A-F-]{36})/'
            match = re.search(pattern, url)
            return match.group(1) if match else None

        try:
            system_api = SystemApi(spy.session.client)
            return [
                id for tool in system_api.get_add_on_tools().add_on_tools
                if (id := extract_id(tool.target_url)) is not None
            ]
        except Exception as e:
            return []

    def _get_packaged_add_on_ids(self):

        def is_adopted_addon(add_on_identifier):
            import uuid
            uuid_string = add_on_identifier.split(".")[-1]
            try:
                uuid_obj = uuid.UUID(uuid_string, version=4)
                return str(uuid_obj) == uuid_string
            except ValueError:
                return False

        prev = 0
        limit = 1000
        packaged_addon_ids = []
        try:
            add_on_api = AddOnsApi(spy.session.client)
            while True:
                resp = add_on_api.get_add_ons(offset=prev, limit=limit)
                prev += limit
                for ao in resp.add_ons:
                    # The Adopted add-on have the version_string as 0.0.1
                    if ao.version_string == "0.0.1" and is_adopted_addon(ao.add_on_identifier):
                        continue
                    aoc = json.loads(ao.add_on_components)
                    for v in aoc.get("elements", {}).values():
                        if v.get("infrastructure_type") == "AddOnTool":
                            project_id = v.get("properties", {}).get("projectId")
                            if project_id:
                                packaged_addon_ids.append(project_id)
                                break
                if resp.next is None:
                    break
        except Exception as e:
            pass
        return packaged_addon_ids

    def _filter_projects_dataframe(self, from_last_date, scheduled_notebook, project_type, sort_projects_by, python311_verified, local_package):

        today = datetime.utcnow()

        # Determine start date based on the selected filter
        date_options = {
            'Last 1 Month': 30,
            'Last 3 Months': 90,
            'Last 6 Months': 180,
            'Last 1 Year': 365
        }

        if from_last_date in date_options:
            start_date = today - timedelta(days=date_options[from_last_date])
        else:
            start_date = pd.Timestamp.min.tz_localize('UTC')

        start_date = start_date.astimezone(self._user_timezone).strftime(self._datetime_format)
        filtered_df = self.projects_df[self.projects_df['updated_at'] >= start_date]
        if python311_verified != 'All':
            filtered_df = filtered_df[filtered_df['python311_verified'] == eval(python311_verified)]
        if 'has_local_packages' in filtered_df.columns and local_package!="All":
            filtered_df = filtered_df[filtered_df['has_local_packages'].str.contains(local_package)]
        if project_type != 'All':
            filtered_df = filtered_df[filtered_df['project_type'] == project_type]
        if scheduled_notebook != 'All':
            filtered_df = filtered_df[filtered_df['scheduled_notebooks'] == scheduled_notebook]
        if sort_projects_by == "Last Updated":
            filtered_df = filtered_df.sort_values(by='updated_at', ascending=False).reset_index(drop=True)
        elif sort_projects_by == "Project Name":
            filtered_df = filtered_df.sort_values(by='project_name', ascending=True).reset_index(drop=True)
        filtered_df.index += 1

        # Rename columns and format DataFrame for display
        columns = ['name', 'id', 'owner_name', 'creator_name', 'project_type', 'updated_at', 'scheduled_notebooks']
        if 'has_local_packages' in filtered_df.columns:
            columns.append('has_local_packages')
        if self._seeq_major_version >=61:
            columns.append('python311_verified')
        filtered_df = filtered_df[columns]

        filtered_df = filtered_df.rename(columns=self._col_name_maps)

        if self._seeq_major_version >=61:
            style_map_function = getattr(filtered_df.style, 'map', filtered_df.style.applymap)
            filtered_df = style_map_function(
                lambda val: 'background-color: lightgreen;' if val else 'background-color: lightcoral;',
                subset=['Python 3.11 Verified']
            )

        # Display the DataFrame
        with self._project_report_output:
            self._project_report_output.clear_output()
            display(HTML(
                self._full_width_table_css + filtered_df.to_html(max_rows=None, index=True, escape=False,
                                                                 table_id="full-width-table")))

    def _verify_project(self, b):
        # Prepare new configuration
        new_verification_state = not b.project_verified
        config = {
            'verified': new_verification_state,
            'by': spy.user.name or spy.user.username,
            'on': datetime.now(timezone.utc).isoformat()
        }
        self._verify_button.description = 'Loading'
        self._verify_button.disabled = True
        # Update project details
        try:
            project = self._projects_api.get_project(id=self._project_id)
            project_input = ProjectInputV1()
            project_input.name = project.name
            project_input.configuration = [ScalarPropertyV1(name=self._is_python311_compatible, value=json.dumps(config))]
            self._projects_api.put_project(body=project_input, id=self._project_id)
            b.project_verified = new_verification_state
        finally:
            self._verify_button.disabled = False
            self._verify_status_label.value = self._verified_label if b.project_verified else self._not_verified_label
            self._verify_button.description = self._remove_verification_button_desc if b.project_verified else self._mark_verified_button_desc
            self._verify_button.button_style = self._success_button_style if b.project_verified else self._danger_button_style

        self.projects_df.loc[self.projects_df["id"]==self._project_id, "python311_verified"] = new_verification_state
        self._track(EventConstants.EVENT_NAME_VERIFY)

        self._verify_by_label.value = self._verified_by_label.format(config['by'])
        parsed_time = isoparse(config['on']).astimezone(self._user_timezone).strftime(self._datetime_format)
        self._verify_on_label.value = self._verified_on_label.format(parsed_time)
        
        if b.project_verified:
            self._verify_section.children = [self._verify_status_label, self._verify_button, self._verify_by_label, self._verify_on_label]
        else:
            self._verify_section.children = [self._verify_status_label, self._verify_button, self._verify_info_label]

    async def _export_projects(self, button):
        timestamp = datetime.now(timezone.utc).astimezone(self._user_timezone).strftime(self._file_export_datetime_format)
        filename = f"Projects_{timestamp}.csv"

        columns_to_export = ['project_name', 'id', 'url', 'owner_name', 'creator_name', 'project_type', 'updated_at', 'scheduled_notebooks']
        if 'has_local_packages' in self.projects_df.columns:
            columns_to_export.append('has_local_packages')
        if self._seeq_major_version >=61:
            columns_to_export.append('python311_verified')
            columns_to_export.append('python311_verified_by')
            
        df_to_export = self.projects_df[columns_to_export].rename(columns=self._col_name_maps)
        df_to_export.to_csv(filename, index=False)

        button.button_style = self._success_button_style
        await asyncio.sleep(2)
        button.button_style = self._info_button_style

    def _on_export_projects_button_click(self, button):
        if self._loop and self._loop.is_running():
            asyncio.create_task(self._export_projects(button))
        else:
            asyncio.run(self._export_projects(button))

    def _create_base_event(self, event_name):
        project_types = self.projects_df['project_type']
        scheduled_notebooks = self.projects_df['scheduled_notebooks']
        python311_verified = self.projects_df['python311_verified']
        
        is_function = project_types == "Data Lab Functions"
        is_addon = project_types == "Data Lab Add-On"
        is_packaged_addon = project_types == "Data Lab Packaged Add-On"
        is_active_scheduled = scheduled_notebooks == "Active"
        has_schedule = scheduled_notebooks != "None"
        
        num_projects = int(len(self.projects_df))
        num_functions = int(is_function.sum())
        num_addons = int(is_addon.sum())
        num_packaged_addons = int(is_packaged_addon.sum())
        num_completed_projects = int(python311_verified.sum())
        num_scheduled_notebooks = int(has_schedule.sum())
        num_active_scheduled_notebooks = int(is_active_scheduled.sum())
        num_completed_functions = int((is_function & python311_verified).sum())
        num_completed_addons = int((is_addon & python311_verified).sum())
        num_completed_scheduled = int((has_schedule & python311_verified).sum())
        num_completed_active_scheduled = int((is_active_scheduled & python311_verified).sum())

        return {
            EventConstants.DLEM_VERSION: self._version,
            EventConstants.EVENT_VERSION: MIXPANEL_EVENT_VERSION,
            EventConstants.EVENT_NAME: event_name,
            EventConstants.HOSTNAME: self._hostname,
            EventConstants.SEEQ_VERSION: spy.session.server_version,
            EventConstants.USER_ID: spy.session.user.email,
            EventConstants.IS_USER_ADMIN: spy.session.user.is_admin,
            EventConstants.NUMBER_OF_PROJECTS: num_projects,
            EventConstants.NUMBER_OF_FUNCTIONS: num_functions,
            EventConstants.NUMBER_OF_ADDONS: num_addons,
            EventConstants.NUMBER_OF_PACKAGED_ADDONS: num_packaged_addons,
            EventConstants.NUMBER_OF_COMPLETED_PROJECTS: num_completed_projects,
            EventConstants.NUMBER_OF_SCHEDULED_NOTEBOOKS: num_scheduled_notebooks,
            EventConstants.NUMBER_OF_ACTIVE_SCHEDULED_NOTEBOOKS: num_active_scheduled_notebooks,
            EventConstants.NUMBER_OF_COMPLETED_FUNCTIONS: num_completed_functions,
            EventConstants.NUMBER_OF_COMPLETED_ADDONS: num_completed_addons,
            EventConstants.NUMBER_OF_COMPLETED_ACTIVE_SCHEDULED_NOTEBOOKS: num_completed_active_scheduled,
            EventConstants.NUMBER_OF_COMPLETED_SCHEDULED_NOTEBOOKS: num_completed_scheduled
        }
    
    def _track(self, event_name, extra_properties = {}):
        anonymous_props = [EventConstants.USER_ID]
        if self._mixpanel:
            properties = self._create_base_event(event_name)
            properties.update(extra_properties)
            self._mixpanel.track(distinct_id=spy.session.user.email, 
                                event_name=event_name,
                                properties=properties,
                                anonymous_props=anonymous_props)
