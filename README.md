# UIAutoTest

## 框架介绍
本框架主要是基于 Python + pytest + unittest + allure + log + yaml + mysql + 企业微信通知 + Jenkins 实现的UI自动化框架。
git地址：https://github.com/sbscxylx/auto_test
项目参与者: 李鑫


## 实现功能
* 支持自动生成测试用例模板yaml文件
* 支持测试人员在yaml文件中填写好测试用例, 程序可以直接生成用例模板，减少重复操作
* 支持用yaml文件存放测试用例数据，实现数据驱动
* 支持jenkins执行测试用例
* 支持查看用例log日志和失败截图  
* 支持用例运行情况用企业微信推送
* 支持查看allure报告



## 目录结构

    ├─Comm                                      // 工具
    │  │  allure_report_data.py                 // allure 报告数据清洗，提取业务需要得数据
    │  │  case_automatic_control.py             // 自动生成测试用例py模板
    │  │  case_yaml_auto.py                     // 自动生成测试用例yaml模板
    │  │  data.py                               // excel, csv调用方法
    │  │  get_local_ip.py                       // 获取本机ip
    │  │  get_path.py                           // 获取文件路径/目录/文件
    │  │  HTMLTestReportCN.py                   // html测试报告模板
    │  │  html_test_runner.py                   // unittest方式运行所有用例
    │  │  log.py                                // 日志生成方法
    │  │  mysql_backup.py                       // 数据库连接/备份
    │  │  testcase_template.py                  // 生成模板的基准方法
    │  │  time_control.py                       // 时间类方法
    │  │  wechat_send.py                        // 企业微信推送
    │  │  __init__.py
    ├─Conf                                      // 配置
    │  │  config.yaml                           // 基本配置
    │  │  exceptions.py                         // 错误
    │  │  models.py                             // 模型
    │  │  readconfig.py                         // 读取ini的方法
    │  │  yaml_control.py                       // 读取yaml文件的方法
    │  │  __init__.py 
    ├─data                                      // 用例yaml文件存放位置
    │  │  __init__.py
    │  │  
    │  └─collect                                
    │          collect_addtool.yaml
    │          collect_edittool.yaml
    ├─IemsPage                                  // 页面逻辑存放
    │  │  basePage.py                           // 重写driver方法，方便调用
    │  │  __init__.py

    │  ├─iems_eqp                               // 设备页面逻辑方法
    │  │  │  iems_eqp.py
    │  │  │  __init__.py
    │          
    ├─IemsTestcase                              // 执行用例存放位置
    │  │  __init__.py
    │  │  
    │  ├─a                                      // 生产环境用例
    │  │  │  __init__.py
    │  │  │  
    │  │  ├─iems_eqp
    │  │  │  │  test_iems_eqp_a.py
    │  │  │  │  __init__.py
    │  │          
    │  ├─sit                                    // 测试环境用例
    │  │  │  __init__.py
    │  │  │      
    │  │  ├─iems_eqp
    │  │  │  │  test_iems_eqp_sit.py
    │  │  │  │  __init__.py
    │          
    ├─Log                                       
    │  ├─log                                    // 日志存放位置
    │  │      log_2022-09-231059.txt
    │  │      
    │  └─screen                                 // 用例失败截图存放位置
    │      └─2022-09-2110
    │              2022-09-21102200失败截图.png
    │              2022-09-21105042失败截图.png
    │              
    ├─Results                                                           // 测试报告存放位置
    │  ├─allure_reports                                                 // allure报告存放位置
    │  │      090a1391-dbe3-4272-9c5a-b2e4f5a0f5a8-container.json
    │  │      337360db-0fd9-43ba-ae9e-bcbe4830dde6-result.json
    │  │      3440508c-3143-4542-8391-2fc4f9693a8d-attachment.png
    │  │      60cf33d4-969a-4d93-bc81-c8d150384d3c-attachment.txt
    │  │      c46a83ff-a51a-427a-8f76-c541348cf8d3-attachment.txt
    │  │      f56348e1-8726-4613-a895-49da61368cfb-result.json
    │  │          
    │  └─reports                                                        // html报告存放位置
    │          iems-reports2022-02-23_09-41-20.html
    │          
    ├─Runner                                                            // unittest执行
    │  │  main.py
    │  │  send_email.py
    │  │  test_runner.py
    │  │  __init__.py
    │  APITestFrame.png
    │  APITestFrame.xmind
    │  failures
    │  pytest.ini
    │  README.md
    │  requirements.txt
    │  run.py                                                           // pyrun
    │  UITestFrame.pdf
    │  UITestFrame.png
    │  UITestFrame.xmind
    │  __init__.py
    │  自动化测试方案.docx
        
## 实现逻辑
C:\Users\Administrator\Desktop\UIAutoTest\自动化测试方案.docx