"""Parser for an `PythonJob` job."""

from aiida.engine import ExitCode
from aiida.parsers.parser import Parser

from aiida_pythonjob.data.serializer import general_serializer


class PythonJobParser(Parser):
    """Parser for an `PythonJob` job."""

    def parse(self, **kwargs):
        """Parse the contents of the output files stored in the `retrieved` output node.

        The function_outputs could be a namespce, e.g.,
        function_outputs=[
            {"identifier": "namespace", "name": "add_multiply"},
            {"name": "add_multiply.add"},
            {"name": "add_multiply.multiply"},
            {"name": "minus"},
        ]
        """
        import pickle

        function_outputs = self.node.inputs.function_data.get_dict()["outputs"]
        if len(function_outputs) == 0:
            function_outputs = [{"name": "result"}]
        self.output_list = function_outputs
        # first we remove nested outputs, e.g., "add_multiply.add"
        top_level_output_list = [output for output in self.output_list if "." not in output["name"]]
        try:
            with self.retrieved.base.repository.open("results.pickle", "rb") as handle:
                results = pickle.load(handle)
                if isinstance(results, tuple):
                    if len(top_level_output_list) != len(results):
                        return self.exit_codes.ERROR_RESULT_OUTPUT_MISMATCH
                    for i in range(len(top_level_output_list)):
                        top_level_output_list[i]["value"] = self.serialize_output(results[i], top_level_output_list[i])
                elif isinstance(results, dict):
                    # pop the exit code if it exists
                    exit_code = results.pop("exit_code", 0)
                    if exit_code:
                        if isinstance(exit_code, dict):
                            exit_code = ExitCode(exit_code["status"], exit_code["message"])
                        elif isinstance(exit_code, int):
                            exit_code = ExitCode(exit_code)
                        return exit_code
                    if len(top_level_output_list) == 1:
                        # if output name in results, use it
                        if top_level_output_list[0]["name"] in results:
                            top_level_output_list[0]["value"] = self.serialize_output(
                                results.pop(top_level_output_list[0]["name"]),
                                top_level_output_list[0],
                            )
                            # if there are any remaining results, raise an warning
                            if len(results) > 0:
                                self.logger.warning(
                                    f"Found extra results that are not included in the output: {results.keys()}"
                                )
                        # otherwise, we assume the results is the output
                        else:
                            top_level_output_list[0]["value"] = self.serialize_output(results, top_level_output_list[0])
                    elif len(top_level_output_list) > 1:
                        for output in top_level_output_list:
                            if output["name"] not in results:
                                if output.get("required", True):
                                    return self.exit_codes.ERROR_MISSING_OUTPUT
                            else:
                                output["value"] = self.serialize_output(results.pop(output["name"]), output)
                        # if there are any remaining results, raise an warning
                        if len(results) > 0:
                            self.logger.warning(
                                f"Found extra results that are not included in the output: {results.keys()}"
                            )

                elif len(top_level_output_list) == 1:
                    # otherwise it returns a single value, we assume the results is the output
                    top_level_output_list[0]["value"] = self.serialize_output(results, top_level_output_list[0])
                else:
                    return self.exit_codes.ERROR_RESULT_OUTPUT_MISMATCH
                for output in top_level_output_list:
                    self.out(output["name"], output["value"])
        except OSError:
            return self.exit_codes.ERROR_READING_OUTPUT_FILE
        except ValueError as exception:
            self.logger.error(exception)
            return self.exit_codes.ERROR_INVALID_OUTPUT

    def find_output(self, name):
        """Find the output with the given name."""
        for output in self.output_list:
            if output["name"] == name:
                return output
        return None

    def serialize_output(self, result, output):
        """Serialize outputs."""

        name = output["name"]
        if output.get("identifier", "Any").upper() == "NAMESPACE":
            if isinstance(result, dict):
                serialized_result = {}
                for key, value in result.items():
                    full_name = f"{name}.{key}"
                    full_name_output = self.find_output(full_name)
                    if full_name_output and full_name_output.get("identifier", "Any").upper() == "NAMESPACE":
                        serialized_result[key] = self.serialize_output(value, full_name_output)
                    else:
                        serialized_result[key] = general_serializer(value)
                return serialized_result
            else:
                self.exit_codes.ERROR_INVALID_OUTPUT
        else:
            return general_serializer(result)
