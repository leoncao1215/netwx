## GET /api/wqs

参数(query params)

| 参数      | 取值           |
| --------- | -------------- |
| dismissed | `true | false` |
| category  | `str`          |

示例:

- `GET /api/wqs?category=数学&dismissed=true`

- `GET /api/wqs?category=数学`

- `GET /api/wqs?dismissed=true`

- `GET /api/wqs`

返回：

```json
{
questions:  //字典的列表
[
{
_id:
description：如果一开始没填就是""字符串
category
dismissed
answer
date
url: 如果不是图片就是null
}
]
}
```

## POST /api/wqs

1. 上传错题

参数(json)：

description

answer

dismissed

category

date

返回：

_id：上传的错题id

## PUT /api/wqs

1. 更新错题

参数：

description

answer

dismissed

category

date

_id：更新的错题id

返回：

matched_count: 匹配uid和_id的错题条目

modified_count: 修改的错题条目 （这两个可以不要）

## DELETE /api/wqs

1. 删除错题

url: `DELETE /wqs/<string:wq_id>`

返回：{'status': 'Success'} 或 404



## GET /api/wqs/categories

获取所有类别

返回：

```json
[
    "数学",
    "皮",
    "2本语",
    "鹅语",
    "文学"
]
```





## POST /api/wqs_file

上传图片文件（支持的拓展格式：pdf、png、jpg、jpeg）

参数 (form-data)：

file: 图片文件

answer: 

dismissed: True/False

catogry:

返回：

上传成功：

_id: 上传的错题id

上传失败：

status: Failed

message:file error



## PUT /api/wqs_file

更新图片文件（支持的拓展格式：pdf、png、jpg、jpeg）

参数 (form-data)：

file: 图片文件

answer: 

dismissed: True/False

catogry:

 **_id: 错题id**

返回：

更新成功：

_id: 更新的错题id

更新失败：

status: Failed

message: _id not found





## POST /api/quiz

上传测试结果

url：`POST /api/quiz`

参数:json
```json
{
    "is_corrected":1,  //是否被批改，1表示批改，0未批改
    "question_arr":[],  //问题的_id数组
    "answer_arr":["a","b","c"],  //问题的用户回答的数组
    "correct_arr":[1,0,0],    //用户回答是否正确的数组，1正确，0不正确
    "date":1576570746,   //上传的时间，timestamp类型
    "time_used":300,    //用户完成测试用时 int类型
    "category": "数学"
}
```

返回：

更新成功：

_id: 上传的测试id



## GET /api/quiz

#### 获取所有测试

url: `GET /api/quiz`

参数：没有

返回：json

```json
{
    "quizzes": [ //这是个数组
        {
            "_id": "5df8f85c335a9071b00f2083",//测试的_id
            "correct_num": 1,//测试回答正确的个数
            "date": 1576570746,//timestamp类型
            "question_list": [
                {
                    "answer": "a",//用户的答案
                    "description": "",//错题的描述
                    "is_correct": true,//回答是否正确
                    "qid": "5df79846a537b8ec7b542a02"//错题的_id
                },
                {
                    "answer": "b",
                    "description": "",
                    "is_correct": false,
                    "qid": "5df79122a537b8ec7b542a01"
                },
                {
                    "answer": "c",
                    "description": "des",
                    "is_correct": false,
                    "qid": "5df8c017ffa085968a71bb6b"
                }
            ],
            "scored": true, //是否被批改
            "time_used": 300, //用户完成测试的用时（秒）
            "total_num": 3, //测试的错题的个数
            "category": "数学"
        }
    ]
}
```



#### 根据ID获取测试

url: 	`GET /api/quiz/<string:id>`

如	`GET /api/quiz/5df8f85c335a9071b00f2083`

参数: 无

返回：json (即上一条列表中的一条）

```json
{
    "_id": "5df8f85c335a9071b00f2083",
    "correct_num": 1,
    "date": 1576570746,
    "question_list": [
        {
            "answer": "a",
            "description": "",
            "is_correct": true,
            "qid": "5df79846a537b8ec7b542a02",
            "scored": true
        },
        {
            "answer": "b",
            "description": "",
            "is_correct": false,
            "qid": "5df79122a537b8ec7b542a01",
            "scored": true
        },
        {
            "answer": "c",
            "description": "des",
            "is_correct": false,
            "qid": "5df8c017ffa085968a71bb6b",
            "scored": true
        }
    ],
    "scored": true,
    "time_used": 300,
    "total_num": 3,
    "category": "数学"
}
```





## GET /api/quiz/generate/.../...

1. 生成测试试卷 GET

url:``` GET /api/quiz/generate/<int:question_num>/<string:category>```

参数:

question_num：测试的错题个数

category：错题类型

返回：
```json
{
    "questions": [
        {
            "_id": "5dfb8888a595b9affd35d6f3",
            "answer": "answer123",
            "category": "文学",
            "date": 1576570617,
            "description": "",
            "dismissed": false,
            "url": "https://i.loli.net/2019/12/19/mBGtQJCELXqzWae.jpg"  //如果不是图片，url是null
        },
        {
            "_id": "5dfb836ea595b9affd35d6ef",
            "answer": "answer123",
            "category": "文学",
            "date": 1576570617,
            "description": "",
            "dismissed": false,
            "url": "https://i.loli.net/2019/12/19/Z8WCbJOQh4KpTqF.jpg"
        }
    ]
}
```