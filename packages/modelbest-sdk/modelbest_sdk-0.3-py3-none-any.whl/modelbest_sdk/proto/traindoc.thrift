namespace py proto
namespace cpp proto

struct BaseDoc {
    // basic info
    10: required list<i32> token_ids,      // token_ids须要包含bos_id和eos_id
    20: optional list<bool> mask,          // 大小与token_ids相同，true表示不需要算loss
    // extra info
    30: optional string docid,
    40: optional list<string> tag,
    50: optional list<string> token,
    // op info
    60: optional string tokenizer_version,  // Deprecated: will store tokenizer version in SSTableMetadata.
    // reserved cols
    70: optional string reserved_col,
}
