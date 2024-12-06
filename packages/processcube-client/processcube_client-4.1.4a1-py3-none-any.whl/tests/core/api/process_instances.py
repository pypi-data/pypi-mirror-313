from processcube_client.core.api.client import Client, ProcessInstanceQueryRequest

def query_instance():
    client = Client("http://localhost:56100")

    result = client.process_instance_query(ProcessInstanceQueryRequest(
        limit=1,
        process_model_id="ProcessResult_Process"
    ))

    print(result[0].end_token) 


def query_by_correlation():
    client = Client("http://localhost:56100")

    result = client.process_instance_query(ProcessInstanceQueryRequest(
        limit=1,
        correlation_id="037f337b-2855-4a36-86bc-a298a3ab873b"
    ))

    print(result[0].end_token)

def main():
    #query_instance()
    query_by_correlation()

if __name__ == '__main__':
    main()