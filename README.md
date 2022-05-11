# rct-sentence-score

用于句子打分相关

# 使用方法

1、将模型copy到models下。\

2、修改docker-compose中的模型地址名称。\

3、确保端口没有被占用，启动docker-compose.yml

4、调用接口

curl --location --request POST 'http://192.168.0.181:8900/ranking/cosin' \
--header 'User-Agent: Apipost client Runtime/+https://www.apipost.cn/' \
--header 'Content-Type: application/json' \
--data '{
    "texts": ["请问你在做什么？", "今天的月色真美", "我在打游戏呢", "哈哈哈哈"]
}'

5、返回内容

{
	"result": [
		{
			"answer": "我在打游戏呢",
			"query": "请问你在做什么？",
			"score": 0.5103771686553955
		},
		{
			"answer": "哈哈哈哈",
			"query": "请问你在做什么？",
			"score": 0.40847328305244446
		},
		{
			"answer": "今天的月色真美",
			"query": "请问你在做什么？",
			"score": 0.2795659303665161
		}
	]
}