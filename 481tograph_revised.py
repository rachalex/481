import os
import pandas as pd
from collections import defaultdict
from graphviz import Source

# CONFIGURATION
dot_input = r"C:\Users\rach_\Downloads\Sun-isolates_dWag-481-nad10.dot"
excel_file = r"C:\Users\rach_\Downloads\parsed_481.xlsx"
downloads_dir = r"C:\Users\rach_\Downloads"
output_basename = "Sun-isolates_dWag-481-nad10_ANNOTATED"


target_ancestor = "0"  # example; update to your real ancestor of interest

# Load DOT file as raw text (preserves layout)
with open(dot_input, "r", encoding="latin-1") as f:
    dot_text = f.read()

# Load Excel edges sheet
edges_df = pd.read_excel(excel_file, sheet_name="edges")

# Normalize edge_start and edge_end to string node IDs
edges_df['edge_start'] = edges_df['edge_start'].apply(lambda x: str(abs(int(x))))
edges_df['edge_end'] = edges_df['edge_end'].astype(str)


children = defaultdict(list)
for _, row in edges_df.iterrows():
    parent = row['edge_start']
    child = row['edge_end']
    children[parent].append(child)

children = defaultdict(list)
for _, row in edges_df.iterrows():
    parent = row['edge_start']
    child = row['edge_end']
    children[parent].append(child)

all_nodes = set(edges_df['edge_start']).union(edges_df['edge_end'])
for n in all_nodes:
    children[n] 

# Recursive descendant computation
def get_descendants(node, children, memo):
    if node in memo:
        return memo[node]
    desc = set(children[node])
    for c in children[node]:
        desc |= get_descendants(c, children, memo)
    memo[node] = desc
    return desc

memo = {}
node_list = list(children.keys())  # freeze keys
descendants = {node: get_descendants(node, children, memo) for node in node_list}

# Compute terminal leaves and reticulation nodes
edge_starts = set(edges_df['edge_start'].tolist())
edge_ends = set(edges_df['edge_end'].tolist())

terminal_leaves = edge_ends - edge_starts

# Reticulation nodes: nodes with indegree > 1
end_counts = edges_df['edge_end'].value_counts()
reticulation_nodes = end_counts[end_counts > 1].index.tolist()

# Extract leaf labels from DOT text (NCBI accessions)
leaf_labels = {}

for line in dot_text.splitlines():
    line = line.strip()
    if "[" in line and "label=" in line:

        try:
            left, right = line.split("[", 1)
            node_id = left.strip()
            attrs = right.split("]", 1)[0]
            parts = attrs.split("label=")
            if len(parts) > 1:
                label_part = parts[1].split(",", 1)[0].strip()
                
                label_part = label_part.strip('";')
                leaf_labels[node_id] = label_part
        except ValueError:
            continue

# Descendant leaves for each reticulation node
reticulation_leaves = {}
for r in reticulation_nodes:
    desc = descendants.get(r, set())
    leaf_desc = [d for d in desc if d in terminal_leaves]
    reticulation_leaves[r] = leaf_desc

# Map reticulation node -> list of NCBI accessions (from labels)
reticulation_accessions = {
    r: [leaf_labels.get(leaf, leaf) for leaf in leaves]
    for r, leaves in reticulation_leaves.items()
}

# Build highlight and annotation DOT code
highlight_lines = []

for node, desc in descendants.items():

    highlight_lines.append(
        f'    {node} [xlabel="desc={len(desc)}"];'
    )

if target_ancestor in descendants:
    subtree_nodes = descendants[target_ancestor] | {target_ancestor}
  
    for node in subtree_nodes:
        highlight_lines.append(
            f'    {node} [color=purple, style=filled, fillcolor=lavender];'
        )
  
    for _, row in edges_df.iterrows():
        src = row['edge_start']
        tgt = row['edge_end']
        if src in subtree_nodes:
            highlight_lines.append(
                f'    {src} -> {tgt} [color=purple, penwidth=3.0];'
            )

# Reticulation edges and nodes (indegree > 1)
for _, row in edges_df.iterrows():
    src = row['edge_start']
    tgt = row['edge_end']
    if tgt in reticulation_nodes:
        
        highlight_lines.append(
            f'    {src} -> {tgt} [color=red, penwidth=4.0, style=bold];'
        )

for r in reticulation_nodes:
    highlight_lines.append(
        f'    {r} [shape=doublecircle, color=red, penwidth=4.0];'
    )


for r, accs in reticulation_accessions.items():
    if accs:
        acc_str = ",".join(accs)
       
        highlight_lines.append(
            f'    {r} [xlabel="NCBI:{acc_str}"];'
        )

for leaf in terminal_leaves:
    highlight_lines.append(
        f'    {leaf} [shape=box, color=blue, penwidth=2.0];'
    )

# Legend 
legend_lines = [
    '    subgraph cluster_legend {',
    '        label="Legend";',
    '        fontsize=12;',
    '        labelloc="t";',
    '        style="rounded,dashed";',
    '        color=gray;',
    '        legend_desc [label="desc=N: number of descendants", shape=plaintext];',
    '        legend_subtree [label="Purple: highlighted subtree from chosen ancestor", shape=plaintext];',
    '        legend_retic [label="Red doublecircle + red edges: reticulation nodes and incoming edges", shape=plaintext];',
    '        legend_term [label="Blue box: terminal leaves", shape=plaintext];',
    '        legend_ncbi [label="NCBI:... in xlabel: descendant leaf accessions for reticulation nodes", shape=plaintext];',
    '    }'
]
highlight_lines.extend(legend_lines)

highlight_block = "\n".join(highlight_lines)


insert_pos = dot_text.rfind("}")
if insert_pos == -1:
    raise ValueError("DOT file missing closing brace '}'")

new_dot_text = dot_text[:insert_pos] + "\n\n" + highlight_block + "\n}"

# Save new DOT file
new_dot_path = os.path.join(downloads_dir, output_basename + ".dot")
with open(new_dot_path, "w", encoding="latin-1") as f:
    f.write(new_dot_text)

# Render PDF from the new DOT file
src = Source(new_dot_text)
src.render(
    filename=output_basename,
    directory=downloads_dir,
    format="pdf",
    cleanup=True
)

print("New DOT file saved to:", new_dot_path)
print("PDF saved to:", os.path.join(downloads_dir, output_basename + ".pdf"))