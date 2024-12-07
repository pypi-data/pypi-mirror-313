import shutil
from pathlib import Path

from setuptools import setup
from setuptools_rust import build_rust


class build_rust_with_wasm_codecs(build_rust):
    def run(self):
        super().run()

        build_ext = self.get_finalized_command("build_ext")
        ext_path = build_ext.get_ext_fullpath("dummy")

        build_dir = Path(ext_path).parent
        wasm_codecs_dir = build_dir / "fcbench" / "data" / "codecs"
        self.mkpath(str(wasm_codecs_dir))

        for codec in (Path(".") / "data" / "codecs").iterdir():
            if codec.suffix in [".wasm", ".toml"]:
                shutil.copy2(codec, wasm_codecs_dir / codec.name)


# all other parameters are taken from the pyproject.toml file
setup(cmdclass=dict(build_rust=build_rust_with_wasm_codecs))
