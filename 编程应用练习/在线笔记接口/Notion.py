from notion.client import NotionClient

# 获取 Notion 栏目
def get_notion_pages(token, database_id):
    # 实例化 NotionClient 客户端
    client = NotionClient(token_v2=token)
    # 根据 database_id 获取对应的数据库
    database = client.get_collection_view(database_id)
    # 获取数据库中的所有行
    pages = database.collection.get_rows()
    # 返回所有行
    return pages

# 获取文章集合
def get_notion_collection(token, collection_id):
    # 实例化 NotionClient 客户端
    client = NotionClient(token_v2=token)
    # 根据 collection_id 获取对应的集合
    collection = client.get_collection(collection_id)
    # 返回集合
    return collection

# 获取文章
def get_notion_page(token, page_id):
    # 实例化 NotionClient 客户端
    client = NotionClient(token_v2=token)
    # 根据 page_id 获取对应的页面
    page = client.get_block(page_id)
    # 返回页面
    return page

# 使用示例
token = "YOUR_NOTION_TOKEN"
database_id = "YOUR_NOTION_DATABASE_ID"
collection_id = "YOUR_NOTION_COLLECTION_ID"
page_id = "YOUR_NOTION_PAGE_ID"

# 获取 Notion 栏目
pages = get_notion_pages(token, database_id)
# 获取文章集合
collection = get_notion_collection(token, collection_id)
# 获取文章
page = get_notion_page(token, page_id)