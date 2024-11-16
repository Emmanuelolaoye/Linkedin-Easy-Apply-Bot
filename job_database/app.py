from flask import Flask, request, jsonify
import send

app = Flask(__name__)


@app.route('/job_database', methods=['POST'])
def receive_links():
    try:
        # Get the links from the incoming JSON data
        data = request.get_json()
        links = data.get("links", [])

        # Print or log received links for verification
        print("Received links:", links)

        link_publisher.publish_link(links)

        # Here, you can add processing code, such as storing links in a database, queue, etc.


        return jsonify({"status": "received", "links_count": len(links)}), 200

    except Exception as e:
        # Log error and return error response
        print(f"Error processing request: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    # Run the receive_links microservice on port 5000
    app.run(host='0.0.0.0', port=5000)