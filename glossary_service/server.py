import grpc
from concurrent import futures
import time
import uuid
import json

# Import generated classes
import glossary_pb2
import glossary_pb2_grpc

from flask import Flask, jsonify, request, send_from_directory

# In-memory data store
TERMS_DB = {
    "1": {
        "id": "1",
        "term": "gRPC",
        "definition": "A high-performance, open-source universal RPC framework.",
        "source_links": ["https://grpc.io/"],
        "related_term_ids": ["2"]
    },
    "2": {
        "id": "2",
        "term": "Protocol Buffers",
        "definition": "Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data.",
        "source_links": ["https://developers.google.com/protocol-buffers"],
        "related_term_ids": ["1"]
    },
    "3": {
        "id": "3",
        "term": "Docker",
        "definition": "A platform for developing, shipping, and running applications in containers.",
        "source_links": ["https://www.docker.com/"],
        "related_term_ids": []
    }
}

class GlossaryService(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetTerm(self, request, context):
        term_id = request.term_id
        term_data = TERMS_DB.get(term_id)
        if term_data:
            return glossary_pb2.Term(**term_data)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Term not found')
            return glossary_pb2.Term()

    def AddTerm(self, request, context):
        new_id = str(uuid.uuid4())
        term = {
            "id": new_id,
            "term": request.term,
            "definition": request.definition,
            "source_links": list(request.source_links),
            "related_term_ids": list(request.related_term_ids)
        }
        TERMS_DB[new_id] = term
        return glossary_pb2.Term(**term)

    def ListTerms(self, request, context):
        terms_list = [glossary_pb2.Term(**term) for term in TERMS_DB.values()]
        return glossary_pb2.TermList(terms=terms_list)

# --- Flask App for REST API and Frontend ---
app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/terms', methods=['GET'])
def list_terms():
    return jsonify(list(TERMS_DB.values()))

@app.route('/api/terms/<term_id>', methods=['GET'])
def get_term(term_id):
    term = TERMS_DB.get(term_id)
    if term:
        return jsonify(term)
    return jsonify({"error": "Term not found"}), 404
    
def serve():
    # gRPC Server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    print("gRPC server started on port 50051")

    # Flask Server
    # Running in a separate thread is not ideal for production, but simple for this demo
    # In a real app, you'd use a production-grade WSGI server like Gunicorn for Flask
    # and run gRPC and Flask as separate processes.
    app.run(host='0.0.0.0', port=8080)
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        grpc_server.stop(0)

if __name__ == '__main__':
    serve()
