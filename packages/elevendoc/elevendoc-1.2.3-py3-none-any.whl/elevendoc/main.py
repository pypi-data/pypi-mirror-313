import argparse
import ast
import os
import subprocess
import sys
import textwrap
import time

import astunparse
import black
import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from .utils import (
    extract_key_elements,
    get_function_definitions,
    reorganize_imports_in_directory,
    send_to_chatgpt,
    write_changes_function,
)

"""
from utils import (
    extract_key_elements,
    get_function_definitions,
    process_notebook,
    reorganize_imports_in_directory,
    send_to_chatgpt,
    write_changes_function,
    generate_requirements,
)
"""

####TEST POETRY


# from utils import *

load_dotenv(dotenv_path=".env")


def create_env_file():
    """
    Create a .env file with user-provided information.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    """
    Creer un fichier .env avec les informations de l'utilisateur.

    Parameters:
    - None

    Returns:
    - None
    """

    OPENAI_API_VERSION = input("Veuillez entrer la version de l'api : ")
    AZURE_OPENAI_API_KEY = input("Veuillez entrer la clé de l'API d'Azure : ")
    AZURE_OPENAI_ENDPOINT = input("Veuillez entrer l'endpoint de l'API (URL) : ")
    MODEL_DOCSTRING = input(
        "Veuillez entrer le modèle à utiliser pour générer les docstrings :"
    )
    MODEL_README = input(
        "Veuillez entrer le modèle à utiliser pour générer le README :"
    )
    MODEL_ADVISORY = input(
        "Veuillez entrer le modèle à utiliser pour générer les avis :"
    )

    # Chemin du fichier .env
    env_file_path = os.path.join(os.path.dirname(__file__), ".env")

    # Créer le fichier .env
    with open(env_file_path, "w") as f:
        f.write(f"OPENAI_API_VERSION={OPENAI_API_VERSION}\n")
        f.write(f"AZURE_OPENAI_API_KEY={AZURE_OPENAI_API_KEY}\n")
        f.write(f"AZURE_OPENAI_ENDPOINT={AZURE_OPENAI_ENDPOINT}\n")
        f.write(f"MODEL_DOCSTRING={MODEL_DOCSTRING}\n")
        f.write(f"MODEL_README={MODEL_README}\n")
        f.write(f"MODEL_ADVISORY={MODEL_ADVISORY}\n")

    print(f"Fichier .env créé à : {env_file_path}")


def main(
    root_dir,
    docstring_bool=False,
    Readme_bool=False,
    advisory_bool=False,
    force_bool=False,
    verbose=False,
    requirements_bool=False,
):
    """
    Perform various tasks based on the provided arguments.

    Parameters
    ----------
    root_dir : str
        The root directory where the function will perform its tasks.
    docstring_bool : bool, optional
        Whether to generate docstrings for Python functions. Default is False.
    Readme_bool : bool, optional
        Whether to create a README file. Default is False.
    advisory_bool : bool, optional
        Whether to generate an advisory file. Default is False.
    force_bool : bool, optional
        Whether to forcefully replace existing docstrings. Default is False.
    verbose : bool, optional
        Whether to print detailed logs during execution. Default is False.

    Returns
    -------
    None
    """

    """
    Summary:
    This function performs various tasks based on the provided arguments. It can generate docstrings for Python functions, create a README file, and generate an advisory file. It also reorganizes imports in the specified directory and formats the code using the 'black' tool.

    Parameters:
    - root_dir: A string representing the root directory where the function will perform its tasks.
    - docstring_bool: A boolean indicating whether to generate docstrings for Python functions. Default is False.
    - Readme_bool: A boolean indicating whether to create a README file. Default is False.
    - advisory_bool: A boolean indicating whether to generate an advisory file. Default is False.

    Returns:
    None
    """

    # Chemin du fichier .env
    env_file_path = os.path.join(os.path.dirname(__file__), ".env")

    # Vérifier si le fichier .env existe
    if not os.path.exists(env_file_path):
        print("Aucun fichier .env trouvé. Création d'un nouveau fichier .env.")
        create_env_file()

    # Charger les variables d'environnement
    load_dotenv(dotenv_path=env_file_path)

    start_time = time.time()
    if (not docstring_bool) and (not Readme_bool) and (not advisory_bool):
        print(
            "No arguments provided. Please provide either 'dockstring' or 'Readme' or 'advisory' argument."
        )
        return
    if root_dir[:] == "":
        print("Please provide a valid root directory.")
        return
    Readme_prompt_memory = ""
    Readme_dictionary = {}
    Project_description = input(
        """Pour plus de précision dans les dosctrings, le readme, ou le fichier advisory, 
            veuillez entrer une description la plus complète possible de votre projet tel que:
            - les objectifs du projet
            - les fonctionnalités
            - la hiérarchie des fichiers
            ...
            (TAPEZ 'entrer' pour passer) : """
    )

    if requirements_bool:
        generate_requirements(root_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            nbr_doctring_generated = 0
            nbr_doctring_replaced = 0
            nbr_docstring_unchanged = 0
            file_path = os.path.join(dirpath, filename)
            if docstring_bool:
                if filename.endswith(".ipynb"):
                    process_notebook(
                        file_path,
                        Readme_prompt_memory,
                        force_bool,
                        Project_description,
                        verbose,
                    )
                elif filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    try:
                        file_content = open(file_path, "r").read()
                    except UnicodeDecodeError:
                        print(f"Error reading file: {file_path}. Skipping this file.")
                        continue
                    (function_defs, tree) = get_function_definitions(file_content)
                    function_defs_list = []
                    docstring_list = []
                    for function_def in function_defs:
                        # function_def is now a tuple, so we extract the second element (the actual function definition)
                        if not ast.get_docstring(function_def[1]):

                            docstring = send_to_chatgpt(
                                function_def[1],
                                Readme_dictionary,
                                Project_description,
                                True,
                                False,
                                False,
                                model=os.getenv("MODEL_DOCSTRING"),
                            )
                            docstring_list.append(docstring)
                            function_defs_list.append(function_def)
                            if verbose:
                                print(
                                    f"Docstring generated for: {function_def[1].name}"
                                )
                            nbr_doctring_generated += 1
                        elif force_bool:
                            # delete the existing docstring
                            docstring = send_to_chatgpt(
                                function_def[1],
                                Readme_dictionary,
                                Project_description,
                                True,
                                False,
                                False,
                                model=os.getenv("MODEL_DOCSTRING"),
                            )
                            docstring_list.append(docstring)
                            function_defs_list.append(function_def)
                            if verbose:
                                print(
                                    f"Former Docstring deleted and replaced by a generated one for: {function_def[1].name}"
                                )
                            nbr_doctring_replaced += 1

                        else:
                            if verbose:
                                print(
                                    f"Docstring already present for function: {function_def[1].name}"
                                )
                            nbr_docstring_unchanged += 1
                    write_changes_function(
                        file_path,
                        tree,
                        docstring_list,
                        function_defs_list,
                        force_bool,
                        verbose,
                    )

                    print("---------------------------------------------------------")
                    print(
                        f"""File: {filename} processed successfully.
                            Docstrings generated: {nbr_doctring_generated}
                            Docstrings replaced: {nbr_doctring_replaced}
                            Docstrings unchanged: {nbr_docstring_unchanged}"""
                    )
                    print("---------------------------------------------------------")

            if Readme_bool or advisory_bool:
                Readme_prompt_memory += f"## {dirpath+filename}"
                if filename.endswith(".py"):
                    file_path = os.path.join(dirpath, filename)
                    key_elements = extract_key_elements(file_path)
                    Readme_prompt_memory += f"```python{key_elements}```"
                Readme_prompt_memory += "***\n\n"
    if Readme_bool:
        author = input("Enter the author name: ")
        project_name = input("Enter the project name: ")
        Readme_dictionary["author"] = author
        Readme_dictionary["project_name"] = project_name
        Readme_generation = send_to_chatgpt(
            Readme_prompt_memory,
            Readme_dictionary,
            Project_description,
            False,
            True,
            False,
            model=os.getenv("MODEL_README"),
        )
        with open((root_dir + "/Generated_Readme.md"), "w", encoding="utf-8") as file:
            file.write(Readme_generation)
    if advisory_bool:
        advisory_generation = send_to_chatgpt(
            Readme_prompt_memory,
            Readme_dictionary,
            Project_description,
            False,
            False,
            True,
            model=os.getenv("MODEL_ADVISORY"),
        )
        with open((root_dir + "/Generated_advisory.md"), "w") as file:
            file.write(advisory_generation)
    reorganize_imports_in_directory(root_dir)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Files processed in {elapsed_time} seconds.")
    # Run black formatting on all files in the root directory
    subprocess.run(["black", root_dir])


def run():
    """
    Run the main function with command line arguments.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    """
    Summary:
    This function is the entry point of the program. It takes command line arguments and calls the main function with the provided arguments.

    Parameters:
    - folder: A string representing the root folder containing Python files to process.
    - docstring: A boolean flag indicating whether to add docstrings to the functions in the python files.
    - Readme: A boolean flag indicating whether to generate a Readme file for the python files.
    - advisory: A boolean flag indicating whether to generate an advisory file for the python files.
    - force: A boolean flag indicating whether to generate the docstring even if it is already present.

    Returns:
    None
    """

    parser = argparse.ArgumentParser(
        description="Add docstrings to Python code using ChatGPT."
    )
    parser.add_argument(
        "folder", help="The root folder containing Python files to process."
    )
    parser.add_argument(
        "--docstring",
        help="Add docstring to the functions in the python files.",
        action="store_true",
    )
    parser.add_argument(
        "--Readme",
        help="Generate a Readme file for the python files.",
        action="store_true",
    )
    parser.add_argument(
        "--advisory",
        help="Generate an advisory file for the python files.",
        action="store_true",
    )
    parser.add_argument(
        "--force",
        help="Generate the docstring even if it is already present.",
        action="store_true",
    )
    parser.add_argument(
        "--verbose",
        help="Display verbose output.",
        action="store_true",
    )
    parser.add_argument(
        "--requirements",
        help="Generate a requirements.txt file for the python files.",
        action="store_true",
    )

    args = parser.parse_args()
    main(
        args.folder,
        args.docstring,
        args.Readme,
        args.advisory,
        args.force,
        args.verbose,
        args.requirements,
    )


if __name__ == "__main__":
    run()
