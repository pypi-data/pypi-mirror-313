import datetime
import random
import string
from typing import Literal

from .utils import add_help


@add_help
class Person:
    """用于生成测试数据，所有数据都是随机生成的，仅用于测试目的"""

    def help() -> None: ...

    def __load_area_code_dict(self) -> dict[str, str]:
        """加载区域地址"""
        from .data._internal_utils import data_dict

        return data_dict

    def __birthday(self) -> str:
        """功能：随机生成1930年之后的出生日期"""
        start_date: datetime.datetime = datetime.datetime.strptime(
            "1950-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
        )
        end_date: datetime.datetime = datetime.datetime.now()
        delta: datetime.timedelta = end_date - start_date
        days: int = delta.days
        rand_day = random.randint(0, days)
        offset = datetime.timedelta(days=rand_day)
        birthday: datetime.datetime = start_date + offset
        return birthday.strftime("%Y%m%d")

    def __check(self, id_num) -> str:
        """生成最后一位校验码"""
        i = 0
        count = 0
        weight: list[int] = [
            7,
            9,
            10,
            5,
            8,
            4,
            2,
            1,
            6,
            3,
            7,
            9,
            10,
            5,
            8,
            4,
            2,
        ]  # 权重项
        check_code: dict[str, str] = {
            "0": "1",
            "1": "0",
            "2": "X",
            "3": "9",
            "4": "8",
            "5": "7",
            "6": "6",
            "7": "5",
            "8": "5",
            "9": "3",
            "10": "2",
        }  # 校验码映射
        for i in range(len(id_num)):
            count: int = count + int(id_num[i]) * weight[i]
        return check_code[str(count % 11)]  # 算出校验码

    def __id_sex_age_area(self) -> tuple[str, Literal["女", "男"], int, str]:
        """生成身份证号码、性别、年龄、区域"""
        area_code_and_name: dict[str, str] = self.__load_area_code_dict()
        rand_area_code: str = random.choice(list(area_code_and_name.keys()))
        area_name: str = area_code_and_name[rand_area_code]

        birthday: str = self.__birthday()  # 生成出生日期
        ord_num: int = random.randint(100, 999)  # 生成顺序号
        sex: int = ord_num % 2  # 生成性别号

        check_code: str = self.__check(f"{rand_area_code}{birthday}{ord_num}")

        # 拼装身份证号
        id_card: str = f"{rand_area_code}{birthday}{ord_num}{check_code}"
        gender: Literal["女"] | Literal["男"] = "女" if sex == 0 else "男"

        # 计算年龄
        birth_date: datetime.datetime = datetime.datetime.strptime(birthday, "%Y%m%d")
        current_date: datetime.datetime = datetime.datetime.now()
        age: int = (
            current_date.year
            - birth_date.year
            - (
                (current_date.month, current_date.day)
                < (birth_date.month, birth_date.day)
            )
        )

        return id_card, gender, age, area_name

    def education(self) -> str:
        """学历、教育经历"""
        return random.choice(
            ["小学", "初中", "高中", "中专", "大专", "本科", "硕士", "研究生", "博士"]
        )

    def id_type(self) -> str:
        """证件类型"""
        return random.choice(
            [
                "身份证",
                "居民身份证",
                "士官证",
                "军官证",
                "学生证",
                "驾驶证",
                "驾照",
                "护照",
                "港澳通行证",
                "营业执照",
                "组织机构代码证",
                "台胞证",
                "文职干部证",
                "部队离退休证",
                "香港特区护照/身份证明",
                "澳门特区护照/身份证明",
                "台湾居民来往大陆通行证",
                "境外永久居住证",
                "户口薄",
            ]
        )

    def marital(self) -> str:
        """婚姻状态"""
        return random.choice(["未婚", "已婚", "离婚", "丧偶", "离异"])

    def passport_number(self) -> str:
        """护照号"""
        return "D" + "".join(random.choices("0123456789", k=8))

    def sex(self) -> str:
        """性别"""
        return random.choice(["男", "女"])

    def address(self) -> str:
        """地址"""
        from .data._addr import addr_info_list

        return random.choice(addr_info_list)

    def province(self, long: bool = False) -> str:
        """省份，简写和全称"""
        name = [
            "北京市",
            "天津市",
            "河北省",
            "山西省",
            "内蒙古自治区",
            "辽宁省",
            "吉林省",
            "黑龙江省",
            "上海市",
            "江苏省",
            "浙江省",
            "安徽省",
            "福建省",
            "江西省",
            "山东省",
            "河南省",
            "湖北省",
            "湖南省",
            "广东省",
            "广西壮族自治区",
            "海南省",
            "重庆市",
            "四川省",
            "贵州省",
            "云南省",
            "西藏自治区",
            "陕西省",
            "甘肃省",
            "青海省",
            "宁夏回族自治区",
            "新疆维吾尔自治区",
            "台湾省",
            "香港特别行政区",
            "澳门特别行政区",
        ]
        short_name = [
            "北京",
            "天津",
            "河北",
            "山西",
            "内蒙古",
            "辽宁",
            "吉林",
            "黑龙江",
            "上海",
            "江苏",
            "浙江",
            "安徽",
            "福建",
            "江西",
            "山东",
            "河南",
            "湖北",
            "湖南",
            "广东",
            "广西",
            "海南",
            "重庆",
            "四川",
            "贵州",
            "云南",
            "西藏",
            "陕西",
            "甘肃",
            "青海",
            "宁夏",
            "新疆",
            "台湾",
            "香港",
            "澳门",
        ]
        if long:
            return random.choice(name)
        else:
            return random.choice(short_name)

    def store_name(self) -> str:
        """店铺名称"""
        from .data._shop_sign import shop_sign_list

        return random.choice(shop_sign_list)

    def id_number(self) -> str:
        """身份证号"""
        return self.__id_sex_age_area()[0]

    def mac_address(self, symbol: Literal[":", "-"] = ":") -> str:
        """MAC地址"""
        mac_parts: list[int] = [random.randint(0x00, 0xFF) for _ in range(6)]
        mac_address: str = symbol.join(["%02x" % part for part in mac_parts])
        return mac_address

    def phone_number(self) -> int:
        """手机号"""
        prefix = random.choice(
            [
                "130",
                "131",
                "132",
                "133",
                "134",
                "135",
                "136",
                "137",
                "138",
                "139",
                "150",
                "151",
                "152",
                "153",
                "155",
                "156",
                "157",
                "158",
                "159",
                "176",
                "180",
                "181",
                "182",
                "183",
                "184",
                "185",
                "186",
                "187",
                "188",
                "189",
            ]
        )
        # 随机生成电话号的后缀
        suffix: str = "".join(
            random.choice(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
            for _ in range(8)
        )
        return int(prefix + suffix)

    def landline_number(self) -> str:
        """座机号"""
        prefix: list[str] = [
            "010",
            "022",
            "0311",
            "0315",
            "0335",
            "0310",
            "0319",
            "0312",
            "0313",
            "0314",
            "0317",
            "0316",
            "0318",
            "0351",
            "0352",
            "0353",
            "0355",
            "0356",
            "0349",
            "0354",
            "0359",
            "0350",
            "0357",
            "0358",
            "0471",
            "0472",
            "0473",
            "0476",
            "0475",
            "0477",
            "0470",
            "0478",
            "0474",
            "0482",
            "0479",
            "0483",
            "024",
            "0411",
            "0412",
            "0413",
            "0414",
            "0415",
            "0416",
            "0417",
            "0418",
            "0419",
            "0427",
            "0410",
            "0421",
            "0429",
            "0431",
            "0423",
            "0434",
            "0437",
            "0435",
            "0439",
            "0438",
            "0436",
            "0433",
            "0451",
            "0452",
            "0467",
            "0468",
            "0469",
            "0459",
            "0458",
            "0454",
            "0464",
            "0453",
            "0456",
            "0455",
            "0457",
            "021",
            "025",
            "0510",
            "0516",
            "0519",
            "0512",
            "0513",
            "0518",
            "0517",
            "0515",
            "0514",
            "0511",
            "0523",
            "0527",
            "0571",
            "0574",
            "0577",
            "0573",
            "0572",
            "0575",
            "0579",
            "0570",
            "0580",
            "0576",
            "0578",
            "0551",
            "0553",
            "0552",
            "0554",
            "0555",
            "0561",
            "0562",
            "0556",
            "0559",
            "0550",
            "0558",
            "0557",
            "0564",
            "0566",
            "0563",
            "0591",
            "0592",
            "0594",
            "0598",
            "0595",
            "0596",
            "0599",
            "0597",
            "0593",
            "0791",
            "0798",
            "0799",
            "0792",
            "0790",
            "0701",
            "0797",
            "0796",
            "0795",
            "0794",
            "0793",
            "0531",
            "0532",
            "0533",
            "0632",
            "0546",
            "0535",
            "0536",
            "0537",
            "0538",
            "0631",
            "0633",
            "0539",
            "0534",
            "0635",
            "0543",
            "0530",
            "0371",
            "0378",
            "0379",
            "0375",
            "0372",
            "0392",
            "0373",
            "0391",
            "0393",
            "0374",
            "0395",
            "0398",
            "0377",
            "0370",
            "0376",
            "0394",
            "0396",
            "027",
            "0714",
            "0719",
            "0717",
            "0710",
            "0711",
            "0724",
            "0712",
            "0716",
            "0713",
            "0715",
            "0722",
            "0718",
            "0728",
            "0731",
            "0733",
            "0732",
            "0734",
            "0739",
            "0730",
            "0736",
            "0744",
            "0737",
            "0735",
            "0746",
            "0745",
            "0738",
            "0743",
            "020",
            "0751",
            "0755",
            "0756",
            "0754",
            "0757",
            "0750",
            "0759",
            "0668",
            "0758",
            "0752",
            "0753",
            "0660",
            "0762",
            "0662",
            "0763",
            "0769",
            "0760",
            "0768",
            "0663",
            "0766",
            "0771",
            "0772",
            "0773",
            "0774",
            "0779",
            "0770",
            "0777",
            "0775",
            "0776",
            "0778",
            "0898",
            "023",
            "028",
            "0813",
            "0812",
            "0830",
            "0838",
            "0816",
            "0839",
            "0825",
            "0832",
            "0833",
            "0817",
            "0831",
            "0826",
            "0818",
            "0835",
            "0827",
            "0873",
            "0836",
            "0834",
            "0851",
            "0858",
            "0852",
            "0853",
            "0857",
            "0856",
            "0859",
            "0855",
            "0854",
            "0871",
            "0874",
            "0877",
            "0875",
            "0870",
            "0888",
            "0879",
            "0883",
            "0878",
            "0876",
            "0691",
            "0872",
            "0692",
            "0886",
            "0887",
            "0891",
            "0892",
            "0895",
            "0894",
            "0893",
            "0896",
            "0897",
            "029",
            "0919",
            "0917",
            "0910",
            "0913",
            "0911",
            "0916",
            "0912",
            "0915",
            "0914",
            "0931",
            "0937",
            "0935",
            "0943",
            "0938",
            "0936",
            "0933",
            "0934",
            "0932",
            "0939",
            "0930",
            "0941",
            "0971",
            "0972",
            "0970",
            "0973",
            "0974",
            "0975",
            "0976",
            "0977",
            "0951",
            "0952",
            "0953",
            "0954",
            "0955",
            "0991",
            "0990",
            "0995",
            "0902",
            "0994",
            "0909",
            "0996",
            "0997",
            "0908",
            "0998",
            "0903",
            "0999",
            "0901",
            "0906",
            "0993",
            "0992",
            "8863",
            "8862",
            "88649",
            "8865",
            "8864",
            "8866",
            "88689",
            "8868",
            "8867",
            "00852",
            "00853",
        ]
        rand_prefix: str = random.choice(prefix)
        return f"{rand_prefix}-{random.choice(string.digits[1:])}{''.join(random.choices(string.digits,k=7))}"

    def latitude(self) -> float:
        """纬度 N（北） 表示北半球。S（南） 表示南半球。"""
        return f"{round(random.uniform(-90, 90), 6)}°{random.choice(['N','S'])}"

    def longitude(self) -> float:
        """经度 E（东） 表示东半球。W（西） 表示西半球。"""
        return f"{round(random.uniform(-180, 180), 6)}°{random.choice(['E','W'])}"

    def occupation(self) -> str:
        """职业"""
        return random.choice(
            [
                "教师",
                "工人",
                "记者",
                "演员",
                "作曲家",
                "架构师",
                "营养师",
                "鼓手",
                "厨师",
                "医生",
                "护士",
                "司机",
                "军人",
                "律师",
                "商人",
                "会计",
                "店员",
                "出纳员",
                "作家",
                "导游",
                "警察",
                "歌手",
                "画家",
                "裁缝",
                "翻译官",
                "法官",
                "保安",
                "花匠",
                "服务员",
                "清洁工",
                "建筑师",
                "理发师",
                "采购员",
                "消防员",
                "机修工",
                "推销员",
                "魔术师",
                "模特",
                "邮递员",
                "售货员",
                "救生员",
                "运动员",
                "工程师",
                "飞行员",
                "管理员",
                "机械师",
                "经纪人",
                "歌唱家",
                "审计员",
                "漫画家",
                "园艺师",
                "科学家",
                "主持人",
                "调酒师",
                "化妆师",
                "艺术家",
                "糕点师",
                "甜品师",
                "外交官",
                "舞蹈家",
                "箭术",
                "溜冰",
                "弹钢琴",
                "古筝手",
                "钢琴家",
                "设计师",
                "CEO",
                "机 长",
                "记者",
                "赛车手",
                "教练",
                "兽医",
                "特警",
                "按摩",
            ]
        )

    def school(self) -> str:
        """学校名称"""
        return random.choice(
            [
                "麻省理工学院",
                "牛津大学",
                "斯坦福大学",
                "剑桥大学",
                "哈佛大学",
                "加州理工学院",
                "帝国理工学院",
                "苏黎世联邦理工大学",
                "伦敦大学学院",
                "芝加哥大学",
            ]
        )

    def full_name(self) -> str:
        """姓名"""
        return f"{self.last_name()}{self.first_name()}"

    def first_name(self) -> str:
        """名，只生成随机名，不包含姓氏"""
        return random.choice(
            [
                "伟",
                "芳",
                "娜",
                "秀英",
                "敏",
                "静",
                "丽",
                "强",
                "磊",
                "军",
                "洋",
                "勇",
                "艳",
                "杰",
                "娟",
                "博",
                "文",
                "涛",
                "慧",
                "明",
                "建国",
                "丽丽",
                "媛",
                "子涵",
                "子轩",
                "浩然",
                "昊然",
                "浩",
                "振华",
            ]
        )

    def last_name(self) -> str:
        """姓，生成随机的姓氏"""
        return random.choice(
            [
                "赵",
                "钱",
                "孙",
                "李",
                "周",
                "吴",
                "郑",
                "王",
                "冯",
                "陈",
                "褚",
                "卫",
                "蒋",
                "沈",
                "韩",
                "杨",
                "朱",
                "秦",
                "尤",
                "许",
                "何",
                "吕",
                "施",
                "张",
                "孔",
                "曹",
                "严",
                "华",
                "金",
                "魏",
                "陶",
                "姜",
                "戚",
                "谢",
                "邹",
                "喻",
                "柏",
                "水",
                "窦",
                "章",
                "云",
                "苏",
                "潘",
                "葛",
                "奚",
                "范",
                "彭",
                "郎",
                "鲁",
                "韦",
                "昌",
                "马",
                "苗",
                "凤",
                "花",
                "方",
                "俞",
                "任",
                "袁",
                "柳",
                "酆",
                "鲍",
                "史",
                "唐",
                "费",
                "廉",
                "岑",
                "薛",
                "雷",
                "贺",
                "倪",
                "汤",
                "滕",
                "殷",
                "罗",
                "毕",
                "郝",
                "邬",
                "安",
                "常",
                "乐",
                "于",
                "时",
                "傅",
                "皮",
                "卞",
                "齐",
                "康",
                "伍",
                "余",
                "元",
                "卜",
                "顾",
                "孟",
                "平",
                "黄",
                "郭",
                "轩辕",
                "公孙",
                "慕容",
                "司马",
            ]
        )

    def religion(self) -> str:
        """宗教信仰"""
        return random.choice(
            [
                "道教",
                "佛教",
                "伊斯兰教",
                "基督教",
                "印度教",
                "犹太教",
                "婆罗门教",
                "耆那教",
            ]
        )

    def age(self, min: int = 16, max: int = 101) -> int:
        """年龄"""
        return random.randint(min, max)

    def ethnicity(self, country: str = "zh") -> str:
        """民族、种族"""
        chinese_ethnicity: list[str] = [
            "汉族",
            "蒙古族",
            "回族",
            "藏族",
            "维吾尔族",
            "苗族",
            "彝族",
            "壮族",
            "布依族",
            "朝鲜族",
            "满族",
            "侗族",
            "瑶族",
            "白族",
            "土家族",
            "哈尼族",
            "哈萨克族",
            "傣族",
            "黎族",
            "傈僳族",
            "佤族",
            "畲族",
            "高山族",
            "拉祜族",
            "水族",
            "东乡族",
            "纳西族",
            "景颇族",
            "柯尔克孜族",
            "土族",
            "达斡尔族",
            "仫佬族",
            "羌族",
            "布朗族",
            "撒拉族",
            "毛南族",
            "仡佬族",
            "锡伯族",
            "阿昌族",
            "普米族",
            "塔吉克族",
            "怒族",
            "乌孜别克族",
            "俄罗斯族",
            "鄂温克族",
            "崩龙族",
            "保安族",
            "裕固族",
            "京族",
            "塔塔尔族",
            "独龙族",
            "鄂伦春族",
            "赫哲族",
            "门巴族",
            "珞巴族",
            "基诺族",
        ]
        match country:
            case "zh":
                return random.choice(chinese_ethnicity)
            case _:
                return random.choice(chinese_ethnicity)

    def residence(self) -> str:
        """小区、住宅"""
        from .data._housing import housing

        return random.choice(housing)

    def country(self, en: bool = False) -> str:
        """国家名"""
        from .data._country import en_country, zh_country

        if en:
            return random.choice(en_country)
        return random.choice(zh_country)

    def industry(self) -> str:
        """行业"""
        return random.choice(
            ["金融", "教育", "通信", "信息安全", "物流", "能源", "医疗", "军工"]
        )

    def license_plate(self, battery: bool = False, symbol: str = "· ") -> str:
        """车牌号"""
        provinces_abbreviations: list[str] = [
            "京",
            "津",
            "沪",
            "渝",
            "冀",
            "晋",
            "蒙",
            "辽",
            "吉",
            "黑",
            "苏",
            "浙",
            "皖",
            "闽",
            "赣",
            "鲁",
            "豫",
            "鄂",
            "湘",
            "粤",
            "桂",
            "琼",
            "川",
            "黔",
            "滇",
            "藏",
            "陕",
            "甘",
            "青",
            "宁",
            "新",
            "港",
            "澳",
            "台",
        ]
        ascii_uppercase = "ABCDEFGHJKLMNPQRSTUVWXYZ"  # I、O
        province_letter: str = random.choice(provinces_abbreviations)
        letter_part: str = random.choice(string.ascii_uppercase)
        license_plate: str = "".join(
            random.choices((string.digits + ascii_uppercase), k=5)
        )

        if battery:
            license_plate: str = "".join(random.choices((string.digits), k=5))
            battery_symbol: str = random.choice(
                "DF"
            )  # D代表纯电动新能源汽车，F代表非纯电动新能源汽车。
            return (
                f"{province_letter}{letter_part}{symbol}{battery_symbol}{license_plate}"
            )

        return f"{province_letter}{letter_part}{symbol}{license_plate }"

    def email(self, prefix=None):
        """邮箱"""
        email_suffix = [
            "@gmail.com",
            "@qq.com",
            "@163.com",
            "@sina.com",
            "@163.com",
            "@outlook.com",
            "@hotmail.com",
            "@yahoo.com",
            "@yahoo.co.uk",
            "@yahoo.ca",
            "@yahoo.fr",
            "@yahoo.de",
            "@yahoo.it",
            "@yahoo.es",
        ]
        if prefix is None:
            prefix = "".join(random.choices(string.ascii_lowercase, k=5))
        return f"{prefix}{random.choice(email_suffix)}"

    def profile(self, zh: bool = False) -> dict:
        """包含随机生成的个人信息的字典，例如姓名、性别、年龄、职业等。"""

        _id_card, _sex, _age, area_code_name = self.__id_sex_age_area()

        labels = {
            "name": "姓名" if zh else "Name",
            "sex": "性别" if zh else "Sex",
            "age": "年龄" if zh else "Age",
            "occupation": "职业" if zh else "Occupation",
            "ethnicity": "民族" if zh else "Ethnicity",
            "school": "学校" if zh else "School",
            "religion": "宗教信仰" if zh else "Religion",
            "phone_number": "手机号" if zh else "Phone Number",
            "landline_number": "座机号" if zh else "Landline Number",
            "address": "地址" if zh else "Address",
            "residence": "居住地" if zh else "Residence",
            "id_card": "身份证" if zh else "ID Card",
            "mac": "MAC",
            "passport_number": "护照号" if zh else "Passport Number",
            "latitude": "经度" if zh else "Longitude",
            "longitude": "纬度" if zh else "Latitude",
            "country": "国家" if zh else "Country",
            "marital": "婚姻状况" if zh else "Marital",
            "email": "邮箱" if zh else "Email",
            "id_type": "证件类型" if zh else "ID Type",
            "education": "学历" if zh else "Education",
            "license_plate": "车牌号" if zh else "License Plate",
        }

        return {
            labels["name"]: self.full_name(),
            labels["sex"]: _sex,
            labels["age"]: _age,
            labels["occupation"]: self.occupation(),
            labels["ethnicity"]: self.ethnicity(),
            labels["school"]: self.school(),
            labels["religion"]: self.religion(),
            labels["phone_number"]: self.phone_number(),
            labels["landline_number"]: self.landline_number(),
            labels["address"]: f"{area_code_name}{self.residence()}",
            labels["residence"]: self.residence(),
            labels["id_card"]: _id_card,
            labels["mac"]: self.mac_address(),
            labels["passport_number"]: self.passport_number(),
            labels["latitude"]: self.latitude(),
            labels["longitude"]: self.longitude(),
            labels["country"]: self.country(),
            labels["marital"]: self.marital(),
            labels["email"]: self.email(),
            labels["id_type"]: self.id_type(),
            labels["education"]: self.education(),
            labels["license_plate"]: self.license_plate(),
        }
