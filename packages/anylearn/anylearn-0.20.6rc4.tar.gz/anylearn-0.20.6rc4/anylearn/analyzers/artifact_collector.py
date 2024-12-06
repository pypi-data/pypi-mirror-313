import ast
import fnmatch
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Union, Optional

from anylearn.utils.errors import AnyLearnException


class AnylearnImportVisitor(ast.NodeVisitor):

    def __init__(self) -> None:
        super().__init__()
        self.visited: bool = False
        self.imported_anylearn_as: Set[str] = set()
        self.imported_elements_as: Dict[str, Set[str]] = {}

    def visit(self, node: ast.AST) -> Any:
        self.visited = True
        return super().visit(node)

    def visit_Import(self, node: ast.Import):
        for child in node.names:
            if child.name:
                first, middle, rest = child.name.partition(".")
                if first == "anylearn" and not middle and not rest:
                    self.imported_anylearn_as.add(child.asname or child.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module and node.level == 0:
            first, _, _ = node.module.partition(".")
            if first == "anylearn":
                for child in node.names:
                    k = f"{node.module}.{child.name}"
                    if not k in self.imported_elements_as:
                        self.imported_elements_as[k] = set()
                    self.imported_elements_as[k].add(child.asname or child.name)
        self.generic_visit(node)


class ArtifactUsageVisitor(ast.NodeVisitor):

    def __init__(
        self,
        import_visitor: AnylearnImportVisitor,
    ) -> None:
        super().__init__()
        self.import_visitor: AnylearnImportVisitor = import_visitor
        self.parsed_import_calls: bool = False
        self.calls: Dict[str, Dict[str, Any]] = {
            'datasets': {
                'attribute_call': "get_dataset",
                'original_name_calls': [
                    "anylearn.get_dataset",
                ],
                'imported_name_calls': [],
                'argn': 0,
                'kwarg': 'full_name',
            },
            'models': {
                'attribute_call': "get_model",
                'original_name_calls': [
                    "anylearn.get_model",
                ],
                'imported_name_calls': [],
                'argn': 0,
                'kwarg': 'full_name',
            },
            'task_outputs': {
                'attribute_call': "get_task_output",
                'original_name_calls': [
                    "anylearn.get_task_output",
                    "anylearn.sdk.get_task_output",
                ],
                'imported_name_calls': [],
                'argn': 0,
                'kwarg': 'task_id',
            }
        }
        self.fullnames: Dict[str, Set[str]] = {
            'datasets': set(),
            'models': set(),
            'task_outputs': set(),
        }
        self.unfetchable: List[Any] = []

    def visit(self, node: ast.AST) -> Any:
        if not self.import_visitor.visited:
            raise AnyLearnException(
                "AnylearnImportVisitor should visit AST first"
            )
        if not self.parsed_import_calls:
            for _t, calls in self.calls.items():
                for call in calls['original_name_calls']:
                    _i = self.import_visitor.imported_elements_as.get(call, [])
                    self.calls[_t]['imported_name_calls'].extend(_i)
            self.parsed_import_calls = True
        return super().visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        for artifact_type in self.calls.keys():
            self.__fetch_full_name_from_call__(
                call=node,
                artifact_type=artifact_type,
            )
        self.generic_visit(node)

    def __fetch_full_name_from_call__(self, call: ast.Call, artifact_type: str):
        f = call.func

        # Calls like foo.bar()
        # where "bar" is raw string in ast.Attribute.attr
        # and foo is in ast.Name.id in ast.Attribute.value
        valid_attr_call = isinstance(f, ast.Attribute) and \
            isinstance(f.value, ast.Name) and \
            f.value.id in self.import_visitor.imported_anylearn_as and \
            f.attr == self.calls[artifact_type]['attribute_call']

        # Calls like print()
        valid_name_call = isinstance(f, ast.Name) and \
            f.id in self.calls[artifact_type]['imported_name_calls']

        if valid_attr_call or valid_name_call:
            _N = self.calls[artifact_type]['argn']
            _KW = self.calls[artifact_type]['kwarg']
            if len(call.args) > _N:
                _fn = self.__fetch_full_name_from_arg__(call.args[_N])
            else:
                kw = next((kw for kw in call.keywords if kw.arg == _KW), None)
                _fn = self.__fetch_full_name_from_kwarg__(kw)
            if _fn:
                self.fullnames[artifact_type].add(_fn)

    def __fetch_full_name_from_arg__(self, arg: ast.AST):
        if not arg:
            return None
        if sys.version_info < (3, 8):
            if isinstance(arg, ast.Str):
                return arg.s
            else:
                self.unfetchable.append(arg)
                return None
        else:
            if isinstance(arg, ast.Constant):
                return arg.value
            else:
                self.unfetchable.append(arg)
                return None

    def __fetch_full_name_from_kwarg__(self, kw: ast.keyword):
        if not kw:
            return None
        if sys.version_info < (3, 8):
            if isinstance(kw.value, ast.Str):
                return kw.value.s
            else:
                self.unfetchable.append(kw)
                return None
        else:
            if isinstance(kw.value, ast.Constant):
                return kw.value.value
            elif not isinstance(kw.value, ast.Constant):
                self.unfetchable.append(kw)
                return None


IGNORE = [
    "__pycache__",
    "build",
    "develop-eggs",
    "dist",
    "eggs",
    ".eggs",
    "sdist",
    "wheels",
    "*.egg-info",
    "htmlcov",
    ".tox",
    ".nox",
    "cover",
    "_build",
    "__pypackages__",
    ".env",
    ".venv",
    "env",
    "venv",
    "ENV",
    ".idea",
    ".vscode",
]


class ArtifactCollector:

    def __init__(self) -> None:
        self.unfetchable: Dict[str, ast.AST] = {}

    def collect(
        self,
        path: Optional[Union[os.PathLike, bytes, str]],
        encoding: str='utf8',
        follow_links: bool=False,
    ) -> Dict[str, Set[str]]:
        path = Path(path)
        if path.is_file():
            return self.__collect_in_file__(
                file_path=path,
                encoding=encoding,
            )
        elif path.is_dir():
            return self.__collect_in_dir__(
                dir_path=path,
                encoding=encoding,
                follow_links=follow_links,
            )
        else:
            raise NotADirectoryError

    def __collect_in_file__(
        self,
        file_path: Optional[Union[os.PathLike, bytes, str]],
        encoding: str='utf8',
    ) -> Dict[str, Set[str]]:
        import_visitor = AnylearnImportVisitor()
        artifact_visitor = ArtifactUsageVisitor(import_visitor)
        _fp = Path(file_path)
        with _fp.open("r", encoding=encoding) as f:
            contents = f.read()
            astroot = ast.parse(contents)
        import_visitor.visit(astroot)
        artifact_visitor.visit(astroot)
        self.unfetchable[_fp.absolute()] = artifact_visitor.unfetchable.copy()
        return artifact_visitor.fullnames

    def __collect_in_dir__(
        self,
        dir_path: Optional[Union[os.PathLike, bytes, str]],
        encoding: str='utf8',
        follow_links: bool=False,
    ) -> Dict[str, Set[str]]:
        fullnames = {
            'datasets': set(),
            'models': set(),
            'task_outputs': set(),
        }

        ignore = IGNORE
        ignore_pattern = r"|".join([fnmatch.translate(i) for i in ignore])

        walk = os.walk(dir_path, followlinks=follow_links, topdown=True)
        for root, dirs, files in walk:
            # In-place update `dirs` to exclude ignored dirs
            dirs[:] = [d for d in dirs if not re.match(ignore_pattern, d)]
            files = [f for f in files if Path(f).suffix == ".py"]

            for file_name in files:
                file = Path(root) / file_name
                _fn = self.__collect_in_file__(
                    file_path=file,
                    encoding=encoding,
                )
                fullnames['datasets'].update(_fn['datasets'])
                fullnames['models'].update(_fn['models'])
                fullnames['task_outputs'].update(_fn['task_outputs'])
        return fullnames
