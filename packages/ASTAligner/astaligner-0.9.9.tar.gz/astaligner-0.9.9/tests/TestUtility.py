import os

### This module should be placed in the Tests directory. The Tests directory
### should have a subdirectory Resources.

# Test case files are located here.
resource_directory = os.path.join(os.path.dirname(__file__),
                                    'Resources')

def _make_case_data(file):
    case_data = {}
    with open(file) as f:
        case_data["path"] = file
        case_data["text"] = f.read()
    return case_data

def _lang_for_ext(file):
    extension = os.path.splitext(file)[1]
    if extension == ".py":
        return "python"
    elif extension == ".cpp":
        return "cpp"
    elif extension == ".java":
        return "java"
    elif extension == ".c":
        return "c"
    elif extension == ".cs":
        return "csharp"
    elif extension == ".go":
        return "go"
    elif extension == ".hs":
        return "haskell"
    elif extension == ".html":
        return "html"
    elif extension == ".js":
        return "javascript"
    elif extension == ".kt":
        return "kotlin"
    elif extension == ".rb":
        return "ruby"
    elif extension == ".rs":
        return "rust"

# Function to read test case files into language-separated lists.
def load_test_cases():

    test_cases = {"python": [],
                    "cpp": [],
                    "java": [],
                    "c": [],
                    "csharp": [],
                    "go": [],
                    "haskell": [],
                    "html": [],
                    "kotlin": [],
                    "javascript": [],
                    "ruby": [],
                    "rust": []}

    fs_dir = os.fsencode(resource_directory)

    for fs_file in sorted(os.listdir(fs_dir)):

        # Get full file path.
        filename = os.fsdecode(fs_file)
        file = os.path.join(resource_directory, filename)

        case_data = _make_case_data(file)
        test_cases[_lang_for_ext(file)].append(case_data)

    return test_cases