from processor_regrex import classify_with_regex
from processor_bert import classify_with_bert
from processor_LLM import classify_with_llm
import pandas as pd

def classify(logs):
    labels = []
    for source, log_meg in logs:
        label = classify_log(source,log_meg)
        labels.append(label)
    return labels

def classify_log(source,log_message):
    if source == "LegacyCRM":
        lable = classify_with_llm(log_message)
    else : 
        lable = classify_with_regex(log_message)
        if lable is None:
            lable = classify_with_bert(log_message)
    return lable

def classify_csv(input_file):
    df = pd.read_csv(input_file)
    #performing classification
    df['target_label'] = classify(list(zip(df['source'], df['log_message'])))

    output_file = "resources/output.csv"
    df.to_csv(output_file,index=False)


if __name__ == '__main__':
    classify_csv("resources/test.csv")
    # logs = [
    #     ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    #     ("BillingSystem", "User User12345 logged in."),
    #     ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
    #     ("AnalyticsEngine", "Backup completed successfully."),
    #     ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
    #     ("ModernHR", "Admin access escalation detected for user 9429"),
    #     ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    #     ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
    #     ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
    #     ("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
    # ]
    # labels = classify(logs)
    # print(labels)