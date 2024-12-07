#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   hierarchical_yaml 
@Time        :   2024/12/4 15:05
@Author      :   Xuesong Chen
@Description :   
"""
import os
import typing as t
from omegaconf import OmegaConf
from omegaconf import DictConfig


def _parse_hierarchy(path: str) -> DictConfig:
    # Resolve path relative to the current working directory (if it's not already absolute)
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(path), path)

    config = t.cast(DictConfig, OmegaConf.load(path))
    base_paths = config.pop("_base", [])

    if isinstance(base_paths, str):
        base_paths = [base_paths]

    # For each base path, resolve it relative to the current path
    bases = []
    for base in base_paths:
        # Handle relative paths by joining with the current config's path
        base_abs_path = os.path.join(os.path.dirname(path), base) if not os.path.isabs(base) else base
        bases.append(_parse_hierarchy(base_abs_path))

    # Merge all base configs with the current config
    return t.cast(DictConfig, OmegaConf.merge(*bases, config))


def parse_hierarchical_yaml(path: str, **kwargs) -> dict[str, t.Any]:
    # Parse the main config file
    file_config = _parse_hierarchy(path)

    # Add any additional kwargs to the configuration
    kwargs_config = OmegaConf.create(kwargs)

    # Merge file config with kwargs config
    config = OmegaConf.merge(file_config, kwargs_config)

    # Resolve all interpolations and return the final config as a dictionary
    resolved_config = t.cast(dict[str, t.Any], OmegaConf.to_container(config, resolve=True))

    return resolved_config
