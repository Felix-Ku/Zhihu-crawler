# Zhihu-crawler
A crawler for dynamic generated website such as Zhihu to extract personal information using Selenium

## Background
- Link of website: https://www.zhihu.com/
- Zhihu is one of the largest knowledges sharing platform in China. It operates in a way similar to Quora where users can post or answer questions and share their opinions on hot debate topics with others.
- This program intends to extract a list of user’s answers on specific questions and organize them for better interpertation.
- Dynamically generated website

## Functions

### 1. User Report
1.	Enter the username of the user that you want to search
2.	Return a csv file user report with the following information:
  a.	Basic information about the user
  b.	Total likes of user’s answers
  c.	A list of the user’s interested topics
  d.	A list of the user’s starred questions

### 2. Question Search
1.	Enter keyword for questions you want to search
2.	Return a list of question for user to choose from
3.	After choosing the question you want to see, return a csv file with a list of the following information:
  a.	Title of the question
  b.	Detail information of all answers
  c.	Number of answers

## Output
- Report for answers in .json format
- Report for users in .json format

### Sample

![Alt text](Sample_output.png)

## Reference
- https://blog.csdn.net/qq_36962569/article/details/77200118?utm_medium=distribute.pc_relevant.none-task-blog-title-3&spm=1001.2101.3001.4242
