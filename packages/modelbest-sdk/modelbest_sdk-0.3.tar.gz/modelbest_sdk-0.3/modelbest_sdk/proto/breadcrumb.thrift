namespace cpp proto

struct BreadCrumb_Item {
  1: string text,
  2: bool islink,
  3: string url,
  4: string parenttext,
  5: i32 begin_pos = 0,
  6: i32 end_pos = 0,
}

struct BreadCrumb_Doc {
  // When save breadcrumb of one url, the doc have url
  // When save breadcrumb of one domain, url is empty
  1: string url,
  2: i32 domainid = 0,
  3: string domainname,
  4: list<BreadCrumb_Item> items,
}
