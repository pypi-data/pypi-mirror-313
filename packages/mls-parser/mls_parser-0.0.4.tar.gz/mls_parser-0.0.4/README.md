# Model Layout Sheet Parser

Parses an *.mls file (Model Layout Sheet) to yield an abstract syntax tree using python named tuples

### Why you need this

You need to process an *.mls file to layout a model diagram

### Installation

Create or use a python 3.11+ environment. Then

% pip install mls-parser

At this point you can invoke the parser via the command line or from your python script.

#### From your python script

You need this import statement at a minimum:

    from mls_parser.parser import LayoutParser

You can then specify a path as shown:

    result = LayoutParser.parse_file(file_input=path_to_file, debug=False)

In either case, `result` will be a list of parsed class model elements. You may find the header of the `visitor.py`
file helpful in interpreting these results.

#### From the command line

This is not the intended usage scenario, but may be helpful for testing or exploration. Since the parser
may generate some diagnostic info you may want to create a fresh working directory and cd into it
first. From there...

    % mls elevator.mls

The .xcm extension is not necessary, but the file must contain xcm text. See this repository's wiki for
more about the mls language. The grammar is defined in the [layout.peg](https://github.com/modelint/mls-parser/blob/main/src/mls_parser/layout.peg) file. (if the link breaks after I do some update to the code, 
just browse through the code looking for the class_model.peg file, and let me know so I can fix it)

You can also specify a debug option like this:

    % mls elevator.mls -D

This will create a scrall-diagnostics folder in your current working directory and deposite a couple of PDFs defining
the parse of both the class model grammar: `class_model_tree.pdf` and your supplied text: `class_model.pdf`.

You should also see a file named `mls_parser.log` in a diagnostics directory within your working directory
