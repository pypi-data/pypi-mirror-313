namespace cpp context
namespace py context

enum TaskType {
  UNSPECIFIED = 0,
  PRETRAIN = 1,
  SFT = 2,
  INFERENCE = 3,
  EVAL = 4,
  TEST = 5,
}

// TaskContext for the tasks hosted by a given zk node.
struct TaskContext {
  // Task name, could be composed by project_name.task_id
  1: optional string task_id,
  2: optional TaskType task_type = TaskType.PRETRAIN,

  // Task environment serialized string according to task_type.
  // e.g. if task_type == pretrain, it's serialized from DatasetContext
  // including dataset checkpoint.
  10: optional string task_env,
}

// NodeContext for each zookeeper node.
struct NodeContext {
  // Machine name/id
  1: optional string node_name,
  // Container name/id
  2: optional string host_name,
  // task_id -> task context
  3: optional map<string, TaskContext> task_info_map,
}
