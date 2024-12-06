import sys,os
from modelbuilder.src.assetmodelbuilder import _asset_model_builder_ as cli_builder, build

__all__ = ["build"]

def __cli_entrypoint__():
    cli_builder()
