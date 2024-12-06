import asyncio
import os
import shutil
import pytest
import sys

from py2docfx.convert_prepare.environment import create_environment
from py2docfx.convert_prepare.environment import remove_environment
from py2docfx.convert_prepare.environment import get_venv_path
from py2docfx.convert_prepare.environment import get_venv_exe
from py2docfx.convert_prepare.environment import install_venv_requirements
from py2docfx.convert_prepare.environment import VENV_REQUIREMENT_MODULES
from py2docfx.convert_prepare.environment import prepare_base_venv
from py2docfx.convert_prepare.environment import get_base_venv_exe
from py2docfx.convert_prepare.environment import get_base_venv_path
from py2docfx.convert_prepare.package_info import PackageInfo
pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_venv_creation_package_install_remove():
    # Test creating a venv
    venv_path = get_venv_path(0)
    await create_environment(venv_path)
    interpreter = get_venv_exe(0)
    assert os.path.exists(interpreter)

    # Test installing requirements
    await install_venv_requirements(0)
    # check if the requirements are installed in the venv
    for module in VENV_REQUIREMENT_MODULES:
        assert os.system(f"{interpreter} -m pip show {module}") == 0

    # Test removing the venv
    await remove_environment(0)
    assert not os.path.exists(interpreter)

@pytest.mark.asyncio
async def test_prepare_base_venv():
    required_package_info = PackageInfo()
    required_package_info.install_type = PackageInfo.InstallType.PYPI
    required_package_info.name = "azure-core"

    await prepare_base_venv([required_package_info], "", "")
    interpreter = get_base_venv_exe()
    assert os.path.exists(interpreter)
    # check if the requirements are installed in the venv
    requrirements = ["setuptools", "sphinx", "pyyaml", "jinja2", "wheel", "azure-core"]
    for module in requrirements:
        assert os.system(f"{interpreter} -m pip show {module}") == 0

    # remove base venv
    base_venv_path = get_base_venv_path()
    shutil.rmtree(base_venv_path)