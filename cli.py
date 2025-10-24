#!/usr/bin/env python3
def main():
    import argparse
    from .core import run_from_cli

    parser = argparse.ArgumentParser(
        prog="nocturne",
        description="Nocturne CLI (modo educativo)"
    )
    # aquí subcomandos y opciones bueno, si es que sigo en este proyecto
    args = parser.parse_args()
    run_from_cli(args)
