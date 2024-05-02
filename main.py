from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
import json
from TTS.api import TTS
import wave

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

class UppercaseText(Resource):

    async def get(self):
        """
        This method responds to the GET request for this endpoint and returns the data in uppercase.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to be converted to uppercase
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The text in uppercase
        """
        text = request.args.get('text')

        #return json.dumps({"text": text.upper()})
        tts = await TTS(model_name = 'tts_models/en/ljspeech/tacotron2-DCA')
        audioFile = await tts.tts_to_file(text=text)
        return json.dumps({"wav": audioFile})

api.add_resource(UppercaseText, "/uppercase")

if __name__ == "__main__":
    app.run(debug=True)