class iOSTranslatePattern:

    # search文件名称后缀
    ios_suffix = [".m"]
    ios_special_str_list = ["%@", '\\"']

    # 正则表达式
    patten_localized_suffix = ',[ ]*@"[\s\S]*?"\)'
    # ObjectC 包含中文的字符串，未本地化
    pattern_oc__no_localized_chinese_str = '(?<!\()@"[^"]*?[\u4E00-\u9FA5][^"]*?"'
    # ObjectC 包含中文的字符串，未本地化  特殊，不处理的情况  例如static
    pattern_oc__static_str = "static [\s\S]*?;\n"
    # ObjectC 包含中文的字符串，未本地化  特殊，不处理的情况  例如NSString * const
    pattern_oc__const_str = "NSString[ ]*\*[ ]*const[\s\S]*?;\n"
    # ObjectC 包含中文的字符串 并使用 NSLocalizedString本地化
    pattern_oc__nslocalized_str = (
        'NSLocalizedString\(@"[^"]*?[\u4E00-\u9FA5][^"]*?".*?\)'
    )

    # 过滤掉不需要翻译的代码的正则
    def pattern_no_filter_str(auto_string_define_str: str):
        return f'{auto_string_define_str}\(@"[^"]*?[\u4E00-\u9FA5][^"]*?".*? *, *NO *\)'

    # 过滤掉埋点相关代码的正则
    pattern_filter_track_str = "\[TDFAnalyticsSDK.share[\s\S]*?\];"
    # 过滤掉路由相关代码的正则
    pattern_filter_router_str = '@"tdf-manager:[^"]*?[\u4E00-\u9FA5][^"]*?"|@"tdf-flutter:[^"]*?[\u4E00-\u9FA5][^"]*?"|@"tdf-ccd:[^"]*?[\u4E00-\u9FA5][^"]*?"|@"YunCash:[^"]*?[\u4E00-\u9FA5][^"]*?"'
