import base64

from volcengine.visual.VisualService import VisualService

from config import configs


visual_service = VisualService()
visual_service.set_ak(configs.VOLC_ACCESS_KEY)
visual_service.set_sk(configs.VOLC_SECRET_KEY)
action = "MultiLanguageOCR"
version = "2022-08-31"
visual_service.set_api_info(action, version)


def handle(image_url: str):
    if not image_url:
        raise RuntimeError("image_url is empty")
    prefix = "data:image/png;base64"
    if image_url.startswith(prefix):
        image_url = image_url[len(prefix):]
        return visual_service.ocr_api(action, {"image_base64": image_url})
    return visual_service.ocr_api(action, {"image_url": image_url})


if __name__ == "__main__":
    # 读取并编码图片
    # with open("test.png", "rb") as image_file:
    #     image_data = image_file.read()
    #     image_base64 = base64.b64encode(image_data).decode('utf-8')
    # print(handle(image_base64))
    print(handle('https://jiujiuchat.oss-cn-chengdu.aliyuncs.com/test.png'))
# 通用识别
# 通用OCR
# action=OCRNormal, version=2020-08-26
# 多语种OCR
# action=MultiLanguageOCR, version=2022-08-31

# 个人卡证
# 银行卡OCR
# action=BankCard, version=2020-08-26
# 身份证OCR
# action=IDCard, version=2020-08-26
# 驾驶证OCR
# action=DrivingLicense, version=2020-08-26
# 行驶证OCR
# action=VehicleLicense, version=2020-08-26
# 台胞证
# action=OcrTaibao, version=2021-08-23

# 财务票据
# 混贴报销
# action=OcrFinance, version=2021-08-23
# 出租车票OCR
# action=OcrTaxiInvoice, version=2020-08-26
# 火车票OCR
# action=OcrTrainTicket, version=2020-08-26
# 行程单OCR
# action=OcrFlightInvoice, version=2020-08-26
# 增值税发票OCR
# action=OcrVatInvoice, version=2020-08-26
# 定额发票OCR
# action=OcrQuotaInvoice, version=2020-08-26
# 高速公路过路费
# action=OcrPassInvoice, version=2021-08-23

# 资质证书
# 食品生产许可证
# action=OcrFoodProduction, version=2021-08-23
# 食品经营许可证
# action=OcrFoodBusiness, version=2020-08-26
# 营业执照OCR
# action=OcrClueLicense, version=2020-08-26
# 商标证
# action=OCRTrade, version=2020-12-21
# 软件著作权
# action=OCRRuanzhu, version=2020-12-21
# 化妆品生产许可证
# action=OCRCosmeticProduct, version=2020-12-21

# 行业文档
# 印章识别
# action=OcrSeal, version=2021-08-23
# 合同校验
# action=OcrTextAlignment, version=2021-08-23
# 表格识别
# action=OCRTable, version=2021-08-23
