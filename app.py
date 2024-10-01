from flask import Flask, request, render_template_string

app = Flask(__name__)

# Store received requests
received_requests = []

# HTML template for displaying the received requests with Bootstrap and auto-refresh
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Received Requests</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Auto-refresh every 1 second -->
    <meta http-equiv="refresh" content="5">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="mb-4">Received POST Requests</h1>
        <div class="card">
            <div class="card-body">
                {% if requests %}
                    <table class="table table-bordered">
                        <thead class="thead-light">
                            <tr>
                                <th scope="col">Path & Headers</th>
                                <th scope="col">Payload</th>
                            </tr>
                        </thead>
                        <tbody>
                        {% for req in requests %}
                            <tr>
                                <td>
                                    <strong>Path:</strong> {{ req.path }} <br/>
                                    <strong>Headers:</strong> 
                                    <ul>
                                        {% for key, value in req.headers.items() %}
                                            <li><strong>{{ key }}:</strong> {{ value }}</li>
                                        {% endfor %}
                                    </ul>
                                </td>
                                <td>
                                    <pre>{{ req.data }}</pre>
                                </td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <p>No requests received yet.</p>
                {% endif %}
            </div>
        </div>
    </div>
    <!-- Bootstrap JS (optional) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    # Display all received POST requests with headers, payloads, and paths
    return render_template_string(html_template, requests=reversed(received_requests))

# Use wildcard to capture any path under /receive
@app.route('/api/<path:subpath>', methods=['POST'])
def receive_post(subpath):
    # Extract headers, payload, and path from the request
    headers = dict(request.headers)
    data = request.get_data(as_text=True)
    path = request.path

    # Store the request details, including the path
    received_requests.append({
        'headers': headers,
        'data': data,
        'path': path
    })

    if (len(received_requests) > 50):
        received_requests.pop(0)

    return f'Request received on /receive/{subpath}', 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
