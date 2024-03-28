from utils import Utils

c1 = Utils.load_config("test_workflow.yaml")
c2 = Utils.load_config("test_workflow_extended.yaml")

workflows_old = c1["workflows"]
workflows_new = c2["workflows"]

for i in range(len(workflows_old)):
    num_nodes_1 = len(workflows_old[i]["nodes"])
    num_nodes_2 = len(workflows_new[i]["nodes"])

    if num_nodes_1 < num_nodes_2:
        run[workflows_old[i]["name"]] = num_nodes_2 - num_nodes_1


num_workflows1 = len(c1["workflows"])
num_workflows2 = len(c2["workflows"])

names_w1 = [c1["workflows"][i]["name"] for i in range(num_workflows1)]
names_w2 = [c2["workflows"][i]["name"] for i in range(num_workflows2)]

names_new = [name for name in names_w2 if name not in names_w1]

cutoff = num_workflows2 - num_workflows1

old = c2["workflows"][:cutoff]
new = c2["workflows"][cutoff:]

# Workflows
# List that contains the workflow names to skip (or to run, doesnt matter)

# Nodes
# Cutoff number is sufficient

# Combined
# Dict {workflow_name: node_cutoff}

run = {}

# Iterate over the indices
for i in range(len(old)):
    num_nodes_1 = len(c1["workflows"][i]["nodes"])
    num_nodes_2 = len(c2["workflows"][i]["nodes"])
    if num_nodes_1 < num_nodes_2:
        run[c1["workflows"][i]["name"]] = num_nodes_2 - num_nodes_1

for name in names_new:
    run["name"] = 0

print(run)