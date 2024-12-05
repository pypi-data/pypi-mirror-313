namespace cpp proto

include "proto/data_base.thrift"
include "proto/breadcrumb.thrift"
include "proto/linkinfo.thrift"

// Anchor text that are processed by counting duplicated.
struct Anchor {
  1: string text,
  2: bool indomain,
  3: i32 count, 
  4: data_base.AnchorType type = data_base.AnchorType.NORMAL_ANCHOR,
  5: i16 pr_bucket,
  6: bool inboilerplate,
  7: data_base.DocType doctype = data_base.DocType.NORMAL,
  8: optional i32 filter_masks = 0,
  9: optional double inconfidence = 0,
  10: optional i32 weight_ex,
  11: optional i32 mutual_link_count,
  12: optional i32 mutual_link_weight,
  13: optional i32 stuffing_link_count,
  14: optional i32 stuffing_link_weight,
  15: data_base.CoreContentType corecontenttype = data_base.CoreContentType.UNKNOWN,
}

struct MergedDoc {
  1: i64 docid = 0,
  2: string url,
  // Web page raw content.
  3: string content,
  4: string seg_body,
  5: string seg_title,
  6: string seg_url,
  7: i16 pagerank = 0,
  8: list<Anchor> anchors,
  9: list<string> seg_anchors,

  11: bool is_dup,
  12: string chash,
  13: bool is_curl,
  14: data_base.DocType doc_type = data_base.DocType.NORMAL,
  16: i64 crawled_timestamp = 0,
  17: i64 content_timestamp = 0,

  30: list<linkinfo.InLink> inlinks,
  32: list<linkinfo.OutLink> outlinks,
  38: i32 language = 0,
  39: bool content_compressed,
  40: i32 domain_id = 0,
  42: i16 host_rank = 0,
  62: string title,
  65: optional list<breadcrumb.BreadCrumb_Item> breadcrumb_info,
  76: data_base.DocFormat orig_doc_format = data_base.DocFormat.DOCFORMAT_HTML,
  136: string body,
  137: double perplexity,
  138: i16 domain_level = 0,
}
