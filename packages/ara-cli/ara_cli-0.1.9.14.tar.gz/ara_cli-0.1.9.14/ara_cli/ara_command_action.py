from os.path import join
import os
import sys
import json
from ara_cli.output_suppressor import suppress_stdout
from . import whitelisted_commands


def check_validity(condition, error_message):
    if not condition:
        print(error_message)
        sys.exit(1)


def create_action(args):
    from ara_cli.artefact_creator import ArtefactCreator
    from ara_cli.classifier import Classifier
    from ara_cli.filename_validator import is_valid_filename
    from ara_cli.template_manager import SpecificationBreakdownAspects

    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    def handle_parent_arguments(args):
        parent_classifier = args.parent_classifier if hasattr(args, "parent_classifier") else None
        parent_name = args.parent_name if hasattr(args, "parent_name") else None
        if parent_classifier and parent_name:
            check_validity(Classifier.is_valid_classifier(parent_classifier), "Invalid parent classifier provided. Please provide a valid classifier")
            check_validity(is_valid_filename(parent_name), "Invalid filename provided for parent. Please provide a valid filename.")
            return parent_classifier, parent_name
        return None, None

    def handle_aspect_creation(args):
        aspect = args.aspect if hasattr(args, "aspect") else None
        if args.parameter and args.classifier and aspect:
            sba = SpecificationBreakdownAspects()
            try:
                sba.create(args.parameter, args.classifier, aspect)
                return True
            except ValueError as ve:
                print(f"Error: {ve}")
                sys.exit(1)
        return False

    parent_classifier, parent_name = handle_parent_arguments(args)
    if handle_aspect_creation(args):
        return

    template_path = join(os.path.dirname(__file__), 'templates')
    artefact_creator = ArtefactCreator()
    artefact_creator.run(args.parameter, args.classifier, template_path, parent_classifier, parent_name)


def delete_action(args):
    from ara_cli.artefact_deleter import ArtefactDeleter

    artefact_deleter = ArtefactDeleter()
    artefact_deleter.delete(args.parameter, args.classifier, args.force)


def rename_action(args):
    from ara_cli.artefact_renamer import ArtefactRenamer
    from ara_cli.classifier import Classifier
    from ara_cli.filename_validator import is_valid_filename

    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")
    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.aspect), "Invalid new filename provided. Please provide a valid filename.")

    artefact_renamer = ArtefactRenamer()
    artefact_renamer.rename(args.parameter, args.aspect, args.classifier)


def list_action(args):
    from ara_cli.artefact_lister import ArtefactLister
    from ara_cli.list_filter import ListFilter

    branch_classifier, branch_artefact_name = args.branch_args
    children_classifier, children_artefact_name = args.children_args
    data_classifier, data_artefact_name = args.data_args

    artefact_lister = ArtefactLister()

    list_filter = ListFilter(
        # include_content=args.include_content,
        # exclude_content=args.exclude_content,
        include_extension=args.include_extension,
        exclude_extension=args.exclude_extension
    )

    if branch_classifier and branch_artefact_name:
        artefact_lister.list_branch(
            classifier=branch_classifier,
            artefact_name=branch_artefact_name,
            list_filter=list_filter
        )
        return

    if children_classifier and children_artefact_name:
        artefact_lister.list_children(
            classifier=children_classifier,
            artefact_name=children_artefact_name,
            list_filter=list_filter
        )
        return

    if data_classifier and data_artefact_name:
        artefact_lister.list_data(
            classifier=data_classifier,
            artefact_name=data_artefact_name,
            list_filter=list_filter
        )
        return

    if (args.tags):
        artefact_lister.list_files(tags=args.tags, list_filter=list_filter)
        return
    artefact_lister.list_files(list_filter=list_filter)


def list_tags_action(args):
    from ara_cli.tag_extractor import TagExtractor

    tag_extractor = TagExtractor()
    tags = tag_extractor.extract_tags()

    if args.json:
        output = json.dumps({"tags": tags})
        print(output)
        return

    output = "\n".join(f"- {tag}" for tag in tags)
    print(output)


def prompt_action(args):
    from ara_cli.classifier import Classifier
    from ara_cli.filename_validator import is_valid_filename

    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    classifier = args.classifier
    param = args.parameter
    init = args.steps

    def handle_init():
        from ara_cli.prompt_handler import initialize_prompt_templates
        initialize_prompt_templates(classifier, param)

    def handle_init_rag():
        from ara_cli.prompt_handler import initialize_prompt_templates
        from ara_cli.prompt_rag import search_and_add_relevant_files_to_prompt_givens
        initialize_prompt_templates(classifier, param)
        search_and_add_relevant_files_to_prompt_givens(classifier, param)

    def handle_load():
        from ara_cli.prompt_handler import load_selected_prompt_templates
        load_selected_prompt_templates(classifier, param)

    def handle_send():
        from ara_cli.prompt_handler import create_and_send_custom_prompt
        create_and_send_custom_prompt(classifier, param)

    def handle_load_and_send():
        from ara_cli.prompt_handler import load_selected_prompt_templates, create_and_send_custom_prompt
        load_selected_prompt_templates(classifier, param)
        create_and_send_custom_prompt(classifier, param)

    def handle_extract():
        from ara_cli.prompt_extractor import extract_and_save_prompt_results
        from ara_cli.update_config_prompt import update_artefact_config_prompt_files
        extract_and_save_prompt_results(classifier, param)
        print(f"automatic update after extract")
        update_artefact_config_prompt_files(classifier, param, automatic_update=True)

    def handle_chat():
        from ara_cli.prompt_chat import initialize_prompt_chat_mode
        chat_name = args.chat_name
        reset = args.reset
        output_mode = args.output_mode
        append_strings = args.append
        restricted = args.restricted
        initialize_prompt_chat_mode(classifier, param, chat_name, reset=reset, output_mode=output_mode, append_strings=append_strings, restricted=restricted)

    def handle_update():
        from ara_cli.update_config_prompt import update_artefact_config_prompt_files
        update_artefact_config_prompt_files(classifier, param, automatic_update=True)

    command_dispatcher = {
        'init': handle_init,
        'init-rag': handle_init_rag,
        'load': handle_load,
        'send': handle_send,
        'load-and-send': handle_load_and_send,
        'extract': handle_extract,
        'chat': handle_chat,
        'update': handle_update,
    }

    if init in command_dispatcher:
        command_dispatcher[init]()
    else:
        raise ValueError(f"Unknown command '{init}' provided.")


def chat_action(args):
    from ara_cli.chat import Chat

    reset = args.reset
    output_mode = args.output_mode
    append_strings = args.append
    restricted = args.restricted

    chat_name = "chat"
    if args.chat_name:
        chat_name = args.chat_name
    cwd = os.getcwd()
    chat_file_path = join(cwd, chat_name)

    with suppress_stdout(output_mode):
        chat = Chat(chat_file_path, reset=reset) if not restricted else Chat(chat_file_path, reset=reset, enable_commands=whitelisted_commands)

    if append_strings:
        chat.append_strings(append_strings)

    if output_mode:
        chat.start_non_interactive()
        return
    chat.start()


def template_action(args):
    from ara_cli.classifier import Classifier
    from ara_cli.template_manager import TemplatePathManager

    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")

    template_manager = TemplatePathManager()
    content = template_manager.get_template_content(args.classifier)

    print(content)


def fetch_templates_action(args):
    import shutil
    from ara_cli.ara_config import ConfigManager
    from ara_cli.template_manager import TemplatePathManager

    config = ConfigManager().get_config()
    prompt_templates_dir = config.local_prompt_templates_dir
    template_base_path = TemplatePathManager.get_template_base_path()
    global_prompt_templates_path = join(template_base_path, "prompt-modules")

    subdirs = ["commands", "rules", "intentions", "blueprints"]

    os.makedirs(join(prompt_templates_dir, "global-prompt-modules"), exist_ok=True)
    for subdir in subdirs:
        target_dir = join(prompt_templates_dir, "global-prompt-modules", subdir)
        source_dir = join(global_prompt_templates_path, subdir)
        os.makedirs(target_dir, exist_ok=True)
        for item in os.listdir(source_dir):
            source = join(source_dir, item)
            target = join(target_dir, item)
            shutil.copy2(source, target)


def read_action(args):
    from ara_cli.artefact_reader import ArtefactReader
    from ara_cli.artefact import Artefact
    from ara_cli.file_classifier import FileClassifier

    classifier = args.classifier
    artefact_name = args.parameter
    read_mode = args.read_mode

    content, file_path = ArtefactReader.read_artefact(artefact_name=artefact_name, classifier=classifier)

    artefacts_by_classifier = {classifier: []}
    file_classifier = FileClassifier(os)
    classified_artefacts = file_classifier.classify_files()

    match read_mode:
        case "branch":
            ArtefactReader.step_through_value_chain(
                artefact_name=artefact_name,
                classifier=classifier,
                artefacts_by_classifier=artefacts_by_classifier,
                classified_artefacts=classified_artefacts
            )
            file_classifier.print_classified_files(artefacts_by_classifier, print_content=True)
        case "children":
            artefacts = ArtefactReader.find_children(
                artefact_name=artefact_name,
                classifier=classifier,
                classified_artefacts=classified_artefacts
            )
            file_classifier.print_classified_files(
                files_by_classifier=artefacts,
                print_content=True
            )
        case _:
            artefact = Artefact.from_content(content)
            artefact_path = next((classified_artefact.file_path for classified_artefact in classified_artefacts.get(classifier, []) if classified_artefact.name == artefact.name), artefact)
            artefact._file_path = artefact_path
            artefacts_by_classifier[classifier].append(artefact)
            file_classifier.print_classified_files(artefacts_by_classifier, print_content=True)
