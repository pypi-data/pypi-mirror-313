from ordered_set import OrderedSet
from collections import defaultdict, OrderedDict, Counter
from IPython.display import HTML, display
from graphviz import Graph
from copy import deepcopy
from maquinas.exceptions import NoSymbolInMachine


class PartialProduction:
    def __init__(self, head, body, lps=None):
        self.head = head
        # TODO: check for errors in tuplñe
        if isinstance(body, tuple):
            self.l = tuple(body[0])
            self.r = tuple(body[1])
        if not lps:
            self.lps = OrderedDict()
        else:
            self.lps = lps

    def __key(self):
        return (self.head, self.l, self.r)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, PartialProduction):
            return self.__key() == other.__key()
        return False

    def set_pointer(self, p1, p2, label):
        if p2:
            p = (p1, p2)
        else:
            p = (p1,)
        try:
            self.lps[label].add(p)
        except KeyError:
            self.lps[label] = OrderedSet([p])

    def is_partial_production(self):
        return not len(self.r) == 0

    def get_next_symbol(self):
        return self.r[0]

    def get_head(self):
        return self.head

    def move_next_symbol(self):
        return PartialProduction(self.head, (self.l + self.r[:1], self.r[1:]))

    def move_prev_symbol(self):
        return PartialProduction(self.head, (self.l[:-1], self.l[-1:] + self.r))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if len(self.l) > 0 or len(self.r) > 0:
            l = "".join(self.l)
            r = "".join(self.r)
            return f"{self.head} → {l}●{r}"
        else:
            return f"{self.head}"

    def __format__(self, format):
        return self.__str__()

    def pointers2str(self):
        res = []
        for l, ps in self.lps.items():
            l = f"{l}"
            ps = ", ".join([f"{p}" for p in ps])
            res.append(f"{l}:{ps}")
        return "; ".join(res)

    def get_pointers(self, l):
        try:
            return self.lps[l]
        except IndexError:
            return []
        except KeyError:
            return []

    def reduce_name(self):
        if len(self.r) > 0:
            l = "".join(self.l)
            r = "".join(self.r)
            return f"{self.head} → {l}●{r}"
        else:
            return f"{self.head}"

    def is_terminal(self):
        return len(self.l) == 0 and len(self.r) == 0

    def is_final(self, root):
        return self.head == root and len(self.r) == 0


class Item:
    def __init__(self, pp, ini, fin=None):
        self.pp = pp
        self.ini = ini
        self.fin = fin

    def get_ini(self):
        return self.ini

    def get_fin(self):
        return self.fin

    def get_pproduction(self):
        return self.pp

    def get_head(self):
        return self.pp.get_head()

    def get_next_symbol(self):
        return self.pp.get_next_symbol()

    def get_span(self):
        if self.fin:
            return self.ini, self.fin
        else:
            return None

    def is_partial_production(self):
        return self.pp.is_partial_production()

    def get(self):
        return self.pp, self.ini, self.fin

    def reduce_name(self):
        if not self.fin is None:
            return f"{self.pp.reduce_name()} {self.ini}∷{self.fin}"
        else:
            return f"{self.pp.reduce_name()} {self.ini}"

    def get_pointers(self, label):
        return self.pp.get_pointers(label)

    def add_pointers(self, pointers):
        return self.pp.add_pointers(pointers)

    def pointers2str(self):
        return self.pp.pointers2str()

    def __str__(self):
        if not self.fin is None:
            return f"{self.pp} {self.ini}∷{self.fin}"
        else:
            return f"{self.pp} {self.ini}"

    def __repr__(self):
        return self.__str__()

    def __format__(self, format):
        return self.__str__()

    def __key(self):
        return (self.pp, self.ini, self.fin)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Item):
            return self.__key() == other.__key()
        return False

    def move_next_symbol(self, ini, fin=None):
        return Item(self.pp.move_next_symbol(), ini=ini, fin=fin)

    def index(self):
        return Item(self.pp, self.ini)

    def is_final(self, root):
        return self.pp.is_final(root) and self.ini == 0

    def is_terminal(self):
        return self.pp.is_terminal()

    def set_pointer(self, p1, p2, l):
        self.pp.set_pointer(p1, p2, l)


# Predictor function
def predictor(item, k, productions, working_table):
    pp = item.get_pproduction()
    next_symbol = pp.get_next_symbol()
    for body in productions[next_symbol]:
        pp = PartialProduction(next_symbol, ([], body))
        working_table.add(Item(pp, k))


# Scanner function
def scanner(item, k, tokens, working_table, chart, terminals):
    symbol = item.get_next_symbol()
    origin = item.get_ini()
    token = tokens[k] if k < len(tokens) else None
    if symbol == token and symbol in terminals:
        new_item = item.move_next_symbol(origin)
        if new_item in chart[k + 1]:
            ix = chart[k + 1].index(new_item)
            new_item = chart[k + 1][ix]
        item_ = Item(item.pp, origin, k)
        if len(item.pp.l) > 0:
            new_item.set_pointer(item_, None, k)
        chart[k + 1].add(new_item)
    elif symbol == "ε":
        new_item = item.move_next_symbol(origin)
        if new_item in chart[k]:
            ix = chart[k].index(new_item)
            new_item = chart[k][ix]
        item_ = Item(item.pp, origin, k)
        working_table.add(new_item)
        if len(item.pp.l) > 0:
            new_item.set_pointer(item_, None, k)


def completer(item, k, working_table, chart):
    origin = item.get_ini()
    head = item.get_head()
    for prev_item in chart[origin]:
        try:
            symbol_canditate = prev_item.get_next_symbol()
        except IndexError:
            continue
        if symbol_canditate == head:
            new_item = prev_item.move_next_symbol(prev_item.ini)
            if new_item in chart[k]:
                ix = chart[k].index(new_item)
                new_item = chart[k][ix]
            elif new_item in working_table:
                ix = working_table.index(new_item)
                new_item = working_table[ix]
            item_ = Item(item.pp, origin, k)
            prev_item_ = Item(prev_item.pp, prev_item.ini, origin)
            if len(prev_item.pp.l) > 0:
                new_item.set_pointer(item_, prev_item_, origin)
            else:
                new_item.set_pointer(item_, None, origin)
            working_table.add(new_item)


def parse(tokens, productions, root, terminals):
    chart = [OrderedSet() for _ in range(len(tokens) + 1)]
    for rule in productions[root]:
        starting_production = PartialProduction(root, ([], rule))
        chart[0].add(Item(starting_production, 0))
    pointers = defaultdict(set)
    for k in range(len(tokens) + 1):
        working_table = OrderedSet(chart[k])
        chart[k].clear()
        # TODO: record the operation
        while len(working_table) > 0:
            item = working_table.pop()
            if item in chart[k]:
                if (len(item.pp.r) > 0 and item.pp.r[0] == "ε") or (
                    len(item.pp.l) > 0 and item.pp.l[0] == "ε"
                ):
                    pass
                else:
                    ix = chart[k].index(item)
                    item_ = chart[k][ix]
                    for l, ps in item.pp.lps.items():
                        item_.pp.lps[l].update(ps)
                    continue
            else:
                chart[k].add(item)

            if item.is_partial_production():
                symbol = item.get_next_symbol()
                if not symbol in terminals and not symbol == "ε":
                    predictor(item, k, productions, working_table)
                else:
                    scanner(item, k, tokens, working_table, chart, terminals)
            else:
                completer(item, k, working_table, chart)
    return chart


def print_chart(string, chart, pointers=False, lspace=40):
    for i, items in enumerate(chart):
        print(f"S({i}):", "{}•{}".format(string[0:i], string[i:]))
        pointers_str = ""
        for j, item in enumerate(items):
            pp = str(item.pp)
            if pointers:
                pointers_str = item.pointers2str()
            print(f"{j:3d} | {pp:20s} |  {item.ini:3d} | {pointers_str}")


def chart2table(string, chart, pointers=False):
    if pointers:
        tbl = [
            "<table><tr><th>No.</th><th>Production</th><th>Origin</th><th>Pointers</th></tr>"
        ]
    else:
        tbl = ["<table><tr><th>No.</th><th>Production</th><th>Origin</th></tr>"]
    for i, items in enumerate(chart):
        tbl.append('<tr><th style="text-align:center" colspan="3">')
        tbl.append(f"S({i}):")
        tbl.append(f"{string[:i]}•{string[i:]}")
        tbl.append("</th></tr>")
        for j, item in enumerate(items):
            pp = str(item.pp)
            tbl.append("<tr>")
            tbl.append(f"<td>{j:3d}</td>")
            tbl.append(f"<td style='text-align:left'>{pp}</td>")
            tbl.append(f"<td>{item.ini:3d}</td>")
            if pointers:
                pointers_str = item.pointers2str()
                tbl.append(f"<td>{pointers_str}</td>")
            tbl.append("</td>")
    tbl.append("</table>")
    return display(HTML("".join(tbl)))


def item2label(item, span=False, symbols={}):
    label = f"{item[0]}"
    label = symbols.get(label, label)
    if span:
        label = f"<{label} <FONT POINT-SIZE='7'>{item[1]}:{item[2]}</FONT>>"
    return label


def _extract_trees(
    stack,
    nodes_dict,
    terminals,
    ancesters=Counter(),
    max_depth=None,
    max_ancesters=None,
    tokens=0,
):
    nchars = 0
    depth = 0
    id = 1
    while len(stack) > 0:
        root, current, children, partials, nchars, depth, ancesters = stack.pop(0)
        if max_depth and depth >= max_depth:
            # yield root
            continue
        prev, currentlist = current
        if prev:
            ancesters[prev["label"]] += 1
        if len(children) == 0:
            if (prev["label"][0] in terminals or prev["label"][0] == "ε") and sum(
                [len(p) for p in partials]
            ) == 0:
                yield root
            else:
                _update_stack(
                    stack,
                    root,
                    partials,
                    nchars,
                    terminals,
                    prev=prev,
                    depth=depth,
                    ancesters=ancesters,
                )
        elif len(children) == 1:
            c = nodes_dict[children[0]]
            u = (
                {
                    "label": c["label"],
                    "id": c["id"],
                    "partial": c["partial"],
                },
                [],
            )
            id += 1
            if max_ancesters and max_ancesters <= ancesters[c["label"]]:
                continue
            currentlist.append(u)
            partials[0].insert(0, (u, c["children"]))
            _update_stack(
                stack,
                root,
                partials,
                nchars,
                terminals,
                prev=prev,
                depth=depth,
                ancesters=ancesters,
            )
        elif len(children) == 2:
            c1 = nodes_dict[children[0]]
            u1 = (
                {
                    "label": c1["label"],
                    "id": c1["id"],
                    "partial": c1["partial"],
                },
                [],
            )
            id += 1
            c2 = nodes_dict[children[1]]
            u2 = (
                {
                    "label": c2["label"],
                    "id": c2["id"],
                    "partial": c2["partial"],
                },
                [],
            )
            id += 1
            if max_ancesters and (
                max_ancesters <= ancesters[c1["label"]]
                or max_ancesters <= ancesters[c2["label"]]
            ):
                continue
            currentlist.append(u1)
            currentlist.append(u2)
            partials[0].insert(0, (u1, c1["children"]))
            partials[0].insert(1, (u2, c2["children"]))
            _update_stack(
                stack,
                root,
                partials,
                nchars,
                terminals,
                prev=prev,
                depth=depth,
                ancesters=ancesters,
            )
    return stack


def _deepcopy(tree, label, link=None):
    p, children = tree
    if "current" in p and p["current"]:
        link = (p, [c for c in children])
        return link, link
    children_ = []
    for c in children:
        c_, link_ = _deepcopy(c, label, link=link)
        children_.append(c_)
        if link_:
            link = link_
    return (p, children_), link


def _update_stack(
    stack, root, partials, nchars, terminals, prev=None, depth=0, ancesters=Counter()
):
    if len(partials) == 0:
        if prev:
            if prev["label"][1] == prev["label"][2]:
                stack.insert(0, (root, (None, []), [], [], nchars, depth, ancesters))
            else:
                stack.insert(
                    0, (root, (None, []), [], [], nchars + 1, depth + 1, ancesters)
                )
        return
    while len(partials) > 0 and len(partials[0]) == 0:
        partials.pop(0)
    if len(partials) == 0:
        return
    current, branches = partials[0].pop(0)
    current[0]["current"] = True
    if len(branches) == 0:
        if current[0]["label"][0] in terminals:
            stack.insert(
                0, (root, current, [], partials, nchars + 1, depth + 1, ancesters)
            )
        elif current[0]["label"][0] == "ε":
            stack.insert(0, (root, current, [], partials, nchars, depth + 1, ancesters))
        else:
            raise NoSymbolInMachine(current[0]["label"][0], terminals)
    if len(branches) > 0:
        root_, current_ = _deepcopy(root, current[0])
        if current_ is None:
            partials.append((current, branches))
            current[0]["current"] = False
        else:
            stack.append(
                (root, current, branches[0], partials, nchars, depth + 1, ancesters)
            )
            for ix in range(1, len(branches)):
                root_, current_ = _deepcopy(root, current[0])
                partials_ = [deepcopy(p) for p in partials]
                stack.append(
                    (
                        root_,
                        current_,
                        branches[ix],
                        partials_,
                        int(nchars),
                        depth + 1,
                        Counter(ancesters),
                    )
                )
    current[0]["current"] = False


def extract_trees(forest, terminals, max_depth=None, max_ancesters=None):
    u0, forest = forest
    u0_ = {
        "label": u0["label"],
        "id": u0["id"],
        "partial": u0["partial"],
    }
    root = (u0_, [])
    _, currentlist = root
    stack = []
    _update_stack(
        stack, root, [[(root, u0["children"])]], 0, terminals, ancesters=Counter()
    )
    return _extract_trees(
        stack,
        forest,
        terminals,
        max_depth=max_depth,
        max_ancesters=max_ancesters,
        tokens=u0["tokens"],
    )


def _graph_tree(
    f,
    tree,
    parent,
    c=0,
    ntree=0,
    symbols={},
    span=False,
    full=False,
    show_id=False,
    **params,
):
    tree = list(tree)
    if len(tree) > 1:
        u, children = tree
    else:
        (u,) = tree
        children = ()
    label = item2label(u["label"], span=span, symbols=symbols)
    u_n = f"u_{c}_{ntree}"
    if show_id:
        params[
            "xlabel"
        ] = f"<<I><FONT POINT-SIZE='8'>u</FONT><FONT POINT-SIZE='5'>{u['id']+1}</FONT></I>>"
    if not u["partial"] or full:
        f.node(u_n, label=label, **params)
        if parent:
            f.edge(parent, u_n)
    else:
        u_n = parent

    for child in children:
        c += 1
        c = _graph_tree(
            f,
            child,
            u_n,
            c=c,
            ntree=ntree,
            symbols=symbols,
            span=span,
            full=full,
            show_id=show_id,
            **params,
        )
    return c


def graph_tree(
    tree,
    symbols={},
    span=False,
    full=False,
    show_id=False,
    node_params={"style": "rounded", "shape": "plain"},
    **params,
):
    params["format"] = "svg"
    params["strict"] = True
    f = Graph(comment="tree", **params)
    c = 0
    _graph_tree(
        f,
        tree,
        None,
        c=c,
        symbols=symbols,
        span=span,
        full=full,
        show_id=show_id,
        **node_params,
    )
    return f


def graph_trees(
    trees,
    symbols={},
    span=False,
    full=False,
    show_id=False,
    node_params={"style": "rounded", "shape": "plain"},
    **params,
):
    params["format"] = "svg"
    params["strict"] = True
    f = Graph(comment="tree", **params)
    for i, tree in enumerate(trees):
        with f.subgraph(name=f"Tree {i}") as f_:
            _graph_tree(
                f_,
                tree,
                None,
                ntree=i,
                symbols=symbols,
                span=span,
                full=full,
                show_id=show_id,
                **node_params,
            )
    return f


def _graph_forest(
    f,
    u,
    forest,
    parent,
    ancesters,
    processed,
    symbols={},
    span=False,
    full=True,
    show_id=False,
    **params,
):
    if not u:
        return

    n = tuple(forest.keys()).index(u["label"])
    u_n = f"u_{u['id']+1}"
    ancesters.add(u["id"])

    node_name = u_n
    original_node_name = u_n
    label = item2label(u["label"], span=span, symbols=symbols)

    if show_id:
        params[
            "xlabel"
        ] = f"<<I><FONT POINT-SIZE='8'>u</FONT><FONT POINT-SIZE='5'>{u['id']+1}</FONT></I>>"
    if not u["partial"] or full:
        f.node(u_n, label=label, **params)
        if parent:
            if not (parent, original_node_name) in processed:
                f.edge(parent, original_node_name, dir="forward")
                processed.add((parent, original_node_name))
    else:
        node_name = parent

    for j, u_child_names in enumerate(u["children"]):
        if len(u["children"]) > 1:
            fake_parent = f"fp_{j}_{original_node_name}"
            f.node(fake_parent, label="", shape="point")
            if not (original_node_name, fake_parent) in processed:
                f.edge(original_node_name, fake_parent)
                processed.add((original_node_name, fake_parent))
            node_name = fake_parent
        for u_child_name in u_child_names:
            u_child = forest[u_child_name]
            if u_child["id"] in ancesters:
                u_n_child = f"u_{u_child['id']+1}"
                if not (node_name, u_n_child) in processed:
                    f.edge(node_name, u_n_child, dir="forward")
                    processed.add((node_name, u_n_child))
                continue
            else:
                _graph_forest(
                    f,
                    u_child,
                    forest,
                    node_name,
                    set(ancesters),
                    processed,
                    symbols=symbols,
                    span=span,
                    full=full,
                    show_id=show_id,
                    **params,
                )


def graph_forest(
    forest,
    symbols={},
    span=False,
    full=True,
    show_id=False,
    node_params={"style": "rounded", "shape": "rectangle"},
    **params,
):
    params["format"] = "svg"
    # params['strict']=True
    f = Graph(comment="tree", **params)
    u0, forest = forest
    _graph_forest(
        f,
        u0,
        forest,
        None,
        set(),
        set(),
        symbols=symbols,
        span=span,
        full=full,
        show_id=show_id,
        **node_params,
    )
    return f


def _make_node(label, elements):
    partial = False if isinstance(label[0], str) else True
    return {
        "label": label,
        "id": len(elements),
        "partial": partial,
        "children": OrderedSet(),
    }  # families


def _extract_forest(u, item, elements, processed, chart, terminals, i_table):
    if len(item.pp.l) == 0:
        return None

    symbol = item.pp.l[-1]
    pos = len(item.pp.l[:-1])
    first = len(item.pp.l) == 1

    if symbol == "ε":
        v_name = (item.pp.head, i_table, i_table)
        v = _make_node(v_name, elements)
        if not v_name in elements:
            elements[v_name] = v
        e_name = ("ε", i_table, i_table)
        e = _make_node(e_name, elements)
        if not e_name in elements:
            elements[e_name] = e
        u["children"].add((e_name,))
        processed.add(item)
        return

    if symbol in terminals and first:
        v_name = (symbol, i_table - 1, i_table)
        v = _make_node(v_name, elements)
        if not v_name in elements:
            elements[v_name] = v
        u["children"].add((v_name,))

    if (not symbol in terminals) and first:
        j = item.ini
        v_name = (symbol, j, i_table)
        v = _make_node(v_name, elements)
        if not v_name in elements:
            elements[v_name] = v
        u["children"].add((v_name,))
        for (q,) in item.pp.lps[j]:
            if not q in processed:
                _extract_forest(
                    v, q, elements, processed, chart, terminals, i_table=i_table
                )

    if symbol in terminals and not first:
        j = item.ini
        v_name = (symbol, i_table - 1, i_table)
        v = _make_node(v_name, elements)
        if not v_name in elements:
            elements[v_name] = v
        w_name = (item.pp.move_prev_symbol(), j, i_table - 1)
        w = _make_node(w_name, elements)
        if not w_name in elements:
            elements[w_name] = w
            for (p_,) in item.pp.lps[i_table - 1]:
                _extract_forest(
                    w, p_, elements, processed, chart, terminals, i_table=i_table - 1
                )
        u["children"].add((w_name, v_name))

    if (not symbol in terminals) and not first:
        j = item.ini
        for l, qps in item.pp.lps.items():
            for ii, (q, p_) in enumerate(qps):
                w_name = (item.pp.move_prev_symbol(), j, l)
                w = _make_node(w_name, elements)
                if not w_name in elements:
                    elements[w_name] = w
                else:
                    w = elements[w_name]
                if not p_ in processed:
                    processed.add(p_)
                    _extract_forest(
                        w, p_, elements, processed, chart, terminals, i_table=l
                    )
                v_name = (symbol, l, i_table)
                v = _make_node(v_name, elements)
                if not v_name in elements:
                    elements[v_name] = v
                else:
                    v = elements[v_name]
                if not q in processed:
                    processed.add(q)
                    _extract_forest(
                        v, q, elements, processed, chart, terminals, i_table=i_table
                    )
                u["children"].add((w_name, v_name))


def extract_forest(root, chart, terminals, tokens):
    elements = OrderedDict()
    processed = OrderedSet()
    i_table = len(chart) - 1
    root_name = (root, 0, i_table)
    u0 = _make_node(root_name, elements)
    elements[u0["label"]] = u0
    u0["tokens"] = tokens
    for item in chart[-1]:
        if item.is_final(root):
            _extract_forest(u0, item, elements, processed, chart, terminals, i_table)
    return u0, elements


def verify_chart(chart, tokens, root):
    if not (len(tokens) + 1) == len(chart):
        return False
    return [
        Item(item.pp, item.ini, len(tokens))
        for item in chart[-1]
        if item.is_final(root)
    ]
