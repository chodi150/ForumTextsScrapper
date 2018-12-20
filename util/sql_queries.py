# select_clause = """select replace(replace(p.content, E'\n', ' '), E'\t', '') post, p.date, t.title as topic_title, concat_ws('/', c2.title,c1.title,c.title) as category from post p
# inner join topic t on p.topic = t.topic_id
# inner join category c on t.category = c.category_id
# full outer join category c1 on c.parent_category = c1.category_id
# full outer join category c2 on c1.parent_category = c2.category_id
# where c.forum = 7 and p.date > '2015-01-01 00:00:00.000000'"""



def query_all_posts(forum_id, date):
    select_clause = """select replace(replace(p.content, E'\n', ' '), E'\t', '') post, p.date, t.title as topic_title, concat_ws('/', c2.title,c1.title,c.title) as category from post p
    inner join topic t on p.topic = t.topic_id
    inner join category c on t.category = c.category_id
    full outer join category c1 on c.parent_category = c1.category_id
    full outer join category c2 on c1.parent_category = c2.category_id"""

    select_clause += " where c.forum=" + str(forum_id)+ " and  p.date > '2012-01-01 00:00:00.000000' and (c.title = 'Impreza' or c.title = 'Forester') "

    return select_clause
