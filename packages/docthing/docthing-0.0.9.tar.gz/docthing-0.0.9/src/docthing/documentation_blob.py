# SPDX-License-Identifier: MIT
''' BEGIN FILE DOCUMENTATION (level: 2)
Everything in `docthing` is about the class [`DocumentationBlob`](@DocumentationBlob).

This class is the one create after the _index file_ is processed accordingly to the _configuration_.

It contains the entire project documentation documentation in a output agnostic way and it can be
used to generate documentation in various formats.

To export the documentation in a specific format, you can use an `Exporter Plugin` which is a
class that implements the [`Exporter`](@Exporter) abstract class.
After being correctly instantiated, a `DocumentationBlob` can be exported to a specific format passing
it to the method `export` of an instance of a concrete `Exporter` implementation.

Before exporting the documentation, it is possible to apply _Meta Interpreters_ plugins to the
`DocumentationBlob` instance. These type of plugins are concrete implementations of the
[`MetaInterpreter`](@MetaInterpreter) abstract class and tehy can be used to apply some specific
modification to each node of the documentation tree based on some rules defined in the plugin itself.

---

`DocumentationBlob` is a tree structured object that contains the entire project documentation
that honors the [`Tree`](@Tree) interface. A tree structure is perfect for representing
the hierarchical structure of documentation, where each node can have multiple child nodes.

Each node with child(ren) is a _Section_ and outermost children (children of the root node) are referred
as _Chapters_ (which are just sections with a fancy name).

Each leaf of the tree represents a documentation piece and its content will be a [`Document`](@Document)
(which is a wrapper class for a list of strings or `ResourceReference`s). A Document has a one-to-one
correspondence with an output file. Read more about it in the appropriate documentation section.
END FILE DOCUMENTATION '''

import pyjson5 as json
import os

from .documentation_content import Document, ResourceReference
from .extractor import extract_documentation
from .tree import Tree, TreeNode


# =======================
# DOCUMENTATION BLOB NODE
# =======================

class DocumentationNode(TreeNode):
    '''
    A node in the documentation tree, representing a chapter, section, file, directory,
    or file list.

    The `DocumentationNode` class represents a node in the documentation tree, which can be
    a chapter, section, file, directory, or file list. Each node has a title and either
    content or a list of child nodes.

        Args:
            title (str): The title of the node.
            content (str, optional): The content of the node, if it is a file.
            children (list, optional): A list of child nodes, if the node is a chapter, section,
                directory, or file list.
            parser_config (dict): The configuration for the parser.

        Raises:
            ValueError: If both `content` and `children` are provided, or if neither is provided.
    '''

    def __init__(
            self,
            parent,
            title,
            content=None,
            children=None,
            parser_config=None):
        '''
        Initialize a new DocumentationNode.

            Args:
                title (str): The title of the node.
                content (str, optional): The content of the node, if it is a file.
                children (list, optional): A list of child nodes, if the node is a chapter,
                    section, directory, or file list.
                parser_config (dict): The configuration for the parser.

            Raises:
                ValueError: If both `content` and `children` are provided, or if neither is
                provided.
        '''
        super().__init__(parent, children)

        if content is not None and children is not None:
            raise ValueError('Both content and children cannot be provided')

        if content is not None and not isinstance(
                content, (str, list, ResourceReference, Document)):
            raise ValueError(
                'content must be None, a path to a file or a ResourceReference')

        if content is not None and parser_config is None:
            raise ValueError('config must be provided for leaf nodes')

        self.title = title
        self.content = content
        self.parser_config = parser_config

        self.options = {'level': 0, 'level-only': False}

        self.lazy = isinstance(
            content, str) and (
            os.path.isfile(content) or os.path.isdir(content))

    def is_lazy(self):
        '''
        Check if the node is lazy.

            Returns:
                bool: True if the node is lazy, False otherwise.
        '''
        return self.lazy

    def _unlazy_content(self):
        '''
        Unlazy the content of the node.

            Raises:
                ValueError: If the content of the node is not a file or a directory.
        '''
        if not self.lazy:
            return

        if os.path.isfile(self.content):
            self.content, options = extract_documentation(self.content,
                                                          self.parser_config)
            for k, v in options.items():
                self.options[k] = v
        elif os.path.isdir(self.content):
            # list all files in the directory with any of the extensions from
            # self.config['extensions'] but not in self.config['iexts']
            files = [f for f in os.listdir(self.content)
                     if os.path.isfile(os.path.join(self.content, f))
                     and f.split('.')[-1] in self.parser_config['extensions']
                     and f.split('.')[-1] not in self.parser_config['iexts']]
            files = [os.path.join(self.content, f) for f in files]
            self.content = []
            for i_f, f in enumerate(files):
                doc, opts = extract_documentation(f, self.parser_config)
                self.content.append(doc)
                # Only options from the first file are kept
                if i_f == 0:
                    self.options = opts
        else:
            raise ValueError(
                'The content of the node ' +
                f'{self.title} is not a file or a directory.')
        self.content = Document(self.content)
        self.lazy = False

    def unlazy(self):
        '''
        Unlazy the node.
        '''
        if self.is_leaf():
            self._unlazy_content()
        else:
            for child in self.children:
                child.unlazy()

    def get_content(self, unlazy=False):
        '''
        Get the content of the node.

            Args:
                unlazy (bool, optional): If True, the content of the node will be unlazy.
                    Defaults to False.
                    If False, the content of the node will be returned as is.
                    If True, the content of the node will be unlazy and returned.
                    If the content of the node is not a file or a directory,
                    a ValueError will be raised.
            Returns:
                str: The content of the node.
        '''
        if not self.lazy or not unlazy:
            return self.content

        if unlazy:
            self._unlazy_content()
            return self.content if self.content is not self.is_leaf() else Document([])

    def get_title(self):
        '''
        Get the title of the node.

            Returns:
                str: The title of the node.
        '''
        return self.title

    def get_options(self):
        '''
        Get the options of the node.

            Returns:
                dict: The options of the node.
        '''
        if self.lazy:
            self._unlazy_content()

        return self.options

    def replace_resources_with_imports(self, import_function):
        '''
        Replace resources with imports in the content of the node.
        '''
        if self.content is not None:
            self.content.replace_resources_with_imports(
                self.get_title(), import_function)

    def __str__(self) -> str:
        if not self.lazy and self.is_leaf():
            return __class__.__name__ + \
                '(' + self.title + ', ' + str(self.content) + ')'
        else:
            return __class__.__name__ + '(' + self.title + ')'


# =======================
# DOCUMENTATION BLOB
# =======================

class DocumentationBlob(Tree):
    '''
    DocumentationBlob is a class that represents a blob of documentation.
        It contains the entire project documentation in a output agnostic way.
        It can be used to generate documentation in various formats.
    '''

    def __init__(self, index_file, parser_config):
        self.parser_config = parser_config
        self.index_file_path = index_file

        super().__init__(self._generate_tree_from_index())

    def _generate_tree_from_index(self):
        return self._generate_node_from_index(None, self.index_file_path)

    def _generate_node_from_index(self, parent, index_file_json):
        '''
        Generate the root node of the tree.
        '''
        with open(index_file_json, 'r') as f:
            index_file_json = json.load(f)

        # Main title
        if 'main-title' not in index_file_json:
            raise ValueError('Index file must contain \'main-title\'')

        res = DocumentationNode(parent, index_file_json['main-title'])

        # Quick Start
        if 'quick' not in index_file_json:
            print('Warning: index file does not contain \'quick\': this is discouraged: it is ' +
                  'important to give the user a grasp of the usage of the project')
        else:
            res.add_child(
                self._generate_leaf(
                    parent,
                    'Quick Start',
                    index_file_json['quick']))

        # Introduction
        if 'intro' not in index_file_json:
            print('Warning: index file does not contain \'intro\': this is discouraged: it is ' +
                  'important to give the user a brief introduction to the project')
        else:
            res.add_child(
                self._generate_leaf(
                    parent,
                    'Introduction',
                    index_file_json['intro']))

        # It is ok to iterate over dict keys since python 3.6; see:
        # https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-compactdict
        for k, v in index_file_json.items():
            if k not in ['main-title', 'quick', 'intro']:
                res.add_child(self._generate_node(parent, k, v))

        return res

    def _generate_internal_node(self, parent, title, children):
        '''
        Generate a node with children.
        '''
        if isinstance(children, dict):
            return DocumentationNode(parent, title, None,
                                     [self._generate_node(parent, child_title, child)
                                      for child_title, child in children.items()])
        else:
            return DocumentationNode(parent, title, None,
                                     [self._generate_node(parent, '', child)
                                      for child in children])

    def _generate_leaf(self, parent, title, content_file_path):
        '''
        Generate a leaf node.
        '''
        return DocumentationNode(
            parent,
            title,
            content_file_path,
            None,
            self.parser_config)

    def _generate_node(self, parent, title, node):
        '''
        Generate a node.
        '''
        if title == '__index__':
            return self._generate_node_from_index(parent, node)
        elif isinstance(node, dict):
            return self._generate_internal_node(parent, title, node)
        elif isinstance(node, list):
            return self._generate_internal_node(parent, title, node)
        elif isinstance(node, str):
            return self._generate_leaf(parent, title, node)
        raise ValueError('Invalid node type')

    def unlazy(self):
        '''
        Unlazy the tree.
        '''
        self.root.unlazy()

    def is_lazy(self):
        '''
        Check if the tree has any lazy nodes.
        '''
        for leaf in self.root.get_leaves():
            if leaf.is_lazy():
                return True
        return False

    def prune_doc(self):
        '''
        Prunes the documentation level of the documentation blob based on the
        provided level.

        Documentation nodes that are at the specified level or lower will be kept.
        Other nodes will be pruned.

        If a node has the option `level-only` enabled this will be kept only if the
        level is exactly the specified level.
        '''
        if self.is_lazy():
            self.unlazy()

        level = self.parser_config['doc_level']
        if level == 0:
            return

        def _prune_function(node: DocumentationNode):
            # The node is internal (do not prune)
            if not node.is_leaf():
                return False

            # The node is a leaf
            if node.get_content() is None:
                # The node is a leaf with no content it means that is an
                #   internal node left with no child
                return True

            node_level = node.get_options().get('level', 0)
            is_level_only = node.get_options().get('level-only', False)
            if node_level > level:
                # Always prune if node level is greater
                return True
            elif node_level == level:
                # Never prune if the node level is the same
                return False
            else:  # node level is lower
                # Prune only if the level-only option was specified
                #   and the node level is lower
                return is_level_only

        self.prune(_prune_function, prune_again_after_children=True)
