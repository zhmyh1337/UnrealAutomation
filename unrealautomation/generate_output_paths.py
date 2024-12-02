import subprocess
import os
from datetime import datetime
from . import config
from . import ctx


def execute():
    target_name = config['TargetName']
    build_platform = config['BuildPlatform']
    build_configuration = config['BuildConfiguration']
    output_name = f"{target_name}_{build_platform}_{build_configuration}"
    if hasattr(ctx, 'last_commit'):
        output_name += "_" + ctx.last_commit
    if config['IncludeTimestamp']:
        current_timestamp = datetime.now()
        output_name += "_" + current_timestamp.strftime("%d-%m-%Y_%H-%M-%S")

    ctx.output_name = output_name
    ctx.output_dir = os.path.abspath(config['OutputDir'])
    ctx.unreal_archive_dir = os.path.join(ctx.output_dir, output_name)

    print(f'unreal_archive_dir = {ctx.unreal_archive_dir}')

    return True
