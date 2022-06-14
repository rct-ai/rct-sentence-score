# coding=utf8
"""================================
@Author: Mr.Chang
@Date  : 2022/5/10 3:09 下午
==================================="""
import torch.cuda
import waitress
from sentence_transformers.util import cos_sim, dot_score
from encoder import get_model, get_cross_model
from logger import get_logger
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import result_format
from argparse import ArgumentParser

app = Flask(__name__)

LOGGER = get_logger()


@app.after_request
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


@app.route('/ranking/cosin', methods=['POST'])
def cosin_score():
    params = request.get_json()
    LOGGER.info(f"params: {params}")
    texts = params.get('texts', [])
    if not texts:
        return jsonify(result_format([{"query": "", "answer": "", "score": 0.0}]))
    result = []
    texts_embedding = qa_model.encode(texts)
    question_embedding = texts_embedding[0]
    for i in range(1, len(texts_embedding)):
        tensor_score = cos_sim(question_embedding, texts_embedding[i])
        score = tensor_score.squeeze(0).tolist()[0]
        result_ = {"query": texts[0], "answer": texts[i], "score": score}
        result.append(result_)
    LOGGER.info(result)
    return jsonify(result_format(result))


@app.route('/ranking/dot', methods=['POST'])
def dot_scores():
    params = request.get_json()
    LOGGER.info(f"params: {params}")
    texts = params.get('texts', [])
    if not texts:
        return jsonify([{"query": "", "answer": "", "score": 0.0}])

    result = []
    texts_embedding = qa_model.encode(texts)
    question_embedding = texts_embedding[0]
    for i in range(1, len(texts_embedding)):
        tensor_score = dot_score(question_embedding, texts_embedding[i])
        score = tensor_score.squeeze(0).tolist()[0]
        result_ = {"query": texts[0], "answer": texts[i], "score": score}
        result.append(result_)
    LOGGER.info(result)
    return jsonify(result_format(result))

@app.route('/ranking/cross_score', methods=['POST'])
def cross_score():
    params = request.get_json()
    LOGGER.info(f'params: {params}')
    texts = params.get('texts', [])
    if not texts:
        return jsonify([{"query": "", "answer": "", "score": 0.0}])

    result = []
    text1 = texts[0]
    text_pairs = []
    for text in texts[1:]:
        text_pairs.append([text1, text])
    scores = cross_model.predict(text_pairs, apply_softmax=True)
    for i, pairs in enumerate(text_pairs):
        if scores[i][0] > scores[i][1]:
            score = 1-scores[i][0]
        else:
            score = scores[i][1]
        result.append({"query": pairs[0], "answer": pairs[1], "score": float("%.4f" % score)})
        # result.append({"query": pairs[0], "answer": pairs[1], "score": float("%.4f" % scores[i])})
    LOGGER.info(result)
    return jsonify(result_format(result))


CORS(app, supports_credentials=True)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--model_path', type=str, required=True, help='The model path!')
    parser.add_argument('--model_type', type=str, required=True, help='The model type!')
    parser.add_argument('--port', type=int, default=8081, help='server port')
    parser.add_argument('--threads', type=int, default=21, help='The model path!')
    args = parser.parse_args()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    LOGGER.info('device: %s', device)
    if args.model_type == 'cross':
        cross_model = get_cross_model(args.model_path, device=device)
    elif args.model_type == 'qa_match':
        qa_model = get_model(args.model_path, device=device)
    else:
        print('please offer a model type.')

    # app.run('0.0.0.0', port=8074)
    waitress.serve(app, host='0.0.0.0', port=args.port, threads=args.threads, url_scheme='http')