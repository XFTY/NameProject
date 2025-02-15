package com.nameproject.nameproject5At;

import org.apache.http.HttpEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.json.JSONObject;

import java.io.IOException;

public class Updater {

    public static JSONObject fetchJsonFromGitHub(String url) throws IOException {
        CloseableHttpClient httpClient = HttpClients.createDefault();
        HttpGet request = new HttpGet(url);

        try (CloseableHttpResponse response = httpClient.execute(request)) {
            // 获取响应实体
            HttpEntity entity = response.getEntity();
            if (entity != null) {
                // 将响应内容转换为字符串
                String result = EntityUtils.toString(entity);
                // 将字符串解析为JSONObject
                return new JSONObject(result);
            }
        }
        return null;
    }

    public static void main(String[] args) {
        String githubUrl = "https://your-github-username.github.io/your-json-file.json";
        try {
            JSONObject json = fetchJsonFromGitHub(githubUrl);
            System.out.println(json.toString(2)); // 以格式化的方式打印JSON
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}