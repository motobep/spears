from dataclasses import dataclass


@dataclass
class ReplaceImports:
    is_test: bool
    target_import: str

    def change(self, files: list[str], func_and_args: dict):
        self.multichange(files, [func_and_args])

    def multichange(self, files: list[str], func_and_args_dicts: list[dict]):
        print(files)
        for filename in files:
            if self.is_test:
                print(f'<{filename}>:')

            with open(filename, 'r') as file:
              data = file.read()

            try:
                for dict in func_and_args_dicts:
                    func = dict['func']
                    func_args = dict['args']
                    data = func(data, self.target_import, *func_args)
            except Exception as ex:
                print('-------------------')
                print('Exception: ', ex)
                print(f'Passing file: {filename}')
                print('-------------------\n')
                continue

            if self.is_test:
                ...
                # print(f'<{filename}>:')
                # print(data)
            else:
                with open(filename, 'w') as file:
                  file.write(data)

