from argparse import Namespace


class Arguments:
    def __init__(
        self,
        args: Namespace,
    ) -> None:
        self.__log = str(args.log)
        self.__output_dir = str(args.output_dir)

    @property
    def log_level(self) -> str:
        return self.__log

    @property
    def output_dir(self) -> str:
        return self.__output_dir

    def get_arguments_summary(self) -> str:
        s_str = Arguments.__name__
        s_str += "\n=======================\n"
        s_str += f"log_level='{self.log_level}'\n"
        s_str += f"output_dir='{self.output_dir}'\n"

        return s_str
