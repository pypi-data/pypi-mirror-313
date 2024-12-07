"""
exceptions.py – Model layout parser specific exceptions
"""

# Every error should have the same format
# with a standard prefix and postfix defined here
pre = "\nModel layout parser: ["
post = "]"


class MLSException(Exception):
    pass

class MLSUserInputException(MLSException):
    pass

class MLSIOException(MLSException):
    pass

class LayoutParseError(MLSUserInputException):
    def __init__(self, model_file, e):
        self.model_file = model_file
        self.e = e

    def __str__(self):
        return f'{pre}Parse error in layout "{self.model_file}"\n\t{self.e}"{post}'

class LayoutInputFileOpen(MLSIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this layout file: "{self.path}"{post}'

class LayoutInputFileEmpty(MLSIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}For some reason, nothing was read from the layout file: "{self.path}"{post}'

class LayoutGrammarFileOpen(MLSIOException):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'{pre}Parser cannot open this layout grammar file: "{self.path}"{post}'

class MultipleFloatsInSameStraightConnector(MLSException):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{pre}Straight connector "{self.name}" has two floating anchors (*). Specify one.{post}'

class MultipleFloatsInSameBranch(MLSException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}There may be at most one floating anchor (*) per branch: "{self.branch}"{post}'

class ConflictingGraftFloat(MLSException):
    def __init__(self, stem):
        self.stem = stem

    def __str__(self):
        return f'{pre}A floating anchor(*) may not graft (>, >>): "{self.stem}"{post}'

class MultipleGraftsInSameBranch(MLSException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}There may be at most one graft (>, >>) per branch: "{self.branch}"{post}'

class TrunkLeafGraftConflict(MLSException):
    def __str__(self):
        return f'{pre}Leaf may not graft locally (>) if Trunk is grafting (>) {post}'

class ExternalLocalGraftConflict(MLSException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}Branch has local (>) graft with conflicting external graft (>>) in preceding branch: "{self.branch}"{post}'

class ExternalGraftOnLastBranch(MLSException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}Last branch in tree layout has a superfluous external (>>) graft: "{self.branch}"{post}'

class GraftRutBranchConflict(MLSException):
    def __init__(self, branch):
        self.branch = branch

    def __str__(self):
        return f'{pre}A rut branch, with (: Ln[R+/-n]), may not include a local graft(>): "{self.branch}"{post}'
