import subprocess
import os
from . import config
from . import ctx


def execute():
    engine_dir = config['EngineDir']
    uproject_path = config['UprojectPath']
    target_name = config['TargetName']
    build_configuration = config['BuildConfiguration']
    build_platform = config['BuildPlatform']
    archive_dir = ctx.output_dir

    command = [
        fr"{engine_dir}/Engine/Build/BatchFiles/RunUAT.bat",
        f"-ScriptsForProject={uproject_path}",
        "Turnkey", 
        "-command=VerifySdk",
        f"-platform={build_platform}",
        "-UpdateIfNeeded",
        "-EditorIO",
        "-EditorIOPort=54570",
        f"-project={uproject_path}",
        "BuildCookRun",
        "-nop4",
        "-utf8output",
        "-nocompileeditor",
        "-skipbuildeditor",
        "-cook",
        f"-project={uproject_path}",
        f"-target={target_name}",
        fr'-unrealexe={engine_dir}/Engine/Binaries/Win64/UnrealEditor-Cmd.exe',
        f"-platform={build_platform}",
        "-installed",
        "-stage",
        "-archive",
        "-package",
        "-build",
        "-pak",
        "-iostore",
        "-compressed",
        "-prereqs",
        f"-archivedirectory={archive_dir}",
        f"-clientconfig={build_configuration}",
        "-nocompile",
        "-nocompileuat"
    ]

    result = subprocess.run(command)

    return result.returncode == 0
