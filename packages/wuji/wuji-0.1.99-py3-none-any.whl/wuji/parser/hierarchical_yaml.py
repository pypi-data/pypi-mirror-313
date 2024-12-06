#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   hierarchical_yaml 
@Time        :   2024/12/4 15:05
@Author      :   Xuesong Chen
@Description :   
"""
import typing as t
from omegaconf import OmegaConf, DictConfig


def _parse_hierarchy(path: str) -> DictConfig:
    config = t.cast(DictConfig, OmegaConf.load(path))
    base_paths = config.pop("_base", [])
    if isinstance(base_paths, str):
        base_paths = [base_paths]
    bases = [_parse_hierarchy(base) for base in base_paths]
    return t.cast(DictConfig, OmegaConf.merge(*bases, config))


def parse_hierarchical_yaml(path: str, **kwargs) -> dict[str, t.Any]:
    file_config = _parse_hierarchy(path)
    kwargs_config = OmegaConf.create(kwargs)
    config = OmegaConf.merge(file_config, kwargs_config)
    resolved_config = t.cast(
        dict[str, t.Any], OmegaConf.to_container(config, resolve=True)
    )
    return resolved_config
