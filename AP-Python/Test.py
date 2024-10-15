import gurobipy as gp
from gurobipy import GRB

# 创建模型
model = gp.Model("WarehouseLogistics")

# 产品集合
products = ["Product1", "Product2", "Product3"]

# 仓库集合
warehouses = ["Warehouse1", "Warehouse2"]

# 每个产品在每个仓库的初始库存
initial_stock = {
    ("Product1", "Warehouse1"): 100,
    ("Product1", "Warehouse2"): 80,
    ("Product2", "Warehouse1"): 60,
    ("Product2", "Warehouse2"): 40,
    ("Product3", "Warehouse1"): 80,
    ("Product3", "Warehouse2"): 60
}

# 每个产品在每个仓库的容量限制
warehouse_capacity = {
    "Warehouse1": 200,
    "Warehouse2": 150
}

# 每个产品从一个仓库搬运到另一个仓库的单位成本
transport_cost = {
    ("Product1", "Warehouse1", "Warehouse2"): 5,
    ("Product1", "Warehouse2", "Warehouse1"): 4,
    ("Product2", "Warehouse1", "Warehouse2"): 3,
    ("Product2", "Warehouse2", "Warehouse1"): 3,
    ("Product3", "Warehouse1", "Warehouse2"): 6,
    ("Product3", "Warehouse2", "Warehouse1"): 5
}

# 决策变量：从一个仓库搬运到另一个仓库的产品数量
x = model.addVars(products, warehouses, warehouses, name="x")

# 目标函数：最小化搬运成本
model.setObjective(gp.quicksum(
    transport_cost[(p, i, j)] * x[p, i, j]
    for p in products
    for i in warehouses
    for j in warehouses if i!= j
), GRB.MINIMIZE)

# 约束1：每个仓库搬运后的库存不能超过其容量
for w in warehouses:
    model.addConstr(gp.quicksum(
        initial_stock[(p, w)] + gp.quicksum(x[p, i, w] for i in warehouses if i!= w) - gp.quicksum(x[p, w, j] for j in warehouses if j!= w)
        for p in products
    ) <= warehouse_capacity[w])

# 约束2：搬运的数量不能为负数
for p in products:
    for i in warehouses:
        for j in warehouses:
            if i!= j:
                model.addConstr(x[p, i, j] >= 0)

# 解决模型
model.optimize()

# 输出结果
if model.status == GRB.OPTIMAL:
    print('Optimal solution found:')
    for p in products:
        for i in warehouses:
            for j in warehouses:
                if i!= j and x[p, i, j].x > 0:
                    print(f"Move {x[p, i, j].x} units of {p} from {i} to {j}")
    print(f"Total cost: {model.objVal}")
else:
    print('No optimal solution found')