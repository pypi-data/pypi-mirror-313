""" layout_visitor.py """
from collections import namedtuple
from enum import Enum
from arpeggio import PTNodeVisitor
from mls_parser.exceptions import (ConflictingGraftFloat, MultipleGraftsInSameBranch, ExternalLocalGraftConflict,
                                   MultipleFloatsInSameBranch, TrunkLeafGraftConflict, GraftRutBranchConflict,
                                   ExternalGraftOnLastBranch)


DiagramLayout = namedtuple('DiagramLayout', 'layout_spec node_placement connector_placement')
LayoutSpec = namedtuple('LayoutSpec', 'dtype pres notation color sheet orientation frame frame_presentation padding')

# class NodeFace(Enum):
#     """
#     Values are multiplied by absolute distance to get an x or y coordinate.
#     """
#     TOP = 0
#     BOTTOM = 1
#     RIGHT = 2
#     LEFT = 3


face_map = {'r': 'RIGHT', 'l': 'LEFT', 't': 'TOP', 'b': 'BOTTOM'}


class LayoutVisitor(PTNodeVisitor):
    """
    Organized in the same categories commented in the clean peg grammar file.

        Some conventions:

        - Comment each visit with parsing semantics
        - Descriptive named variables if processing is required
        - Use *node.rule_name* in case the rule name changes
        - Combine values into dictionaries for stability, ease of interpretation and to avoid mistakes
        - Assigining result to a variable that is returned for ease of debugging
    """

    # Root
    @classmethod
    def visit_diagram_layout(cls, node, children) -> DiagramLayout:
        """
        EOL* layout_spec ((node_block connector_block) / (node_block))? EOF

        Root Rule
        """
        # Organize the input into a layout spec, a node dictionary, and an optional connector block
        lspec = children.results['layout_spec'][0]
        node_pdict = {}
        for n in children.results['node_block'][0]:
            dup_num = n.get('duplicate')
            key = n['node_name'] if not dup_num else f"{n['node_name']}_{dup_num}"
            node_pdict[key] = n

        if 'connector_block' in children.results:
            rc = children.results['connector_block'][0]
        else:
            rc = None
        return DiagramLayout(layout_spec=lspec, node_placement=node_pdict, connector_placement=rc)

    @classmethod
    def visit_layout_spec(cls, node, children) -> LayoutSpec:
        """
        (diagram notation color? presentation sheet padding? orientation frame? frame_presentation?)#

        Layout specification
        """
        ld = children.results
        frame = ld.get('frame')
        color = ld.get('color', ['white'])
        frame_presentation = ld.get('frame_presentation')
        padding = ld.get('padding')
        lspec = LayoutSpec(dtype=ld['diagram'][0], notation=ld['notation'][0], pres=ld['presentation'][0],
                           orientation=ld['orientation'][0], sheet=ld['sheet'][0],
                           color=color[0],
                           frame=None if not frame else frame[0],
                           # frame_presentation not relevant if no frame
                           frame_presentation=None if not frame else frame_presentation[0],
                           padding=None if not padding else padding[0])
        return lspec

    # Diagram
    @classmethod
    def visit_diagram(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_notation(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_color(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_presentation(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_sheet(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_padding(cls, node, children):
        """Keyword argument"""
        d = {k: v for c in children for k, v in c.items()}
        return d

    @classmethod
    def visit_tpad(cls, node, children):
        return {'top': children[0]}

    @classmethod
    def visit_bpad(cls, node, children):
        return {'bottom': children[0]}

    @classmethod
    def visit_lpad(cls, node, children):
        return {'left': children[0]}

    @classmethod
    def visit_rpad(cls, node, children):
        return {'right': children[0]}

    @classmethod
    def visit_orientation(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_frame(cls, node, children):
        """Keyword argument"""
        return children[0]

    @classmethod
    def visit_frame_presentation(cls, node, children):
        """Keyword argument"""
        return children[0]


    # Node
    @classmethod
    def visit_node_block(cls, node, children):
        """ nodes_header node_spec+ """
        return children

    @classmethod
    def visit_node_spec(cls, node, children):
        """
        INDENT node_name wrap? (SP+ node_width_expansion)? (SP+ node_height_expansion)?
         SP+ node_placement (SP+ color_tag)? EOL*
        """
        ditems = {k: v for c in children for k, v in c.items()}
        return ditems

    @classmethod
    def visit_node_name(cls, node, children):
        """ name """
        return {node.rule_name: ''.join(children)}

    @classmethod
    def visit_node_width_expansion(cls, node, children):
        """ number '%' """
        # Convert percentage to ratio ensuring ratio is positive
        user_percent = children[0]
        ratio = 0 if user_percent < 0 else round(user_percent / 100, 2)
        return {node.rule_name: ratio}

    @classmethod
    def visit_node_height_expansion(cls, node, children):
        """ number '%' """
        d = {k: v for k, v in children}
        return {node.rule_name: d}

    @classmethod
    def visit_comp_height_expansion(cls, node, children):
        """ '[C' number ']' number '%' """
        # Convert percentage to ratio ensuring ratio is positive
        user_percent = children[1]
        ratio = 0 if user_percent < 0 else round(user_percent / 100, 2)
        return [children[0], ratio]

    @classmethod
    def visit_node_placement(cls, node, children):
        """ grid_place (SP+ ':' SP+ grid_place)* """
        return {'placements': children}

    @classmethod
    def visit_grid_place(cls, node, children):
        """ node_loc (SP+ node_align)? """
        d = {k: v for c in children for k, v in c.items()}
        return d

    @classmethod
    def visit_node_loc(cls, node, children):
        """
        span ',' span

        row and column
        """
        return {node.rule_name: children}

    @classmethod
    def visit_span(cls, node, children):
        """
        number '-' number / number

        for example:
        3-5 is returned as span [3,5]
        3 is returned as span [3]
        """
        return children

    @classmethod
    def visit_color_tag(cls, node, children):
        """ '<' name '>' """
        return {node.rule_name: children[0]}

    # Connector
    @classmethod
    def visit_connector_block(cls, node, children):
        return children

    @classmethod
    def visit_connector_layout(cls, node, children):
        """All layout info for the connector"""
        # Combine all child dictionaries
        items = {k: v for d in children for k, v in d.items()}
        items['bend'] = items.get('bend', 1)  # No bend supplied, assume 1
        return items

    @classmethod
    def visit_cname_place(cls, node, children):
        """Name of connector and the side of the connector axis where it is placed"""
        # If a value is supplied it will be a single time list, so extract with [0]
        # If no value is supplied for an optional item, default must also be a single item list [default_value]
        w = children.results.get('wrap')
        wrap_value = 1 if not w else w[0]['wrap']
        cplace = {'cname': children.results['name'][0],  # Required component
                  'dir': children.results.get('dir', [1])[0],  # many optional components with default values
                  'bend': children.results.get('bend', [1])[0],
                  'notch': children.results.get('notch', [0])[0],
                  'wrap': wrap_value,
                  }
        return cplace

    @classmethod
    def visit_bend(cls, node, children):
        """Number of bend where cname appears"""
        # return {node.rule_name: int(children[0])}
        bend = int(children[0])
        return bend

    # Binary connector
    @classmethod
    def visit_binary_layout(cls, node, children):
        """All layout info for the binary connector"""
        # Combine all child dictionaries
        items = {k: v for d in children for k, v in d.items()}
        return items

    @classmethod
    def visit_tstem(cls, node, children):
        """T stem layout info"""
        items = {k: v for d in children for k, v in d.items()}
        items['anchor'] = items.get('anchor', 0)
        tstem = {node.rule_name: items}
        return tstem

    @classmethod
    def visit_pstem(cls, node, children):
        """P stem layout info"""
        items = {k: v for d in children for k, v in d.items()}
        items['anchor'] = items.get('anchor', 0)
        pstem = {node.rule_name: items}
        return pstem

    @classmethod
    def visit_tertiary_node(cls, node, children):
        """Tertiary node face and anchor"""
        return {node.rule_name: children[0]}

    @classmethod
    def visit_paths(cls, node, children):
        """A sequence of one or more paths since a binary connector may bend multiple times"""
        paths = {node.rule_name: [p['path'] for p in children]}
        return paths

    @classmethod
    def visit_sname_place(cls, node, children):
        """Side of stem axis and number of lines in text block"""
        d = {'stem_dir': children[0]}  # initialize d
        d.update(children[1])  # Add wrap key
        return d

    # Tree connector
    @classmethod
    def visit_tree_layout(cls, node, children):
        """All layout info for the tree connector"""
        tlayout = children[0]
        # If the trunk is grafting (>), there can be no other leaf stem grafting locally (>)
        tlayout['branches'] = [c['branch'] for c in children[1:]]
        tgraft = tlayout['trunk_face']['graft']
        tleaves = tlayout['branches'][0]['leaf_faces']
        if tgraft and [tleaves[n]['graft'] for n in tleaves if tleaves[n]['graft'] == 'local']:
            raise TrunkLeafGraftConflict()  # In the first branch (trunk branch) both trunk and some leaf are grafting
        # For all offshoot (non-trunk) branches, there can be no local graft (>) if the preceding branch
        # is grafting externally (>>).  In other words, no more than one graft per branch.
        for b, next_b in zip(tlayout['branches'], tlayout['branches'][1:]):
            lf = b['leaf_faces']
            external_graft = [lf[n]['graft'] for n in lf if lf[n]['graft'] == 'next']
            if external_graft:
                next_lf = next_b['leaf_faces']
                if [next_lf[n]['graft'] for n in next_lf if next_lf[n]['graft'] == 'local']:
                    # External graft conflicts with local branch
                    raise ExternalLocalGraftConflict(set(lf.keys()))
        # Check for dangling external graft in last branch
        last_lf = tlayout['branches'][-1]['leaf_faces']
        external_graft = [last_lf[n]['graft'] for n in last_lf if last_lf[n]['graft'] == 'next']
        if external_graft:
            raise ExternalGraftOnLastBranch(branch=set(last_lf.keys()))
        return tlayout

    @classmethod
    def visit_trunk_face(cls, node, children):
        """A single trunk node at the top of the tree layout. It may or may not graft its branch."""
        face = children[0]  # Face, node and optional notch
        graft = False if len(children) == 1 else True
        if 'anchor' not in face.keys():
            face['anchor'] = 0  # A Trunk face is never grafted, so an unspecified anchor is 0
        tface = {'trunk_face': {'node_ref': face.pop('node_ref'), **face, 'graft': graft}}
        return tface

    @classmethod
    def visit_branch(cls, node, children):
        """A tree connector branch"""
        branch = {k: v for d in children for k, v in d.items()}
        # Verify that this is either an interpolated, rut or graft branch and not an illegal mix
        # If a path is specified it is a rut branch or if there is a local graft it is a grafted branch
        # If both path and local graft are present in the same branch it is illegal
        if branch.get('path', None):  # Path specified, so there should be no local grafts in this branch
            lf = branch['leaf_faces']
            local_graft = [lf[n]['graft'] for n in lf if lf[n]['graft'] == 'local']
            if local_graft:
                raise GraftRutBranchConflict(branch=set(lf.keys()))
        # Return dictionary of leaf faces and an optional path keyed to the local rule
        return {node.rule_name: branch}

    @classmethod
    def visit_leaf_faces(cls, node, children):
        """Combine into dictionary of each leaf face indexed by node name"""
        lfaces = {k: v for d in children for k, v in d.items()}
        if len([lfaces[n]['graft'] for n in lfaces if lfaces[n]['graft']]) > 1:
            raise MultipleGraftsInSameBranch(branch=set(lfaces.keys()))
        if len([lfaces[n]['anchor'] for n in lfaces if lfaces[n]['anchor'] == 'float']) > 1:
            raise MultipleFloatsInSameBranch(branch=set(lfaces.keys()))
        return {node.rule_name: lfaces}

    @classmethod
    def visit_leaf_face(cls, node, children):
        """Branch face that may be a graft to its branch (local) or the (next) branch"""
        lface = children[0]
        graft = None
        if 'anchor' not in lface.keys():
            lface['anchor'] = 0  # If not float or a number, it must be zero in a tree layout
        if len(children) == 2:
            graft = 'local' if children[1] == '>' else 'next'
        if lface['anchor'] == 'float' and graft:
            raise ConflictingGraftFloat(stem=lface['name'])
        lface['graft'] = graft
        node_ref = lface.pop('node_ref')
        # name = node_ref[0] if len(node_ref) == 1 else f"{node_ref[0]}_{node_ref[1]}"
        return {node_ref: lface}  # Single element dictionary indexed by the node name

    # Unary connector
    @classmethod
    def visit_unary_layout(cls, node, children):
        """Unary layout which is just a single stem"""
        return {'ustem': children[0]}

    # Face attachment
    @classmethod
    def visit_node_ref(cls, node, children):
        """name number?"""
        return children[0] if len(children) < 2 else f"{children[0]}_{children[1]}"

    @classmethod
    def visit_face(cls, node, children):
        """Face character"""
        return face_map[node.value]

    @classmethod
    def visit_dir(cls, node, children):
        """Pos-neg direction"""
        return 1 if node.value == '+' else -1

    @classmethod
    def visit_anchor(cls, node, children):
        """Anchor position"""
        anchor = 'float' if children[0] == '*' else children[0]
        return anchor

    @classmethod
    def visit_node_face(cls, node, children):
        """Where connector attaches to node face"""
        nface = {k: v[0] for k, v in children.results.items()}
        return nface

    # Alignment
    @classmethod
    def visit_valign(cls, node, children):
        """Vertical alignment of noce in its cell"""
        return {node.rule_name: children[0].upper()}

    @classmethod
    def visit_halign(cls, node, children):
        """Horizontal alignment of noce in its cell"""
        return {node.rule_name: children[0].upper()}

    @classmethod
    def visit_node_align(cls, node, children):
        """Vertical and/or horizontal alignment of node in its cell"""
        if len(children) == 2:
            # Merge the two dictionaries
            return {**children[0], **children[1]}
        else:
            return children[0]

    @classmethod
    def visit_notch(cls, node, children):
        """The digit 0 or a positive or negative number of notches"""
        if children[0] == '0':
            return 0
        else:
            scale = -1 if children[0] == '-' else 1
            return int(children[1]) * scale

    @classmethod
    def visit_path(cls, node, children):
        """
        'L' number ('R' notch)?

        Lane and rut, assume rut 0 if R not specified
        """
        # Rut is zero by default
        path = {node.rule_name: {'lane': children[0], 'rut': children.results.get('notch', [0])[0]}}
        return path  # { path: { lane: <lane_num>, rut: <rut_displacement> }

    # Elements
    @classmethod
    def visit_wrap(cls, node, children):
        """
        '/' number

        Number of lines to wrap an associated string
        """
        return {node.rule_name: int(children[0])}

    @classmethod
    def visit_number(cls, node, children):
        """
        r'[1-9][0-9]*'

        Natural nummber
        """
        return int(node.value)

    @classmethod
    def visit_name(cls, node, children):
        """
        word (delim word)*

        Sequence of delimited words forming a name
        """
        name = ''.join(children)
        return name

    # Discarded whitespace and comments
    @classmethod
    def visit_LINEWRAP(cls, node, children):
        """
        EOL SP*

        end of line followed by optional INDENT on next line
        """
        return None

    @classmethod
    def visit_EOL(cls, node, children):
        """
        SP* COMMENT? '\n'

        end of line: Spaces, Comments, blank lines, whitespace we can omit from the parser result
        """
        return None

    @classmethod
    def visit_SP(cls, node, children):
        """
        ' '

        Single space character (SP)
        """
        return None

