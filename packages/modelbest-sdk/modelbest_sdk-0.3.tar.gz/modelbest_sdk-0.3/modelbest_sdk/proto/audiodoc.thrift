namespace py proto
namespace cpp proto


struct AudioMeta {
    1: required string void_id,
    2: optional string title,
    3: required i32 offset,
    4: required i32 audio_end,
    5: optional string source,
}

struct AudioDoc {
    1: required binary buffer,
    2: required list<i32> shape,
    3: optional AudioMeta meta,
    4: required string id,
}

// to be deperecated, use mm_doc instead
struct WaveDoc {
    // basic info
    10: required list<list<i32> > token_ids,  // 二阶张量
    11: required list<i32> shape,  // token_ids的shape
}
