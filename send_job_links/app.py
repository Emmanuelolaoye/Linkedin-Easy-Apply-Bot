from flask import Flask, request, jsonify
import aiohttp
import asyncio

app = Flask(__name__)


# Define the async function to send links to the microservice
async def send_links_to_microservice(links):
    # Define your microservice URL here
    url = 'http://localhost:5000/job_database'  # Replace with the actual microservice URL
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={"links": links}) as response:
                if response.status == 200:
                    print("Links successfully sent to the microservice.")
                    return {"status": "success"}
                else:
                    print(f"Failed to send links. Status code: {response.status}")
                    return {"status": "failed", "code": response.status}
        except Exception as e:
            print(f"Error sending links to microservice: {e}")
            return {"status": "error", "message": str(e)}


async def send_cookies(cookies):

    url = 'http://localhost:5000/job_database'

    async with aiohttp.ClientSession() as session:

        try:

            async with session.post(url, json = {'cookies': cookies}) as response:

                if response.status == 200:
                    print('cookies sent to microservice.')
                    return {"status": "success"}

                else:
                    print(f'failed to send cookies to microservice status code: {response.status}')
                    return {"status": "failed", "code": response.status}

        except Exception as e:
            print(f"Error sending links to microservice: {e}")
            return {"status": "error", "message": str(e)}





# Flask route to handle incoming links and call the async function
@app.route('/send_job_links', methods=['POST'])
def send_out_links():
    data = request.get_json()
    links = data.get("links", [])

    # Run the async function in an event loop
    result = asyncio.run(send_links_to_microservice(links))

    return jsonify(result)


if __name__ == '__main__':
    app.run()