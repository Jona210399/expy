from dotenv import dotenv_values


class EnvironmentEmptyError(Exception):
    ENVIRONMENT_EMPTY_ERROR_MESSAGE = (
        f"The specified environment file either does not exist or is empty."
    )
    pass


class EnvironmentLoader:
    def __init__(
        self,
        enivronment_filename: str,
    ) -> None:
        self.environment_variables = dotenv_values(enivronment_filename)
        self._verify_dotenv()
        self._auto_parse_values()

    def _verify_dotenv(self) -> None:
        if not self.environment_variables:
            raise EnvironmentEmptyError(
                EnvironmentEmptyError.ENVIRONMENT_EMPTY_ERROR_MESSAGE
            )

    def _auto_parse_values(self) -> None:
        for key, value in self.environment_variables.items():
            if value.lower() == "none":
                self.environment_variables[key] = None
                continue

            if value.lower() == "true":
                self.environment_variables[key] = True
                continue

            if value.lower() == "false":
                self.environment_variables[key] = False
                continue

            try:
                number = float(value)
                if number.is_integer():
                    number = int(number)

                self.environment_variables[key] = number
            except ValueError:
                pass

    def get_variables(self) -> dict[str, str | int | float]:
        return self.environment_variables
