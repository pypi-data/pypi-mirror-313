class TrainParams:
    def __init__(self, project_id, run_id, algorithm, scope, label, dataset, params, epoch):
        self.project_id = project_id,
        self.run_id = run_id,
        self.algorithm = algorithm
        self.scope = scope
        self.label = label
        self.dataset = dataset
        self.params = params
        self.epoch = epoch

    def __repr__(self):
        return f"TrainParams(project_id={self.project_id}, run_id={self.run_id}, algorithm={self.algorithm}, " \
               f"scope={self.scope}, label={self.label}, dataset={self.dataset}, params={self.params})"