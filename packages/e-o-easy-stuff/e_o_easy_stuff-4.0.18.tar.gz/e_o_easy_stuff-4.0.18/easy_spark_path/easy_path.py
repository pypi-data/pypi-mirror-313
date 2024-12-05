class Path:
    def __init__(self, workspace_id: str, warehouse_id: str):
        self.workspace_id = workspace_id
        self.warehouse_id = warehouse_id
        self.path = f"abfss://{workspace_id}@onelake.dfs.fabric.microsoft.com/{warehouse_id}"
