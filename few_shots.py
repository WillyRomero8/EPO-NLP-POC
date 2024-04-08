examples = [

    {'input': "How many requests were received?",
     'query': "SELECT SUM(Count) as 'Number of UP requests' FROM upp;",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many UPs have been received at the EPO?",
     'query': "SELECT SUM(Count) as 'Number of UP requests' FROM upp;",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many UP requests have been received at the EPO?",
     'query': "SELECT SUM(Count)  as 'Number of UP requests' FROM upp;",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many unitary patents request were registered?",
     'query': """SELECT SUM(Count) as 'Number of UP registered' FROM upp WHERE "Status of registration" = 'Registered'""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many unitary patents requests are still pending?",
     'query': """SELECT SUM(Count) as 'Number of pending UP requests' FROM upp WHERE "Status of registration" = 'Pending'""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many unitary patents requests are in Measurement?",
     'query': """SELECT SUM(Count) as 'Number of UP requests in Measurement' FROM upp WHERE "Technology" = 'Measurement'""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many requests were received from Germany so far?",
     'query': """SELECT SUM(Count) as 'Number of requests from Germany' FROM upp WHERE "Country" = 'Germany'""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "Out of the requests received from France, what is the proportion of withdrawals?",
     'query': """SELECT
                    ROUND(
                        CAST((SELECT SUM(Count) FROM upp WHERE "Country" = 'France' and "Status of request" = 'Withdrawn') as float)/
                        CAST((SELECT SUM(Count) FROM upp WHERE "Country" = 'France') as float) * 100, 2) as 'Percentage of withdrawals from France';""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},


    {'input': "What is the proportion of unitary patent registered?",
     'query': """SELECT
                    ROUND(
                        CAST((SELECT SUM(Count) FROM upp WHERE "Status of registration" = 'Registered') as float)/
                        CAST((SELECT SUM(Count) FROM upp) as float) * 100, 2) as 'Percentage of UP registered';""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "What is the Top-3 for Spain in terms of fields of technology?",
     'query': """SELECT SUM(Count) as 'Number of requests', Technology FROM upp WHERE Country = 'Spain' and Technology IS NOT NULL GROUP BY Technology ORDER BY SUM(Count) DESC LIMIT 3;""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "What is the number of UP requests received in Germany in 2023?",
     'query': """SELECT SUM(Count) as 'UP Requests'AS count FROM upp WHERE Country = 'Germany' and strftime('%Y', Date) = '2023';""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many UP requests have been received in average on a monthly basis since the launch of the system?",
     'query':""" WITH n_month AS
                    (SELECT CAST(Count(*) as float) as months
                    from (SELECT strftime('%m', Date), strftime('%Y', Date) FROM upp group by Date))
                    SELECT ROUND((SELECT CAST(SUM(Count) as float) from upp)/ months, 2) 'Monthly UP requests' from n_month """,
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many UP requests (in volumes and percentage of the total) originating from Europe have been received at the EPO in 2024?",
     'query': """ WITH num AS (SELECT cast(SUM(Count) as float) as cnt_f, SUM(Count) as cnt_i FROM upp WHERE Continent = 'Europe' and strftime('%Y', Date) = '2024'),
                          den AS (SELECT cast(SUM(Count) as float) as cnt FROM upp WHERE strftime('%Y', Date) = '2024')
                         SELECT num.cnt_i as 'Volume of request', ROUND(num.cnt_f/den.cnt * 100 , 2) 'Percentage of requests' from num, den """,
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "Show me a list of technology fields",
     'query':""" SELECT distinct Technology from upp WHERE Technology is not NULL""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many requests were filed in English?",
     'query':""" SELECT sum(Count) as 'Number of Requests' from upp WHERE "Language Procedural" = 'English' """,
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many requests have Dutch as translation language?",
     'query':""" SELECT sum(Count) as 'Number of Requests' from upp WHERE "Language Translation" = 'Dutch' """,
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "How many requests received from Spain were filed in French?",
     'query':""" SELECT coalesce(sum(Count), 0) as 'Requests received' from upp WHERE Country = 'Spain' AND "Language Procedural" = 'French' """,
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

     {'input': "In November 2023, what is the origin (country) of the requests filed in German?",
     'query':""" SELECT distinct Country from upp WHERE strftime('%m', Date) = '11' AND strftime('%Y', Date) = '2023' AND "Language Procedural" = 'German' """,
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "What are the top 3 technologies where other procedural languages than English are used most frequently?",
     'query':""" SELECT SUM(Count), Technology from upp  WHERE "Language Procedural" = 'English' AND Technology is not NULL GROUP BY Technology ORDER BY SUM(Count) LIMIT 3""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "What is the average rejection rate?",
     'query':""" SELECT
                    ROUND(
                        CAST((SELECT SUM(Count) FROM upp WHERE "Status of registration" = 'Rejection') as float)/
                        CAST((SELECT SUM(Count) FROM upp) as float) * 100, 2) as 'Avarage Rejection Rate in %'""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

    {'input': "What is rejection rate in percentage by country?",
     'query':""" with n_rej as ( SELECT SUM(Count) cnt, Country FROM upp WHERE "Status of registration" = 'Rejection' GROUP BY Country),
                    tot_rq as ( SELECT SUM(Count) cnt, Country FROM upp GROUP BY Country)
                    SELECT ROUND(cast(coalesce(n_rej.cnt, 0) as float)/cast(tot_rq.cnt as float) * 100, 2) 'Rejection Rate in %', n_rej.Country from tot_rq inner join n_rej on n_rej.Country = tot_rq.Country
                    ORDER BY 1 DESC""",
     'SQLResult': "SQLResult of the SQL SQLQuery",
     'Answer': ""},

]
