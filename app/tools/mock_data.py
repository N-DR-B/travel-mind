# -*- coding: utf-8 -*-
"""模拟数据 - 用于开发调试和 demo 演示"""

MOCK_FLIGHTS = {
    "东京": [
        {"airline": "中国国际航空", "flight": "CA925", "price": 2800, "duration": "3h20m", "departure": "08:30", "arrival": "12:50"},
        {"airline": "东方航空", "flight": "MU523", "price": 2500, "duration": "3h15m", "departure": "14:20", "arrival": "18:35"},
        {"airline": "全日空", "flight": "NH920", "price": 3200, "duration": "3h10m", "departure": "09:00", "arrival": "13:10"},
    ],
    "大阪": [
        {"airline": "南方航空", "flight": "CZ389", "price": 2400, "duration": "3h40m", "departure": "07:50", "arrival": "12:30"},
        {"airline": "东方航空", "flight": "MU729", "price": 2300, "duration": "3h35m", "departure": "16:00", "arrival": "20:40"},
    ],
    "首尔": [
        {"airline": "大韩航空", "flight": "KE868", "price": 1500, "duration": "2h10m", "departure": "09:30", "arrival": "11:40"},
        {"airline": "东方航空", "flight": "MU5033", "price": 1200, "duration": "2h05m", "departure": "13:00", "arrival": "15:05"},
    ],
    "曼谷": [
        {"airline": "泰国国际航空", "flight": "TG615", "price": 1800, "duration": "4h30m", "departure": "10:00", "arrival": "14:30"},
        {"airline": "南方航空", "flight": "CZ303", "price": 1600, "duration": "4h15m", "departure": "22:00", "arrival": "02:15"},
    ],
    "巴黎": [
        {"airline": "法国航空", "flight": "AF111", "price": 5200, "duration": "11h30m", "departure": "23:50", "arrival": "05:20+1"},
        {"airline": "中国国际航空", "flight": "CA933", "price": 4800, "duration": "10h50m", "departure": "01:30", "arrival": "06:20"},
    ],
    "新加坡": [
        {"airline": "新加坡航空", "flight": "SQ801", "price": 2800, "duration": "5h40m", "departure": "08:20", "arrival": "14:00"},
        {"airline": "东方航空", "flight": "MU545", "price": 2200, "duration": "6h00m", "departure": "09:50", "arrival": "15:50"},
    ],
}

MOCK_HOTELS = {
    "东京": [
        {"name": "新宿华盛顿酒店", "rating": 4.2, "price_per_night": 600, "location": "新宿区", "stars": 3},
        {"name": "东京湾希尔顿", "rating": 4.6, "price_per_night": 1200, "location": "港区", "stars": 5},
        {"name": "浅草微笑酒店", "rating": 4.0, "price_per_night": 400, "location": "浅草", "stars": 3},
    ],
    "大阪": [
        {"name": "大阪难波假日酒店", "rating": 4.3, "price_per_night": 550, "location": "难波", "stars": 3},
        {"name": "大阪瑞吉酒店", "rating": 4.8, "price_per_night": 1500, "location": "中央区", "stars": 5},
    ],
    "首尔": [
        {"name": "明洞九树酒店", "rating": 4.4, "price_per_night": 450, "location": "明洞", "stars": 3},
        {"name": "首尔四季酒店", "rating": 4.7, "price_per_night": 1300, "location": "钟路区", "stars": 5},
    ],
    "曼谷": [
        {"name": "暹罗凯宾斯基", "rating": 4.7, "price_per_night": 800, "location": "暹罗区", "stars": 5},
        {"name": "曼谷城市酒店", "rating": 4.1, "price_per_night": 300, "location": "拉差贴威", "stars": 4},
    ],
    "巴黎": [
        {"name": "巴黎歌剧院酒店", "rating": 4.3, "price_per_night": 1100, "location": "歌剧院区", "stars": 4},
        {"name": "巴黎半岛酒店", "rating": 4.8, "price_per_night": 3500, "location": "十六区", "stars": 5},
    ],
    "新加坡": [
        {"name": "滨海湾金沙酒店", "rating": 4.7, "price_per_night": 2500, "location": "滨海湾", "stars": 5},
        {"name": "新加坡武吉士酒店", "rating": 4.2, "price_per_night": 600, "location": "武吉士", "stars": 4},
    ],
}

MOCK_ATTRACTIONS = {
    "东京": ["浅草寺·仲见世通", "涩谷十字路口", "东京塔·六本木", "秋叶原电器街", "银座购物", "上野公园", "明治神宫", "台场海滨公园", "迪士尼乐园"],
    "大阪": ["大阪城公园", "道顿堀美食街", "环球影城", "心斋桥购物", "通天阁", "海游馆", "梅田蓝天大厦"],
    "首尔": ["景福宫", "明洞购物街", "南山N首尔塔", "弘大创意街", "北村韩屋村", "梨泰院", "东大门DDP"],
    "曼谷": ["大皇宫·玉佛寺", "卧佛寺", "郑王庙", "乍都乍周末市场", "暹罗百丽宫", "考山路", "水上市场"],
    "巴黎": ["埃菲尔铁塔", "卢浮宫", "凯旋门·香榭丽舍", "巴黎圣母院", "蒙马特高地", "凡尔赛宫", "塞纳河游船"],
    "新加坡": ["滨海湾花园", "圣淘沙岛", "鱼尾狮公园", "环球影城", "牛车水", "小印度", "克拉码头"],
}

MOCK_VISA_INFO = {
    "日本": {"visa_required": True, "type": "旅游签证（单次/多次）", "processing_days": "5-7个工作日", "fee": "约200元",
             "materials": ["护照原件（有效期6个月以上）", "签证申请表", "2寸白底照片", "在职证明", "银行存款证明（10万+）", "机票酒店预订单"],
             "notes": "上海/北京/广州等领区可办理三年/五年多次签证"},
    "韩国": {"visa_required": True, "type": "旅游签证（C-3-9）", "processing_days": "5-7个工作日", "fee": "约280元",
             "materials": ["护照原件", "签证申请表", "2寸白底照片", "在职证明", "近6个月银行流水"],
             "notes": "济州岛免签停留30天"},
    "泰国": {"visa_required": False, "type": "免签（30天）", "processing_days": "无需办理", "fee": "免费",
             "materials": ["护照原件（有效期6个月以上）", "往返机票", "酒店预订单（抽查）"],
             "notes": "2024年起对中国公民永久免签，单次停留不超过30天"},
    "法国": {"visa_required": True, "type": "申根旅游签证（短期C类）", "processing_days": "10-15个工作日", "fee": "约600元",
             "materials": ["护照原件（有效期3个月以上）", "申根签证申请表", "2寸白底照片", "在职/在校证明", "近3-6个月银行流水", "机票酒店预订单", "行程计划", "医疗保险（覆盖申根区）"],
             "notes": "需录指纹，建议提前1-2个月申请"},
    "新加坡": {"visa_required": True, "type": "旅游签证（电子签）", "processing_days": "3-5个工作日", "fee": "约300元",
               "materials": ["护照扫描件", "Form 14A申请表", "2寸白底电子照片", "在职证明", "银行流水", "机票酒店预订单"],
               "notes": "电子签证，出签后打印随身携带"},
}

MOCK_CITY_INFO = {
    "东京": {"country": "日本", "language": "日语", "currency": "日元 (JPY)", "timezone": "UTC+9",
             "best_season": "3-5月（樱花季）/ 9-11月（红叶季）",
             "description": "东京是日本的首都，融合了超现代与传统文化的魅力。从涩谷的霓虹灯到浅草的古老寺庙，每一处都充满惊喜。",
             "cuisine": ["寿司", "拉面", "天妇罗", "和牛", "抹茶甜品"],
             "tips": ["地铁+JR覆盖全市，推荐Suica卡", "很多餐厅有中文菜单", "消费税8-10%，含在标价内"]},
    "大阪": {"country": "日本", "language": "日语", "currency": "日元 (JPY)", "timezone": "UTC+9",
             "best_season": "3-5月 / 9-11月",
             "description": "大阪被称为\"日本的厨房\"，是美食爱好者的天堂。道顿堀的霓虹灯和章鱼烧是大阪的灵魂。",
             "cuisine": ["章鱼烧", "大阪烧", "串炸", "河豚料理"],
             "tips": ["大阪周游卡可免费进入40+景点", "道顿堀是美食集中地", "心斋桥购物到晚上9点"]},
    "首尔": {"country": "韩国", "language": "韩语", "currency": "韩元 (KRW)", "timezone": "UTC+9",
             "best_season": "3-5月 / 9-11月",
             "description": "首尔是一座充满活力的城市，古老的宫殿与摩天大楼并存，K-pop文化与传统韩屋和谐共处。",
             "cuisine": ["韩式烤肉", "参鸡汤", "拌饭", "辣炒年糕"],
             "tips": ["T-money卡通用所有公共交通", "明洞换钱汇率较好", "很多店铺支持支付宝"]},
    "曼谷": {"country": "泰国", "language": "泰语", "currency": "泰铢 (THB)", "timezone": "UTC+7",
             "best_season": "11-2月（凉季）",
             "description": "曼谷是东南亚最受欢迎的旅游目的地之一，金碧辉煌的寺庙、热闹的水上市场和令人垂涎的街头美食。",
             "cuisine": ["泰式炒河粉", "冬阴功汤", "青木瓜沙拉", "芒果糯米饭"],
             "tips": ["突突车记得讲价", "寺庙需穿过膝衣物", "街边小吃干净又便宜"]},
    "巴黎": {"country": "法国", "language": "法语", "currency": "欧元 (EUR)", "timezone": "UTC+1",
             "best_season": "4-6月 / 9-10月",
             "description": "巴黎是世界浪漫之都，从埃菲尔铁塔到卢浮宫，从塞纳河畔到蒙马特高地，处处是艺术与历史的气息。",
             "cuisine": ["可颂面包", "法式焗蜗牛", "鹅肝", "马卡龙"],
             "tips": ["地铁系统发达，推荐10次票", "餐厅一般已含服务费", "博物馆通票很划算"]},
    "新加坡": {"country": "新加坡", "language": "英语/中文/马来语", "currency": "新加坡元 (SGD)", "timezone": "UTC+8",
               "best_season": "全年（3-8月较干燥）",
               "description": "新加坡是花园城市国家，融合了中华、马来和印度文化。滨海湾的夜景和多元美食让人流连忘返。",
               "cuisine": ["海南鸡饭", "辣椒螃蟹", "肉骨茶", "叻沙"],
               "tips": ["地铁+公交覆盖全岛", "室内冷气很足建议带外套", "口香糖禁止进口"]},
}

MOCK_PACKING_LISTS = {
    "日本": {
        "essentials": ["护照/签证", "机票行程单", "酒店预订单", "日元现金", "信用卡/Visa卡", "IC卡（Suica/Pasmo）"],
        "clothing": ["符合季节的衣物", "舒适步行鞋", "外套（春秋）", "防晒帽/伞"],
        "electronics": ["转换插头（两脚扁插）", "充电宝", "随身WiFi/eSIM", "相机"],
        "health": ["常用药品", "创可贴", "口罩"],
        "other": ["小垃圾袋（日本垃圾桶少）", "零钱包", "购物袋"]
    },
    "泰国": {
        "essentials": ["护照/签证", "机票行程单", "酒店预订单", "泰铢现金", "信用卡"],
        "clothing": ["夏季衣物（速干优先）", "防晒衣", "泳衣", "拖鞋", "薄外套（商场冷气足）"],
        "electronics": ["充电宝", "手机防水袋", "相机"],
        "health": ["驱蚊液", "防晒霜（高倍数）", "肠胃药", "创可贴"],
        "other": ["湿纸巾", "按摩小费零钱", "购物袋"]
    },
}


def get_destination_info(city: str) -> dict:
    return MOCK_CITY_INFO.get(city, MOCK_CITY_INFO.get("东京", {}))


def get_exchange_rate(base_currency: str = "CNY") -> dict:
    rates = {
        "CNY": {"JPY": 21.5, "KRW": 185.0, "THB": 5.1, "EUR": 0.13, "SGD": 0.19, "USD": 0.14},
        "USD": {"JPY": 150.0, "KRW": 1320.0, "THB": 36.0, "EUR": 0.92, "SGD": 1.35, "CNY": 7.25},
    }
    return {"base": base_currency, "rates": rates.get(base_currency, rates["CNY"])}
