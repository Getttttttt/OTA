#include <WiFi.h>

#include <HTTPClient.h>
#include <ESP32httpUpdate.h>
#include <Arduino_JSON.h>

/**********根据实际修改**********/
const char* wifi_ssid = "TP-LINK_1760"; // WIFI名称，区分大小写
const char* wifi_password = "987654321"; // WIFI密码

// 特别重要，升级依据！！！
// 设置当前代码版本 格式 1_0_0
char* version = "1_0_0";

//远程固件链接，只支持http
const char* baseUpdateUrl = "http://192.168.56.1:5500/esp32/";
const char* updateJson = "http://192.168.56.1:5500/esp32/esp32_update.json";


// esp32_update.json
// {
//     "version":"1_0_1"
// }

/**********根据实际修改**********/


int need_ota_update = 0;
int i = 0;
String jsonBuffer;


// 获取远程 json 升级文件
String httpGETRequest(const char* serverName) {
 WiFiClient client;
 HTTPClient http;
 String payload = "";
 //连接目标网址
  http.begin(client, serverName);
 //发送HTTP站点请求
 int httpCode = http.GET();
 if (httpCode > 0) {
 Serial.printf("[HTTP] GET... code: %d\n", httpCode);
    payload = http.getString();
 } else {
 Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
 }

  http.end(); //关闭连接
 //返回获得的数据用于Json处理
 return payload;
}

// 依据json文件中版本号与本地版本号，判断是否需要进行更新
void isOrNotNeedUpdate(){
 // 获取远程的升级 json ，判断内部版本与本地是否相同，判断是否需要升级
  jsonBuffer = httpGETRequest(updateJson);
 Serial.println(jsonBuffer);
 //将解析的Json对象值储存在Jsonu缓冲区中
 JSONVar myObject = JSON.parse(jsonBuffer);
 Serial.println(myObject);
 // Serial.println(myObject["version"]);
 const char* ota_version = myObject["version"];
 // Serial.println(ota_version);

 Serial.println("---");

 Serial.print("远程版本： ");
 Serial.println(ota_version);
 Serial.print("本地版本： ");
 Serial.println(version);
 // char * 与 const char * 比较
 // 判断远程版本与本地版本是否相同
 if (String(version) == String(ota_version)) {
    need_ota_update = 0;
 Serial.println("无需升级。。。");

 } else {
    need_ota_update = 1;
 Serial.println("需要升级。。。");
 Serial.print("OTA 升级地址为：");
 // 升级的完整链接， 例如：http://example.cn/esp32/esp32_1_0_1.bin
 String fullUpdateUrl = String(baseUpdateUrl) + "esp32_" + ota_version + ".bin";
 Serial.println(String(fullUpdateUrl));


 // 获取远程 bin 文件进行升级
    t_httpUpdate_return ret = ESPhttpUpdate.update(fullUpdateUrl);
 Serial.println(ret);
 switch (ret) {
 case HTTP_UPDATE_FAILED:
 Serial.printf("HTTP_UPDATE_FAILED Error (%d): %s\n", ESPhttpUpdate.getLastError(), ESPhttpUpdate.getLastErrorString().c_str());
 break;
 case HTTP_UPDATE_NO_UPDATES:
 Serial.println("HTTP_UPDATE_NO_UPDATES");
 break;
 case HTTP_UPDATE_OK:
 Serial.println("HTTP_UPDATE_OK");
 break;
 default:
 Serial.println(ret);
 }
 // version=(char *)ota_version;
 }
  need_ota_update = 0;
}

void setup() {
 Serial.begin(115200); //波特率115200
 Serial.print("Connection WIFI");
 WiFi.begin(wifi_ssid, wifi_password); //连接wifi
 while (WiFi.status() != WL_CONNECTED) { //等待连接wifi
    delay(500);
 Serial.print(".");
 }
 Serial.println("");
 // 调用判断是否需要升级函数
  isOrNotNeedUpdate();
}

void loop() {
// 主程序
 Serial.println(i);
 Serial.println("OTA 升级成功");
  i++;
  delay(2000);
}