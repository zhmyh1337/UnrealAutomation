import shutil
import os
from . import ctx


def execute():
    base_name = os.path.join(ctx.output_dir, ctx.output_name)
    ctx.archive_path = shutil.make_archive(base_name, 'zip', ctx.unreal_archive_dir)

    print(f'archive_path = {ctx.archive_path}')

    return True
