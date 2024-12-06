from tree_sitter import Language, Parser, Tree, Node, Range
from tokenizers import Tokenizer
from transformers import BertTokenizer, AutoTokenizer, CodeLlamaTokenizer, GPT2Tokenizer, CodeLlamaTokenizerFast
import os
import tree_sitter_python as tspython
import tree_sitter_cpp as tscpp
import tree_sitter_java as tsjava

# new languages
import tree_sitter_c_sharp as tscsharp
import tree_sitter_go as tsgo
import tree_sitter_haskell as tshaskell
import tree_sitter_javascript as tsjavascript
import tree_sitter_kotlin as tskotlin
import tree_sitter_rust as tsrust
import tree_sitter_html as tshtml
import tree_sitter_c as tsc
import tree_sitter_ruby as tsruby


# US1: String, Language, Tokenizer
# US2: file_path, Language, Tokenizer

#Tokenizer can either be name of pretrained tokenizer or instance object of the tokenizer

# US3: receives and object or datastructure containing the alignments. Then it prints the content in a well-formatted way.
# US4: receives the offset of a node (tree-sitter node location), and the original snippet string. and then computes the range in the string where it is located within (start pos/ end pos).
# US5: receives a range, a string containing the snippet, a programming language. returns the specific nodes in the AST containing the tokens within that range.

# Data structure to store alignments
# 2D array or Dictionary? Object?

# Main method. Aligns tokens to AST trees
# exposed
# Takes 3 inputs,
# code is a String containing the code snippet or a file_path to a file containing the code
# language is a String containing the language of the code snippet
# tokenizer is the name of a pretrained tokenizer or instance object of the tokenizer
#
# Checks if code is a file path. If a File path, open + read the file as a String
# Checks if language is a supported language (Java, C++, Python)
# Check if tokenizer is a instance object of the tokenizer or a String (then check if the name matches pretrained tokenizers)
# 
# tokenizes the snippet
# creates an AST tree
# aligns the tokens to the AST tree
#
# returns a data structure representing the AST tree with extra information
def ASTalign (code, language, tokenizer, include_whitespace_and_special_tokens=False):
    # check if code is a string
    # check if code is a file path
    if _checkPath(code):
        code = _fileToString(code)

    # check if language is a supported language
    _checkLanguage(language)
        
    language = _getLanguage(language)

    # generate the AST
    tree = _generateAST(code, language)

    # create the tokenizer
    # checks if tokenizer is one of the pretrained tokenizers supported
    tokenizerTree = _initializeTokenizer(tokenizer)

    # parse the AST
    # tokenize each named node's text
    # store in data structure or object
    nodes = _traverse_tree(tree)

    # dictionary to store alignments
    # Key = Node, Values = List containing the tokens
    alignments = _alignTokensTo_Nodes(nodes, tokenizerTree, code, include_whitespace_and_special_tokens)

    return alignments
    
# private
# checks if the provided file path is valid
# returns True if the path is valid
# returns False if the path is not valid
def _checkPath (filePath):

    if(not isinstance(filePath, str)):
        raise TypeError("invalid input, please input a string")

    return os.path.exists(filePath)

SUPPORTED_LANGS = {'python': Language(tspython.language()), 
                   'cpp': Language(tscpp.language()), 
                   'java': Language(tsjava.language()),
                   'c': Language(tsc.language()),
                   'csharp': Language(tscsharp.language()),
                   'go': Language(tsgo.language()),
                   'haskell': Language(tshaskell.language()),
                   'html': Language(tshtml.language()),
                   'javascript': Language(tsjavascript.language()),
                   'kotlin': Language(tskotlin.language()),
                   'ruby' : Language(tsruby.language()),
                   'rust': Language(tsrust.language())}

# private
# check if the provided language is one of the supported languages (python, Java, C++)
# return true if so
# return false if it is not
def _checkLanguage (language):

    if(not isinstance(language, str)):
        TypeError("invalid input, please input a string for language")

    if language in SUPPORTED_LANGS:
        return True
    raise TypeError("invalid input, please input a supported language")

# private
# returns a language
def _getLanguage (language):
    # to do: check language
    if isinstance(language, Language):
        return language
    elif language in SUPPORTED_LANGS:
        return SUPPORTED_LANGS[language]

# private
# Converts the file located at filePath to a String using open/read
# returns a String containing the contents of the file
def _fileToString (filePath):
    with open(filePath) as f:
        fileString = f.read()
    return fileString
    
# private
# Verifies a tokenizer object or creates a pretrained tokenizer
#
# Checks if tokenizer is an instance object (already made tokenizer)
# if tokenizer is not an instance object, then check if it is a String
# if a String, check if it matches the pretrained tokenizers
# if it matches one, create a tokenizer of that type
# returns a tokenizer object
def _initializeTokenizer (tokenizer):
    # Verify if the input is a string
    if(not isinstance(tokenizer, str)):
        raise TypeError("invalid input, please input a string for tokenizer")

    if isinstance(tokenizer, str):
        tokenizer = tokenizer.lower()
        # Use of switch statement leaves room for future expansion
        match tokenizer:
            case "codellama":
                return CodeLlamaTokenizerFast.from_pretrained("codellama/CodeLlama-7b-hf")
            case "gpt2":
                return AutoTokenizer.from_pretrained("openai-community/gpt2")
            case "bert-base-uncased":
                return AutoTokenizer.from_pretrained('bert-base-uncased')
            case "roberta-base":
                return AutoTokenizer.from_pretrained('roberta-base', trim_offsets=False)
            case "dialogpt":
                return AutoTokenizer.from_pretrained('microsoft/DialoGPT-small', add_prefix_space=False)
            case "qwen":
                return AutoTokenizer.from_pretrained("Qwen/Qwen2-7B-Instruct")
            
            
    raise TypeError("invalid input, please input a supported tokenizer")
    # Default tokenizer, can be changed if needed
    # return AutoTokenizer.from_pretrained("openai-community/gpt2")          
    
#public
# Helper method to get root for easier whole tree printing
def getRootNode(alignments):
    return list(alignments.keys())[0]
# private
# Generates the AST based on the code snippet using the language provided
# returns an AST object
def _generateAST (code, language):
    language = _getLanguage(language)
    parser = Parser(language)
    src = code.encode()
    tree = parser.parse(src)
    return tree
    
# private
# from examples folder, walk_tree.py in py-tree-sitter repo
# traverses the entire tree and returns the nodes in a Generator
# Generator can be iterated over
def _traverse_tree(tree):
    cursor = tree.walk()

    visited_children = False
    while True:
        if not visited_children:
            yield cursor.node
            if not cursor.goto_first_child():
                visited_children = True
        elif cursor.goto_next_sibling():
            visited_children = False
        elif not cursor.goto_parent():
            break

# private
# Removes white space from a token.
def _clean_token(token):
    # GPT2 remove special characters
    token = token.replace("Ġ", "")
    token = token.replace("Ċ", "")
    token = token.replace("ĉ", "")
    # Codellama remove special characters
    token = token.replace("▁", "")
    token = token.replace("<0x0A>", "")
    token = token.replace("<0x09>", "")
    return token

# private
# Modifies a token and its offset information based on the presence of 
# whitespace and the include_whitespace flag.
# If whitespace is prepended to the token, the token start offset is
# incremented to account for it.
# If the include_whitespace flag is NOT set, the whitespace is removed
# from the token.
# Returns the updated token and offset.
def _preprocess_token(token, token_offset, include_whitespace):

    # Unpack the token offset.
    token_start, token_end = token_offset

    # Clean the token.
    cleaned_token = _clean_token(token)

    # Account for changes in token length in the token start offset.
    # *** NOTE: The update to the token start offset is agnostic to 
    #           the include_whitespace flag. This is based on an assumption
    #           that in the event of whitespace prefix overlap between TSNodes,
    #           only the part of the token that a TSNode would contain
    #           in its text should be considered to overlap with the node.
    #           If this assumption changes, this block should also change.
    if cleaned_token != token and cleaned_token != "":
        token_start += token.find(cleaned_token)

    # Unless the include_whitespace flag is set, replace the token
    # with its cleaned counterpart.
    if not include_whitespace:
        token = cleaned_token

    return token, (token_start, token_end)

# private
# Assigns a token to the token list of each node in the alignments dict it overlaps with.
def _assign_token(token_info, node_ranges, alignments):

    # Unpack token info.
    token, token_offset = token_info
    token_start, token_end = token_offset

    # If any node overlaps with the token, we assign the token to it.
    for node in alignments:
        node_start, node_end = node_ranges[node]
        if token_start < node_end and token_end > node_start:
            alignments[node].append(token)

# private
# receives a generator containing the nodes of an AST tree, a tokenizer, and the snippet
# creates a batch encoding using the tokenizer
# aligns the tokens to each node of the AST
# stores alignments in a data structure
# returns the data structure
def _alignTokensTo_Nodes(nodes, tokenizer, code, include_whitespace_and_special_tokens=False):

    # Create batch encoding.
    batch_encoding = tokenizer(code, add_special_tokens=include_whitespace_and_special_tokens)

    # There is only one encoding in the batch. 
    # Get its tokens and offsets.
    tokens = batch_encoding[0].tokens
    token_offsets = batch_encoding[0].offsets
    
    # Dictionary to store alignments.
    alignments = { node: [] for node in nodes }

    # Get the ranges in the snippet for each node to reference for overlaps.
    # Avoids repeat calls to rangeFinder during token assignment.
    node_ranges = { node: rangeFinder(node.range, code) for node in alignments }

    # Go through tokens and assign each token to all nodes it belongs to.
    for token, token_offset in zip(tokens, token_offsets):

        # Update token info based on whitespace flag.
        token_info = _preprocess_token(token, token_offset, include_whitespace_and_special_tokens)

        # Skip empty tokens.
        if (token_info[0]):
            _assign_token(token_info, node_ranges, alignments)
        
    # return dictionary
    return alignments

# exposed
# receives a data structure containing the AST alignments and an ID of a node
# then prints the alignments of the specified node with subtrees
# no return value
def printAlignmentsTree (node, alignments):

    # check the inputs
    _testPrintInputs(node, alignments)

    # call _recursive print with correct depth
    _recursivePrint(node, 0, alignments)

# private
# recursive method for printing tree + alignments
# traverses every child of a specified node recursively
# prints each depth with seperate indentation
# no return value
def _recursivePrint(node, depth, alignments):

    # print current node + alignments
    # indent based on depth, -> depth 'node type'
    # indent based on depth,       alignments

    print("    " * depth + "->" ,depth, " \'" + node.type + "\'")
    print("    " * depth + "     " , alignments[node])
    print()
    
    # iterate over each child
    for child in node.children:
        _recursivePrint(child, depth+1, alignments)



# exposed
# receives a data structure containing the AST alignments and an ID of a node
# then prints the alignments of the specified node without subtrees
# no return value
def printAlignmentsNode (node, alignments):

    # check the inputs
    _testPrintInputs(node, alignments)

    # print the node and alignments
    print(node.type)
    print(alignments[node])


def _testPrintInputs (targetnode, alignments):

    # check types of inputs
    if(not isinstance(targetnode, Node)):
        raise TypeError("invalid input, please input a node")
    if(not isinstance(alignments, dict)):
        raise TypeError("invalid input, please input a alignment dictionary")
    
    # check if dictionary is empty
    if(not alignments):
        raise TypeError("invalid input, please input an alignment object from ASTalign")

    nodes = list(alignments.keys())
    tokens = list(alignments.values())

    for node in nodes:
        if(not isinstance(node, Node)):
            raise TypeError("invalid input, please input an alignment object from ASTalign")
    for token in tokens:
        if(not isinstance(token, list)):
            raise TypeError("invalid input, please input an alignment object from ASTalign")

    # check if the node is in the dictionary
    for node in nodes:
        if node == targetnode:
            return
    raise TypeError("invalid input, please input a node from the alignment object")

        
# exposed
# receives the range of a node (tree-sitter Range object), and the original snippet string.
# then computes the index range in the string at which it is located, as [start_index, end_index).
# returns the index range [start_index, end_index)
def rangeFinder (node_range, snippet):

    if(not isinstance(node_range, Range)):
        raise TypeError("invalid input, please input a node.range")
    
    if(not isinstance(snippet, str)):
        raise TypeError("invalid input, please input a string")

    # Convert snippet to byte string.
    byte_string = snippet.encode()

    # Get the start_ and end_byte of the node range.
    start_byte, end_byte = node_range.start_byte, node_range.end_byte

    # Get start and end indices in the snippet by slicing the byte string
    # up to the start and end bytes and finding the lengths of the decoded 
    # substrings. 
    start_index = len(byte_string[:start_byte].decode())
    end_index = len(byte_string[:end_byte].decode())

    return (start_index, end_index)

# exposed
# receives a range as tuple [start_index, end_index) into snippet, a snippet, a programming language, and a tokenizer.
# returns the specific nodes in the resulting AST containing the tokens within that range. 
def ASTtokenFinder (range, snippet, language, tokenizer):

    # other params get type checked in ASTalign
    if(not isinstance(range, tuple)):
        raise TypeError("invalid input, please input a tuple")
    
    # Start index inclusive, end index exlusive.
    start, end = range[0], range[1]

    if (start < 0 or start >= len(snippet) or
        end < 0 or end > len(snippet) or
        end <= start):
        return {}    

    # Find byte offset into snippet string for start and end indices.
    start_offset = len(snippet[:start].encode())
    end_offset = start_offset + len(snippet[start:end].encode())

    # Construct AST alignment for snippet.
    alignments = ASTalign(snippet, language, tokenizer)

    # Build dict of node alignments whose nodes' content overlaps with byte offset range.
    target_alignments = {}
    for node in alignments:
        if (node.start_byte < end_offset and node.end_byte > start_offset):
            target_alignments[node] = alignments[node]

    return target_alignments

