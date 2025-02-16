
package com.nameproject.nameproject5At;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.logging.HttpLoggingInterceptor;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

public class Updater {
    OkHttpClient client;

    public Updater() {
        // 设置 User-Agent
        String userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577";

        // 创建日志拦截器
        HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
        logging.setLevel(HttpLoggingInterceptor.Level.BASIC); // 或 Level.BODY 查看完整日志

        // 创建 OkHttpClient 并添加拦截器
        client = new OkHttpClient.Builder()
                .addInterceptor(logging)
                .addInterceptor(chain -> {
                    Request originalRequest = chain.request();
                    Request requestWithUserAgent = originalRequest.newBuilder()
                            .header("User-Agent", userAgent)
                            .build();
                    return chain.proceed(requestWithUserAgent);
                })
                .build();
    }

    public String run(String url) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .build();

        try (Response response = client.newCall(request).execute()) {
            return response.body().string();
        }
    }

    public List<String> getLatestReleaseDownloadUrls(String repoUrl) throws IOException {
        String jsonResponse = run(repoUrl);
        JSONObject jsonObject = new JSONObject(jsonResponse);
        JSONArray assets = jsonObject.getJSONArray("assets");
        List<String> downloadUrls = new ArrayList<>();
        for (int i = 0; i < assets.length(); i++) {
            JSONObject asset = assets.getJSONObject(i);
            downloadUrls.add(asset.getString("browser_download_url"));
        }
        return downloadUrls;
    }

    public ReleaseInfo getLatestReleaseInfo(String repoUrl) throws IOException {
        String jsonResponse = run(repoUrl);
        JSONObject jsonObject = new JSONObject(jsonResponse);
        JSONArray assets = jsonObject.getJSONArray("assets");
        List<String> downloadUrls = new ArrayList<>();
        for (int i = 0; i < assets.length(); i++) {
            JSONObject asset = assets.getJSONObject(i);
            downloadUrls.add(asset.getString("browser_download_url"));
        }
        String title = jsonObject.getString("name");
        String body = jsonObject.getString("body");
        return new ReleaseInfo(title, body, downloadUrls);
    }

    public List<String> getLatestPrereleaseDownloadUrls(String repoUrl) throws IOException {
        String jsonResponse = run(repoUrl);
        JSONArray jsonArray = new JSONArray(jsonResponse);
        List<String> downloadUrls = new ArrayList<>();
        JSONObject latestPrerelease = null;

        for (int i = 0; i < jsonArray.length(); i++) {
            JSONObject jsonObject = jsonArray.getJSONObject(i);
            if (jsonObject.getBoolean("prerelease")) {
                Instant currentPublishedAt = Instant.parse(jsonObject.getString("published_at"));
                if (latestPrerelease == null || Instant.parse(latestPrerelease.getString("published_at")).isBefore(currentPublishedAt)) {
                    latestPrerelease = jsonObject;
                }
            }
        }

        if (latestPrerelease != null) {
            JSONArray assets = latestPrerelease.getJSONArray("assets");
            for (int j = 0; j < assets.length(); j++) {
                JSONObject asset = assets.getJSONObject(j);
                downloadUrls.add(asset.getString("browser_download_url"));
            }
        }

        return downloadUrls;
    }

    public ReleaseInfo getLatestPrereleaseInfo(String repoUrl) throws IOException {
        String jsonResponse = run(repoUrl);
        JSONArray jsonArray = new JSONArray(jsonResponse);
        JSONObject latestPrerelease = null;

        for (int i = 0; i < jsonArray.length(); i++) {
            JSONObject jsonObject = jsonArray.getJSONObject(i);
            if (jsonObject.getBoolean("prerelease")) {
                Instant currentPublishedAt = Instant.parse(jsonObject.getString("published_at"));
                if (latestPrerelease == null || Instant.parse(latestPrerelease.getString("published_at")).isBefore(currentPublishedAt)) {
                    latestPrerelease = jsonObject;
                }
            }
        }

        if (latestPrerelease != null) {
            JSONArray assets = latestPrerelease.getJSONArray("assets");
            List<String> downloadUrls = new ArrayList<>();
            for (int j = 0; j < assets.length(); j++) {
                JSONObject asset = assets.getJSONObject(j);
                downloadUrls.add(asset.getString("browser_download_url"));
            }
            String title = latestPrerelease.getString("name");
            String body = latestPrerelease.getString("body");
            return new ReleaseInfo(title, body, downloadUrls);
        }

        return null;
    }

    public List<String> getAllPrereleaseDownloadUrls(String repoUrl) throws IOException {
        String jsonResponse = run(repoUrl);
        JSONArray jsonArray = new JSONArray(jsonResponse);
        List<String> downloadUrls = new ArrayList<>();
        for (int i = 0; i < jsonArray.length(); i++) {
            JSONObject jsonObject = jsonArray.getJSONObject(i);
            if (jsonObject.getBoolean("prerelease")) {
                JSONArray assets = jsonObject.getJSONArray("assets");
                for (int j = 0; j < assets.length(); j++) {
                    JSONObject asset = assets.getJSONObject(j);
                    downloadUrls.add(asset.getString("browser_download_url"));
                }
            }
        }
        return downloadUrls;
    }

    public static void main(String[] args) {
        Updater fetcher = new Updater();
        try {
            ReleaseInfo latestReleaseInfo = fetcher.getLatestReleaseInfo("https://api.github.com/repos/XFTY/NameProject/releases/latest");
            if (latestReleaseInfo != null) {
                System.out.println("Latest Release Title: " + latestReleaseInfo.getTitle());
                System.out.println("Latest Release Body: " + latestReleaseInfo.getBody());
                System.out.println("Latest Release Download URLs:");
                for (String url : latestReleaseInfo.getDownloadUrls()) {
                    System.out.println(url);
                }
            }

            ReleaseInfo latestPrereleaseInfo = fetcher.getLatestPrereleaseInfo("https://api.github.com/repos/XFTY/NameProject/releases");
            if (latestPrereleaseInfo != null) {
                System.out.println("Latest Prerelease Title: " + latestPrereleaseInfo.getTitle());
                System.out.println("Latest Prerelease Body: " + latestPrereleaseInfo.getBody());
                System.out.println("Latest Prerelease Download URLs:");
                for (String url : latestPrereleaseInfo.getDownloadUrls()) {
                    System.out.println(url);
                }
            }

            System.out.println("done");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class ReleaseInfo {
        private final String title;
        private final String body;
        private final List<String> downloadUrls;

        public ReleaseInfo(String title, String body, List<String> downloadUrls) {
            this.title = title;
            this.body = body;
            this.downloadUrls = downloadUrls;
        }

        public String getTitle() {
            return title;
        }

        public String getBody() {
            return body;
        }

        public List<String> getDownloadUrls() {
            return downloadUrls;
        }
    }
}