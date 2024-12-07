import getpass

from . import Constants


class Utils:
    @staticmethod
    def __get_colored_string(input: str, color_code: int) -> str:
        match color_code:
            case 1:
                return f"\033[92m{input}\033[0m"
            case 2:
                return f"\033[93m{input}\033[0m"
            case 3:
                return f"\033[96m{input}\033[0m"
            case _:
                return input

    @staticmethod
    def print(message: str):
        print("\n" + Utils.__get_colored_string(message, 2))

    @staticmethod
    def print_list(input: list[str]):
        print()
        for item in input:
            print("    " + "\u2022 " + Utils.__get_colored_string(item, 3))

    @staticmethod
    def input(prompt: str) -> str:
        return input("\n" + Utils.__get_colored_string(prompt, 1))

    @staticmethod
    def input_password(prompt: str) -> str:
        return getpass.getpass("\n" + Utils.__get_colored_string(prompt, 1))

    @staticmethod
    def get_next_object_name(object_name: str = None) -> str:
        if object_name is None:
            return "a" * Constants.OBJ_NAME_LEN

        object_name_as_num = [0] * Constants.OBJ_NAME_LEN
        for i in range(Constants.OBJ_NAME_LEN):
            object_name_as_num[i] = ord(object_name[i]) - ord("a")

        for i in reversed(range(Constants.OBJ_NAME_LEN)):
            if object_name_as_num[i] != 15:
                object_name_as_num[i] += 1
                break
            else:
                object_name_as_num[i] = 0

        result = [""] * Constants.OBJ_NAME_LEN
        for i in range(Constants.OBJ_NAME_LEN):
            result[i] = chr(object_name_as_num[i] + ord("a"))

        return "".join(result)
