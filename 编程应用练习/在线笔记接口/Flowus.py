import requests

# Flowus API基础URL
base_url = "https://api.flowus.io"

# 获取分类列表的函数
def get_categories():
    url = f"{base_url}/categories"
    response = requests.get(url)
    categories = response.json()
    return categories

# 获取某个分类下的文章列表的函数
def get_articles(category_id):
    url = f"{base_url}/categories/{category_id}/articles"
    response = requests.get(url)
    articles = response.json()
    return articles

# 获取特定文章的函数
def get_article(category_id, article_id):
    url = f"{base_url}/categories/{category_id}/articles/{article_id}"
    response = requests.get(url)
    article = response.json()
    return article

# 编辑特定分类的函数
def edit_category(category_id, new_name):
    url = f"{base_url}/categories/{category_id}"
    data = {
        "name": new_name
    }
    response = requests.put(url, json=data)
    return response.status_code == 200

# 编辑特定文章的函数
def edit_article(category_id, article_id, new_content):
    """
    通过向API发送PUT请求来编辑文章。

    参数:
        category_id (int): 包含文章的分类的ID。
        article_id (int): 要编辑的文章的ID。
        new_content (str): 要设置为文章的新内容。

    返回:
        bool: 如果文章成功编辑，则为True，否则为False。
    """
    url = f"{base_url}/categories/{category_id}/articles/{article_id}"
    data = {
        "content": new_content
    }
    response = requests.put(url, json=data)
    return response.status_code == 200

# 删除特定分类的函数
def delete_category(category_id):
    url = f"{base_url}/categories/{category_id}"
    response = requests.delete(url)
    return response.status_code == 204

# 删除特定文章的函数
def delete_article(category_id, article_id):
    url = f"{base_url}/categories/{category_id}/articles/{article_id}"
    response = requests.delete(url)
    return response.status_code == 204
