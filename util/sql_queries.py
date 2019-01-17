

def query_all_posts(forum_id, date_from, date_to):
    select_clause = """select distinct (replace(replace(p.content, E'\n', ' '), E'\t', '')) post, p.date, t.title as topic_title, concat_ws('/', c2.title,c1.title,c.title) as category from post p
    inner join topic t on p.topic = t.topic_id
    inner join category c on t.category = c.category_id
    full outer join category c1 on c.parent_category = c1.category_id
    full outer join category c2 on c1.parent_category = c2.category_id"""

    select_clause += " where c.forum=" + str(forum_id)
    select_clause += " and p.date > '" + str(date_from) + "' and p.date<'" + str(date_to) + "'"
    select_clause += " group by p.content, p.date, t.title, c2.title, c1.title, c.title"

    return select_clause
