from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    robot_env: str = 'local'
    robot_user: str = 'user'
    robot_password: str = 'password'
    robot_data_folder: str = './.data'
    robot_data_db_folder: str = 'vector_db'
    robot_data_db_folder_src: str = 'src'
    robot_data_db_folder_out: str = 'out'
    robot_data_db_folder_store: str = 'store'
    robot_data_db_retention_days: float = 60
    robot_task_max_concurrent: int = os.cpu_count() or 1
    robot_task_retention_days: float = 1
    robot_cms_host: str = ''
    robot_cms_auth: str = ''
    robot_cms_db_folder: str = 'llmVectorDb'
    robot_cms_kb_folder: str ='llmKbFile'
    robot_debugger_openai_key: str = ''
    model_config = ConfigDict(
        env_file='./.env',
        extra='ignore',
        case_sensitive=False
    )

    class RuntimeOptions(BaseModel):
        @staticmethod
        def _get_number_of_workers() -> int:
            """
            Returns the number of worker processes to use for the application.

            This function inspects the command-line arguments to determine the number
            of worker processes to use. It looks for the "--workers" argument and
            returns the subsequent value as an integer.
            Sample of command-line arguments:
            fastapi dev main.py --port 6001
            fastapi run main.py --port 6001 --workers 4
            uvicorn main:app --port 6001 --workers 4

            Returns:
                Optional[int]: The number of worker processes to use, or 1 if
                               the argument is not found or the value is invalid.
            """
            import sys
            try:
                for i, arg in enumerate(sys.argv):
                    if arg == "--workers" and i + 1 < len(sys.argv):
                        return int(sys.argv[i + 1])
            except (ValueError, IndexError):
                pass
            return 1
        debug: bool
        loader_strategy: str
        loader_show_progress: bool
        loader_silent_errors: bool
        number_of_workers: int = _get_number_of_workers()
        is_multi_process: bool = _get_number_of_workers() > 1


    def runtime_options(self) -> RuntimeOptions:
      """_summary_
      Returns:
          _runtime_options:
            return degug flag and loader options based on the robot environment.
            the loader options is usefull to minimizing sytem requirements/dependencies for local development
      """
      if self.robot_env == "local":
        return self.RuntimeOptions(debug=True,loader_strategy="auto",loader_show_progress=True, loader_silent_errors=True)
      elif self.robot_env == "development":
        return self.RuntimeOptions(debug=True,loader_strategy="",loader_show_progress=True, loader_silent_errors=False)
      else:
        return self.RuntimeOptions(debug=False,loader_strategy="",loader_show_progress=False, loader_silent_errors=True)

# global instance
config = Settings()

