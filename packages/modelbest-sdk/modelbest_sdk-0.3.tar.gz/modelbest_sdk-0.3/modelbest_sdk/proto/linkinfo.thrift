namespace cpp indexing
namespace php Indexing
namespace java com.chinaso.search.indexing.proto

include "proto/data_base.thrift"

struct OutLink {
  1: i64 docid,
  2: i32 hostid = 0,
  3: bool indomain,
  4: bool inboilerplate,
  5: i32 domainid = 0,
  6: string url,
  7: string text,
  8: data_base.AnchorType type = data_base.AnchorType.NORMAL_ANCHOR,
  9: bool nofollow = 0,
  10: bool incomment,
  11: optional i32 link_position,
  12: optional i32 link_index,
  13: optional i32 num_link,
  14: optional i32 num_tag,
  15: optional i32 tag_hash,
  16: optional i32 upper_context_hash,
  17: optional i32 downer_context_hash,
}

// If add new type, please
// add corresponding type into 
// indexing/pipeline/util/unilink_score_computer/unilink_score_computer.cc
enum LinkScorerType {
  UNKNOWN_SCORER = 0,
  // Uni_Outlink decay
  TIME_DECAY = 1,
  BLACKLIST_DECAY = 2,
  SPAM_LINK_DECAY = 3,
  LINK_COUNT_DECAY = 4,
  ANNOTATION_DECAY = 5,
  DEDECMS_DECAY = 6,
  SAME_IP_DECAY = 7,
  SPAM_DOC_DECAY = 8,
  NO_OUTLINK_CONTRIB_DECAY = 9,
  INFERRED_FRIENDLY_LINK_DECAY = 10,
  OUTLINK_TEXT_SPAM_DECAY = 11,
  DEAD_HOST_DECAY = 12,
  HIDDEN_TEXT_SRC_DECAY = 13,
  OUTLINK_SPAM_WORDS_STUFF_DECAY = 14,
  BLACKLIST_DOC_DECAY = 15,
  MUTUAL_LINK_BY_JS_DECAY = 16,
  BAD_DOC_TYPE_DECAY = 17,
  MUTUAL_LINK_BY_REDIRECT_DECAY = 18,
  ZOOSNET_DOC_DECAY = 19,
  CONTENT_DEDUP_DOC_DECAY = 20,
  
  // Uni_Inlink decay
  HASHDEDUP_DECAY = 21,
  BLACKLIST_INLINK_DECAY = 22,
  SPAM_INLINK_DECAY = 23,
  MUTUAL_LINK_DECAY = 24,
  LINK_STUFFING_DECAY = 25,
}

struct LinkAttributes {
 1: map<LinkScorerType, i16> attributes_info,
}

// Raw anchor text extracted from the source document.
struct InLink {
  1: string src_url,
  2: string text,
  3: data_base.AnchorType anchor_type = data_base.AnchorType.NORMAL_ANCHOR,
  4: i16 src_pagerank = 0,
  5: data_base.CoreContentType src_type = data_base.CoreContentType.UNKNOWN,
  6: bool indomain,
  7: i64 src_docid,
  8: i64 timestamp,
  9: bool inboilerplate,
  10: i32 src_hostid = 0,
  11: i32 src_domainid = 0,
  // when was this inlink extracted
  12: i64 extracted_timestamp = 0,
  13: optional i32 filter_masks = 0,
  14: optional double inconfidence = 0,
  15: i32 template_fingerprint = 0,
  16: bool incomment = 0,
  17: optional i32 link_position = 0,
  18: optional i32 link_index = 0,
  19: optional i32 num_link;
  20: optional i32 num_tag;
  21: optional i32 tag_hash;
  22: optional i32 upper_context_hash;
  23: optional i32 downer_context_hash;
  24: optional i16 link_score = 100,
  25: optional i32 language = 0,
  26: optional double spam_score = 0.0,
  27: optional data_base.FilterType blacklist_type,
  28: optional list<i64> redirect_domain_id_path,
  29: optional bool from_redirect,
  30: optional bool is_mutual_link,
  31: optional string link_attribute_from_anchor_pipeline,
  32: optional i64 src_main_content_anchor_hash;
  33: data_base.CoreContentType core_content_type = data_base.CoreContentType.UNKNOWN,
}

struct LinkScorerInfo {
  1: bool force_select,
  2: bool force_drop,
  3: i32 confidence, // lower_bound:0, upper_bound:100, the higher the better
  4: optional string message, // Comments: result and log for every handler
}

struct LinkStatus {
 1: map<LinkScorerType, LinkScorerInfo> link_infos,
 2: i16 link_score = 100, // 0 for worst, 100 for best
}

enum LinkDirection {
  UNKNOWN = 0,
  OUTLINK = 1,
  INLINK  = 2,
}
