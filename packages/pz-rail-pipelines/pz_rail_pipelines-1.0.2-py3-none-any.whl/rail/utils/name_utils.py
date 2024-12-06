"""
Utility code to help define standard paths for various data products
"""

import copy
# import enum
import re
from functools import partial
from typing import Any


CommonPaths = dict(
    root='.',
    scratch_root='.',
    project='',
    project_dir='{root}/projects/{project}',
    project_scratch_dir='{scratch_root}/projects/{project}',
    catalogs_dir='{root}/catalogs',
    pipelines_dir='{project_dir}/pipelines',
)

PathTemplates = dict(
    pipeline_path="{pipelines_dir}/{pipeline}_{flavor}.yaml",
    ceci_output_dir="{project_dir}/data/{selection}_{flavor}",
    ceci_file_path="{tag}_{stage}.{suffix}",
)


def _get_required_interpolants(template: str) -> list[str]:
    """ Get the list of interpolants required to format a template string

    Notes
    -----
    'interpolants' are strings that must be replaced in to format a string,
    e.g., in "{project_dir}/models" "{project_dir}" would an interpolant
    """
    return re.findall('{.*?}', template)


def _format_template(template: str, **kwargs: Any) -> str:
    """ Resolve a specific template

    This is fault-tolerant and will not raise KeyError if some
    of the required interpolants are missing, but rather just
    leave them untouched
    """

    required_interpolants = re.findall('{.*?}', template)
    interpolants = kwargs.copy()

    for interpolant_ in required_interpolants:
        interpolants.setdefault(interpolant_.replace('}', '').replace('{', ''), interpolant_)
    return template.format(**interpolants)


def _resolve_dict(source: dict, interpolants: dict) -> dict:
    """ Recursively resolve a dictionary using interpolants

    Parameters
    ----------
    source: dict
        Dictionary of string templates

    interpolants: dict
        Dictionary of strings used to resolve templates

    Returns
    -------
    sink : dict
        Dictionary of resolved templates
    """
    if source:
        sink = copy.deepcopy(source)
        for k, v in source.items():
            v_interpolated: list | dict | str = ""
            match v:
                case dict():
                    v_interpolated = _resolve_dict(source[k], interpolants)
                case list():
                    v_interpolated = [_resolve_dict(_v, interpolants) for _v in v]
                case str():
                    v_interpolated = v.format(**interpolants)
                case _:
                    raise ValueError("Cannot interpolate type!")

            sink[k] = v_interpolated
    else:
        sink = {}

    return sink


def _resolve(templates: dict, source: dict, interpolants: dict) -> dict:
    """ Resolve a set of templates using interpolants and allow for overrides

    Parameters
    ----------
    templates: dict
        Dictionary of string templates

    source: dict
        Dictionary of overrides

    interpolants: dict
        Dictionary of strings used to resolve templates


    Returns
    -------
    sink : dict
        Dictionary of resoluved templates
    """

    sink = copy.deepcopy(templates)
    if (overrides := source) is not None:
        for k, v in overrides.items():
            sink[k] = v
    for k, v in sink.items():
        match v:
            case partial():
                sink[k] = v(**sink)
            case _:
                continue
    sink = _resolve_dict(sink, interpolants)
    return sink


class NameFactory:
    """ Class defining standard paths for various data products

    """
    config_template = dict(
        CommonPaths = CommonPaths,
        PathTemplates = PathTemplates,
    )

    def __init__(
        self,
        config: dict | None=None,
        templates: dict | None=None,
        interpolants: dict | None=None,
    ):
        """ C'tor

        """
        if config is None:
            config = {}
        if templates is None:
            templates = {}
        if interpolants is None:
            interpolants = {}

        self._config = copy.deepcopy(self.config_template)
        for key, _val in config.items():
            if key in self._config:
                self._config[key].update(**config[key])
        self._templates = copy.deepcopy(self._config['PathTemplates'])
        self._templates.update(**templates)
        self._interpolants: dict = {}

        self.templates = {}
        for k, v in templates.items():
            self.templates[k] = partial(v.format, **templates)

        self.interpolants = self._config['CommonPaths']
        self.interpolants = interpolants

    def get_path_templates(self) -> dict:
        return self._config['PathTemplates']

    def get_common_paths(self) -> dict:
        return self._config['CommonPaths']

    @property
    def interpolants(self) -> dict:
        """ Return the dict of interpolants that are used to resolve templates """
        return self._interpolants

    @interpolants.setter
    def interpolants(self, config: dict) -> None:
        """ Update the dict of interpolants that are used to resolve templates """
        for key, value in config.items():
            new_value = value.format(**self.interpolants)
            self.interpolants[key] = new_value

    @interpolants.deleter
    def interpolants(self) -> None:
        """ Reset the dict of interpolants that are used to resolve templates"""
        self._interpolants = {}

    def resolve_from_config(self, config: dict) -> dict:
        """ Resolve all the templates in a dict

        Parameters
        ----------
        config: dict
            Dictionary containing templates to be resolved

        Returns
        -------
        resolved: dict
            Dictionary with resolved versions of the templates
        """
        resolved = _resolve(
            self.templates,
            config,
            self.interpolants,
        )
        config.update(resolved)

        return resolved

    def resolve_path(self, config: dict, path_key: str, **kwargs: Any) -> str:
        """ Resolve a particular template in a config dict

        Parameters
        ----------
        config: dict
            Dictionary containing templates to be resolved

        path_key: str
            Key for the specific template

        Returns
        -------
        formatted: str
            Resolved version of the template
        """
        if (path_value := config.get(path_key)) is not None:
            formatted = _format_template(path_value, **kwargs, **self.interpolants)
        else:
            raise KeyError(f"Path '{path_key}' not found in {config}")
        return formatted


    def get_template(self, section_key: str, path_key: str) -> str:
        """ Return the template for a particular file type

        Parameters
        ----------
        section_key: str
            Which part of the config to look in
            E.g., (CommonPaths, PathTemplates, Files)

        path_key: str
            Key for the specific template

        Returns
        -------
        the_template: str
            Template for file of this type
        """
        try:
            section = self._config[section_key]
        except KeyError as msg:
            raise KeyError(
                f"Config section {section_key} not present:"
                f"available sections are {list(self._config.keys())}",
            ) from msg
        try:
            return section[path_key]
        except KeyError as msg:
            raise KeyError(
                f"Config key {path_key} not present in {section_key}:"
                f"available paths are {list(section.keys())}",
            ) from msg

    def resolve_template(self, section_key: str, path_key: str, **kwargs: Any) -> str:
        """ Return the template for a particular file type

        Parameters
        ----------
        section_key: str
            Which part of the config to look in
            E.g., (CommonPaths, PathTemplates, Files)

        path_key: str
            Key for the specific template

        Returns
        -------
        resovled: str
            Resolved path
        """
        template = self.get_template(section_key, path_key)
        return _format_template(template, **self.interpolants, **kwargs)

    def resolve_path_template(self, path_key: str, **kwargs: Any) -> str:
        """ Return a particular path templated

        Parameters
        ----------
        path_key: str
            Key for the specific template

        Returns
        -------
        resovled: str
            Resolved path
        """
        template = self.get_template('PathTemplates', path_key)
        interp_dict = self.interpolants.copy()
        interp_dict.update(**kwargs)
        return _format_template(template, **interp_dict)


    def resolve_common_path(self, path_key: str, **kwargs: Any) -> str:
        """ Return a particular common path template

        Parameters
        ----------
        path_key: str
            Key for the specific template

        Returns
        -------
        resovled: str
            Resolved path
        """
        template = self.get_template('CommonPaths', path_key)
        interp_dict = self.interpolants.copy()
        interp_dict.update(**kwargs)
        return _format_template(template, **interp_dict)
