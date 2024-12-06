import os
import cmd2

from ara_cli.prompt_handler import send_prompt


class Chat(cmd2.Cmd):
    CATEGORY_CHAT_CONTROL = "Chat control commands"

    INTRO = """/***************************************/
                 araarar
               aa       ara
             aa    aa   aara
             a        araarar
             a        ar  ar
           aa          ara
          a               a
          a               aa
           a              a
   ar      aa           aa
    (c) ara chat by talsen team
              aa      aa
               aa    a
                a aa
                 aa
/***************************************/
Start chatting (type 'HELP'/'h' for available commands, 'QUIT'/'q' to exit chat mode):"""

    ROLE_PROMPT = "ara prompt"
    ROLE_RESPONSE = "ara response"

    def __init__(
        self,
        chat_name: str,
        reset: bool | None = None,
        enable_commands: list[str] | None = None
    ):
        shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)
        if enable_commands:
            enable_commands.append("quit")  # always allow quitting
            enable_commands.append("eof")  # always allow quitting with ctrl-D
            enable_commands.append("help")  # always allow help

            shortcuts = {key: value for key, value in shortcuts.items() if value in enable_commands}

        super().__init__(
            allow_cli_args=False,
            shortcuts=shortcuts
        )
        self.create_default_aliases()

        if enable_commands:
            all_commands = self.get_all_commands()
            commands_to_disable = [command for command in all_commands if command not in enable_commands]
            self.disable_commands(commands_to_disable)

        self.prompt = "ara> "
        self.intro = Chat.INTRO

        self.default_chat_content = f"# {Chat.ROLE_PROMPT}:\n"
        self.chat_name = self.setup_chat(chat_name, reset)
        self.chat_name = os.path.abspath(self.chat_name)
        self.chat_history = []
        self.message_buffer = []

    def disable_commands(self, commands: list[str]):
        for command in commands:
            setattr(self, f'do_{command}', self.default)
            self.hidden_commands.append(command)
        aliases_to_remove = [alias for alias, cmd in self.aliases.items() if cmd in commands]
        for alias in aliases_to_remove:
            del self.aliases[alias]

    def create_default_aliases(self):
        self.aliases["QUIT"] = "quit"
        self.aliases["q"] = "quit"
        self.aliases["r"] = "RERUN"
        self.aliases["s"] = "SEND"
        self.aliases["c"] = "CLEAR"
        self.aliases["HELP"] = "help"
        self.aliases["h"] = "help"
        self.aliases["n"] = "NEW"
        self.aliases["e"] = "EXTRACT"
        self.aliases["l"] = "LOAD"
        self.aliases["lr"] = "LOAD_RULES"
        self.aliases["li"] = "LOAD_INTENTION"
        self.aliases["lc"] = "LOAD_COMMANDS"
        self.aliases["lg"] = "LOAD_GIVENS"
        self.aliases["lb"] = "LOAD_BLUEPRINT"
        self.aliases["lt"] = "LOAD_TEMPLATE"

    def setup_chat(self, chat_name, reset: bool = None):
        if os.path.exists(chat_name):
            return self.handle_existing_chat(chat_name, reset=reset)
        if os.path.exists(f"{chat_name}.md"):
            return self.handle_existing_chat(f"{chat_name}.md", reset=reset)
        if os.path.exists(f"{chat_name}_chat.md"):
            return self.handle_existing_chat(f"{chat_name}_chat.md", reset=reset)
        return self.initialize_new_chat(chat_name)

    def handle_existing_chat(self, chat_file: str, reset: bool = None):
        chat_file_short = os.path.split(chat_file)[-1]

        if reset is None:
            user_input = input(f"{chat_file_short} already exists. Do you want to reset the chat? (y/N): ")
            if user_input.lower() == 'y':
                self.create_empty_chat_file(chat_file)
        if reset:
            self.create_empty_chat_file(chat_file)
        self.chat_history = self.load_chat_history(chat_file)
        print(f"Reloaded {chat_file_short} content")
        return chat_file

    def initialize_new_chat(self, chat_name: str):
        if chat_name.endswith(".md"):
            chat_name_md = chat_name
        else:
            if not chat_name.endswith("chat"):
                chat_name = f"{chat_name}_chat"
            chat_name_md = f"{chat_name}.md"
        self.create_empty_chat_file(chat_name_md)
        # open(chat_name_md, 'a', encoding='utf-8').close()
        chat_name_md_short = os.path.split(chat_name_md)[-1]
        print(f"Created new chat file {chat_name_md_short}")
        return chat_name_md

    def file_exists_check(method):
        def wrapper(self, file_name, *args, **kwargs):
            file_path = self.determine_file_path(file_name)
            if not file_path:
                print(f"File {file_name} not found.")
                return False
            return method(self, file_path, *args, **kwargs)
        return wrapper

    @staticmethod
    def get_last_role_marker(lines):
        if not lines:
            return
        role_markers = [
            f"# {Chat.ROLE_PROMPT}:",
            f"# {Chat.ROLE_RESPONSE}"
        ]
        for line in reversed(lines):
            stripped_line = line.strip()
            if stripped_line.startswith(tuple(role_markers)):
                return stripped_line
        return None

    def start_non_interactive(self):
        with open(self.chat_name, 'r') as file:
            content = file.read()
        print(content)

    def start(self):
        chat_name = self.chat_name
        directory = os.path.dirname(chat_name)
        os.chdir(directory)
        self.cmdloop()

    def get_last_non_empty_line(self, file) -> str:
        stripped_line = ""
        file.seek(0)
        lines = file.read().splitlines()
        if lines:
            for line in reversed(lines):
                stripped_line = line.strip()
                if stripped_line:
                    break
        return stripped_line

    def get_last_line(self, file):
        file.seek(0)
        lines = file.read().splitlines()
        if lines:
            return lines[-1].strip()
        return ""

    def assemble_prompt(self):
        import re
        from ara_cli.prompt_handler import append_images_to_content

        text_content = []
        image_data_list = []

        image_pattern = re.compile(r'\((data:image/[^;]+;base64,.*?)\)')

        for message in self.chat_history:
            match = image_pattern.search(message)
            if match:
                image_data = {"type": "image_url", "image_url": {"url": match.group(1)}}
                image_data_list.append(image_data)
            else:
                text_content.append(message)

        combined_content = "\n".join(text_content)
        combined_content_with_images = append_images_to_content(combined_content, image_data_list)
        return combined_content_with_images

    def send_message(self):
        self.chat_history = self.load_chat_history(self.chat_name)
        prompt_to_send = self.assemble_prompt()
        role_marker = f"# {Chat.ROLE_RESPONSE}:"

        with open(self.chat_name, 'a+', encoding='utf-8') as file:
            last_line = self.get_last_line(file)

            print(role_marker)

            if not last_line.startswith(role_marker):
                if last_line:
                    file.write("\n")
                file.write(role_marker + "\n")

            for chunk in send_prompt(prompt_to_send):
                print(chunk.content, end="", flush=True)
                file.write(chunk.content)
                file.flush()
            print()

        self.message_buffer.clear()

    def save_message(self, role: str, message: str):
        role_marker = f"# {role}:"
        with open(self.chat_name, 'r', encoding='utf-8') as file:
            stripped_line = self.get_last_non_empty_line(file)
        line_to_write = f"{message}\n\n"
        if stripped_line != role_marker:
            line_to_write = f"\n{role_marker}\n{message}\n"

        with open(self.chat_name, 'a', encoding='utf-8') as file:
            file.write(line_to_write)
        self.chat_history.append(line_to_write)

    def resend_message(self):
        with open(self.chat_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if not lines:
            return
        index_to_remove = self.find_last_reply_index(lines)
        if index_to_remove is not None:
            with open(self.chat_name, 'w', encoding='utf-8') as file:
                file.writelines(lines[:index_to_remove])
        self.send_message()

    def find_last_reply_index(self, lines: list[str]):
        index_to_remove = None
        for i, line in enumerate(reversed(lines)):
            if line.strip().startswith(f"# {Chat.ROLE_PROMPT}"):
                break
            if line.strip().startswith(f"# {Chat.ROLE_RESPONSE}"):
                index_to_remove = len(lines) - i - 1
                break
        return index_to_remove

    def append_strings(self, strings: list[str]):
        output = '\n'.join(strings)
        with open(self.chat_name, 'a') as file:
            file.write(output + '\n')

    def load_chat_history(self, chat_file: str):
        chat_history = []
        if os.path.exists(chat_file):
            with open(chat_file, 'r', encoding='utf-8') as file:
                chat_history = file.readlines()
        return chat_history

    def create_empty_chat_file(self, chat_file: str):
        with open(chat_file, 'w', encoding='utf-8') as file:
            file.write(self.default_chat_content)
        self.chat_history = []

    def add_prompt_tag_if_needed(self, chat_file: str):
        with open(chat_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        prompt_tag = f"# {Chat.ROLE_PROMPT}:"
        if Chat.get_last_role_marker(lines) == prompt_tag:
            return
        append = prompt_tag
        last_line = lines[-1].strip()
        if last_line != "" and last_line != '\n':
            append = f"\n{append}"
        with open(chat_file, 'a', encoding='utf-8') as file:
            file.write(append)

    def determine_file_path(self, file_name: str):
        current_directory = os.path.dirname(self.chat_name)
        file_path = os.path.join(current_directory, file_name)
        if not os.path.exists(file_path):
            file_path = file_name
        if not os.path.exists(file_path):
            print(f"File {file_name} not found")
            return None
        return file_path

    @file_exists_check
    def load_text_file(self, file_path, prefix: str = "", suffix: str = "", block_delimiter: str = ""):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            if block_delimiter:
                file_content = f"{block_delimiter}\n{file_content}\n{block_delimiter}"
        write_content = f"{prefix}{file_content}{suffix}\n"

        with open(self.chat_name, 'a', encoding='utf-8') as chat_file:
            chat_file.write(write_content)
            return True

    @file_exists_check
    def load_binary_file(self, file_path, mime_type: str, prefix: str = "", suffix: str = ""):
        import base64

        with open(file_path, 'rb') as file:
            file_content = file.read()
        base64_image = base64.b64encode(file_content).decode("utf-8")

        write_content = f"{prefix}![{os.path.basename(file_path)}](data:{mime_type};base64,{base64_image}){suffix}\n"

        with open(self.chat_name, 'a', encoding='utf-8') as chat_file:
            chat_file.write(write_content)
            return True

    def load_file(self, file_name: str, prefix: str = "", suffix: str = "", block_delimiter: str = ""):
        binary_type_mapping = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
        }

        file_type = None
        file_name_lower = file_name.lower()
        for extension, mime_type in binary_type_mapping.items():
            if file_name_lower.endswith(extension):
                file_type = mime_type
                break

        if file_type:
            return self.load_binary_file(
                file_name=file_name,
                mime_type=file_type,
                prefix=prefix,
                suffix=suffix
            )
        else:
            return self.load_text_file(
                file_name=file_name,
                prefix=prefix,
                suffix=suffix,
                block_delimiter=block_delimiter
            )

    def choose_file_to_load(self, files: list[str], pattern: str):
        if len(files) > 1 or pattern in ["*", "global/*"]:
            files.sort()
            for i, file in enumerate(files):
                print(f"{i + 1}: {os.path.basename(file)}")
            choice = input("Please choose a file to load (enter number): ")
            try:
                choice_index = int(choice) - 1
                if choice_index < 0 or choice_index >= len(files):
                    print("Invalid choice. Aborting load.")
                    return None
                file_path = files[choice_index]
            except ValueError:
                print("Invalid input. Aborting load.")
                return None
        else:
            file_path = files[0]
        return file_path

    def _help_menu(self, verbose: bool = False):
        super()._help_menu(verbose)
        if self.aliases:
            aliases = [f"{alias} -> {command}" for alias, command in self.aliases.items()]
            self._print_topics("Aliases", aliases, verbose)

    def do_quit(self, _):
        """Exit ara-cli"""
        print("Chat ended")
        self.last_result = True
        return True

    def onecmd_plus_hooks(self, line, orig_rl_history_length):
        # store the full line for use with default()
        self.full_input = line
        return super().onecmd_plus_hooks(line, orig_rl_history_length=orig_rl_history_length)

    def default(self, line):
        self.message_buffer.append(self.full_input)

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD(self, file_name):
        """Load a file and append its contents to chat file. Can be given the file name in-line. Will attempt to find the file relative to chat file first, then treat the given path as absolute"""
        import glob

        if file_name == "":
            file_name = input("What file do you want to load? ")
        file_pattern = os.path.join(os.path.dirname(self.chat_name), file_name)
        matching_files = glob.glob(file_pattern)
        if not matching_files:
            print(f"No files matching pattern {file_name} found.")
            return
        for file_path in matching_files:
            block_delimiter = "```"
            prefix = f"\nFile: {file_path}\n\n"
            self.add_prompt_tag_if_needed(self.chat_name)
            if not os.path.isdir(file_path) and self.load_file(file_path, prefix=prefix, block_delimiter=block_delimiter):
                print(f"Loaded contents of file {file_path}")

    def complete_LOAD(self, text, line, begidx, endidx):
        import glob

        return [x for x in glob.glob(text + '*')]

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_NEW(self, chat_name):
        """Create a new chat. Optionally provide a chat name in-line: NEW new_chat"""
        if chat_name == "":
            chat_name = input("What should be the new chat name? ")
        current_directory = os.path.dirname(self.chat_name)
        chat_file_path = os.path.join(current_directory, chat_name)
        self.__init__(chat_file_path)

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_RERUN(self, _):
        """Rerun the last prompt in the chat file"""
        self.resend_message()

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_CLEAR(self, _):
        """Clear the chat and the file containing it"""
        user_input = input("Are you sure you want to clear the chat? (y/N): ")
        if user_input.lower() != 'y':
            return
        self.create_empty_chat_file(self.chat_name)
        self.chat_history = self.load_chat_history(self.chat_name)
        print(f"Cleared content of {self.chat_name}")

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD_RULES(self, rules_name):
        """Load rules from ./prompt.data/*.rules.md or from a specified template directory if an argument is given. Specify global/<rules_template> to access globally defined rules templates"""
        self._load_template_helper(rules_name, "rules", "*.rules.md")

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD_INTENTION(self, intention_name):
        """Load intention from ./prompt.data/*.intention.md or from a specified template directory if an argument is given. Specify global/<intention_template> to access globally defined intention templates"""
        self._load_template_helper(intention_name, "intention", "*.intention.md")

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD_COMMANDS(self, commands_name):
        """Load commands from ./prompt.data/*.commands.md or from a specified template directory if an argument is given. Specify global/<commands_template> to access globally defined commands templates"""
        self._load_template_helper(commands_name, "commands", "*.commands.md")

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD_BLUEPRINT(self, blueprint_name):
        """Load specified blueprint. Specify global/<blueprint_name> to access globally defined blueprints"""
        self._load_template_from_global_or_local(blueprint_name, "blueprint")

    def _load_helper(self, directory: str, pattern: str, file_type: str, exclude_pattern: str | None = None):
        import glob

        directory_path = os.path.join(os.path.dirname(self.chat_name), directory)
        file_pattern = os.path.join(directory_path, pattern)

        exclude_files = []
        matching_files = glob.glob(file_pattern)
        if exclude_pattern:
            exclude_files = glob.glob(exclude_pattern)
            matching_files = list(set(matching_files) - set(exclude_files))

        if not matching_files:
            print(f"No {file_type} file found.")
            return

        file_path = self.choose_file_to_load(matching_files, pattern)

        if file_path is None:
            return

        self.add_prompt_tag_if_needed(self.chat_name)
        if self.load_file(file_path):
            print(f"Loaded {file_type} from {os.path.basename(file_path)}")

    def _load_template_from_global_or_local(self, template_name, template_type):
        from ara_cli.template_manager import TemplatePathManager
        from ara_cli.ara_config import ConfigManager

        plurals = {
            "commands": "commands",
            "rules": "rules"
        }

        plural = f"{template_type}s"
        if template_type in plurals:
            plural = plurals[template_type]

        if template_name.startswith("global/"):
            directory = f"{TemplatePathManager.get_template_base_path()}/prompt-modules/{plural}/"
            self._load_helper(directory, template_name.removeprefix("global/"), template_type)
            return

        ara_config = ConfigManager.get_config()
        local_templates_path = ara_config.local_prompt_templates_dir
        template_directory = f"{local_templates_path}/custom-prompt-modules/{plural}"
        self._load_helper(template_directory, template_name, template_type)

    def _load_template_helper(self, template_name, template_type, default_pattern):
        if not template_name:
            self._load_helper("prompt.data", default_pattern, template_type)
            return

        self._load_template_from_global_or_local(template_name=template_name, template_type=template_type)

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_EXTRACT(self, _):
        """Search for markdown code blocks containing \"# [x] extract\" as first line and \"# filename: <path/filename>\" as second line and copy the content of the code block to the specified file. The extracted code block is then marked with \"# [v] extract\""""
        from ara_cli.prompt_extractor import extract_responses

        extract_responses(self.chat_name, True)
        print("End of extraction")

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD_GIVENS(self, file_name):
        """Load all files listed in a ./prompt.data/config.prompt_givens.md"""
        from ara_cli.directory_navigator import DirectoryNavigator
        from ara_cli.prompt_handler import load_givens

        base_directory = os.path.dirname(self.chat_name)

        if file_name == "":
            file_name = f"{base_directory}/prompt.data/config.prompt_givens.md"

        # Check the relative path first
        relative_givens_path = os.path.join(base_directory, file_name)
        if os.path.exists(relative_givens_path):
            givens_path = relative_givens_path
        elif os.path.exists(file_name):  # Check the absolute path
            givens_path = file_name
        else:
            print(f"No givens file found at {relative_givens_path} or {file_name}")
            user_input = input("Please specify a givens file: ")
            if os.path.exists(os.path.join(base_directory, user_input)):
                givens_path = os.path.join(base_directory, user_input)
            elif os.path.exists(user_input):
                givens_path = user_input
            else:
                print(f"No givens file found at {user_input}. Aborting.")
                return

        cwd = os.getcwd()
        navigator = DirectoryNavigator()
        navigator.navigate_to_target()
        os.chdir('..')
        content, image_data = load_givens(givens_path)
        os.chdir(cwd)

        with open(self.chat_name, 'a', encoding='utf-8') as chat_file:
            chat_file.write(content)

        print(f"Loaded files listed and marked in {givens_path}")

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_SEND(self, _):
        """Send prompt to the LLM"""
        message = "\n".join(self.message_buffer)
        self.save_message(Chat.ROLE_PROMPT, message)
        self.send_message()

    @cmd2.with_category(CATEGORY_CHAT_CONTROL)
    def do_LOAD_TEMPLATE(self, template_name):
        """Load artefact template"""
        directory = os.path.join(os.path.dirname(__file__), 'templates')
        pattern = f"template.{template_name}"
        file_type = "template"
        exclude_pattern = os.path.join(directory, "template.*.prompt_log.md")

        self._load_helper(directory, pattern, file_type, exclude_pattern)
