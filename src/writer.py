# https://note.com/ippei_suzuki_us/n/n6792eb6321aa
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
# os.environ["OPENAI_API_KEY"] = "NA"

llm = ChatOpenAI(
    # model = "crewai-llama3",
    model = "elyza:jp8b",
    base_url = "http://localhost:11434/v1")

planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory="You're working on planning a blog article "
              "about the topic: {topic} in '<https://qiita.com/>'."
              "You collect information that helps the "
              "audience learn something "
              "and make informed decisions. "
              "You have to prepare a detailed "
              "outline and the relevant topics and sub-topics that has to be a part of the"
              "blogpost."
              "Your work is the basis for "
              "the Content Writer to write an article on this topic."
              "日本語で。",
    llm=llm,
    allow_delegation=False,
 verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic} in '<https://qiita.com/>'. "
              "You base your writing on the work of "
              "the Content Planner, who provides an outline "
              "and relevant context about the topic. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provide by the Content Planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements."
              "日本語で。",
    allow_delegation=False,
    llm=llm,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization '<https://qiita.com/>'. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible."
              "日本語で。",
    llm=llm,
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources."
        "日本語で。",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
  "3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs."
        "日本語で。",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs."
                    "日本語で。",
    agent=editor
)

# planner = Agent(
#     role="Content Planner",
#     goal="魅力的で正確な内容のコンテンツを{topic}に基づいて計画する。",
#     backstory="あなたは、<https://qiita.com/>に関する{topic}というテーマのブログ記事を計画しています。"
#               "読者が何かを学び、情報に基づいた判断を下せるような情報を収集します。"
#               "詳細なアウトラインや、ブログ記事に含めるべきトピックやサブトピックを準備する必要があります。"
#               "あなたの仕事は、Content Writerがこのトピックに基づいて記事を書くための基礎となります。",
#     llm=llm,
#     allow_delegation=False,
#  verbose=True
# )

# writer = Agent(
#     role="Content Writer",
#     goal="{topic}について洞察に満ちた正確な意見記事を書く。",
#     backstory="あなたは、<https://qiita.com/>に関する{topic}についての新しい意見記事を書いています。"
#               "執筆はContent Plannerの仕事に基づいて行われ、アウトラインと関連するコンテキストが提供されます。"
#               "Content Plannerが提供する主要な目的と方向性に従って執筆を進めます。"
#               "また、客観的で公平な洞察を提供し、それをContent Plannerが提供した情報で裏付けます。"
#               "意見と客観的な声明が異なる場合、意見であることを明確に示します。",
#     allow_delegation=False,
#     llm=llm,
#     verbose=True
# )

# editor = Agent(
#     role="Editor",
#     goal="ブログ記事を<https://qiita.com/>の組織のライティングスタイルに合わせて編集する。",
#     backstory="あなたは、Content Writerからブログ記事を受け取る編集者です。"
#               "記事がジャーナリズムのベストプラクティスに従っているか確認し、"
#               "意見や主張を提供する際にバランスの取れた視点を提供します。"
#               "可能であれば、大きな論争を呼ぶトピックや意見を避けます。",
#     llm=llm,
#     allow_delegation=False,
#     verbose=True
# )

# plan = Task(
#     description=(
#         "1. 最新のトレンド、主要なプレイヤー、注目すべきニュースを{topic}に基づいて優先順位付けする。\n"
#         "2. ターゲットオーディエンスを特定し、その興味や課題を考慮する。\n"
#         "3. 導入部、主要なポイント、行動喚起を含む詳細なコンテンツのアウトラインを作成する。\n"
#         "4. SEOキーワードと関連するデータや情報源を含める。"
#     ),
#     expected_output="アウトライン、オーディエンス分析、SEOキーワード、情報源を含む包括的なコンテンツ計画書。",
#     agent=planner,
# )

# write = Task(
#     description=(
#         "1. コンテンツ計画を使用して、{topic}に関する説得力のあるブログ記事を作成する。\n"
#         "2. SEOキーワードを自然に組み込む。\n"
#         "3. セクションや小見出しを魅力的な形式で適切に命名する。\n"
#         "4. 魅力的な導入部、洞察に満ちた本文、要約的な結論で記事を構成する。\n"
#         "5. 文法的なエラーやブランドの声との整合性をチェックする。"
#     ),
#     expected_output="公開準備が整った、Markdown形式のよく書かれたブログ記事。各セクションは2〜3段落にする。",
#     agent=writer,
# )

# edit = Task(
#     description=("文法エラーやブランドの声との整合性をチェックするために、指定されたブログ記事を校正する。"),
#     expected_output="公開準備が整った、Markdown形式のよく書かれたブログ記事。各セクションは2〜3段落にする。",
#     agent=editor
# )

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

# inputs = {"topic":"Comparative study of LangGraph, Autogen and Crewai for building multi-agent system."}
inputs = {"topic":"おいしいカレーの作り方についての研究"}
result = crew.kickoff(inputs=inputs)
