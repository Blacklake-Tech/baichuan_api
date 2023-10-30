from enum import IntEnum

from pydantic import BaseModel

# 成功	成功	0	success	请求成功并获得预期的结果
# 请求错误	失败	1	system error	请求失败
# 请求错误	参数非法	10000	Invalid parameters, please check	请求中的参数不合法，请仔细检查
# 请求错误	私钥缺失	10100	Missing apikey	请求缺少必要的私钥参数
# 请求错误	私钥非法	10101	Invalid apikey	提供的私钥无效，无法解码
# 请求错误	私钥过期	10102	apikey has expired	提供的私钥已过期，如果非永久有效，需重新获取
# 请求错误	时间戳无效	10103	Invalid Timestamp parameter in request header	错误的时间戳格式
# 请求错误	时间戳过期	10104	Expire Timestamp parameter in request header	过期的时间戳
# 请求错误	无效签名	10105	Invalid Signature parameter in request header	请求头中的签名无效
# 请求错误	无效加密算法	10106	Invalid encryption algorithm in request header, not supported by server	请求头中的加密算法不被支持
# 账号错误	账号未知	10200	Account not found	请求的账号不存在
# 账号错误	账号锁定	10201	Account is locked, please contact the support staff	请求的账号已锁定，请联系支持人员
# 账号错误	账号临时锁定	10202	Account is temporarily locked, please try again later	请求的账号临时锁定，请稍后再试
# 账号错误	账号请求频繁	10203	Request too frequent, please try again later	请求过于频繁，已触发频率控制。当前单 apikey 限制 10rpm
# 账号错误	账号余额不足	10300	Insufficient account balance, please recharge	账号余额不足，请进行充值
# 账号错误	账户未认证	10301	Account is not verified, please complete the verification first	账号未认证，请先认证通过
# 安全错误	prompt 不安全	10400	Topic violates security policy	返回的 prompt 内容不符合安全策略
# 安全错误	answer 不安全	10401	Topic violates security policy	返回的 answer 内容不符合安全策略
# 服务错误	服务内部错误	10500	Internal error	服务内部发生错误，请稍后再试


# code as enum
class RespCode(IntEnum):
    Success = 0
    SystemError = 1

    InvalidParameters = 10000
    MissingApikey = 10100
    InvalidApikey = 10101
    ApikeyExpired = 10102
    InvalidTimestamp = 10103
    ExpireTimestamp = 10104
    InvalidSignature = 10105
    InvalidEncryptionAlgorithm = 10106

    AccountNotFound = 10200
    AccountLocked = 10201
    AccountTempLocked = 10202
    AccountRequestTooFrequent = 10203

    AccountBalanceInsufficient = 10300
    AccountNotVerified = 10301

    PromptNotSafe = 10400
    AnswerNotSafe = 10401

    InternalError = 10500

    def get_message(self):
        """
        get the human readable message for each value
        """
        return {
            RespCode.Success: "成功",
            RespCode.SystemError: "失败",
            RespCode.InvalidParameters: "参数非法",
            RespCode.MissingApikey: "私钥缺失",
            RespCode.InvalidApikey: "私钥非法",
            RespCode.ApikeyExpired: "私钥过期",
            RespCode.InvalidTimestamp: "时间戳无效",
            RespCode.ExpireTimestamp: "时间戳过期",
            RespCode.InvalidSignature: "无效签名",
            RespCode.InvalidEncryptionAlgorithm: "无效加密算法",
            RespCode.AccountNotFound: "账号未知",
            RespCode.AccountLocked: "账号锁定",
            RespCode.AccountTempLocked: "账号临时锁定",
            RespCode.AccountRequestTooFrequent: "账号请求频繁",
            RespCode.AccountBalanceInsufficient: "账号余额不足",
            RespCode.AccountNotVerified: "账户未认证",
            RespCode.PromptNotSafe: "prompt 不安全",
            RespCode.AnswerNotSafe: "answer 不安全",
            RespCode.InternalError: "服务内部错误",
        }.get(self, "未知错误")


class ChatMessage(BaseModel):
    role: str
    content: str
    finish_reason: str | None = None


class BaichuanData(BaseModel):
    messages: list[ChatMessage]


class UsageInfo(BaseModel):
    prompt_tokens: int
    answer_tokens: int
    total_tokens: int


class BaichuanResp(BaseModel):
    code: RespCode
    msg: str
    data: BaichuanData | None = None
    usage: UsageInfo | None = None


class BaichuanReq(BaseModel):
    model: str
    messages: list[ChatMessage]
    parameters: dict | None = None
