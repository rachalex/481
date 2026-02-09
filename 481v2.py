import os
import re
import pandas as pd
from collections import defaultdict
from graphviz import Source

# =========================
# CONFIG
# =========================
dot_input = r"C:\Users\rach_\Downloads\Sun-isolates_dWag-481-nad10.dot"
excel_file = r"C:\Users\rach_\Downloads\parsed_481.xlsx"
downloads_dir = r"C:\Users\rach_\Downloads"
output_basename = "Sun-isolates_dWag-481-nad10_ANNOTATED"

target_ancestor = "0"


with open(dot_input, "r", encoding="latin-1") as f:
    dot_text = f.read()



def normalize(x):
    x = str(x)
    return x.replace("HTU", "").replace("HYU", "")

edges_df = pd.read_excel(excel_file, sheet_name="edges")
edges_df["edge_start"] = edges_df["edge_start"].apply(normalize)
edges_df["edge_end"] = edges_df["edge_end"].apply(normalize)


dot_nodes = set()
node_pattern = re.compile(r"^\s*(\d+)\s*\[")

for line in dot_text.splitlines():
    m = node_pattern.match(line)
    if m:
        dot_nodes.add(m.group(1))



label_pattern = re.compile(r"label\s*=\s*([^,\]]+)")

raw_labels = {}
for line in dot_text.splitlines():
    line = line.strip()
    if "[" in line and "label=" in line:
        try:
            left, right = line.split("[", 1)
            node_id = left.strip()
            attrs = right.split("]", 1)[0]
            m = label_pattern.search(attrs)
            if m:
                label_val = m.group(1).strip().strip('"')
                raw_labels[node_id] = label_val
        except ValueError:
            continue

leaf_labels = {}
for k, v in raw_labels.items():
    leaf_labels[normalize(k)] = v


indegree = defaultdict(int)
dot_edge_pattern = re.compile(r"^\s*(\d+)\s*->\s*(\d+)\s*\[")

for line in dot_text.splitlines():
    m = dot_edge_pattern.match(line)
    if m:
        src, tgt = m.groups()
        indegree[tgt] += 1

reticulation_nodes = {n for n, deg in indegree.items() if deg > 1}


# =========================
# Excel Adjacency (for descendants only)
# =========================
children = defaultdict(list)
for _, row in edges_df.iterrows():
    parent = row["edge_start"]
    child = row["edge_end"]
    children[parent].append(child)

for n in dot_nodes:
    children[n]



dot_lines = dot_text.splitlines()
new_dot_lines = []

edge_pattern = re.compile(r'^(\s*)(\d+)\s*->\s*(\d+)\s*(\[[^\]]*\])\s*;')

for line in dot_lines:
    m = edge_pattern.match(line)
    if m:
        indent, src, tgt, attr_block = m.groups()
        if tgt in reticulation_nodes:
            attrs = attr_block.strip()[1:-1].strip()
            if attrs:
                attrs = attrs + ", penwidth=4.0, color=black"
            else:
                attrs = "penwidth=4.0, color=black"
            new_dot_lines.append(f"{indent}{src} -> {tgt} [{attrs}];")
            continue
    new_dot_lines.append(line)

dot_text = "\n".join(new_dot_lines)


# =========================
# Descendants
# =========================
def get_descendants(node, children, memo):
    if node in memo:
        return memo[node]
    desc = set(children[node])
    for c in children[node]:
        desc |= get_descendants(c, children, memo)
    memo[node] = desc
    return desc

memo = {}
descendants = {node: get_descendants(node, children, memo) for node in children.keys()}


dot_starts = set()
dot_ends = set()

for line in dot_text.splitlines():
    m = dot_edge_pattern.match(line)
    if m:
        src, tgt = m.groups()
        dot_starts.add(src)
        dot_ends.add(tgt)

terminal_leaves = dot_ends - dot_starts


# ============================================================
# PDF 
# ============================================================
highlight_lines_orig = []

for node in dot_nodes:
    base_label = leaf_labels.get(node, f"HTU{node}")

    if node in reticulation_nodes:
        highlight_lines_orig.append(
            f'    {node} [label="{base_label}", shape=doublecircle, color=red, penwidth=4.0];'
        )

    elif node in terminal_leaves:
        highlight_lines_orig.append(
            f'    {node} [label="{base_label}", shape=box, color=blue, penwidth=2.0];'
        )

    else:
        highlight_lines_orig.append(
            f'    {node} [label="{base_label}"];'
        )

legend_lines = [
    '    subgraph cluster_legend {',
    '        label="Legend";',
    '        fontsize=12;',
    '        labelloc="t";',
    '        style="rounded,dashed";',
    '        color=gray;',
    '        legend_retic [label="Red doublecircle: indegree>1 in DOT", shape=plaintext];',
    '        legend_incoming [label="Black: incoming edges to reticulation nodes", shape=plaintext];',
    '        legend_term [label="Blue box: terminal leaves", shape=plaintext];',
    '    }'
]

highlight_lines_orig.extend(legend_lines)
highlight_block_orig = "\n".join(highlight_lines_orig)

insert_pos = dot_text.rfind("}")
new_dot_text_orig = dot_text[:insert_pos] + "\n\n" + highlight_block_orig + "\n}"


orig_dot_path = os.path.join(downloads_dir, output_basename + "_ORIGINAL.dot")
with open(orig_dot_path, "w", encoding="latin-1") as f:
    f.write(new_dot_text_orig)

src_orig = Source(new_dot_text_orig)
src_orig.render(
    filename=output_basename + "_ORIGINAL",
    directory=downloads_dir,
    format="pdf",
    cleanup=True
)

highlight_lines_rj = []

for node in dot_nodes:
    base_label = leaf_labels.get(node, f"HTU{node}")

    if node in reticulation_nodes:
        highlight_lines_rj.append(
            f'    {node} [label="{base_label}", shape=doublecircle, color=red, penwidth=4.0];'
        )

    elif node in terminal_leaves:
        if base_label.startswith("HTU"):
            highlight_lines_rj.append(
                f'    {node} [label="{base_label}", shape=box, color=blue, penwidth=2.0];'
            )
        else:
            htu_label = f"HTU{node}"
            taxid_label = base_label
            record_label = f'{{ {htu_label} | <r> {taxid_label} }}'

            highlight_lines_rj.append(
                f'    {node} [label="{record_label}", shape=box, color=blue, penwidth=2.0, labeljust="l", labelloc="c"];'
            )

    else:
        highlight_lines_rj.append(
            f'    {node} [label="{base_label}"];'
        )

highlight_lines_rj.extend(legend_lines)
highlight_block_rj = "\n".join(highlight_lines_rj)

new_dot_text_rj = dot_text[:insert_pos] + "\n\n" + highlight_block_rj + "\n}"


rj_dot_path = os.path.join(downloads_dir, output_basename + "_RIGHTJUSTIFIED.dot")
with open(rj_dot_path, "w", encoding="latin-1") as f:
    f.write(new_dot_text_rj)

src_rj = Source(new_dot_text_rj)
src_rj.render(
    filename=output_basename + "_RIGHTJUSTIFIED",
    directory=downloads_dir,
    format="pdf",
    cleanup=True
)

print("PDF #1 (original) saved:", os.path.join(downloads_dir, output_basename + "_ORIGINAL.pdf"))
print("PDF #2 (right-justified) saved:", os.path.join)