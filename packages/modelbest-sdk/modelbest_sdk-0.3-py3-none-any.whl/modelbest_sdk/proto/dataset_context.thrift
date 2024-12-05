namespace cpp proto
namespace py proto

struct DatasetContext {
  // Global training args for dataset.
  1: optional i32 rank,
  2: optional i32 world_size,
  3: optional i32 tp_size,
  4: optional i32 tp_rank,
  5: optional i32 num_workers,

  // Dataset config file location to read dataset info.
  30: optional string dataset_config_path,
  // Dataset checkpoint file location to read checkpoint list.
  31: optional string dataset_checkpoint_path,
}
