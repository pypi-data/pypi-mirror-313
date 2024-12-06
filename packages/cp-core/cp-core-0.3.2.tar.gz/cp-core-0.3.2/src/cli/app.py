# coding: utf-8
import sys
import argparse
import traceback
import json
from cp_core.libs.validator.schema import parse_config
from cp_core.libs.validator.parse import process_values


class App:
    @staticmethod
    def get_config_file():
        parser = argparse.ArgumentParser(description="material process")
        parser.add_argument("--f", help="the config file path")

        args = parser.parse_args()
        file_path = args.f

        try:
            with open(file_path, "r") as fp:
                fp = json.load(fp)
        except TypeError as e:
            print("Error: ", e)
            traceback.print_exc(file=sys.stdout)
            return None
        return fp

    @staticmethod
    def entry(f):
        values, msg = parse_config(values=f)
        if not values:
            print(f"Error msg: {msg}")
        else:
            # TODO: interval always be True, might be a error.
            # 20221020
            process_values(values, True)

    def run(self):
        f = self.get_config_file()
        self.entry(f)


if __name__ == "__main__":
    App().run()
