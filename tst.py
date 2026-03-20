#from rag.query_engine import QAQueryEngine

#engine = QAQueryEngine()

#print(engine.answer("What is automation coverage for the Login module?"))


##from rag.analytics_router import detect_intent

#print(detect_intent("What is automation coverage for Login?"))
##print(detect_intent("Show automation trend over last 4 sprints"))
#print(detect_intent("Explain defect removal efficiency"))


#from analytics.automation import automation_summary

#summary = automation_summary()
#print(summary)

#from analytics.automation_trend import automation_trend

#df, summary = automation_trend(last_n_sprints=4)

#print(df)
#print(summary)

#from analytics.automation_trend import automation_trend

###df, summary = automation_trend(last_n_sprints=4)

#print(df)
#print(summary)


#from analytics.automation_trend import automation_trend
##from analytics.visuals import plot_automation_trend




#from analytics.visuals import plot_automation_trend
#import matplotlib.pyplot as plt
#trend_df, summary = automation_trend(last_n_sprints=4)
###fig = plot_automation_trend(trend_df)
#plt.show(block=True)

#from src.rag.unified_handler import handle_query

# # Text-only
# print(handle_query("What is automation coverage?")["text"])

# # Trend explanation
# print(handle_query("Explain automation trend")["text"])

# # Trend with visualization
# res = handle_query("Show automation trend over last 4 sprints")
# print(res["text"])
# res["figure"].show()


#from src.rag.unified_handler import handle_query
#print(handle_query("Show automation trend")["text"])


#print(handle_query("What is defect removal efficiency?")["text"])

# from src.rag.query_engine import QAQueryEngine  
# engine = QAQueryEngine()

# print(engine.query("What is defect removal efficiency?"))
# print(engine.query("What is automation coverage for Login module?"))


# from src.rag.unified_handler import handle_query

# print(handle_query("What is defect removal efficiency?")["text"])
# print(handle_query("Show automation trend over last 4 sprints")["text"])

# from src.analytics.defects import defect_summary

# print(defect_summary())

# import pandas as pd

# df = pd.read_csv("src/data/documents/defects.csv")
# print(df.columns.tolist())

# from src.analytics.defects import defect_summary
# print(defect_summary())

# from src.analytics.defect_leakage import defect_leakage_trend

# df, summary = defect_leakage_trend(last_n_sprints=4)

# print(df)
# print(summary)


# from src.analytics.defect_leakage import defect_leakage_trend

# df, summary = defect_leakage_trend(last_n_sprints=4)

# print(df)
# print(summary)







# import matplotlib.pyplot as plt


# def plot_defect_leakage(trend_df):
#     fig, ax = plt.subplots()
#     ax.plot(
#         trend_df["Sprint_Number"],
#         trend_df["Production_Defects"],
#         marker="o",
#     )
#     ax.set_title("Production Defect Leakage Trend")
#     ax.set_xlabel("Sprint")
#     ax.set_ylabel("Production Defects")
#     ax.grid(True)
#     return fig


# fig = plot_defect_leakage(df)
# fig.show()

# from src.analytics.execution import execution_stability_trend, flaky_tests

# trend_df, summary = execution_stability_trend(last_n_sprints=4)
# print(trend_df)
# print(summary)

# flaky = flaky_tests()
# print(f"Flaky tests found: {len(flaky)}")
# print(flaky.head())

# from src.rag.unified_handler import handle_query

# print(handle_query("What is defect removal efficiency?")["text"])
# print(handle_query("Is execution stable?")["text"])
# print(handle_query("Are there flaky tests?")["text"])


# from src.agents.router_agent import intent_router

# state = {
#     "query": "Which modules are risky next sprint?",
#     "intent": None,
#     "analytics_result": None,
#     "risk_result": None,
#     "rag_context": None,
#     "final_answer": None,
# }

# print(intent_router(state))


# from src.agents.analytics_agent import analytics_agent

# state = {
#     "query": "What is automation coverage?",
#     "intent": "analytics",
#     "analytics_result": None,
#     "risk_result": None,
#     "rag_context": None,
#     "final_answer": None,
# }

# print(analytics_agent(state)["analytics_result"])


from src.agents.risk_agent import risk_agent

state = {
    "query": "Which modules are risky next sprint?",
    "intent": "risk",
    "analytics_result": None,
    "risk_result": None,
    "rag_context": None,
    "final_answer": None,
}

print(risk_agent(state)["risk_result"])


# from src.agents.intent_router import route_intent

# queries = [
#     "Which modules are risky next sprint?",
#     "Is execution stable?",
#     "Explain defect removal efficiency",
#     "What is regression testing?"
# ]

# for q in queries:
#     print(q, "→", route_intent(q))


# from src.agents.orchestrator import orchestrate

# queries = [
#     "Which modules are risky next sprint?",
#     "Is execution stable?",
#     "Explain defect removal efficiency",
#     "What is regression testing?",
# ]

# for q in queries:
#     state = {
#         "query": q,
#         "intent": None,
#         "analytics_result": None,
#         "risk_result": None,
#         "rag_context": None,
#         "final_answer": None,
#     }

#     result = orchestrate(state)
#     print("\nQ:", q)
#     print("Intent:", result["intent"])
#     print("Answer:", result["final_answer"])



# # from src.agents.orchestrator import orchestrate

# # state = {
# #     "query": "who is Atul Dandin?",
# #     "intent": None,
# #     "analytics_result": None,
# #     "risk_result": None,
# #     "rag_context": None,
# #     "final_answer": None,
# # }

# # result = orchestrate(state)
# print(_rag_engine.retrieve("Who is Atul Dandin"))

# from src.rag.query_engine import QAQueryEngine

# engine = QAQueryEngine()

# print(engine.retrieve("Who is Atul Dandin?"))


# from src.analytics.defect_lookup import get_defect_by_id

# print(get_defect_by_id("DF_0007"))

from src.analytics.execution_lookup import get_execution_by_test_case
print(get_execution_by_test_case("TC_0108"))







