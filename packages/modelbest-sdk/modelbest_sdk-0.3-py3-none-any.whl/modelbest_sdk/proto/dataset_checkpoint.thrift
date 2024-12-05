namespace py proto

struct Chunk {
  1: i32 epoch,
  2: i64 start,
  3: i64 stop
}

struct Used {
  1: map<Chunk, set<i64>> active,
  2: map<i32, set<Chunk>> done,
  3: i32 epoch
}

struct DatasetInfo {
  1: string path,
  2: optional double weight,
  3: optional i32 max_epoch,
  4: optional string name,
}

struct DatasetInfoList {
  1: list<DatasetInfo> dataset_info_list,
}

struct DatasetCheckpoint {
  1: DatasetInfo dataset_info,
  2: optional Used used,
  3: optional i32 chunk_size,
  4: optional i64 num_chunks,
  5: optional LastSample last_sample,
}

struct DatasetCheckpointList {
  1: list<DatasetCheckpoint> checkpoint_list,
  2: optional i32 world_size,
  3: optional i32 tp_size,
  4: optional i64 sample_idx,
  5: optional list<i64> current_samples
}

struct LastSample {
  1: Chunk chunk,
  2: i64 index,
  3: i64 offset
}