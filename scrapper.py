import requests
import pandas as pd
import time

def get_problems():
    problems = []
    graphql_url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/problemset/all/"
    }
    query = """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        total: totalNum
        questions: data {
          title
          titleSlug
          content
        }
      }
    }
    """
    variables = {
        "categorySlug": "",
        "skip": 0,
        "limit": 50,
        "filters": {}
    }

    total_problems_fetched = 0
    while total_problems_fetched < 1000:
        response = requests.post(graphql_url, json={"query": query, "variables": variables}, headers=headers)
        data = response.json()

        if response.status_code != 200 or 'errors' in data:
            print("Error fetching data")
            break

        questions = data['data']['problemsetQuestionList']['questions']
        for question in questions:
            problems.append({
                'problem_title': question['title'],
                'problem_description': question['content'],
                'problem_link': f"https://leetcode.com/problems/{question['titleSlug']}/"
            })

        total_problems_fetched += len(questions)
        variables['skip'] += len(questions)

        if len(questions) == 0:
            break  # Exit if there are no more problems to fetch

        time.sleep(1)  # Be considerate and do not overload the server

    return problems[:1000]

problems = get_problems()

problems_df = pd.DataFrame(problems)
problems_df.to_csv('leetcode_problems.csv', index=False)

print("Scraping complete and data saved to leetcode_problems.csv")
